# Contexto geral

Contexto que Claude e Claude Code precisam ter em mente em **qualquer** projeto do Aryel. Documento vivo:
atualize sempre que algo mudar.

> **Este repositório é público.** Aqui entram só informações de trabalho e aprendizado. **Nunca** coloque dados
> pessoais sensíveis (saúde, finanças, documentos, endereço, contatos), segredos, nem planos de carreira confidenciais
> (como nomes de empresas em processo seletivo). Dúvida? Deixe de fora.

> **Leitura:** seções 1 a 5 e 7 no começo de cada projeto. As seções 6 (glossário) e 8 (decisões) são de consulta.

## 1. Quem e para quê

- **Pessoa:** Aryel, desenvolvedor iniciante, no Brasil. Idioma de tudo: português do Brasil.
- **Objetivo:** montar um portfólio para trabalhar como **freelancer** ou conseguir uma vaga **júnior**.
- **Prioridade nº 1: aprender.** Terminar rápido é secundário. Um projeto concluído que a pessoa não consegue explicar não cumpre o objetivo.
- **Restrições:** orçamento zero (só ferramentas gratuitas), dados reais nunca em repositório público, segurança e LGPD desde o início.
- **Nível técnico atual:** iniciante completo em API, endpoints e mapeamento de tabelas; já fez páginas em HTML/CSS/JS e trabalhos em C.

## 2. Como ensinar

As instruções de ensino, na forma que o Claude Code executa, ficam em **um só lugar**: o estilo de saída
[`templates/output-styles/professor.md`](templates/output-styles/professor.md), instalado uma vez por máquina e ligado
ou desligado com um comando (`README.md`, "Estilo de saída Professor"). Aqui fica o porquê de cada princípio; as fontes
estão em [`docs/REFERENCIAS.md`](docs/REFERENCIAS.md).

| Princípio | Por quê |
| --- | --- |
| Liberação gradual: Claude mostra, depois fazem juntos com lacunas, depois a pessoa escreve e Claude revisa | Passar do exemplo resolvido para o problema aos poucos funciona melhor do que pular direto (Renkl e Atkinson, 2003) |
| Detalhe na primeira vez, referência depois: cada decisão, sintaxe e linha explicadas quando aparecem; depois, só o que é novo | Orientação detalhada ajuda quem está começando e atrapalha quem já sabe (Kalyuga e outros, 2003); pedido da pessoa (2026-11-12) |
| Dica em vez de resposta nas tarefas que a pessoa escreve | IA sem salvaguardas pode prejudicar o aprendizado; salvaguardas que fazem raciocinar o protegem (Bastani e outros, 2025) |
| Conferir pelo que a pessoa faz (explicar de volta, prever, escrever sem olhar), não pelo "entendi" | Lembrar ativamente fixa mais do que reler (Roediger e Karpicke, 2006); iniciantes com IA tendem a achar que sabem mais do que sabem (Prather e outros, 2024) |
| Claude escreve o repetitivo; a pessoa escreve a lógica | Gerar código com IA não piorou o desempenho de iniciantes sem IA, e quem sabia mais aproveitou mais (Kazemitabaar e outros, 2023) |
| Explicar cada arquivo antes de criar (para que serve, pasta, nome, alternativas) e manter o `docs/MAPA-DE-ARQUIVOS.md` | Pedido da pessoa (2026-11-10); em teste no painel (`PRATICAS.md`) |
| Termos em inglês com tradução; a pessoa tenta ler o erro antes da explicação | Pedido da pessoa (2026-11-10): aprender inglês junto com o código |
| Diagramas e outros recursos visuais, de preferência algo que abra no celular | Pedido da pessoa (2026-11-10) |
| Cada etapa termina com algo visível funcionando e com um teste | Motivação e prova de que funciona |

A pessoa prefere não gastar tempo escrevendo CSS de variáveis (cores e tamanhos); o foco de escrita dela é a lógica
(JavaScript, TypeScript, Python), os testes e a API.

## 3. Mapa dos projetos

Aqui fica só o estado geral, que muda pouco. O andamento de cada projeto está no repositório dele (`README.md` e
`docs/PASSAGEM.md`), para esta tabela não ficar desatualizada.

