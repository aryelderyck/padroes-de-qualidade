# padroes-de-qualidade

Kit de padrões que mantém o mesmo nível de qualidade em todos os projetos de portfólio do Aryel
(landing page, painel de Dota 2, e-commerce, AtendeFlow e os próximos).

> Versão **0.8**. Os modelos de CI, Docker e `pyproject` ainda **não foram executados** em um projeto real.
> O primeiro projeto que usar cada um deve validar e corrigir o modelo aqui.

## O que tem aqui

Por que cada arquivo existe, onde fica e que alternativas havia: [`docs/MAPA-DE-ARQUIVOS.md`](docs/MAPA-DE-ARQUIVOS.md).

| Arquivo | Para que serve |
| --- | --- |
| [`REGRAS.md`](REGRAS.md) | **A única leitura de toda sessão:** o que abrir em cada momento, as 18 regras que saíram dos erros e quando registrar um erro |
| [`PADROES.md`](PADROES.md) | Documento mestre, lido por seção: princípios, níveis e ritmo, testes, CI/CD, segurança, LGPD, API, front-end |
| [`CONTEXTO.md`](CONTEXTO.md) | Quem é a pessoa, objetivos, restrições, como ensinar, mapa dos projetos, glossário e dificuldades |
| [`REVISAO.md`](REVISAO.md) | Perguntas de revisão por momento: é a melhor maneira? dá para ter menos código? dá para otimizar sem quebrar? |
| [`PRATICAS.md`](PRATICAS.md) | Boas práticas candidatas, com ciclo de vida até serem adotadas ou descartadas |
| [`ERROS.md`](ERROS.md) | Catálogo de erros, de consulta: índice e registro com causa raiz e prevenção |
| [`templates/CHECKLIST-PRONTO.md`](templates/CHECKLIST-PRONTO.md) | Definição de pronto, por nível, com campo de evidência |
| [`templates/CLAUDE.template.md`](templates/CLAUDE.template.md) | `CLAUDE.md` inicial de cada repositório novo |
| [`templates/output-styles/professor.md`](templates/output-styles/professor.md) | Estilo de saída do Claude Code com o jeito de ensinar (instalado uma vez por máquina) |
| [`templates/claude/`](templates/claude/) | Para o `.claude/` de cada projeto: orientação e padrões de segurança do plugin `security-guidance`, e o hook que formata e confere cada arquivo editado |
| [`templates/skills/conferir-codigo/`](templates/skills/conferir-codigo/) | Skill de revisão independente do código, com a lista de armadilhas e o Código Limpo adotado (instalada uma vez por máquina) |
| `templates/conferir.py`, `eslint.regras.mjs`, `eslint.config.mjs`, `prettierrc.json`, `editorconfig` | Formatação, linter com limites e comando único de conferência, por linguagem |
| [`provas/`](provas/) | Exemplo ruim e exemplo bom por linguagem, e o script que prova que cada regra automática funciona |
| [`templates/APRENDIZADOS.template.md`](templates/APRENDIZADOS.template.md) | Diário de aprendizado, preenchido a cada etapa |
| [`templates/pyproject-python.toml`](templates/pyproject-python.toml) | Configuração de ruff, pytest e cobertura para projetos Python |
| [`templates/Dockerfile.python`](templates/Dockerfile.python) e [`templates/dockerignore`](templates/dockerignore) | Imagem Docker em múltiplos estágios, sem root |
| [`templates/github/`](templates/github/) | Workflows de CI (Python e Node), CodeQL e Dependabot |

## O que ler, e quando

O kit é lido **aos pedaços**. Toda sessão começa só pelo [`REGRAS.md`](REGRAS.md), que tem a tabela "o que abrir, e
quando" e manda abrir os outros arquivos por seção, no momento em que servem. Ler tudo no início de cada sessão gastava
contexto e tempo sem melhorar o resultado.

## Estilo de saída Professor

O jeito de ensinar (explicar cada arquivo e cada decisão, sintaxe nova linha por linha, trechos para a pessoa escrever,
inglês junto) não fica mais repetido no `CLAUDE.md` de cada projeto. Fica num **estilo de saída** do Claude Code, que
vale para todos os projetos da máquina e liga ou desliga com um comando.

> **Ainda não testado.** O arquivo segue o formato da documentação oficial, mas não foi executado no Claude Code.
> O primeiro uso deve conferir os três passos abaixo e corrigir aqui o que não bater.

1. Instalar, uma vez por máquina (PowerShell, na pasta do kit):
   `New-Item -ItemType Directory -Force "$HOME\.claude\output-styles" | Out-Null; Copy-Item templates\output-styles\professor.md "$HOME\.claude\output-styles\"`
2. Reabrir o Claude Code e escolher o estilo: `/output-style professor` (no VS Code, digite `/` e escolha **Output styles**).
3. Para uma sessão sem aula, só de execução: `/output-style default`. Para voltar: `/output-style professor`.

O Claude Code também traz estilos prontos: **Learning** (explica e deixa trechos para a pessoa escrever, em inglês) e
**Explanatory** (só explica). O Professor é o Learning adaptado ao que a pessoa pediu.

## Conferência de código: três camadas

Regras em `PADROES.md`, seção 4A. Todo código passa por formatação, linter, tipos e testes, e por uma revisão feita
por quem não escreveu.

**O que foi executado de verdade no kit** (`python provas/conferir-provas.py`, que também roda no CI do kit): as regras
do ruff e do ESLint pegando o exemplo ruim e liberando o bom; os dois formatadores; o `mypy` estrito; o `conferir.py`;
e os dois scripts de hook, alimentados com a mesma entrada que o Claude Code envia.
**O que ainda não foi executado:** o Claude Code disparando o hook a partir do `settings.json`; a skill
`/conferir-codigo`; o `eslint.config.mjs` com o `typescript-eslint`; e tudo isso no Windows.

Em cada projeto:

1. **Formatação e regras.** Copie `templates/editorconfig` como `.editorconfig`.
   Python: use o `templates/pyproject-python.toml` e copie `templates/conferir.py` para a raiz.
   Node: copie `eslint.regras.mjs` e `eslint.config.mjs` para a raiz, `prettierrc.json` como `.prettierrc.json`, e crie
   o script `"conferir": "prettier --check . && eslint . && tsc --noEmit && vitest run"` no `package.json`.
2. **Hook de edição.** Copie `templates/claude/settings.python.json` (ou `settings.node.json`) como
   `.claude/settings.json` e o `conferir-edicao.py` (ou `.mjs`) para `.claude/hooks/`. Se o projeto já tiver
   `settings.json`, junte só o bloco `hooks`. No Linux e no macOS, troque `python` por `python3` se for preciso.
3. **CI.** Use `templates/github/ci-python.yml` ou `ci-node.yml`: são as mesmas etapas do comando único.

Uma vez por máquina, a skill de revisão (PowerShell, na pasta do kit):
`New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null; Copy-Item -Recurse -Force templates\skills\conferir-codigo "$HOME\.claude\skills\"`

Depois, no Claude Code: `/conferir-codigo` (confere a branch atual) ou `/conferir-codigo src/arquivo.py`.

## Segurança: revisão que não depende de quem escreveu

Quem usa assistente de IA tende a achar o código mais seguro do que ele é (`docs/REFERENCIAS.md`, seção 5). Por isso o
kit pede revisão independente, em três camadas. **Nenhuma delas foi executada ainda com os modelos do kit.**

1. **Enquanto o Claude escreve:** plugin oficial `security-guidance`. Instalar uma vez (no VS Code, em *Manage plugins*;
   no terminal, `/plugin install security-guidance@claude-plugins-official`). Precisa de Python no computador. A
   conferência de padrões a cada edição não gasta uso; as revisões de fim de turno e de commit gastam.
   Em cada projeto, copie `templates/claude/claude-security-guidance.md` e `templates/claude/security-patterns.json`
   para a pasta `.claude/` e ajuste a lista de rotas públicas.
2. **Antes de dizer "pronto":** `/security-review` na branch (item da checklist do nível 2).
3. **No CI:** `pip-audit` ou `npm audit`, CodeQL e, no GitHub, *secret scanning* com *push protection*.

As regras em si estão no `PADROES.md`, seção 6, por nível.

## Ferramentas do Claude Code que vale usar junto

- `/doctor prompt-audit`: o próprio Claude Code confere os arquivos de instrução (desatualizados, contraditórios, que
  apontam para arquivo que não existe) e propõe as correções.
- Plugin `claude-md-management`, da Anthropic: avalia o `CLAUDE.md` e propõe melhorias como diff.
- De onde vieram as regras do kit (documentação, exemplos e artigos): [`docs/REFERENCIAS.md`](docs/REFERENCIAS.md).

## Como Claude consulta e edita o kit

- **Consulta:** o kit fica clonado ao lado de cada projeto (`../padroes-de-qualidade`) e o `CLAUDE.md` do projeto aponta
  para ele. Sem o clone, os arquivos são lidos pelo link "raw" do GitHub.
- **Edição:** Claude **pode e deve** acrescentar erros, dificuldades, perguntas, práticas e termos do glossário. Regras:
  acrescente em vez de apagar (marque como obsoleto, com data e motivo), um assunto por commit com mensagem
  `tipo(kit): o que mudou` (`docs`, `feat`, `fix`, `test`, `refactor` ou `chore`; as provas conferem o formato), anote no `CHANGELOG.md`, e peça aprovação da pessoa antes de mudar a estrutura dos arquivos.
- **Privacidade:** o repositório é público; nada sensível sobre a pessoa entra aqui (ver `CONTEXTO.md`).

## Como começar um projeto novo

1. Crie o repositório vazio no GitHub (nome em minúsculas, com hífens).
2. Defina o **nível** (1, 2 ou 3) e o **ritmo** (rápido ou completo) do projeto com a seção 2 do `PADROES.md`.
3. Copie para o projeto: `CLAUDE.template.md` como `CLAUDE.md`, `CHECKLIST-PRONTO.md` e `APRENDIZADOS.template.md` como `docs/` e `APRENDIZADOS.md`, e os arquivos `github/` e de stack que usar (em `.github/` e na raiz).
4. Preencha os `[colchetes]` do `CLAUDE.md`.
5. No GitHub, ative Dependabot alerts, secret scanning e push protection, e exija o CI antes de mesclar na `main`.
6. Ao fim de cada etapa: atualize o `APRENDIZADOS.md` e marque a checklist.

Frase para abrir uma sessão do Claude Code em um projeto novo:

> Leia o CLAUDE.md e o REGRAS.md do kit. Este projeto é de nível [N], ritmo [rápido ou completo]. Antes de escrever código, proponha o desenho e espere minha aprovação.

## Como este kit evolui

Erro que ensina vira uma entrada no `ERROS.md` ao fechar a tarefa; se revelar uma regra geral, ela entra no `REGRAS.md`.
Práticas novas entram em `PRATICAS.md`, perguntas úteis em `REVISAO.md`, dificuldades e decisões em `CONTEXTO.md`.
Mudanças do kit ficam no `CHANGELOG.md`.
Este repositório deve ser **público**: ele não contém segredos e o `CLAUDE.md` dos projetos o lê pelo link "raw".
