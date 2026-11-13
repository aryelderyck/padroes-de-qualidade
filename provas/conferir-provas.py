"""Provas do kit: confirma que cada regra automática pega o exemplo ruim e deixa passar o bom.

Uso, na raiz do kit:  python provas/conferir-provas.py
Precisa de ruff, mypy e pytest (versões em provas/requisitos.txt) e de node, eslint e prettier
(versões em .github/workflows/kit.yml).
Monta projetos de exemplo numa pasta temporária, com os modelos de templates/ nos lugares em que
ficam num projeto de verdade, e roda as ferramentas de verdade. Sai com 1 se alguma prova falhar.
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / "templates"
PROVAS = RAIZ / "provas"
INSTALADOR = RAIZ / "instalar.py"
LIMITE_DE_LINHAS_DO_REGRAS = 80
SAIDA_DE_PROBLEMA_DO_HOOK = 2
SAIDA_SEM_FERRAMENTA = 3
TAMANHO_DO_TRECHO = 300
# Ambiente sem nenhuma ferramenta no PATH (o Windows precisa do SYSTEMROOT para iniciar o Python).
SEM_FERRAMENTAS = {"PATH": "", "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
PACOTES_DE_TYPESCRIPT = [
    "eslint@10.1.0",
    "@eslint/js@10.0.1",
    "typescript-eslint@8.72.2",
    "typescript@6.0.3",
    "globals@17.14.0",
    "prettier@3.8.1",
]
# O que a configuração de TypeScript do kit PRECISA apontar em provas/ts/ruim.ts.
ESPERADO_TS = {
    "@typescript-eslint/switch-exhaustiveness-check": "switch que não cobre todos os casos",
    "@typescript-eslint/no-explicit-any": "uso de any",
    "@typescript-eslint/no-floating-promises": "promessa sem await",
    "@typescript-eslint/no-implied-eval": "código em texto no setTimeout",
    "eqeqeq": "comparação com conversão implícita",
}
EXTENSOES_DE_TEXTO = {".md", ".py", ".js", ".jsx", ".mjs", ".json", ".toml", ".yml", ".yaml", ""}
PASTAS_IGNORADAS = {".git", ".mypy_cache", ".ruff_cache", "__pycache__", "node_modules"}
FORMATO_DO_COMMIT = re.compile(r"^(docs|feat|fix|test|refactor|chore)\(kit\): \S|^Merge ")
LINK_DE_MARKDOWN = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
USO_DE_ACTION = re.compile(r"uses: ([\w./-]+)@(\S+)")
FIXACAO_POR_COMMIT = re.compile(r"[0-9a-f]{40}")
MARCADOR_DE_VERSAO = "<versão"
LINGUAGENS_DO_CODEQL_DO_KIT = ("language: [python]", "language: [python, javascript-typescript]")
CODIGO_DE_REGRA = re.compile(r"`([A-Z]{1,4}\d{3,4})`")
# Os scripts do kit imprimem no terminal e chamam ferramentas: só isso é liberado para eles.
EXCECOES_DOS_SCRIPTS_DO_KIT = ["kit/*:T201", "kit/*:S603"]

# O que o linter do kit PRECISA apontar em provas/python/ruim.py.
ESPERADO_PYTHON = {
    "S608": "SQL montado com texto",
    "B006": "valor padrão mutável",
    "B023": "função de laço que captura a variável do laço",
    "DTZ005": "data e hora sem fuso",
    "PLR2004": "número mágico",
    "PLR0913": "parâmetros demais",
    "PLR0915": "função longa demais",
    "C901": "função complexa demais",
    "E722": "except sem tipo",
    "S110": "exceção engolida",
    "T201": "print esquecido",
    "F841": "variável sem uso",
    "F632": "comparação de valor com is",
    "E711": "comparação com None usando ==",
    "N802": "nome de função fora do padrão",
    "S113": "chamada de rede sem tempo limite",
    "A001": "nome que esconde função embutida",
    "ERA001": "código comentado",
    "ARG001": "parâmetro sem uso",
    "PLW2901": "variável do laço sobrescrita",
    "RUF012": "valor mutável como padrão de classe",
}

# Regras de typescript-eslint citadas nas listas da skill: só rodam na prova com rede.
REGRAS_COM_TIPO = {"no-floating-promises", "no-explicit-any"}

# Padrões de segurança: (deve pegar, não deve pegar).
CASOS_DE_SEGURANCA = {
    "segredo_no_navegador": (
        ["const k = import.meta.env.VITE_API_KEY", "NEXT_PUBLIC_STRIPE_SECRET=x"],
        ["import.meta.env.VITE_API_URL", "API_KEY=abc"],
    ),
    "cors_aberto": (
        ['allow_origins=["*"]', "allow_origins = [ '*' ]", '"Access-Control-Allow-Origin": "*"'],
        ['allow_origins=["https://exemplo.test"]'],
    ),
    "tls_desligado": (
        ["httpx.get(u, verify=False)", "{ rejectUnauthorized: false }"],
        ["verify=True", "verify_token(x)"],
    ),
    "sql_montado_com_texto": (
        [
            'cur.execute(f"SELECT * FROM t WHERE id={x}")',
            'cur.execute("SELECT * FROM t WHERE id=" + x)',
            "cur.execute('SELECT * FROM t WHERE id=%s' % x)",
        ],
        ['cur.execute("SELECT * FROM t WHERE id = ?", (x,))', "session.execute(select(T))"],
    ),
    "depuracao_ligada": (["app = FastAPI(debug=True)", "DEBUG = True"], ["debug=False"]),
    "segredo_na_url": (
        ["https://exemplo.test/v1?api_key=abc", 'u + "&token=" + t'],
        ["https://exemplo.test/v1?pagina=2", "tokenizer=1"],
    ),
}

BOM_PY = '"""Módulo novo."""\n\n\ndef um() -> int:\n    return 1\n'
BOM_JS = "export function um() {\n  return 1;\n}\n"
RUIM_JS = "export function um(a) {\n    return a == 1\n}\n"

TESTE_TIPICO = """from app.bom import classificar


def test_classificar_desconhecido():
    senha_de_mentira = "abc123"
    assert senha_de_mentira
    assert classificar(99) == "outro"
"""

TESTE_COM_FIXTURE = """import pytest


@pytest.fixture
def banco_limpo():
    return None


def test_usa_fixture_so_pelo_efeito(banco_limpo):
    assert True
