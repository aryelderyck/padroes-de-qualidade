# Orientação de segurança deste repositório

<!-- Copie para .claude/claude-security-guidance.md do projeto. O plugin security-guidance do Claude Code lê este
     arquivo nas revisões de fim de turno e de commit. Apague os blocos que não valem para o projeto e acrescente as
     regras próprias dele. Limite do plugin: 8 KB somando todos os arquivos de orientação. -->

## Sempre
- Chave, token ou senha nunca aparece em código, URL, log, mensagem de erro nem em arquivo que vai para o navegador
  (variáveis `VITE_*`, `NEXT_PUBLIC_*` e `REACT_APP_*` são públicas).
- Dado vindo de API de terceiros, de usuário ou de modelo de IA é entrada não confiável: validar o formato e nunca
  inserir como HTML cru (`innerHTML`, `dangerouslySetInnerHTML`).
- Pacote novo só entra depois de conferido no registro oficial (nome exato, dono, repositório).

## Projeto que expõe uma API
- Toda rota exige autenticação, salvo as da lista de rotas públicas: [liste aqui as rotas públicas].
- Rota que recebe um ID confere no servidor se o recurso pertence a quem pede.
- Modelo de entrada recusa campo extra; resposta usa modelo explícito, nunca o objeto do banco.
- Toda rota tem tamanho máximo de corpo, paginação com teto, tempo limite e limite de requisições com resposta 429.
- O servidor não busca endereço montado com texto do usuário sem validar; destinos ficam fixos na configuração.
- CORS com lista de origens, nunca `*` com credenciais. Modo de depuração desligado.
- Consulta ao banco sempre parametrizada ou via ORM.
- Erro para o cliente é genérico; nada de *stack trace* na resposta. Log sem dado pessoal, senha ou token.

## Projeto que chama um modelo de IA
- A chave do modelo fica só no servidor, com teto de gasto e limite por usuário.
- A saída do modelo não vira HTML cru, SQL, comando nem código executado sem validação.
- Texto de usuário, de página ou de documento não muda permissões; ação com efeito pede confirmação da pessoa.
