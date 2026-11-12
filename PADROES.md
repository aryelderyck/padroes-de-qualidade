# Padrões de qualidade dos projetos

Versão 0.5 · 2026-11-12 · Dono: Aryel

Este é o documento mestre. Todo projeto novo (landing, painel, e-commerce, AtendeFlow e os que vierem)
começa por aqui e só é considerado **pronto** quando cumpre a Definição de Pronto (seção 2).

> **Para Claude e Claude Code:** a leitura de toda sessão é o [`REGRAS.md`](REGRAS.md), que é curto e diz o que abrir em
> cada momento. Deste documento, leia **só as seções do nível do projeto** (tabela na seção 2), no começo do projeto e
> quando o assunto aparecer. Se algum padrão não for cumprido, registre o motivo em uma seção "Desvios" na especificação
> ou no README. Nunca ignore em silêncio.

## 1. Princípios

1. **Aprender vem antes de terminar rápido.** Cada etapa deixa a pessoa capaz de explicar o que foi feito.
2. **Prove, não diga.** Nada é "funciona" sem o comando rodado e a saída lida. O que não foi verificado fica escrito como não verificado.
3. **Segurança e privacidade desde o primeiro commit**, não no fim.
4. **Orçamento zero.** Só ferramentas gratuitas. Se uma ferramenta passar a ser paga, troque.
5. **Dados reais nunca entram em repositório público.** Só dados fictícios.
6. **Erro que ensina é registrado.** O que pode se repetir, custou mais de uns 15 minutos ou chegou à pessoa vai para o [`ERROS.md`](ERROS.md) ao fechar a tarefa, com causa raiz e prevenção ([`REGRAS.md`](REGRAS.md), seção 3).
7. **Questione antes de entregar:** é a melhor maneira? dá para fazer com menos código? dá para otimizar sem quebrar? ([`REVISAO.md`](REVISAO.md)).
8. **Simples primeiro.** Cada regra abaixo tem um nível e um ritmo (seção 2). Não aplique o nível 3 num projeto de nível 1, nem o ritmo completo num projeto rápido.

## 2. Níveis, ritmo e Definição de Pronto

O nível é decidido pelo que o projeto **hospeda**, não pelo que ele consome.

| Nível | Quando se aplica | Exemplos | Seções deste documento |
| --- | --- | --- | --- |
| **1. Base** | Todo projeto. Inclui front-end sem servidor próprio, mesmo que leia dados públicos de terceiros sem chave | Landing page, explorador de campeões | 1 a 5, 9 (se tem tela), 9A (se quer ser achado na busca) e 11 |
| **2. API e dados** | Tem servidor próprio (API), banco de dados ou segredo (chave de API) | Painel de Dota 2 | As do nível 1, mais 6, 8 e 10, e a 7 se tocar dado de pessoa |
| **3. Usuários e dados pessoais** | Tem contas, login ou dados de pessoas | E-commerce, AtendeFlow | Todas |

Cada nível inclui os anteriores. Projeto de nível 1 que chama uma API pública segue também o último item da seção 8
(tempo limite, erro tratado, cache) e testa sem acessar a internet.

**Ritmo.** É combinado com a pessoa no começo e escrito no `CLAUDE.md` do projeto:

- **Completo** (padrão; obrigatório nos níveis 2 e 3): todos os itens da checklist do nível, com a evidência anotada.
- **Rápido** (só nível 1, projeto de até uma semana): valem os itens marcados **[E]** (essencial) na checklist. Os outros
  ficam listados no README como "não feito, de propósito". O que nunca sai: nenhum segredo ou dado real no repositório,
  testes da lógica, CI verde, verificar antes de afirmar e a pessoa conseguir explicar o que foi feito.

O projeto só é "pronto" com os itens do seu nível e do seu ritmo marcados, com a evidência (comando, link ou captura)
anotada. Use `templates/CHECKLIST-PRONTO.md`.

## 3. Repositório (nível 1)

