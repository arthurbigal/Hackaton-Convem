"""
Dados iniciais (seed) do Incident Hub.

Insere os incidentes de exemplo exigidos pelo desafio, mas apenas se o
banco ainda estiver vazio — assim, reiniciar a aplicação não duplica os
dados a cada startup (persistência real).

Como os incidentes seed 2 e 3 já "nascem" em In Progress/Resolved (ou
seja, já passaram por transições antes de a aplicação existir), o seed
também grava o histórico correspondente, para manter a coerência do
requisito de histórico de transições.
"""

from sqlalchemy.orm import Session

from app.models.enums import Severity, Status
from app.models.incident import Incident, StatusHistory

_SEED_INCIDENTS = [
    {
        "title": "Payment API instability",
        "description": "A API de pagamentos está apresentando instabilidade intermitente.",
        "severity": Severity.CRITICAL.value,
        "owner": "Ana",
        "status": Status.OPEN.value,
        "history": [],
    },
    {
        "title": "Reconciliation delay",
        "description": "O processo de reconciliação financeira está atrasado.",
        "severity": Severity.HIGH.value,
        "owner": "Bruno",
        "status": Status.IN_PROGRESS.value,
        "history": [(Status.OPEN.value, Status.IN_PROGRESS.value)],
    },
    {
        "title": "Incorrect customer notification",
        "description": "Clientes receberam uma notificação com informação incorreta.",
        "severity": Severity.MEDIUM.value,
        "owner": "Carla",
        "status": Status.RESOLVED.value,
        "history": [
            (Status.OPEN.value, Status.IN_PROGRESS.value),
            (Status.IN_PROGRESS.value, Status.RESOLVED.value),
        ],
    },
]


def seed_initial_data(db: Session) -> None:
    """Popula o banco com os incidentes iniciais, se ainda estiver vazio.

    É seguro chamar esta função em todo startup da aplicação: se já
    existir pelo menos um incidente, ela não faz nada.
    """
    already_has_data = db.query(Incident).first() is not None
    if already_has_data:
        return

    for seed in _SEED_INCIDENTS:
        incident = Incident(
            title=seed["title"],
            description=seed["description"],
            severity=seed["severity"],
            owner=seed["owner"],
            status=seed["status"],
        )
        db.add(incident)
        db.flush()  # garante que incident.id já existe para o histórico

        for previous_status, new_status in seed["history"]:
            db.add(
                StatusHistory(
                    incident_id=incident.id,
                    previous_status=previous_status,
                    new_status=new_status,
                )
            )

    db.commit()