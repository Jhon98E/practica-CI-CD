from fastapi.testclient import TestClient
from src.main import app, APIResponse
import requests
import pytest

client = TestClient(app)

def _mock_response(status_code=200, json_data=None):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data or {{}}

        def json(self):
            return self._json_data
    return MockResponse(status_code, json_data)

def test_create_user_success(monkeypatch):
    def mock_post(url, json, timeout):
        return _mock_response(200, {"name": "admin", "code": 1, "state": True})
    monkeypatch.setattr(requests, "post", mock_post)

    response = client.post("/create_user", json={"name": "admin"})
    assert response.status_code == 201
    expected = APIResponse(success=True, detail="Usuario creado correctamente", data={"name": "admin", "code": 1, "state": True}).dict()
    assert response.json() == expected

def test_create_user_disabled(monkeypatch):
    def mock_post(url, json, timeout):
        return _mock_response(200, {"name": "user", "code": 3, "state": False})
    monkeypatch.setattr(requests, "post", mock_post)

    response = client.post("/create_user", json={"name": "user"})
    assert response.status_code == 400
    assert response.json() == {"detail": "El usuario está desactivado"}

def test_create_user_remote_502(monkeypatch):
    def mock_post(url, json, timeout):
        return _mock_response(500, {"error": "server error"})
    monkeypatch.setattr(requests, "post", mock_post)

    response = client.post("/create_user", json={"name": "admin"})
    assert response.status_code == 502
    assert "Error al comunicarse" in response.json()["detail"]

def test_create_user_request_exception(monkeypatch):
    def mock_post(url, json, timeout):
        raise requests.Timeout("timeout")
    monkeypatch.setattr(requests, "post", mock_post)

    response = client.post("/create_user", json={"name": "admin"})
    assert response.status_code == 502
    assert "timeout" in response.json()["detail"]
