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

## 11. Bug nos modais da interface

### Objetivo

Validar a interface web após a implementação e corrigir um problema que impedia a utilização da aplicação.

### Contexto

Após abrir a aplicação no navegador, a página apresentava uma tela/modal contendo os campos:

* Responsável
* Status
* Criado em
* Atualizado em
* Histórico
* Fechar

O botão "Fechar" não permitia sair da tela, fazendo com que a aplicação permanecesse aparentemente travada. O restante da interface aparecia atrás do modal, mas não podia ser utilizado.

### Instrução

Foi informado ao Claude o comportamento observado no navegador e solicitado que identificasse a causa do problema e propusesse uma correção rápida, considerando a limitação de uso restante da sessão.

### Resultado

Claude identificou que a regra CSS `.modal-overlay { display: flex; }` estava sobrescrevendo o comportamento esperado do atributo HTML `hidden`.

Como consequência, os modais que deveriam permanecer ocultos estavam sendo exibidos automaticamente ao carregar a página.

A correção proposta foi adicionar ao final de `static/style.css`:

```css
.modal-overlay[hidden] {
  display: none;
}
```

### Validação

A correção deveria ser validada salvando o arquivo e recarregando a aplicação com `Ctrl+F5`, verificando se os modais permanecem ocultos inicialmente e aparecem somente após a interação correspondente.

### Decisão

Adotar a correção proposta e continuar a validação da interface antes de realizar novas alterações.

### Aprendizado

O problema reforçou a necessidade de validar o comportamento da interface diretamente no navegador, pois o código podia estar estruturado corretamente do ponto de vista funcional, mas uma regra de CSS poderia alterar o comportamento esperado dos elementos HTML.

## 12. Redesign visual com identidade da Convem
Objetivo

Aprimorar a apresentação visual do Incident Hub, aproximando a interface da identidade visual e do posicionamento da Convem, sem alterar as funcionalidades existentes da aplicação.

Contexto

Após a primeira versão funcional estar estabelecida, foi identificado que a interface ainda apresentava um aspecto muito genérico. Como o projeto seria apresentado em um processo seletivo da Convem, foi considerada importante uma evolução visual que transmitisse uma aparência mais profissional e alinhada à empresa.

A alteração deveria ser exclusivamente visual, preservando a lógica existente da aplicação, incluindo:

criação de incidentes;
alteração de status por drag-and-drop;
filtros;
dashboard;
abertura dos detalhes;
histórico;
comunicação com a API.
Instrução

Foi solicitado à IA que analisasse a interface existente e propusesse alterações no templates/index.html e no static/style.css para aproximar a aplicação de uma solução SaaS/fintech profissional, incorporando elementos visuais associados à identidade da Convem.

Também foi solicitado que a alteração não modificasse o static/app.js nem a lógica funcional existente.

Resultado

A interface foi redesenhada mantendo a estrutura funcional existente.

Entre as principais alterações realizadas:

criação de uma identidade visual para a marca na interface;
inclusão do nome "CONVEM" junto ao "Incident Hub";
utilização de uma paleta visual mais moderna;
melhoria do cabeçalho;
criação de maior separação visual entre o header e o restante da aplicação;
aprimoramento dos cards do dashboard;
melhoria visual dos filtros;
aprimoramento das colunas do Kanban;
melhorias nos cards de incidentes;
aprimoramento visual dos modais;
melhoria de espaçamentos, bordas, sombras e tipografia.

As alterações foram concentradas em templates/index.html e static/style.css, preservando o JavaScript existente.

Validação

A aplicação foi executada localmente após as alterações e a interface foi analisada diretamente no navegador.

Durante a validação visual, foi identificado um novo comportamento inesperado relacionado à barra de erro, registrado na seção seguinte.

Decisão

Manter o redesign visual, pois ele melhora significativamente a apresentação da aplicação sem introduzir mudanças na lógica de negócio.

## 13. Barra de erro exibida indevidamente após o redesign
Objetivo

Corrigir um comportamento visual identificado após o redesign da interface, no qual a barra de erro aparecia na página mesmo sem a ocorrência de um erro.

Contexto

A aplicação possui um elemento error-banner destinado a apresentar mensagens de erro somente quando alguma operação falha.

O HTML já utilizava o atributo:

hidden

e o JavaScript controlava a exibição da mensagem por meio da função showError().

Entretanto, após as alterações de CSS, a barra vermelha permanecia visível logo ao carregar a aplicação.

Instrução

Foi informado à IA que a barra vermelha aparecia mesmo quando não havia erro e solicitado que fosse identificada uma correção que preservasse o comportamento existente do JavaScript.

Resultado

Foi identificado que o CSS possuía uma regra visual para .error-banner, mas não possuía uma regra explícita para o estado [hidden].

Como o JavaScript depende do atributo hidden para controlar a exibição da mensagem, a solução escolhida foi adicionar ao static/style.css:

.error-banner[hidden] {
  display: none;
}

Essa abordagem permite que o elemento permaneça oculto inicialmente e continue sendo exibido normalmente quando o JavaScript remover o estado hidden.

Validação

