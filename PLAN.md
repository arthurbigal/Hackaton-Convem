# Incident Hub — Plano Inicial

## Entendimento

O Incident Hub será uma aplicação web para uma pequena equipe de operações registrar, acompanhar e resolver incidentes operacionais em um único ambiente compartilhado.

A aplicação deverá substituir o acompanhamento informal de incidentes por uma visão centralizada, permitindo identificar rapidamente quais incidentes estão abertos, qual é sua severidade, quem é o responsável e qual é o estado atual do tratamento.

Além do cadastro e acompanhamento dos incidentes, a aplicação deverá manter o histórico das alterações de status e apresentar um dashboard com uma visão resumida dos incidentes.

O foco da primeira versão será entregar uma aplicação funcional, confiável, simples de executar localmente e que implemente corretamente as regras de negócio descritas no desafio.

---

## Escopo

### Obrigatório

A primeira versão deverá implementar:

* Cadastro de incidentes.
* Identificador único para cada incidente.
* Título.
* Descrição.
* Severidade: Low, Medium, High ou Critical.
* Responsável.
* Status: Open, In Progress ou Resolved.
* Data/hora de criação.
* Data/hora da última atualização.
* Status inicial automaticamente definido como Open.
* Listagem de incidentes.
* Filtro por status.
* Filtro por severidade.
* Visualização dos detalhes de um incidente.
* Alteração de status.
* Regra de transição para incidentes Critical:

  * Open → In Progress → Resolved.
  * Open → Resolved não será permitido.
* Feedback compreensível para transições inválidas.
* Histórico persistido das alterações de status.
* Dashboard contendo:

  * incidentes atualmente abertos;
  * incidentes Critical não resolvidos;
  * incidentes resolvidos.
* Persistência dos dados.
* Dados iniciais de exemplo.
* Execução local.
* Testes automatizados para as principais regras de negócio.
* Instruções claras de execução e reprodução.

### Desejável

Caso o desenvolvimento do escopo obrigatório seja concluído com segurança, poderão ser consideradas melhorias como:

* Melhorias visuais na interface.
* Ordenação dos incidentes.
* Indicadores visuais de severidade.
* Melhorias na experiência de filtros.
* Mais validações de entrada.
* Testes adicionais de integração.
* Melhor organização e detalhamento da documentação.

Esses itens não deverão comprometer a conclusão dos requisitos obrigatórios.

### Fora de escopo

Não serão implementados nesta primeira versão:

* Autenticação.
* Recuperação de senha.
* Diferentes níveis de permissão.
* Organizações ou múltiplos tenants.
* Integrações externas.
* Sistema de notificações.
* Arquitetura distribuída.
* Funcionalidades não necessárias para o fluxo principal de gerenciamento de incidentes.

---

## Decisões técnicas

### Stack

A proposta inicial é utilizar:

* **Python** como linguagem principal.
* **FastAPI** para construção do backend e da API.
* **HTML, CSS e JavaScript** para a interface web.
* **SQLAlchemy** para persistência e acesso aos dados.
* **SQLite** como banco de dados.
* **pytest** para testes automatizados.

### Persistência

Será utilizado SQLite por ser um banco de dados relacional simples, local e adequado ao tamanho do desafio.

A utilização de um arquivo de banco permite que os dados permaneçam disponíveis após o recarregamento da aplicação e após reinicializações, sem exigir a configuração de um servidor de banco de dados externo.

### Estrutura geral

A aplicação será organizada de forma a separar:

* modelos de dados;
* acesso/persistência;
* regras de negócio;
* rotas/API;
* interface;
* testes.

A regra de negócio relacionada às transições de status deverá ficar separada da camada visual, permitindo que ela seja testada independentemente da interface.

Estrutura inicial planejada:

```text
incident-hub/
├── app/
│   ├── models/
│   ├── services/
│   ├── routes/
│   ├── database/
│   └── main.py
├── tests/
├── static/
├── templates/
├── README.md
├── START.md
├── PLAN.md
├── AI_LOG.md
├── FINAL_REPORT.md
└── requirements.txt
```

A estrutura poderá ser ajustada durante o desenvolvimento caso isso simplifique ou melhore a solução.

### Estratégia de testes

Os testes terão prioridade nas regras de negócio críticas.

Inicialmente serão testados:

* criação de incidentes;
* status inicial como Open;
* transições válidas;
* transição Open → Resolved para incidentes Critical sendo rejeitada;
* fluxo Critical Open → In Progress → Resolved;
* registro do histórico;
* atualização das datas relevantes;
* cálculo dos indicadores do dashboard.

Também poderão ser adicionados testes de integração para os principais fluxos da aplicação.

---

## Decomposição

O desenvolvimento será dividido nas seguintes etapas:

### 1. Estrutura inicial

* Criar estrutura do projeto.
* Configurar ambiente Python.
* Configurar dependências.
* Configurar aplicação FastAPI.
* Configurar banco SQLite.

### 2. Modelo de dados

Criar os modelos necessários para:

* Incident.
* Histórico de alterações de status.

Definir relacionamentos, campos obrigatórios e timestamps.

### 3. Regras de negócio

Implementar:

* criação de incidentes;
* status inicial Open;
* alteração de status;
* validação da regra específica para Critical;
* registro do histórico;
* atualização de última alteração.

