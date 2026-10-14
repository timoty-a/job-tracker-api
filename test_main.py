import pytest
from fastapi.testclient import TestClient

from main import app, applications


client = TestClient(app)

INITIAL_APPLICATIONS = [
    {
        "id": 1,
        "company": "Paystack",
        "role": "Backend Engineering Intern",
        "status": "applied"
    },
    {
        "id": 2,
        "company": "Flutterwave",
        "role": "Junior Backend Engineer",
        "status": "interview"
    }
]


@pytest.fixture(autouse=True)
def reset_applications():
    applications.clear()
    applications.extend(
        application.copy()
        for application in INITIAL_APPLICATIONS
    )


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API is running"
    }


def test_get_all_applications():
    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_one_application():
    response = client.get("/applications/1")

    assert response.status_code == 200
    assert response.json()["company"] == "Paystack"


def test_get_missing_application():
    response = client.get("/applications/99")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Moniepoint",
            "role": "Backend Intern",
            "status": "applied"
        }
    )

    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["company"] == "Moniepoint"


def test_reject_invalid_status():
    response = client.post(
        "/applications",
        json={
            "company": "Moniepoint",
            "role": "Backend Intern",
            "status": "whatever"
        }
    )

    assert response.status_code == 422


def test_update_application():
    response = client.patch(
        "/applications/1",
        json={"status": "offer"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "offer"


def test_delete_application():
    response = client.delete("/applications/2")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get("/applications/2")
    assert get_response.status_code == 404


def test_delete_missing_application():
    response = client.delete("/applications/99")

    assert response.status_code == 404