"""Provas do kit: confirma que cada regra automática pega o exemplo ruim e deixa passar o bom.

Uso, na raiz do kit:  python provas/conferir-provas.py
Precisa de ruff, mypy, eslint e prettier instalados (as versões estão em .github/workflows/kit.yml).
Monta projetos de exemplo numa pasta temporária, com os modelos de templates/ nos lugares em que
ficam num projeto de verdade, e roda as ferramentas de verdade. Sai com 1 se alguma prova falhar.
"""

import json
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
EXTENSOES_DE_TEXTO = {".md", ".py", ".js", ".mjs", ".json", ".toml", ".yml", ".yaml", ".txt", ""}
PASTAS_IGNORADAS = {".git", ".mypy_cache", ".ruff_cache", "__pycache__", "node_modules"}

# O que o linter do kit PRECISA apontar em provas/python/ruim.py.
ESPERADO_PYTHON = {
    "S608": "SQL montado com texto",
    "B006": "valor padrão mutável",
    "B023": "função de laço que captura a variável do laço",
    "DTZ005": "data e hora sem fuso",
    "PLR2004": "número mágico",
    "PLR0913": "parâmetros demais",
    "C901": "função complexa demais",
    "E722": "except sem tipo",
    "S110": "exceção engolida",
    "T201": "print esquecido",
    "F841": "variável sem uso",
    "E711": "comparação com None usando ==",
    "N802": "nome de função fora do padrão",
    "S113": "chamada de rede sem tempo limite",
    "A001": "nome que esconde função embutida",
    "ERA001": "código comentado",
    "ARG001": "parâmetro sem uso",
}

# O que o ESLint do kit PRECISA apontar em provas/js/ruim.js.
ESPERADO_JS = {
    "eqeqeq": "comparação com conversão implícita",
    "no-eval": "eval",
    "radix": "parseInt sem a base",
    "no-magic-numbers": "número mágico",
    "max-params": "parâmetros demais",
    "array-callback-return": "map sem return",
    "no-loop-func": "função de laço que captura a variável do laço",
    "max-depth": "aninhamento demais",
    "no-param-reassign": "parâmetro reatribuído",
    "prefer-const": "let que nunca muda",
    "complexity": "função complexa demais",
    "no-unused-vars": "variável sem uso",
    "default-case": "switch sem caso padrão",
    "camelcase": "nome fora do padrão",
    "no-var": "var",
    "no-else-return": "else depois de return",
    "curly": "if sem chaves",
}

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

falhas: list[str] = []
avisos: list[str] = []


def conferir(condicao: bool, descricao: str) -> None:
    print(f"  {'ok   ' if condicao else 'FALHA'} {descricao}")
    if not condicao:
        falhas.append(descricao)


def rodar(comando: list[str], pasta: Path, entrada: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        comando, cwd=pasta, input=entrada, capture_output=True, encoding="utf-8", errors="replace", check=False
    )


def ferramenta(nome: str) -> str | None:
    caminho = shutil.which(nome)
    if caminho is None:
        avisos.append(f"{nome} não está instalado: as provas que dependem dele NÃO foram conferidas")
    return caminho


