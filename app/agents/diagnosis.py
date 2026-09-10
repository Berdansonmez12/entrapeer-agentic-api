from enum import Enum

from pydantic import BaseModel, Field


class ProblemType(str, Enum):
    GROWTH = "growth"
    COST = "cost"
    OPERATIONAL = "operational"
    TECHNOLOGY = "technology"
    REGULATION = "regulation"
    ORGANIZATIONAL = "organizational"
    HYBRID = "hybrid"


class ProblemSubCause(BaseModel):
    name: str = Field(
        ...,
        description="A specific sub-cause contributing to a main cause.",
    )
    explanation: str = Field(
        ...,
        description="A concise explanation of how this sub-cause contributes to the problem.",
    )


class ProblemMainCause(BaseModel):
    name: str = Field(
        ...,
        description="A main cause contributing to the identified business problem.",
    )
    sub_causes: list[ProblemSubCause] = Field(
        ...,
        min_length=2,
        max_length=3,
        description="Two to three sub-causes supporting this main cause.",
    )


class DiagnosisResult(BaseModel):
    problem_type: ProblemType
    main_problem: str
    main_causes: list[ProblemMainCause] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="Three to five main causes forming the structured problem tree.",
    )

class ProblemStructuringDiagnosisAgent:
    """
    Agent responsible for diagnosing an already discovered business problem
    and converting it into a structured problem tree.
    """

    def __init__(self, llm):
        self.llm = llm

    async def diagnose(
        self,
        discovery_handoff: dict[str, str],
    ) -> DiagnosisResult:
        """
        Diagnose the business problem using only the discovery handoff.
        This agent must not ask the customer additional questions.
        """
        structured_llm = self.llm.with_structured_output(DiagnosisResult)

        system_prompt = """
        You are the Problem Structuring & Diagnosis Agent in a business-focused
        agentic system.

        You receive a completed handoff from the Business Sense Discovery Agent.
        Your job is to diagnose and structure the business problem using only
        the information already collected during discovery.

        STRICT RULES:
        1. Do not ask the customer any new questions.
        2. Do not invent facts that are not supported by the discovery handoff.
        3. Classify the problem as exactly one of:
           growth, cost, operational, technology, regulation,
           organizational, or hybrid.
        4. Clearly state the main business problem.
        5. Build a structured problem tree with 3 to 5 main causes.
        6. Each main cause must contain 2 to 3 specific sub-causes.
        7. Treat causes as diagnostic hypotheses when the handoff does not
           provide enough evidence to establish them as facts.
        8. Keep the analysis business-focused, concise, and structured.
        """

        handoff_text = "\n".join(
            f"{key}: {value}"
            for key, value in discovery_handoff.items()
        )

        messages = [
            ("system", system_prompt),
            (
                "human",
                f"""
                Analyze the completed discovery handoff below and produce
                the structured diagnosis.

                Discovery Handoff:
                {handoff_text}
                """,
            ),
        ]

        return await structured_llm.ainvoke(messages)