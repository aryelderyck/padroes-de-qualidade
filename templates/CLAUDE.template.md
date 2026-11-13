# CLAUDE.md: [NOME DO PROJETO]

<!-- Copie para a raiz do repositório novo, preencha os [colchetes] e apague os comentários.
     Este arquivo é carregado em toda sessão: mantenha abaixo de 100 linhas. Para cada linha, pergunte
     "se eu tirar, o Claude erra?". Se não erra, tire. Instrução boa é concreta o bastante para conferir. -->

## O projeto

[Uma ou duas frases: o que faz e para quem.] Stack: [linguagem e versão, framework e versão, ferramenta de teste].
Dados e nomes no repositório são **fictícios**. [Se o produto mostra dado real em execução, diga de onde ele vem.]

## Comandos

- Instalar: `[comando]`
- Rodar: `[comando]`
- Testes: `[comando]` · um teste só: `[comando]`
- Conferência completa (formatação, linter, tipos e testes): `[python conferir.py ou npm run conferir]`

## Estrutura

- `[pasta]/`: [o que mora aqui]
- `docs/MAPA-DE-ARQUIVOS.md`: uma linha por arquivo (`arquivo | para que serve | por que está aqui | alternativas | tarefa`),
  atualizada no mesmo commit que cria, move ou apaga o arquivo. Arquivo que não dá para justificar não é criado.

## Limites

**Sempre**

- Teste antes do código (TDD): ver o teste falhar pelo motivo certo, depois implementar.
- Rodar o comando e ler a saída antes de dizer que funciona; listar o que não foi verificado.
- Conferência completa antes de cada commit; `/conferir-codigo` antes de dizer que a tarefa está pronta.
- Commits pequenos, em português, no formato `tipo: o que mudou`.

**Pergunte antes**

- Acrescentar dependência (confira antes se o pacote existe no registro oficial), mudar a estrutura de pastas, apagar
  arquivo ou mexer no CI.
- Criar rota pública, mudar CORS, autenticação ou permissões.
- Escrever um arquivo da lista "A pessoa escreve".

**Nunca**

- Dado real, segredo, token ou e-mail em arquivo, commit ou conversa. Segredo fica em `.env`, fora do git, e nunca em
  código que vai para o navegador.
- Dado de fora (API de terceiros, usuário, modelo de IA) inserido na página como HTML cru.
- SQL montado com texto, ou regra do linter desligada no projeto para o código passar (exceção é na linha, com o motivo).
- [Proibições do projeto: recurso de terceiros no navegador, teste que acessa a internet...]

## A pessoa e o jeito de ensinar

Aryel é desenvolvedor iniciante e usa o projeto para **aprender** e montar portfólio. Orçamento zero. Português do Brasil.
O jeito de ensinar está no estilo de saída **Professor** (`../padroes-de-qualidade/templates/output-styles/professor.md`).
Se a sessão não estiver nesse estilo, avise a pessoa uma vez e siga as instruções daquele arquivo.

**A pessoa escreve** (não entregue a solução; dê uma dica por vez, quando ela pedir):

1. [arquivo ou módulo]
2. [arquivo ou módulo]

## Kit de padrões

Kit **padroes-de-qualidade** [0.9], nível **[1, 2 ou 3]**, ritmo **[rápido ou completo]**, clonado em `../padroes-de-qualidade`
(se faltar, peça à pessoa para clonar `https://github.com/aryelderyck/padroes-de-qualidade`).

- O kit é opcional: vale quando a pessoa pedir. Nesse caso, leia só o `REGRAS.md` do kit. Ele diz o que mais abrir, e quando. Não leia o kit inteiro.
- "Pronto" é o `docs/CHECKLIST-PRONTO.md` (em ritmo rápido, só os itens **[E]**). Desvio vai na seção "Desvios" da
  especificação ou do README, com o motivo.
- Erro que pode se repetir, que custou mais de uns 15 minutos ou que chegou à pessoa: `ERROS.md` do kit, ao fechar a
  tarefa (commit `docs(kit): ...` no repositório do kit, depois de ler as regras de commit de lá).
