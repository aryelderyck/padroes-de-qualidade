"""Instala o kit num projeto ou na máquina. O uso do kit é opcional: nada se instala sozinho.

Num projeto (copia os modelos para os lugares certos, sem sobrescrever o que já existe):
    python instalar.py projeto CAMINHO_DO_PROJETO --tipo python
    python instalar.py projeto CAMINHO_DO_PROJETO --tipo node

Na máquina, uma vez (skill de revisão e estilo de saída Professor, em ~/.claude):
    python instalar.py maquina

Acrescente --forcar para substituir arquivos que já existem. Cada cópia é listada na tela.
"""

import argparse
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

KIT = Path(__file__).resolve().parent
MODELOS = KIT / "templates"
SAIDA_DE_USO_ERRADO = 2
PERMISSAO_DE_EXECUCAO = 0o755

# modelo em templates/ -> destino dentro do projeto
COMUNS = {
    "editorconfig": ".editorconfig",
    "gitattributes": ".gitattributes",
    "githooks/pre-commit": ".githooks/pre-commit",
    "claude/claude-security-guidance.md": ".claude/claude-security-guidance.md",
    "claude/security-patterns.json": ".claude/security-patterns.json",
    "CLAUDE.template.md": "CLAUDE.md",
    "APRENDIZADOS.template.md": "APRENDIZADOS.md",
    "CHECKLIST-PRONTO.md": "docs/CHECKLIST-PRONTO.md",
    "github/codeql.yml": ".github/workflows/codeql.yml",
    "github/dependabot.yml": ".github/dependabot.yml",
}
POR_TIPO = {
    "python": {
        "gitignore-python": ".gitignore",
        "pyproject-python.toml": "pyproject.toml",
        "conferir.py": "conferir.py",
        "claude/settings.python.json": ".claude/settings.json",
        "claude/hooks/conferir-edicao.py": ".claude/hooks/conferir-edicao.py",
        "claude/hooks/conferir-fim.py": ".claude/hooks/conferir-fim.py",
        "github/ci-python.yml": ".github/workflows/ci.yml",
    },
    "node": {
        "gitignore-node": ".gitignore",
        "eslint.regras.mjs": "eslint.regras.mjs",
        "eslint.config.mjs": "eslint.config.mjs",
        "prettierrc.json": ".prettierrc.json",
        "prettierignore": ".prettierignore",
        "tsconfig.json": "tsconfig.json",
        "claude/settings.node.json": ".claude/settings.json",
        "claude/hooks/conferir-edicao.mjs": ".claude/hooks/conferir-edicao.mjs",
        "claude/hooks/conferir-fim.mjs": ".claude/hooks/conferir-fim.mjs",
        "github/ci-node.yml": ".github/workflows/ci.yml",
    },
}
MAQUINA = {
    "skills/conferir-codigo/SKILL.md": "skills/conferir-codigo/SKILL.md",
    "skills/conferir-codigo/armadilhas.md": "skills/conferir-codigo/armadilhas.md",
    "skills/conferir-codigo/codigo-limpo.md": "skills/conferir-codigo/codigo-limpo.md",
    "output-styles/professor.md": "output-styles/professor.md",
}
ECOSSISTEMAS = {"python": {"pip", "github-actions"}, "node": {"npm", "github-actions"}}
LINGUAGEM_DO_CODEQL = {"python": "python", "node": "javascript-typescript"}
PROXIMOS_PASSOS = {
    "python": [
        "Preencha os [colchetes] do CLAUDE.md.",
        "No pyproject.toml, troque o nome do projeto e liste as dependências.",
        "Crie o ambiente: python -m venv .venv",
        'Instale as ferramentas: .venv/Scripts/pip install -e ".[dev]"',
        "(em Linux e macOS o pip fica em .venv/bin/pip)",
        "Antes de cada commit a conferência roda sozinha; à mão: python conferir.py",
    ],
    "node": [
        "Preencha os [colchetes] do CLAUDE.md.",
        "Instale: npm install -D eslint @eslint/js typescript-eslint typescript globals prettier",
        'No package.json, crie o script "conferir": '
        '"prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run"',
        "Se o gerador do projeto já criou um tsconfig.json, confira as opções com as do kit.",
    ],
}


