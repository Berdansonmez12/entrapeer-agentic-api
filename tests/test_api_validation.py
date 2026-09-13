from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_empty_task_is_rejected():
    response = client.post(
        "/v1/agent/execute",
        json={
            "task": "     ",
            "session_id": "pytest-empty-task",
        },
    )

    assert response.status_code == 422

    response_body = response.json()
    assert response_body["detail"][0]["loc"] == ["body", "task"]
    assert "Task must not be empty" in response_body["detail"][0]["msg"]