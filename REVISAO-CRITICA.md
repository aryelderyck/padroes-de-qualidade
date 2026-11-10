# Revisão crítica

Perguntas para **questionar o próprio trabalho** antes, durante e depois de escrever código. O objetivo é descobrir
se existe um jeito melhor, menor, mais simples ou mais rápido, **sem quebrar nada**.

> **Para Claude e Claude Code:**
> 1. Leia este arquivo no início de cada projeto e aplique a "Revisão relâmpago" (seção 2) ao fim de **cada etapa**,
>    sem esperar a pessoa pedir.
> 2. Quando a pessoa fizer uma dessas perguntas, **não responda só "sim"**. Compare alternativas, mostre a evidência
>    (teste, medição, trecho de código) e diga quando o código atual já é a melhor opção, e por quê (seção 8).
> 3. Registre em [`ERROS.md`](ERROS.md) o que a revisão revelar de errado.

## 1. As perguntas que a pessoa pode fazer a qualquer momento

Copie e cole. Cada uma já pede uma resposta com argumento, não com elogio.

| Pergunta | O que ela força |
| --- | --- |
| **"Essa é a melhor maneira de fazer isso?"** | Comparar com pelo menos 2 alternativas, com prós, contras e a recomendação. |
| **"Daria para ter o mesmo resultado com um código menor e mais enxuto?"** | Procurar duplicação, código morto, função da biblioteca padrão e simplificações, mostrando o antes e o depois. |
| **"Dá para otimizar mais isso sem quebrar nada?"** | Medir primeiro, achar o gargalo real e propor mudanças pequenas protegidas por testes. |
| **"O que acontece se isso falhar?"** | Mapear erros, tempo limite, dados ruins e o que o usuário vê. |
| **"O que acontece se isso crescer 10 vezes?"** | Olhar consultas, memória, paginação, limites de API e custo. |
| **"Um iniciante entenderia isso em 5 minutos?"** | Nomes, comentários, tamanho das funções e quantidade de "mágica". |
| **"Isso é seguro? Como um atacante abusaria?"** | Entrada não confiável, autorização, vazamento e abuso. |
| **"Preciso mesmo dessa biblioteca / dessa camada / desse arquivo?"** | Remover o que não se paga (YAGNI). |
| **"O que você faria diferente se começasse do zero?"** | Enxergar decisões que não valeram a pena e registrá-las. |
| **"Como eu provo que isso funciona?"** | Teste, comando e saída, e não afirmação. |
| **"Explique isso como se eu fosse iniciante."** | Garantir que a pessoa aprendeu, não só recebeu código. |

## 2. Revisão relâmpago (ao fim de cada etapa)

Responda por escrito, em poucas linhas cada, antes de dar a etapa por concluída:

1. **Melhor jeito?** Existe uma forma mais simples ou mais comum de resolver? Qual alternativa descartei e por quê?
2. **Menos código?** O que dá para apagar, juntar ou substituir por algo que já existe, sem perder clareza?
3. **Otimizar sem quebrar?** Há um gargalo medido? Se não há, não otimize agora.
4. **Pode falhar como?** Entrada vazia, enorme, estranha; rede fora; banco vazio; usuário malicioso.
5. **Está provado?** Os testes falham se eu quebrar o código de propósito?
6. **Dá para explicar?** A pessoa consegue explicar o que foi feito com as próprias palavras?
7. **O que aprendi / errei?** Entrou em `APRENDIZADOS.md` e, se foi erro, em `ERROS.md`?

## 3. Antes de escrever (desenho)

- Estou resolvendo o problema certo? Qual é o resultado que a pessoa precisa ver funcionando?
- Já existe solução pronta (biblioteca padrão, framework, serviço gratuito) que cobre 90%? Reinventar só se o objetivo for aprender.
- Qual é a forma **mais simples** que atende ao requisito de hoje? (Complexidade futura só entra quando houver necessidade real.)
- Considerei pelo menos duas abordagens? O que cada uma custa em código, tempo, risco e manutenção?
- Quais são as partes difíceis de mudar depois (formato dos dados, contrato da API, modelo do banco)? Essas merecem mais cuidado agora.
- O que acontece se a API externa mudar, ficar fora do ar ou limitar as chamadas?

## 4. Enquanto escreve (código)

- O nome diz **o que é** e **por que existe**? (Se precisa de comentário para entender o nome, troque o nome.)
- Cada função faz uma coisa só e cabe numa tela?
- Estou repetindo lógica em dois lugares? (Três repetições: extraia. Duas: avalie.)
- Esse código é idiomático na linguagem? (Em Python: compreensões, `with`, `pathlib`, `dataclasses`/Pydantic; em JS/TS: `map`/`filter`, `const`, tipos.)
- Há código que "pode ser útil depois"? Apague. O histórico do Git guarda.
- Os comentários explicam o **porquê**, e não repetem o que o código já diz?
- Os erros são tratados no lugar certo, com mensagem útil? Nenhum `except:` vazio, nenhum erro engolido.
- Há número ou texto "mágico" que deveria ser constante nomeada?

