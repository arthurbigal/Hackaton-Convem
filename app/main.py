"""
Ponto de entrada da aplicação Incident Hub.

Neste incremento, a app só sobe, cria as tabelas no SQLite (se ainda
não existirem) e expõe um health-check em `/`. Rotas de negócio
(incidentes, dashboard) e regras de transição de status entram em
incrementos futuros.
"""

from fastapi import FastAPI

from app.database.db import Base, engine
from app.models import incident  # noqa: F401 - garante que os modelos sejam registrados

app = FastAPI(title="Incident Hub", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    """Cria as tabelas do banco caso ainda não existam (persistência)."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check() -> dict:
    """Endpoint simples para confirmar que a aplicação está no ar."""
    return {"status": "ok", "service": "Incident Hub"}