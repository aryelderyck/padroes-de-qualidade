# padroes-de-qualidade

Kit de padrões que mantém o mesmo nível de qualidade em todos os projetos de portfólio do Aryel
(landing page, painel de Dota 2, e-commerce, AtendeFlow e os próximos).

> Versão **0.5**. Os modelos de CI, Docker e `pyproject` ainda **não foram executados** em um projeto real.
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
| [`templates/APRENDIZADOS.template.md`](templates/APRENDIZADOS.template.md) | Diário de aprendizado, preenchido a cada etapa |
| [`templates/pyproject-python.toml`](templates/pyproject-python.toml) | Configuração de ruff, pytest e cobertura para projetos Python |
| [`templates/Dockerfile.python`](templates/Dockerfile.python) e [`templates/dockerignore`](templates/dockerignore) | Imagem Docker em múltiplos estágios, sem root |
| [`templates/github/`](templates/github/) | Workflows de CI (Python e Node), CodeQL e Dependabot |

## O que ler, e quando

O kit é lido **aos pedaços**. Toda sessão começa só pelo [`REGRAS.md`](REGRAS.md), que tem a tabela "o que abrir, e
quando" e manda abrir os outros arquivos por seção, no momento em que servem. Ler tudo no início de cada sessão gastava
contexto e tempo sem melhorar o resultado.

## Como Claude consulta e edita o kit

- **Consulta:** o kit fica clonado ao lado de cada projeto (`../padroes-de-qualidade`) e o `CLAUDE.md` do projeto aponta
  para ele. Sem o clone, os arquivos são lidos pelo link "raw" do GitHub.
- **Edição:** Claude **pode e deve** acrescentar erros, dificuldades, perguntas, práticas e termos do glossário. Regras:
  acrescente em vez de apagar (marque como obsoleto, com data e motivo), um assunto por commit com mensagem
  `docs(kit): o que mudou`, anote no `CHANGELOG.md`, e peça aprovação da pessoa antes de mudar a estrutura dos arquivos.
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
