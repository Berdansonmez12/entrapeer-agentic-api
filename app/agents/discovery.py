from pydantic import BaseModel, Field


class DiscoveryQuestion(BaseModel):
    question: str = Field(
        ...,
        description="A business discovery question to ask the customer.",
    )
    purpose: str = Field(
        ...,
        description="Why this question is important for understanding the business problem.",
    )


class DiscoveryHandoff(BaseModel):
    customer_stated_problem: str
    identified_business_problem: str
    hidden_root_risk: str
    customer_chat_summary: str


class DiscoveryDecision(BaseModel):
    is_discovery_complete: bool
    next_question: DiscoveryQuestion | None = None
    handoff: DiscoveryHandoff | None = None
class BusinessSenseDiscoveryAgent:
    """
    Agent responsible for understanding the customer's real business problem
    through an adaptive discovery conversation before any diagnosis or solution.
    """

    MIN_MAIN_QUESTIONS = 3

    def __init__(self, llm):
        self.llm = llm

    async def discover(
        self,
        conversation: list[dict[str, str]],
    ) -> DiscoveryDecision:
        """
        Continue the discovery conversation or produce a structured handoff
        when enough information has been collected.
        """
        questions_asked = sum(
            1
            for message in conversation
            if message["role"] == "assistant"
        )
        structured_llm = self.llm.with_structured_output(DiscoveryDecision)

        system_prompt = f"""
        You are the Business Sense Discovery Agent in a business-focused
        agentic system.

        Your responsibility is to understand the customer's real business
        problem before any diagnosis or solution is produced.

        DISCOVERY GOALS:
        1. Clarify the customer's stated problem.
        2. Distinguish the customer's actual business need from a requested
           or assumed solution.
        3. Identify important context, previous attempts, and hidden risks.

        DISCOVERY RULES:
        - Ask one clear question at a time.
        - Ask at least {self.MIN_MAIN_QUESTIONS} meaningful main questions
          before completing discovery.
        - Adapt follow-up questions based on the customer's previous answers.
        - Focus on topics such as:
          * the main operational or business problem,
          * affected department or process,
          * when the problem started,
          * current way of handling the problem,
          * whether the customer wants a solution or first wants to
            understand the cause,
          * previous attempts and why they failed,
          * visibility, measurement, or data gaps.
        - Do not provide a solution.
        - Do not diagnose the problem during discovery.
        - Do not build a problem tree.
        - Do not invent information that the customer has not provided.
        - Avoid repeating questions already answered in the conversation.

        COMPLETION RULES:
        - If discovery is not complete, set is_discovery_complete to false,
          provide exactly one next_question, and set handoff to null.
        - If discovery is complete, set is_discovery_complete to true,
          set next_question to null, and provide a handoff containing:
          customer_stated_problem,
          identified_business_problem,
          hidden_root_risk,
          customer_chat_summary.
        - Preserve all critical customer information in customer_chat_summary.
        """

        conversation_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation
        )

        messages = [
            ("system", system_prompt),
            (
                "human",
                f"""
                Review the discovery conversation below and decide whether
                discovery should continue or a structured handoff can be made.

                Conversation:
                {conversation_text}
                """,
            ),
        ]

        result = await structured_llm.ainvoke(messages)

        if questions_asked < self.MIN_MAIN_QUESTIONS and result.is_discovery_complete:
            result.is_discovery_complete = False
            result.handoff = None

            if result.next_question is None:
                result.next_question = DiscoveryQuestion(
                    question="What additional information would help clarify the underlying business problem?",
                    purpose="Ensure that enough discovery has been completed before diagnosis.",
                )

        return result