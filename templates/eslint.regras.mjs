// Regras do kit para JavaScript e TypeScript (PADROES.md, seção 4A).
// Só usa regras do próprio ESLint, sem plugin. TODAS têm prova em provas/ no kit: as provas
// falham se uma regra daqui não tiver um exemplo ruim que ela pega.
// Copie para a raiz do projeto, ao lado do eslint.config.mjs.

// Modo do kit neste projeto: "essencial" ou "completo". Para mudar de modo, troque só esta linha.
// Essencial: erros de lógica e de segurança, que quase não acusam código correto.
// Completo: soma os limites de tamanho, o número mágico e as regras de estilo.
export const MODO = "completo";

const LIMITE_DE_LINHAS = { skipBlankLines: true, skipComments: true };

export const regrasEssenciais = {
  // Erros de lógica e armadilhas
  eqeqeq: ["error", "always"],
  "no-self-compare": "error",
  "no-unreachable": "error",
  "no-constant-condition": "error",
  "no-unmodified-loop-condition": "error",
  "use-isnan": "error",
  "valid-typeof": "error",
  "no-fallthrough": "error",
  "array-callback-return": "error",
  "no-loop-func": "error",
  "no-promise-executor-return": "error",
  "no-unused-vars": "error",
  "no-throw-literal": "error",
  "prefer-promise-reject-errors": "error",
  "no-template-curly-in-string": "error",
  "no-var": "error",
  "prefer-const": "error",

  // Segurança
  "no-eval": "error",
  "no-implied-eval": "error",
  "no-new-func": "error",
  "no-script-url": "error",
};

export const regrasDeRigor = {
  // Armadilhas que também acusam código correto com alguma frequência
  "default-case": "error",
  radix: "error",
  "no-shadow": "error",
  "no-param-reassign": "error",
  "no-implicit-coercion": "error",
  "consistent-return": "error",
  "no-await-in-loop": "error",

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
  "no-else-return": "error",
  "no-lonely-if": "error",
  "no-nested-ternary": "error",
  "no-unneeded-ternary": "error",
  "no-useless-return": "error",
  curly: ["error", "all"],
  // Aviso também reprova: o comando de conferência roda o ESLint com --max-warnings 0.
  "no-console": "warn",
};

// Todas as regras do kit (modo completo). As provas conferem cada uma.
export const regrasDoKit = { ...regrasEssenciais, ...regrasDeRigor };

// As regras que valem neste projeto, conforme o modo escolhido na primeira linha.
export const regrasDoModo = MODO === "completo" ? regrasDoKit : regrasEssenciais;

// Componente de tela (JSX) carrega a marcação junto, então o limite de linhas é maior.
export const regrasParaComponentes =
  MODO === "completo"
    ? { "max-lines-per-function": ["error", { max: 120, ...LIMITE_DE_LINHAS }] }
    : {};
