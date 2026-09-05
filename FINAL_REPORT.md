# Incident Hub — Relatório Final

### 1. O que foi entregue?

- CRUD de incidentes (criação, listagem, detalhes) com título, descrição, severidade, responsável, status e timestamps.
- Status inicial automático `Open`.
- Regra de transição de status implementada no backend, incluindo a restrição de incidentes `Critical` (não podem ir de `Open` direto para `Resolved`).
- Histórico de transições de status persistido.
- Comentários em incidentes (autor, conteúdo, data/hora), com validação de campos obrigatórios (inclusive contra conteúdo só com espaços).
- Timeline unificada por incidente, combinando status e comentários em ordem cronológica.
- Dashboard com contagem de abertos (Open + In Progress), Critical não resolvidos e resolvidos.
- Exclusão de incidentes.
- Filtros por status e severidade.
- Interface Kanban (Open / In Progress / Resolved) com drag-and-drop, feedback de erro compreensível e reversão visual em transições rejeitadas.
- Dados de exemplo (seed) carregados automaticamente na primeira execução, sem duplicar em reinícios.
- Persistência via SQLite, validada após reload e reinício da aplicação.
- 29 testes automatizados cobrindo as regras de negócio críticas.
- Documentação: README, START, PLAN, AI_LOG.

### 2. O que não foi entregue?

- Filtro/ordenação por severidade dentro de cada coluna do Kanban (tentado, causou regressão no frontend e foi revertido).
- Refinamentos visuais adicionais além do redesign básico feito manualmente.
- Testes de interface (E2E automatizado do drag-and-drop); a validação do frontend foi manual.

### 3. O que você deliberadamente decidiu não fazer?

- Autenticação, permissões, múltiplos tenants — fora de escopo desde o planejamento inicial, conforme o próprio desafio orientava.
- Edição ou exclusão de comentários após criados — só criação, para manter o escopo simples e íntegro com o requisito.
- Paginação na listagem de incidentes — volume de dados esperado (pequena equipe) não justifica a complexidade.
- Ordenação por severidade dentro das colunas do Kanban — abandonada no meio da implementação por não ser requisito obrigatório e ter causado uma regressão visual perto do code freeze; risco maior que o benefício.

### 4. Quais foram as três principais decisões técnicas?

1. **Regra de transição de status isolada na camada de serviço** (`incident_service.py`), independente da API e do frontend — permitiu testar a regra do `Critical` de forma unitária, sem subir servidor nem depender de HTTP, e garantir que o drag-and-drop nunca pudesse contornar a regra.
2. **SQLite + SQLAlchemy com seed idempotente** — persistência simples o suficiente para o prazo do hackathon, com uma função de seed que checa se já existem dados antes de inserir, evitando duplicação a cada reinício.
3. **Exceções de domínio traduzidas em handlers HTTP centralizados** (`InvalidTransitionError`, `IncidentNotFoundError`, `InvalidCommentError` → 400/404 no `main.py`) — mantém as rotas "finas" e garante mensagens de erro compreensíveis de forma consistente em toda a API, sem duplicar tratamento de erro em cada endpoint.

### 5. Qual foi o maior erro produzido pela IA durante o desenvolvimento?

Uma regra CSS (`.modal-overlay { display: flex; }`) sobrescrevia o atributo HTML `hidden`, fazendo os modais de criação/detalhes aparecerem sempre visíveis e sobrepostos, travando a interface logo na primeira abertura da aplicação.

### 6. Como você identificou esse erro?

Validação manual no navegador: ao abrir a aplicação, a tela de detalhes aparecia por cima de tudo e o botão "Fechar" não respondia, mesmo a lógica JavaScript estando correta.

### 7. Como você corrigiu e validou a correção?

