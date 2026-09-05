# AI Engineering Hackathon
## Challenge Pack

**Início:** 08:00  
**Code freeze:** 17:40  
**Entrega final:** 18:00

Leia todo este documento antes de iniciar o desenvolvimento.

---

# 1. O desafio

Você foi contratado para construir a primeira versão de uma aplicação chamada **Incident Hub**.

Uma empresa precisa de uma ferramenta simples para registrar e acompanhar incidentes operacionais.

Atualmente os incidentes são comunicados por mensagens e acompanhados de maneira informal. Isso dificulta saber:

- quais incidentes continuam abertos;
- quais são mais graves;
- quem é responsável;
- o que aconteceu durante o tratamento;
- quais incidentes já foram resolvidos.

Seu objetivo é transformar esse problema em uma **aplicação web funcional**.

Você é responsável por decidir como estruturar e implementar a solução.

Todas as regras apresentadas no Candidate Guide continuam válidas.

---

# 2. Usuário da aplicação

Considere que a primeira versão será utilizada por uma pequena equipe de operações.

Não é necessário implementar:

- autenticação;
- diferentes níveis de permissão;
- recuperação de senha;
- organizações ou múltiplos tenants.

Considere um único ambiente compartilhado.

---

# 3. Incident

Cada incidente deve possuir pelo menos:

- identificador;
- título;
- descrição;
- severidade;
- responsável;
- status;
- data/hora de criação;
- data/hora da última atualização.

## Severidade

Os valores possíveis são:

- Low
- Medium
- High
- Critical

## Status

Os valores possíveis são:

- Open
- In Progress
- Resolved

---

# 4. Criar incidente

O usuário deverá conseguir criar um novo incidente.

Os seguintes campos são obrigatórios:

- título;
- descrição;
- severidade;
- responsável.

Todo novo incidente deverá começar automaticamente com:

**Status = Open**

A data/hora de criação deverá ser registrada automaticamente.

---

# 5. Lista de incidentes

O usuário deverá conseguir visualizar os incidentes existentes.

A lista deverá apresentar informações suficientes para identificar rapidamente pelo menos:

- título;
- severidade;
- responsável;
- status.

O usuário deverá conseguir filtrar a lista por:

- status;
- severidade.

A forma de apresentação fica a seu critério.

---

# 6. Detalhes do incidente

O usuário deverá conseguir abrir um incidente e visualizar seus detalhes.

A tela deverá apresentar pelo menos:

- título;
- descrição;
- severidade;
- responsável;
- status;
- data/hora de criação;
- data/hora da última atualização.

---

# 7. Alteração de status

O usuário deverá conseguir alterar o status de um incidente.

Entretanto, existe uma regra de negócio:

> **Um incidente Critical não pode passar diretamente de Open para Resolved.**

Para um incidente Critical ser resolvido, ele deverá primeiro passar por:

**In Progress**

Exemplo permitido:

`Open → In Progress → Resolved`

Exemplo proibido:

`Open → Resolved`

Caso o usuário tente realizar uma transição inválida, a aplicação deverá impedir a operação e apresentar feedback compreensível.

---

# 8. Histórico

A aplicação deverá manter um histórico das alterações de status.

Cada registro do histórico deverá permitir identificar:

- status anterior;
- novo status;
- data/hora da alteração.

Exemplo:

`10:31 — Open → In Progress`

`11:14 — In Progress → Resolved`

O histórico deverá estar associado ao incidente correspondente e ser persistido.

---

# 9. Dashboard

A aplicação deverá possuir uma visão resumida apresentando pelo menos:

- quantidade de incidentes atualmente abertos;
- quantidade de incidentes Critical ainda não resolvidos;
- quantidade de incidentes resolvidos.

Os valores apresentados deverão refletir o estado atual dos dados.

---

# 10. Persistência

Os dados não poderão desaparecer simplesmente ao atualizar a página ou reiniciar a aplicação.

Você deverá implementar algum mecanismo de persistência.

A tecnologia utilizada fica a seu critério.

Considere o tamanho e objetivo deste desafio antes de escolher sua solução.

---

# 11. Dados iniciais

A aplicação deverá permitir que o avaliador comece a utilizá-la sem precisar cadastrar muitos registros manualmente.

Sua solução deverá possuir uma forma simples de disponibilizar alguns incidentes de exemplo.

Os dados iniciais deverão incluir pelo menos:

### Incident 1

**Title:** Payment API instability  
**Severity:** Critical  
**Owner:** Ana  
**Status:** Open

### Incident 2

