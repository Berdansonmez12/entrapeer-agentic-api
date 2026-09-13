from fastapi import APIRouter, HTTPException

from app.graph.workflow import graph
from app.schemas.agent import AgentExecuteRequest, AgentExecuteResponse
from app.services.logging_service import logging_service
from app.workers.tasks import execute_agent_task


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

        status = result.get("status", "completed")
        agent = result.get("current_agent", "peer_agent")
        response = result.get(
            "response",
            "The request was processed but no response was generated.",
        )
        data = result.get("data") or result.get("diagnosis")
        sources = result.get("sources")

        await logging_service.log(
            session_id=session_id,
            task=request.task,
            agent=agent,
            status=status,
            response=response,
            data=data,
            sources=sources,
        )

        return AgentExecuteResponse(
            status=status,
            agent=agent,
            response=response,
            session_id=session_id,
            data=data,
            sources=sources,
        )

    except Exception as exc:
        print(
            f"Agent execution failed "
            f"[session_id={session_id}]: {exc}"
        )

        await logging_service.log(
            session_id=session_id,
            task=request.task,
            agent="unknown",
            status="failed",
            error=str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed.",
        ) from exc

@router.post("/queue")
async def queue_agent_task(
    request: AgentExecuteRequest,
) -> dict:
    """
    Submit an agent task to the Redis-backed Celery queue.
    """
    session_id = request.get_session_id()

    try:
        queued_task = execute_agent_task.delay(
            request.task,
            session_id,
        )

        return {
            "status": "queued",
            "task_id": queued_task.id,
            "session_id": session_id,
        }

    except Exception as exc:
        print(
            f"Queue submission failed "
            f"[session_id={session_id}]: {exc}"
        )

        raise HTTPException(
            status_code=503,
            detail="Task queue is unavailable.",
        ) from exc