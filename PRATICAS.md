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

## Como acrescentar

Nova linha no fim da tabela: prática, por que pode valer, quando testar, status. Para mudar o status, edite a linha
e registre no `CHANGELOG.md`. Prática adotada: copie para o `PADROES.md`, na seção certa, e troque o status para
`Adotada (PADROES.md, seção N)`.
