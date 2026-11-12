// Configuração usada só pelas provas do kit: aplica as regras de templates/eslint.regras.mjs.
import { regrasDoKit } from "../templates/eslint.regras.mjs";

export default [
  {
    files: ["**/*.js", "**/*.mjs"],
    languageOptions: { ecmaVersion: "latest", sourceType: "module" },
    rules: regrasDoKit,
  },
];
