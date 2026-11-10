# Catálogo de erros

Registro de **todo erro relevante** que aparece nos projetos, com a causa raiz e a regra que evita a repetição.
Erro registrado e esquecido vira erro repetido: por isso este arquivo é consultado **antes** de começar cada etapa.

> **Para Claude e Claude Code:** leia a seção "Regras que saíram dos erros" no início de cada projeto e de cada etapa.
> Ao encontrar um erro (seu, da ferramenta, do ambiente ou do processo), **registre-o aqui no mesmo dia**, antes de
> seguir. Não espere a pessoa pedir. Se o erro revelar uma regra, leve-a ao `PADROES.md` e anote o link na entrada.

## Como registrar

Copie o modelo abaixo para o fim da seção "Registro", com o próximo número (`E-NNN`). Seja específico e honesto,
sem culpar ninguém: o objetivo é aprender. Escreva a **causa raiz**, não só o sintoma.

```markdown
### E-NNN · [título curto]
- **Data / projeto:** AAAA-MM-DD · [projeto]
- **Categoria:** Processo | Ambiente | Ferramenta | Código | Teste | Segurança | Documentação | Comunicação
- **Sintoma:** o que se viu.
- **Causa raiz:** por que aconteceu de verdade.
- **Como foi detectado:** quem ou o que percebeu, e quando (ideal: antes de chegar à pessoa).
- **Correção:** o que foi feito.
- **Como evitar:** regra, teste ou item de checklist que impede a repetição.
- **Virou regra em:** seção do `PADROES.md` ou `templates/...`
- **Status:** Resolvido | Aberto
```

Categorias: **Processo** (jeito de trabalhar), **Ambiente** (rede, permissões, máquina), **Ferramenta** (comportamento de
uma ferramenta), **Código**, **Teste**, **Segurança**, **Documentação**, **Comunicação** (o que foi dito à pessoa).

## Regras que saíram dos erros (leia antes de começar)

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

## Índice

| ID | Título | Categoria | Projeto | Status |
| --- | --- | --- | --- | --- |
| E-001 | Aviso de "push recusado" lido como falta de permissão | Comunicação | repositórios antigos | Resolvido |
| E-002 | Otimização `-O2` gerou avisos do `scanf` | Ferramenta | repositórios antigos (C) | Resolvido |
| E-003 | README com afirmações não testadas | Documentação | repositórios antigos | Resolvido |
| E-004 | Arquivo com finais de linha misturados (CRLF e LF) | Ferramenta | estudos | Resolvido |
| E-005 | npm e pip bloqueados no ambiente | Ambiente | landing | Resolvido (com ressalvas) |
| E-006 | Claude Doc criado e deixado só com o esqueleto | Processo | portfólio (planejamento) | Aberto |
| E-007 | Tarja em bloco único e revelando para o lado errado | Código | landing | Resolvido |
| E-008 | Títulos de seção sem tamanho definido | Código | landing | Resolvido |
| E-009 | Teste de "sem rede" não percebeu a chamada barrada pelo CSP | Teste | landing | Resolvido |
| E-010 | Suíte toda verde na primeira rodada | Teste | landing | Resolvido |
| E-011 | YAML inválido por `:` sem aspas | Ferramenta | landing | Resolvido |
| E-012 | Código divergiu do plano (variáveis da luz) | Documentação | landing | Resolvido |
| E-013 | Ferramentas de verificação nunca executadas | Ambiente | landing | Aberto |
| E-014 | Chave de desenvolvimento da API impede produto público | Processo | painel (ideia Riot/OP.GG) | Resolvido |
| E-015 | Três rodadas de ideias sem perguntar o que animava a pessoa | Processo | escolha do 2º projeto | Resolvido |
| E-016 | Diretiva do Dockerfile fora da primeira linha | Código | kit de padrões | Resolvido |
| E-017 | Páginas oficiais de API que não renderizam para a ferramenta | Ferramenta | painel de Dota 2 | Aberto |
| E-018 | Inline `style=""` bloqueado pelo CSP | Segurança | landing | Resolvido |
| E-019 | Página de login sem acesso para o assistente (LinkedIn) | Ambiente | portfólio (planejamento) | Resolvido |
| E-020 | Clone local 53 commits atrás do remoto | Processo | landing | Resolvido |
| E-021 | Endereço com nome de usuário espalhado em vários arquivos | Código | landing | Resolvido |
| E-022 | Envio recusado depois da mudança do nome da conta | Ambiente | landing | Resolvido |
| E-023 | Leitura de página recusada por falta de origem (PROVENANCE_REQUIRED) | Ambiente | landing | Resolvido |
| E-024 | "Dados fictícios" dito sem separar produto de repositório | Comunicação | painel | Resolvido |
| E-025 | Verificação com `git grep` passaria sem olhar o arquivo novo | Processo | painel | Resolvido |
| E-026 | Primeira chamada à OpenDota caiu com "Connection was reset" | Ambiente | painel | Aberto |
| E-027 | Aspas internas somem ao passar JSON para outro `powershell.exe` | Ferramenta | painel | Resolvido |
| E-028 | Lista de um item só vira objeto no PowerShell e quebra o `+` | Código | painel | Resolvido |
| E-029 | `ConvertFrom-Json` do PowerShell 5.1 quebra com a chave `__type` | Ferramenta | painel | Resolvido |
| E-030 | Acentos trocados em script `.ps1` salvo sem BOM | Ferramenta | painel | Resolvido |
| E-031 | `git checkout-index -f -a` não aplicou o `eol=lf` novo | Ferramenta | kit de padrões | Resolvido |
| E-032 | Contagem de CR com `od` e `grep` contou a letra "r" | Teste | kit de padrões | Resolvido |

