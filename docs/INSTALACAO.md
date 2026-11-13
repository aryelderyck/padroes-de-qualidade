# Instalação e uso

O uso do kit é opcional. Nada aqui roda sem você instalar, e tudo pode ser desligado (seção 5).

## 1. Antes

- Clone o kit ao lado dos projetos: a pasta `padroes-de-qualidade` fica vizinha da pasta de cada projeto.
- Precisa de Python 3.12 ou mais novo para o instalador. Projeto Node precisa também do Node.
- Crie o repositório do projeto e rode `git init` (ou clone) **antes** de instalar, para a trava do commit ser ligada.

## 2. Num projeto

Na pasta do kit, **primeiro olhe** (não escreve nada) e **depois instale**:

```text
python instalar.py avaliar ..\meu-projeto --tipo python
python instalar.py projeto ..\meu-projeto --tipo python
```

Para projeto Node, use `--tipo node` e **crie o projeto antes** (por exemplo, com `npm create vite@latest`): o gerador
recusa pasta que já tem arquivos, e as configurações dele precisam chegar primeiro.

### A avaliação de risco

O `avaliar` e o `projeto` mostram o que seria criado, mantido ou deixado de fora, e uma lista de riscos:

| Nível | Exemplos | O que o instalador faz |
| --- | --- | --- |
| ALTO | Modo completo; projeto Node sem `package.json`; mais de 50 apontamentos do linter no código que já existe | **Para e não instala.** Resolva, ou repita com `--aceitar-risco` |
| MÉDIO | Pasta sem git; mudanças sem commit; arquivo de regras que já existe (`pyproject.toml`, `eslint.config.js`, `tsconfig`), em que as regras do kit só valem depois de você juntar; alguns apontamentos no código que já existe | Instala e diz o que fazer |
| BAIXO | Nada encontrado, ou algo que não deu para medir | Instala |

Antes de instalar num projeto que já tem código, faça um commit: assim o `git status` mostra só o que o kit trouxe.

### Os dois modos

| | Essencial (padrão) | Completo (`--modo completo`) |
| --- | --- | --- |
| Formatação e indentação | Sim | Sim |
| Linter | Erros de lógica e regras de segurança | Soma limites de tamanho, número mágico, código comentado, `print`, estilo |
| Tipos | Conferidos sem o modo estrito | Estritos (`mypy --strict`; `typescript-eslint` no conjunto mais estrito) |
| Hook de edição do Claude Code | Só formata; nunca devolve nada ao Claude | Formata e devolve ao Claude o que o linter apontou |
| Trava do pronto | Desligada | Ligada |
| Trava do commit | Formatação e linter | Formatação, linter, tipos e testes |
| CI | Cobertura só informada; auditoria de dependências só avisa | Cobertura mínima de 80%; auditoria reprova |
| Padrões por texto do plugin de segurança e CodeQL | Não instalados | Instalados (o CodeQL é gratuito só em repositório público) |

O modo completo pega mais e também acusa mais código que está certo, e a trava do pronto e o linter a cada edição ainda
não rodaram numa sessão real do Claude Code. Por isso ele conta como risco alto e pede `--aceitar-risco`.

**Trocar de modo depois:** rode o instalador de novo com o outro `--modo` e `--forcar`, depois de apagar só os
arquivos que quer trocar (seção 6). Para mudar partes: em Node, a primeira linha do `eslint.regras.mjs`; a trava do
commit, com `git config kit.trava completa` (ou `git config --unset kit.trava`).

### O que é instalado

O instalador lista cada arquivo como `criado`, `mantido (já existia)`, `substituído` ou `não copiado`. Ele nunca
sobrescreve sem `--forcar`. O que ele coloca no projeto:

| O quê | Onde fica | Para quê |
| --- | --- | --- |
| Formatação e regras | `.editorconfig`; `pyproject.toml` e `conferir.py` (Python); `eslint.config.mjs`, `eslint.regras.mjs`, `.prettierrc.json`, `.prettierignore` e `tsconfig.json` (Node) | Indentação, linter, tipos e o comando único |
| Hooks do Claude Code | `.claude/settings.json` e `.claude/hooks/` | Formatar cada arquivo editado (no completo, também conferir) |
| Trava do commit | `.githooks/pre-commit` | Recusar o commit que não passa na conferência |
| Segurança | `.claude/claude-security-guidance.md` (no completo, também `.claude/security-patterns.json`) | Orientação para o plugin `security-guidance` |
| Git | `.gitignore` e `.gitattributes` | Segredos e caches fora do repositório; fim de linha igual em toda máquina |
| CI | `.github/workflows/ci.yml` e `.github/dependabot.yml` (no completo, também `codeql.yml`) | As mesmas etapas da conferência e atualização de dependências |
| Documentos | `CLAUDE.md`, `APRENDIZADOS.md` e `docs/CHECKLIST-PRONTO.md` | Contexto do projeto, diário de aprendizado e definição de pronto |

Se o projeto já tem configuração de ESLint ou de TypeScript (o Vite cria as duas), o kit **não cria uma segunda**:
copia só o `eslint.regras.mjs` e diz a linha a acrescentar na configuração que já existe.

Depois de instalar:

1. Preencha os `[colchetes]` do `CLAUDE.md` e, na orientação de segurança, a lista de rotas públicas.
2. **Python:** no `pyproject.toml`, troque o nome do projeto e liste as dependências. Crie o ambiente
   (`python -m venv .venv`) e instale as ferramentas (`.venv\Scripts\pip install -e ".[dev]"`; em Linux e macOS,
   `.venv/bin/pip`). O comando único é `python conferir.py`. Se a pasta do código não se chamar `app`, troque o nome
   nos dois lugares do `pyproject.toml` marcados com "pasta do código".
3. **Node:** instale `eslint`, `@eslint/js`, `typescript-eslint`, `typescript`, `globals` e `prettier` como
   dependências de desenvolvimento e crie no `package.json` os scripts
   `"conferir:rapido": "prettier --check . && eslint . --max-warnings 0"` e
   `"conferir": "npm run conferir:rapido && tsc --noEmit && vitest run"`.
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

**Linux e macOS:** os hooks do `.claude/settings.json` de projeto Python chamam o comando `python`. Se na máquina só
existe `python3`, o hook não roda e o Claude Code não avisa: troque `"command": "python"` por `"command": "python3"`
nesse arquivo. O instalador já faz essa troca quando roda numa máquina sem o comando `python`. A trava do commit e o CI não dependem disso (procuram `.venv`, `python` e `python3`).

## 4. O que cada conferência faz

| Conferência | Quando roda | O que acontece se achar problema |
| --- | --- | --- |
| Hook de edição | Depois de cada arquivo que o Claude edita | Corrige a formatação; no modo completo, também devolve ao Claude o que o linter apontou |
| Trava do pronto (só no completo) | Quando o Claude vai encerrar a resposta | O Claude continua até corrigir os arquivos alterados (uma vez por tentativa, para não ficar em laço) |
| Trava do commit | Em todo `git commit` (formatação e linter; tudo, com `git config kit.trava completa`) | O commit é recusado e a tela diz em qual etapa falhou |
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

**Quem mantém o kit:** o Dependabot abre no kit um pull request por semana com as actions e as ferramentas novas. As
provas recusam o pull request de actions enquanto os modelos de `templates/github/` não tiverem a mesma fixação do
`kit.yml`: leve a mesma linha `uses:` para os modelos, no mesmo pull request.
