// Configuração usada só pelas provas do kit: aplica as regras de templates/eslint.regras.mjs.
import { regrasDoKit, regrasParaComponentes } from "../templates/eslint.regras.mjs";

const linguagem = {
  ecmaVersion: "latest",
  sourceType: "module",
  parserOptions: { ecmaFeatures: { jsx: true } },
};

export default [
  { files: ["**/*.js", "**/*.mjs", "**/*.jsx"], languageOptions: linguagem, rules: regrasDoKit },
  { files: ["**/*.jsx"], rules: regrasParaComponentes },
];
