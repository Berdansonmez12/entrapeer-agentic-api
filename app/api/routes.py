from fastapi import APIRouter, HTTPException

from app.graph.workflow import graph
from app.schemas.agent import AgentExecuteRequest, AgentExecuteResponse


router = APIRouter(prefix="/v1/agent", tags=["agent"])


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute_agent(
    request: AgentExecuteRequest,
) -> AgentExecuteResponse:
    """
    Execute a user task through the LangGraph agent workflow.
    """
    session_id = request.get_session_id()

    config = {
        "configurable": {
            "thread_id": session_id,
        }
    }

    try:
        result = await graph.ainvoke(
            {
                "task": request.task,
            },
            config=config,
        )

        return AgentExecuteResponse(
            status=result.get("status", "completed"),
            agent=result.get("current_agent", "peer_agent"),
            response=result.get(
                "response",
                "The request was processed but no response was generated.",
            ),
            session_id=session_id,
            data=result.get("data") or result.get("diagnosis"),
            sources=result.get("sources"),
        )

    except Exception as exc:
        print(
            f"Agent execution failed "
            f"[session_id={session_id}]: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed.",
        ) from exc