# padroes-de-qualidade

Kit de padrões que mantém o mesmo nível de qualidade em todos os projetos de portfólio do Aryel
(landing page, painel de Dota 2, e-commerce, AtendeFlow e os próximos).

> Versão **0.3**. Os modelos de CI, Docker e `pyproject` ainda **não foram executados** em um projeto real.
> O primeiro projeto que usar cada um deve validar e corrigir o modelo aqui.

## O que tem aqui

| Arquivo | Para que serve |
| --- | --- |
| [`PADROES.md`](PADROES.md) | Documento mestre: princípios, níveis, testes, CI/CD, segurança, LGPD, API, front-end, aprendizado e lições |
| [`CONTEXTO.md`](CONTEXTO.md) | Quem é a pessoa, objetivos, restrições, como ensinar, mapa dos projetos, glossário e dificuldades |
| [`REVISAO.md`](REVISAO.md) | Perguntas de revisão por momento: é a melhor maneira? dá para ter menos código? dá para otimizar sem quebrar? |
| [`PRATICAS.md`](PRATICAS.md) | Boas práticas candidatas, com ciclo de vida até serem adotadas ou descartadas |
| [`ERROS.md`](ERROS.md) | Catálogo de erros: regras que saíram deles, índice e registro com causa raiz e prevenção |
| [`templates/CHECKLIST-PRONTO.md`](templates/CHECKLIST-PRONTO.md) | Definição de pronto, por nível, com campo de evidência |
| [`templates/CLAUDE.template.md`](templates/CLAUDE.template.md) | `CLAUDE.md` inicial de cada repositório novo |
| [`templates/APRENDIZADOS.template.md`](templates/APRENDIZADOS.template.md) | Diário de aprendizado, preenchido a cada etapa |
| [`templates/pyproject-python.toml`](templates/pyproject-python.toml) | Configuração de ruff, pytest e cobertura para projetos Python |
| [`templates/Dockerfile.python`](templates/Dockerfile.python) e [`templates/dockerignore`](templates/dockerignore) | Imagem Docker em múltiplos estágios, sem root |
| [`templates/github/`](templates/github/) | Workflows de CI (Python e Node), CodeQL e Dependabot |

## Mapa de consulta: em que momento abrir qual arquivo

| Momento | Arquivo |
| --- | --- |
| Início de projeto ou de sessão | `CONTEXTO.md`, `PADROES.md` (nível e regras) e as regras do `ERROS.md` |
| Escolher tema, abordagem ou stack | `REVISAO.md` bloco A, `PRATICAS.md` |
| Escrever código | `REVISAO.md` blocos B e D |
| Otimizar ou refatorar | `REVISAO.md` bloco C |
| Testar | `PADROES.md` seção 4 e `REVISAO.md` bloco E |
| Antes de dizer "pronto" | `REVISAO.md` bloco F e `templates/CHECKLIST-PRONTO.md` |
| Apareceu um erro | `ERROS.md` (consultar se já aconteceu e registrar) |
| Ensinar um conceito | `CONTEXTO.md` (glossário e dificuldades) e `REVISAO.md` bloco G |

## Como Claude consulta e edita o kit

- **Consulta:** em cada projeto, o `CLAUDE.md` aponta para os arquivos pelo link "raw" do GitHub. Em uma sessão com acesso ao
  repositório, Claude pode também clonar o kit e ler os arquivos locais.
- **Edição:** Claude **pode e deve** acrescentar erros, dificuldades, perguntas, práticas e termos do glossário. Regras:
  acrescente em vez de apagar (marque como obsoleto, com data e motivo), um assunto por commit com mensagem
  `docs(kit): o que mudou`, anote no `CHANGELOG.md`, e peça aprovação da pessoa antes de mudar a estrutura dos arquivos.
- **Privacidade:** o repositório é público; nada sensível sobre a pessoa entra aqui (ver `CONTEXTO.md`).

## Como começar um projeto novo

1. Crie o repositório vazio no GitHub (nome em minúsculas, com hífens).
2. Defina o **nível** do projeto (1, 2 ou 3) com a tabela da seção 2 do `PADROES.md`.
3. Copie para o projeto: `CLAUDE.template.md` como `CLAUDE.md`, `CHECKLIST-PRONTO.md` e `APRENDIZADOS.template.md` como `docs/` e `APRENDIZADOS.md`, e os arquivos `github/` e de stack que usar (em `.github/` e na raiz).
4. Preencha os `[colchetes]` do `CLAUDE.md`.
5. No GitHub, ative Dependabot alerts, secret scanning e push protection, e exija o CI antes de mesclar na `main`.
6. Ao fim de cada etapa: atualize o `APRENDIZADOS.md` e marque a checklist.

Frase para abrir uma sessão do Claude Code em um projeto novo:

> Leia o CLAUDE.md e o PADROES.md (link dentro do CLAUDE.md). Este projeto é de nível [N]. Antes de escrever código, proponha o desenho e espere minha aprovação.

## Como este kit evolui

Todo erro vira uma entrada no `ERROS.md` no mesmo dia; se revelar uma regra, ela sobe para o `PADROES.md`.
Práticas novas entram em `PRATICAS.md`, perguntas úteis em `REVISAO.md`, dificuldades e decisões em `CONTEXTO.md`.
Mudanças do kit ficam no `CHANGELOG.md`.
Este repositório deve ser **público**: ele não contém segredos e o `CLAUDE.md` dos projetos o lê pelo link "raw".
