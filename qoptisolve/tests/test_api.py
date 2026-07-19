from fastapi.testclient import TestClient

from qoptisolve.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qaoa_endpoint():
    payload = {
        "graph": [
            {"source": 0, "target": 1, "weight": 1.0},
            {"source": 1, "target": 2, "weight": 2.0},
        ],
        "reps": 2,
        "shots": 1024,
        "backend": "simulator",
    }

    response = client.post("/optimize/qaoa", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["algorithm"] == "QAOA"
    assert data["status"] == "completed"
    assert data["optimal_value"] >= 0


def test_qaoa_invalid_payload():
    payload = {
        "graph": [],
        "reps": 2,
        "shots": 1024,
        "backend": "simulator",
    }

    response = client.post("/optimize/qaoa", json=payload)

    assert response.status_code == 422
