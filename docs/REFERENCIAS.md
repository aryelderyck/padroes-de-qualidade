# Referências do kit

De onde vieram as regras de escrita e de ensino do kit. Arquivo **de consulta**: nenhuma sessão precisa lê-lo. Regra
nova baseada em fonte externa entra aqui com a fonte e com o que ela sustenta. Levantamento de 2026-11-12.

## 1. Documentação oficial do Claude Code (lida na íntegra nos trechos citados)

| Fonte | O que sustenta no kit |
| --- | --- |
| [Como o Claude lembra do projeto](https://code.claude.com/docs/en/memory.md), seção "Write effective instructions" | `CLAUDE.md` abaixo de 200 linhas; instrução concreta o bastante para conferir; instruções que se contradizem são escolhidas ao acaso; importar arquivos não reduz o custo de contexto; `/doctor prompt-audit` |
| [Boas práticas](https://code.claude.com/docs/en/best-practices.md), "Write an effective CLAUDE.md" | O teste de cada linha ("se eu tirar, o Claude erra?"); o que incluir e o que deixar de fora; arquivo longo demais faz as regras se perderem; o que só serve às vezes vai para skill; o que tem de acontecer sempre vai para hook |
| [Estilos de saída](https://code.claude.com/docs/en/output-styles) | O jeito de responder mora num estilo de saída, não no `CLAUDE.md`; estilos prontos Explanatory e Learning; formato do estilo próprio (`templates/output-styles/professor.md`) |

## 2. Exemplos e ferramentas com a mesma função

| Fonte | O que foi aproveitado |
| --- | --- |
| [GitHub Blog: lições de mais de 2.500 arquivos `agents.md`](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) | Comandos no começo; stack com versões; limites em três níveis (sempre, pergunte antes, nunca); "comece simples e acrescente quando o agente errar" |
| [Plugin `learning-output-style` da Anthropic](https://github.com/anthropics/claude-code/blob/main/plugins/learning-output-style/README.md) | A pessoa escreve trechos de 5 a 10 linhas nos pontos de decisão; o que é repetitivo ou configuração fica com o Claude |
| [Plugin `claude-md-management` da Anthropic](https://claude.com/plugins/claude-md-management) (skill `claude-md-improver`) | Critérios para avaliar um `CLAUDE.md`: comandos, arquitetura, padrões não óbvios, concisão, atualidade e acionabilidade |

## 3. Artigos revisados por pares

Título, autores e local de publicação conferidos na busca. Resumo lido: Liu, Levy, Prather e Kazemitabaar. De Bastani
foi lida só a página de divulgação da universidade dos autores, não o artigo. Os três clássicos de psicologia da
aprendizagem (Renkl, Kalyuga, Roediger) estão resumidos de memória.

| Artigo | Onde saiu | O que sustenta no kit |
| --- | --- | --- |
| Liu e outros, [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/) | *TACL*, v. 12, 2024 | Modelos usam pior a informação que fica no meio de um contexto longo: leitura curta por sessão, o importante no começo |
| Levy, Jacoby e Goldberg, [Same Task, More Tokens](https://aclanthology.org/2024.acl-long.818) | ACL 2024 | O raciocínio piora com entradas maiores, bem antes do limite técnico: não ler o kit inteiro |
| Bastani e outros, [Generative AI without guardrails can harm learning](https://www.pnas.org/doi/10.1073/pnas.2422633122) | *PNAS*, 2025 | IA sem salvaguardas pode prejudicar o aprendizado; salvaguardas que fazem a pessoa raciocinar o protegem: dica em vez de resposta |
| Prather e outros, [The Widening Gap](https://arxiv.org/abs/2405.17739) | ICER 2024 | Iniciantes em dificuldade saíram com ilusão de competência ao usar IA: conferir pelo que a pessoa faz, não pelo "entendi" |
| Kazemitabaar e outros, [Studying the effect of AI Code Generators on Supporting Novice Learners](https://arxiv.org/abs/2302.07427v1) | CHI 2023 | Com 69 iniciantes de 10 a 17 anos, gerar código com IA não piorou o desempenho posterior sem IA, e quem sabia mais aproveitou mais: Claude pode escrever o repetitivo |
| Renkl e Atkinson, [Structuring the Transition From Example Study to Problem Solving](https://asu.elsevierpure.com/en/publications/structuring-the-transition-from-example-study-to-problem-solving--2) | *Educational Psychologist*, 2003 | Passar do exemplo resolvido para o problema aos poucos: mostrar, completar lacunas, escrever sozinho |
| Kalyuga, Ayres, Chandler e Sweller, [The Expertise Reversal Effect](https://ro.uow.edu.au/edupapers/136) | *Educational Psychologist*, 2003 | Orientação detalhada ajuda o iniciante e atrapalha quem já sabe: detalhe na primeira vez, referência depois |
| Roediger e Karpicke, [Test-Enhanced Learning](https://pubmed.ncbi.nlm.nih.gov/16507066/) | *Psychological Science*, 2006 | Lembrar ativamente fixa mais do que reler: explicar de volta e prever o resultado |

**Limites.** Os dois estudos de contexto longo testaram modelos mais antigos que os atuais; a direção combina com a
documentação oficial, mas o tamanho do efeito hoje não foi medido. Os estudos de ensino são com estudantes, não com
adultos aprendendo com um assistente de programação.

## 4. Lidos, mas fora da conta (não são revisados por pares, ou não foi possível confirmar)

- Gloaguen e outros, [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) (preprint, 2026): arquivos de contexto tenderam a reduzir a taxa de sucesso dos agentes e aumentaram o custo em mais de 20%; os autores recomendam só requisitos mínimos. Aponta na mesma direção do kit 0.5, mas é preprint.
- Chatlatanagulchai e outros, [Agent READMEs](https://arxiv.org/abs/2511.12884) (2.303 arquivos de contexto): crescem por pequenos acréscimos, ficam difíceis de ler e quase não tratam de segurança (14,8%) e desempenho (14,5%). Tem DOI da ACM, mas a página não abriu para confirmar onde saiu.