"""

falhas: list[str] = []
avisos: list[str] = []


# --------------------------------------------------------------------------- utilidades
def conferir(condicao: bool, descricao: str, detalhe: object = "") -> None:
    print(f"  {'ok   ' if condicao else 'FALHA'} {descricao}")
    if not condicao:
        falhas.append(f"{descricao} {str(detalhe)[:TAMANHO_DO_TRECHO]}".strip())


def titulo(texto: str) -> None:
    print(f"\n{texto}")


def rodar(
    comando: list[str],
    pasta: Path,
    entrada: str | None = None,
    ambiente: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        comando,
        cwd=pasta,
        input=entrada,
        env=ambiente,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def ferramenta(nome: str) -> str | None:
    caminho = shutil.which(nome)
    if caminho is None:
        avisos.append(
            f"{nome} não está instalado: as provas que dependem dele NÃO foram conferidas"
        )
    return caminho


def arquivos_do_kit(padrao: str) -> list[Path]:
    return [a for a in RAIZ.rglob(padrao) if a.is_file() and not PASTAS_IGNORADAS & set(a.parts)]


def ler(arquivo: Path) -> str:
    return arquivo.read_text(encoding="utf-8")


def escrever(arquivo: Path, texto: str) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(texto, encoding="utf-8", newline="\n")


def copiar(origem: Path, destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(origem, destino)


def instalar_no_venv(pasta: Path, nomes: list[str]) -> None:
    """Copia as ferramentas para o ambiente virtual do projeto, como um `pip install` deixaria."""
    destino = pasta / ".venv" / ("Scripts" if os.name == "nt" else "bin")
    for nome in nomes:
        origem = shutil.which(nome)
        if origem is not None:
            copiar(Path(origem), destino / Path(origem).name)


def entrada_do_hook(pasta: Path, arquivo: Path) -> str:
    """A mesma entrada que o Claude Code envia a um hook PostToolUse de Edit ou Write."""
    return json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(arquivo)}})


# --------------------------------------------------------------------------- [1] estrutura
def provar_links() -> None:
    quebrados = [
        f"{arquivo.relative_to(RAIZ)} -> {alvo}"
        for arquivo in arquivos_do_kit("*.md")
        for alvo in LINK_DE_MARKDOWN.findall(ler(arquivo))
        if not alvo.startswith(("http", "mailto:")) and not (arquivo.parent / alvo).exists()
    ]
    conferir(not quebrados, "links internos dos .md existem", quebrados)


def provar_configuracoes() -> None:
    invalidos = []
    for arquivo in arquivos_do_kit("*.json"):
        try:
            json.loads(ler(arquivo))
        except json.JSONDecodeError as erro:
            invalidos.append(f"{arquivo.name}: {erro}")
    for arquivo in arquivos_do_kit("*.toml"):
        try:
            tomllib.loads(ler(arquivo))
        except tomllib.TOMLDecodeError as erro:
            invalidos.append(f"{arquivo.name}: {erro}")
    conferir(not invalidos, "arquivos JSON e TOML abrem sem erro", invalidos)


def provar_yaml_e_cabecalhos() -> None:
    try:
        # Dependência opcional: sem ela, a prova é pulada com aviso.
        import yaml  # type: ignore[import-untyped, unused-ignore]  # noqa: PLC0415
    except ImportError:
        avisos.append("pyyaml não está instalado: YAML e cabeçalhos NÃO foram conferidos")
        return
    for arquivo in [*arquivos_do_kit("*.yml"), *arquivos_do_kit("*.yaml")]:
        yaml.safe_load(ler(arquivo))
    conferir(True, "arquivos YAML abrem sem erro")
    for arquivo in [*MODELOS.glob("skills/*/SKILL.md"), *MODELOS.glob("output-styles/*.md")]:
        cabecalho = yaml.safe_load(ler(arquivo).split("---")[1])
        nome = arquivo.relative_to(RAIZ)
        conferir(
            {"name", "description"} <= set(cabecalho), f"cabeçalho com name e description: {nome}"
        )


def provar_git() -> None:
    git = shutil.which("git")
    if git is None or not (RAIZ / ".git").exists():
        avisos.append("git ou a pasta .git ausente: commit e mapa de arquivos NÃO foram conferidos")
        return
    assunto = rodar([git, "log", "-1", "--format=%s"], RAIZ).stdout.strip()
    conferir(
        bool(FORMATO_DO_COMMIT.search(assunto)),
        "último commit no formato tipo(kit): o que mudou",
        assunto,
    )
    mapa = ler(RAIZ / "docs" / "MAPA-DE-ARQUIVOS.md")
    rastreados = rodar([git, "ls-files"], RAIZ).stdout.split()
    sem_linha = [arquivo for arquivo in rastreados if f"`{arquivo}`" not in mapa]
    conferir(not sem_linha, "todo arquivo do kit tem linha no mapa de arquivos", sem_linha)


def provar_codigos_citados(regras_js: set[str]) -> None:
    """Todo código de regra citado nas listas da skill precisa ter prova."""
    citados: set[str] = set()
    for arquivo in MODELOS.glob("skills/*/*.md"):
        citados |= set(CODIGO_DE_REGRA.findall(ler(arquivo)))
    sem_prova = sorted(citados - set(ESPERADO_PYTHON))
    conferir(not sem_prova, "códigos de regra citados nas listas da skill têm prova", sem_prova)
    texto = "".join(ler(arquivo) for arquivo in MODELOS.glob("skills/*/*.md"))
    citadas_js = {
        regra
        for regra in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", texto)
        if regra.startswith(("no-", "max-"))
    }
    sem_prova_js = sorted(citadas_js - regras_js - REGRAS_COM_TIPO)
    conferir(
        not sem_prova_js,
        "regras de ESLint citadas nas listas da skill existem no kit",
        sem_prova_js,
    )


def provar_versao() -> None:
    """O número da versão do topo do CHANGELOG aparece igual em todo lugar que o cita."""
    achada = re.search(r"^## (\d+\.\d+)", ler(RAIZ / "CHANGELOG.md"), re.MULTILINE)
    versao = achada.group(1) if achada else "?"
    citacoes = {
        "README.md": f"Versão **{versao}**",
        "PADROES.md": f"Versão {versao} ·",
        "templates/CLAUDE.template.md": f"[{versao}]",
    }
    atrasados = [nome for nome, trecho in citacoes.items() if trecho not in ler(RAIZ / nome)]
    conferir(not atrasados, f"versão {versao} citada igual em todos os documentos", atrasados)


def provar_actions() -> None:
    """Toda action é fixada pelo commit, e os modelos usam a mesma fixação do CI do kit."""
    fixacoes: dict[str, set[str]] = {}
    soltas = []
    workflows = [*(RAIZ / ".github" / "workflows").glob("*.yml"), *MODELOS.glob("github/*.yml")]
    for arquivo in workflows:
        for action, versao in USO_DE_ACTION.findall(ler(arquivo)):
            if versao == MARCADOR_DE_VERSAO:
                continue
            if not FIXACAO_POR_COMMIT.fullmatch(versao):
                soltas.append(f"{arquivo.name}: {action}@{versao}")
            fixacoes.setdefault(action.split("/")[1], set()).add(versao)
    conferir(bool(fixacoes) and not soltas, "toda action é fixada pelo commit", soltas)
    diferentes = {nome: versoes for nome, versoes in fixacoes.items() if len(versoes) > 1}
    conferir(
        not diferentes,
        "modelos de workflow usam a mesma fixação de actions do CI do kit",
        f"{diferentes}: atualize também templates/github/",
    )
    modelo = ler(MODELOS / "github" / "codeql.yml").replace(*LINGUAGENS_DO_CODEQL_DO_KIT)
    do_kit = ler(RAIZ / ".github" / "workflows" / "codeql.yml")
    conferir(
        sem_comentarios_do_topo(modelo) == sem_comentarios_do_topo(do_kit),
        "o CodeQL do kit é o modelo, só com as linguagens trocadas",
    )


def sem_comentarios_do_topo(texto: str) -> str:
    return texto[texto.index("name:") :]


def provar_estrutura() -> None:
    titulo("[1] Estrutura do kit")
    provar_links()
    linhas = len(ler(RAIZ / "REGRAS.md").splitlines())
    conferir(
        linhas <= LIMITE_DE_LINHAS_DO_REGRAS,
        f"REGRAS.md tem {linhas} linhas (limite {LIMITE_DE_LINHAS_DO_REGRAS})",
    )
    provar_configuracoes()
    provar_yaml_e_cabecalhos()
    provar_actions()
    provar_versao()
    provar_git()
    com_cr = [
        str(arquivo.relative_to(RAIZ))
        for arquivo in arquivos_do_kit("*")
        if arquivo.suffix in EXTENSOES_DE_TEXTO and b"\r" in arquivo.read_bytes()
    ]
    conferir(not com_cr, "nenhum arquivo de texto com fim de linha CRLF", com_cr)


# --------------------------------------------------------------------------- [2-5] Python
def montar_projeto_python(pasta: Path) -> None:
    copiar(MODELOS / "pyproject-python.toml", pasta / "pyproject.toml")
    copiar(MODELOS / "conferir.py", pasta / "conferir.py")
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-edicao.py",
        pasta / ".claude" / "hooks" / "conferir-edicao.py",
    )
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-fim.py",
        pasta / ".claude" / "hooks" / "conferir-fim.py",
    )
    copiar(PROVAS / "python" / "bom.py", pasta / "app" / "bom.py")
    escrever(pasta / "app" / "__init__.py", "")
    escrever(pasta / "tests" / "__init__.py", "")
    escrever(pasta / "tests" / "test_bom.py", TESTE_TIPICO)
    escrever(pasta / "tests" / "test_fixture.py", TESTE_COM_FIXTURE)


def provar_regras_python(pasta: Path, ruff: str, mypy: str | None) -> None:
    titulo("[2] Regras de Python (ruff e mypy com o pyproject do kit)")
    achados = json.loads(
        rodar([ruff, "check", "--output-format", "json", "."], pasta).stdout or "[]"
    )
    conferir(
        not achados,
        "exemplo bom, teste típico e scripts sem apontamento",
        [a["code"] for a in achados],
    )
    formato = rodar([ruff, "format", "--check", "."], pasta)
    conferir(
        formato.returncode == 0, "exemplo bom, teste típico e scripts já formatados", formato.stdout
    )
    if mypy is not None:
        if rodar([mypy, "-c", "import pytest"], pasta).returncode != 0:
            # O mypy desta máquina não enxerga o pytest (instalações separadas).
            avisos.append(
                "mypy não enxerga o pytest aqui: o teste com fixture só passou pelo linter"
            )
            (pasta / "tests" / "test_fixture.py").unlink()
        tipos = rodar([mypy, "."], pasta)
        conferir(
            tipos.returncode == 0,
            "mypy estrito passa no projeto bom (teste sem anotação liberado)",
            tipos.stdout,
        )
        hook = rodar([mypy, "--strict", ".claude/hooks/conferir-edicao.py"], pasta)
        conferir(
            hook.returncode == 0,
            "mypy estrito passa no hook (pasta oculta, conferida à parte)",
            hook.stdout,
        )

    copiar(PROVAS / "python" / "ruim.py", pasta / "app" / "ruim.py")
    ruim = json.loads(
        rodar([ruff, "check", "--output-format", "json", "app/ruim.py"], pasta).stdout or "[]"
    )
    codigos = {achado["code"] for achado in ruim}
    for codigo, significado in ESPERADO_PYTHON.items():
        conferir(codigo in codigos, f"{codigo} pega: {significado}")
    recusou = rodar([ruff, "format", "--check", "app/ruim.py"], pasta).returncode != 0
    conferir(recusou, "formatador recusa a indentação do exemplo ruim")


def provar_hook_python(pasta: Path, ruff: str) -> None:
    titulo("[3] Hook de edição para Python (conferir-edicao.py)")
    hook = [sys.executable, str(pasta / ".claude" / "hooks" / "conferir-edicao.py")]
    resultado = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "ruim.py"))
    conferir(
        resultado.returncode == SAIDA_DE_PROBLEMA_DO_HOOK,
        "arquivo ruim: sai com 2 e devolve os problemas",
    )
    conferir(
        "S608" in resultado.stderr, "arquivo ruim: a mensagem cita a regra (S608)", resultado.stderr
    )
    formatado = rodar([ruff, "format", "--check", "app/ruim.py"], pasta).returncode == 0
    conferir(formatado, "arquivo ruim: o hook corrigiu a indentação")
    bom = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "bom.py"))
    conferir(bom.returncode == 0, "arquivo bom: sai com 0", bom.stderr)
    escrever(pasta / "app" / "meio.py", "import os\n\n\ndef um() -> int:\n    return 1\n")
    meio = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "meio.py"))
    conferir(
        meio.returncode == 0,
        "import ainda sem uso (meio de uma edição): não interrompe",
        meio.stderr,
    )
    (pasta / "app" / "meio.py").unlink()
    sumiu = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "nao_existe.py"))
    conferir(sumiu.returncode == 0, "arquivo que não existe mais: não interrompe", sumiu.stderr)
    outro = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "notas.txt"))
    conferir(outro.returncode == 0, "arquivo que não é Python: não faz nada")
    conferir(
        rodar(hook, pasta, "isto não é JSON").returncode == 0,
        "entrada inválida: não trava o trabalho",
    )
    conferir(
        rodar(hook, pasta, "{}").returncode == 0,
        "entrada sem caminho de arquivo: não trava o trabalho",
    )
    sem_ruff = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "bom.py"), SEM_FERRAMENTAS)
    conferir(
        sem_ruff.returncode == 0 and "ruff" in sem_ruff.stderr,
        "sem o ruff: avisa e não trava",
        sem_ruff.stderr,
    )
    instalar_no_venv(pasta, ["ruff"])
    copiar(PROVAS / "python" / "ruim.py", pasta / "app" / "ruim.py")
    do_venv = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "app" / "ruim.py"), SEM_FERRAMENTAS)
    conferir(
        do_venv.returncode == SAIDA_DE_PROBLEMA_DO_HOOK and "S608" in do_venv.stderr,
        "ruff só no .venv do projeto (fora do PATH): o hook o encontra e confere",
        do_venv.stderr,
    )


def provar_conferir(pasta: Path) -> None:
    titulo("[4] Comando único (conferir.py)")
    (pasta / "app" / "ruim.py").unlink()
    comando = [sys.executable, "conferir.py"]
    passou = rodar(comando, pasta)
    conferir(
        passou.returncode == 0,
        "projeto bom: passa nas quatro etapas",
        passou.stdout[-TAMANHO_DO_TRECHO:],
    )
    sem_nada = rodar(comando, pasta, ambiente=SEM_FERRAMENTAS)
    explicou = (
        sem_nada.returncode == SAIDA_SEM_FERRAMENTA and "não foi encontrada" in sem_nada.stdout
    )
    conferir(explicou, "sem as ferramentas: diz que não rodou e como instalar", sem_nada.stdout)
    conferir(
        "FALHOU em" not in sem_nada.stdout, "sem as ferramentas: não diz que o código está errado"
    )
    instalar_no_venv(pasta, ["ruff", "mypy", "pytest"])
    do_venv = rodar(comando, pasta, ambiente=SEM_FERRAMENTAS)
    conferir(
        do_venv.returncode == 0 and "tudo passou" in do_venv.stdout,
        "ferramentas só no .venv do projeto (fora do PATH): passa nas quatro etapas",
        do_venv.stdout[-TAMANHO_DO_TRECHO:],
    )

    escrever(pasta / "app" / "feio.py", "def  f( ):\n  return  1\n")
    feio = rodar(comando, pasta)
    conferir(
        feio.returncode != 0 and "FALHOU em: Formatação" in feio.stdout,
        "código fora do formato: para na etapa 1",
    )
    escrever(pasta / "app" / "feio.py", '"""Módulo."""\n\nimport os\n')
    lint = rodar(comando, pasta)
    conferir(
        lint.returncode != 0 and "FALHOU em: Linter" in lint.stdout,
        "import sem uso: para na etapa 2",
        lint.stdout,
    )
    escrever(pasta / "app" / "feio.py", '"""Módulo."""\n\n\ndef soma(a, b):\n    return a + b\n')
    tipos = rodar(comando, pasta)
    conferir(
        tipos.returncode != 0 and "FALHOU em: Tipos" in tipos.stdout,
        "função sem tipo: para na etapa 3",
        tipos.stdout,
    )
    escrever(
        pasta / "app" / "feio.py",
        '"""Módulo."""\n\n\ndef soma(a: int, b: int) -> int:\n    return a - b\n',
    )
    escrever(
        pasta / "tests" / "test_feio.py",
        "from app.feio import soma\n\n\ndef test_soma():\n    assert soma(2, 2) == 4\n",
    )
    testes = rodar(comando, pasta)
    conferir(
        testes.returncode != 0 and "FALHOU em: Testes" in testes.stdout,
        "erro de lógica com teste: para na etapa 4",
    )
    (pasta / "app" / "feio.py").unlink()
    (pasta / "tests" / "test_feio.py").unlink()


def provar_scripts_do_kit(base: Path, ruff: str, mypy: str | None) -> None:
    titulo("[5] O kit segue as próprias regras")
    pasta = base / "kit-como-projeto"
    copiar(MODELOS / "pyproject-python.toml", pasta / "pyproject.toml")
    copiar(PROVAS / "conferir-provas.py", pasta / "kit" / "conferir_provas.py")
    copiar(MODELOS / "conferir.py", pasta / "kit" / "conferir.py")
    hooks = MODELOS / "claude" / "hooks"
    copiar(hooks / "conferir-edicao.py", pasta / "kit" / "conferir_edicao.py")
    copiar(hooks / "conferir-fim.py", pasta / "kit" / "conferir_fim.py")
    copiar(INSTALADOR, pasta / "kit" / "instalar.py")
    excecoes = [
        parte
        for regra in EXCECOES_DOS_SCRIPTS_DO_KIT
        for parte in ("--extend-per-file-ignores", regra)
    ]
    lint = rodar([ruff, "check", *excecoes, "."], pasta)
    conferir(
        lint.returncode == 0,
        "scripts do kit passam no linter do kit",
        lint.stdout[-TAMANHO_DO_TRECHO:],
    )
    formato = rodar([ruff, "format", "--check", "."], pasta)
    conferir(formato.returncode == 0, "scripts do kit estão no formato do kit", formato.stdout)
    if mypy is not None:
        tipos = rodar([mypy, "kit"], pasta)
        conferir(
            tipos.returncode == 0,
            "scripts do kit passam no mypy estrito",
            tipos.stdout[-TAMANHO_DO_TRECHO:],
        )


def preparar_repositorio(git: str, pasta: Path) -> None:
    """Cria um repositório com a trava do commit instalada do jeito que o kit ensina."""
    copiar(MODELOS / "githooks" / "pre-commit", pasta / ".githooks" / "pre-commit")
    (pasta / ".githooks" / "pre-commit").chmod(0o755)
    for comando in (
        ["init", "-q"],
        ["config", "user.name", "Prova do Kit"],
        ["config", "user.email", "prova@exemplo.test"],
        ["config", "commit.gpgsign", "false"],
        ["config", "core.hooksPath", ".githooks"],
    ):
        rodar([git, *comando], pasta)


def tentar_commit(git: str, pasta: Path, mensagem: str) -> subprocess.CompletedProcess[str]:
    rodar([git, "add", "-A"], pasta)
    return rodar([git, "commit", "-q", "-m", mensagem], pasta)


def provar_trava_do_commit(base: Path, projeto_python: Path) -> None:
    titulo("[4A] Trava do commit (templates/githooks/pre-commit)")
    git = shutil.which("git")
    if git is None:
        avisos.append("git ausente: a trava do commit NÃO foi conferida")
        return
    copiar(MODELOS / "gitignore-python", projeto_python / ".gitignore")
    preparar_repositorio(git, projeto_python)
    bom = tentar_commit(git, projeto_python, "feat: projeto bom")
    conferir(bom.returncode == 0, "projeto Python bom: o commit é aceito", bom.stdout + bom.stderr)
    escrever(projeto_python / "app" / "feio.py", "def  f( ):\n  return  1\n")
    ruim = tentar_commit(git, projeto_python, "feat: código fora do formato")
    recusou = ruim.returncode != 0 and "FALHOU em" in ruim.stdout + ruim.stderr
    conferir(recusou, "projeto Python com código fora do formato: o commit é recusado", ruim.stdout)
    registrados = rodar([git, "log", "--oneline"], projeto_python).stdout.strip().splitlines()
    conferir(len(registrados) == 1, "o commit recusado não entrou no histórico", registrados)
    (projeto_python / "app" / "feio.py").unlink()

    if shutil.which("npm") is None:
        avisos.append("npm ausente: a trava do commit em projeto Node NÃO foi conferida")
    else:
        for nome, saida, esperado in (("node-bom", 0, True), ("node-ruim", 1, False)):
            pasta = base / f"trava-{nome}"
            script = f'node -e "process.exit({saida})"'
            escrever(pasta / "package.json", json.dumps({"scripts": {"conferir": script}}) + "\n")
            preparar_repositorio(git, pasta)
            aceito = tentar_commit(git, pasta, "feat: teste").returncode == 0
            situacao = "aceito" if esperado else "recusado"
            conferir(
                aceito == esperado,
                f"projeto Node com conferência {situacao[:-1]}a: commit {situacao}",
            )
        casos = (("sem-script", '{"scripts": {}}\n'), ("sem-scripts", "{}\n"), ("json-ruim", "{"))
        for caso, conteudo in casos:
            pasta = base / f"trava-node-{caso}"
            escrever(pasta / "package.json", conteudo)
            preparar_repositorio(git, pasta)
            sem_script = tentar_commit(git, pasta, "feat: teste")
            conferir(
                sem_script.returncode != 0 and 'script "conferir"' in sem_script.stderr,
                f"projeto Node {caso}: commit recusado com explicação",
                sem_script.stderr,
            )
    vazio = base / "trava-sem-conferencia"
    escrever(vazio / "leia.txt", "sem comando de conferência\n")
    preparar_repositorio(git, vazio)
    sem = tentar_commit(git, vazio, "feat: teste")
    conferir(
        sem.returncode != 0 and "não tem comando de conferência" in sem.stderr,
        "projeto sem comando de conferência: commit recusado com explicação",
        sem.stderr,
    )


def provar_trava_do_pronto(
    nome: str, hook: list[str], pasta: Path, arquivo: str, textos: tuple[str, str]
) -> None:
    """A pasta chega com tudo commitado; o arquivo novo simula o que um comando criou."""
    titulo(f"[4B] Trava do pronto para {nome} (conferir-fim)")
    ruim, bom = textos
    parar = json.dumps({"cwd": str(pasta), "stop_hook_active": False})
    conferir(rodar(hook, pasta, parar).returncode == 0, "nada alterado: deixa encerrar")
    escrever(pasta / arquivo, ruim)
    travou = rodar(hook, pasta, parar)
    conferir(
        travou.returncode == SAIDA_DE_PROBLEMA_DO_HOOK and Path(arquivo).name in travou.stderr,
        "arquivo novo com problema (criado por comando): não deixa encerrar e diz qual é",
        travou.stderr,
    )
    de_novo = json.dumps({"cwd": str(pasta), "stop_hook_active": True})
    conferir(
        rodar(hook, pasta, de_novo).returncode == 0,
        "segunda tentativa seguida: deixa encerrar (sem laço)",
    )
    escrever(pasta / arquivo, bom)
    liberou = rodar(hook, pasta, parar)
    conferir(liberou.returncode == 0, "arquivo corrigido: deixa encerrar", liberou.stderr)
    (pasta / arquivo).unlink()
    conferir(
        rodar(hook, pasta, "isto não é JSON").returncode == 0,
        "entrada inválida: não trava o trabalho",
    )
    conferir(
        rodar(hook, pasta, "[]").returncode == 0,
        "entrada em formato inesperado: não trava o trabalho",
    )
    fora = pasta.parent / f"sem-git-{nome.lower()}"
    escrever(fora / arquivo, ruim)
    sem_git = rodar(hook, fora, json.dumps({"cwd": str(fora)}))
    conferir(
        sem_git.returncode == 0,
        "pasta que não é repositório git: não trava o trabalho",
        sem_git.stderr,
    )


def provar_python(base: Path) -> None:
    ruff, mypy = ferramenta("ruff"), ferramenta("mypy")
    if ruff is None:
        return
    pasta = base / "projeto-python"
    montar_projeto_python(pasta)
    provar_regras_python(pasta, ruff, mypy)
    provar_hook_python(pasta, ruff)
    if mypy is None or ferramenta("pytest") is None:
        avisos.append("mypy ou pytest ausente: o conferir.py NÃO foi conferido")
    else:
        provar_conferir(pasta)
        provar_trava_do_commit(base, pasta)
        hook = [sys.executable, str(pasta / ".claude" / "hooks" / "conferir-fim.py")]
        provar_trava_do_pronto(
            "Python", hook, pasta, "app/novo.py", ("def  f( ):\n  return  1\n", BOM_PY)
        )
    provar_scripts_do_kit(base, ruff, mypy)


# --------------------------------------------------------------------------- [6-7] JavaScript
def pasta_do_modulo(executavel: str, nome: str) -> Path | None:
    """Acha a pasta node_modules/<nome> a partir do executável (Linux, macOS e Windows)."""
    real = Path(executavel).resolve()
    candidatos = [
        pai for pai in real.parents if pai.name == nome and pai.parent.name == "node_modules"
    ]
    candidatos += [
        real.parent / "node_modules" / nome,
        real.parent.parent / "lib" / "node_modules" / nome,
    ]
    return next((candidato for candidato in candidatos if candidato.is_dir()), None)


def comandos_de_node() -> tuple[list[str], list[str], Path, Path] | None:
    """Devolve como chamar o ESLint e o Prettier pelo node, sem depender de .cmd nem de shell."""
    node, eslint, prettier = ferramenta("node"), ferramenta("eslint"), ferramenta("prettier")
    if node is None or eslint is None or prettier is None:
        return None
    modulo_eslint, modulo_prettier = (
        pasta_do_modulo(eslint, "eslint"),
        pasta_do_modulo(prettier, "prettier"),
    )
    if modulo_eslint is None or modulo_prettier is None:
        avisos.append(
            "pasta do eslint ou do prettier não encontrada: as provas de JavaScript NÃO rodaram"
        )
        return None
    chamar_eslint = [node, str(modulo_eslint / "bin" / "eslint.js")]
    chamar_prettier = [node, str(modulo_prettier / "bin" / "prettier.cjs")]
    return chamar_eslint, chamar_prettier, modulo_eslint, modulo_prettier


def regras_apontadas(eslint: list[str], arquivo: str) -> set[str]:
    saida = rodar([*eslint, "-c", str(PROVAS / "eslint.config.mjs"), "-f", "json", arquivo], RAIZ)
    try:
        relatorio = json.loads(saida.stdout)
    except json.JSONDecodeError:
        conferir(False, f"ESLint rodou em {arquivo}", saida.stderr)
        return set()
    return {
        mensagem["ruleId"] or "erro-de-análise"
        for item in relatorio
        for mensagem in item["messages"]
    }


def regras_do_kit(node: str) -> set[str]:
    codigo = (
        f'import("{(MODELOS / "eslint.regras.mjs").as_uri()}")'
        ".then((m) => console.log(JSON.stringify(Object.keys(m.regrasDoKit))))"
    )
    return set(json.loads(rodar([node, "-e", codigo], RAIZ).stdout or "[]"))


def provar_regras_js(eslint: list[str], prettier: list[str]) -> set[str]:
    titulo("[6] Regras de JavaScript (ESLint com eslint.regras.mjs e Prettier com prettierrc.json)")
    regras = regras_do_kit(eslint[0])
    conferir(bool(regras), f"o kit declara {len(regras)} regras de ESLint")
    bons = [
        "provas/js/bom.js",
        "provas/js/componente-bom.jsx",
        "templates/claude/hooks/conferir-edicao.mjs",
        "templates/claude/hooks/conferir-fim.mjs",
    ]
    for arquivo in bons:
        apontadas = regras_apontadas(eslint, arquivo)
        conferir(not apontadas, f"sem apontamento: {arquivo}", sorted(apontadas))
    apontadas = regras_apontadas(eslint, "provas/js/ruim.js")
    for regra in sorted(regras):
        conferir(regra in apontadas, f"{regra} pega o exemplo ruim")
    componente = regras_apontadas(eslint, "provas/js/componente-ruim.jsx")
    conferir(
        "max-lines-per-function" in componente,
        "componente de tela com mais de 120 linhas é recusado",
    )

    formato = [*prettier, "--config", str(MODELOS / "prettierrc.json"), "--check"]
    copiados_para_o_projeto = [
        *bons,
        "templates/eslint.regras.mjs",
        "templates/eslint.config.mjs",
        "templates/CHECKLIST-PRONTO.md",
        "templates/APRENDIZADOS.template.md",
        "templates/CLAUDE.template.md",
        "templates/claude/claude-security-guidance.md",
        "templates/claude/security-patterns.json",
        "templates/claude/settings.node.json",
        "templates/claude/settings.python.json",
        "templates/prettierrc.json",
    ]
    certo = rodar([*formato, *copiados_para_o_projeto], RAIZ)
    conferir(
        certo.returncode == 0,
        "tudo o que o kit manda copiar já está no formato do Prettier",
        certo.stdout,
    )
    recusou = rodar([*formato, "provas/js/ruim.js"], RAIZ).returncode != 0
    conferir(recusou, "formatador recusa a indentação do exemplo ruim")
    return regras


def ligar_pasta(origem: Path, destino: Path) -> None:
    """Liga uma pasta dentro de outra: atalho simbólico, ou junção no Windows sem privilégio."""
    try:
        destino.symlink_to(origem, target_is_directory=True)
    except OSError:
        cmd = shutil.which("cmd") or "cmd"
        rodar([cmd, "/c", "mklink", "/J", str(destino), str(origem)], destino.parent)


def montar_projeto_node(pasta: Path, modulo_eslint: Path, modulo_prettier: Path) -> None:
    (pasta / "node_modules").mkdir(parents=True)
    ligar_pasta(modulo_eslint, pasta / "node_modules" / "eslint")
    ligar_pasta(modulo_prettier, pasta / "node_modules" / "prettier")
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-edicao.mjs",
        pasta / ".claude" / "hooks" / "conferir-edicao.mjs",
    )
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-fim.mjs",
        pasta / ".claude" / "hooks" / "conferir-fim.mjs",
    )
    copiar(MODELOS / "eslint.regras.mjs", pasta / "eslint.regras.mjs")
    copiar(MODELOS / "prettierrc.json", pasta / ".prettierrc.json")
    copiar(MODELOS / "gitignore-node", pasta / ".gitignore")
    escrever(
        pasta / "eslint.config.mjs",
        'import { regrasDoKit } from "./eslint.regras.mjs";\n\n'
        'const linguagem = { ecmaVersion: "latest", sourceType: "module" };\n\n'
        'const arquivos = ["**/*.js"];\n\n'
        "export default [{ files: arquivos, languageOptions: linguagem, rules: regrasDoKit }];\n",
    )
    escrever(pasta / "package.json", '{ "type": "module" }\n')
    copiar(PROVAS / "js" / "ruim.js", pasta / "src" / "ruim.js")
    copiar(PROVAS / "js" / "bom.js", pasta / "src" / "bom.js")
    escrever(pasta / "src" / "notas.md", "# Notas\n* item com asterisco\n")


def provar_hook_node(
    base: Path, node: str, prettier: list[str], modulos: tuple[Path, Path]
) -> None:
    titulo("[7] Hook de edição para Node (conferir-edicao.mjs)")
    pasta = base / "projeto-node"
    montar_projeto_node(pasta, *modulos)
    hook = [node, str(pasta / ".claude" / "hooks" / "conferir-edicao.mjs")]
    resultado = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "src" / "ruim.js"))
    conferir(
        resultado.returncode == SAIDA_DE_PROBLEMA_DO_HOOK,
        "arquivo ruim: sai com 2",
        resultado.stderr,
    )
    conferir("eqeqeq" in resultado.stderr, "arquivo ruim: a mensagem cita a regra (eqeqeq)")
    formatado = rodar([*prettier, "--check", "src/ruim.js"], pasta).returncode == 0
    conferir(formatado, "arquivo ruim: o hook corrigiu a indentação")
    bom = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "src" / "bom.js"))
    conferir(bom.returncode == 0, "arquivo bom: sai com 0", bom.stderr)
    notas = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "src" / "notas.md"))
    formatou = rodar([*prettier, "--check", "src/notas.md"], pasta).returncode == 0
    conferir(
        notas.returncode == 0 and formatou,
        "Markdown: formata e não passa pelo ESLint",
        notas.stderr,
    )
    outro = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "notas.txt"))
    conferir(outro.returncode == 0, "arquivo de outro tipo: não faz nada")
    sumiu = rodar(hook, pasta, entrada_do_hook(pasta, pasta / "src" / "nao_existe.js"))
    conferir(sumiu.returncode == 0, "arquivo que não existe mais: não interrompe", sumiu.stderr)
    conferir(
        rodar(hook, pasta, "isto não é JSON").returncode == 0,
        "entrada inválida: não trava o trabalho",
    )
    conferir(
        rodar(hook, pasta, "{}").returncode == 0,
        "entrada sem caminho de arquivo: não trava o trabalho",
    )
    vazio = base / "projeto-sem-dependencias"
    escrever(vazio / "a.js", "var x = 1\n")
    sem_modulos = rodar(hook, vazio, entrada_do_hook(vazio, vazio / "a.js"))
    conferir(
        sem_modulos.returncode == 0,
        "projeto sem node_modules: avisa e não trava",
        sem_modulos.stderr,
    )
    git = shutil.which("git")
    if git is None:
        avisos.append("git ausente: a trava do pronto em Node NÃO foi conferida")
        return
    (pasta / "src" / "ruim.js").unlink()
    for comando in (
        ["init", "-q"],
        ["config", "user.name", "Prova do Kit"],
        ["config", "user.email", "prova@exemplo.test"],
        ["config", "commit.gpgsign", "false"],
    ):
        rodar([git, *comando], pasta)
    tentar_commit(git, pasta, "feat: projeto bom")
    fim = [node, str(pasta / ".claude" / "hooks" / "conferir-fim.mjs")]
    provar_trava_do_pronto("Node", fim, pasta, "src/novo.js", (RUIM_JS, BOM_JS))


def provar_js(base: Path) -> set[str]:
    comandos = comandos_de_node()
    if comandos is None:
        return set()
    eslint, prettier, modulo_eslint, modulo_prettier = comandos
    regras = provar_regras_js(eslint, prettier)
    provar_hook_node(base, eslint[0], prettier, (modulo_eslint, modulo_prettier))
    return regras


# --------------------------------------------------------------------------- [13] Docker
APP_DE_EXEMPLO = """from fastapi import FastAPI

