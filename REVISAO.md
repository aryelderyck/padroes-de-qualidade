# Perguntas de revisão

Perguntas que Claude (e a pessoa) fazem **antes de decidir, enquanto escreve e antes de entregar**. O objetivo é
sair do "funciona" para o "é a melhor forma, é a mais simples, é segura e dá para manter".

> **Para Claude e Claude Code:** passe pelo bloco do momento em que está. Leva um minuto. Responda a você mesmo com
> honestidade; "não sei" vira tarefa de pesquisa, nunca suposição. Quando uma resposta **mudar** a decisão, mostre à
> pessoa em poucas linhas (formato no fim). Perguntas marcadas *(à pessoa)* são feitas a ela, para o aprendizado.

## Como usar

- **Não é burocracia.** Cada bloco cabe em um minuto. Se uma pergunta não faz sentido no caso, pule e siga.
- **Proporcional ao nível do projeto** (`PADROES.md`, seção 2): nível 1 usa os blocos A, B, F; níveis 2 e 3 usam todos.
- **Recomende, não só liste.** Ao apresentar alternativas, diga qual escolheria e por quê.
- **Esta lista cresce.** Se uma pergunta evitou um erro ou revelou algo, ela ganhou o lugar. Veja "Como evoluir".

## A. Antes de desenhar (entender e escolher)

1. Qual é o problema real, para quem, e como vamos saber que deu certo?
2. **Já existe pronto?** Recurso do framework, biblioteca bem mantida, serviço gratuito. Por que não usar?
3. **Qual a versão mais simples que ainda resolve?** O que dá para deixar para depois sem custo? (YAGNI)
4. **Essa é a melhor maneira de fazer isso?** Para *este* projeto, *este* nível da pessoa e *este* orçamento. Quais 2 ou 3 alternativas e por que esta?
5. **Quão caro é voltar atrás?** Reversível (decida rápido). Irreversível (pense mais): modelo de dados, API pública, licença, nome de rota.
6. **Pré-morte:** daqui a três meses isso deu errado. Por quê?
7. **Que suposição estou fazendo sem ter verificado?** Limites, preços, termos de uso e regras oficiais foram lidos?
8. Continua gratuito se o uso crescer? Qual é o limite do plano gratuito?
9. *(à pessoa)* Você consegue explicar essa escolha para um colega? Se não, vamos voltar um passo.

## B. Enquanto escreve (código)

1. **Dá para ter o mesmo resultado com um código menor e mais enxuto?** O que posso apagar sem perder comportamento?
2. A função faz **uma coisa só**? O nome diz o que ela faz, sem precisar ler o corpo?
3. Isso é duplicação **real** (terceira vez) ou só parecida? Não abstraia cedo: três repetições antes de extrair.
4. A biblioteca padrão ou a ferramenta que já usamos faz isso?
5. Estou resolvendo um problema que **ainda não existe**? Se sim, remova.
6. Tratei entrada vazia, `null`, enorme, com acento, negativa, duplicada? E falha de rede ou de banco?
7. Validei na borda (entrada do usuário, resposta de API externa)?
8. O código é legível sem comentário? O comentário explica o **porquê**, não o que o código já diz?
9. Entendo cada linha que escrevi? A pessoa entenderia lendo?

**Sinais de que está complicado demais:** aninhamento acima de 3 níveis, função com mais de ~40 linhas, mais de 4 parâmetros,
nomes genéricos (`utils`, `helper`, `data`), parâmetros booleanos que mudam o comportamento, copiar e colar com pequenas diferenças.

## C. Antes de otimizar ou refatorar

1. **Medi?** Onde está o gargalo real (tempo da requisição, `EXPLAIN` da consulta, perfil de execução)? Otimizar sem medir é adivinhar.
2. **O ganho vale a perda de clareza?** Só otimize quando o ganho importa para quem usa ou para o custo.
3. **Os testes protegem o comportamento atual?** Se não, escreva primeiro testes que descrevam o que o código faz hoje.
4. **Dá para otimizar sem quebrar nada?** Faça **uma mudança por vez**, rode os testes depois de cada uma, e dê commit separado (`refactor:` ou `perf:`).
5. Se não tenho certeza de que o comportamento fica igual: comparo a saída **antes e depois** com os mesmos dados.
6. Medi **depois**? Teve ganho real? Se não, desfaça: código mais complexo sem ganho é prejuízo.
7. Ordem de prioridade: **faça funcionar, faça certo, faça rápido**, nessa ordem.

