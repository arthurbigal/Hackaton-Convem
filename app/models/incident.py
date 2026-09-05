"""
Modelos ORM do domínio de incidentes.

- `Incident`: representa um incidente operacional (título, descrição,
  severidade, responsável, status e timestamps de criação/atualização).
- `StatusHistory`: registra cada transição de status sofrida por um
  incidente (status anterior, novo status e o momento da mudança).

A regra de negócio de transição de status (ex.: Critical não pode ir
direto de Open para Resolved) NÃO fica aqui — este módulo só descreve
a estrutura de dados. A regra vive na camada de services (próximo
incremento), para ser testável de forma independente da API/DB.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.models.enums import Status


def _utcnow() -> datetime:
    """Timestamp UTC usado como default para os campos de data/hora."""
    return datetime.now(timezone.utc)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)

    # Guardados como String no banco (não Enum nativo do SQLite) para manter
    # a migração/manuseio simples; a validação de valores válidos é feita
    # pela camada de services/schemas usando os enums de app.models.enums.
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    owner: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=Status.OPEN.value
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow
    )

    history: Mapped[list["StatusHistory"]] = relationship(
        "StatusHistory",
        back_populates="incident",
        cascade="all, delete-orphan",
        order_by="StatusHistory.changed_at",
    )

    def __repr__(self) -> str:  # pragma: no cover - apenas debug
        return f"<Incident id={self.id} title={self.title!r} status={self.status!r}>"


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
    previous_status: Mapped[str] = mapped_column(String(20), nullable=False)
    new_status: Mapped[str] = mapped_column(String(20), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="history")

    def __repr__(self) -> str:  # pragma: no cover - apenas debug
        return (
            f"<StatusHistory incident_id={self.incident_id} "
            f"{self.previous_status!r} -> {self.new_status!r}>"
        )