"""Testes do requisito de comentários e da timeline unificada."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _create_incident(client, severity="High"):
    response = client.post(
        "/incidents",
        json={
            "title": "Payment API instability",
            "description": "Descrição.",
            "severity": severity,
            "owner": "Ana",
        },
    )
    return response.json()


def test_add_comment_persists_and_appears_in_detail(client):
    incident = _create_incident(client)

    response = client.post(
        f"/incidents/{incident['id']}/comments",
        json={"author": "Ana", "content": "Provider contacted."},
    )
    assert response.status_code == 201
    assert response.json()["author"] == "Ana"

    detail = client.get(f"/incidents/{incident['id']}").json()
    assert len(detail["comments"]) == 1
    assert detail["comments"][0]["content"] == "Provider contacted."


def test_empty_content_is_rejected(client):
    incident = _create_incident(client)

    response = client.post(
        f"/incidents/{incident['id']}/comments",
        json={"author": "Ana", "content": ""},
    )
    assert response.status_code == 422  # Pydantic min_length=1


def test_whitespace_only_content_is_rejected(client):
    incident = _create_incident(client)

    response = client.post(
        f"/incidents/{incident['id']}/comments",
        json={"author": "Ana", "content": "   "},
    )
    assert response.status_code == 400  # pego pela validação de negócio (strip)


def test_comment_on_unknown_incident_returns_404(client):
    response = client.post(
        "/incidents/9999/comments",
        json={"author": "Ana", "content": "Oi"},
    )
    assert response.status_code == 404


def test_timeline_merges_status_changes_and_comments_in_order(client):
    incident = _create_incident(client, severity="Critical")
    incident_id = incident["id"]

    client.post(
        f"/incidents/{incident_id}/comments",
        json={"author": "Ana", "content": "Provider contacted."},
    )
    client.patch(f"/incidents/{incident_id}/status", json={"status": "In Progress"})
    client.post(
        f"/incidents/{incident_id}/comments",
        json={"author": "Bruno", "content": "Fix deployed."},
    )
    client.patch(f"/incidents/{incident_id}/status", json={"status": "Resolved"})

    timeline = client.get(f"/incidents/{incident_id}").json()["timeline"]

    assert len(timeline) == 4
    descriptions = [event["description"] for event in timeline]
    assert descriptions[0] == 'Ana commented: "Provider contacted."'
    assert descriptions[1] == "Status changed: Open → In Progress"
    assert descriptions[2] == 'Bruno commented: "Fix deployed."'
    assert descriptions[3] == "Status changed: In Progress → Resolved"


def test_existing_incident_flow_still_works_after_comments_feature(client):
    """Garante que o requisito de comentários não quebrou nada anterior."""
    incident = _create_incident(client, severity="Critical")

    reject = client.patch(
        f"/incidents/{incident['id']}/status", json={"status": "Resolved"}
    )
    assert reject.status_code == 400

    dashboard = client.get("/dashboard").json()
    assert dashboard["open_count"] == 1