app = FastAPI()


@app.get("/saude")
def saude() -> dict[str, str]:
    return {"situacao": "ok"}
"""
ESPERA_DA_SAUDE_EM_SEGUNDOS = 120
INTERVALO_EM_SEGUNDOS = 5


def provar_docker(base: Path) -> None:
    titulo("[13] Imagem Docker do modelo (Dockerfile.python)")
    docker = shutil.which("docker")
    if os.environ.get("PROVAS_COM_REDE") != "1" or docker is None or os.name == "nt":
        avisos.append("sem rede, sem Docker ou em Windows: a imagem Docker NÃO foi conferida aqui")
        return
    pasta = base / "projeto-docker"
    copiar(MODELOS / "Dockerfile.python", pasta / "Dockerfile")
    copiar(MODELOS / "dockerignore", pasta / ".dockerignore")
    escrever(pasta / "requirements.txt", "fastapi\nuvicorn\n")
    escrever(pasta / "app" / "__init__.py", "")
    escrever(pasta / "app" / "main.py", APP_DE_EXEMPLO)
    escrever(pasta / ".env", "SEGREDO=nao-pode-entrar-na-imagem\n")
    construir = rodar([docker, "build", "-q", "-t", "kit-prova", "."], pasta)
    conferir(
        construir.returncode == 0, "a imagem é construída", construir.stderr[-TAMANHO_DO_TRECHO:]
    )
    if construir.returncode != 0:
        return
    usuario = rodar([docker, "run", "--rm", "kit-prova", "id", "-u"], pasta).stdout.strip()
    conferir(usuario == "10001", "o processo roda sem root (usuário 10001)", usuario)
    segredo = rodar([docker, "run", "--rm", "kit-prova", "ls", "-a", "/app"], pasta).stdout
    conferir(".env" not in segredo.split(), "o arquivo .env não entra na imagem", segredo)
    rodar([docker, "run", "-d", "--name", "kit-prova-no-ar", "kit-prova"], pasta)
    situacao = ""
    for _ in range(ESPERA_DA_SAUDE_EM_SEGUNDOS // INTERVALO_EM_SEGUNDOS):
        consulta = [docker, "inspect", "--format", "{{.State.Health.Status}}", "kit-prova-no-ar"]
        situacao = rodar(consulta, pasta).stdout.strip()
        if situacao in {"healthy", "unhealthy"}:
            break
        time.sleep(INTERVALO_EM_SEGUNDOS)
    registro = rodar([docker, "logs", "kit-prova-no-ar"], pasta)
    conferir(
        situacao == "healthy",
        "a aplicação sobe e responde na rota /saude",
        situacao + registro.stderr,
    )
    rodar([docker, "rm", "-f", "kit-prova-no-ar"], pasta)


# --------------------------------------------------------------------------- [12] instalador
ESPERADO_NO_PROJETO = {
    "python": [
        "pyproject.toml",
        "conferir.py",
        ".claude/hooks/conferir-edicao.py",
        ".claude/hooks/conferir-fim.py",
    ],
    "node": [
        "eslint.config.mjs",
        "eslint.regras.mjs",
        ".prettierrc.json",
        ".prettierignore",
        "tsconfig.json",
    ],
    "comum": [
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".githooks/pre-commit",
        ".claude/settings.json",
        ".claude/claude-security-guidance.md",
        ".claude/security-patterns.json",
        "CLAUDE.md",
        "APRENDIZADOS.md",
        "docs/CHECKLIST-PRONTO.md",
        ".github/workflows/ci.yml",
        ".github/workflows/codeql.yml",
        ".github/dependabot.yml",
        ".kit-versao",
    ],
}
ECOSSISTEMAS_ESPERADOS = {"python": {"pip", "github-actions"}, "node": {"npm", "github-actions"}}
LINGUAGEM_ESPERADA = {"python": "[python]", "node": "[javascript-typescript]"}


def instalar_kit(*argumentos: str) -> subprocess.CompletedProcess[str]:
    return rodar([sys.executable, str(INSTALADOR), *argumentos], RAIZ)


def provar_instalacao(base: Path, tipo: str, git: str) -> Path:
    pasta = base / f"instalado-{tipo}"
    pasta.mkdir()
    rodar([git, "init", "-q"], pasta)
    primeira = instalar_kit("projeto", str(pasta), "--tipo", tipo)
    conferir(
        primeira.returncode == 0, f"{tipo}: instala sem erro", primeira.stdout + primeira.stderr
    )
    faltando = [
        a
        for a in ESPERADO_NO_PROJETO[tipo] + ESPERADO_NO_PROJETO["comum"]
        if not (pasta / a).is_file()
    ]
    conferir(not faltando, f"{tipo}: todos os arquivos esperados foram criados", faltando)
    ajustes = json.loads(ler(pasta / ".claude" / "settings.json"))["hooks"]
    alvos = [
        hook["args"][0].replace("${CLAUDE_PROJECT_DIR}/", "")
        for evento in ajustes.values()
        for grupo in evento
        for hook in grupo["hooks"]
    ]
    orfaos = [alvo for alvo in alvos if not (pasta / alvo).is_file()]
    conferir(
        len(alvos) > 1 and not orfaos,
        f"{tipo}: todo hook do settings.json aponta para arquivo instalado",
        orfaos,
    )
    dependabot = ler(pasta / ".github" / "dependabot.yml")
    ecossistemas = set(re.findall(r'package-ecosystem: "([a-z-]+)"', dependabot))
    conferir(
        ecossistemas == ECOSSISTEMAS_ESPERADOS[tipo],
        f"{tipo}: dependabot só com o que o projeto usa",
        ecossistemas,
    )
    codeql = ler(pasta / ".github" / "workflows" / "codeql.yml")
    conferir(
        f"language: {LINGUAGEM_ESPERADA[tipo]}" in codeql, f"{tipo}: CodeQL na linguagem do projeto"
    )
    trava = rodar([git, "config", "core.hooksPath"], pasta).stdout.strip()
    conferir(trava == ".githooks", f"{tipo}: trava do commit ligada no git", trava)

    escrever(pasta / "CLAUDE.md", "# Editado pela pessoa\n")
    segunda = instalar_kit("projeto", str(pasta), "--tipo", tipo)
    conferir(
        "criado" not in segunda.stdout, f"{tipo}: instalar de novo não cria nada", segunda.stdout
    )
    conferir(
        ler(pasta / "CLAUDE.md") == "# Editado pela pessoa\n",
        f"{tipo}: arquivo editado pela pessoa é mantido",
    )
    forcada = instalar_kit("projeto", str(pasta), "--tipo", tipo, "--forcar")
    substituiu = "substituído" in forcada.stdout and "Editado pela pessoa" not in ler(
        pasta / "CLAUDE.md"
    )
    conferir(substituiu, f"{tipo}: --forcar substitui o arquivo")
    return pasta


def provar_instalador(base: Path) -> None:
    titulo("[12] Instalador (instalar.py)")
    git = shutil.which("git")
    if git is None:
        avisos.append("git ausente: o instalador NÃO foi conferido")
        return
    python = provar_instalacao(base, "python", git)
    provar_instalacao(base, "node", git)
    if shutil.which("ruff") and shutil.which("mypy") and shutil.which("pytest"):
        copiar(PROVAS / "python" / "bom.py", python / "app" / "bom.py")
        escrever(python / "app" / "__init__.py", "")
        escrever(python / "tests" / "__init__.py", "")
        escrever(python / "tests" / "test_bom.py", TESTE_TIPICO)
        confere = rodar([sys.executable, "conferir.py"], python)
        conferir(
            confere.returncode == 0,
            "python: projeto recém-instalado passa na conferência",
            confere.stdout[-TAMANHO_DO_TRECHO:],
        )

    casa = base / "casa"
    maquina = instalar_kit("maquina", "--pasta", str(casa))
    esperados = ["skills/conferir-codigo/SKILL.md", "skills/conferir-codigo/armadilhas.md"]
    esperados += ["skills/conferir-codigo/codigo-limpo.md", "output-styles/professor.md"]
    faltando = [a for a in esperados if not (casa / a).is_file()]
    conferir(
        maquina.returncode == 0 and not faltando,
        "máquina: skill e estilo de saída instalados",
        faltando,
    )
    conferir(
        "criado" not in instalar_kit("maquina", "--pasta", str(casa)).stdout,
        "máquina: instalar de novo não cria nada",
    )

    inexistente = instalar_kit("projeto", str(base / "nao-existe"), "--tipo", "python")
    conferir(
        inexistente.returncode == SAIDA_DE_PROBLEMA_DO_HOOK and "não existe" in inexistente.stdout,
        "pasta inexistente: recusa e explica",
    )
    no_kit = instalar_kit("projeto", str(RAIZ), "--tipo", "python")
    conferir(no_kit.returncode == SAIDA_DE_PROBLEMA_DO_HOOK, "pasta do próprio kit: recusa")
    conferir(not (RAIZ / ".kit-versao").exists(), "pasta do próprio kit: nada foi copiado")
    tipo_errado = instalar_kit("projeto", str(base), "--tipo", "java")
    conferir(tipo_errado.returncode != 0, "tipo de projeto desconhecido: recusa")
    conferir(instalar_kit().returncode != 0, "sem argumentos: mostra o uso e não faz nada")


# --------------------------------------------------------------------------- [11] TypeScript
def montar_projeto_typescript(pasta: Path) -> None:
    """Monta o projeto com o instalador do kit: é o que um projeto de verdade recebe."""
    pasta.mkdir(parents=True)
    rodar([sys.executable, str(INSTALADOR), "projeto", str(pasta), "--tipo", "node"], RAIZ)
    copiar(PROVAS / "ts" / "bom.ts", pasta / "src" / "bom.ts")
    escrever(pasta / "package.json", '{\n  "type": "module",\n  "private": true\n}\n')


def apontamentos_do_eslint(comando: list[str], pasta: Path, alvo: str) -> dict[str, set[str]]:
    saida = rodar([*comando, alvo, "--max-warnings", "0", "-f", "json"], pasta)
    try:
        relatorio = json.loads(saida.stdout)
    except json.JSONDecodeError:
        conferir(False, f"ESLint com TypeScript rodou em {alvo}", saida.stderr or saida.stdout)
        return {}
    return {
        Path(item["filePath"]).name: {m["ruleId"] or m["message"] for m in item["messages"]}
        for item in relatorio
        if item["messages"]
    }


def provar_typescript(base: Path) -> None:
    titulo("[11] Configuração de TypeScript (eslint.config.mjs, com pacotes baixados da internet)")
    if os.environ.get("PROVAS_COM_REDE") != "1":
        avisos.append(
            "PROVAS_COM_REDE não está ligada: a configuração de TypeScript NÃO foi conferida"
        )
        return
    node, npm = ferramenta("node"), ferramenta("npm")
    if node is None or npm is None:
        return
    pasta = base / "projeto-typescript"
    montar_projeto_typescript(pasta)
    instalar = rodar(
        [npm, "install", "--no-audit", "--no-fund", "--save-dev", *PACOTES_DE_TYPESCRIPT], pasta
    )
    conferir(instalar.returncode == 0, "pacotes instalados", instalar.stderr[-TAMANHO_DO_TRECHO:])
    if instalar.returncode != 0:
        return
    print(
        "  versões:",
        rodar([npm, "ls", "--depth=0"], pasta).stdout.replace("\n", " ")[:TAMANHO_DO_TRECHO],
    )
    modulos = pasta / "node_modules"
    eslint = [node, str(modulos / "eslint" / "bin" / "eslint.js")]
    limpo = apontamentos_do_eslint(eslint, pasta, ".")
    conferir(
        not limpo, "projeto bom (código, configuração e hook) sem apontamento nem aviso", limpo
    )
    tipos = rodar([node, str(modulos / "typescript" / "bin" / "tsc"), "--noEmit"], pasta)
    conferir(tipos.returncode == 0, "tsc estrito passa no exemplo bom", tipos.stdout)
    formato = rodar(
        [node, str(modulos / "prettier" / "bin" / "prettier.cjs"), "--check", "."], pasta
    )
    fora = (formato.stdout + formato.stderr).replace("Checking formatting...", "").strip()
    conferir(formato.returncode == 0, "prettier --check . passa no projeto montado", fora)
    copiar(PROVAS / "ts" / "ruim.ts", pasta / "src" / "ruim.ts")
    apontadas = apontamentos_do_eslint(eslint, pasta, "src/ruim.ts").get("ruim.ts", set())
    for regra, significado in ESPERADO_TS.items():
        conferir(regra in apontadas, f"{regra} pega: {significado}", sorted(apontadas))
    compilou = rodar([node, str(modulos / "typescript" / "bin" / "tsc"), "--noEmit"], pasta)
    recusou = compilou.returncode != 0 and "TS7030" in compilou.stdout
    conferir(
        recusou, "tsc recusa função que nem sempre retorna (noImplicitReturns)", compilou.stdout
    )


# --------------------------------------------------------------------------- [14] ambiente real
SOMA = '''"""Exemplo mínimo com cobertura total."""


def somar(primeiro: int, segundo: int) -> int:
    return primeiro + segundo
'''
TESTE_DA_SOMA = """from app.soma import somar