# --------------------------------------------------------------------------- estrutura do kit
def provar_estrutura() -> None:
    print("\n[1] Estrutura do kit")
    quebrados = []
    for arquivo in RAIZ.rglob("*.md"):
        if PASTAS_IGNORADAS & set(arquivo.parts):
            continue
        for alvo in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", arquivo.read_text(encoding="utf-8")):
            if not alvo.startswith(("http", "mailto:")) and not (arquivo.parent / alvo).exists():
                quebrados.append(f"{arquivo.relative_to(RAIZ)} -> {alvo}")
    conferir(not quebrados, f"links internos dos .md existem {quebrados[:3] if quebrados else ''}")

    linhas = len((RAIZ / "REGRAS.md").read_text(encoding="utf-8").splitlines())
    conferir(linhas <= LIMITE_DE_LINHAS_DO_REGRAS, f"REGRAS.md tem {linhas} linhas (limite {LIMITE_DE_LINHAS_DO_REGRAS})")

    for arquivo in RAIZ.rglob("*.json"):
        if not PASTAS_IGNORADAS & set(arquivo.parts):
            try:
                json.loads(arquivo.read_text(encoding="utf-8"))
            except json.JSONDecodeError as erro:
                conferir(False, f"JSON válido: {arquivo.relative_to(RAIZ)} ({erro})")
    for arquivo in RAIZ.rglob("*.toml"):
        if not PASTAS_IGNORADAS & set(arquivo.parts):
            try:
                tomllib.loads(arquivo.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as erro:
                conferir(False, f"TOML válido: {arquivo.relative_to(RAIZ)} ({erro})")
    conferir(True, "arquivos JSON e TOML abrem sem erro")

    try:
        import yaml  # noqa: PLC0415 (dependência opcional: sem ela, a prova de YAML é pulada com aviso)
    except ImportError:
        avisos.append("pyyaml não está instalado: YAML e cabeçalhos NÃO foram conferidos")
    else:
        for arquivo in [*RAIZ.rglob("*.yml"), *RAIZ.rglob("*.yaml")]:
            if not PASTAS_IGNORADAS & set(arquivo.parts):
                yaml.safe_load(arquivo.read_text(encoding="utf-8"))
        conferir(True, "arquivos YAML abrem sem erro")
        for arquivo in [*MODELOS.glob("skills/*/SKILL.md"), *MODELOS.glob("output-styles/*.md")]:
            cabecalho = yaml.safe_load(arquivo.read_text(encoding="utf-8").split("---")[1])
            conferir(
                {"name", "description"} <= set(cabecalho),
                f"cabeçalho com name e description: {arquivo.relative_to(RAIZ)}",
            )

    com_cr = [
        str(arquivo.relative_to(RAIZ))
        for arquivo in RAIZ.rglob("*")
        if arquivo.is_file()
        and arquivo.suffix in EXTENSOES_DE_TEXTO
        and not PASTAS_IGNORADAS & set(arquivo.parts)
        and b"\r" in arquivo.read_bytes()
    ]
    conferir(not com_cr, f"nenhum arquivo com fim de linha CRLF {com_cr[:3] if com_cr else ''}")


# --------------------------------------------------------------------------- Python
def montar_projeto_python(pasta: Path) -> None:
    (pasta / ".claude" / "hooks").mkdir(parents=True)
    (pasta / "app").mkdir()
    shutil.copy(MODELOS / "pyproject-python.toml", pasta / "pyproject.toml")
    shutil.copy(MODELOS / "conferir.py", pasta / "conferir.py")
    shutil.copy(MODELOS / "claude" / "hooks" / "conferir-edicao.py", pasta / ".claude" / "hooks" / "conferir-edicao.py")
    shutil.copy(PROVAS / "python" / "bom.py", pasta / "app" / "bom.py")


def provar_python(base: Path) -> None:
    print("\n[2] Regras de Python (ruff e mypy com o pyproject do kit)")
    ruff, mypy = ferramenta("ruff"), ferramenta("mypy")
    if ruff is None:
        return
    pasta = base / "projeto-python"
    pasta.mkdir()
    montar_projeto_python(pasta)

    limpo = rodar([ruff, "check", "--output-format", "json", "."], pasta)
    achados = json.loads(limpo.stdout or "[]")
    conferir(not achados, f"exemplo bom e scripts do kit sem apontamento {[a['code'] for a in achados][:5] if achados else ''}")
    conferir(rodar([ruff, "format", "--check", "."], pasta).returncode == 0, "exemplo bom e scripts do kit já formatados")
    if mypy is not None:
        tipos = rodar([mypy, "."], pasta)
        conferir(tipos.returncode == 0, f"mypy estrito passa no exemplo bom e nos scripts {tipos.stdout.strip()[-200:] if tipos.returncode else ''}")

    shutil.copy(PROVAS / "python" / "ruim.py", pasta / "app" / "ruim.py")
    ruim = json.loads(rodar([ruff, "check", "--output-format", "json", "app/ruim.py"], pasta).stdout or "[]")
    codigos = {achado["code"] for achado in ruim}
    for codigo, significado in ESPERADO_PYTHON.items():
        conferir(codigo in codigos, f"{codigo} pega: {significado}")
    conferir(rodar([ruff, "format", "--check", "app/ruim.py"], pasta).returncode != 0, "formatador recusa a indentação do exemplo ruim")

    print("\n[3] Hook de edição para Python (conferir-edicao.py)")
    hook = [sys.executable, str(pasta / ".claude" / "hooks" / "conferir-edicao.py")]
    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "app" / "ruim.py")}})
    resultado = rodar(hook, pasta, entrada)
    conferir(resultado.returncode == SAIDA_DE_PROBLEMA_DO_HOOK, "arquivo ruim: o hook sai com 2 e devolve os problemas")
    conferir("S608" in resultado.stderr, "arquivo ruim: a mensagem cita a regra (S608)")
    conferir(rodar([ruff, "format", "--check", "app/ruim.py"], pasta).returncode == 0, "arquivo ruim: o hook corrigiu a indentação")
    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "app" / "bom.py")}})
    conferir(rodar(hook, pasta, entrada).returncode == 0, "arquivo bom: o hook sai com 0")
    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "notas.txt")}})
    conferir(rodar(hook, pasta, entrada).returncode == 0, "arquivo que não é Python: o hook não faz nada")
    conferir(rodar(hook, pasta, "isto não é JSON").returncode == 0, "entrada inválida: o hook não trava o trabalho")

    print("\n[4] Comando único (conferir.py)")
    (pasta / "app" / "ruim.py").unlink()
    (pasta / "tests").mkdir()
    (pasta / "tests" / "test_bom.py").write_text(
        "from app.bom import classificar\n\n\ndef test_classificar_desconhecido() -> None:\n    assert classificar(99) == \"outro\"\n",
        encoding="utf-8",
    )
    (pasta / "app" / "__init__.py").write_text("", encoding="utf-8")
    (pasta / "tests" / "__init__.py").write_text("", encoding="utf-8")
    if shutil.which("pytest") is None or mypy is None:
        avisos.append("pytest ou mypy ausente: o conferir.py NÃO foi conferido")
        return
    passou = rodar([sys.executable, "conferir.py"], pasta)
    conferir(passou.returncode == 0, f"projeto bom: conferir.py passa nas quatro etapas {passou.stdout[-300:] if passou.returncode else ''}")
    shutil.copy(PROVAS / "python" / "ruim.py", pasta / "app" / "ruim.py")
    falhou = rodar([sys.executable, "conferir.py"], pasta)
    conferir(falhou.returncode != 0 and "FALHOU em: Formatação" in falhou.stdout, "projeto com o exemplo ruim: conferir.py para na primeira etapa")


