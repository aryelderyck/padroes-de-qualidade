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
| Escrever código | `REVISAO.md`, bloco B (e o D, se houver rota, campo ou dado novo) |
| Otimizar ou refatorar | `REVISAO.md`, bloco C |
| Testar | `PADROES.md`, seção 4 · `REVISAO.md`, bloco E |
| Site que quer ser achado na busca | `PADROES.md`, seção 9A |
| Antes de dizer "pronto" | `REVISAO.md`, bloco F · `docs/CHECKLIST-PRONTO.md` do projeto |
| Apareceu um erro | `ERROS.md`: procure no índice ou por palavra e leia só a entrada. Nunca o arquivo inteiro |
| Ensinar um conceito | `CONTEXTO.md`, seção 6 (glossário) · `REVISAO.md`, bloco G |

O glossário e o registro de decisões do `CONTEXTO.md` são de consulta, não de leitura corrida.

## 2. Regras que saíram dos erros

1. **Verifique antes de afirmar ou de pedir algo à pessoa.** Sinal de ferramenta não é fato: tente a ação real (E-001).
2. **Documentação só descreve comportamento que foi executado.** Rode e leia a saída antes de escrever no README (E-003).
3. **Teste que passa de primeira merece mutação.** Quebre o código de propósito e veja o teste falhar (E-009, E-010).
4. **Olhe o resultado de verdade.** Capturas de tela encontram o que o código não mostra (E-007, E-008).
5. **Valide arquivos de configuração antes de subir** (YAML, JSON, TOML) e leia a primeira linha de diretivas (E-011, E-016).
6. **Declare o que não foi verificado.** Ferramenta bloqueada não é desculpa para omitir; é item de lista (E-005, E-013).
7. **Não contorne bloqueio de ambiente.** Se o acesso é negado, diga e adapte, ou peça o arquivo (E-005).
8. **Confira regras e limites oficiais antes de desenhar** o projeto em torno de uma API ou serviço (E-014).
9. **Pergunte o que anima a pessoa antes de propor o tema.** Em projeto de aprendizado, motivação é requisito (E-015).
10. **Não deixe entregas pela metade.** Esqueleto criado precisa ser preenchido ou o estado deve ser dito claramente (E-006).
11. **Mantenha plano e código alinhados.** Quando o código diverge do plano, registre o desvio (E-012).
12. **Finais de linha e formatação:** `.gitattributes` com LF desde o primeiro commit (E-004).
13. **Antes de editar, confira se o clone local está em dia** com o remoto (E-020).
14. **Endereço público em um só lugar,** com teste que o confere; URL absoluta espalhada quebra na mudança de nome (E-021).
15. **Autorização de ferramenta depende do nome do repositório.** Depois de renomear conta ou repositório, confirme o acesso antes de prometer o envio (E-022).
16. **Distinga dado real de dado fictício ao explicar o projeto:** o que o produto mostra em execução e o que o repositório guarda (E-024).
17. **Verificação que procura a ausência de algo precisa provar que olhou.** Rode-a antes num caso que deve ser encontrado; `git grep` não lê arquivo fora do git sem `--untracked` (E-025).
18. **Script que gasta chamadas limitadas de uma API roda antes contra um dublê** (resposta inventada, sem rede); só depois vai à API de verdade (E-029).

## 3. Quando registrar um erro

Registre no `ERROS.md` o erro que **pode se repetir**, que **custou mais de uns 15 minutos** ou que **chegou à pessoa,
ao repositório ou ao ar**. Deslize corrigido na hora (digitação, comando refeito em seguida) não entra. Registre **ao
fechar a tarefa**, no mesmo dia, sem interromper o trabalho; erro pequeno usa a entrada curta (modelo no `ERROS.md`).
Antes do primeiro commit em qualquer repositório: leia as regras de commit dele e confira `git config user.email` (E-034, E-035).
