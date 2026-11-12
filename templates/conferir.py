"""Conferência completa do projeto, em um comando só: `python conferir.py`.

Roda, nesta ordem, formatação, linter, tipos e testes, e para na primeira etapa que falhar.
É o mesmo conjunto de etapas do CI: se passa aqui, passa lá. Copie para a raiz do projeto.
"""

import shutil
import subprocess
import sys

ETAPAS: list[tuple[str, list[str]]] = [
    ("Formatação (ruff format)", ["ruff", "format", "--check", "."]),
    ("Linter (ruff check)", ["ruff", "check", "."]),
    ("Tipos (mypy)", ["mypy", "."]),
    ("Testes (pytest)", ["pytest"]),
]


def comando(ferramenta: str, argumentos: list[str]) -> list[str]:
    """Usa o executável do PATH; se não houver, chama a ferramenta como módulo deste Python."""
    executavel = shutil.which(ferramenta)
    if executavel:
        return [executavel, *argumentos]
    return [sys.executable, "-m", ferramenta, *argumentos]


def main() -> int:
    for nome, (ferramenta, *argumentos) in ETAPAS:
        print(f"\n== {nome}", flush=True)
        resultado = subprocess.run(comando(ferramenta, argumentos), check=False)
        if resultado.returncode != 0:
            print(f"\nFALHOU em: {nome}. Corrija e rode de novo.")
            return resultado.returncode
    print("\nConferência completa: tudo passou.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
