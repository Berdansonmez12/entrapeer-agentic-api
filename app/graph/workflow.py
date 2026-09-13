from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver

from app.agents.peer import PeerAgent
from app.agents.discovery import BusinessSenseDiscoveryAgent
from app.agents.diagnosis import ProblemStructuringDiagnosisAgent
from app.graph.state import AgentState
from app.services.llm_service import LLMService


llm_service = LLMService()
llm = llm_service.get_model()

peer_agent = PeerAgent(llm)
discovery_agent = BusinessSenseDiscoveryAgent(llm)
diagnosis_agent = ProblemStructuringDiagnosisAgent(llm)

def prepare_conversation_node(state: AgentState) -> dict:
    """
    Add the latest user message to the discovery conversation.
    """
    conversation = list(state.get("conversation", []))

    if not conversation:
        conversation.append(
            {
                "role": "user",
                "content": state["task"],
            }
        )
    elif conversation[-1]["content"] != state["task"]:
        conversation.append(
            {
                "role": "user",
                "content": state["task"],
            }
        )

    return {
        "conversation": conversation,
    }

async def peer_node(state: AgentState) -> dict:
    """
    Classify the incoming task and store the routing decision in the graph state.
    """
    decision = await peer_agent.classify(state["task"])

    return {
        "route": decision.route.value,
        "routing_reasoning": decision.reasoning,
        "current_agent": "peer_agent",
        "status": "routing_complete",
    }


async def discovery_node(state: AgentState) -> dict:
    """
    Continue business discovery and either ask the next question
    or prepare a structured handoff for diagnosis.
    """
    conversation = state.get("conversation", [])

    if not conversation:
        conversation = [
            {
                "role": "user",
                "content": state["task"],
            }
        ]

    decision = await discovery_agent.discover(conversation)

    if not decision.is_discovery_complete:
        conversation.append(
    {
        "role": "assistant",
        "content": decision.next_question.question,
    }
        )
        return {
            "conversation": conversation,
            "current_agent": "business_sense_discovery_agent",
            "response": decision.next_question.question,
            "discovery_complete": False,
            "status": "awaiting_user_input",
        }

    return {
        "conversation": conversation,
        "current_agent": "business_sense_discovery_agent",
        "discovery_complete": True,
        "discovery_handoff": decision.handoff.model_dump(),
        "status": "discovery_complete",
    }


async def diagnosis_node(state: AgentState) -> dict:
    """
    Build a structured problem diagnosis from the discovery handoff.
    """
    handoff = state["discovery_handoff"]

    result = await diagnosis_agent.diagnose(handoff)

    return {
        "current_agent": "problem_structuring_diagnosis_agent",
        "diagnosis": result.model_dump(),
        "response": result.model_dump_json(indent=2),
        "status": "completed",
    }

def route_after_prepare(state: AgentState) -> str:
    """
    Continue an active discovery session without reclassifying
    the user's follow-up answer through Peer Agent.
    """
    if (
        state.get("status") == "awaiting_user_input"
        and state.get("route") == "business_problem"
    ):
        return "discovery"

    return "peer"


def route_after_peer(state: AgentState) -> str:
    """
    Decide which workflow branch should run after Peer Agent classification.
    """
    route = state["route"]

    if route == "business_problem":
        return "discovery"

    return "unsupported"


def route_after_discovery(state: AgentState) -> str:
    """
    Decide whether discovery should stop for user input
    or continue to diagnosis.
    """
    if state.get("discovery_complete"):
        return "diagnosis"

    return "end"


workflow = StateGraph(AgentState)

workflow.add_node("prepare_conversation", prepare_conversation_node)
workflow.add_node("peer", peer_node)
workflow.add_node("discovery", discovery_node)
workflow.add_node("diagnosis", diagnosis_node)
workflow.add_edge(START, "prepare_conversation")
workflow.add_conditional_edges(
    "prepare_conversation",
    route_after_prepare,
    {
        "peer": "peer",
        "discovery": "discovery",
    },
)

workflow.add_conditional_edges(
    "peer",
    route_after_peer,
    {
        "discovery": "discovery",
        "unsupported": END,
    },
)


workflow.add_conditional_edges(
    "discovery",
    route_after_discovery,
    {
        "diagnosis": "diagnosis",
        "end": END,
    },
)

workflow.add_edge("diagnosis", END)


memory = InMemorySaver()

graph = workflow.compile(checkpointer=memory)