**Title:** Reconciliation delay  
**Severity:** High  
**Owner:** Bruno  
**Status:** In Progress

### Incident 3

**Title:** Incorrect customer notification  
**Severity:** Medium  
**Owner:** Carla  
**Status:** Resolved

Você poderá adicionar outros dados de exemplo.

---

# 12. Requisitos de qualidade

Além das funcionalidades descritas, sua solução deverá:

- ser executável localmente;
- possuir persistência;
- tratar entradas inválidas relevantes;
- apresentar feedback compreensível em operações inválidas;
- possuir interface minimamente utilizável;
- possuir instruções claras de execução;
- possuir testes automatizados para as regras de negócio que você considerar críticas;
- permitir reprodução da solução a partir do repositório.

Não esperamos uma interface visual sofisticada.

**Funcionalidade, confiabilidade e clareza são mais importantes do que aparência.**

---

# 13. Liberdade técnica

Você poderá escolher:

- linguagem;
- framework;
- bibliotecas;
- banco de dados;
- arquitetura;
- organização do projeto;
- estratégia de testes.

Não existe uma stack preferida para fins de avaliação.

Lembre-se de que você possui tempo limitado.

---

# 14. Repositório

Crie agora um novo repositório especificamente para este hackathon.

O repositório deverá conter toda a solução e os documentos solicitados abaixo.

Crie como primeiro commit um arquivo:

`START.md`

contendo:

- seu nome;
- horário em que iniciou o desafio;
- ferramenta(s) de IA que pretende utilizar inicialmente.

Nenhum código da solução deverá existir antes desse primeiro commit.

---

# 15. Entregáveis

Ao final do desafio, esperamos encontrar no repositório pelo menos:

```text
README.md
START.md
PLAN.md
AI_LOG.md
FINAL_REPORT.md
[código da aplicação]
[testes]
```

Você poderá criar outros documentos ou arquivos caso considere úteis.

---

# 16. PLAN.md

Antes de iniciar a implementação, crie um documento chamado:

`PLAN.md`

O documento deverá registrar sua abordagem inicial.

Ele deverá conter pelo menos:

## Entendimento

Explique brevemente, com suas próprias palavras, o problema que pretende resolver.

## Escopo

Defina o que considera:

- obrigatório;
- desejável;
- fora de escopo.

## Decisões técnicas

Registre as principais decisões iniciais, incluindo:

- stack;
- persistência;
- estrutura geral da solução;
- estratégia de testes.

Explique brevemente o motivo das escolhas.

## Decomposição

Apresente as principais atividades que pretende executar.

## Critérios de aceite

Defina como pretende determinar se os principais requisitos foram realmente concluídos.

## Riscos

Liste os principais riscos que identifica para completar o desafio dentro do tempo disponível.

## Estratégia de IA

Explique brevemente como pretende utilizar IA durante o desenvolvimento.

---

# 17. Checkpoint obrigatório — 08:45

Até **08:45**, deverá existir no repositório um commit contendo pelo menos:

- `START.md`;
- primeira versão do `PLAN.md`.

Esse checkpoint faz parte da avaliação.

O `PLAN.md` poderá continuar evoluindo depois desse horário.

Não esperamos que sua primeira versão seja perfeita.

Queremos conseguir observar como seu planejamento evolui durante o desenvolvimento.

---

# 18. AI_LOG.md

Crie um arquivo:

`AI_LOG.md`

Não é necessário copiar todas as suas conversas com IA.

Registre as interações que considerar relevantes para compreender como a solução foi construída.

Para cada interação relevante, procure registrar:

### Objetivo

O que você estava tentando alcançar?

### Contexto

Que informações ou arquivos foram fornecidos à IA?

### Instrução

Qual foi a instrução ou estratégia utilizada?

### Resultado

O que aconteceu?

### Validação

Como você verificou se o resultado estava correto?

### Decisão

Qual foi sua próxima decisão?

Também registre situações relevantes nas quais:

- a IA produziu algo incorreto;
- uma abordagem precisou ser abandonada;
- ocorreu regressão;
- você rejeitou uma sugestão da IA;
- precisou fornecer contexto adicional;
- mudou sua estratégia.

As conversas originais deverão continuar disponíveis para eventual auditoria, conforme definido no Candidate Guide.

---

# 19. README.md

Seu `README.md` deverá permitir que outra pessoa execute sua aplicação.

Inclua pelo menos:

## Pré-requisitos

O que precisa estar instalado?

## Instalação

Como instalar as dependências?

## Execução

Como iniciar a aplicação?

## Dados iniciais

Como disponibilizar/resetar os dados de exemplo?

