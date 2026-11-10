# Contexto geral

Contexto que Claude e Claude Code precisam ter em mente em **qualquer** projeto do Aryel. Documento vivo:
atualize sempre que algo mudar.

> **Este repositório é público.** Aqui entram só informações de trabalho e aprendizado. **Nunca** coloque dados
> pessoais sensíveis (saúde, finanças, documentos, endereço, contatos), segredos, nem planos de carreira confidenciais
> (como nomes de empresas em processo seletivo). Dúvida? Deixe de fora.

## 1. Quem e para quê

- **Pessoa:** Aryel, desenvolvedor iniciante, no Brasil. Idioma de tudo: português do Brasil.
- **Objetivo:** montar um portfólio para trabalhar como **freelancer** ou conseguir uma vaga **júnior**.
- **Prioridade nº 1: aprender.** Terminar rápido é secundário. Um projeto concluído que a pessoa não consegue explicar não cumpre o objetivo.
- **Restrições:** orçamento zero (só ferramentas gratuitas), dados reais nunca em repositório público, segurança e LGPD desde o início.
- **Nível técnico atual:** iniciante completo em API, endpoints e mapeamento de tabelas; já fez páginas em HTML/CSS/JS e trabalhos em C.

## 2. Como ensinar

- **Liberação gradual:** primeiro Claude mostra e explica; depois fazem juntos, com lacunas para a pessoa preencher; depois a pessoa escreve e Claude só revisa.
- Explicar cada conceito novo em poucas linhas, com um exemplo mínimo, **antes** de usá-lo.
- Cada etapa termina com algo **visível funcionando** e com um teste.
- Perguntar, em vez de entregar a resposta, quando o arquivo faz parte do plano de aprendizado.
- Linguagem direta, sem jargão não explicado. Quando usar um termo técnico novo, definir e, se for importante, acrescentar ao glossário (seção 6).
- A pessoa prefere não gastar tempo escrevendo CSS de variáveis (cores e tamanhos); o foco de escrita dela é a lógica (JavaScript/Python), os testes e a API.

## 3. Mapa dos projetos

| Projeto | Nível | Stack | Situação |
| --- | --- | --- | --- |
| Landing page (escritório fictício) | 1 | HTML, CSS, JavaScript, Playwright, GitHub Actions | v1 na `main` (GitHub Pages ainda não ativado); faltam: rodar axe, html-validate, Lighthouse e fontes reais, ativar Pages e as etapas guiadas |
| Painel de estatísticas de Dota 2 | 2 | Python, FastAPI, SQLAlchemy, pytest | Em desenho (SEO, idiomas e escopo em aprovação; repositório criado só com licença e aviso) |
| E-commerce | 3 | TypeScript, NestJS, React | Não iniciado |
| AtendeFlow (CRM, agenda, orçamentos multiempresa, pt/en) | 3 | A definir | Não iniciado |

Repositórios antigos já organizados e com README; não são prioridade.

## 4. Decisões técnicas já tomadas

- Fluxo de trabalho: ideia, especificação, plano, implementação (skills *superpowers*), com aprovação da pessoa a cada etapa.
- Python: FastAPI, Pydantic, SQLAlchemy 2, httpx, pytest, ruff, Docker. Banco: SQLite no início, PostgreSQL perto do fim.
- Fontes e recursos hospedados no próprio projeto, sem terceiros (LGPD).
- CI com GitHub Actions; publicação gratuita no GitHub Pages quando for site estático.
- Ordem de aprendizado do painel: consumir uma API, guardar no banco, criar a própria API, testar, proteger, entregar.

## 5. Ambiente de trabalho

- **Claude no chat/nuvem:** bom para planejar, escrever documentos e arquivos; a rede é limitada (muitas vezes sem npm, pip ou acesso a sites de documentação), então não consegue rodar tudo.
- **Claude Code na máquina da pessoa:** onde o código roda de verdade, com internet. É o lugar certo para instalar dependências, rodar testes e a pessoa escrever código.
- A pessoa cria os repositórios vazios no GitHub; Claude consegue enviar arquivos para repositórios que ela autorizou.
- Os modelos de CI, Docker e `pyproject` do kit ainda **não foram executados** em um projeto real.

## 6. Glossário vivo

Definições curtas, para consulta rápida. Acrescente termos novos ao longo dos projetos.

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

Decisões que valem para vários projetos. Acrescente no topo, com data.

- **2026-11-10:** aprovados pela pessoa: arquitetura híbrida (páginas estáticas para busca e API para jogadores), ordem de idiomas (pt-BR e inglês, depois os demais) e versão 1 (heróis e meta, busca de jogador, diagnóstico em pt-BR). Fonte de dados proposta: OpenDota atrás de uma interface própria; limites e regras ainda sem confirmação oficial. Especificação em `painel-dota/docs/superpowers/specs/`, aguardando revisão.
- **2026-11-10:** o painel de Dota 2 é um site público para jogadores, com **dados reais em execução** (OpenDota, API da comunidade, não da Valve); o repositório, os testes e os exemplos continuam só com dados fictícios.
- **2026-11-10:** o painel entra com busca (SEO) e vários idiomas desde o desenho (`PADROES.md`, seção 9A). Arquitetura e ordem dos idiomas dependem de aprovação.
- **2026-11-10:** a conta do GitHub passou a se chamar `aryelderyck`; endereços e links foram atualizados (E-021, E-022).
- **2026-11-09:** projeto 2 passa a ser o painel de estatísticas de Dota 2 (OpenDota), no lugar do radar de licitações. Motivo: a pessoa não se animou com o tema; busca algo ligado a jogos.
- **2026-11-09:** criado o kit `padroes-de-qualidade` (padrões, erros, perguntas de revisão, contexto, práticas) para manter a qualidade entre os projetos.

## 9. Como evoluir

- Atualize a seção 3 quando um projeto mudar de estado, a seção 6 a cada termo novo, a seção 7 a cada dificuldade e a seção 8 a cada decisão.
- Antes de gravar algo sobre a pessoa, confirme que é adequado a um repositório público.
- Registre a mudança no `CHANGELOG.md`.
