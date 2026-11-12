// Regras do kit para JavaScript e TypeScript (PADROES.md, seção 4A).
// Só usa regras do próprio ESLint, sem plugin. TODAS têm prova em provas/ no kit: as provas
// falham se uma regra daqui não tiver um exemplo ruim que ela pega.
// Copie para a raiz do projeto, ao lado do eslint.config.mjs.

const LIMITE_DE_LINHAS = { skipBlankLines: true, skipComments: true };

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
  "no-promise-executor-return": "error",
  "no-unused-vars": "error",
  "no-shadow": "error",
  "no-param-reassign": "error",
  "no-implicit-coercion": "error",
  "consistent-return": "error",
  "no-throw-literal": "error",
  "prefer-promise-reject-errors": "error",
  "no-template-curly-in-string": "error",
  "no-await-in-loop": "error",

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
  "max-lines-per-function": ["error", { max: 50, ...LIMITE_DE_LINHAS }],
  // 404, 3000 e afins viram constante com nome; os valores abaixo são claros sozinhos.
  "no-magic-numbers": [
    "error",
    {
      ignore: [-1, 0, 1, 2, 10, 100],
      ignoreArrayIndexes: true,
      ignoreDefaultValues: true,
      enforceConst: true,
    },
  ],
  // Campo de API em snake_case é renomeado na chegada: const { account_id: idDaConta } = dados
  camelcase: ["error", { properties: "never" }],
  "no-var": "error",
  "prefer-const": "error",
  "no-else-return": "error",
  "no-lonely-if": "error",
  "no-nested-ternary": "error",
  "no-unneeded-ternary": "error",
  "no-useless-return": "error",
  curly: ["error", "all"],
  // Aviso também reprova: o comando de conferência roda o ESLint com --max-warnings 0.
  "no-console": "warn",
};

// Componente de tela (JSX) carrega a marcação junto, então o limite de linhas é maior.
export const regrasParaComponentes = {
  "max-lines-per-function": ["error", { max: 120, ...LIMITE_DE_LINHAS }],
};
