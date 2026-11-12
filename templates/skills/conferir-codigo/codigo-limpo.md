# Código Limpo: o que o kit adota

Base: *Clean Code*, de Robert C. Martin (2008). O livro é um conjunto de recomendações de um autor, não um resultado
científico, e algumas são discutidas (funções muito curtas, por exemplo). Por isso o kit separa o que a ferramenta mede
do que pede julgamento, e põe uma regra acima de todas: **o código mais simples que passa nos testes e que a pessoa
consegue explicar**.

## 1. O que a ferramenta já mede (não repita no relatório)

| Regra | Limite do kit | Quem confere |
| --- | --- | --- |
| Formatação e indentação | A do formatador | `ruff format`, Prettier |
| Complexidade de uma função | Até 10 caminhos | `C901`, `complexity` |
| Parâmetros | Até 5 (Python) ou 4 (JavaScript) | `PLR0913`, `max-params` |
| Aninhamento | Até 3 níveis | `max-depth` em JavaScript; em Python a regra ainda é experimental, então quem confere é o revisor |
| Tamanho da função | Até 40 instruções (Python) ou 50 linhas (JavaScript) | `PLR0915`, `max-lines-per-function` |
| Número mágico | Nenhum fora de constante com nome | `PLR2004`, `no-magic-numbers` |
| Código comentado, variável ou parâmetro sem uso | Nenhum | `ERA001`, `F841`, `ARG`, `no-unused-vars` |
| Nome no padrão da linguagem | `snake_case` ou `camelCase` | `N`, `camelcase` |
| Exceção engolida | Nenhuma | `BLE`, `E722`, `S110` |

Exceção a um limite se justifica **na linha**, com o motivo (`# noqa: PLR0913 motivo` ou
`// eslint-disable-next-line max-params -- motivo`). Desligar a regra no projeto inteiro pede a aprovação da pessoa.

## 2. O que pede julgamento (confira isto)

**Nomes**
- O nome diz a intenção sem precisar de comentário: `dias_ate_vencer`, não `d` nem `dias`.
- Palavra inteira, sem abreviação inventada. Nome curto só em escopo de poucas linhas (`i` num laço).
- Um conceito, uma palavra: não misturar `buscar`, `obter` e `pegar` para a mesma coisa.
- Função é verbo (`calcular_total`); booleano é pergunta (`esta_ativo`, `tem_itens`).

**Funções**
- Faz uma coisa só. Sinal de que faz duas: o nome precisa de "e", ou há blocos separados por comentário.
- Um nível de abstração por função: não misturar regra de negócio com detalhe de banco ou de HTTP.
- Sem parâmetro booleano que troca o comportamento: são duas funções.
- Sem efeito escondido: função chamada `validar` não grava nada.
- Retorno antecipado no lugar de `if` dentro de `if`.

**Comentários**
- Comentário explica o **porquê** (decisão, limite externo, armadilha). O **quê** quem diz é o código.
- Comentário que repete a linha de baixo sai. Comentário desatualizado é pior que nenhum.

**Duplicação e abstração**
- Repetiu duas vezes: tolere. Repetiu três: extraia. Abstração criada "para o futuro" sai.
- Código que parece igual mas muda por motivos diferentes não é duplicação: mantenha separado.

**Erros**
- Erro tratado onde dá para fazer algo a respeito; nos outros lugares, deixa subir.
- A mensagem de erro diz o que aconteceu e com qual valor, sem dado sensível.

**Testes**
- O nome do teste é uma frase sobre o comportamento. Cada teste confere uma coisa, em três passos: preparar, agir, conferir.
- Teste não repete a lógica da implementação para calcular o resultado esperado.
