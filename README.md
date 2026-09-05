# Hackaton-Convem

# Incident Hub

Aplicação web para uma pequena equipe de operações registrar e acompanhar incidentes, com board estilo Kanban, dashboard resumido, histórico de status, comentários e timeline unificada.

## Pré-requisitos

- Python 3.10 ou superior
- pip

Nenhum banco externo é necessário: a aplicação usa SQLite (arquivo local).

## Instalação

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload
```

Acesse `http://127.0.0.1:8000/` para o board Kanban. A documentação interativa da API (Swagger) fica em `http://127.0.0.1:8000/docs`.

## Dados iniciais

Ao subir pela primeira vez, a aplicação cria automaticamente o arquivo `incident_hub.db` e popula 3 incidentes de exemplo obrigatórios:

1. **Payment API instability** — Critical, Ana, Open
2. **Reconciliation delay** — High, Bruno, In Progress
3. **Incorrect customer notification** — Medium, Carla, Resolved

Esse seed só roda se o banco estiver vazio (reiniciar a aplicação não duplica os dados).

**Para resetar os dados** e voltar ao estado inicial, pare a aplicação, apague o arquivo `incident_hub.db` na raiz do projeto e suba a aplicação de novo.

## Testes

```bash
pytest tests/ -v
```

Cobertura: regras de transição de status (incluindo a regra do Critical), API HTTP, seed de dados iniciais, comentários e timeline unificada.

## Arquitetura
Frontend (HTML/CSS/JS puro, templates/ e static/)
↓ fetch (HTTP/JSON)
Rotas FastAPI (app/routes/)
↓
Camada de serviço / regras de negócio (app/services/)
↓
SQLAlchemy (app/database/)
↓
SQLite (incident_hub.db)


- **`app/models/`** — modelos ORM: `Incident`, `StatusHistory`, `Comment`.
- **`app/services/incident_service.py`** — toda a regra de negócio (criação, listagem, transição de status, comentários, timeline, dashboard), testável sem depender da API ou do banco real.
- **`app/services/exceptions.py`** — exceções de domínio (`InvalidTransitionError`, `IncidentNotFoundError`, `InvalidCommentError`), traduzidas em `app/main.py` para respostas HTTP com mensagens compreensíveis (400/404), em vez de erros genéricos.
- **`app/routes/`** — rotas HTTP "finas": validam entrada via Pydantic e delegam para a camada de serviço.
- **`app/database/seed.py`** — dados iniciais obrigatórios.
- **Regra crítica de transição:** incidentes com severidade `Critical` não podem ir diretamente de `Open` para `Resolved`; precisam passar por `In Progress`. Essa regra é aplicada no backend (`incident_service.change_status`), independente do frontend — o drag-and-drop no Kanban é só uma forma de UX de disparar essa chamada, e é rejeitado pelo backend se inválido.
- **Timeline:** cada incidente tem uma visão cronológica única combinando mudanças de status e comentários, ordenada por data/hora (`incident_service.get_timeline`).
- **Persistência:** SQLite via SQLAlchemy; os dados sobrevivem a reload de página e reinício da aplicação.

## Limitações conhecidas

- Não há autenticação, permissões ou múltiplos usuários/tenants — ambiente único e compartilhado, por decisão de escopo do desafio.
- Não há edição ou exclusão de incidentes/comentários após criados, apenas criação e alteração de status.
- O SQLite é adequado para o escopo do desafio, mas não é recomendado para uso concorrente intenso em produção.
- Não há paginação na listagem de incidentes (adequado ao volume esperado de uma pequena equipe de operações).
