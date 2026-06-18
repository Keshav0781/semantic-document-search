import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_documents.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_and_teardown_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


def test_create_document_returns_id_and_created_at():
    response = client.post(
        "/documents",
        json={
            "title": "Test Title",
            "content": "Test content for creation check.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert data["title"] == "Test Title"


def test_search_returns_relevant_document_first():
    sample_documents = [
        {
            "title": "RCS Thruster Firing Procedure",
            "content": "This procedure describes the cold gas thruster ignition sequence for the reaction control system. It covers pre-ignition checks, valve actuation order, and post-firing telemetry verification.",
        },
        {
            "title": "Solar Panel Deployment Sequence",
            "content": "Detailed steps for deploying the photovoltaic arrays after orbital insertion. Includes hinge release commands, deployment angle monitoring, and power generation confirmation checks.",
        },
        {
            "title": "Thermal Control System Overview",
            "content": "Description of the passive and active thermal regulation mechanisms onboard Nyx. Covers heat pipe routing, multi-layer insulation zones, and heater activation thresholds.",
        },
        {
            "title": "Communication Link Budget",
            "content": "Analysis of the S-band uplink and downlink margins. Includes antenna gain figures, free-space path loss calculations, and minimum required Eb/N0 for command reception.",
        },
        {
            "title": "Propellant Tank Pressurisation Procedure",
            "content": "Step-by-step guide for pressurising the hydrazine tank prior to orbital manoeuvre. Covers regulator settings, pressure transducer readings, and abort criteria.",
        },
    ]

    for doc in sample_documents:
        client.post("/documents", json=doc)

    response = client.get("/documents/search", params={"q": "thruster firing sequence"})
    assert response.status_code == 200
    results = response.json()

    assert len(results) == 5
    assert results[0]["title"] == "RCS Thruster Firing Procedure"
    assert results[0]["score"] > results[1]["score"]


def test_delete_nonexistent_document_returns_404():
    response = client.delete("/documents/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_create_document_missing_content_returns_422():
    response = client.post(
        "/documents",
        json={"title": "Incomplete Document"},
    )
    assert response.status_code == 422
