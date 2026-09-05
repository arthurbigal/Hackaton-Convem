# Incident Hub — AI Log

Este documento registra as interações com ferramentas de Inteligência Artificial consideradas relevantes para a construção do Incident Hub. Não são reproduzidas todas as conversas, apenas as interações que contribuíram para decisões, implementação, validação, correções ou mudanças de estratégia.

---

## 1. Planejamento inicial da solução

### Objetivo

Definir uma estratégia inicial para desenvolver o Incident Hub durante o hackathon, priorizando o cumprimento dos requisitos obrigatórios, confiabilidade e velocidade de implementação.

### Contexto

Foi fornecido à IA o desafio completo do hackathon, incluindo os requisitos funcionais do Incident Hub, restrições de escopo, necessidade de persistência, testes automatizados, documentação e uso de IA para construção da solução.

### Instrução

Solicitei apoio para interpretar o desafio, definir uma arquitetura adequada para um hackathon de um dia e identificar quais funcionalidades deveriam ser priorizadas.

### Resultado

Foi definida uma abordagem simples, com foco nas funcionalidades obrigatórias e evitando complexidade desnecessária.

A arquitetura inicial escolhida foi:

* Python
* FastAPI
* SQLite
* SQLAlchemy
* HTML/CSS/JavaScript
* pytest

A estrutura foi planejada separando aplicação, regras de negócio, persistência, API, interface e testes.

### Validação

A arquitetura foi comparada com os requisitos do desafio, principalmente persistência, regras de transição de status, dashboard, testes e facilidade de execução local.

### Decisão

Adotar uma arquitetura simples e adequada ao tempo disponível, evitando tecnologias e funcionalidades não exigidas, como autenticação, microsserviços e banco de dados externo.

---

## 2. Decisão da interface Kanban

### Objetivo

Definir uma interface que tornasse o acompanhamento dos incidentes rápido e visual.

### Contexto

O desafio exige listagem de incidentes, filtros por status e severidade e possibilidade de alteração de status.

### Instrução

Foi discutida com a IA uma alternativa de interface baseada em Kanban para representar o fluxo dos incidentes.

### Resultado

Foi escolhida uma interface Kanban com três colunas:

* Open
* In Progress
* Resolved

Cada incidente seria representado por um card contendo, entre outras informações, título, severidade e responsável.

A severidade permaneceria como uma característica visual do card, enquanto as colunas representariam o status.

Também foi planejada a utilização de drag-and-drop para alterar o status.

### Validação

A abordagem foi comparada aos requisitos do desafio. A interface permite visualizar o estado dos incidentes e torna a movimentação entre estados explícita.

### Decisão

Adotar o Kanban como interface principal.

A decisão foi posteriormente registrada no `PLAN.md`.

---

## 3. Construção da estrutura inicial com Claude

### Objetivo

Construir a estrutura inicial do projeto e iniciar a implementação da aplicação.

### Contexto

Foram fornecidos ao Claude os requisitos do desafio, a arquitetura definida e a decisão de utilizar FastAPI, SQLite, HTML/CSS/JavaScript e pytest.

### Instrução

Claude foi utilizado para construir a estrutura inicial da aplicação e seus arquivos de código.

### Resultado

Foi criada a estrutura inicial contendo componentes para:

* aplicação FastAPI;
* banco de dados;
* modelos;
* serviços;
* testes;
* configuração de dependências.

Posteriormente, a aplicação evoluiu para incluir rotas, schemas, seed, interface web e testes de API e regras de negócio.

### Validação

A estrutura foi executada localmente e os arquivos foram posteriormente utilizados como base para a implementação funcional da aplicação.

### Decisão

Continuar o desenvolvimento utilizando a estrutura criada pelo Claude, realizando validações durante cada etapa.

---

## 4. Erro na criação do ambiente virtual

### Objetivo

Criar o ambiente virtual Python para instalar as dependências do projeto.

### Contexto

O ambiente de desenvolvimento utilizado era Windows PowerShell.

### Instrução

Claude sugeriu inicialmente a utilização do comando:

`python3 -m venv venv`

### Resultado

O comando não funcionou no Windows PowerShell porque `python3` não estava disponível como comando reconhecido no ambiente.

### Validação

O erro foi identificado diretamente no terminal.

### Decisão

Adaptar o comando para o ambiente Windows utilizando:

`python -m venv venv`

O ambiente virtual foi criado corretamente dessa forma.

### Observação

A situação demonstrou a necessidade de fornecer à IA informações específicas sobre o ambiente de desenvolvimento antes de executar comandos sugeridos.

---

## 5. Erro na ativação do ambiente virtual

### Objetivo

Ativar o ambiente virtual Python criado anteriormente.

### Contexto

O sistema utilizado era Windows PowerShell.

### Instrução

Claude sugeriu inicialmente:

`source venv/bin/activate`

### Resultado

O comando não funcionou no PowerShell, pois utiliza a sintaxe de ativação normalmente empregada em ambientes Unix/Linux.

