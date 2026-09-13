from datetime import datetime, timezone
from typing import Any

from app.db.mongo import mongodb


class LoggingService:
    COLLECTION_NAME = "agent_logs"

    async def log(
        self,
        *,
        session_id: str,
        task: str,
        agent: str,
        status: str,
        response: str | None = None,
        data: dict[str, Any] | None = None,
        sources: list[dict[str, Any]] | None = None,
        error: str | None = None,
    ) -> None:
        log_entry = {
            "session_id": session_id,
            "task": task,
            "agent": agent,
            "status": status,
            "response": response,
            "data": data,
            "sources": sources or [],
            "error": error,
            "timestamp": datetime.now(timezone.utc),
        }

        try:
            database = mongodb.get_database()
            await database[self.COLLECTION_NAME].insert_one(log_entry)
        except Exception as exc:
            # Logging must never break the main agent workflow.
            print(
                f"[LOGGING WARNING] Failed to write MongoDB log "
                f"for session={session_id}: {exc}"
            )


logging_service = LoggingService()