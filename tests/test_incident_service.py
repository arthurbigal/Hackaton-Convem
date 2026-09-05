"""
Testes da camada de serviço de incidentes, com foco especial na regra
crítica de transição de status.

Usa um banco SQLite em memória, isolado por teste, para não depender
do arquivo incident_hub.db real e não deixar resíduos entre execuções.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.db import Base
from app.models.enums import Severity, Status
from app.services import incident_service
from app.services.exceptions import IncidentNotFoundError, InvalidTransitionError


@pytest.fixture()
def db_session():
    """Cria um banco SQLite em memória novo para cada teste."""
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


def _make_incident(db_session, severity):
    return incident_service.create_incident(
        db_session,
        title="Payment API instability",
        description="API de pagamentos apresentando instabilidade.",
        severity=severity,
        owner="Ana",
    )


def test_create_incident_starts_as_open(db_session):
    incident = _make_incident(db_session, Severity.HIGH.value)

    assert incident.status == Status.OPEN.value
    assert incident.id is not None
    assert incident.created_at is not None
    assert incident.updated_at is not None


def test_valid_transition_records_history(db_session):
    incident = _make_incident(db_session, Severity.HIGH.value)

    updated = incident_service.change_status(
        db_session, incident.id, Status.IN_PROGRESS.value
    )

    assert updated.status == Status.IN_PROGRESS.value
    assert len(updated.history) == 1
    assert updated.history[0].previous_status == Status.OPEN.value
    assert updated.history[0].new_status == Status.IN_PROGRESS.value
    assert updated.history[0].changed_at is not None


def test_critical_cannot_skip_from_open_to_resolved(db_session):
    incident = _make_incident(db_session, Severity.CRITICAL.value)

    with pytest.raises(InvalidTransitionError):
        incident_service.change_status(db_session, incident.id, Status.RESOLVED.value)

    # Garante que o status não foi alterado e nenhum histórico foi criado.
    reloaded = incident_service.get_incident(db_session, incident.id)
    assert reloaded.status == Status.OPEN.value
    assert len(reloaded.history) == 0


def test_critical_can_go_through_in_progress(db_session):
    incident = _make_incident(db_session, Severity.CRITICAL.value)

    incident_service.change_status(db_session, incident.id, Status.IN_PROGRESS.value)
    final = incident_service.change_status(
        db_session, incident.id, Status.RESOLVED.value
    )

    assert final.status == Status.RESOLVED.value
    assert len(final.history) == 2
    assert final.history[0].new_status == Status.IN_PROGRESS.value
    assert final.history[1].new_status == Status.RESOLVED.value


def test_non_critical_can_go_directly_to_resolved(db_session):
    incident = _make_incident(db_session, Severity.MEDIUM.value)

    updated = incident_service.change_status(
        db_session, incident.id, Status.RESOLVED.value
    )

    assert updated.status == Status.RESOLVED.value
    assert len(updated.history) == 1


def test_transition_to_same_status_is_rejected(db_session):
    incident = _make_incident(db_session, Severity.LOW.value)

    with pytest.raises(InvalidTransitionError):
        incident_service.change_status(db_session, incident.id, Status.OPEN.value)


def test_backward_transition_is_rejected(db_session):
    incident = _make_incident(db_session, Severity.LOW.value)
    incident_service.change_status(db_session, incident.id, Status.IN_PROGRESS.value)

    with pytest.raises(InvalidTransitionError):
        incident_service.change_status(db_session, incident.id, Status.OPEN.value)


def test_change_status_of_unknown_incident_raises(db_session):
    with pytest.raises(IncidentNotFoundError):
        incident_service.change_status(db_session, 9999, Status.IN_PROGRESS.value)


def test_list_incidents_filters_by_status_and_severity(db_session):
    critical = _make_incident(db_session, Severity.CRITICAL.value)
    incident_service.create_incident(
        db_session,
        title="Reconciliation delay",
        description="Atraso na reconciliação.",
        severity=Severity.HIGH.value,
        owner="Bruno",
    )

    only_open = incident_service.list_incidents(db_session, status=Status.OPEN.value)
    assert len(only_open) == 2

    only_critical = incident_service.list_incidents(
        db_session, severity=Severity.CRITICAL.value
    )
    assert len(only_critical) == 1
    assert only_critical[0].id == critical.id