- Nome em minúsculas com hífens, descritivo (`painel-dota`, `landing-escritorio-advocacia`).
- Arquivos obrigatórios: `README.md`, `.gitignore`, `.gitattributes` (finais de linha LF), `LICENSE` (MIT, salvo motivo contrário), `CLAUDE.md`.
- `README.md` em pt-BR com esta ordem: o que é e para quem, aviso se for fictício, como rodar, como testar, decisões e por quê, segurança e LGPD, limitações conhecidas.
- Commits pequenos, em pt-BR, no formato `tipo: o que mudou` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`).
- Nos projetos novos: trabalhar em branches curtas e abrir Pull Request, mesmo sozinho. Assim o CI protege a `main`.
  Ative em *Settings → Branches*: exigir que o CI passe antes de mesclar. Em ritmo rápido, commit direto na `main` com o CI rodando é aceito.
- Ative no GitHub (gratuito em repositório público): *Dependabot alerts*, *Dependabot security updates*, *Secret scanning* e *Push protection*.
- Decisões importantes viram um parágrafo curto na especificação (`docs/superpowers/specs/`). Mudanças depois disso vão em "Desvios".
- Nunca versione: `.env`, chaves, tokens, dumps de banco, dados reais. Se vazar um segredo, **revogue-o** primeiro e limpe o histórico depois.

## 4. Testes (nível 1 em diante)

- **Todo comportamento tem teste.** Mudou comportamento: escreva ou ajuste o teste antes (TDD) e veja falhar pelo motivo certo.
- Pirâmide: muitos testes unitários (rápidos, sem rede nem banco real), alguns de integração (banco e API de verdade), poucos E2E.
- Testes não chamam a internet. Use respostas fictícias gravadas (fixtures) no lugar de APIs externas.
- Cada teste é independente dos outros e pode rodar em qualquer ordem.
- Cubra casos de erro e de borda, não só o caminho feliz: vazio, `null`, texto enorme, acentos, valores negativos, duplicados.
- Cobertura é sinal, não meta: mire em 80% ou mais **da lógica de negócio**, e olhe os trechos não cobertos.
- **Teste de mutação manual.** Teste que passa de primeira merece desconfiança. Quebre o código de propósito e confirme que algum teste falha.
- Nível 3: testes **negativos** de segurança (usuário A não lê dado do usuário B, rota protegida sem login devolve 401/403).

## 5. Pipeline de CI/CD

Ordem das etapas (para na primeira que falhar):

1. Instalar com lockfile (`npm ci`, `pip install` com versões travadas).
2. Verificar formatação e lint (`ruff`, `eslint`).
3. Verificar tipos, quando o projeto usar (`mypy`, `tsc`).
4. Testes unitários.
5. Testes de integração e E2E.
6. Cobertura mínima.
7. Segurança: auditoria de dependências, análise estática (SAST) e varredura de segredos.
8. Build (e imagem Docker, se houver) e varredura da imagem.
9. Deploy, **só na `main` e só se tudo acima passou**.

Regras do workflow:

- `permissions: contents: read` por padrão; dê mais só ao job que precisa (ex.: Pages).
- Versões das actions fixadas (`@v4`) e conferidas de tempos em tempos; Dependabot atualiza.
- Segredos só em *Settings → Secrets*, nunca no YAML nem em logs.
- Valide o YAML antes de subir (`python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" arquivo.yml`). Valores com `:` precisam de aspas.
- Verificações lentas ou instáveis (ex.: Lighthouse) ficam em workflow separado e não travam o deploy.
- O pipeline é parte do aprendizado: o aluno deve conseguir explicar cada etapa.

## 6. Segurança (nível 2 em diante)

Base: OWASP Top 10 e OWASP ASVS. Itens mínimos:

- **Entrada:** validar tudo na borda (Pydantic, Zod). Consultas sempre parametrizadas ou via ORM. Nunca montar SQL com texto do usuário.
- **Segredos:** em variáveis de ambiente. Entregue um `.env.example` sem valores reais. Chave de API nunca no front-end nem no repositório.
- **Dependências:** versões travadas, `pip-audit` / `npm audit` no CI, Dependabot ligado, dependências novas justificadas.
- **Erros:** mensagens genéricas para o cliente, detalhes só no log. Nada de stack trace na resposta.
- **Rede:** HTTPS, CORS restritivo (lista de origens, nunca `*` com credenciais), limite de requisições nas rotas sensíveis, cabeçalhos de segurança, CSP quando houver HTML.
- **Docker:** imagem base fixada, build em múltiplos estágios, usuário sem privilégio de root, `.dockerignore`, sem segredos na imagem, varredura com Trivy.
- **Registros (logs):** estruturados, com id de requisição e **sem dados pessoais, senhas, tokens**.
- **Nível 3, contas e senhas:** hash com argon2 ou bcrypt (nunca criar o próprio), tokens com expiração, autorização verificada em **cada** recurso (evita acessar dado de outro usuário), bloqueio gradual de tentativas de login, redefinição de senha segura, MFA quando fizer sentido.

