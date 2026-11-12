# Armadilhas comuns de modelagem e de algoritmos

Lista de conferência para a skill `conferir-codigo`. Em cada linha: a armadilha, por que quebra e como pegar. "Linter"
quer dizer que a regra do kit já aponta; nos outros casos, quem pega é o revisor ou um teste.

## 1. Modelagem de dados

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Dinheiro em ponto flutuante | `0.1 + 0.2` não dá `0.3`; centavos somem ou aparecem | Guardar em centavos (inteiro) ou decimal; teste com `0.1 + 0.2` |
| Data e hora sem fuso | O mesmo instante vira horas diferentes no servidor e no cliente | Guardar em UTC com fuso; linter (`DTZ`) |
| Regra só no código, sem restrição no banco | Um segundo caminho de escrita grava dado inválido | `NOT NULL`, `UNIQUE`, chave estrangeira e `CHECK` na migração |
| Estado em texto livre | `"ativo"`, `"Ativo"` e `"ativa"` viram três estados | Enumeração no código e `CHECK` ou tipo enumerado no banco |
| Dado derivado guardado junto com a origem | Os dois saem de sincronia (total diferente da soma dos itens) | Calcular na leitura, ou atualizar na mesma transação com teste |
| Lista dentro de uma coluna de texto | Não dá para buscar, validar nem relacionar | Tabela filha com chave estrangeira |
| Identificador sequencial exposto | Quem vê o `41` tenta o `42`; revela o volume | Conferir a posse no servidor; UUID quando o número não deve ser adivinhado |
| Tudo opcional por omissão | Cada leitura precisa tratar ausência que nunca deveria existir | Campo obrigatório até prova em contrário |
| Apagar de verdade o que precisa de histórico, ou "apagado lógico" esquecido nas consultas | Perde o rastro, ou o item apagado reaparece numa listagem | Decisão escrita; teste de que a listagem não traz apagados |
| Migração que apaga ou renomeia coluna em uso | A versão antiga do código quebra durante a publicação | Migrar em passos: criar, copiar, trocar a leitura, remover depois |

## 2. Números, texto e datas

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Comparar ponto flutuante com `==` | Erro de arredondamento torna falso o que parece igual | Comparar com tolerância ou usar inteiro |
| Divisão ou média de lista vazia | Erro em tempo de execução ou `NaN` silencioso | Teste com a lista vazia |
| `0`, `""` e lista vazia tratados como "ausente" | `if valor:` descarta um zero legítimo | Comparar com `None` ou `undefined` de forma explícita |
| Arredondar antes de somar | O erro acumula a cada parcela | Somar primeiro, arredondar uma vez no fim |
| Comparar texto sem normalizar | Maiúsculas, acentos e espaços fazem iguais parecerem diferentes | Normalizar na entrada; teste com acento e espaço nas pontas |
| Contar caracteres por bytes | Acentos e emojis ocupam mais de um byte | Medir em caracteres; teste com acento |
| Intervalo de datas com fim inclusivo | O último dia entra duas vezes ou fica de fora | Convenção de fim exclusivo; teste na virada do dia e do mês |

## 3. Coleções, laços e limites

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Erro de um a mais ou a menos | `<` no lugar de `<=`, índice final, página final | Teste com 0, 1, o limite exato e o limite mais um |
| Alterar a coleção enquanto percorre | Pula elementos ou estoura erro | Percorrer uma cópia ou montar uma nova |
| Cópia rasa tratada como cópia completa | Alterar o "novo" altera o original | Teste que altera a cópia e confere o original |
| Paginação sem ordem estável | Itens repetem ou somem entre as páginas | `ORDER BY` com desempate por chave única |
| Consulta sem teto | Uma tabela grande derruba a memória | Limite máximo sempre; teste com mais itens que o teto |
| Função de laço que captura a variável do laço | Todas as funções enxergam o último valor | Linter (`B023`, `no-loop-func`) |

## 4. Custo

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Uma consulta por item (N+1) | 100 itens viram 101 idas ao banco | Contar as consultas no teste; buscar em lote ou com junção |
| Procurar em lista dentro de laço | Custo quadrático: 10 mil itens viram 100 milhões de comparações | Trocar a lista por conjunto ou dicionário |
| Ordenar ou recalcular a cada volta | Trabalho repetido que não muda | Tirar para fora do laço |
| Filtro em coluna sem índice | Cada busca lê a tabela inteira | Índice nas colunas de filtro e de junção; ver o plano da consulta |
| Otimizar sem medir | Código mais difícil sem ganho real | Medir antes e depois; sem medição, fica a versão simples |
| Cache sem validade ou com chave incompleta | Devolve dado velho, ou o dado de outro usuário | Validade definida; a chave inclui tudo o que muda a resposta |

## 5. Concorrência e repetição

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Conferir e depois agir | Entre o "existe?" e o "cria", outro pedido passa | Restrição única no banco e tratar o conflito; operação atômica |
| Tentar de novo uma operação que não é idempotente | A repetição cobra ou cria duas vezes | Chave de idempotência; teste que envia o mesmo pedido duas vezes |
| Ler, calcular e gravar sem trava | Duas atualizações simultâneas, uma se perde | Atualização atômica (`SET x = x + 1`) ou controle de versão |
| Esquecer de esperar uma operação assíncrona | O código segue antes do resultado; o erro some | Linter (`no-floating-promises`, `require-atomic-updates`); tipos |

## 6. Erros e fluxo

| Armadilha | Por que quebra | Como pegar |
| --- | --- | --- |
| Exceção engolida | A falha vira dado errado mais adiante | Linter (`BLE`, `S110`, `E722`); tratar ou deixar subir |
| Devolver `None` ou `-1` para indicar erro | Quem chama esquece de conferir | Lançar exceção ou devolver um tipo que obriga o tratamento |
| Condição composta negada errado | `not (a and b)` não é `not a and not b` | Teste com as quatro combinações |
| `else` que cobre "todo o resto" | Um caso novo cai no ramo errado em silêncio | Tratar cada caso e falhar no desconhecido |
| Ramo que nunca é testado | Só o caminho feliz roda; o erro estreia em produção | Um teste por ramo; olhar o que a cobertura não alcança |

## 7. Próprias de cada linguagem

| Linguagem | Armadilha | Como pegar |
| --- | --- | --- |
| Python | Valor padrão mutável (`def f(x=[])`): a mesma lista é reusada entre chamadas | Linter (`B006`, `RUF012`) |
| Python | `is` no lugar de `==` para comparar valores | Linter (`F632`); revisão |
| Python | Variável do laço reaproveitada ou sobrescrita dentro dele | Linter (`PLW2901`) |
| JavaScript | `==` com conversão implícita (`0 == ""` é verdadeiro) | Linter (`eqeqeq`) |
| JavaScript | `sort()` sem função ordena números como texto (`10` antes de `2`) | Revisão; teste com 2 e 10 |
| JavaScript | `parseInt` sem a base; `map` ou `filter` sem `return` | Linter (`radix`, `array-callback-return`) |
| JavaScript | `sort`, `reverse` e `splice` alteram o array original | Revisão; usar `toSorted`, `toReversed`, `toSpliced` |
| TypeScript | `any` e `as` escondem o erro que o tipo mostraria | Linter (`no-explicit-any`); `strict` e `noUncheckedIndexedAccess` |
