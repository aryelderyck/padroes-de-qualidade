# Changelog

## 0.10 · 2026-11-13
Último pente fino: os modelos passam a ser executados pelo caminho que a pessoa percorre.
- **Projeto Python instala de verdade:** o `pyproject` modelo ganhou `[build-system]` e a lista de pacotes (sem isso o
  `pip install -e ".[dev]"` falhava com duas pastas na raiz) e deixou de trazer dependências de uma stack específica.
  O CI modelo instala com o mesmo comando, sem pedir um `requirements-dev.txt` que o instalador não cria.
- **Prova de ponta a ponta** (seção [14], Linux e Windows): instala o kit, cria o ambiente virtual, roda cada etapa do
  CI modelo, roda o `conferir.py` e faz o primeiro commit pela trava.
- **Trava do commit:** projeto Node sem o script `conferir` era recusado sem mensagem; agora explica o que falta.
- **Actions:** `checkout`, `setup-python` e `setup-node` na versão 7 e CodeQL na 4, no kit e nos modelos. Prova nova:
  toda action fixada pelo commit, e os modelos com a mesma fixação do CI do kit.
- **CodeQL roda no próprio kit**, com o mesmo arquivo do modelo.
- Versões das ferramentas das provas em `provas/requisitos.txt`, atualizadas pelo Dependabot; atualizações agrupadas
  em um pull request por ecossistema, no kit e no modelo.
- Documentos: referência quebrada no `CONTEXTO.md`, mapa de arquivos em dia, nota sobre `python3` em Linux e macOS,
  E-040 e E-041 no `ERROS.md`. Prova nova: o número da versão é o mesmo em todos os lugares.
- **Ainda não executado:** o Claude Code disparando os hooks, a skill, o estilo de saída e os plugins de segurança; os
  workflows modelo de Node e de Dependabot no GitHub de um projeto.

## 0.9 · 2026-11-12
Correção dos defeitos achados na revisão do kit e fechamento das etapas que dependiam de alguém lembrar.
As provas passaram de 79 para mais de 200 e rodam no CI em Linux e em Windows.
- **O uso do kit é opcional:** só vale quando a pessoa pede. Registrado no `README.md`, no `REGRAS.md` e no `CONTEXTO.md`.
- **Defeitos corrigidos:** modelos fora do formato do Prettier (o comando de conferência de um projeto Node falhava
  por causa dos documentos do próprio kit); regras de JavaScript que atritavam com React e com dados de API; regras de
  Python que acusavam fixture e senha de mentira em testes; `conferir.py` que dizia "corrija" quando faltava a
  ferramenta; hooks que travavam com arquivo apagado; quatro regras citadas sem prova; scripts do kit fora das próprias
  regras; `eslint.config.mjs` com função descontinuada e regras em conflito.
- **Novo `instalar.py`:** monta um projeto (Python ou Node) ou a máquina com um comando, sem sobrescrever o que existe.
- **Trava do commit** (`templates/githooks/pre-commit`) e **trava do pronto** (`conferir-fim`, evento Stop do Claude
  Code): a conferência deixa de depender de lembrar, e arquivo criado por comando também é conferido.
- **Modelos novos:** `.gitignore` (Python e Node), `.gitattributes`, `.prettierignore` e `tsconfig.json` estrito.
- **Provas novas:** toda regra de ESLint do kit precisa de um exemplo ruim; todo código citado nas listas da skill
  precisa de prova; configuração de TypeScript com pacotes reais; ferramentas só no `.venv`; instalador; travas;
  imagem Docker do modelo; todo arquivo do kit no mapa de arquivos.
- Actions fixadas pelo identificador do commit, com Dependabot no kit. `README.md` reescrito com diagrama e
  `docs/INSTALACAO.md` novo. Skill `conferir-codigo` confere a orientação de segurança do projeto e orienta o que
  fazer com cada achado.
- **Ainda não executado:** o Claude Code disparando os hooks, a skill, o estilo de saída e os plugins de segurança.

## 0.8 · 2026-11-12
Conferência obrigatória de todo código, com as regras provadas por execução (`docs/REFERENCIAS.md`, seção 6).
- `PADROES.md`, nova seção 4A: três camadas (hook na edição, comando único, revisão independente), formatação decidida
  pelo formatador, Código Limpo com limite medido, SQL sempre parametrizado, tipos estritos, armadilhas de modelagem e
  de algoritmos e o roteiro de simplificação sem perda de segurança nem de desempenho.
- Nova pasta `provas/` e CI do próprio kit (`.github/workflows/kit.yml`): 17 regras de Python e 17 de JavaScript, os
  dois formatadores, o `mypy` estrito, o `conferir.py`, os dois hooks e os padrões de segurança são conferidos contra
  um exemplo ruim e um bom. Regra automática nova só entra com prova.
- A primeira execução das provas achou três falhas antes de qualquer projeto usar: a regra de aninhamento do ruff
  (`PLR1702`) é experimental e não disparava; o hook de Python acusava a si mesmo; dois modelos estavam fora do formato.
