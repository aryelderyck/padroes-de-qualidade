# Instalação e uso

O uso do kit é opcional. Nada aqui roda sem você instalar, e tudo pode ser desligado (seção 5).

## 1. Antes

- Clone o kit ao lado dos projetos: a pasta `padroes-de-qualidade` fica vizinha da pasta de cada projeto.
- Precisa de Python 3.12 ou mais novo para o instalador. Projeto Node precisa também do Node.
- Crie o repositório do projeto e rode `git init` (ou clone) **antes** de instalar, para a trava do commit ser ligada.

## 2. Num projeto

Na pasta do kit:

```text
python instalar.py projeto ..\meu-projeto --tipo python
python instalar.py projeto ..\meu-projeto --tipo node
```

O instalador lista cada arquivo como `criado`, `mantido (já existia)` ou `substituído`. Ele nunca sobrescreve sem
`--forcar`. O que ele coloca no projeto:

| O quê | Onde fica | Para quê |
| --- | --- | --- |
| Formatação e regras | `.editorconfig`; `pyproject.toml` e `conferir.py` (Python); `eslint.config.mjs`, `eslint.regras.mjs`, `.prettierrc.json`, `.prettierignore` e `tsconfig.json` (Node) | Indentação, linter com limites de Código Limpo, tipos estritos e o comando único |
| Hooks do Claude Code | `.claude/settings.json` e `.claude/hooks/` | Formatar e conferir cada arquivo editado, e conferir os alterados antes de encerrar |
| Trava do commit | `.githooks/pre-commit` | Recusar o commit que não passa na conferência |
| Segurança | `.claude/claude-security-guidance.md` e `.claude/security-patterns.json` | Orientação e padrões para o plugin `security-guidance` |
| Git | `.gitignore` e `.gitattributes` | Segredos e caches fora do repositório; fim de linha igual em toda máquina |
| CI | `.github/workflows/ci.yml`, `codeql.yml` e `.github/dependabot.yml` | As mesmas etapas da conferência, análise de segurança e atualização de dependências |
| Documentos | `CLAUDE.md`, `APRENDIZADOS.md` e `docs/CHECKLIST-PRONTO.md` | Contexto do projeto, diário de aprendizado e definição de pronto |

Depois de instalar:

1. Preencha os `[colchetes]` do `CLAUDE.md` e, na orientação de segurança, a lista de rotas públicas.
2. **Python:** crie o ambiente (`python -m venv .venv`) e instale as dependências de desenvolvimento
   (`.venv\Scripts\pip install -e ".[dev]"`). O comando único é `python conferir.py`.
3. **Node:** instale `eslint`, `@eslint/js`, `typescript-eslint`, `typescript`, `globals` e `prettier` como
   dependências de desenvolvimento e crie no `package.json` o script
   `"conferir": "prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run"`.
   Se o gerador do projeto já criou um `tsconfig.json`, o instalador o mantém: confira as opções com as do kit.
4. No GitHub, ative Dependabot alerts, secret scanning e push protection.
5. Projeto de nível 2 com Docker: copie à mão `templates/Dockerfile.python` e `templates/dockerignore`.

## 3. Na máquina (uma vez)

```text
python instalar.py maquina
```

Instala em `~/.claude` a skill de revisão `conferir-codigo` e o estilo de saída `professor`. No Claude Code:

- `/output-style professor` liga o jeito de ensinar; `/output-style default` desliga.
- `/conferir-codigo` pede a revisão independente da branch atual; `/conferir-codigo src/arquivo.py`, de um arquivo.

Para a camada de segurança, instale também o plugin oficial `security-guidance` (no VS Code, em *Manage plugins*).
Ele precisa de Python. A conferência de padrões a cada edição não gasta uso; as revisões de fim de turno e de commit
gastam. O comando `/security-review` confere a branch antes de dizer "pronto".

## 4. O que cada conferência faz

| Conferência | Quando roda | O que acontece se achar problema |
| --- | --- | --- |
| Hook de edição | Depois de cada arquivo que o Claude edita | Corrige a formatação e devolve ao Claude o que o linter apontou |
| Trava do pronto | Quando o Claude vai encerrar a resposta | O Claude continua até corrigir os arquivos alterados (uma vez por tentativa, para não ficar em laço) |
| Trava do commit | Em todo `git commit` | O commit é recusado e a tela diz em qual etapa falhou |
| CI | Em todo envio ao GitHub | O envio fica marcado como reprovado |
| `/conferir-codigo` | Quando você pede | Relatório com achados, a entrada que quebra e o veredito |

## 5. Como desligar

- **Trava do commit:** `git config --unset core.hooksPath`. Só para um commit de emergência: `git commit --no-verify`
  (o CI confere depois do mesmo jeito).
- **Hooks do Claude Code:** apague o bloco `hooks` de `.claude/settings.json`, ou o arquivo.
- **Estilo Professor:** `/output-style default`.
- **Tudo:** apague os arquivos que o instalador listou. O `.kit-versao` diz qual versão foi instalada.

## 6. Atualizar

Rode `git pull` no kit e o instalador de novo. Ele mantém o que você editou. Para trocar um arquivo pelo modelo novo,
apague-o antes ou use `--forcar` (que substitui **todos**, inclusive o `CLAUDE.md` preenchido: prefira apagar só o que
quer trocar).
