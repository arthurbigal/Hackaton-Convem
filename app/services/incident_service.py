"""
Regras de negócio (camada de serviço) do domínio de incidentes.

Este módulo não sabe nada sobre HTTP/FastAPI — recebe uma sessão do
SQLAlchemy e trabalha diretamente com os modelos. Isso permite testar
a regra de transição de status (a mais crítica do desafio) de forma
totalmente independente da API ou do frontend.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.enums import Severity, Status
from app.models.comment import Comment
from app.models.incident import Incident, StatusHistory
from app.services.exceptions import (
    IncidentNotFoundError,
    InvalidCommentError,
    InvalidTransitionError,
)

# Transições de status permitidas em geral (independentemente da severidade).
# Chave: (status_atual, novo_status) -> permitido.
# Transições não listadas aqui (incluindo qualquer transição "para trás",
# como Resolved -> Open) são sempre rejeitadas.
_GENERAL_ALLOWED_TRANSITIONS = {
    (Status.OPEN, Status.IN_PROGRESS),
    (Status.IN_PROGRESS, Status.RESOLVED),
    (Status.OPEN, Status.RESOLVED),
}

# Transições que são permitidas em geral, mas proibidas especificamente
# quando a severidade do incidente é Critical.
_BLOCKED_FOR_CRITICAL = {
    (Status.OPEN, Status.RESOLVED),
}


def create_incident(
    db: Session, title: str, description: str, severity: str, owner: str
) -> Incident:
    """Cria um novo incidente com status inicial Open.

    `severity` deve ser um dos valores de `Severity` (ex.: "Critical").
    Levanta `ValueError` se a severidade informada for inválida.
    """
    # Valida a severidade cedo, com mensagem clara, em vez de deixar
    # um valor inválido ser gravado silenciosamente no banco.
    Severity(severity)

    incident = Incident(
        title=title,
        description=description,
        severity=severity,
        owner=owner,
        status=Status.OPEN.value,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def list_incidents(
    db: Session,
    status: Optional[str] = None,
    severity: Optional[str] = None,
) -> list[Incident]:
    """Lista incidentes, com filtros opcionais por status e severidade."""
    query = db.query(Incident)
    if status is not None:
        query = query.filter(Incident.status == status)
    if severity is not None:
        query = query.filter(Incident.severity == severity)
    return query.order_by(Incident.created_at.desc()).all()


def get_incident(db: Session, incident_id: int) -> Incident:
    """Busca um incidente pelo id. Levanta `IncidentNotFoundError` se não existir."""
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise IncidentNotFoundError(incident_id)
    return incident

def get_dashboard_summary(db: Session) -> dict:
    """Calcula os números resumidos exibidos no dashboard.

    - open_count: incidentes atualmente com status Open.
    - critical_unresolved_count: incidentes Critical cujo status ainda
      não é Resolved (ou seja, Open ou In Progress).
    - resolved_count: incidentes com status Resolved.
    """
    open_count = (
        db.query(Incident)
        .filter(Incident.status != Status.RESOLVED.value)
        .count()
    )
    critical_unresolved_count = (
        db.query(Incident)
        .filter(
            Incident.severity == Severity.CRITICAL.value,
            Incident.status != Status.RESOLVED.value,
        )
        .count()
    )
    resolved_count = (
        db.query(Incident).filter(Incident.status == Status.RESOLVED.value).count()
    )
    return {
        "open_count": open_count,
        "critical_unresolved_count": critical_unresolved_count,
        "resolved_count": resolved_count,
    }

def delete_incident(db: Session, incident_id: int) -> None:
    """Remove um incidente (e seu histórico/comentários, via cascade)."""
    incident = get_incident(db, incident_id)
    db.delete(incident)
    db.commit()

def add_comment(db: Session, incident_id: int, author: str, content: str) -> Comment:
    """Adiciona um comentário a um incidente.

    Autor e conteúdo são obrigatórios e não podem ser vazios (nem só
    espaços em branco). Levanta `InvalidCommentError` caso contrário, e
    `IncidentNotFoundError` se o incidente não existir.
    """
    incident = get_incident(db, incident_id)

    author = (author or "").strip()
    content = (content or "").strip()
    if not author or not content:
        raise InvalidCommentError(
            "Autor e conteúdo do comentário são obrigatórios e não podem ser vazios."
        )

    comment = Comment(incident_id=incident.id, author=author, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_timeline(incident: Incident) -> list[dict]:
    """Monta a timeline cronológica única de status + comentários de um incidente.

    Retorna uma lista de dicts com `timestamp` e `description`, ordenada
    do evento mais antigo para o mais recente.
    """
    events: list[dict] = []

    for entry in incident.history:
        events.append(
            {
                "timestamp": entry.changed_at,
                "description": (
                    f"Status changed: {entry.previous_status} → {entry.new_status}"
                ),
            }
        )

    for comment in incident.comments:
        events.append(
            {
                "timestamp": comment.created_at,
                "description": f'{comment.author} commented: "{comment.content}"',
            }
        )

    events.sort(key=lambda event: event["timestamp"])
    return events

def change_status(db: Session, incident_id: int, new_status: str) -> Incident:
    """Altera o status de um incidente, aplicando as regras de transição.

    Regras:
    - Só são aceitas transições "para frente": Open -> In Progress,
      In Progress -> Resolved, Open -> Resolved.
    - Incidentes Critical NÃO podem ir direto de Open para Resolved;
      precisam passar por In Progress.
    - Qualquer outra transição (ex.: para o mesmo status, ou "para trás")
      é rejeitada.

    Em caso de transição válida, grava um registro em `StatusHistory`
    com o status anterior, o novo status e o timestamp da mudança.

    Levanta `InvalidTransitionError` com mensagem compreensível quando a
    transição não é permitida, e `IncidentNotFoundError` se o incidente
    não existir.
    """
    incident = get_incident(db, incident_id)

    current_status = Status(incident.status)
    target_status = Status(new_status)

    if current_status == target_status:
        raise InvalidTransitionError(
            f"O incidente já está com status '{current_status.value}'."
        )

    transition = (current_status, target_status)

    if transition not in _GENERAL_ALLOWED_TRANSITIONS:
        raise InvalidTransitionError(
            f"Transição inválida: não é possível mudar de "
            f"'{current_status.value}' para '{target_status.value}'."
        )

    if (
        incident.severity == Severity.CRITICAL.value
        and transition in _BLOCKED_FOR_CRITICAL
    ):
        raise InvalidTransitionError(
            "Incidentes Critical não podem ir diretamente de 'Open' para "
            "'Resolved'. É necessário passar por 'In Progress' primeiro."
        )

    history_entry = StatusHistory(
        incident_id=incident.id,
        previous_status=current_status.value,
        new_status=target_status.value,
    )
    db.add(history_entry)

    incident.status = target_status.value
    db.commit()
    db.refresh(incident)
    return incident