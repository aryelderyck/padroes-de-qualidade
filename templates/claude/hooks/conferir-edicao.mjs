// Hook do Claude Code para projeto Node (evento PostToolUse, ferramentas Edit e Write).
// Formata com o Prettier o arquivo que o Claude acabou de editar e devolve ao Claude o que o
// ESLint apontar. Sai com 0 quando não há nada a dizer e com 2 quando há problema: nesse caso o
// Claude lê a mensagem e corrige. Copie para .claude/hooks/ do projeto.

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import process from "node:process";

const SAIDA_COM_PROBLEMA = 2;
const SAIDA_DE_ERRO_DO_ESLINT = 1;
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

function conferirComEslint(raiz, arquivo) {
  // Variável ainda sem uso é comum no meio de uma edição; o comando completo confere depois.
  const lint = rodar(raiz, "eslint/bin/eslint.js", ["--rule", "no-unused-vars: off", arquivo]);
  if (lint === null) {
    process.stderr.write("conferir-edicao: ESLint não encontrado; rode npm install.\n");
    return 0;
  }
  if (lint.status === 0) {
    return 0;
  }
  const titulo =
    lint.status === SAIDA_DE_ERRO_DO_ESLINT
      ? "O ESLint apontou problemas neste arquivo. Corrija antes de seguir:"
      : "O ESLint não conseguiu rodar (configuração ou instalação). Corrija antes de seguir:";
  process.stderr.write(`${titulo}\n${(lint.stdout || lint.stderr).trim()}\n`);
  return SAIDA_COM_PROBLEMA;
}

function main() {
  const dados = lerEntrada();
  const arquivo = String(dados.tool_input?.file_path ?? "");
  const extensao = path.extname(arquivo);
  if (!FORMATAVEIS.has(extensao) || !existsSync(arquivo)) {
    return 0;
  }
  const raiz = process.env.CLAUDE_PROJECT_DIR || dados.cwd || process.cwd();
  rodar(raiz, "prettier/bin/prettier.cjs", ["--write", "--log-level", "silent", arquivo]);
  return CODIGO.has(extensao) ? conferirComEslint(raiz, arquivo) : 0;
}

process.exit(main());
