"""
Ponto de entrada da aplicação Incident Hub.

Sobe a app, cria as tabelas no SQLite (se ainda não existirem), popula
os dados iniciais obrigatórios (seed), registra as rotas de incidentes
e dashboard, serve o frontend Kanban (HTML/CSS/JS estático) e trata as
exceções de negócio (transição inválida, incidente não encontrado)
como respostas HTTP claras em vez de erros 500 genéricos.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.database.db import Base, SessionLocal, engine
from app.database.seed import seed_initial_data
from app.models import incident  # noqa: F401 - garante que os modelos sejam registrados
from app.routes import dashboard, incidents
from app.services.exceptions import IncidentNotFoundError, InvalidTransitionError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cria as tabelas (se necessário) e popula os dados iniciais no startup."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Incident Hub", version="0.1.0", lifespan=lifespan)

app.include_router(incidents.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(InvalidTransitionError)
def handle_invalid_transition(request: Request, exc: InvalidTransitionError):
    """Transição de status inválida -> 400 com mensagem compreensível."""
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.exception_handler(IncidentNotFoundError)
def handle_incident_not_found(request: Request, exc: IncidentNotFoundError):
    """Incidente inexistente -> 404 com mensagem compreensível."""
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.get("/")
def serve_frontend() -> FileResponse:
    """Serve a página principal do Kanban."""
    return FileResponse("templates/index.html")


@app.get("/health")
def health_check() -> dict:
    """Endpoint simples para confirmar que a aplicação está no ar."""
    return {"status": "ok", "service": "Incident Hub"}