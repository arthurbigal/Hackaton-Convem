"""
Testes de integração da API HTTP.

Usam um banco SQLite em memória isolado (via override de `get_db`),
independente do arquivo incident_hub.db real, para não misturar dados
de teste com dados de desenvolvimento.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    """Cria um TestClient com banco em memória isolado por teste."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

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


def _create_incident(client, severity="High", title="Payment API instability"):
    response = client.post(
        "/incidents",
        json={
            "title": title,
            "description": "Descrição de teste.",
            "severity": severity,
            "owner": "Ana",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_incident_returns_open_status(client):
    incident = _create_incident(client)

    assert incident["status"] == "Open"
    assert incident["title"] == "Payment API instability"
    assert "id" in incident


def test_create_incident_with_invalid_severity_returns_422(client):
    response = client.post(
        "/incidents",
        json={
            "title": "X",
            "description": "Y",
            "severity": "Urgentissimo",
            "owner": "Ana",
        },
    )
    assert response.status_code == 422


def test_list_incidents_filters_by_status_and_severity(client):
    _create_incident(client, severity="Critical", title="Payment API instability")
    _create_incident(client, severity="High", title="Reconciliation delay")

    all_incidents = client.get("/incidents").json()
    assert len(all_incidents) == 2

    only_critical = client.get("/incidents", params={"severity": "Critical"}).json()
    assert len(only_critical) == 1
    assert only_critical[0]["title"] == "Payment API instability"


def test_get_incident_detail_includes_history(client):
    incident = _create_incident(client, severity="High")
    incident_id = incident["id"]

    client.patch(f"/incidents/{incident_id}/status", json={"status": "In Progress"})

    detail = client.get(f"/incidents/{incident_id}").json()
    assert detail["status"] == "In Progress"
    assert len(detail["history"]) == 1
    assert detail["history"][0]["previous_status"] == "Open"
    assert detail["history"][0]["new_status"] == "In Progress"


def test_get_unknown_incident_returns_404(client):
    response = client.get("/incidents/9999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_critical_open_to_resolved_is_rejected_with_400(client):
    incident = _create_incident(client, severity="Critical")

    response = client.patch(
        f"/incidents/{incident['id']}/status", json={"status": "Resolved"}
    )

    assert response.status_code == 400
    assert "Critical" in response.json()["detail"]

    # Confirma que o status realmente não mudou.
    reloaded = client.get(f"/incidents/{incident['id']}").json()
    assert reloaded["status"] == "Open"


def test_critical_full_valid_flow_is_accepted(client):
    incident = _create_incident(client, severity="Critical")
    incident_id = incident["id"]

    r1 = client.patch(
        f"/incidents/{incident_id}/status", json={"status": "In Progress"}
    )
    assert r1.status_code == 200

    r2 = client.patch(f"/incidents/{incident_id}/status", json={"status": "Resolved"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "Resolved"


def test_dashboard_reflects_current_data(client):
    critical = _create_incident(client, severity="Critical", title="Payment API instability")
    _create_incident(client, severity="High", title="Reconciliation delay")
    resolved = _create_incident(client, severity="Medium", title="Incorrect customer notification")

    client.patch(f"/incidents/{resolved['id']}/status", json={"status": "Resolved"})

    dashboard = client.get("/dashboard").json()
    assert dashboard["open_count"] == 2
    assert dashboard["critical_unresolved_count"] == 1
    assert dashboard["resolved_count"] == 1