A correção foi adicionar uma regra CSS explícita para o estado oculto (`.modal-overlay[hidden] { display: none; }`), sem alterar HTML ou JavaScript. A validação foi feita recarregando a aplicação com cache limpo (`Ctrl+F5`) e confirmando que os modais permaneciam ocultos até a interação do usuário. O mesmo padrão de bug se repetiu depois com a barra de erro (`.error-banner`) e foi corrigido da mesma forma.

### 8. Houve alguma regressão?

Sim, duas:

- Ao tentar adicionar um filtro de ordenação por severidade em cada coluna do Kanban, uma edição manual no HTML perdeu inteiramente o bloco da coluna "In Progress", quebrando a renderização do board inteiro. Identificado pela ausência total de incidentes na tela e travamento da interface. Como a funcionalidade não era obrigatória, a decisão foi reverter a mudança em vez de depurar mais a fundo, priorizando a estabilidade antes do code freeze.
- Uma edição manual nos botões do modal de detalhes (HTML) deixou duas tags `<div class="modal-actions">` abertas e o texto "Fechar" foi parar dentro da tag errada, fazendo o botão de excluir responder no lugar do botão de fechar. Identificado por teste manual (clique não fazia nada) e corrigido reestruturando o bloco HTML dos dois botões.

### 9. Em qual parte houve mais retrabalho?

No frontend, especificamente após o usuário passar a editar o HTML/CSS manualmente (fora do fluxo assistido por IA) para aplicar identidade visual própria. Isso gerou desalinhamento entre o que a IA presumia sobre a estrutura do HTML e o que de fato existia no arquivo, causando os dois bugs de regressão descritos acima. O backend, por ser inteiramente gerado e validado via testes automatizados a cada incremento, não teve retrabalho.

### 10. Cite uma situação em que você rejeitou ou alterou uma abordagem sugerida pela IA.

Ao adicionar a funcionalidade de ordenação por severidade nas colunas do Kanban, a implementação sugerida quebrou a interface durante a integração manual. Diante do risco identificado, a decisão foi abandonar a funcionalidade por completo (não era requisito obrigatório) em vez de insistir na correção, priorizando a estabilidade do que já estava funcionando perto do code freeze.

### 11. Qual parte da aplicação você considera menos confiável?

O frontend, por ter passado por edição manual direta (fora do controle incremental e testado da IA) e não possuir testes automatizados — toda a validação da interface foi manual. O backend, em contraste, tem 29 testes automatizados cobrindo as regras de negócio.

### 12. Se tivesse mais duas horas, quais seriam suas três prioridades?

1. Adicionar testes automatizados de frontend (ou ao menos um checklist de regressão manual mais completo), já que foi a parte com mais bugs.
2. Reimplementar a ordenação por severidade nas colunas do Kanban de forma mais cuidadosa, com backup do HTML antes da edição.
3. Refinar UX de pequenos detalhes (contraste do indicador de comentários, mensagens de coluna vazia) e revisar responsividade para telas menores.

### 13. Como você avalia sua estratégia inicial?

A estratégia de dividir o desenvolvimento em incrementos pequenos e validados (modelos → regras de negócio → API → frontend → seed) funcionou bem: cada camada foi testada isoladamente antes de avançar, o que manteve o backend estável mesmo com a chegada do Change Request de comentários no meio do desenvolvimento. O que mudaria: ter definido desde o início um processo mais controlado para edições manuais de frontend (ex.: sempre revisar o diff antes de aplicar), já que foi a origem das duas regressões do projeto.

### 14. Aproximadamente quantas interações relevantes com IA foram necessárias?

Aproximadamente 40 a 50 interações relevantes ao longo do dia, entre planejamento, geração de código por incremento, depuração de bugs de ambiente (Windows/PowerShell), correções de frontend e documentação.

### 15. Quais ferramentas de IA foram utilizadas?

Claude foi a ferramenta usada para toda a construção de código e testes, do planejamento inicial até a documentação final. ChatGPT e Gemini estavam planejados no `START.md` para apoio adicional, mas a implementação efetiva do código foi conduzida integralmente com Claude ao longo do dia.
