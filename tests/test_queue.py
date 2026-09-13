from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_queue_agent_task_returns_task_id():
    mock_result = MagicMock()
    mock_result.id = "test-task-id"

    with patch(
        "app.api.routes.execute_agent_task.delay",
        return_value=mock_result,
    ):
        response = client.post(
            "/v1/agent/queue",
            json={
                "task": "Analyze why our sales are declining.",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "queued"
    assert body["task_id"] == "test-task-id"
    assert body["session_id"]