- Modelos novos: `conferir.py`, `editorconfig`, `prettierrc.json`, `eslint.regras.mjs`, `eslint.config.mjs`, os hooks
  `conferir-edicao` (Python e Node) com os `settings` correspondentes, e a skill `conferir-codigo` com `armadilhas.md`
  e `codigo-limpo.md`. `pyproject-python.toml` com 22 grupos de regras, limites e `mypy` estrito.
- `ci-python.yml` e `ci-node.yml` rodam as mesmas etapas do comando único. Checklist, `REGRAS.md` e `CLAUDE.template.md`
  apontam para a conferência.
- **Ainda não executado:** o disparo do hook pelo Claude Code, a skill, o `eslint.config.mjs` com `typescript-eslint`,
  o CI do kit no GitHub e tudo isso no Windows.

## 0.7 · 2026-11-12
Revisão da segurança contra o OWASP, a documentação do Claude Code e artigos revisados por pares
(`docs/REFERENCIAS.md`, seção 5).
- `PADROES.md`, seção 6, reescrita por nível: 6.1 front-end que consome dados de fora, 6.2 quem expõe uma API (os dez
  riscos do OWASP API Security Top 10), 6.3 contas e senhas, 6.4 projeto que chama modelo de IA, 6.5 código de
  segurança escrito com IA. Cada item diz como conferir.
- `CHECKLIST-PRONTO.md`: nível 2 com itens de API que pedem o teste que os prova (rotas fechadas por padrão, posse do
  recurso, campos previstos, limites, CORS e cabeçalhos, revisão independente); dois itens essenciais novos no nível 1.
- `REVISAO.md`, bloco D, com dez perguntas voltadas a API, dado de terceiros, segredo e dependência.
- Novos `templates/claude/claude-security-guidance.md` e `templates/claude/security-patterns.json`, para o plugin
  oficial `security-guidance`. O JSON e as expressões foram validados com casos que devem e que não devem ser pegos;
  **o plugin ainda não foi executado com eles.**
- `CLAUDE.template.md`: limites novos (rota pública, CORS e permissões pedem pergunta; dado de fora nunca como HTML cru).
- `README.md`: as três camadas de revisão de segurança. `PRATICAS.md`: quatro práticas de segurança.

## 0.6 · 2026-11-12
Revisão do kit contra a documentação oficial do Claude Code, exemplos do GitHub e artigos revisados por pares
(fontes em `docs/REFERENCIAS.md`).
- Novo `templates/output-styles/professor.md`: o jeito de ensinar vira um estilo de saída do Claude Code, um só lugar
  para todos os projetos, que liga e desliga com um comando. **Ainda não executado no Claude Code.**
- `CONTEXTO.md`, seção 2: sai o texto longo das regras de ensino (repetido em três lugares) e entra uma tabela com o
  porquê de cada princípio. Conferir o aprendizado pelo que a pessoa faz, não pelo "entendi".
- `CLAUDE.template.md` reescrito (52 linhas): projeto e stack, comandos no começo, estrutura, limites em três níveis
  (sempre, pergunte antes, nunca) e o apontamento para o kit.
- `REGRAS.md`: as 18 regras reescritas como gatilho e ação, com a mesma numeração.
- `CONTEXTO.md`: mapa dos projetos só com o estado geral; decisões de um projeto só saem para a especificação dele;
  sai a stack que contradizia a especificação do painel.
- Novo `docs/REFERENCIAS.md` e cinco práticas candidatas no `PRATICAS.md` (auditoria com `/doctor prompt-audit`, plugin
  `claude-md-management`, conferência automática do mapa de arquivos, kit como plugin).

## 0.5 · 2026-11-12
Objetivo da versão, a pedido da pessoa: regras o mais eficientes possível, sem atrasar os projetos.
- Novo `REGRAS.md`: única leitura de toda sessão (tabela "o que abrir, e quando", as 18 regras que saíram dos erros e
  o critério para registrar erro), com limite de 80 linhas. As regras saíram do `ERROS.md`, que passa a ser de consulta.
- `PADROES.md`, `README.md` e `CLAUDE.template.md`: leitura por seção, conforme o nível e o momento, no lugar de ler
  quatro arquivos inteiros no início de cada etapa. O kit é lido do clone ao lado do projeto (`../padroes-de-qualidade`).
- `PADROES.md`, seção 2: o nível é decidido pelo que o projeto **hospeda** (front-end sem servidor próprio é nível 1) e
  cada nível lista as seções que lhe cabem. Novo **ritmo rápido** para projetos de nível 1 de até uma semana.
- `CHECKLIST-PRONTO.md`: itens essenciais marcados com **[E]**; item novo de teclado, foco e contraste conferidos à mão.
- Registro de erros: só o que pode se repetir, custou mais de uns 15 minutos ou chegou à pessoa, ao repositório ou ao
  ar; ao fechar a tarefa; com **entrada curta** para erro pequeno. Antes era "todo erro, antes de seguir".
