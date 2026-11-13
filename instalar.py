"""Instala o kit num projeto ou na máquina. O uso do kit é opcional: nada se instala sozinho.

Antes de instalar, veja o que vai acontecer (não escreve nada):
    python instalar.py avaliar CAMINHO_DO_PROJETO --tipo python

Num projeto (copia os modelos para os lugares certos, sem sobrescrever o que já existe):
    python instalar.py projeto CAMINHO_DO_PROJETO --tipo python
    python instalar.py projeto CAMINHO_DO_PROJETO --tipo node

Modos: `--modo essencial` (padrão: só o que quase não acusa código correto) ou `--modo completo`
(soma limites de tamanho, tipos estritos, a trava do pronto e a conferência a cada edição).
Com risco alto na avaliação, a instalação para; `--aceitar-risco` instala assim mesmo.

Na máquina, uma vez (skill de revisão e estilo de saída Professor, em ~/.claude):
    python instalar.py maquina

Acrescente --forcar para substituir arquivos que já existem. Cada cópia é listada na tela.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

KIT = Path(__file__).resolve().parent
MODELOS = KIT / "templates"
SAIDA_DE_USO_ERRADO = 2
PERMISSAO_DE_EXECUCAO = 0o755
MUITOS_APONTAMENTOS = 50
REGRAS_MOSTRADAS = 5
ALTO, MEDIO, BAIXO = "ALTO", "MÉDIO", "BAIXO"
Risco = tuple[str, str]

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
# Só entram no modo completo: partes que nunca rodaram numa sessão real do Claude Code, que dão
# alarme falso com mais frequência ou que falham fora de repositório público.
SO_NO_COMPLETO = {
    "claude/security-patterns.json",
    "claude/hooks/conferir-fim.py",
    "claude/hooks/conferir-fim.mjs",
    "github/codeql.yml",
}
# Arquivo do projeto que já traz as mesmas decisões: se existe um deles, o modelo do kit não entra.
JA_DECIDIDO_POR = {
    "eslint.config.mjs": "eslint.config.*",
    "tsconfig.json": "tsconfig*.json",
}
COMO_JUNTAR = {
    "pyproject.toml": "copie para ele as seções [tool.ruff], [tool.mypy] e [tool.pytest] do modelo "
    "templates/pyproject-python.toml",
    "eslint.config.mjs": "no arquivo de configuração do ESLint que já existe, importe "
    '{ regrasDoModo } de "./eslint.regras.mjs" e acrescente um bloco { rules: regrasDoModo }',
    "tsconfig.json": "confira se o tsconfig que já existe tem as opções `strict` e "
    "`noImplicitReturns` ligadas",
}
# Trecho que mostra que o arquivo que já existe traz as regras do kit (nada a juntar).
SINAL_DE_JUNTO = {
    "pyproject.toml": "[tool.ruff",
    "eslint.config.mjs": "eslint.regras",
    "tsconfig.json": "noImplicitReturns",
}
OPCOES_SO_DO_COMPLETO = ("noUncheckedIndexedAccess", "noImplicitOverride")
ECOSSISTEMAS = {"python": {"pip", "github-actions"}, "node": {"npm", "github-actions"}}
LINGUAGEM_DO_CODEQL = {"python": "python", "node": "javascript-typescript"}
PROXIMOS_PASSOS = {
    "python": [
        "Preencha os [colchetes] do CLAUDE.md.",
        "No pyproject.toml, troque o nome do projeto e liste as dependências.",
        "Crie o ambiente: python -m venv .venv",
        'Instale as ferramentas: .venv/Scripts/pip install -e ".[dev]"',
        "(em Linux e macOS o pip fica em .venv/bin/pip)",
        "A trava do commit roda formatação e linter; tudo, à mão: python conferir.py",
    ],
    "node": [
        "Preencha os [colchetes] do CLAUDE.md.",
        "Instale: npm install -D eslint @eslint/js typescript-eslint typescript globals prettier",
        'No package.json, crie os scripts "conferir:rapido": '
        '"prettier --check . && eslint . --max-warnings 0"',
        '  e "conferir": "npm run conferir:rapido && tsc --noEmit && vitest run"',
    ],
}


def versao_do_kit() -> str:
    achado = re.search(r"^## (\d+\.\d+)", (KIT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    return achado.group(1) if achado else "desconhecida"


# ----------------------------------------------------------------- ajustes de cada modelo
def do_modo(texto: str, modo: str) -> str:
    """Tira os trechos marcados para o outro modo e as próprias linhas de marcação."""
    outro = "completo" if modo == "essencial" else "essencial"
    mantidas: list[str] = []
    pulando = False
    for linha in texto.splitlines(keepends=True):
        marca = linha.strip().lstrip("#/ ").strip()
        if marca in {f"[{outro}]", f"[/{outro}]"}:
            pulando = marca == f"[{outro}]"
        elif marca not in {f"[{modo}]", f"[/{modo}]"} and not pulando:
            mantidas.append(linha)
    texto_do_modo = "".join(mantidas)
    if texto_do_modo == texto:
        return texto
    return re.sub(r"\n{3,}", "\n\n", texto_do_modo)


def so_os_ecossistemas(texto: str, tipo: str, _modo: str) -> str:
    """Deixa no dependabot.yml só os blocos do tipo de projeto."""
    cabecalho, *blocos = texto.split("  - package-ecosystem:")
    mantidos = [bloco for bloco in blocos if bloco.split('"')[1] in ECOSSISTEMAS[tipo]]
    return cabecalho + "".join("  - package-ecosystem:" + bloco for bloco in mantidos)


def com_a_linguagem(texto: str, tipo: str, _modo: str) -> str:
    return texto.replace("language: [python]", f"language: [{LINGUAGEM_DO_CODEQL[tipo]}]")


def com_o_modo_escrito(texto: str, _tipo: str, modo: str) -> str:
    return texto.replace('export const MODO = "completo";', f'export const MODO = "{modo}";')


def hooks_do_modo(texto: str, _tipo: str, modo: str) -> str:
    """Essencial: só o hook de edição, e só formatando. Troca `python` por `python3` se preciso."""
    ajustes = json.loads(texto)
    if modo == "essencial":
        ajustes["hooks"].pop("Stop", None)
    for evento in ajustes["hooks"].values():
        for grupo in evento:
            for hook in grupo["hooks"]:
                if modo == "essencial":
                    hook["args"].append("--so-formatar")
                if hook["command"] == "python" and not shutil.which("python"):
                    hook["command"] = "python3" if shutil.which("python3") else "python"
    return json.dumps(ajustes, indent=2, ensure_ascii=False) + "\n"


def tsconfig_do_modo(texto: str, _tipo: str, modo: str) -> str:
    if modo == "completo":
        return texto
    opcoes = json.loads(texto)
    for opcao in OPCOES_SO_DO_COMPLETO:
        opcoes["compilerOptions"].pop(opcao, None)
    return json.dumps(opcoes, indent=2, ensure_ascii=False) + "\n"


AJUSTES: dict[str, Callable[[str, str, str], str]] = {
    "github/dependabot.yml": so_os_ecossistemas,
    "github/codeql.yml": com_a_linguagem,
    "eslint.regras.mjs": com_o_modo_escrito,
    "claude/settings.python.json": hooks_do_modo,
    "claude/settings.node.json": hooks_do_modo,
    "tsconfig.json": tsconfig_do_modo,
}


def texto_do_modelo(modelo: str, tipo: str, modo: str) -> str:
    """O conteúdo que vai para o projeto: o modelo, no modo e no tipo escolhidos."""
    texto = do_modo((MODELOS / modelo).read_text(encoding="utf-8"), modo)
    return AJUSTES[modelo](texto, tipo, modo) if modelo in AJUSTES else texto


# ----------------------------------------------------------------- o que será feito
def situacao(projeto: Path, destino: str, forcar: bool) -> str:
    """O que acontece com um destino: criado, substituído, mantido ou deixado de fora."""
    padrao = JA_DECIDIDO_POR.get(destino)
    outros = [a.name for a in projeto.glob(padrao) if a.name != destino] if padrao else []
    if outros:
        return f"não copiado (o projeto já tem {outros[0]})"
    if not (projeto / destino).exists():
        return "criado"
    return "substituído" if forcar else "mantido (já existia)"


def plano(projeto: Path, tipo: str, modo: str, forcar: bool) -> list[tuple[str, str, str]]:
    """Lista (modelo, destino, situação) de tudo o que o modo instala neste projeto."""
    itens = {**COMUNS, **POR_TIPO[tipo]}
    return [
        (modelo, destino, situacao(projeto, destino, forcar))
        for modelo, destino in itens.items()
        if modo == "completo" or modelo not in SO_NO_COMPLETO
    ]


# ----------------------------------------------------------------- avaliação de risco
def saida_de(comando: list[str], pasta: Path) -> str | None:
    """A saída de um comando, ou None se ele não existe ou falhou."""
    try:
        feito = subprocess.run(
            comando, cwd=pasta, capture_output=True, encoding="utf-8", errors="replace", check=False
        )
    except OSError:
        return None
    return feito.stdout if feito.returncode == 0 else None


def riscos_do_git(projeto: Path) -> list[Risco]:
    git = shutil.which("git")
    if git is None or not (projeto / ".git").exists():
        return [
            (
                MEDIO,
                "A pasta não é um repositório git. Rode `git init` antes: sem ele a trava do "
                "commit não liga e não há como ver ou desfazer o que o kit trouxe.",
            )
        ]
    if saida_de([git, "status", "--porcelain"], projeto):
        return [
            (
                MEDIO,
                "Há mudanças sem commit. Faça um commit antes: assim o `git status` mostra só o "
                "que o kit trouxe, e fica fácil desfazer.",
            )
        ]
    return []


def ja_esta_junto(projeto: Path, destino: str) -> bool:
    """O arquivo de regras que já existe no projeto cita as regras do kit?"""
    padrao = JA_DECIDIDO_POR.get(destino, destino)
    textos = [a.read_text(encoding="utf-8", errors="replace") for a in projeto.glob(padrao)]
    return any(SINAL_DE_JUNTO[destino] in texto for texto in textos)


def riscos_dos_arquivos(projeto: Path, passos: list[tuple[str, str, str]]) -> list[Risco]:
    """Arquivo de regras que já existe: o do kit não entra, e as regras não valem sozinhas."""
    return [
        (MEDIO, f"{destino}: {estado}. As regras do kit NÃO valem até você juntar: {dica}.")
        for _modelo, destino, estado in passos
        if not estado.startswith(("criado", "substituído"))
        and (dica := COMO_JUNTAR.get(destino))
        and not ja_esta_junto(projeto, destino)
    ]


def achar_ruff(projeto: Path) -> str | None:
    for candidato in (".venv/Scripts/ruff.exe", ".venv/bin/ruff"):
        if (projeto / candidato).exists():
            return str(projeto / candidato)
    return shutil.which("ruff")


def apontamentos_do_ruff(projeto: Path, modo: str) -> dict[str, int] | None:
    """Quantos apontamentos cada regra do modo faria no código que já existe."""
    ruff = achar_ruff(projeto)
    if ruff is None:
        return None
    with tempfile.TemporaryDirectory() as temporaria:
        configuracao = Path(temporaria) / "pyproject.toml"
        configuracao.write_text(
            texto_do_modelo("pyproject-python.toml", "python", modo), encoding="utf-8"
        )
        comando = [ruff, "check", ".", "--config", str(configuracao), "--exit-zero"]
        saida = saida_de([*comando, "--statistics", "--output-format", "json"], projeto)
    if saida is None:
        return None
    return {str(item["code"]): int(item["count"]) for item in json.loads(saida or "[]")}


def riscos_do_codigo_python(projeto: Path, modo: str) -> list[Risco]:
    if not any(projeto.glob("**/*.py")):
        return []
    contagem = apontamentos_do_ruff(projeto, modo)
    if contagem is None:
        return [(BAIXO, "ruff não encontrado: o código que já existe não foi medido.")]
    total = sum(contagem.values())
    if total == 0:
        return [(BAIXO, f"O código que já existe passa nas regras do modo {modo}.")]
    maiores = sorted(contagem.items(), key=lambda par: -par[1])[:REGRAS_MOSTRADAS]
    resumo = ", ".join(f"{regra} ({vezes})" for regra, vezes in maiores)
    texto = (
        f"O código que já existe tem {total} apontamento(s) nas regras do modo {modo}: {resumo}. "
        "A trava do commit vai recusar até corrigir (`ruff check --fix .` resolve parte)."
    )
    return [(ALTO if total > MUITOS_APONTAMENTOS else MEDIO, texto)]


def riscos_do_tipo(projeto: Path, tipo: str, modo: str) -> list[Risco]:
    if tipo == "python":
        return riscos_do_codigo_python(projeto, modo)
    if not (projeto / "package.json").exists():
        return [
            (
                ALTO,
                "Não há package.json. Crie o projeto antes (por exemplo, `npm create vite@latest`) "
                "e instale o kit depois: o gerador recusa pasta que já tem arquivos, e as "
                "configurações dele precisam chegar primeiro.",
            )
        ]
    return [(BAIXO, "Em projeto Node o código que já existe não é medido: rode o ESLint depois.")]


def riscos_do_modo(modo: str) -> list[Risco]:
    if modo == "essencial":
        return []
    return [
        (
            ALTO,
            "O modo completo liga a trava do pronto e a conferência a cada edição, que ainda não "
            "rodaram numa sessão real do Claude Code, e regras que acusam código correto com "
            "alguma frequência (número mágico, limites de tamanho, tipos estritos). Teste antes "
            "num projeto pequeno.",
        )
    ]


def avaliar(projeto: Path, tipo: str, modo: str, forcar: bool) -> list[Risco]:
    passos = plano(projeto, tipo, modo, forcar)
    return [
        *riscos_do_modo(modo),
        *riscos_do_git(projeto),
        *riscos_dos_arquivos(projeto, passos),
        *riscos_do_tipo(projeto, tipo, modo),
    ]


def mostrar_avaliacao(riscos: list[Risco]) -> str:
    """Imprime os riscos e devolve o maior nível encontrado."""
    print("\nAvaliação de risco:")
    for nivel, texto in riscos:
        print(f"  [{nivel}] {texto}")
    niveis = {nivel for nivel, _texto in riscos}
    geral = next((nivel for nivel in (ALTO, MEDIO) if nivel in niveis), BAIXO)
    print(f"  Risco geral: {geral}")
    return geral


# ----------------------------------------------------------------- instalação
def gravar(projeto: Path, passos: list[tuple[str, str, str]], tipo: str, modo: str) -> None:
    for modelo, destino, estado in passos:
        print(f"  {estado:<22} {destino}")
        if estado in {"criado", "substituído"}:
            alvo = projeto / destino
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(texto_do_modelo(modelo, tipo, modo), encoding="utf-8", newline="\n")


def ligar_trava_do_commit(projeto: Path, modo: str) -> None:
    (projeto / ".githooks" / "pre-commit").chmod(PERMISSAO_DE_EXECUCAO)
    git = shutil.which("git")
    if git is None or not (projeto / ".git").exists():
        print("\nTrava do commit: ainda NÃO está ligada. Depois do `git init`, rode:")
        print("  git config core.hooksPath .githooks")
        return
    subprocess.run([git, "config", "core.hooksPath", ".githooks"], cwd=projeto, check=False)
    trava = ["kit.trava", "completa"] if modo == "completo" else ["--unset", "kit.trava"]
    subprocess.run([git, "config", *trava], cwd=projeto, check=False)
    alcance = "tudo" if modo == "completo" else "formatação e linter"
    print(f"\nTrava do commit: ligada, conferindo {alcance} (git config core.hooksPath .githooks).")


def pasta_valida(projeto: Path) -> bool:
    if not projeto.is_dir():
        print(f"A pasta do projeto não existe: {projeto}")
        return False
    if projeto.resolve() == KIT:
        print("Esta é a pasta do próprio kit. Indique a pasta do projeto.")
        return False
    return True


def avaliar_projeto(opcoes: argparse.Namespace) -> int:
    if not pasta_valida(opcoes.pasta):
        return SAIDA_DE_USO_ERRADO
    print(f"Kit {versao_do_kit()}, modo {opcoes.modo}, em {opcoes.pasta}. Nada será escrito.")
    for _modelo, destino, estado in plano(opcoes.pasta, opcoes.tipo, opcoes.modo, forcar=False):
        print(f"  {estado.replace('criado', 'seria criado'):<22} {destino}")
    mostrar_avaliacao(avaliar(opcoes.pasta, opcoes.tipo, opcoes.modo, forcar=False))
    return 0


def instalar_no_projeto(opcoes: argparse.Namespace) -> int:
    projeto, tipo, modo = opcoes.pasta, opcoes.tipo, opcoes.modo
    if not pasta_valida(projeto):
        return SAIDA_DE_USO_ERRADO
    print(f"Kit {versao_do_kit()}, modo {modo}, em {projeto} (projeto {tipo}).")
    geral = mostrar_avaliacao(avaliar(projeto, tipo, modo, opcoes.forcar))
    if geral == ALTO and not opcoes.aceitar_risco:
        print("\nNada foi instalado. Resolva o risco alto, ou repita com --aceitar-risco.")
        return SAIDA_DE_USO_ERRADO
    print("\nArquivos:")
    gravar(projeto, plano(projeto, tipo, modo, opcoes.forcar), tipo, modo)
    marca = f"{versao_do_kit()} (modo {modo})\n"
    (projeto / ".kit-versao").write_text(marca, encoding="utf-8", newline="\n")
    ligar_trava_do_commit(projeto, modo)
    print("\nPróximos passos:")
    for passo in PROXIMOS_PASSOS[tipo]:
        print(f"  - {passo}")
    return 0


def instalar_na_maquina(pasta: Path, forcar: bool) -> int:
    print(f"Kit {versao_do_kit()} em {pasta} (skill de revisão e estilo de saída):")
    for modelo, destino in MAQUINA.items():
        existia = (pasta / destino).exists()
        estado = "mantido (já existia)" if existia and not forcar else "criado"
        print(f"  {'substituído' if existia and forcar else estado:<22} {destino}")
        if not existia or forcar:
            (pasta / destino).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(MODELOS / modelo, pasta / destino)
    print("\nNo Claude Code: /output-style professor  e  /conferir-codigo")
    return 0


def ler_argumentos(argumentos: list[str]) -> argparse.Namespace:
    leitor = argparse.ArgumentParser(description="Instala o kit padroes-de-qualidade.")
    comandos = leitor.add_subparsers(dest="comando", required=True)
    for nome, ajuda in (
        ("avaliar", "mostra o que seria feito e os riscos, sem escrever nada"),
        ("projeto", "copia os modelos para um projeto"),
    ):
        comando = comandos.add_parser(nome, help=ajuda)
        comando.add_argument("pasta", type=Path)
        comando.add_argument("--tipo", choices=sorted(POR_TIPO), required=True)
        comando.add_argument("--modo", choices=["essencial", "completo"], default="essencial")
        if nome == "projeto":
            comando.add_argument("--forcar", action="store_true", help="substitui o que já existe")
            comando.add_argument(
                "--aceitar-risco", action="store_true", help="instala mesmo com risco alto"
            )
    maquina = comandos.add_parser("maquina", help="instala a skill e o estilo de saída")
    maquina.add_argument("--pasta", type=Path, default=Path.home() / ".claude")
    maquina.add_argument("--forcar", action="store_true", help="substitui o que já existe")
    return leitor.parse_args(argumentos)


def main(argumentos: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    opcoes = ler_argumentos(argumentos)
    if opcoes.comando == "avaliar":
        return avaliar_projeto(opcoes)
    if opcoes.comando == "projeto":
        return instalar_no_projeto(opcoes)
    return instalar_na_maquina(opcoes.pasta, opcoes.forcar)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
