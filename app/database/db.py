"""
Configuração de acesso ao banco de dados (SQLite via SQLAlchemy).

Este módulo expõe:
- `engine`: engine do SQLAlchemy apontando para um arquivo SQLite local.
- `SessionLocal`: factory de sessões usada pelas rotas/serviços.
- `Base`: classe base declarativa para os modelos ORM.
- `get_db`: dependency do FastAPI para injetar uma sessão por requisição.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Caminho do arquivo SQLite. Fica na raiz do projeto para persistir
# entre reinícios da aplicação (requisito de persistência).
DATABASE_URL = "sqlite:///./incident_hub.db"

# `check_same_thread=False` é necessário porque o SQLite por padrão
# só permite uso na thread que criou a conexão, e o FastAPI/Starlette
# pode atender requisições em threads diferentes.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency do FastAPI: entrega uma sessão e garante que ela é fechada."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()