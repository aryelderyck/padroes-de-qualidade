"""Conferência completa do projeto, em um comando só: `python conferir.py`.

Roda, nesta ordem, formatação, linter, tipos e testes, e para na primeira etapa que falhar.
Com `--rapido` roda só formatação e linter (é o que a trava do commit usa por padrão).
São as mesmas quatro etapas do começo do CI; o CI ainda mede a cobertura dos testes e audita as
dependências. Copie para a raiz do projeto.
"""

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SAIDA_SEM_FERRAMENTA = 3
ETAPAS: list[tuple[str, list[str]]] = [
    ("Formatação (ruff format)", ["ruff", "format", "--check", "."]),
    ("Linter (ruff check)", ["ruff", "check", "."]),
    ("Tipos (mypy)", ["mypy", "."]),
    ("Testes (pytest)", ["pytest"]),
]
ETAPAS_RAPIDAS = 2
DICAS = {
    "ruff format": "Para formatar tudo de uma vez: ruff format .",
    "ruff check": "Parte dos apontamentos se corrige sozinha com: ruff check --fix .",
}


def achar(ferramenta: str) -> str | None:
    """Prefere a ferramenta do ambiente virtual do projeto; depois, a do PATH."""
    for pasta, sufixo in ((".venv/Scripts", ".exe"), (".venv/bin", "")):
        candidato = RAIZ / pasta / f"{ferramenta}{sufixo}"
        if candidato.exists():
            return str(candidato)
    return shutil.which(ferramenta)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    etapas = ETAPAS[:ETAPAS_RAPIDAS] if "--rapido" in sys.argv[1:] else ETAPAS
    for nome, (ferramenta, *argumentos) in etapas:
        print(f"\n== {nome}", flush=True)
        executavel = achar(ferramenta)
        if executavel is None:
            print(f"\nNÃO RODOU: a ferramenta '{ferramenta}' não foi encontrada.")
            print("Crie o ambiente virtual em .venv e instale as dependências de desenvolvimento:")
            print('  python -m venv .venv   e depois   .venv/Scripts/pip install -e ".[dev]"')
            print("  (em Linux e macOS o pip fica em .venv/bin/pip)")
            return SAIDA_SEM_FERRAMENTA
        resultado = subprocess.run([executavel, *argumentos], cwd=RAIZ, check=False)
        if resultado.returncode != 0:
            print(f"\nFALHOU em: {nome}. Corrija e rode de novo.")
            for trecho, dica in DICAS.items():
                if trecho in nome:
                    print(dica)
            return resultado.returncode
    print("\nConferência: tudo passou.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
