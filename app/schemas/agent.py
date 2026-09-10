from typing import Any

from pydantic import BaseModel, Field


class AgentExecuteRequest(BaseModel):
    task: str = Field(
        ...,
        min_length=1,
        description="The task or question to be handled by the agent system.",
    )


class AgentExecuteResponse(BaseModel):
    status: str
    agent: str
    response: str
    data: dict[str, Any] | None = None