# --------------------------------------------------------------------------- JavaScript
def pasta_do_modulo(executavel: str, nome: str) -> Path | None:
    """Acha a pasta node_modules/<nome> a partir do executável instalado."""
    for pai in Path(executavel).resolve().parents:
        if pai.name == nome and pai.parent.name == "node_modules":
            return pai
    return None


def provar_js(base: Path) -> None:
    print("\n[5] Regras de JavaScript (ESLint com eslint.regras.mjs e Prettier com prettierrc.json)")
    eslint, prettier = ferramenta("eslint"), ferramenta("prettier")
    if eslint is None or prettier is None:
        return
    configuracao = ["-c", str(PROVAS / "eslint.config.mjs")]

    def regras_apontadas(arquivo: str) -> set[str]:
        saida = rodar([eslint, *configuracao, "-f", "json", arquivo], RAIZ)
        try:
            relatorio = json.loads(saida.stdout)
        except json.JSONDecodeError:
            conferir(False, f"ESLint rodou em {arquivo}: {saida.stderr.strip()[:300]}")
            return set()
        return {mensagem["ruleId"] or "erro-de-análise" for item in relatorio for mensagem in item["messages"]}

    conferir(not regras_apontadas("provas/js/bom.js"), "exemplo bom sem apontamento")
    hook_modelo = "templates/claude/hooks/conferir-edicao.mjs"
    apontadas_no_hook = regras_apontadas(hook_modelo)
    conferir(not apontadas_no_hook, f"hook do kit sem apontamento {sorted(apontadas_no_hook) if apontadas_no_hook else ''}")
    apontadas = regras_apontadas("provas/js/ruim.js")
    for regra, significado in ESPERADO_JS.items():
        conferir(regra in apontadas, f"{regra} pega: {significado}")

    formato = ["--config", str(MODELOS / "prettierrc.json"), "--check"]
    conferir(rodar([prettier, *formato, "provas/js/bom.js", hook_modelo, "templates/eslint.regras.mjs"], RAIZ).returncode == 0, "exemplo bom e arquivos do kit já formatados")
    conferir(rodar([prettier, *formato, "provas/js/ruim.js"], RAIZ).returncode != 0, "formatador recusa a indentação do exemplo ruim")

    print("\n[6] Hook de edição para Node (conferir-edicao.mjs)")
    node = shutil.which("node")
    modulo_eslint, modulo_prettier = pasta_do_modulo(eslint, "eslint"), pasta_do_modulo(prettier, "prettier")
    if node is None or modulo_eslint is None or modulo_prettier is None:
        avisos.append("node, ou a pasta do eslint ou do prettier, não foi encontrado: o hook de Node NÃO foi conferido")
        return
    pasta = base / "projeto-node"
    (pasta / "node_modules").mkdir(parents=True)
    (pasta / ".claude" / "hooks").mkdir(parents=True)
    (pasta / "src").mkdir()
    (pasta / "node_modules" / "eslint").symlink_to(modulo_eslint, target_is_directory=True)
    (pasta / "node_modules" / "prettier").symlink_to(modulo_prettier, target_is_directory=True)
    shutil.copy(MODELOS / "claude" / "hooks" / "conferir-edicao.mjs", pasta / ".claude" / "hooks" / "conferir-edicao.mjs")
    shutil.copy(MODELOS / "eslint.regras.mjs", pasta / "eslint.regras.mjs")
    shutil.copy(MODELOS / "prettierrc.json", pasta / ".prettierrc.json")
    (pasta / "eslint.config.mjs").write_text(
        'import { regrasDoKit } from "./eslint.regras.mjs";\n\n'
        'export default [{ files: ["**/*.js"], languageOptions: { ecmaVersion: "latest", sourceType: "module" }, rules: regrasDoKit }];\n',
        encoding="utf-8",
    )
    (pasta / "package.json").write_text('{ "type": "module" }\n', encoding="utf-8")
    shutil.copy(PROVAS / "js" / "ruim.js", pasta / "src" / "ruim.js")
    shutil.copy(PROVAS / "js" / "bom.js", pasta / "src" / "bom.js")
    hook = [node, str(pasta / ".claude" / "hooks" / "conferir-edicao.mjs")]

    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "src" / "ruim.js")}})
    resultado = rodar(hook, pasta, entrada)
    conferir(resultado.returncode == SAIDA_DE_PROBLEMA_DO_HOOK, f"arquivo ruim: o hook sai com 2 e devolve os problemas {resultado.stderr[:200] if resultado.returncode != SAIDA_DE_PROBLEMA_DO_HOOK else ''}")
    conferir("eqeqeq" in resultado.stderr, "arquivo ruim: a mensagem cita a regra (eqeqeq)")
    conferir(rodar([prettier, "--check", "src/ruim.js"], pasta).returncode == 0, "arquivo ruim: o hook corrigiu a indentação")
    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "src" / "bom.js")}})
    conferir(rodar(hook, pasta, entrada).returncode == 0, "arquivo bom: o hook sai com 0")
    entrada = json.dumps({"cwd": str(pasta), "tool_input": {"file_path": str(pasta / "notas.txt")}})
    conferir(rodar(hook, pasta, entrada).returncode == 0, "arquivo de outro tipo: o hook não faz nada")
    conferir(rodar(hook, pasta, "isto não é JSON").returncode == 0, "entrada inválida: o hook não trava o trabalho")


