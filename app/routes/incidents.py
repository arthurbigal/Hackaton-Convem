"""
Rotas HTTP do domínio de incidentes.

As rotas são "finas": validam a entrada via schemas Pydantic, chamam a
camada de services e formatam a saída. Nenhuma regra de negócio vive
aqui — isso está em `app.services.incident_service`, onde já é testada
de forma isolada.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.incident import (
    CommentCreate,
    CommentResponse,
    IncidentCreate,
    IncidentDetailResponse,
    IncidentResponse,
    StatusHistoryResponse,
    StatusUpdateRequest,
)
from app.services import incident_service

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = incident_service.create_incident(
        db,
        title=payload.title,
        description=payload.description,
        severity=payload.severity.value,
        owner=payload.owner,
    )
    return incident


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    status: str | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
):
    return incident_service.list_incidents(db, status=status, severity=severity)


@router.get("/{incident_id}", response_model=IncidentDetailResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = incident_service.get_incident(db, incident_id)
    # Atributo dinâmico (não persistido) só para a serialização da resposta.
    incident.timeline = incident_service.get_timeline(incident)
    return incident


@router.post("/{incident_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    incident_id: int, payload: CommentCreate, db: Session = Depends(get_db)
):
    return incident_service.add_comment(
        db, incident_id, payload.author, payload.content
    )


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_status(
    incident_id: int, payload: StatusUpdateRequest, db: Session = Depends(get_db)
):
    return incident_service.change_status(db, incident_id, payload.status.value)


@router.get("/{incident_id}/history", response_model=list[StatusHistoryResponse])
def get_history(incident_id: int, db: Session = Depends(get_db)):
    incident = incident_service.get_incident(db, incident_id)
    return incident.history

@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident_service.delete_incident(db, incident_id)