def test_somar():
    assert somar(2, 3) == 5
"""
SAIDAS_DA_AUDITORIA = {0, 1}  # 1 = achou vulnerabilidade publicada hoje: a etapa rodou


def etapas_do_ci(arquivo: Path) -> list[list[str]] | None:
    """Os comandos das etapas `run` de um workflow, na ordem, já separados em argumentos."""
    try:
        import yaml  # type: ignore[import-untyped, unused-ignore]  # noqa: PLC0415
    except ImportError:
        avisos.append("pyyaml não está instalado: as etapas do CI modelo NÃO foram executadas")
        return None
    passos = yaml.safe_load(ler(arquivo))["jobs"]["qualidade"]["steps"]
    linhas = [linha for passo in passos for linha in passo.get("run", "").splitlines()]
    return [shlex.split(linha) for linha in linhas if linha.strip()]


def provar_ambiente_real(base: Path) -> None:
    titulo("[14] Projeto Python instalado de verdade (ambiente virtual, etapas do CI e commit)")
    git = shutil.which("git")
    if os.environ.get("PROVAS_COM_REDE") != "1" or git is None:
        avisos.append("sem rede ou sem git: o projeto Python de verdade NÃO foi conferido aqui")
        return
    pasta = base / "ambiente-real"
    pasta.mkdir()
    rodar([git, "init", "-q"], pasta)
    for ajuste in (("user.name", "Prova do Kit"), ("user.email", "prova@exemplo.test")):
        rodar([git, "config", *ajuste], pasta)
    rodar([git, "config", "commit.gpgsign", "false"], pasta)
    instalar_kit("projeto", str(pasta), "--tipo", "python")
    escrever(pasta / "app" / "__init__.py", "")
    escrever(pasta / "app" / "soma.py", SOMA)
    escrever(pasta / "tests" / "__init__.py", "")
    escrever(pasta / "tests" / "test_soma.py", TESTE_DA_SOMA)
    escrever(pasta / "scripts" / "__init__.py", "")  # segunda pasta na raiz: o pip tem de aceitar
    etapas = etapas_do_ci(pasta / ".github" / "workflows" / "ci.yml")
    if etapas is None:
        return
    criar = rodar([sys.executable, "-m", "venv", ".venv"], pasta)
    conferir(criar.returncode == 0, "ambiente virtual criado", criar.stderr)
    executaveis = pasta / ".venv" / ("Scripts" if os.name == "nt" else "bin")
    ambiente = {
        **os.environ,
        "PATH": f"{executaveis}{os.pathsep}{os.environ.get('PATH', '')}",
        "PIP_CONSTRAINT": str(PROVAS / "requisitos.txt"),
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
    }
    for programa, *argumentos in etapas:
        executavel = shutil.which(programa, path=str(executaveis))
        etapa = " ".join([programa, *argumentos])
        if executavel is None:
            conferir(False, f"etapa do CI modelo: {etapa}", "programa não está no ambiente virtual")
            return
        saida = rodar([executavel, *argumentos], pasta, ambiente=ambiente)
        aceitas = SAIDAS_DA_AUDITORIA if programa == "pip-audit" else {0}
        registro = (saida.stdout + saida.stderr)[-TAMANHO_DO_TRECHO:]
        conferir(saida.returncode in aceitas, f"etapa do CI modelo: {etapa}", registro)
        if saida.returncode not in aceitas:
            return
    python = shutil.which("python", path=str(executaveis)) or sys.executable
    confere = rodar([python, "conferir.py"], pasta, ambiente=ambiente)
    conferir(
        confere.returncode == 0,
        "conferir.py passa com as ferramentas do ambiente virtual",
        confere.stdout[-TAMANHO_DO_TRECHO:],
    )
    commit = tentar_commit(git, pasta, "feat: primeiro commit")
    conferir(
        commit.returncode == 0,
        "primeiro commit do projeto recém-instalado é aceito pela trava",
        (commit.stdout + commit.stderr)[-TAMANHO_DO_TRECHO:],
    )
    rastreados = rodar([git, "ls-files"], pasta).stdout
    conferir(
        ".venv" not in rastreados and "egg-info" not in rastreados,
        "ambiente virtual e pasta egg-info ficam fora do commit",
    )


# --------------------------------------------------------------------------- [8-9] git e segurança
def provar_modelos_de_git(base: Path) -> None:
    titulo("[8] Modelos de .gitignore e .gitattributes")
    git = shutil.which("git")
    if git is None:
        avisos.append("git ausente: os modelos de .gitignore NÃO foram conferidos")
        return
    casos = {
        "gitignore-python": (
            [".env", ".env.local", ".venv/x", "app/__pycache__/a.pyc"],
            [".env.example", "app/a.py"],
        ),
        "gitignore-node": (
            [".env", "node_modules/x/a.js", "dist/a.js"],
            [".env.example", "src/a.ts"],
        ),
    }
    for modelo, (ignorados, mantidos) in casos.items():
        pasta = base / modelo
        copiar(MODELOS / modelo, pasta / ".gitignore")
        copiar(MODELOS / "gitattributes", pasta / ".gitattributes")
        rodar([git, "init", "-q"], pasta)
        for caminho in ignorados:
            ignorou = rodar([git, "check-ignore", "-q", caminho], pasta).returncode == 0
            conferir(ignorou, f"{modelo} ignora {caminho}")
        for caminho in mantidos:
            manteve = rodar([git, "check-ignore", "-q", caminho], pasta).returncode != 0
            conferir(manteve, f"{modelo} mantém {caminho}")
    fim_de_linha = rodar([git, "check-attr", "eol", "--", "a.py"], base / "gitignore-python").stdout
    conferir("eol: lf" in fim_de_linha, "gitattributes força fim de linha LF", fim_de_linha)


def provar_padroes_de_seguranca() -> None:
    titulo("[9] Padrões de segurança (templates/claude/security-patterns.json)")
    dados = json.loads(ler(MODELOS / "claude" / "security-patterns.json"))
    com_expressao = [padrao for padrao in dados["patterns"] if "regex" in padrao]
    sem_caso = sorted({padrao["rule_name"] for padrao in com_expressao} - set(CASOS_DE_SEGURANCA))
    conferir(not sem_caso, "todo padrão com expressão tem casos de prova", sem_caso)
    for padrao in com_expressao:
        nome = padrao["rule_name"]
        if nome not in CASOS_DE_SEGURANCA:
            continue
        expressao = re.compile(padrao["regex"])
        deve_pegar, nao_deve_pegar = CASOS_DE_SEGURANCA[nome]
        pegou = all(expressao.search(texto) for texto in deve_pegar)
        conferir(pegou, f"{nome} pega os {len(deve_pegar)} casos ruins")
        liberou = not any(expressao.search(texto) for texto in nao_deve_pegar)
        conferir(liberou, f"{nome} deixa passar os {len(nao_deve_pegar)} casos bons")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    provar_estrutura()
    with tempfile.TemporaryDirectory(prefix="provas-kit-") as temporaria:
        base = Path(temporaria)
        provar_python(base)
        regras_js = provar_js(base)
        provar_modelos_de_git(base)
        provar_instalador(base)
        provar_typescript(base)
        provar_ambiente_real(base)
        provar_docker(base)
    provar_padroes_de_seguranca()
    titulo("[10] Coerência entre as listas da skill e as provas")
    provar_codigos_citados(regras_js)
    print()
    for aviso in avisos:
        print(f"AVISO: {aviso}")
    if falhas:
        print(f"\n{len(falhas)} prova(s) FALHARAM:")
        for falha in falhas:
            print(f"  - {falha}")
        return 1
    print(
        "Todas as provas passaram."
        if not avisos
        else "As provas que rodaram passaram; veja os avisos."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