Posteriormente, a alternativa de utilizar o script do PowerShell também encontrou uma restrição de política de execução do sistema.

### Validação

Os erros foram identificados diretamente pelo retorno do PowerShell.

### Decisão

Em vez de depender da ativação do ambiente virtual, foi adotada a estratégia de executar diretamente o Python e o pip presentes no ambiente virtual, por exemplo:

`.\venv\Scripts\python.exe`

Essa abordagem permitiu continuar o desenvolvimento sem alterar desnecessariamente as configurações de segurança do sistema.

### Aprendizado

Passou-se a considerar explicitamente o sistema operacional e o shell utilizado ao avaliar comandos sugeridos pela IA.

---

## 6. Organização do repositório e checkpoint

### Objetivo

Organizar o Git para preservar o checkpoint exigido pelo hackathon e separar os documentos iniciais do primeiro commit de código.

### Contexto

O desafio exigia que o início do projeto fosse registrado com `START.md` e que o primeiro planejamento fosse disponibilizado em `PLAN.md`.

### Instrução

Foi utilizada IA para auxiliar na organização do fluxo de Git e na verificação dos arquivos que deveriam entrar em cada commit.

### Resultado

O histórico do repositório ficou organizado de forma que os documentos do checkpoint fossem registrados antes do primeiro commit de código.

Posteriormente, foi realizado um commit separado contendo a estrutura inicial da aplicação.

### Validação

O histórico foi verificado utilizando:

`git log --oneline --all --decorate -5`

O histórico mostrou os commits dos documentos iniciais seguidos pelo commit de código.

### Decisão

Manter o histórico de desenvolvimento organizado, evitando misturar o checkpoint inicial com a implementação da aplicação.

---

## 7. Correção de arquivos gerados indevidamente pelo Python

### Objetivo

Garantir que apenas arquivos relevantes ao projeto fossem incluídos no primeiro commit de código.

### Contexto

Durante a execução do projeto, arquivos `__pycache__` e arquivos compilados `.pyc` foram gerados automaticamente pelo Python.

### Instrução

Durante a preparação do commit, foi feita uma verificação dos arquivos que seriam adicionados ao Git.

### Resultado

Foi identificado que arquivos `__pycache__` e `.pyc` estavam sendo adicionados ao staging.

### Validação

O problema foi identificado através do `git status`.

### Decisão

Os arquivos gerados automaticamente foram removidos do staging e foi criado um `.gitignore` para evitar que arquivos temporários e artefatos locais fossem versionados.

Também foi mantido o banco local `incident_hub.db` fora do commit.

---

## 8. Implementação do núcleo da aplicação

### Objetivo

Implementar uma primeira versão funcional do Incident Hub.

### Contexto

Após a definição da arquitetura e estrutura inicial, o desenvolvimento continuou utilizando IA para construção dos componentes da aplicação.

### Instrução

Claude foi utilizado para implementar componentes adicionais da aplicação, incluindo API, serviços, schemas, seed, interface e testes.

### Resultado

A aplicação passou a possuir:

* API para gerenciamento de incidentes;
* regras de negócio;
* persistência em SQLite;
* dados iniciais por meio de seed;
* interface web;
* dashboard;
* testes automatizados;
* estrutura para gerenciamento dos incidentes.

### Validação

A aplicação foi executada localmente e, até o momento do registro, apresentava funcionamento satisfatório para a primeira versão.

Também foram criados testes automatizados relacionados à API, serviço de incidentes e seed.

### Decisão

Manter a implementação atual como base para os próximos ajustes, evitando refatorações grandes enquanto as funcionalidades obrigatórias estiverem funcionando.

---

## 9. Estado da solução às 10h

### Objetivo

Registrar o estado do projeto após aproximadamente duas horas de hackathon.

### Contexto

O hackathon começou às 8h e, por volta das 10h, a primeira versão funcional da aplicação já estava disponível.

### Resultado

A aplicação web estava funcionando e o código, testes e interface já haviam sido versionados no Git.

### Validação

A aplicação foi executada e verificada manualmente durante o desenvolvimento.

### Decisão

Com a base funcional estabelecida, a estratégia passou a ser revisar os requisitos restantes, melhorar a apresentação da aplicação e corrigir eventuais pontos de baixa qualidade antes de adicionar funcionalidades extras.

---

## 10. Próximas etapas

As próximas decisões serão registradas neste documento à medida que forem tomadas, especialmente quando envolverem:

* erros produzidos pela IA;
* mudanças de estratégia;
* sugestões rejeitadas;
* regressões;
* alterações importantes na arquitetura;
* funcionalidades adicionadas ou removidas;
* problemas encontrados durante testes;
* necessidade de fornecer contexto adicional às ferramentas de IA.

---

## Observações

As conversas originais com as ferramentas de IA permanecem disponíveis para eventual auditoria, conforme as regras do hackathon.

Este documento tem como objetivo registrar as interações e decisões relevantes, e não reproduzir integralmente todas as conversas realizadas durante o desenvolvimento.