| Projeto | Nível e ritmo | Stack | O que pesa mais | Estado |
| --- | --- | --- | --- | --- |
| Landing page (escritório fictício) | 1, completo | HTML, CSS, JavaScript, Playwright, GitHub Actions | Front-end, acessibilidade, LGPD sem terceiros, CI e Pages | Publicada (v1) |
| Painel de estatísticas de Dota 2 (projeto principal) | 2, completo | Python, FastAPI, Jinja2, PostgreSQL, pytest | API externa e limites, testes sem rede, busca (SEO) e idiomas, direito de apagar dados | Em andamento |
| Explorador de campeões de League of Legends | 1, rápido | React, TypeScript, Vite, Vitest | React e TypeScript, dados públicos sem chave, testes sem rede, acessibilidade | A iniciar (nome do repositório a confirmar pela pessoa) |
| E-commerce | 3, completo | TypeScript, NestJS, React | Contas, carrinho, pagamento fictício, autorização, testes de segurança | Não iniciado |
| AtendeFlow (CRM, agenda, orçamentos multiempresa, pt/en) | 3, completo | A definir | Multiempresa (isolamento entre clientes), permissões, LGPD completa | Não iniciado |

Repositórios antigos já organizados e com README; não são prioridade.

## 4. Decisões técnicas que valem para todos os projetos

- Fluxo de trabalho: ideia, especificação, plano, implementação (skills *superpowers*), com aprovação da pessoa a cada etapa.
- Stack e arquitetura de cada projeto ficam na especificação dele, não aqui.
- Recursos de terceiros no navegador: nenhum por padrão. Exceção só com o motivo escrito na especificação (por exemplo,
  imagens oficiais de um jogo carregadas em tempo de execução).
- CI com GitHub Actions; publicação gratuita no GitHub Pages quando for site estático.

## 5. Ambiente de trabalho

- **Claude no chat/nuvem:** bom para planejar, escrever documentos e arquivos; a rede é limitada (muitas vezes sem npm, pip ou acesso a sites de documentação), então não consegue rodar tudo.
- **Claude Code na máquina da pessoa** (extensão do VS Code): onde o código roda de verdade, com internet. É o lugar certo para instalar dependências, rodar testes e a pessoa escrever código. O login é pela conta do Claude, não pelo Console da API (E-037).
- O kit fica clonado ao lado de cada projeto (`../padroes-de-qualidade`), para ser lido sem depender de rede.
- A pessoa cria os repositórios vazios no GitHub; Claude consegue enviar arquivos para repositórios que ela autorizou.

## 6. Glossário vivo

Definições curtas, **para a pessoa consultar**. Claude abre esta seção só para não definir de outro jeito um termo que
já foi ensinado. Acrescente termos novos ao longo dos projetos.

| Termo | O que é, em uma frase |
| --- | --- |
| API | Combinação de endereços e regras pela qual um programa pede dados ou ações a outro |
| Endpoint | Um endereço específico da API que faz uma coisa (ex.: `GET /jogadores/123`) |
| HTTP | Protocolo da web: o cliente faz uma requisição, o servidor devolve uma resposta |
| Método HTTP | O tipo de pedido: `GET` lê, `POST` cria, `PUT/PATCH` altera, `DELETE` apaga |
| Código de status | Número na resposta que resume o resultado (200 ok, 404 não achou, 422 dado inválido, 500 erro do servidor) |
| JSON | Formato de texto para trocar dados, com chaves e valores |
| Tabela, linha, coluna | Uma "planilha" do banco: cada linha é um registro; cada coluna, um campo |
| Chave primária | Coluna que identifica cada linha de forma única |
| Chave estrangeira | Coluna que aponta para a chave primária de outra tabela e cria a relação |
| SQL | Linguagem para consultar e alterar um banco de dados |
| ORM (SQLAlchemy) | Camada que traduz tabelas em objetos do código, para não escrever SQL à mão em tudo |
| Migração | Arquivo versionado que descreve uma mudança na estrutura do banco |
| Validação | Conferir se o dado recebido tem o formato e os limites esperados antes de usar |
| Teste unitário | Verifica uma peça pequena do código, isolada |
| Teste de integração | Verifica peças trabalhando juntas (ex.: API com banco) |
| Teste E2E | Usa o sistema como o usuário usaria, de ponta a ponta |
| TDD | Escrever o teste antes do código e vê-lo falhar antes de fazê-lo passar |
| Fixture / mock | Dado ou objeto falso para testar sem depender de rede ou banco real |
| Cobertura | Porcentagem do código executada pelos testes (sinal, não garantia) |
| CI | Rodar verificações automáticas a cada alteração enviada ao repositório |
| CD | Publicar automaticamente quando as verificações passam |
| Pipeline | A sequência de etapas do CI/CD |
| Lockfile | Arquivo que fixa as versões exatas das dependências para o build ser reproduzível |
| Variável de ambiente | Valor de configuração (como uma chave) fora do código |
| Limite de requisições (rate limit) | Máximo de chamadas que uma API aceita em um período |
| Cache | Guardar um resultado para não buscá-lo de novo |
| Hash de senha | Transformação irreversível da senha (argon2, bcrypt) para nunca guardá-la em texto |
| CSP | Política que diz ao navegador de onde a página pode carregar recursos |
| LGPD | Lei brasileira de proteção de dados pessoais |
| Contêiner (Docker) | Pacote com o programa e o que ele precisa para rodar igual em qualquer máquina |

