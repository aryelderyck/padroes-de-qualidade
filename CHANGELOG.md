# Changelog

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
