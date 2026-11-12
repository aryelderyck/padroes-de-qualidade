// Modelo de configuração do ESLint para projeto TypeScript (com ou sem React).
// ATENÇÃO: a ligação com o typescript-eslint abaixo NÃO foi executada no kit (o pacote não estava
// disponível); as regras de eslint.regras.mjs foram. Valide no primeiro projeto e corrija aqui.
// Instalar: npm install -D eslint @eslint/js typescript-eslint prettier
// package.json: "conferir": "prettier --check . && eslint . && tsc --noEmit && vitest run"

import js from "@eslint/js";
import tseslint from "typescript-eslint";
import { regrasDoKit } from "./eslint.regras.mjs";

export default tseslint.config(
  { ignores: ["dist", "coverage"] },
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      ...regrasDoKit,
      // Em TypeScript, a versão com tipos substitui a regra básica.
      "no-unused-vars": "off",
      "no-shadow": "off",
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/no-shadow": "error",
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/switch-exhaustiveness-check": "error",
    },
  },
  {
    // Números de exemplo e funções longas são normais em testes.
    files: ["**/*.test.*", "**/tests/**"],
    rules: { "no-magic-numbers": "off", "max-lines-per-function": "off" },
  },
);