## Registro

### E-001 · Aviso de "push recusado" lido como falta de permissão
- **Data / projeto:** 2026-10 · repositórios antigos
- **Categoria:** Comunicação
- **Sintoma:** a ferramenta de anexar repositórios devolveu `push_check: "refused"`, e a pessoa foi orientada a instalar o GitHub App do Claude.
- **Causa raiz:** tratei o indicador da ferramenta como fato, sem tentar o `git push` real.
- **Como foi detectado:** o push de verdade funcionou, e o erro foi percebido pela diferença entre o aviso e o resultado.
- **Correção:** avisei a pessoa de que era falso alarme e que não precisava instalar nada.
- **Como evitar:** antes de pedir qualquer ação à pessoa (instalar, conceder acesso), tentar a operação real e só pedir se ela falhar.
- **Virou regra em:** `ERROS.md`, regra 1.
- **Status:** Resolvido

### E-002 · Otimização `-O2` gerou avisos do `scanf`
- **Data / projeto:** 2026-10 · repositórios antigos (C)
- **Categoria:** Ferramenta
- **Sintoma:** o Makefile com `-O2` mostrou `-Wunused-result` em chamadas de `scanf`.
- **Causa raiz:** com otimização, o compilador passa a avisar sobre o retorno ignorado do `scanf`; o código antigo nunca o verificava.
- **Como foi detectado:** compilando e lendo os avisos.
- **Correção:** o Makefile passou a usar `-g` sem `-O2`, e os READMEs documentam que o retorno do `scanf` não é checado.
- **Como evitar:** compilar com `-Wall -Wextra` e ler os avisos antes de commitar o Makefile; documentar limitações conhecidas em vez de escondê-las.
- **Virou regra em:** `PADROES.md`, seções 4 e 11.
- **Status:** Resolvido

### E-003 · README com afirmações não testadas
- **Data / projeto:** 2026-10 · repositórios antigos
- **Categoria:** Documentação
- **Sintoma:** READMEs descreviam comportamentos (entrada não numérica no Tetris, ordem de CSS, tabela de autenticação da API) sem que eu os tivesse executado.
- **Causa raiz:** escrevi a partir do que o código parecia fazer, não do que ele fazia.
- **Como foi detectado:** revisão antes de commitar; testei cada afirmação.
- **Correção:** o Tetris, na verdade, entrava em laço infinito com entrada não numérica; `utilities.css` era carregado pela home e pelo cadastro, não pelo login; `/api/logout` não exige autenticação; `/api/session` devolve 401; Noto Serif era importada e não usada; não havia `@media` nem viewport. O README foi corrigido.
- **Como evitar:** toda afirmação de comportamento no README precisa de um comando executado ou de uma leitura do código citada.
- **Virou regra em:** `ERROS.md`, regra 2; `PADROES.md`, seção 11.
- **Status:** Resolvido

### E-004 · Arquivo com finais de linha misturados (CRLF e LF)
- **Data / projeto:** 2026-10 · estudos
- **Categoria:** Ferramenta
- **Sintoma:** correções com `sed` no `index.html` não surtiam efeito.
- **Causa raiz:** o arquivo tinha CRLF e LF misturados, e os padrões do `sed` não casavam com as linhas de fim `\r\n`.
- **Como foi detectado:** a substituição falhou em silêncio e a conferência mostrou o texto antigo.
- **Correção:** um commit só para normalizar para LF, depois outro com as correções de conteúdo; marcação das tags balanceadas e dos ids únicos.
- **Como evitar:** `.gitattributes` com `* text=auto eol=lf` desde o primeiro commit; separar commits de formatação e de conteúdo.
- **Virou regra em:** `PADROES.md`, seção 3.
- **Status:** Resolvido

