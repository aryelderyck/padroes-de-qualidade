// Regras do kit para JavaScript e TypeScript (PADROES.md, seção 4A).
// Só usa regras do próprio ESLint, sem plugin. Cada uma tem prova em provas/ no kit.
// Copie para a raiz do projeto, ao lado do eslint.config.mjs.

export const regrasDoKit = {
  // Erros de lógica e armadilhas
  eqeqeq: ["error", "always"],
  "no-self-compare": "error",
  "no-unreachable": "error",
  "no-constant-condition": "error",
  "no-unmodified-loop-condition": "error",
  "use-isnan": "error",
  "valid-typeof": "error",
  "no-fallthrough": "error",
  "default-case": "error",
  "array-callback-return": "error",
  "no-loop-func": "error",
  radix: "error",
  "require-atomic-updates": "error",
  "no-promise-executor-return": "error",
  "no-unused-vars": "error",
  "no-shadow": "error",
  "no-param-reassign": "error",
  "no-implicit-coercion": "error",

  // Segurança
  "no-eval": "error",
  "no-implied-eval": "error",
  "no-new-func": "error",
  "no-script-url": "error",

  // Código Limpo com limite medido
  complexity: ["error", 10],
  "max-depth": ["error", 3],
  "max-params": ["error", 4],
  "max-nested-callbacks": ["error", 3],
  "max-lines-per-function": ["error", { max: 50, skipBlankLines: true, skipComments: true }],
  "no-magic-numbers": [
    "error",
    {
      ignore: [-1, 0, 1, 2],
      ignoreArrayIndexes: true,
      ignoreDefaultValues: true,
      enforceConst: true,
    },
  ],
  camelcase: "error",
  "no-var": "error",
  "prefer-const": "error",
  "no-else-return": "error",
  "no-lonely-if": "error",
  "no-nested-ternary": "error",
  "no-unneeded-ternary": "error",
  "no-useless-return": "error",
  curly: ["error", "all"],
  "no-console": "warn",
};
