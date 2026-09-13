from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state passed between agents in the LangGraph workflow.
    """

    session_id: str
    task: str

    conversation: list[dict[str, str]]

    route: str
    routing_reasoning: str
    current_agent: str

    response: str

    discovery_complete: bool
    discovery_handoff: dict[str, str] | None

    diagnosis: dict[str, Any] | None

    sources: list[dict[str, str]]

    status: str
    error: str | None