### E-005 · npm e pip bloqueados no ambiente
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Ambiente
- **Sintoma:** `npm` falhou com 403 e DNS, `pip` não achou distribuições; não foi possível instalar fontes, axe, html-validate, `@playwright/test` nem `http-server`.
- **Causa raiz:** a rede do ambiente só libera uma lista de destinos; os registros de pacotes não estavam nela.
- **Como foi detectado:** a primeira instalação falhou.
- **Correção:** não contornei o bloqueio. Disse à pessoa, troquei o servidor por um sem dependências, usei o `playwright` já instalado no ambiente e escrevi os arquivos de fontes, axe e Lighthouse sem executá-los, listando-os como não verificados.
- **Como evitar:** na primeira tarefa, testar `npm ping` e `pip download`; se bloqueados, planejar a versão sem dependências e a lista de pendências para o Claude Code rodar na máquina da pessoa.
- **Virou regra em:** `ERROS.md`, regras 6 e 7.
- **Status:** Resolvido (com ressalvas: ver E-013)

### E-006 · Claude Doc criado e deixado só com o esqueleto
- **Data / projeto:** 2026-10 · portfólio (planejamento)
- **Categoria:** Processo
- **Sintoma:** o documento pedido foi criado com título e seções pendentes, mas o turno terminou antes de preenchê-lo.
- **Causa raiz:** criei o esqueleto primeiro, como manda a regra de documentos, mas não fechei o trabalho no mesmo turno.
- **Como foi detectado:** ao revisar o que havia sido entregue; avisei a pessoa e ofereci preencher.
- **Correção:** ainda não preenchido.
- **Como evitar:** criar o esqueleto só quando for preencher no mesmo turno; se não der, dizer no fim do turno o estado do documento e o que falta.
- **Virou regra em:** `ERROS.md`, regra 10.
- **Status:** Aberto (https://claude.ai/artifact/KQQYSvUUezmAvBRgmriA4U)

### E-007 · Tarja em bloco único e revelando para o lado errado
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Código
- **Sintoma:** na captura de tela, a tarja do título era um retângulo preto pesado com contorno, e se recolhia para a esquerda, mostrando o fim da frase primeiro.
- **Causa raiz:** `::after` com `transform-origin: left` cobrindo o bloco inteiro; nada no teste exigia a aparência.
- **Como foi detectado:** olhando as capturas de tela do estado intermediário da animação.
- **Correção:** faixas por linha com `repeating-linear-gradient` e `1lh`, sem contorno, recolhendo para a direita (revela na ordem de leitura).
- **Como evitar:** fotografar também o **meio** da animação, não só o início e o fim.
- **Virou regra em:** `ERROS.md`, regra 4; `PADROES.md`, seção 9.
- **Status:** Resolvido

### E-008 · Títulos de seção sem tamanho definido
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Código
- **Sintoma:** os `h2` ficaram pequenos demais, justamente onde as tarjas aparecem.
- **Causa raiz:** defini a família e o peso da fonte, mas não o tamanho; valeu o padrão do navegador.
- **Como foi detectado:** captura de tela da página inteira.
- **Correção:** `.secao h2` com `--texto-6`.
- **Como evitar:** definir tamanho, peso e espaçamento de cada nível de título no mesmo lugar; revisar a página inteira em captura antes de dar por pronto.
- **Virou regra em:** `ERROS.md`, regra 4.
- **Status:** Resolvido

### E-009 · Teste de "sem rede" não percebeu a chamada barrada pelo CSP
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Teste
- **Sintoma:** ao inserir de propósito um `fetch` para um domínio externo no envio do formulário, o teste "não faz requisição de rede" continuou verde.
- **Causa raiz:** o CSP barrou a chamada antes de virar requisição, então o evento `request` nunca disparou. A defesa funcionou, mas o teste não enxergava a tentativa.
- **Como foi detectado:** teste de mutação (quebrar o código de propósito).
- **Correção:** o teste passou a observar também as violações de CSP no console.
- **Como evitar:** em testes de "não deve fazer X", verificar a tentativa e a camada de bloqueio, não só o efeito final.
- **Virou regra em:** `ERROS.md`, regra 3; `PADROES.md`, seções 4 e 13.
- **Status:** Resolvido

### E-010 · Suíte toda verde na primeira rodada
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Teste
- **Sintoma:** 25 testes unitários e 21 E2E passaram de primeira, sem nenhuma falha prévia.
- **Causa raiz:** testes escritos depois do código (no E2E) não provam que conseguem falhar.
- **Como foi detectado:** desconfiança deliberada; fiz três mutações (tarja que não abre, tarja que fecha de novo, formulário que envia dados).
- **Correção:** a suíte pegou duas; a terceira revelou E-009.
- **Como evitar:** mutação manual em pelo menos três pontos críticos antes de dar a suíte por confiável.
- **Virou regra em:** `PADROES.md`, seção 4; `templates/CHECKLIST-PRONTO.md`.
- **Status:** Resolvido

### E-011 · YAML inválido por `:` sem aspas
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Ferramenta
- **Sintoma:** o `lighthouse.yml` falhou ao ser lido (`mapping values are not allowed here`).
- **Causa raiz:** o `name:` de um passo continha `:` ("metas: Desempenho...") sem aspas.
- **Como foi detectado:** validação do YAML com Python antes do commit.
- **Correção:** o texto do `name` foi colocado entre aspas.
- **Como evitar:** validar todo YAML antes de subir, e usar aspas em textos livres com `:`.
- **Virou regra em:** `PADROES.md`, seção 5.
- **Status:** Resolvido

### E-012 · Código divergiu do plano (variáveis da luz)
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Documentação
- **Sintoma:** a especificação falava em `--x`/`--y`; o código usa `--lx`/`--ly`.
- **Causa raiz:** as propriedades precisaram ser registradas com `@property` para animar a luz no toque, e escolhi nomes mais específicos sem atualizar a especificação na hora.
- **Como foi detectado:** conferindo o plano contra o código ao fechar a implementação.
- **Correção:** seção "Desvios" no plano com a lista de diferenças.
- **Como evitar:** toda divergência entre o plano e o código entra em "Desvios" no mesmo commit.
- **Virou regra em:** `ERROS.md`, regra 11; `PADROES.md`, seção 3.
- **Status:** Resolvido

### E-013 · Ferramentas de verificação nunca executadas
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Ambiente
- **Sintoma:** `axe`, `html-validate`, Lighthouse, as fontes reais e o CI no GitHub nunca rodaram; a tipografia (Bodoni Moda e Hanken Grotesk) nunca foi vista.
- **Causa raiz:** consequência de E-005.
- **Como foi detectado:** ao montar a lista de pendências.
- **Correção:** a lista foi registrada no plano e no prompt do Claude Code, que deve executar tudo na máquina da pessoa.
- **Como evitar:** ver E-005; fechar o projeto só quando cada item da checklist tiver evidência.
- **Virou regra em:** `templates/CHECKLIST-PRONTO.md`.
- **Status:** Aberto (depende de a pessoa rodar a etapa 1 do prompt)

### E-014 · Chave de desenvolvimento da API impede produto público
- **Data / projeto:** 2026-11-03 · painel (ideia estilo OP.GG com a API da Riot)
- **Categoria:** Processo
- **Sintoma:** a ideia previa um site público com dados ao vivo, mas as regras da Riot proíbem manter produto público com chave de desenvolvimento (que expira em 24 horas) ou pessoal.
- **Causa raiz:** a ideia partiu da popularidade do OP.GG, antes de ler as regras da API.
- **Como foi detectado:** li a documentação oficial antes de propor o desenho.
- **Correção:** apresentei a limitação e a alternativa (demonstração com dados fictícios, ou trocar para uma API aberta); a pessoa escolheu o Dota 2.
- **Como evitar:** antes de desenhar em torno de uma API, ler limites, chaves, termos e atribuição.
- **Virou regra em:** `ERROS.md`, regra 8; `PADROES.md`, seção 8.
- **Status:** Resolvido

### E-015 · Três rodadas de ideias sem perguntar o que animava a pessoa
- **Data / projeto:** 2026-11-03 · escolha do segundo projeto
- **Categoria:** Processo
- **Sintoma:** o radar de licitações foi recusado ("não fiquei animado"), e as duas listas seguintes também.
- **Causa raiz:** propus temas pelo valor para o mercado, sem perguntar o que a pessoa usa e gosta. Em projeto de aprendizado, a motivação decide se o projeto termina.
- **Como foi detectado:** a recusa repetida da pessoa.
- **Correção:** parei de propor, perguntei o que ela usa; a resposta (OP.GG) levou ao painel de Dota 2.
- **Como evitar:** começar a escolha de tema perguntando "quais apps você usa e o que te incomoda", e só depois propor.
- **Virou regra em:** `ERROS.md`, regra 9; `PADROES.md`, seção 11.
- **Status:** Resolvido

### E-016 · Diretiva do Dockerfile fora da primeira linha
- **Data / projeto:** 2026-11-09 · kit de padrões
- **Categoria:** Código
- **Sintoma:** o modelo de Dockerfile tinha um comentário antes de `# syntax=docker/dockerfile:1`.
- **Causa raiz:** a diretiva só vale se for a **primeira linha**; escrevi o comentário explicativo antes dela.
- **Como foi detectado:** conferindo o arquivo ao validar o kit.
- **Correção:** a diretiva passou para a primeira linha.
- **Como evitar:** em arquivos com diretivas (Dockerfile, shebang, `# -*- coding`), ler a primeira linha depois de editar.
- **Virou regra em:** `ERROS.md`, regra 5.
- **Status:** Resolvido

### E-017 · Páginas oficiais de API que não renderizam para a ferramenta
- **Data / projeto:** 2026-11-01 e 2026-11-03 · painel de Dota 2 (e pesquisa do PNCP)
- **Categoria:** Ferramenta
- **Sintoma:** a leitura das páginas oficiais da OpenDota e do PNCP (Swagger UI, documentação em página dinâmica) devolveu só o título; uma página redirecionou de HTTPS para HTTP e não foi seguida.
- **Causa raiz:** essas páginas carregam o conteúdo por JavaScript, e a ferramenta de leitura só vê o HTML estático.
- **Como foi detectado:** a resposta vazia.
- **Correção:** usei a documentação de bibliotecas de terceiros como fonte, dizendo que **não era oficial** e que os limites precisam ser confirmados.
- **Como evitar:** marcar como "não confirmado" tudo que veio de fonte indireta; incluir "confirmar limites e termos na documentação oficial" como primeira tarefa do projeto.
- **Virou regra em:** `ERROS.md`, regras 6 e 8.
- **Status:** Aberto (confirmar na etapa 1 do painel, com acesso à internet)

### E-018 · Inline `style=""` bloqueado pelo CSP
- **Data / projeto:** 2026-10-27 · landing
- **Categoria:** Segurança
- **Sintoma:** o HTML do documento decorativo usava `style="--l: 92%"`, que a política `default-src 'self'` bloquearia.
- **Causa raiz:** `default-src 'self'` também proíbe atributos `style` e scripts inline; escrevi o HTML por hábito.
- **Como foi detectado:** revisão do HTML contra o CSP antes de abrir a página no navegador.
- **Correção:** larguras passaram para regras `nth-child` no CSS; o marcador `js` virou um arquivo externo (`marca-js.js`).
- **Como evitar:** com CSP restritivo, procurar `style=` e `<script>` sem `src` no HTML antes de testar; o teste de erros do console cobre o resto.
- **Virou regra em:** `PADROES.md`, seção 13 (CSP); `CLAUDE.md` da landing.
- **Status:** Resolvido

### E-019 · Página de login sem acesso para o assistente (LinkedIn)
- **Data / projeto:** 2026-10 · portfólio (planejamento)
- **Categoria:** Ambiente
- **Sintoma:** a leitura do perfil do LinkedIn falhou por exigir login; a busca devolveu perfis de outras pessoas.
- **Causa raiz:** a página exige autenticação, e ferramenta de leitura não faz login.
- **Como foi detectado:** a leitura retornou erro, e os resultados da busca não batiam com o perfil.
- **Correção:** descartei os perfis errados e pedi à pessoa que colasse o texto do próprio perfil.
- **Como evitar:** para páginas autenticadas, pedir o conteúdo colado em vez de tentar contornar ou adivinhar por busca.
- **Virou regra em:** `ERROS.md`, regra 7.
- **Status:** Resolvido

### E-020 · Clone local 53 commits atrás do remoto
- **Data / projeto:** 2026-11-10 · landing
- **Categoria:** Processo
- **Sintoma:** o clone usado pelo assistente estava em um commit antigo; o Claude Code já tinha avançado o projeto.
- **Causa raiz:** o clone foi feito em outra sessão e não foi atualizado antes de começar a editar.
- **Como foi detectado:** `git status -sb` mostrou "behind 53" antes de qualquer edição.
- **Correção:** `git pull --ff-only` e só depois as edições.
- **Como evitar:** primeiro passo de toda sessão em repositório existente: `git fetch` e `git status -sb`.
- **Virou regra em:** `ERROS.md`, regra 13.
- **Status:** Resolvido

### E-021 · Endereço com nome de usuário espalhado em vários arquivos
- **Data / projeto:** 2026-11-10 · landing
- **Categoria:** Código
- **Sintoma:** depois que a conta do GitHub mudou de nome, o endereço antigo continuava em `og:url`, `og:image`, no rodapé, no README, no selo do CI e em uma constante de teste.
- **Causa raiz:** o endereço público foi escrito à mão em vários lugares. O GitHub Pages usa o nome da conta no endereço e não redireciona o endereço antigo.
- **Como foi detectado:** busca por texto do nome antigo em todo o repositório logo após a renomeação.
- **Correção:** substituição em 4 arquivos, testes unitários rodados (40 de 40) e commit.
- **Como evitar:** guardar o endereço público em um único lugar (constante ou variável de build) e ter um teste que compara os demais com ele. Depois de renomear, buscar o nome antigo no repositório inteiro.
- **Virou regra em:** `ERROS.md`, regra 14; candidata em `PRATICAS.md`.
- **Status:** Resolvido

### E-022 · Envio recusado depois da mudança do nome da conta
- **Data / projeto:** 2026-11-10 · landing
- **Categoria:** Ambiente
- **Sintoma:** o envio para o endereço novo foi recusado ("não está no conjunto autorizado"), e adicionar o repositório sob o nome novo falhou por haver outro de mesmo nome já anexado.
- **Causa raiz:** a autorização da sessão ficou registrada com o nome antigo da conta; o GitHub redireciona o nome antigo para o novo, mas a ferramenta confere o nome.
- **Como foi detectado:** a mensagem de erro do envio.
- **Correção:** envio pelo endereço antigo, que a sessão autorizava e o GitHub redirecionou para o repositório certo. Em outro caso, iniciar nova sessão com o repositório pelo nome novo.
- **Como evitar:** depois de renomear conta ou repositório, avisar no começo da sessão e confirmar o acesso antes de prometer um envio.
- **Virou regra em:** `ERROS.md`, regra 15.
- **Status:** Resolvido

### E-023 · Leitura de página recusada por falta de origem (PROVENANCE_REQUIRED)
- **Data / projeto:** 2026-11-10 · landing
- **Categoria:** Ambiente
- **Sintoma:** a leitura do endereço novo do GitHub Pages foi recusada, então não foi possível confirmar que a página está no ar.
- **Causa raiz:** a ferramenta só abre endereços que a pessoa escreveu na conversa ou que apareceram em resultados anteriores; o endereço foi montado por mim.
- **Como foi detectado:** retorno `PROVENANCE_REQUIRED`.
- **Correção:** pedir que a pessoa cole o endereço na conversa; enquanto isso, a publicação fica marcada como não verificada.
- **Como evitar:** pedir o endereço à pessoa quando precisar verificar uma publicação nova; não afirmar que está no ar sem ter aberto.
- **Virou regra em:** `ERROS.md`, regras 1 e 6.
- **Status:** Resolvido

### E-024 · "Dados fictícios" dito sem separar produto de repositório
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Comunicação
- **Sintoma:** a pessoa entendeu que o painel usaria dados inventados, quando quer estatísticas reais de partidas.
- **Causa raiz:** a regra "só dados fictícios em repositório público" (LGPD) foi explicada sem dizer que vale para o repositório e os testes, não para o que o site mostra em execução.
- **Como foi detectado:** a pessoa corrigiu na mensagem seguinte.
- **Correção:** explicação refeita com duas colunas: em execução, dados reais da API; no repositório e nos testes, só fictícios.
- **Como evitar:** ao falar de dados, dizer sempre onde ficam (produto, banco, repositório, testes) e de onde vêm.
- **Virou regra em:** `ERROS.md`, regra 16.
- **Status:** Resolvido

### E-025 · Verificação com `git grep` passaria sem olhar o arquivo novo
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Processo
- **Sintoma:** o passo 5 da tarefa 1 do plano 1 manda conferir `git grep -nE "[0-9]{8,}" docs/api-fontes.md` antes do commit. O arquivo é novo e ainda não está no git, então o comando não devolve nada e a verificação "passa" sem ter lido o arquivo.
- **Causa raiz:** `git grep` só procura em arquivos rastreados pelo git; arquivo novo exige `--untracked` (ou `git add` antes). A verificação foi escrita sem ser executada contra um caso que deveria ser encontrado.
- **Como foi detectado:** Claude Code, antes de usar o passo: criou um arquivo de teste fora do git com um número fictício de 9 dígitos; `git grep` saiu com código 1 (nada achado) e `git grep --untracked` achou a linha.
- **Correção:** com a aprovação da pessoa, o passo 5 do plano passou a usar `git grep --untracked` e a exigir um ensaio com número fictício antes da verificação real.
- **Como evitar:** regra 17. Toda verificação de "não tem X" roda primeiro contra um exemplo que tem X. Observação: ID de conta do Dota pode ter menos de 8 dígitos (contas antigas), então o padrão `{8,}` também não pega todos os IDs; ele é uma rede, não uma prova.
- **Virou regra em:** `ERROS.md`, regra 17.
- **Status:** Resolvido

### E-026 · Primeira chamada à OpenDota caiu com "Connection was reset"
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Ambiente
- **Sintoma:** a primeira execução de `curl.exe -i https://api.opendota.com/api/constants/patch` na máquina da pessoa falhou com "Connection was reset"; a segunda, logo depois, devolveu 200. No mesmo dia, Claude Code repetiu o padrão na mesma máquina: para obter 13 respostas (curl e navegador) houve cerca de 14 tentativas que caíram antes da resposta; todas as chamadas acabaram respondendo depois de repetir. Aconteceu também com `www.dota2.com`; `api.github.com` respondeu na primeira. O curl mostra a queda durante o aperto de mãos TLS (erro 35), antes de qualquer código HTTP, e, pelo contador `X-Rate-Limit-Remaining-Day`, as tentativas que caíram não foram descontadas do saldo (inferência, não regra documentada).
- **Causa raiz:** não confirmada. Como cai antes do HTTP e afeta dois domínios diferentes, limite de requisições da OpenDota (que responderia 429) fica improvável. Hipóteses não verificadas: rede local, antivírus ou firewall inspecionando HTTPS, ou o provedor de internet. Teste que separaria as causas: repetir em outra rede (por exemplo, o roteador do celular).
- **Como foi detectado:** a pessoa, ao rodar o passo 1 da tarefa 1.
- **Correção:** nova tentativa manual.
- **Como evitar:** o cliente da fonte (plano 2) trata conexão encerrada como falha temporária, com nova tentativa e espera crescente (especificação, seção 5), e tem teste para isso. Se voltar a acontecer, anotar hora, rede e mensagem completa para comparar.
- **Virou regra em:** ainda não (aguarda repetição para ter causa).
- **Status:** Aberto

### E-027 · Aspas internas somem ao passar JSON para outro `powershell.exe`
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Ferramenta
- **Sintoma:** `powershell -File script.ps1 -JsonDeTeste '{"a":{"b":1}}'` falhou com "JSON primitivo inválido"; o script recebeu o texto sem as aspas duplas.
- **Causa raiz:** o Windows PowerShell 5.1, ao chamar um programa externo (inclusive outro `powershell.exe`), não escapa as aspas duplas de dentro do argumento, e elas se perdem na linha de comando.
- **Como foi detectado:** Claude Code, no ensaio sem rede do script que lista os campos do jogador.
- **Correção:** rodar o script na mesma sessão (`& $script -JsonDeTeste '...'`), sem criar outro processo.
- **Como evitar:** no PowerShell 5.1, passar JSON a outro processo por arquivo, não por argumento; ou chamar o script com `&` na mesma sessão.
- **Virou regra em:** ainda não (registro de ferramenta).
- **Status:** Resolvido

### E-028 · Lista de um item só vira objeto no PowerShell e quebra o `+`
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Código
- **Sintoma:** no script de verificação do STRATZ, `($lista | Select-Object -First 5) + ($lista | Select-Object -Last 5)` falha com "não contém um método denominado 'op_Addition'" quando a lista tem 1 item.
- **Causa raiz:** o PowerShell "desembrulha" o resultado de um pipeline com um item só: devolve o objeto, não uma lista, e objeto não sabe somar. Escrevi pensando só no caso de muitos itens.
- **Como foi detectado:** Claude Code, ao revisar o script linha a linha para explicar à pessoa, antes de ela rodar; reproduzido com uma lista fictícia de 1 item.
- **Correção:** `@(...)` em volta de cada parte, que força lista; com até 10 itens, mostra a lista inteira.
- **Como evitar:** no PowerShell, envolver em `@(...)` todo resultado de pipeline que será somado, contado ou indexado; testar com 0, 1 e muitos itens (`PADROES.md`, seção 4, casos de borda).
- **Virou regra em:** `PADROES.md`, seção 4 (casos de borda), já existente.
- **Status:** Resolvido

### E-029 · `ConvertFrom-Json` do PowerShell 5.1 quebra com a chave `__type`
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Ferramenta
- **Sintoma:** no teste sem rede do script do STRATZ, toda consulta de introspecção "falhava 4 vezes", e o arquivo saía só com "sem resposta". Erro escondido: "Nenhum construtor sem parâmetros foi definido para o tipo de 'System.String'".
- **Causa raiz:** o `ConvertFrom-Json` do Windows PowerShell 5.1 usa o `JavaScriptSerializer` do .NET, que trata a chave `__type` como instrução interna de tipo, e não como dado. A introspecção do GraphQL devolve exatamente `"__type": {...}`. O `catch` do script engolia a exceção e repetia a chamada.
- **Como foi detectado:** Claude Code, com um dublê de `Invoke-WebRequest` que devolvia um esquema inventado, antes de a pessoa rodar com o token real. Hipótese confirmada isolando `'{"__type":{}}' | ConvertFrom-Json` (quebra) contra a chave `tipo` (funciona). Sem o dublê, a rodada real teria gastado cerca de 100 chamadas sem resultado.
- **Correção:** apelido do GraphQL na consulta (`tipo: __type(...)`), e a resposta volta com a chave `tipo`; o dublê passou a respeitar apelidos, como um servidor de verdade.
- **Como evitar:** regra 18. No PowerShell 5.1, evitar chaves `__type` em JSON lido com `ConvertFrom-Json`; e `catch` que repete deve, ao desistir, mostrar o motivo da última falha.
- **Virou regra em:** `ERROS.md`, regra 18.
- **Status:** Resolvido

### E-030 · Acentos trocados em script `.ps1` salvo sem BOM
- **Data / projeto:** 2026-11-10 · painel
- **Categoria:** Ferramenta
- **Sintoma:** o texto "até", gravado pelo script do STRATZ, saiu como "atÃ©"; a pergunta do script do jogador também teria saído trocada.
- **Causa raiz:** o Windows PowerShell 5.1 lê arquivo `.ps1` em UTF-8 sem BOM (a marca de 3 bytes `EF BB BF` no começo) como se fosse Windows-1252. Os scripts foram criados em UTF-8 sem BOM.
- **Como foi detectado:** Claude Code, lendo o arquivo gerado pelo teste com dublê; os 3 primeiros bytes dos scripts confirmaram a falta da marca.
- **Correção:** os scripts foram regravados em UTF-8 com BOM, e o teste mostrou "até" correto.
- **Como evitar:** script `.ps1` com acentos para o PowerShell 5.1 vai em UTF-8 **com** BOM; conferir com os 3 primeiros bytes. Quando o projeto tiver `.editorconfig`, fixar isso lá para `*.ps1`.
- **Virou regra em:** ainda não (registro de ferramenta).
- **Status:** Resolvido

### E-031 · `git checkout-index -f -a` não aplicou o `eol=lf` novo
- **Data / projeto:** 2026-11-10 · kit de padrões
- **Categoria:** Ferramenta
- **Sintoma:** depois do commit do `.gitattributes` (`* text=auto eol=lf`), `git checkout-index -f -a` terminou sem erro, mas 17 arquivos continuaram em CRLF na pasta (`git ls-files --eol` mostrava `w/crlf` com `attr/text=auto eol=lf`).
- **Causa raiz:** não confirmada. O comando não regravou os arquivos, embora os atributos estivessem certos (`git check-attr`). Hipótese: o git considera o arquivo em dia pelo registro de data e tamanho e não o reescreve.
- **Como foi detectado:** Claude Code, conferindo `git ls-files --eol` depois do comando, em vez de presumir que funcionou.
- **Correção:** com a pasta limpa (`git status --porcelain` vazio), apagar os arquivos rastreados e restaurar do git: `git ls-files -z | xargs -0 rm -f && git checkout -- .`. Resultado: 20 de 20 em LF, sem nenhum byte CR, e `git status` vazio.
- **Como evitar:** depois de criar ou mudar o `.gitattributes`, usar o apagar-e-restaurar (só com a pasta limpa) e conferir com `git ls-files --eol`. Vale para o painel na tarefa 2.
- **Virou regra em:** ainda não (registro de ferramenta).
- **Status:** Resolvido

### E-032 · Contagem de CR com `od` e `grep` contou a letra "r"
- **Data / projeto:** 2026-11-10 · kit de padrões
- **Categoria:** Teste
- **Sintoma:** `head -c 200 README.md | od -c | grep -c '\\r'` (no Git Bash) deu 7 num arquivo que já estava em LF.
- **Causa raiz:** o padrão chegou ao `grep` como `\r`, que o GNU grep trata como a letra "r", e não como o byte CR; a saída do `od` tem letras "r" do texto, e o comando contou linhas com elas. Por que as duas barras viraram uma não foi investigado. Usei a medição sem antes testá-la num caso conhecido (regra 17).
- **Como foi detectado:** Claude Code, ao perceber que a contagem não batia com `git ls-files --eol` (`w/lf`).
- **Correção:** contar os bytes CR com Python (`open(f, "rb").read().count(b"")`), que deu 201 num arquivo ainda em CRLF (controle positivo) e 0 no arquivo restaurado.
- **Como evitar:** regra 17: toda medição de "não tem X" roda antes num caso que tem X.
- **Virou regra em:** `ERROS.md`, regra 17 (já existente).
- **Status:** Resolvido