## 7. LGPD (todos os projetos que tocam dados de pessoas)

Isto é boa prática de engenharia, não aconselhamento jurídico. Para cada projeto, responda por escrito (no README ou em `docs/`):

1. **Quais dados pessoais** o sistema trata? (Faça uma tabela: dado, origem, para quê.)
2. **Finalidade** de cada dado e **base legal** (art. 7º: consentimento, execução de contrato, legítimo interesse etc.).
3. **Minimização:** dá para não coletar? dá para coletar menos? (princípio da necessidade, art. 6º.)
4. **Retenção:** por quanto tempo guardamos e como apagamos?
5. **Direitos do titular** (art. 18): como a pessoa confirma, acessa, corrige, exclui e leva os dados? Crie o endpoint ou a rotina correspondente.
6. **Segurança** (art. 46) e **plano para incidente** (art. 48): quem avisa quem, e em quanto tempo, se houver vazamento.
7. **Terceiros:** nada de CDN, fontes, analytics ou cookies de terceiros sem necessidade e sem aviso. Prefira hospedar no próprio projeto.
8. **Política de privacidade** pública e em linguagem simples, mesmo em projeto fictício (indicando que é demonstração).
9. Dados de teste e de demonstração são **fictícios**. Dado público de pessoa (nome, ID) continua sendo dado pessoal.

## 8. API e banco de dados (nível 2)

- REST: substantivos no plural (`/jogadores`, `/partidas`), verbos HTTP corretos, códigos de status corretos (200, 201, 204, 400/422, 401, 403, 404, 409, 429).
- Versão no caminho (`/v1/...`), paginação em toda listagem, formato de erro único e consistente.
- Documentação automática (OpenAPI/Swagger) sempre atualizada. Rota de saúde (`/saude`) sem dados sensíveis.
- Banco: migrações versionadas (Alembic, Prisma ou equivalente), chaves estrangeiras e restrições no banco (não só no código), índices para as consultas reais, dados de exemplo fictícios.
- Chamadas a APIs externas: tempo limite, nova tentativa com espera, respeito ao limite de requisições, cache no banco, tratamento de erro e de resposta inesperada.

## 9. Front-end (quando houver)

- HTML semântico, `lang`, foco visível, navegação por teclado, contraste mínimo de 4,5:1, `prefers-reduced-motion` respeitado.
- Teste de acessibilidade automatizado (axe) e Lighthouse com nota de pelo menos 95 em Desempenho, Acessibilidade e Boas práticas.
- Melhoria progressiva: sem JavaScript o conteúdo continua legível.
- Verificação visual real, com capturas de tela em 1440 px e 390 px, antes de dar por concluído.

## 9A. Web pública: busca, idiomas e velocidade (todo site que quer ser encontrado)

Vale para o painel de Dota 2 e para qualquer site público. **Nenhuma regra garante posição nos resultados:** a
posição depende da concorrência, de links vindos de outros sites e de tempo. O que o projeto controla é a base técnica
sem falhas e o conteúdo realmente útil.

**Rastreamento e indexação**
- Cada página tem `<title>` e `meta description` próprios, um único `<h1>`, URL canônica (`rel="canonical"`) e HTML semântico.
- `sitemap.xml` e `robots.txt` gerados pelo build, com endereços completos e só das páginas que devem aparecer na busca.
- Conteúdo importante existe no HTML entregue (renderização no servidor ou geração estática); não depende de JavaScript para aparecer.
- Páginas com dados pessoais (por exemplo, a página de um jogador) usam `noindex` e ficam fora do sitemap (LGPD).
- Dados estruturados (JSON-LD) só descrevem o que a página realmente mostra.
- Links internos com texto descritivo ("heróis mais fortes do patch", não "clique aqui"); toda página importante é alcançável em poucos cliques e tem migalhas de pão.
- Páginas geradas em massa só entram no índice se tiverem valor próprio; páginas repetitivas e vazias contam como abuso de conteúdo em escala na política do Google.

