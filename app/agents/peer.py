from enum import Enum

from pydantic import BaseModel


class TaskRoute(str, Enum):
    BUSINESS_INFORMATION = "business_information"
    BUSINESS_PROBLEM = "business_problem"
    CODE = "code"
    CONTENT = "content"
    NON_BUSINESS = "non_business"


class PeerRoutingDecision(BaseModel):
    route: TaskRoute
    reasoning: str

class PeerAgent:
    """
Entry-point agent responsible for understanding the user's request
and deciding which specialized agent should handle it.
"""

def __init__(self, llm):
    self.llm = llm

async def classify(self, task: str) -> PeerRoutingDecision:
    """
    Classify the incoming task into one of the supported routes.
    """
    structured_llm = self.llm.with_structured_output(PeerRoutingDecision)

    system_prompt = """
    You are the Peer Agent, the entry point of a business-focused agentic system.

    Classify the user's request into exactly one of these routes:

    - business_information:
      Questions asking for business information such as competitors,
      market trends, sector information, or company information.

    - business_problem:
      Requests describing a business problem that requires discovery
      and diagnosis, such as declining sales, increasing costs,
      operational inefficiency, or organizational problems.

    - code:
      Requests asking to write, explain, debug, or modify code.

    - content:
      Requests asking to create or modify written content.

    - non_business:
      Requests unrelated to business, code, or content.

    Important rules:
    - Do not solve the user's request.
    - Do not ask discovery questions.
    - Only classify the request.
    - Provide a short reasoning for the classification.
    """

    messages = [
        ("system", system_prompt),
        ("human", task),
    ]

    return await structured_llm.ainvoke(messages)