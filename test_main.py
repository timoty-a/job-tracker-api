import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


def create_test_application():
    return client.post(
        "/applications",
        json={
            "company": "Paystack",
            "role": "Backend Engineering Intern",
            "status": "applied"
        }
    )


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API is running"
    }


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == []


def test_create_application():
    response = create_test_application()
    data = response.json()

    assert response.status_code == 201
    assert data["company"] == "Paystack"
    assert data["role"] == "Backend Engineering Intern"
    assert data["status"] == "applied"
    assert isinstance(data["id"], int)


def test_get_application():
    created = create_test_application().json()

    response = client.get(f"/applications/{created['id']}")

    assert response.status_code == 200
    assert response.json()["company"] == "Paystack"


def test_get_missing_application():
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }


def test_reject_invalid_status():
    response = client.post(
        "/applications",
        json={
            "company": "Paystack",
            "role": "Backend Engineer",
            "status": "waiting"
        }
    )

    assert response.status_code == 422


def test_update_application():
    created = create_test_application().json()

    response = client.patch(
        f"/applications/{created['id']}",
        json={"status": "interview"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "interview"


def test_delete_application():
    created = create_test_application().json()

    response = client.delete(f"/applications/{created['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/applications/{created['id']}")
    assert get_response.status_code == 404


def test_delete_missing_application():
    response = client.delete("/applications/999")

    assert response.status_code == 404

def test_filter_applications_by_status():
    create_test_application()

    client.post(
        "/applications",
        json={
            "company": "Flutterwave",
            "role": "Junior Backend Engineer",
            "status": "interview"
        }
    )

    response = client.get(
        "/applications",
        params={"status": "interview"}
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["company"] == "Flutterwave"
    assert data[0]["status"] == "interview"


def test_reject_invalid_status_filter():
    response = client.get(
        "/applications",
        params={"status": "waiting"}
    )

    assert response.status_code == 422