## Testes

Como executar os testes?

## Arquitetura

Uma explicação curta da estrutura da solução.

## Limitações conhecidas

Problemas ou limitações que o avaliador deveria conhecer.

O avaliador poderá tentar executar sua solução utilizando apenas essas instruções.

---

# 20. FINAL_REPORT.md

Antes do code freeze, crie:

`FINAL_REPORT.md`

Responda de forma objetiva às seguintes perguntas.

### 1. O que foi entregue?

Liste as principais funcionalidades concluídas.

### 2. O que não foi entregue?

Liste funcionalidades incompletas ou ausentes.

### 3. O que você deliberadamente decidiu não fazer?

Explique decisões de escopo.

### 4. Quais foram as três principais decisões técnicas?

Explique brevemente cada uma.

### 5. Qual foi o maior erro produzido pela IA durante o desenvolvimento?

Explique o problema.

### 6. Como você identificou esse erro?

Descreva o processo.

### 7. Como você corrigiu e validou a correção?

Explique como determinou que o problema estava resolvido.

### 8. Houve alguma regressão?

Se sim, explique como foi identificada e corrigida.

### 9. Em qual parte houve mais retrabalho?

Explique por quê.

### 10. Cite uma situação em que você rejeitou ou alterou uma abordagem sugerida pela IA.

Explique sua decisão.

### 11. Qual parte da aplicação você considera menos confiável?

Explique por quê.

### 12. Se tivesse mais duas horas, quais seriam suas três prioridades?

Coloque-as em ordem.

### 13. Como você avalia sua estratégia inicial?

Explique o que manteria e o que mudaria.

### 14. Aproximadamente quantas interações relevantes com IA foram necessárias?

Não é necessário contabilizar tokens com precisão.

### 15. Quais ferramentas de IA foram utilizadas?

Informe também se precisou trocar de ferramenta durante o desafio e por quê.

---

# 21. Mudanças no desafio

Considere que os requisitos apresentados neste documento representam o estado atual do produto.

**Novas informações ou mudanças poderão ser apresentadas durante o hackathon.**

Caso isso aconteça, você será responsável por decidir como incorporá-las ao seu trabalho.

---

# 22. Prioridades

Não existe pontuação automática por quantidade de funcionalidades.

Antes de adicionar algo que não foi solicitado, considere se os requisitos existentes estão:

- implementados;
- funcionando;
- testados;
- documentados.

Funcionalidades extras não compensam requisitos obrigatórios que não funcionam.

---

# 23. Code freeze — 17:40

Às **17:40**, todo desenvolvimento deverá parar.

Até esse horário:

- código deverá estar finalizado;
- testes deverão estar finalizados;
- documentação deverá estar finalizada;
- alterações deverão estar commitadas;
- alterações deverão estar enviadas ao repositório remoto.

Após 17:40, você não poderá alterar:

- código;
- testes;
- README;
- PLAN;
- AI_LOG;
- FINAL_REPORT;
- histórico Git.

Registre o hash do commit final.

---

# 24. Vídeo final

Entre **17:40 e 18:00**, grave uma apresentação de no máximo **5 minutos**.

O vídeo deverá ser gravado em uma única tomada, sem cortes ou edição.

Não prepare slides.

## 0:00–0:30 — Introdução

Seu nome e uma descrição da solução.

## 0:30–2:30 — Demonstração

Mostre a aplicação funcionando.

Demonstre principalmente os requisitos que considera mais importantes.

## 2:30–3:30 — Processo

Mostre brevemente:

- planejamento;
- histórico Git;
- estrutura do projeto;
- principais decisões.

## 3:30–4:30 — IA

Apresente um problema real ocorrido durante o desenvolvimento e mostre como utilizou IA para investigá-lo e resolvê-lo.

## 4:30–5:00 — Retrospectiva

Explique:

- principal limitação;
- o que ficou faltando;
- o que faria diferente.

---

# 25. Entrega

Até **18:00**, envie pelo canal indicado pela organização:

- seu nome;
- URL do repositório;
- hash do commit final;
- link ou arquivo do vídeo.

Certifique-se de que os avaliadores possuem acesso ao repositório.

---

# 26. Antes de começar

Leia novamente os requisitos.

A partir deste momento, as decisões são suas.

Você decide:

- como estruturar o problema;
- como dividir o trabalho;
- quando utilizar IA;
- que contexto fornecer;
- como verificar o resultado;
- quando uma tarefa está realmente concluída;
- quando seguir para a próxima etapa;
- o que simplificar;
- o que priorizar.

**Boa sorte.**