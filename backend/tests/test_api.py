from fastapi.testclient import TestClient

from data_agent.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_rejects_empty_question():
    response = client.post(
        "/api/v1/query",
        json={"question": ""},
    )

    assert response.status_code == 422