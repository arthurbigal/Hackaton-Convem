"""
Testes do seed de dados iniciais.

Confirma que:
- os 3 incidentes obrigatórios são criados com os dados corretos;
- o histórico dos incidentes 2 e 3 é coerente com o status inicial deles;
- rodar o seed de novo (simulando um reinício da aplicação) NÃO duplica
  os dados.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.db import Base
from app.database.seed import seed_initial_data
from app.models.enums import Severity, Status
from app.models.incident import Incident


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_seed_creates_the_three_required_incidents(db_session):
    seed_initial_data(db_session)

    incidents = db_session.query(Incident).order_by(Incident.id).all()
    assert len(incidents) == 3

    payment = incidents[0]
    assert payment.title == "Payment API instability"
    assert payment.severity == Severity.CRITICAL.value
    assert payment.owner == "Ana"
    assert payment.status == Status.OPEN.value
    assert len(payment.history) == 0

    reconciliation = incidents[1]
    assert reconciliation.title == "Reconciliation delay"
    assert reconciliation.severity == Severity.HIGH.value
    assert reconciliation.owner == "Bruno"
    assert reconciliation.status == Status.IN_PROGRESS.value
    assert len(reconciliation.history) == 1

    notification = incidents[2]
    assert notification.title == "Incorrect customer notification"
    assert notification.severity == Severity.MEDIUM.value
    assert notification.owner == "Carla"
    assert notification.status == Status.RESOLVED.value
    assert len(notification.history) == 2
    assert notification.history[0].new_status == Status.IN_PROGRESS.value
    assert notification.history[1].new_status == Status.RESOLVED.value


def test_seed_does_not_duplicate_on_second_run(db_session):
    seed_initial_data(db_session)
    seed_initial_data(db_session)  # simula um segundo startup da aplicação

    incidents = db_session.query(Incident).all()
    assert len(incidents) == 3


def test_seed_does_not_run_if_data_already_exists(db_session):
    from app.services import incident_service

    incident_service.create_incident(
        db_session,
        title="Incidente já existente antes do seed",
        description="Descrição.",
        severity=Severity.LOW.value,
        owner="Alguém",
    )

    seed_initial_data(db_session)

    incidents = db_session.query(Incident).all()
    # Não deve ter adicionado os 3 incidentes do seed, pois já havia dado.
    assert len(incidents) == 1