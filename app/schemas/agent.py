from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class AgentExecuteRequest(BaseModel):
    task: str = Field(
        ...,
        min_length=1,
        description="The task or question to be handled by the agent system.",
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier used to preserve conversation state.",
    )

    @field_validator("task")
    @classmethod
    def validate_task(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Task must not be empty or contain only whitespace.")

        return cleaned_value

    def get_session_id(self) -> str:
        return self.session_id or str(uuid4())


class AgentExecuteResponse(BaseModel):
    status: str
    agent: str
    response: str
    session_id: str
    data: dict[str, Any] | None = None
    sources: list[dict[str, Any]] | None = None