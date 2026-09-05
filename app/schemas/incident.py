"""
Schemas Pydantic usados pela API de incidentes.

Servem para validar entradas (ex.: severidade precisa ser um dos valores
válidos) e para formatar as respostas de forma consistente. A validação
de regra de negócio (transição de status) continua na camada de
services, não aqui.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import Severity, Status


class IncidentCreate(BaseModel):
    """Payload para criação de um incidente."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)
    severity: Severity
    owner: str = Field(min_length=1, max_length=120)


class StatusUpdateRequest(BaseModel):
    """Payload para alteração de status de um incidente."""

    status: Status


class StatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    previous_status: str
    new_status: str
    changed_at: datetime

class CommentCreate(BaseModel):
    """Payload para adicionar um comentário a um incidente."""

    author: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: str
    content: str
    created_at: datetime


class TimelineEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    description: str


class IncidentResponse(BaseModel):
    """Resposta usada na criação e na listagem de incidentes."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    severity: str
    owner: str
    status: str
    created_at: datetime
    updated_at: datetime
    comment_count: int = 0


class IncidentDetailResponse(IncidentResponse):
    """Resposta de detalhe: inclui histórico, comentários e a timeline unificada."""

    history: list[StatusHistoryResponse] = []
    comments: list[CommentResponse] = []
    timeline: list[TimelineEntryResponse] = []


class DashboardResponse(BaseModel):
    """Resumo agregado usado no dashboard."""

    open_count: int
    critical_unresolved_count: int
    resolved_count: int