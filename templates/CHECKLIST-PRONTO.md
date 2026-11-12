# Definição de pronto: [NOME DO PROJETO]

Nível do projeto: [1, 2 ou 3] · Ritmo: [rápido ou completo]. Marque cada item e anote a **evidência** (comando, link ou captura).
Um item que não se aplica é riscado com o motivo. Item não verificado fica desmarcado e explicado no README.
**Ritmo rápido** (só nível 1): valem os itens marcados **[E]**; os outros vão para o README como "não feito, de propósito".

## Nível 1 (todo projeto)
- [ ] **[E]** README completo (o que é, rodar, testar, decisões, segurança e LGPD, limitações) · evidência:
- [ ] **[E]** `.gitignore`, `.gitattributes`, `LICENSE`, `CLAUDE.md` presentes · evidência:
- [ ] **[E]** Dependabot alerts, secret scanning e push protection ativados · evidência:
- [ ] **[E]** Testes cobrem os comportamentos da lógica, inclusive erros e casos de borda · saída dos testes:
- [ ] **[E]** Comando de conferência (formatação, linter, tipos e testes) passa na máquina e no CI, sem regra desligada no projeto · saída:
- [ ] Conferência independente (`/conferir-codigo`) sem achado alto ou médio em aberto · relatório:
- [ ] **[E]** Teste de mutação manual em pelo menos 3 pontos críticos (ritmo rápido: pelo menos 1) · o que foi quebrado:
- [ ] **[E]** CI roda na `main` (e em todo Pull Request, quando houver) e está verde · link:
- [ ] **[E]** Deploy (se houver) só ocorre com CI verde · link:
- [ ] **[E]** Nenhum dado real, segredo ou chave no repositório (inclusive no histórico e nos autores dos commits) nem nos arquivos que vão para o navegador · como verifiquei:
- [ ] **[E]** Nenhum recurso de terceiros desnecessário · como verifiquei:
- [ ] **[E]** Dado de fora aparece como texto, nunca como HTML cru, e a resposta é validada antes do uso, se o projeto consome API · teste:
- [ ] **[E]** Dependências novas conferidas no registro oficial (nome exato, dono, repositório) · quais:
- [ ] Revisão de simplicidade feita (`REVISAO.md`, blocos B, C e F): o que foi simplificado ou deixado de fora de propósito · anotação:
- [ ] **[E]** Erros da etapa que entram no critério do `REGRAS.md` (seção 3) registrados no `ERROS.md` · IDs:
- [ ] **[E]** `APRENDIZADOS.md` atualizado e a pessoa consegue explicar o projeto · data:
- [ ] **[E]** Verificação visual com capturas (1440 px e 390 px), se houver front-end · arquivos:
- [ ] **[E]** Teclado, foco visível e contraste conferidos à mão, se houver front-end · como:
- [ ] Acessibilidade (axe sem violações) e Lighthouse >= 95, se houver front-end · números:

## Nível 2 (API e dados)
Segurança da API: `PADROES.md`, seção 6.2. Cada item pede o teste que o prova.
- [ ] Lista escrita de rotas públicas; todas as outras recusam pedido sem credencial (401 ou 403) · teste:
- [ ] Rota que recebe ID confere a posse: A não acessa o recurso de B · teste:
- [ ] Entrada validada em todas as rotas e campo extra recusado; resposta com modelo explícito · teste:
- [ ] Limites: tamanho do corpo, paginação com teto, tempo limite e limite de requisições com 429 · um teste por limite:
- [ ] CORS com lista de origens e cabeçalhos de segurança presentes; depuração desligada · teste:
- [ ] Consultas parametrizadas ou via ORM, sem SQL montado com texto do usuário · evidência:
- [ ] Nenhum segredo em URL, log, mensagem de erro, imagem ou front-end; `.env.example` sem valores · como verifiquei:
- [ ] Dado de API de terceiros (ou de modelo de IA) validado e nunca repassado como HTML cru · teste:
- [ ] Erro com formato único e mensagem genérica, sem *stack trace*; códigos de status corretos · teste:
- [ ] Migrações versionadas; chaves estrangeiras e restrições no banco · evidência:
- [ ] OpenAPI igual ao código, rota `/saude` sem dado sensível, nenhuma rota de teste no ar · evidência:
- [ ] Chamadas externas com tempo limite, nova tentativa, limite de requisições e cache · evidência:
- [ ] Testes de integração com banco e API sem acessar a internet · evidência:
- [ ] `pip-audit` / `npm audit` sem vulnerabilidades altas ou críticas · saída:
- [ ] Análise estática de segurança (CodeQL ou regras `S` do ruff) sem alertas abertos · link:
- [ ] Revisão de segurança independente feita (`/security-review` na branch) e achados tratados · resultado:
- [ ] Logs estruturados, com falhas de autenticação e de validação, e sem dados pessoais · evidência:
- [ ] Docker: multi-stage, usuário sem root, `.dockerignore`, varredura Trivy · saída:
- [ ] Se o projeto chama um modelo de IA: chave só no servidor, teto de gasto, saída tratada como não confiável (seção 6.4) · evidência:

## Nível 3 (usuários e dados pessoais)
- [ ] Tabela de dados pessoais (dado, finalidade, base legal, retenção) escrita · local:
- [ ] Direitos do titular implementados (acessar, corrigir, excluir, exportar) · evidência:
- [ ] Política de privacidade publicada · link:
- [ ] Plano de resposta a incidente escrito · local:
- [ ] Senhas com argon2/bcrypt; tokens com expiração e algoritmo fixo; limite de tentativas de login · evidência:
- [ ] Autorização verificada em cada recurso, com testes negativos (A não acessa dado de B) · evidência:
- [ ] CORS restritivo, cabeçalhos de segurança e limite de requisições · evidência:
- [ ] Isolamento entre clientes testado (multiempresa) · evidência:
