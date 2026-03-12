from fastapi.testclient import TestClient

from edge_traffic.api.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info() -> None:
    client = TestClient(app)
    response = client.get("/info")
    assert response.status_code == 200
    body = response.json()
    assert "app_name" in body
    assert "environment" in body
    assert "api_port" in body
    assert "log_level" in body
