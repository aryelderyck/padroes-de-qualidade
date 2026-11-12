// Hook do Claude Code para projeto Node (evento PostToolUse, ferramentas Edit e Write).
// Formata com o Prettier o arquivo que o Claude acabou de editar e devolve ao Claude o que o
// ESLint apontar. Sai com 0 quando não há nada a dizer e com 2 quando há problema: nesse caso o
// Claude lê a mensagem e corrige. Copie para .claude/hooks/ do projeto.

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

function lerEntrada() {
  try {
    return JSON.parse(readFileSync(ENTRADA_PADRAO, "utf8"));
  } catch {
    return {};
  }
}

// Roda a ferramenta instalada no projeto com o próprio Node, sem depender de shell.
function rodar(raiz, binario, argumentos) {
  const caminhoDoBinario = path.join(raiz, "node_modules", binario);
  if (!existsSync(caminhoDoBinario)) {
    return null;
  }
  return spawnSync(process.execPath, [caminhoDoBinario, ...argumentos], {
    cwd: raiz,
    encoding: "utf8",
  });
}

function main() {
  const dados = lerEntrada();
  const arquivo = String(dados.tool_input?.file_path ?? "");
  const extensao = path.extname(arquivo);
  if (!FORMATAVEIS.has(extensao)) {
    return 0;
  }
  const raiz = process.env.CLAUDE_PROJECT_DIR || dados.cwd || process.cwd();
  rodar(raiz, "prettier/bin/prettier.cjs", ["--write", "--log-level", "silent", arquivo]);
  if (!CODIGO.has(extensao)) {
    return 0;
  }
  // Variável ainda sem uso é comum no meio de uma edição; o comando completo confere depois.
  const lint = rodar(raiz, "eslint/bin/eslint.js", ["--rule", "no-unused-vars: off", arquivo]);
  if (lint !== null && lint.status !== 0) {
    process.stderr.write("O ESLint apontou problemas neste arquivo. Corrija antes de seguir:\n");
    process.stderr.write(`${(lint.stdout || lint.stderr).trim()}\n`);
    return SAIDA_COM_PROBLEMA;
  }
  return 0;
}

process.exit(main());
