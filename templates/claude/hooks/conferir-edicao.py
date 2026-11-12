"""Hook do Claude Code para projeto Python (evento PostToolUse, ferramentas Edit e Write).

Formata o arquivo que o Claude acabou de editar e devolve ao Claude o que o linter apontar.
Sai com 0 quando não há nada a dizer e com 2 quando há problema: nesse caso o Claude lê a
mensagem e corrige. Copie para .claude/hooks/ do projeto.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SAIDA_COM_PROBLEMA = 2
# Import ou variável ainda sem uso é comum no meio de uma edição; o comando completo confere depois.
IGNORAR_NA_EDICAO = "F401,F841"


def achar_ruff(raiz: Path) -> str | None:
    """Prefere o ruff do ambiente virtual do projeto; depois, o do PATH."""
    for candidato in (raiz / ".venv" / "Scripts" / "ruff.exe", raiz / ".venv" / "bin" / "ruff"):
        if candidato.exists():
            return str(candidato)
    return shutil.which("ruff")


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        dados = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    caminho = str(dados.get("tool_input", {}).get("file_path", ""))
    if not caminho.endswith(".py"):
        return 0
    raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or ".")
    ruff = achar_ruff(raiz)
    if ruff is None:
        sys.stderr.write("conferir-edicao: ruff não encontrado; instale as dependências de dev.\n")
        return 0
    subprocess.run([ruff, "format", caminho], cwd=raiz, check=False, capture_output=True)
    lint = subprocess.run(
        [ruff, "check", "--output-format", "concise", "--ignore", IGNORAR_NA_EDICAO, caminho],
        cwd=raiz,
        check=False,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if lint.returncode != 0:
        sys.stderr.write("O linter apontou problemas neste arquivo. Corrija antes de seguir:\n")
        sys.stderr.write(lint.stdout.strip() + "\n")
        return SAIDA_COM_PROBLEMA
    return 0


if __name__ == "__main__":
    sys.exit(main())