# --------------------------------------------------------------------------- segurança
def provar_padroes_de_seguranca() -> None:
    print("\n[7] Padrões de segurança (templates/claude/security-patterns.json)")
    dados = json.loads((MODELOS / "claude" / "security-patterns.json").read_text(encoding="utf-8"))
    for padrao in dados["patterns"]:
        if "regex" not in padrao:
            continue
        expressao = re.compile(padrao["regex"])
        deve_pegar, nao_deve_pegar = CASOS_DE_SEGURANCA[padrao["rule_name"]]
        conferir(all(expressao.search(texto) for texto in deve_pegar), f"{padrao['rule_name']} pega os {len(deve_pegar)} casos ruins")
        conferir(not any(expressao.search(texto) for texto in nao_deve_pegar), f"{padrao['rule_name']} deixa passar os {len(nao_deve_pegar)} casos bons")


def main() -> int:
    provar_estrutura()
    with tempfile.TemporaryDirectory(prefix="provas-kit-") as temporaria:
        base = Path(temporaria)
        provar_python(base)
        provar_js(base)
    provar_padroes_de_seguranca()
    print()
    for aviso in avisos:
        print(f"AVISO: {aviso}")
    if falhas:
        print(f"\n{len(falhas)} prova(s) FALHARAM:")
        for falha in falhas:
            print(f"  - {falha}")
        return 1
    print("Todas as provas passaram." if not avisos else "As provas que rodaram passaram; veja os avisos acima.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
