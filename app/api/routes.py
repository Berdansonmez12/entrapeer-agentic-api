from fastapi import APIRouter

from app.schemas.agent import AgentExecuteRequest, AgentExecuteResponse


router = APIRouter(prefix="/v1/agent", tags=["agent"])


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute_agent(request: AgentExecuteRequest) -> AgentExecuteResponse:
    return AgentExecuteResponse(
        status="success",
        agent="peer_agent",
        response=f"Task received: {request.task}",
        data=None,
    )