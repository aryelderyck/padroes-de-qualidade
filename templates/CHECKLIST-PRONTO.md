# Definição de pronto: [NOME DO PROJETO]

Nível do projeto: [1, 2 ou 3]. Marque cada item e anote a **evidência** (comando, link ou captura).
Um item que não se aplica é riscado com o motivo. Item não verificado fica desmarcado e explicado no README.

## Nível 1 (todo projeto)
- [ ] README completo (o que é, rodar, testar, decisões, segurança e LGPD, limitações) · evidência:
- [ ] `.gitignore`, `.gitattributes`, `LICENSE`, `CLAUDE.md` presentes · evidência:
- [ ] Dependabot alerts, secret scanning e push protection ativados · evidência:
- [ ] Testes cobrem os comportamentos, inclusive erros e casos de borda · saída dos testes:
- [ ] Teste de mutação manual feito em pelo menos 3 pontos críticos · o que foi quebrado:
- [ ] CI roda em todo Pull Request e na `main` e está verde · link:
- [ ] Deploy (se houver) só ocorre com CI verde · link:
- [ ] Nenhum dado real, segredo ou chave no repositório (inclusive no histórico) · como verifiquei:
- [ ] Nenhum recurso de terceiros desnecessário · como verifiquei:
- [ ] Revisão de simplicidade feita (`REVISAO.md`, blocos B, C e F): o que foi simplificado ou deixado de fora de propósito · anotação:
- [ ] Todos os erros da etapa registrados no catálogo (`ERROS.md`) · IDs:
- [ ] `APRENDIZADOS.md` atualizado e a pessoa consegue explicar o projeto · data:
- [ ] Verificação visual com capturas (1440 px e 390 px), se houver front-end · arquivos:
- [ ] Acessibilidade (axe sem violações) e Lighthouse >= 95, se houver front-end · números:

## Nível 2 (API e dados)
- [ ] Validação de entrada em todas as rotas · evidência:
- [ ] Consultas parametrizadas ou via ORM, sem SQL montado com texto do usuário · evidência:
- [ ] Migrações versionadas; chaves estrangeiras e restrições no banco · evidência:
- [ ] Paginação, formato de erro único e códigos de status corretos · evidência:
- [ ] OpenAPI atualizada e rota `/saude` · evidência:
- [ ] Chamadas externas com tempo limite, nova tentativa, limite de requisições e cache · evidência:
- [ ] Testes de integração com banco e API sem acessar a internet · evidência:
- [ ] `pip-audit` / `npm audit` sem vulnerabilidades altas ou críticas · saída:
- [ ] Análise estática de segurança (CodeQL ou regras `S` do ruff) sem alertas abertos · link:
- [ ] Logs estruturados e sem dados pessoais · evidência:
- [ ] Docker: multi-stage, usuário sem root, `.dockerignore`, varredura Trivy · saída:

## Nível 3 (usuários e dados pessoais)
- [ ] Tabela de dados pessoais (dado, finalidade, base legal, retenção) escrita · local:
- [ ] Direitos do titular implementados (acessar, corrigir, excluir, exportar) · evidência:
- [ ] Política de privacidade publicada · link:
- [ ] Plano de resposta a incidente escrito · local:
- [ ] Senhas com argon2/bcrypt; tokens com expiração; limite de tentativas de login · evidência:
- [ ] Autorização verificada em cada recurso, com testes negativos (A não acessa dado de B) · evidência:
- [ ] CORS restritivo, cabeçalhos de segurança e limite de requisições · evidência:
- [ ] Isolamento entre clientes testado (multiempresa) · evidência:
