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


class IncidentDetailResponse(IncidentResponse):
    """Resposta de detalhe: inclui o histórico de transições."""

    history: list[StatusHistoryResponse] = []


class DashboardResponse(BaseModel):
    """Resumo agregado usado no dashboard."""

    open_count: int
    critical_unresolved_count: int
    resolved_count: int