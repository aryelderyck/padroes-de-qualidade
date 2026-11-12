// Configuração do ESLint para projeto TypeScript (com ou sem React).
// Provada no CI do kit (provas/conferir-provas.py, parte com rede), em Linux e em Windows.
// Instalar: npm install -D eslint @eslint/js typescript-eslint typescript globals prettier
// package.json:
//   "conferir": "prettier --check . && eslint . --max-warnings 0 && tsc --noEmit && vitest run"

import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";
import { regrasDoKit, regrasParaComponentes } from "./eslint.regras.mjs";

export default defineConfig(
  globalIgnores(["dist", "build", "coverage"]),
  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      ...regrasDoKit,
      // Em TypeScript, a versão que conhece os tipos substitui a regra básica.
      "no-unused-vars": "off",
      "no-shadow": "off",
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/no-shadow": "error",
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-floating-promises": "error",
      // O switch sem "default" deixa o TypeScript avisar quando surge um caso novo.
      "default-case": "off",
      "@typescript-eslint/switch-exhaustiveness-check": "error",
    },
  },
  { files: ["**/*.{jsx,tsx}"], rules: regrasParaComponentes },
  {
    // Arquivos JavaScript soltos (configuração, hooks) ficam fora do tsconfig: sem regras de tipo.
    files: ["**/*.{js,mjs,cjs}"],
    extends: [tseslint.configs.disableTypeChecked],
  },
  {
    // Números de exemplo e funções longas são normais em testes.
    files: ["**/*.test.*", "**/tests/**"],
    rules: { "no-magic-numbers": "off", "max-lines-per-function": "off" },
  },
);