def versao_do_kit() -> str:
    achado = re.search(r"^## (\d+\.\d+)", (KIT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    return achado.group(1) if achado else "desconhecida"


def so_os_ecossistemas(texto: str, tipo: str) -> str:
    """Deixa no dependabot.yml só os blocos do tipo de projeto."""
    cabecalho, *blocos = texto.split("  - package-ecosystem:")
    mantidos = [bloco for bloco in blocos if bloco.split('"')[1] in ECOSSISTEMAS[tipo]]
    return cabecalho + "".join("  - package-ecosystem:" + bloco for bloco in mantidos)


def com_a_linguagem(texto: str, tipo: str) -> str:
    return texto.replace("language: [python]", f"language: [{LINGUAGEM_DO_CODEQL[tipo]}]")


AJUSTES: dict[str, Callable[[str, str], str]] = {
    "github/dependabot.yml": so_os_ecossistemas,
    "github/codeql.yml": com_a_linguagem,
}


def copiar(modelo: str, destino: Path, tipo: str | None, forcar: bool) -> str:
    """Copia um modelo e devolve o que aconteceu: criado, substituído ou mantido."""
    existia = destino.exists()
    if existia and not forcar:
        return "mantido (já existia)"
    destino.parent.mkdir(parents=True, exist_ok=True)
    origem = MODELOS / modelo
    if modelo in AJUSTES and tipo is not None:
        texto = AJUSTES[modelo](origem.read_text(encoding="utf-8"), tipo)
        destino.write_text(texto, encoding="utf-8", newline="\n")
    else:
        shutil.copyfile(origem, destino)
    return "substituído" if existia else "criado"


def instalar(itens: dict[str, str], raiz: Path, tipo: str | None, forcar: bool) -> None:
    for modelo, destino in itens.items():
        print(f"  {copiar(modelo, raiz / destino, tipo, forcar):<22} {destino}")


def ligar_trava_do_commit(projeto: Path) -> None:
    (projeto / ".githooks" / "pre-commit").chmod(PERMISSAO_DE_EXECUCAO)
    git = shutil.which("git")
    if git is None or not (projeto / ".git").exists():
        print("\nTrava do commit: ainda NÃO está ligada. Depois do `git init`, rode:")
        print("  git config core.hooksPath .githooks")
        return
    subprocess.run([git, "config", "core.hooksPath", ".githooks"], cwd=projeto, check=False)
    print("\nTrava do commit: ligada (git config core.hooksPath .githooks).")


def instalar_no_projeto(projeto: Path, tipo: str, forcar: bool) -> int:
    if not projeto.is_dir():
        print(f"A pasta do projeto não existe: {projeto}")
        return SAIDA_DE_USO_ERRADO
    if projeto.resolve() == KIT:
        print("Esta é a pasta do próprio kit. Indique a pasta do projeto.")
        return SAIDA_DE_USO_ERRADO
    print(f"Kit {versao_do_kit()} em {projeto} (projeto {tipo}):")
    instalar({**COMUNS, **POR_TIPO[tipo]}, projeto, tipo, forcar)
    (projeto / ".kit-versao").write_text(f"{versao_do_kit()}\n", encoding="utf-8", newline="\n")
    ligar_trava_do_commit(projeto)
    print("\nPróximos passos:")
    for passo in PROXIMOS_PASSOS[tipo]:
        print(f"  - {passo}")
    return 0


def instalar_na_maquina(pasta: Path, forcar: bool) -> int:
    print(f"Kit {versao_do_kit()} em {pasta} (skill de revisão e estilo de saída):")
    instalar(MAQUINA, pasta, None, forcar)
    print("\nNo Claude Code: /output-style professor  e  /conferir-codigo")
    return 0


def ler_argumentos(argumentos: list[str]) -> argparse.Namespace:
    leitor = argparse.ArgumentParser(description="Instala o kit padroes-de-qualidade.")
    comandos = leitor.add_subparsers(dest="comando", required=True)
    projeto = comandos.add_parser("projeto", help="copia os modelos para um projeto")
    projeto.add_argument("pasta", type=Path)
    projeto.add_argument("--tipo", choices=sorted(POR_TIPO), required=True)
    projeto.add_argument("--forcar", action="store_true", help="substitui o que já existe")
    maquina = comandos.add_parser("maquina", help="instala a skill e o estilo de saída")
    maquina.add_argument("--pasta", type=Path, default=Path.home() / ".claude")
    maquina.add_argument("--forcar", action="store_true", help="substitui o que já existe")
    return leitor.parse_args(argumentos)


def main(argumentos: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    opcoes = ler_argumentos(argumentos)
    if opcoes.comando == "projeto":
        return instalar_no_projeto(opcoes.pasta, opcoes.tipo, opcoes.forcar)
    return instalar_na_maquina(opcoes.pasta, opcoes.forcar)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
