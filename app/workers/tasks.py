import asyncio
from uuid import uuid4

from app.graph.workflow import graph
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.execute_agent_task")
def execute_agent_task(task: str, session_id: str | None = None) -> dict:
    """Execute an agent request asynchronously through the Celery worker."""

    resolved_session_id = session_id or str(uuid4())

    async def run_graph() -> dict:
        result = await graph.ainvoke(
            {"task": task},
            config={
                "configurable": {
                    "thread_id": resolved_session_id,
                }
            },
        )

        return {
            "status": result.get("status", "completed"),
            "agent": result.get("current_agent", "peer_agent"),
            "response": result.get(
                "response",
                "The request was processed but no response was generated.",
            ),
            "session_id": resolved_session_id,
            "data": result.get("data") or result.get("diagnosis"),
            "sources": result.get("sources"),
        }

    return asyncio.run(run_graph())