## 5. Protocolo de simplificação (código menor, sem quebrar)

Menor só vale se continuar **claro**. Legibilidade vem antes de concisão.

1. Rode os testes: devem estar **verdes antes** de mexer. Se não há teste, escreva um primeiro.
2. Faça **uma** simplificação por vez (remover duplicação, apagar código morto, trocar loop manual por função existente).
3. Rode os testes de novo. Verde: commit pequeno (`refactor: ...`). Vermelho: desfaça e entenda por quê.
4. Compare o antes e o depois: menos linhas **e** igualmente fácil de ler? Se ficou "esperto demais", volte.
5. Não misture refatoração com mudança de comportamento no mesmo commit.

Sinais de que há o que simplificar: função com mais de uns 30 linhas, mais de 3 níveis de `if`/`for` aninhados,
muitos parâmetros, copiar e colar, variáveis `temp`/`data2`, código comentado, classe que só repassa chamadas.

## 6. Protocolo de otimização segura

Regra de ouro: **primeiro correto, depois claro, depois rápido** — e só rápido se medido.

1. **Meça antes.** Qual o tempo ou a quantidade de consultas hoje? Sem número, não há otimização, só palpite.
2. **Ache o gargalo real** (perfilador, log de tempo, plano da consulta). 80% do ganho costuma estar em 1 ou 2 lugares.
3. **Garanta os testes verdes** antes. Eles são a rede de segurança.
4. **Mude uma coisa por vez** e meça de novo. Não ganhou? Desfaça.
5. **Registre** o ganho (de X para Y) no commit ou em `APRENDIZADOS.md`.
6. Não troque clareza por um ganho que ninguém percebe.

Candidatos comuns, do que mais rende para o que menos rende:

| Onde | Sinal | Ideia |
| --- | --- | --- |
| Banco | muitas consultas por requisição (o problema "N+1") | carregar relacionamentos de uma vez (`selectinload`/`joinedload`), consulta única |
| Banco | consulta lenta em coluna filtrada | criar índice; conferir com `EXPLAIN` |
| Banco | listas enormes | paginar, selecionar só as colunas necessárias |
| API externa | mesma chamada repetida | guardar em cache (banco ou memória) com prazo de validade |
| API externa | muitas chamadas pequenas | agrupar (lote), respeitar o limite de requisições |
| Código | trabalho repetido dentro de laço | tirar do laço, guardar o resultado |
| Estrutura de dados | procurar em lista várias vezes | trocar lista por conjunto ou dicionário |
| Front-end | página pesada | comprimir imagens, carregar o necessário, fontes locais |

## 7. Depois de escrever (qualidade e segurança)

- **Testes:** testam o comportamento (não os detalhes internos)? Cobrem erro e borda? Falham se eu quebrar o código?
- **Segurança:** quem pode chamar isso? A entrada é validada? O que vaza numa mensagem de erro ou no log? Qual o pior caso?
- **Dados pessoais:** estou coletando só o necessário? Dá para apagar?
- **Dependências:** a biblioteca é mantida, de licença compatível e sem vulnerabilidades conhecidas? Dá para viver sem ela?
- **Operação:** como saberei que quebrou (log, `/saude`)? Como desfaço (rollback, migração reversível)?
- **Documentação:** o README reflete **o que foi executado**? As limitações estão escritas?

## 8. Como Claude responde a essas perguntas

- **Honestidade acima de agradar.** Se o código está bom, diga "sim, é uma boa escolha, porque...". Se não está, diga e mostre.
- **Alternativas de verdade:** apresente 2 ou 3 opções com prós e contras e **recomende uma**, como na seção de abordagens do desenho.
- **Evidência:** cite teste, medição, número de linhas antes e depois, trecho de código ou documentação oficial. Sem medir, diga "não medi".
- **Sem otimização prematura:** se não há problema medido, explique que o ganho não compensa e deixe a sugestão registrada.
- **Sem quebrar:** toda sugestão de mudança vem com o teste que protege e o comando para rodar.
- **Ensine:** explique o motivo em linguagem de iniciante, e deixe a pessoa tentar escrever a mudança quando for didático.
- **Limites:** diga o que não consegue verificar (por exemplo, desempenho real em produção) em vez de supor.

## 9. Gatilhos automáticos

Aplique a revisão (mesmo sem a pessoa pedir) quando:

- terminar uma etapa ou um módulo;
- um teste passar de primeira (faça a mutação);
- aparecer código copiado ou uma função grande;
- antes de abrir um Pull Request;
- antes de dizer "pronto".