### 4. API

Criar os endpoints necessários para:

* criar incidente;
* listar incidentes;
* filtrar incidentes;
* visualizar detalhes;
* alterar status;
* consultar histórico;
* obter dados do dashboard.

### 5. Interface

Construir uma interface simples contendo:

* dashboard;
* lista de incidentes;
* filtros;
* formulário de criação;
* página de detalhes;
* histórico;
* controles para alteração de status;
* mensagens de erro e sucesso.

### 6. Dados iniciais

Adicionar os três incidentes fornecidos pelo desafio:

1. Payment API instability — Critical — Ana — Open.
2. Reconciliation delay — High — Bruno — In Progress.
3. Incorrect customer notification — Medium — Carla — Resolved.

Os dados deverão ser inseridos de maneira idempotente ou através de um mecanismo que evite duplicações ao reiniciar a aplicação.

### 7. Testes

Executar os testes automatizados e corrigir as falhas encontradas.

A prioridade será testar as regras de negócio antes de realizar melhorias visuais.

### 8. Validação final

Validar manualmente os principais fluxos:

* criar incidente;
* visualizar incidente;
* filtrar incidentes;
* alterar status;
* tentar realizar uma transição inválida;
* verificar histórico;
* verificar dashboard;
* reiniciar aplicação e confirmar persistência.

### 9. Documentação

Atualizar:

* README.md;
* PLAN.md;
* AI_LOG.md;
* FINAL_REPORT.md.

Também será registrada a forma de executar e reproduzir a aplicação.

---

## Critérios de aceite

### Criação

Um usuário consegue criar um incidente informando título, descrição, severidade e responsável.

O incidente criado possui:

* identificador;
* status Open;
* data/hora de criação;
* data/hora da última atualização.

### Listagem

O usuário consegue visualizar os incidentes existentes e identificar:

* título;
* severidade;
* responsável;
* status.

Também consegue filtrar por status e severidade.

### Detalhes

Ao abrir um incidente, todas as informações obrigatórias são apresentadas.

### Status

O usuário consegue alterar o status de um incidente.

Para um incidente Critical:

```text
Open → In Progress → Resolved
```

é permitido.

Já:

```text
Open → Resolved
```

deve ser rejeitado e apresentar uma mensagem compreensível.

### Histórico

Cada alteração de status gera um registro contendo:

* status anterior;
* novo status;
* data/hora.

O histórico permanece associado ao incidente e é persistido.

### Dashboard

Os indicadores apresentados correspondem aos dados atuais armazenados:

* quantidade de incidentes abertos;
* quantidade de Critical não resolvidos;
* quantidade de incidentes resolvidos.

### Persistência

Os dados permanecem disponíveis após:

* recarregar a página;
* reiniciar a aplicação.

### Reprodução

Uma pessoa que clone o repositório consegue instalar as dependências e executar a aplicação seguindo as instruções do README.

### Testes

As principais regras de negócio possuem testes automatizados e todos os testes devem passar antes da entrega final.

---

## Riscos

### Tempo limitado

O principal risco é gastar tempo excessivo com funcionalidades ou melhorias visuais antes de concluir o fluxo principal.

**Mitigação:** priorizar os requisitos obrigatórios e deixar melhorias visuais para depois do MVP.

### Complexidade desnecessária

Uma arquitetura excessivamente complexa pode aumentar o tempo de desenvolvimento e a quantidade de pontos de falha.

**Mitigação:** utilizar uma arquitetura simples e adequada ao tamanho da aplicação.

### Erros nas regras de negócio

A regra de transição de incidentes Critical é um requisito importante e pode gerar inconsistências se implementada apenas no frontend.

**Mitigação:** implementar a regra na camada de negócio e criar testes automatizados específicos para ela.

### Persistência

Dados podem ser perdidos caso a persistência seja implementada de maneira inadequada.

**Mitigação:** utilizar banco SQLite e validar explicitamente a persistência após reinicialização.

### Dependência excessiva de IA

A geração de código por IA pode introduzir erros ou decisões inconsistentes.

**Mitigação:** dividir o desenvolvimento em pequenas etapas, revisar o código gerado, executar testes frequentemente e validar os fluxos principais manualmente.

### Integração entre frontend e backend

Erros de integração podem aparecer mesmo quando cada parte funciona isoladamente.

**Mitigação:** implementar e validar os fluxos completos progressivamente.

---

## Estratégia de IA

A IA será utilizada como principal ferramenta de desenvolvimento, respeitando as regras do hackathon.

A utilização será dividida em etapas:

1. Planejamento da arquitetura e decomposição do problema.
2. Geração da estrutura inicial do projeto.
3. Implementação dos modelos e persistência.
4. Implementação das regras de negócio.
5. Geração dos endpoints da API.
6. Construção da interface.
7. Geração dos testes automatizados.
8. Análise e correção de erros.
9. Revisão dos requisitos e critérios de aceite.
10. Geração e atualização da documentação.

Cada etapa deverá ser validada antes de avançar para a próxima.

O `AI_LOG.md` será utilizado para registrar as principais interações com IA e decisões relevantes tomadas durante o desenvolvimento.

O plano será atualizado conforme novas informações forem descobertas durante a implementação, permitindo acompanhar a evolução da estratégia ao longo do hackathon.
