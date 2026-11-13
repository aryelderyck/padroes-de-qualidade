// Configuração do ESLint para projeto TypeScript (com ou sem React).
// Provada no CI do kit (provas/conferir-provas.py, parte com rede), em Linux e em Windows.
// Instalar: npm install -D eslint @eslint/js typescript-eslint typescript globals prettier
// package.json:
//   "conferir:rapido": "prettier --check . && eslint . --max-warnings 0"
//   "conferir": "npm run conferir:rapido && tsc --noEmit && vitest run"

import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";
import { MODO, regrasDoModo, regrasParaComponentes } from "./eslint.regras.mjs";

// O modo ("essencial" ou "completo") é escolhido na primeira linha do eslint.regras.mjs.
const completo = MODO === "completo";

// No modo completo, as regras do ESLint que têm versão com tipos dão lugar a ela.
const trocasDoRigor = {
  "no-shadow": "off",
  "@typescript-eslint/no-shadow": "error",
  // O switch sem "default" deixa o TypeScript avisar quando surge um caso novo.
  "default-case": "off",
  "@typescript-eslint/switch-exhaustiveness-check": "error",
  // Quem confere os retornos é o compilador: ligue "noImplicitReturns" no tsconfig.json.
  "consistent-return": "off",
};

export default defineConfig(
  globalIgnores(["dist", "build", "coverage"]),
  js.configs.recommended,
  // Essencial: o conjunto recomendado. Completo: o mais estrito, com as regras que leem os tipos.
  completo ? tseslint.configs.strictTypeChecked : tseslint.configs.recommended,
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      ...regrasDoModo,
      // Em TypeScript, a versão que conhece os tipos substitui a regra básica.
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-floating-promises": "error",
      ...(completo ? trocasDoRigor : {}),
    },
  },
  { files: ["**/*.{jsx,tsx}"], rules: regrasParaComponentes },
  {
    // Arquivos JavaScript soltos (configuração, hooks) ficam fora do tsconfig: sem regras de tipo.
    files: ["**/*.{js,mjs,cjs}"],
    extends: [tseslint.configs.disableTypeChecked],
  },
  {
    // Arquivo de configuração é feito de números e listas: os limites ficam declarados nele.
    files: ["**/*.config.*", "eslint.regras.mjs"],
    rules: { "no-magic-numbers": "off" },
  },
  {
    // Números de exemplo e funções longas são normais em testes.
    files: ["**/*.test.*", "**/*.spec.*", "**/tests/**", "**/__tests__/**"],
    rules: { "no-magic-numbers": "off", "max-lines-per-function": "off" },
  },
);
