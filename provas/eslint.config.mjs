// Configuração usada só pelas provas do kit: aplica as regras de templates/eslint.regras.mjs.
import process from "node:process";
import {
  regrasDoKit,
  regrasEssenciais,
  regrasParaComponentes,
} from "../templates/eslint.regras.mjs";

// As provas escolhem o modo pela variável de ambiente; sem ela, vale o completo.
const essencial = process.env.MODO_DAS_PROVAS === "essencial";
const regras = essencial ? regrasEssenciais : regrasDoKit;

const linguagem = {
  ecmaVersion: "latest",
  sourceType: "module",
  parserOptions: { ecmaFeatures: { jsx: true } },
};

export default [
  { files: ["**/*.js", "**/*.mjs", "**/*.jsx"], languageOptions: linguagem, rules: regras },
  { files: ["**/*.jsx"], rules: essencial ? {} : regrasParaComponentes },
];