Após salvar o CSS e recarregar a aplicação, a barra deixou de aparecer automaticamente durante o carregamento inicial.

O comportamento de exibição de erros foi preservado, pois o JavaScript continua responsável por alterar o estado do elemento.

Decisão

Manter a correção exclusivamente no CSS, sem modificar o index.html ou o app.js.

A decisão foi tomada para reduzir o risco de regressão e preservar a lógica funcional já implementada.

Aprendizado

Nem todo problema visual exige alteração da lógica JavaScript. A utilização correta dos estados CSS e dos atributos HTML existentes pode resolver problemas de interface sem alterar o comportamento da aplicação.

## 14. Criação de checkpoint antes de novas alterações
Objetivo

Criar um ponto seguro no histórico do Git antes de continuar realizando alterações na interface.

Contexto

Após a conclusão do redesign visual, foi considerado importante preservar uma versão estável da aplicação antes de realizar novas correções.

Instrução

Foi solicitado apoio da IA para verificar o estado do repositório e realizar um commit contendo as alterações do redesign.

Resultado

Os arquivos templates/index.html e static/style.css foram adicionados ao staging e foi criado o commit:

feat: redesign interface do Incident Hub

O commit gerado localmente recebeu o identificador:

9de0281

O arquivo Hackaton Instructions.md, que aparecia como não rastreado, não foi incluído no commit.

Validação

O comando git status confirmou que o branch local estava à frente do origin/main por um commit.

Posteriormente, foi realizada uma tentativa de enviar as alterações para o GitHub.

Decisão

Manter o checkpoint separado dos arquivos não relacionados à implementação, evitando adicionar acidentalmente arquivos ao histórico do projeto.

## 15. Rejeição do primeiro push para o GitHub
Objetivo

Publicar no GitHub o checkpoint criado localmente.

Contexto

Após a criação do commit local, foi executado:

git push origin main

O GitHub rejeitou a operação.

Resultado

O terminal retornou:

! [rejected] main -> main (fetch first)

O erro indicava que o repositório remoto possuía alterações que ainda não estavam presentes no repositório local.

Instrução

Foi solicitado apoio à IA para interpretar o erro e determinar uma forma segura de sincronizar os históricos sem sobrescrever alterações existentes no GitHub.

Decisão

Foi evitado o uso de git push --force, pois isso poderia sobrescrever alterações existentes no repositório remoto.

Foi utilizada a estratégia:

git pull --rebase origin main

seguida novamente por:

git push origin main

Validação

O procedimento foi concluído com sucesso e as alterações locais foram publicadas no GitHub.

Aprendizado

O erro demonstrou a importância de verificar se o repositório remoto possui commits adicionais antes de realizar operações que possam alterar seu histórico.

Também foi reforçada a preferência por estratégias de sincronização seguras, evitando force push quando não há necessidade.

## 16. Estado atual da interface
Resultado

Após as correções, a interface apresenta:

identidade visual mais próxima da Convem;
cabeçalho visualmente separado do restante da aplicação;
dashboard aprimorado;
Kanban com apresentação mais profissional;
modais visualmente aprimorados;
barra de erro inicialmente oculta;
manutenção das funcionalidades existentes;
histórico Git contendo checkpoints das alterações relevantes.
Validação

A aplicação foi executada novamente após as alterações e o comportamento da barra de erro foi validado diretamente no navegador.

Decisão

Continuar priorizando melhorias de qualidade visual e usabilidade, sem realizar alterações desnecessárias na lógica de negócio enquanto as funcionalidades existentes permanecerem estáveis.

## 17. Ajuste de fuso horário 
— timestamps exibidos em UTC cru; corrigido forçando timeZone: "America/Sao_Paulo" no toLocaleString, e depois corrigido de novo porque o backend não enviava indicador de timezone (Z) — bug só aparecia por cache do navegador mascarando a correção real.

## 18. Mudança de regra do dashboard 
— "abertos" passou a somar Open + In Progress por decisão do usuário, não só Open.

## 19. Change Request: comentários e timeline 
— implementação do modelo Comment, add_comment, get_timeline, rotas e testes; decisão de fazer validação dupla (Pydantic min_length + strip() no service) para rejeitar comentários só com espaços.

## 20. Exclusão de incidentes e contador de comentários 
— adicionado por necessidade de usabilidade (não é requisito obrigatório do desafio original nem do CR), DELETE /incidents/{id} e campo comment_count.

## 21. Bugs de frontend pós-edição manual 
— usuário passou a editar HTML/CSS diretamente; ocorreram 2 regressões: botões "Fechar"/"Excluir" com HTML malformado (divs duplicadas) e quebra total do board ao tentar adicionar filtro de ordenação por severidade nas colunas (coluna "In Progress" foi perdida na cópia). Decisão: reverter o filtro de ordenação por severidade — funcionalidade não obrigatória, risco de regressão maior que o benefício perto do code freeze.


## Observações

As conversas originais com as ferramentas de IA permanecem disponíveis para eventual auditoria, conforme as regras do hackathon.

Este documento tem como objetivo registrar as interações e decisões relevantes, e não reproduzir integralmente todas as conversas realizadas durante o desenvolvimento.
