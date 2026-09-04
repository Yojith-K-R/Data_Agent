from fastapi.testclient import TestClient

from data_agent.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}