- `REVISAO.md` recebeu o que era só do `REVISAO-CRITICA.md` (perguntas que a pessoa pode fazer, como Claude responde,
  gatilhos e três perguntas), e o `REVISAO-CRITICA.md` ficou marcado como obsoleto.
- `PADROES.md`: seção 12 aponta para o mapa dos projetos do `CONTEXTO.md` (um só lugar) e a seção 13 guarda só as
  lições técnicas que não viraram regra geral.
- `CONTEXTO.md`: situação dos projetos atualizada, novo projeto (explorador de campeões de League of Legends, nível 1,
  ritmo rápido), regra "detalhe na primeira vez, referência depois", regra "ensinar com recursos visuais" (de
  2026-11-10), ambiente (Claude Code no VS Code) e decisões de 2026-11-11 e 2026-11-12.
- `ERROS.md`: entradas E-036 (nível errado em projeto de front-end), E-037 (cobrança pela API no Claude Code) e E-038
  (linha do changelog anexada na versão errada).

## 0.4 · 2026-11-10
- `PADROES.md`: nova seção 9A (web pública: indexação, idiomas com `hreflang`, Core Web Vitals, testes de SEO) e três
  lições novas na seção 13.
- `ERROS.md`: entradas E-020 a E-024 (clone desatualizado, endereço com nome de usuário, autorização depois da
  renomeação, leitura recusada, "dados fictícios" sem contexto) e regras 13 a 16.
- `CONTEXTO.md`: decisões de 2026-11-10 (dados reais em execução, SEO e idiomas, nome da conta).
- `PRATICAS.md`: quatro práticas candidatas ligadas a SEO, idiomas e endereço público.
- Kit publicado em `aryelderyck/padroes-de-qualidade` com licença MIT.
- `CONTEXTO.md` e `CLAUDE.template.md`: aprender inglês junto com o código.
- `ERROS.md`: entradas E-025 (verificação com `git grep` que não lê arquivo novo), E-026 (conexão encerrada na primeira chamada à OpenDota) e E-027 (aspas perdidas entre processos do PowerShell 5.1), E-028 (lista de um item só no PowerShell), E-029 (`__type` no `ConvertFrom-Json`) e E-030 (`.ps1` sem BOM), E-031 a E-033 (atualização dos finais de linha) e regras 17 e 18.
- `.gitattributes` com `* text=auto eol=lf` (o kit cumpria a regra 12 só por acaso).
- `CONTEXTO.md` e `CLAUDE.template.md`: regra "cada arquivo com o seu porquê" (explicar antes de criar e manter `docs/MAPA-DE-ARQUIVOS.md` em cada repositório).
- Regra "cada arquivo com o seu porquê": mapa atualizado no mesmo commit do arquivo; temporários ganham uma linha;
  registrada em `PRATICAS.md` como "Em teste (painel)".
- Novo `docs/MAPA-DE-ARQUIVOS.md` do kit, com o porquê de cada arquivo; link no `README.md`. `REVISAO-CRITICA.md` fica marcado como sem justificativa separada (sobreposto ao `REVISAO.md`), a decidir com a pessoa.
- `ERROS.md`: entrada E-034 (commits do kit fora do formato `docs(kit):`).
- `ERROS.md`: entrada E-035 (identidade do git da máquina nos commits).

## 0.3 · 2026-11-09
- Novo `REVISAO.md`: perguntas de revisão por momento (design, código, otimização, segurança, testes, entrega,
  aprendizado, comunicação, operação) e formato curto "Decisão / Alternativas / Por que / Risco".
- Novo `CONTEXTO.md`: contexto geral seguro para repositório público, como ensinar, mapa dos projetos, decisões,
  glossário vivo e dificuldades conhecidas.
- Novo `PRATICAS.md`: boas práticas candidatas com ciclo de vida (Candidata, Em teste, Adotada, Descartada).
- `README.md`: mapa "momento → arquivo" e protocolo de consulta e edição por Claude.
- `PADROES.md`: princípio "questione antes de entregar" e regra de que o documento é vivo.
- `CLAUDE.template.md` e `CHECKLIST-PRONTO.md`: passam a exigir a revisão de simplicidade.

## 0.2 · 2026-11-09
- Novo `ERROS.md`: catálogo de erros com modelo de registro, 12 regras de prevenção e 19 entradas retroativas
  (repositórios antigos, landing, planejamento e esta sessão).
- `PADROES.md`: princípio "todo erro é registrado" e seção 13 resumida, apontando para o catálogo.
- `CLAUDE.template.md` e `CHECKLIST-PRONTO.md`: passam a exigir o registro de erros.

## 0.1 · 2026-11-09
- Primeira versão: documento mestre, checklist por nível, modelos de `CLAUDE.md` e diário de aprendizado,
  modelos de CI (Python e Node), CodeQL, Dependabot, `pyproject` e Dockerfile.
- Lições iniciais vindas da landing page.
- Pendente: validar os modelos em um projeto real (nenhum foi executado).
