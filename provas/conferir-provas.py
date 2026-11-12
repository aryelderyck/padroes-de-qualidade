"""Provas do kit: confirma que cada regra automática pega o exemplo ruim e deixa passar o bom.

Uso, na raiz do kit:  python provas/conferir-provas.py
Precisa de ruff, mypy, pytest, node, eslint e prettier (versões em .github/workflows/kit.yml).
Monta projetos de exemplo numa pasta temporária, com os modelos de templates/ nos lugares em que
ficam num projeto de verdade, e roda as ferramentas de verdade. Sai com 1 se alguma prova falhar.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / "templates"
PROVAS = RAIZ / "provas"
LIMITE_DE_LINHAS_DO_REGRAS = 80
SAIDA_DE_PROBLEMA_DO_HOOK = 2
SAIDA_SEM_FERRAMENTA = 3
TAMANHO_DO_TRECHO = 300
# Ambiente sem nenhuma ferramenta no PATH (o Windows precisa do SYSTEMROOT para iniciar o Python).
SEM_FERRAMENTAS = {"PATH": "", "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
PACOTES_DE_TYPESCRIPT = [
    "eslint@10.1.0",
    "@eslint/js",
    "typescript-eslint",
    "typescript",
    "globals",
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
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-edicao.py", pasta / "kit" / "conferir_edicao.py"
    )
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
    copiar(MODELOS / "eslint.regras.mjs", pasta / "eslint.regras.mjs")
    copiar(MODELOS / "prettierrc.json", pasta / ".prettierrc.json")
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


def provar_js(base: Path) -> set[str]:
    comandos = comandos_de_node()
    if comandos is None:
        return set()
    eslint, prettier, modulo_eslint, modulo_prettier = comandos
    regras = provar_regras_js(eslint, prettier)
    provar_hook_node(base, eslint[0], prettier, (modulo_eslint, modulo_prettier))
    return regras


# --------------------------------------------------------------------------- [11] TypeScript
def montar_projeto_typescript(pasta: Path) -> None:
    copiar(MODELOS / "eslint.regras.mjs", pasta / "eslint.regras.mjs")
    copiar(MODELOS / "eslint.config.mjs", pasta / "eslint.config.mjs")
    copiar(MODELOS / "prettierrc.json", pasta / ".prettierrc.json")
    copiar(MODELOS / "prettierignore", pasta / ".prettierignore")
    copiar(
        MODELOS / "claude" / "hooks" / "conferir-edicao.mjs",
        pasta / ".claude" / "hooks" / "conferir-edicao.mjs",
    )
    copiar(PROVAS / "ts" / "tsconfig.json", pasta / "tsconfig.json")
    copiar(PROVAS / "ts" / "bom.ts", pasta / "src" / "bom.ts")
    escrever(pasta / "package.json", '{ "type": "module", "private": true }\n')


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
    conferir(formato.returncode == 0, "prettier --check . passa no projeto montado", formato.stdout)
    copiar(PROVAS / "ts" / "ruim.ts", pasta / "src" / "ruim.ts")
    apontadas = apontamentos_do_eslint(eslint, pasta, "src/ruim.ts").get("ruim.ts", set())
    for regra, significado in ESPERADO_TS.items():
        conferir(regra in apontadas, f"{regra} pega: {significado}", sorted(apontadas))


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
        provar_typescript(base)
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
