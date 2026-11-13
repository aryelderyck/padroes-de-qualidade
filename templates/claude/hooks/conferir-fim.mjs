// Hook do Claude Code para projeto Node (evento Stop): a trava do "pronto".
// Quando o Claude vai encerrar a resposta, confere com o Prettier e o ESLint os arquivos alterados
// ou novos (inclusive os criados por comando, que escapam do hook de edição). Com problema, sai
// com 2: o Claude lê a mensagem e continua até corrigir. Só trava uma vez por tentativa de parar
// (campo stop_hook_active), para não prender o Claude num laço. Copie para .claude/hooks/.

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import process from "node:process";

const SAIDA_COM_PROBLEMA = 2;
const ENTRADA_PADRAO = 0;
const FORMATAVEIS = new Set([
  ".js",
  ".jsx",
  ".ts",
  ".tsx",
  ".mjs",
  ".cjs",
  ".css",
  ".html",
  ".json",
  ".md",
  ".yml",
  ".yaml",
]);
const CODIGO = new Set([".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"]);
const LISTAGENS_DO_GIT = [
  ["ls-files", "--modified", "--others", "--exclude-standard"],
  ["diff", "--name-only", "--cached"],
];

function lerEntrada() {
  try {
    return JSON.parse(readFileSync(ENTRADA_PADRAO, "utf8")) ?? {};
  } catch {
    return {};
  }
}

function arquivosAlterados(raiz) {
  const nomes = new Set();
  for (const argumentos of LISTAGENS_DO_GIT) {
    const saida = spawnSync("git", argumentos, { cwd: raiz, encoding: "utf8" });
    for (const nome of (saida.stdout ?? "").split("\n")) {
      if (nome && existsSync(path.join(raiz, nome))) {
        nomes.add(nome);
      }
    }
  }
  return [...nomes].sort();
}

// Roda a ferramenta instalada no projeto com o próprio Node, sem depender de shell.
function rodar(raiz, binario, argumentos) {
  const caminhoDoBinario = path.join(raiz, "node_modules", binario);
  if (!existsSync(caminhoDoBinario) || argumentos.length === 0) {
    return "";
  }
  const saida = spawnSync(process.execPath, [caminhoDoBinario, ...argumentos], {
    cwd: raiz,
    encoding: "utf8",
  });
  return saida.status === 0 ? "" : `${saida.stdout}${saida.stderr}`.trim();
}

function main() {
  const dados = lerEntrada();
  if (dados.stop_hook_active) {
    return 0;
  }
  const raiz = process.env.CLAUDE_PROJECT_DIR || dados.cwd || process.cwd();
  const arquivos = arquivosAlterados(raiz);
  const formataveis = arquivos.filter((nome) => FORMATAVEIS.has(path.extname(nome)));
  const codigo = arquivos.filter((nome) => CODIGO.has(path.extname(nome)));
  const problemas = [
    rodar(raiz, "prettier/bin/prettier.cjs", formataveis.length ? ["--check", ...formataveis] : []),
    rodar(raiz, "eslint/bin/eslint.js", codigo.length ? ["--max-warnings", "0", ...codigo] : []),
  ].filter(Boolean);
  if (problemas.length === 0) {
    return 0;
  }
  process.stderr.write(
    "Antes de encerrar, corrija os arquivos alterados e rode `npm run conferir`:\n",
  );
  process.stderr.write(`${problemas.join("\n")}\n`);
  return SAIDA_COM_PROBLEMA;
}

process.exit(main());
