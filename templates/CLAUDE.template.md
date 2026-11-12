# CLAUDE.md: [NOME DO PROJETO]

<!-- Copie este arquivo para a raiz do repositório novo, preencha os [colchetes] e apague os comentários. -->

## Padrões obrigatórios
Este projeto segue o kit **padroes-de-qualidade**, versão **[0.5]**, nível **[1, 2 ou 3]**, ritmo **[rápido ou completo]**.
O kit fica clonado ao lado deste repositório, em `../padroes-de-qualidade`. Se não estiver, peça à pessoa para clonar
(`https://github.com/aryelderyck/padroes-de-qualidade`) ou leia pelo link "raw"
(`https://raw.githubusercontent.com/aryelderyck/padroes-de-qualidade/main/<arquivo>`).
- **Toda sessão:** leia só o `REGRAS.md` do kit. Ele é curto e diz o que mais abrir, e em que momento.
- **Não leia o kit inteiro.** `PADROES.md`, `CONTEXTO.md`, `REVISAO.md` e `ERROS.md` são abertos por seção, quando o
  momento pedir (tabela do `REGRAS.md`).
- Antes de decidir algo importante, de otimizar ou de dizer "pronto", passe pelo bloco correspondente do `REVISAO.md`.
- Erro que pode se repetir, que custou mais de uns 15 minutos ou que chegou à pessoa ou ao repositório: registre no
  `ERROS.md` do kit ao fechar a tarefa (commit `docs(kit): ...` no repositório do kit) e resuma em `APRENDIZADOS.md`.
- Práticas novas que valham a pena ficam em `PRATICAS.md`; dificuldades da pessoa, em `CONTEXTO.md` (seção 7).
- Os critérios de "pronto" estão em `docs/CHECKLIST-PRONTO.md` (cópia do modelo do kit). Em ritmo rápido valem só os
  itens marcados **[E]**. Desvios vão na especificação ou no README, na seção "Desvios", com o motivo.

## Contexto da pessoa
Aryel é desenvolvedor iniciante e usa o projeto para **aprender** e montar portfólio (freelance ou vaga júnior).
Orçamento zero: só ferramentas gratuitas. Explique em português, de forma direta.
Aryel também quer **aprender inglês**: use o termo técnico em inglês com a tradução na primeira vez; diante de mensagem de
erro ou tela em inglês, peça primeiro que ele diga o que entendeu e só depois confirme ou corrija; ao fechar cada tarefa,
registre de 3 a 5 termos novos em `APRENDIZADOS.md`.
**Ensine com recursos visuais:** use diagramas, gráficos, tabelas e maquetes sempre que ajudarem, de preferência algo
que abra no celular; o visual complementa o texto.
**Cada arquivo com o seu porquê:** antes de criar qualquer arquivo (inclusive de configuração), explique em poucas linhas
para que serve, por que fica naquela pasta e com aquele nome, quais alternativas existiam e por que não foram escolhidas.
Mantenha `docs/MAPA-DE-ARQUIVOS.md` com uma linha por arquivo do repositório
(`arquivo | para que serve | por que está aqui | alternativas | tarefa em que foi criado`), atualizado no mesmo commit que
cria, move ou apaga o arquivo. Se não conseguir justificar um arquivo, não o crie e avise. Arquivo temporário, fora do
repositório: basta uma linha dizendo para que serve. No fechamento da tarefa, uma das perguntas de explicar de volta pode ser sobre um arquivo criado nela.
Nível atual em [API, banco, testes, Docker...]: [iniciante completo / já usou / confortável].

## O que é este projeto
[Uma ou duas frases: o que faz, para quem, e se os dados/nomes são fictícios.]

## Regras que não podem ser quebradas
- Dados reais nunca entram no repositório. Só dados fictícios.
- Segredos nunca no código: variáveis de ambiente e `.env.example` sem valores.
- Nada de "funciona" sem rodar o comando e ler a saída. O que não foi verificado é dito.
- [Regras específicas do projeto: stack, proibições, restrições de LGPD.]

## Comandos
- Instalar: `[comando]`
- Rodar: `[comando]`
- Testes: `[comando]`
- Lint e formatação: `[comando]`

## Como trabalhar
- Mudou comportamento? Escreva ou ajuste o teste antes (TDD) e veja falhar pelo motivo certo.
- Ao fim de cada etapa: atualize `APRENDIZADOS.md` com a pessoa, rode a checklist do nível e commite.
- Teste que passa de primeira: quebre o código de propósito para confirmar que o teste falha.
- Commits pequenos, em português, `tipo: o que mudou`. Branch curta e Pull Request com CI verde.

## Plano de aprendizado
Método: Claude mostra, depois fazem juntos com lacunas, depois a pessoa escreve e Claude revisa.
Arquivos que a pessoa deve escrever (Claude **não** entrega a solução, guia por perguntas):
1. [arquivo ou módulo]
2. [arquivo ou módulo]