**Idiomas (i18n)**
- Um endereço por idioma, no caminho (`/pt-br/`, `/en/`), nunca decidido só por cookie ou por IP.
- `hreflang` conforme a documentação do Google: cada página aponta para si mesma e para todas as versões, de volta em ambos os sentidos, com endereços completos, mais `x-default`. Códigos de idioma ISO 639-1 e de região ISO 3166-1 (`es-419` não é aceito).
- `<html lang>` correto em cada página; seletor de idioma feito de links comuns.
- Textos em arquivos de tradução; sem tradução automática crua em página indexada (revisar antes de publicar).
- Números, datas e plurais com `Intl`; fontes próprias com subconjunto para cirílico e chinês, sem Google Fonts.
- Idioma novo só entra com tradução revisada de todas as páginas indexáveis dele; melhor menos idiomas bem feitos do que muitos pela metade.

**Velocidade e qualidade**
- Core Web Vitals no percentil 75: LCP até 2,5 s, INP até 200 ms, CLS até 0,1. Medir com Lighthouse CI no pipeline (nota mínima de 95 em Desempenho, Acessibilidade, Boas práticas e SEO) e conferir em campo depois de publicar.
- Reservar espaço para imagens e gráficos (sem saltos de layout), imagens em formatos modernos e com `width`/`height`, CSS crítico pequeno, JavaScript só onde há interação.
- HTTPS, cabeçalhos de segurança e CSP sem recursos de terceiros (sem CDN, sem analytics que dependam de cookies).
- Teste automatizado do que dá para provar: `hreflang` recíproco, links internos sem erro 404, um `<h1>` por página, canônica presente, `noindex` nas páginas de jogador.

## 10. Observabilidade (nível 2 em diante)

- Log estruturado (JSON) com nível, hora e id de requisição.
- Rota de saúde e mensagens de erro úteis para quem opera o sistema.
- Sem dados pessoais nos registros.

## 11. Documentação e aprendizado

- Cada projeto tem `APRENDIZADOS.md` (modelo em `templates/`). Ao fim de cada etapa a pessoa escreve, **com as próprias palavras**: o que aprendeu, o erro que cometeu e como corrigiu.
- Dificuldades de aprendizado e o que ajuda ficam na seção 7 do [`CONTEXTO.md`](CONTEXTO.md).
- O jeito de ensinar fica em um só lugar: o estilo de saída Professor (`templates/output-styles/professor.md`). Os
  motivos de cada princípio estão no [`CONTEXTO.md`](CONTEXTO.md), seção 2.
- `README.md` conta as decisões e as limitações com honestidade, incluindo o que **não** foi verificado.

## 12. Mapa dos projetos

A lista dos projetos, com nível, ritmo, stack, o que pesa mais e a situação de cada um, fica em um só lugar:
[`CONTEXTO.md`](CONTEXTO.md), seção 3.

## 13. Lições já aprendidas

As regras gerais que saíram dos erros estão no [`REGRAS.md`](REGRAS.md), seção 2. Aqui ficam só as lições técnicas
que não viraram regra geral:

- **CSP `default-src 'self'` bloqueia script inline e atributo `style=""`.** Use arquivos externos e classes (E-018).
- **Gere o `package-lock.json` e use `npm ci` no CI.** Sem isso, o build não é reproduzível (E-005).
- **O efeito nunca esconde conteúdo:** animação e luz precisam de plano B (sem JavaScript, movimento reduzido, script que falha).

## 14. Como evoluir este documento

- **Erro que ensina vira uma entrada no [`ERROS.md`](ERROS.md)** ao fechar a tarefa (critério no `REGRAS.md`, seção 3).
  Quem encontra registra (Claude, Claude Code ou a pessoa). Se o erro revela uma regra geral, ela entra no `REGRAS.md`.
- **O kit tem de continuar leve.** O `REGRAS.md` tem limite de 80 linhas. Antes de acrescentar uma regra a qualquer
  arquivo, veja se ela cabe fundida a uma existente ou se substitui uma que perdeu o sentido. Regra que só atrasa, sem
  ter evitado erro em um projeto inteiro, é candidata a sair.
- No fim de cada etapa, releia as entradas novas com a pessoa: o que aprendemos e o que mudou no processo.
- Toda regra nova entra com o motivo e começa em [`PRATICAS.md`](PRATICAS.md) como candidata; só vira obrigatória
  depois de testada em um projeto de verdade.
- Este documento é **vivo**: Claude pode e deve propor acréscimos, correções e remoções (marcando como obsoleto, com
  data e motivo, em vez de apagar). Mudanças grandes na estrutura pedem aprovação da pessoa.
- Mude a versão no topo e anote o que mudou em `CHANGELOG.md`.