## 7. Dificuldades conhecidas

Registro de pontos em que a pessoa (ou o processo) enfrenta dificuldade, com o que ajuda. Quando uma dificuldade
for superada, mude o status em vez de apagar. Dificuldades de ferramenta e de ambiente ficam no `ERROS.md`.

| Dificuldade | Sinal | O que ajuda | Status |
| --- | --- | --- | --- |
| API, endpoints, tabelas e mapeamento (pessoa declara saber "quase nada") | Conceitos novos juntos em um mesmo projeto | Consumir uma API antes de criar a sua; exemplo mínimo antes de cada conceito; glossário; prever o resultado antes de rodar | Em andamento |
| Projeto novo sem tema que motive | Recusa repetida das ideias propostas | Perguntar o que a pessoa usa e admira antes de sugerir (E-015) | Resolvido |

Modelo de nova linha: `| situação | como percebi | o que ajudou ou vai tentar | Aberto / Em andamento / Resolvido |`

## 8. Registro de decisões

Só decisões que valem para **vários projetos**. Decisão de um projeto só fica na especificação dele (as do painel
estão em `painel-dota/docs/superpowers/specs/`; foram tiradas daqui em 2026-11-12 e continuam no histórico do git).
Acrescente no topo, com data.

- **2026-11-12:** kit na versão 0.6: o jeito de ensinar passa a morar no estilo de saída Professor, um só lugar para todos os projetos (seção 2); as regras foram reescritas como gatilho e ação; as fontes ficam em `docs/REFERENCIAS.md`.
- **2026-11-12:** kit na versão 0.5, a pedido da pessoa (regras o mais eficientes possível): o `REGRAS.md` é a única leitura de toda sessão e o resto é aberto por seção; o nível é decidido pelo que o projeto hospeda; projetos de até uma semana podem usar o ritmo rápido (`PADROES.md`, seção 2); erro só é registrado se pode se repetir, custou mais de uns 15 minutos ou chegou à pessoa; `REVISAO-CRITICA.md` fica obsoleto.
- **2026-11-12:** novo projeto de portfólio, curto e em paralelo ao painel: explorador de campeões de League of Legends em React e TypeScript, com o catálogo público da Riot (Data Dragon, sem chave). Nível 1, ritmo rápido. Motivo: o portfólio ainda não mostra React nem TypeScript. O painel continua sendo o projeto principal.
- **2026-11-12:** ao ensinar, detalhe na primeira vez e referência depois: cada decisão, lógica, sintaxe e linha explicadas quando aparecem pela primeira vez, com alternativas nas decisões de arquitetura.
- **2026-11-10:** ao ensinar, usar diagramas e outros recursos visuais sempre que ajudarem.
- **2026-11-10:** todo arquivo novo é explicado antes de ser criado e ganha uma linha no `docs/MAPA-DE-ARQUIVOS.md` do repositório; arquivo sem justificativa não é criado.
- **2026-11-10:** aprender inglês passa a ser objetivo de todos os projetos.
- **2026-11-10:** produto público pode mostrar **dados reais em execução**; o repositório, os testes e os exemplos continuam só com dados fictícios (E-024).
- **2026-11-10:** a conta do GitHub passou a se chamar `aryelderyck`; endereços e links foram atualizados (E-021, E-022).
- **2026-11-09:** projeto 2 passa a ser o painel de estatísticas de Dota 2, no lugar do radar de licitações. Motivo: a pessoa não se animou com o tema; busca algo ligado a jogos.
- **2026-11-09:** criado o kit `padroes-de-qualidade` para manter a qualidade entre os projetos.

## 9. Como evoluir

- Atualize a seção 3 só quando um projeto mudar de estado geral (iniciado, publicado), a seção 6 a cada termo novo, a seção 7 a cada dificuldade e a seção 8 a cada decisão.
- Antes de gravar algo sobre a pessoa, confirme que é adequado a um repositório público.
- Registre a mudança no `CHANGELOG.md`.