**Suspeitos comuns de lentidão:** consulta N+1, falta de índice, listagem sem paginação, carregar tudo em memória,
chamadas repetidas à mesma API (falta cache), laços aninhados, imagens e fontes pesadas, JavaScript bloqueando a página.

## D. Segurança e dados (a cada rota, campo ou dado novo)

1. O que alguém mal-intencionado enviaria aqui? (texto enorme, SQL, HTML, caminho de arquivo, número negativo)
2. **O usuário A consegue ler ou alterar o dado do usuário B?** Existe teste que prova que não?
3. Esse dado é pessoal? Preciso mesmo guardá-lo? Por quanto tempo? Entra no log?
4. Há segredo em lugar errado (código, log, mensagem de erro, imagem Docker)?
5. A dependência nova é necessária, mantida e sem vulnerabilidade conhecida?
6. A mensagem de erro entrega informação demais?

## E. Testes

1. **Este teste falharia se o código estivesse errado?** (Quebre o código de propósito para ver.)
2. Testa o **comportamento** ou um detalhe de implementação que vai mudar?
3. Cobre erro e casos de borda, e não só o caminho feliz?
4. Depende de rede, de hora, de ordem ou de dados do ambiente?
5. Lendo o teste, dá para entender o que o sistema deve fazer?

## F. Antes de dizer "pronto"

1. **Rodei e li a saída?** Ou estou presumindo que funciona?
2. **O que não verifiquei?** Está dito, com clareza, para a pessoa?
3. Atende ao que foi pedido? Releia o pedido, palavra por palavra.
4. Funciona numa máquina limpa, seguindo só o README?
5. O plano e a especificação continuam iguais ao código? Divergência foi para "Desvios"?
6. Erros e aprendizados da etapa foram registrados (`ERROS.md`, `APRENDIZADOS.md`)?
7. **A pessoa consegue explicar e manter isso?** Se não, a etapa não terminou.

## G. Aprendizado *(à pessoa)*

1. Explique com as suas palavras o que esse trecho faz.
2. Antes de rodar: o que você acha que vai acontecer se mudarmos X? (Prever e depois conferir ensina mais do que ler.)
3. Que alternativa você teria escolhido, e por quê?
4. O que você ainda não entendeu? (Qualquer resposta serve; ela vira tarefa nas "Dificuldades" do `CONTEXTO.md`.)
5. Você escreveria isso do zero amanhã, sem olhar?

## H. Comunicação (ao responder à pessoa)

1. Estou afirmando um **fato verificado** ou uma suposição? Deixei claro qual é qual?
2. É a menor explicação que a pessoa precisa para decidir? Cabe na tela?
3. Reconheci o erro com causa e correção, sem rodeios?
4. Dei uma **recomendação** com motivo, e não só uma lista de opções?
5. Existe algo que a pessoa precisa saber e eu estou deixando de dizer?

## I. Operação e manutenção

1. Como eu saberia que isso quebrou em produção? Existe log, rota de saúde, alerta?
2. Como voltamos atrás (reverter o deploy, desfazer a migração)?
3. O que o próximo desenvolvedor precisa saber para mexer aqui sem medo?

## Formato curto para mostrar à pessoa

Use quando uma pergunta mudou ou confirmou uma decisão importante:

```text
Decisão: [o que vamos fazer]
Alternativas consideradas: [A, B] e por que ficou fora
Por que esta: [motivo em uma frase]
Simplicidade: [o que deixei de fora de propósito]
Risco / não verificado: [o que pode falhar ou ainda não foi conferido]
```

## Como evoluir

- Quando uma pergunta evitar um erro ou revelar algo útil, **acrescente-a** no bloco certo (ou crie um bloco novo) com a data entre parênteses.
- Se uma pergunta nunca ajudou depois de vários projetos, marque como `(revisar)` em vez de apagar, e decida com a pessoa.
- Perguntas nascidas de um erro citam o `ERROS.md` (ex.: *"... (E-009)"*).
- Registre a mudança no `CHANGELOG.md`.
