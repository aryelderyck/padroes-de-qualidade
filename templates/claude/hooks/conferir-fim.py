"""Hook do Claude Code para projeto Python (evento Stop): a trava do "pronto".

Quando o Claude vai encerrar a resposta, confere a formatação e o linter dos arquivos Python
alterados ou novos (inclusive os criados por comando, que escapam do hook de edição). Com problema,
sai com 2: o Claude lê a mensagem e continua até corrigir. Só trava uma vez por tentativa de parar
(campo stop_hook_active), para não prender o Claude num laço. Copie para .claude/hooks/ do projeto.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SAIDA_COM_PROBLEMA = 2


def achar(ferramenta: str, raiz: Path) -> str | None:
    """Prefere a ferramenta do ambiente virtual do projeto; depois, a do PATH."""
    for pasta, sufixo in ((".venv/Scripts", ".exe"), (".venv/bin", "")):
        candidato = raiz / pasta / f"{ferramenta}{sufixo}"
        if candidato.exists():
            return str(candidato)
    return shutil.which(ferramenta)


def rodar(comando: list[str], raiz: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        comando, cwd=raiz, check=False, capture_output=True, encoding="utf-8", errors="replace"
    )


def arquivos_alterados(git: str, raiz: Path) -> list[str]:
    """Arquivos Python modificados, novos ou já preparados para commit, que ainda existem."""
    nomes: set[str] = set()
    for argumentos in (
        ["ls-files", "--modified", "--others", "--exclude-standard"],
        ["diff", "--name-only", "--cached"],
    ):
        nomes |= set(rodar([git, *argumentos], raiz).stdout.splitlines())
    return sorted(nome for nome in nomes if nome.endswith(".py") and (raiz / nome).is_file())


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        dados = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if not isinstance(dados, dict) or dados.get("stop_hook_active"):
        return 0
    raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or ".")
    git, ruff = shutil.which("git"), achar("ruff", raiz)
    if git is None or ruff is None:
        return 0
    arquivos = arquivos_alterados(git, raiz)
    if not arquivos:
        return 0
    formato = rodar([ruff, "format", "--check", *arquivos], raiz)
    lint = rodar([ruff, "check", "--output-format", "concise", *arquivos], raiz)
    if formato.returncode == 0 and lint.returncode == 0:
        return 0
    sys.stderr.write(
        "Antes de encerrar, corrija os arquivos alterados e rode `python conferir.py`:\n"
    )
    if formato.returncode != 0:
        sys.stderr.write("Fora do formato (rode `ruff format`):\n" + formato.stdout.strip() + "\n")
    if lint.returncode != 0:
        sys.stderr.write(lint.stdout.strip() + "\n")
    return SAIDA_COM_PROBLEMA


if __name__ == "__main__":
    sys.exit(main())
