# Práticas candidatas

Caixa de entrada de **boas práticas novas**. Aqui nada é obrigatório. Uma prática só vai para o `PADROES.md` depois
de ser testada em um projeto de verdade e de provar que vale o custo.

> **Para Claude e Claude Code:** sempre que você conhecer, ou a pessoa sugerir, uma prática que poderia elevar a
> qualidade, **acrescente-a aqui** como `Candidata`, com o motivo. Quando um projeto estiver prestes a começar,
> releia esta lista e proponha à pessoa quais testar. Não aumente a carga obrigatória sem ela concordar.

## Ciclo de vida

`Candidata` → `Em teste` (em qual projeto) → `Adotada` (vai para o `PADROES.md` e o link fica aqui) ou `Descartada` (com o porquê).

Uma prática é adotada quando: foi usada em pelo menos um projeto inteiro, o custo de manter foi pequeno, e algo concreto
melhorou (erro evitado, tempo poupado, clareza). Descartar também é aprendizado: nunca apague, registre o motivo.

## Lista

| Prática | Por que pode valer | Quando testar | Status |
| --- | --- | --- | --- |
| Ganchos de pre-commit (`pre-commit` com ruff e testes rápidos) | Pega erro de formatação e lint antes do commit, e cria o hábito | Painel de Dota 2 | Candidata |
| Checagem de tipos (`mypy` ou `pyright`) | Evita uma classe inteira de erros em Python; ajuda a entender o código | Painel, depois que os modelos estiverem prontos | Candidata |
| Registro curto de decisões (ADR) | Explica o porquê de cada escolha meses depois e treina a argumentação | Painel | Candidata |
| Testes baseados em propriedades (`hypothesis`) | Encontra casos de borda que a pessoa não imaginou, principalmente em validação | Painel (validações) | Candidata |
| Testes de contrato para API externa | Fixture gravada para os testes diários e uma checagem ocasional contra a API real avisam quando ela mudar | Painel (OpenDota) | Candidata |
| Mutação automatizada (`mutmut` no Python, Stryker no JavaScript) | Automatiza o "quebrar de propósito" que hoje fazemos à mão | Depois do painel | Candidata |
| Commits convencionais com changelog automático | Histórico legível e versões geradas sem esforço | E-commerce | Candidata |
| Fixar actions do GitHub por hash do commit | Reduz risco de cadeia de suprimentos nos workflows | E-commerce ou AtendeFlow | Candidata |
| Orçamento de desempenho no Lighthouse CI | Impede que a página fique mais lenta sem ninguém notar | Landing, na etapa 1 | Candidata (já configurada na landing, ainda não executada) |
| Log estruturado com id de requisição | Rastrear um pedido de ponta a ponta | Painel | Candidata (planejada para o painel) |
| Endereço público em um só lugar (`SITE_URL`) com teste que o confere | Evita o quebra-cabeça do E-021 quando conta ou domínio mudam | Painel | Candidata |
| Lighthouse CI com SEO, Acessibilidade e Desempenho a partir de 95 | Impede regressão de busca e velocidade sem ninguém notar | Painel (páginas públicas) | Candidata |
| Teste automatizado de `hreflang` recíproco, canônica e links internos | Erros de idioma e link quebrado são silenciosos e prejudicam a busca | Painel | Candidata |
| Medir Core Web Vitals em campo depois de publicar | O laboratório (Lighthouse) não vê o que o jogador real vê | Painel, depois do deploy | Candidata |
| Feature flags simples | Liga e desliga recursos novos sem novo deploy | AtendeFlow | Candidata |
| Revisão por um segundo agente, independente | Quem revisa não é quem escreveu; útil em trabalho de alto risco | Qualquer etapa crítica (segurança, pagamentos) | Candidata |
| Cada arquivo com o seu porquê: explicar antes de criar (para que serve, pasta, nome, alternativas) e manter `docs/MAPA-DE-ARQUIVOS.md`, atualizado no mesmo commit do arquivo; temporários ganham uma linha | A pessoa entende a estrutura do projeto, e arquivo sem motivo não nasce; vira pergunta do `/fechar-tarefa` | Painel de Dota 2 (desde o plano 1) e o próprio kit | Em teste (painel) |
| Estilo de saída Professor (`templates/output-styles/professor.md`) no lugar das regras de ensino repetidas em cada `CLAUDE.md` | Um só lugar, liga e desliga com um comando e não pesa em sessão só de execução | Explorador de campeões | Em teste (ainda não executado no Claude Code) |
| Auditar os arquivos de instrução com `/doctor prompt-audit` do Claude Code ao fim de cada projeto | Acha instrução desatualizada, contraditória ou que aponta para arquivo que não existe | Fim do plano 1 do painel | Candidata |
| Plugin `claude-md-management` da Anthropic (skill `claude-md-improver`) para avaliar o `CLAUDE.md` | Dá nota por comandos, arquitetura, concisão e atualidade, e propõe mudanças como diff | Explorador de campeões | Candidata |
| Conferir o `docs/MAPA-DE-ARQUIVOS.md` contra `git ls-files` por script (no CI ou em hook) | O que tem de valer sempre não deve depender de o Claude lembrar; a documentação recomenda hook nesses casos | Painel, tarefa 2 | Candidata |
| Empacotar o kit como plugin do Claude Code (skills para as perguntas de revisão e para fechar tarefa, estilo de saída, hooks) | Cada parte carrega só quando serve e a instalação vira um comando | Depois do explorador | Candidata |
| Plugin `security-guidance` da Anthropic com a orientação e os padrões de `templates/claude/` | Revisão de segurança feita por outro contexto, e não por quem escreveu; a conferência de padrões a cada edição não gasta uso | Painel, a partir da tarefa 2 | Em teste (arquivos validados, plugin ainda não executado) |
| `/security-review` na branch antes de dizer "pronto" (nível 2 em diante) | Segunda opinião sobre injeção, autenticação, autorização e tratamento de dados | Painel, fim do plano 1 | Em teste (já está na checklist do nível 2) |
| Teste que percorre as rotas do OpenAPI sem credencial e espera 401 ou 403 fora da lista de rotas públicas | Rota nova esquecida sem proteção é pega pelo CI, sem depender de alguém lembrar | Painel, quando houver a segunda rota | Candidata |
| Varredura de segredos antes do commit (`gitleaks` em gancho de pre-commit) | Pega a chave antes de ela chegar ao histórico; o *push protection* do GitHub só age no envio | Painel | Candidata |

## Como acrescentar

Nova linha no fim da tabela: prática, por que pode valer, quando testar, status. Para mudar o status, edite a linha
e registre no `CHANGELOG.md`. Prática adotada: copie para o `PADROES.md`, na seção certa, e troque o status para
`Adotada (PADROES.md, seção N)`.
