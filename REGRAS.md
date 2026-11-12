# Regras de toda sessão

**Única leitura obrigatória do kit no início de cada sessão**, em qualquer projeto. O `CLAUDE.md` do projeto, que o
Claude Code já carrega sozinho, traz o contexto da pessoa e as regras do projeto. Todo o resto do kit é aberto **por
seção, no momento em que serve** (tabela abaixo). Ler o kit inteiro gasta contexto e tempo sem melhorar o resultado.

> **Limite deste arquivo: 80 linhas.** Regra nova entra fundida a uma existente ou no lugar de uma que perdeu o sentido.
> A numeração não muda: o `ERROS.md` e o histórico citam as regras pelo número.

## 1. O que abrir, e quando

| Momento | Abrir só isto |
| --- | --- |
| Toda sessão | Este arquivo |
| Começo de um projeto (uma vez) | `CONTEXTO.md`, seções 1 a 5 e 7 · `PADROES.md`, seções 1 a 5 e as do nível (tabela na seção 2 de lá) · `PRATICAS.md` |
| Escolher tema, abordagem ou stack | `REVISAO.md`, bloco A |
| Escrever código | `REVISAO.md`, bloco B |
| Rota, campo, dado, dependência ou chave nova; chamada a API ou a modelo de IA | `PADROES.md`, seção 6 (bloco do nível) · `REVISAO.md`, bloco D |
| Otimizar ou refatorar | `REVISAO.md`, bloco C |
| Testar | `PADROES.md`, seção 4 · `REVISAO.md`, bloco E |
| Site que quer ser achado na busca | `PADROES.md`, seção 9A |
| Antes de dizer "pronto" | `REVISAO.md`, bloco F · `docs/CHECKLIST-PRONTO.md` do projeto |
| Apareceu um erro | `ERROS.md`: procure no índice ou por palavra e leia só a entrada. Nunca o arquivo inteiro |
| Ensinar um conceito | `CONTEXTO.md`, seção 6 (glossário, para não redefinir um termo de outro jeito) · `REVISAO.md`, bloco G |
| Surgiu uma prática nova ou uma dificuldade da pessoa | `PRATICAS.md` (candidata) · `CONTEXTO.md`, seção 7 |

O glossário e o registro de decisões do `CONTEXTO.md` são de consulta, não de leitura corrida.

## 2. Regras que saíram dos erros

Cada regra diz **quando** vale e **o que fazer**, para dar para conferir se foi cumprida.

1. **Antes de afirmar algo ou de pedir algo à pessoa, faça a ação real** (rode o comando, tente o envio). Aviso de ferramenta não é fato (E-001).
2. **Só entra no README o que foi executado:** rode o comando e leia a saída antes de documentar (E-003).
3. **Teste passou de primeira? Quebre o código de propósito,** veja o teste falhar e desfaça (E-009, E-010).
4. **Mudou tela ou efeito? Capturas em 1440 px e 390 px,** olhadas antes de dizer que ficou bom (E-007, E-008).
5. **Arquivo de configuração (YAML, JSON, TOML, Dockerfile): valide com um comando antes de subir** (E-011, E-016).
6. **Toda entrega lista o que não foi verificado,** inclusive a ferramenta que não rodou (E-005, E-013).
7. **Acesso negado pelo ambiente: diga e adapte, ou peça o arquivo.** Não contorne o bloqueio (E-005).
8. **Antes de desenhar em torno de uma API ou serviço, leia limites, preço e termos na página oficial** (E-014).
9. **Antes de propor o tema de um projeto, pergunte o que a pessoa usa e gosta** (E-015).
10. **Criou um esqueleto? Preencha, ou diga com todas as letras que ficou vazio** (E-006).
11. **Código saiu diferente do plano? Registre em "Desvios" no mesmo commit** (E-012).
12. **O primeiro commit de um repositório já tem `.gitattributes` com `* text=auto eol=lf`** (E-004).
13. **Antes de editar: `git status -sb` e `git pull --ff-only`** (E-020).
14. **Endereço público (usuário, domínio) em uma constante só,** com um teste que a confere (E-021).
15. **Depois de renomear conta ou repositório, teste o envio antes de prometê-lo** (E-022).
16. **Ao descrever o projeto, diga onde mora o dado real (em execução) e onde mora o fictício (repositório e testes)** (E-024).
17. **Verificação que procura a ausência de algo roda antes num caso que deve ser encontrado;** `git grep` só lê arquivo novo com `--untracked` (E-025).
18. **Script que gasta chamadas limitadas de uma API roda antes contra um dublê** (resposta inventada, sem rede) (E-029).

## 3. Quando registrar um erro

Registre no `ERROS.md` o erro que **pode se repetir**, que **custou mais de uns 15 minutos** ou que **chegou à pessoa,
ao repositório ou ao ar**. Deslize corrigido na hora (digitação, comando refeito em seguida) não entra. Registre **ao
fechar a tarefa**, no mesmo dia, sem interromper o trabalho; erro pequeno usa a entrada curta (modelo no `ERROS.md`).
Antes do primeiro commit em qualquer repositório: leia as regras de commit dele e confira `git config user.email` (E-034, E-035).
