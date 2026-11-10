# Padrões de qualidade dos projetos

Versão 0.3 · 2026-11-09 · Dono: Aryel

Este é o documento mestre. Todo projeto novo (landing, painel, e-commerce, AtendeFlow e os que vierem)
começa por aqui e só é considerado **pronto** quando cumpre a Definição de Pronto (seção 2).

> **Para Claude e Claude Code:** leia este arquivo, o [`CONTEXTO.md`](CONTEXTO.md) e a seção "Regras que saíram dos
> erros" do [`ERROS.md`](ERROS.md) no início de cada projeto e de cada etapa grande. Antes de decidir ou entregar,
> passe pelo bloco certo de [`REVISAO.md`](REVISAO.md). Mapa completo de consulta no `README.md`.
> Copie `templates/CLAUDE.template.md` para o repositório novo e preencha. Se algum padrão não for cumprido,
> registre o motivo em uma seção "Desvios" na especificação ou no README. Nunca ignore em silêncio.

## 1. Princípios

1. **Aprender vem antes de terminar rápido.** Cada etapa deixa a pessoa capaz de explicar o que foi feito.
2. **Prove, não diga.** Nada é "funciona" sem o comando rodado e a saída lida. O que não foi verificado fica escrito como não verificado.
3. **Segurança e privacidade desde o primeiro commit**, não no fim.
4. **Orçamento zero.** Só ferramentas gratuitas. Se uma ferramenta passar a ser paga, troque.
5. **Dados reais nunca entram em repositório público.** Só dados fictícios.
6. **Todo erro é registrado.** Erro que aparece vai para o [`ERROS.md`](ERROS.md) no mesmo dia, com causa raiz e regra de prevenção.
7. **Questione antes de entregar:** é a melhor maneira? dá para fazer com menos código? dá para otimizar sem quebrar? ([`REVISAO.md`](REVISAO.md)).
8. **Simples primeiro.** Cada regra abaixo tem um nível (seção 2). Não aplique o nível 3 num projeto de nível 1.

## 2. Níveis e Definição de Pronto

| Nível | Quando se aplica | Exemplos |
| --- | --- | --- |
| **1. Base** | Todo projeto | Landing page |
| **2. API e dados** | Tem backend, banco ou API externa | Painel de Dota 2, e-commerce |
| **3. Usuários e dados pessoais** | Tem contas, login ou dados de pessoas | E-commerce, AtendeFlow |

Cada nível inclui os anteriores. O projeto só é "pronto" com **todos** os itens do seu nível marcados e com a evidência
(comando, link ou captura) anotada. Use `templates/CHECKLIST-PRONTO.md`.

## 3. Repositório (nível 1)

- Nome em minúsculas com hífens, descritivo (`painel-dota`, `landing-escritorio-advocacia`).
- Arquivos obrigatórios: `README.md`, `.gitignore`, `.gitattributes` (finais de linha LF), `LICENSE` (MIT, salvo motivo contrário), `CLAUDE.md`.
- `README.md` em pt-BR com esta ordem: o que é e para quem, aviso se for fictício, como rodar, como testar, decisões e por quê, segurança e LGPD, limitações conhecidas.
- Commits pequenos, em pt-BR, no formato `tipo: o que mudou` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`).
- Nos projetos novos: trabalhar em branches curtas e abrir Pull Request, mesmo sozinho. Assim o CI protege a `main`.
  Ative em *Settings → Branches*: exigir que o CI passe antes de mesclar.
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

## 10. Observabilidade (nível 2 em diante)

- Log estruturado (JSON) com nível, hora e id de requisição.
- Rota de saúde e mensagens de erro úteis para quem opera o sistema.
- Sem dados pessoais nos registros.

## 11. Documentação e aprendizado

- Cada projeto tem `APRENDIZADOS.md` (modelo em `templates/`). Ao fim de cada etapa a pessoa escreve, **com as próprias palavras**: o que aprendeu, o erro que cometeu e como corrigiu.
- Dificuldades de aprendizado e o que ajuda ficam na seção 7 do [`CONTEXTO.md`](CONTEXTO.md).
- Método de ensino: o professor (Claude) mostra, depois fazem juntos com lacunas, depois a pessoa escreve sozinha e Claude só revisa. Cada etapa termina com algo visível e um teste.
- Todo conceito novo (API, endpoint, tabela, migração, token…) ganha uma explicação de poucas linhas com exemplo mínimo antes de ser usado.
- `README.md` conta as decisões e as limitações com honestidade, incluindo o que **não** foi verificado.

## 12. Mapa dos projetos

| Projeto | Nível | O que pesa mais |
| --- | --- | --- |
| Landing page | 1 | Front-end, acessibilidade, LGPD sem terceiros, CI e Pages |
| Painel de Dota 2 | 2 | API externa e limites, banco, testes sem rede, direito de apagar dados |
| E-commerce | 3 | Contas, carrinho, pagamento fictício, autorização, testes de segurança |
| AtendeFlow | 3 | Multiempresa (isolamento entre clientes), permissões, LGPD completa |

## 13. Lições já aprendidas

O registro completo, com causa raiz e correção de cada erro, está em [`ERROS.md`](ERROS.md). Resumo do que mais pesa:

- **CSP `default-src 'self'` bloqueia script inline e atributo `style=""`.** Use arquivos externos e classes (E-018).
- **Teste que passa de primeira precisa de mutação,** e teste de "não faz X" deve observar a tentativa, não só o efeito (E-009, E-010).
- **Gere o `package-lock.json` e use `npm ci` no CI.** Sem isso, o build não é reproduzível (E-005).
- **Valide YAML e outros arquivos de configuração antes de subir** (E-011, E-016).
- **O efeito nunca esconde conteúdo:** tarja e luz precisam de plano B (sem JavaScript, movimento reduzido, script que falha).
- **Capturas de tela mostram o que o código não mostra,** inclusive o meio de uma animação (E-007, E-008).
- **Ferramentas que não rodaram são declaradas** como não verificadas (E-005, E-013).
- **Confirme limites e termos de uma API na fonte oficial** antes de desenhar o projeto em torno dela (E-014, E-017).

## 14. Como evoluir este documento

- **Todo erro vira uma entrada no [`ERROS.md`](ERROS.md)** no mesmo dia, antes de seguir. Quem encontra registra
  (Claude, Claude Code ou a pessoa). Se o erro revela uma regra, ela entra neste documento e a entrada aponta para ela.
- No fim de cada etapa, releia as entradas novas com a pessoa: o que aprendemos e o que mudou no processo.
- Toda regra nova entra com o motivo e começa em [`PRATICAS.md`](PRATICAS.md) como candidata; só vira obrigatória
  depois de testada em um projeto de verdade.
- Este documento é **vivo**: Claude pode e deve propor acréscimos, correções e remoções (marcando como obsoleto, com
  data e motivo, em vez de apagar). Mudanças grandes na estrutura pedem aprovação da pessoa.
- Mude a versão no topo e anote o que mudou em `CHANGELOG.md`.
