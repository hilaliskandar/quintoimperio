# Roteiro de produção

## Estado consolidado

O projeto possui três baselines já integrados e uma primeira tranche funcional de P3 também integrada ao `main`:

- MVP Lisboa–Calecute: `f308fb0e97687e34365fd23ed257a0114fd81613`;
- P1 retorno até BRG: `47fb82baad1289077c048576f3bc52815d6b192f`;
- P2 Cochim mínimo: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`;
- P3-func-A: merge do PR #117 em `1011507d5dd1332585b01cfd90351395952bb5f1`;
- CI pós-P3-func-A: run `34160737955` — integralmente verde.

O objetivo de produção passa a ser explícito: **concluir e estabilizar em Python o domínio necessário para representar 1497–1505 antes de migrar o runtime de produção para Godot**.

O Python permanece, até esse gate, como laboratório de domínio, implementação de referência, ambiente de pesquisa histórica, diagnóstico e playtest sintético. Pygame continua apenas como interface suficiente para validação e smoke tests; não deve receber investimento de produção que será descartado na migração.

Princípio permanente: **dados históricos e parâmetros de simulação permanecem separados; fatos históricos não são recalibrados para resolver jogabilidade**.

## Método de execução

A partir de P3, cada tranche histórica segue obrigatoriamente:

`documentação suficiente → normalização mínima → implementação → testes/CI → playtest/diagnóstico → fechamento → próxima tranche`.

Não se deve acumular vários anos de especificação sem feedback do domínio, nem criar uma mecânica geral antes de um caso histórico demonstrar sua necessidade.

## Baselines concluídos

### M0–M8 — MVP Lisboa–Calecute

**Status: CONCLUÍDO.**

Fluxo canônico:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`.

A vertical slice permanece o baseline canônico de regressão.

### P1 — Retorno da primeira viagem

**Status: CONCLUÍDO.**

Fluxo estabilizado:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`.

O retorno é opt-in e preserva o encerramento canônico do MVP em Calecute.

### P2 — Cochim e primeiros apoios portugueses no Malabar

**Status: CONCLUÍDO.**

Cochim foi integrado minimamente como porto soberano local, com pimenta, autoridade institucional, comunidades mercantis documentadas e rota costeira preexistente `CAL→COC`, sem fortificação ou posse portuguesa retroativas.

### P3-func-A — primeira tranche 1500–1503

**Status: INTEGRADA AO MAIN.**

Resultados já incorporados:

- `VCR` e `CAN`;
- `expedition_events.csv` / `ExpeditionEventModel`;
- `node_state_events.csv` / `NodeStateEventModel`;
- campanha guiada de Cabral até Cananor;
- ruptura temporal de Calecute e presença inicial em Cochim/Cananor;
- ações documentais específicas de logística em Vera Cruz, Moçambique e Melinde;
- teto logístico específico de Cabral preservando o teto genérico do MVP;
- wave20 com dez arquétipos fixos + `RANDOM_PER_LEG`;
- seeds sentinela e diagnóstico qualitativo;
- início de `JoaoNovaCampaignModel` com aquisição tardia do aviso de Cabral em São Brás.

Baseline integrado: `1011507d5dd1332585b01cfd90351395952bb5f1`.

## Gate-mãe atual — P3-1505

Issue #118 — **Fechar domínio Python 1497–1505 e preparar freeze para Godot**.

A #110 continua como guarda-chuva documental de 1500–1505. Os subgates #111–#114 estão concluídos; #115 permanece aberto para 1504.

## F1 — João da Nova 1501–1502

**Status: PRÓXIMO GATE FUNCIONAL.**

Objetivos:

1. completar somente as pernas e âncoras temporais documentalmente sustentáveis;
2. manter a partida em Lisboa sem conhecimento do desfecho de Cabral no Malabar;
3. aplicar a aquisição de informação em São Brás como evento próprio da expedição;
4. integrar Cananor/Cochim e a presença institucional correspondente;
5. preservar Ceilão fora da rota enquanto a evidência permanecer insuficiente;
6. representar confronto específico sem combate geral, salvo necessidade demonstrada;
7. testar save/load, cronologia e informação sem vazamento retrospectivo;
8. CI integral e smoke da campanha antes do fechamento.

Critério de verde de F1: campanha representável até seu limite documental, informação correta por data/local e regressão integral contra MVP/P1/P2/P3-func-A.

## F2 — Vasco da Gama 1502–1503

Objetivos:

1. integrar `EXP_GAMA_1502`;
2. normalizar apenas as rotas e escalas necessárias;
3. aplicar reorganização de Cochim e Cananor por estados temporais;
4. representar mudanças de feitor/presença sem alterar soberania local;
5. representar Vicente Sodré como subcampanha/força residente se o schema atual bastar;
6. distinguir missão institucional de decisão operacional;
7. manter Mîrî, bloqueio e bombardeio como eventos específicos enquanto não houver necessidade de combate geral;
8. testar persistência de efeitos mundiais após separação da força residente.

Critério de verde de F2: Gama 1502 e Sodré representáveis sem lacuna arquitetural bloqueante, save/load íntegro e regressão completa.

## F3 — Ciclo de 1503 em Cochim

Objetivos:

1. integrar crise e retirada para Vaipim como eventos/estados históricos;
2. restaurar Cochim no momento documentado;
3. materializar fortificação e guarnição com temporalidade;
4. preservar soberania do rajá;
5. manter Vaipim fora do grafo jogável salvo necessidade operacional demonstrada;
6. testar persistência de feitoria, fortificação, guarnição, acesso e relação como dimensões distintas;
7. provar que estados de 1503 não contaminam campanhas anteriores.

Critério de verde de F3: transições de Cochim reproduzíveis por data, sem anacronismo e com regressão integral.

## F4 — Lopo Soares 1504

Issue documental atual: #115.

Objetivos:

1. concluir cronologia, comando e composição de 1504;
2. reconstruir as ofensivas contra Cochim e a defesa sob Duarte Pacheco Pereira;
3. carregar corretamente fortificação, guarnição, aliança e soberania herdadas de 1503;
4. decidir formalmente entre `eventos guiados` e `combate funcional mínimo`;
5. incorporar Coulão e outros nós somente se indispensáveis ao loop;
6. representar a transição de comando/presença após o ciclo defensivo;
7. implementar a tranche mínima;
8. executar playtests sintéticos específicos se surgirem decisões novas de agência/risco.

Critério de verde de F4: 1504 representável sem lacuna militar/institucional bloqueante e decisão de arquitetura sobre combate formalmente encerrada.

## F5 — Francisco de Almeida 1505

**Status: gate documental ainda não aberto.**

Objetivos documentais:

1. reconstruir armada, comando, itinerário, escalas e objetivos de 1505;
2. identificar mudanças institucionais necessárias ao loop;
3. documentar fortificações, guarnições, forças residentes, relações e novos nós somente quando sustentados e necessários;
4. distinguir continuidade de estados 1503–1504 de mudanças efetivas em 1505;
5. avaliar se o horizonte 1505 exige generalização de governo/autoridade, frota, força residente ou combate;
6. produzir proposta mínima de normalização antes de implementação.

Objetivos funcionais:

1. implementar apenas os estados/campanhas necessários ao horizonte 1505;
2. preservar decisões metodológicas anteriores;
3. validar persistência e transição entre campanhas;
4. executar smoke, playtests e regressão completa.

Critério de verde de F5: o estado do mundo e as campanhas necessárias em 1505 são reproduzíveis sem lacuna arquitetural bloqueante.

## Gates transversais obrigatórios

### T1 — Estado mundial temporal

Consolidar `node_state_events` e `expedition_events` como contratos estáveis para:

- soberania;
- acesso;
- relação;
- presença institucional;
- feitoria;
- fortificação;
- guarnição;
- eventos de expedição e aquisição de informação.

Nenhuma transição posterior pode existir retroativamente em campanhas anteriores.

### T2 — Expedições, subcampanhas e forças residentes

- verificar até 1505 se `active_expedition_id` + subcampanhas continuam suficientes;
- generalizar múltiplas forças simultâneas somente se os casos de 1502–1505 demonstrarem necessidade;
- garantir efeitos persistentes de forças não controladas pelo jogador.

### T3 — Informação e latência

- manter separados estado objetivo/local, conhecimento da Coroa e conhecimento da expedição;
- impedir vazamento retrospectivo;
- criar mensagens/cartas persistentes somente se os casos até 1505 realmente exigirem.

### T4 — Combate e violência

1504–1505 constituem o gate decisório.

- não criar combate geral por antecipação;
- se eventos guiados forem suficientes, manter essa arquitetura;
- se houver decisões relevantes do jogador que exijam resolução funcional, criar a menor abstração testável;
- evitar microtática, controle individual de tripulação ou estatísticas militares sem necessidade demonstrada.

### T5 — Persistência e interface Python

- manter save/load compatível ou versionado;
- cobrir estados temporais, subcampanhas, ações one-shot e informação adquirida;
- Pygame continua ferramenta de validação, não alvo de produção final.

### T6 — Regressão e playtests

Para cada tranche com nova decisão jogável:

- CI integral;
- smoke específico da campanha;
- baterias de arquétipos quando úteis;
- `RANDOM_PER_LEG` nas baterias comparáveis;
- seeds sentinela para regimes de risco/agência;
- telemetria de blockers;
- diagnóstico antes de recalibrar qualquer parâmetro.

## Sistemas que só entram por necessidade demonstrada

- doença e mortalidade sistêmica;
- tripulação individual;
- classes detalhadas de navio;
- naufrágio/encalhe gerais;
- combate geral;
- crédito, câmbio e contratos complexos;
- reputação/diplomacia global;
- economia monetária histórica completa.

## Gate final — Python 1505 GREEN

O domínio Python somente será considerado pronto para freeze quando todos os critérios abaixo forem atendidos:

1. campanhas e estados necessários de 1497 a 1505 representados no grau definido neste roadmap;
2. nenhuma lacuna arquitetural conhecida bloqueante para esse horizonte;
3. CI integralmente verde no `main`;
4. regressão canônica integrada 1497–1505;
5. cronologia `GUIDED` validada onde há evidência suficiente e incerteza explícita onde não há;
6. save/load cobrindo campanhas, estados temporais e transições relevantes;
7. baterias sintéticas e seeds sentinela consolidadas;
8. zero blockers artificiais conhecidos no runner/telemetria;
9. divergências históricas preservadas e rastreáveis;
10. `README`, roadmap, docs metodológicas e Diário do Drive sincronizados;
11. criação de `docs/domain-freeze-1505.md` com contratos de dados e estado;
12. geração de golden states/golden tests suficientes para validar uma implementação futura em outro engine.

## Freeze e migração para Godot

Somente depois de `Python 1505 GREEN` será aberta a frente Godot.

No freeze:

- Python deixa de ser o runtime de produção alvo, mas permanece implementação de referência;
- `data/` e `simulation/` continuam fontes canônicas;
- golden tests passam a definir paridade de domínio;
- Godot recebe interface, mapa, UX, animação, áudio e distribuição;
- a migração deve portar contratos e comportamento, não copiar literalmente a arquitetura Pygame.

## Ordem de execução imediata

1. **F1 — João da Nova 1501–1502**;
2. **F2 — Vasco da Gama 1502–1503**;
3. **F3 — ciclo de 1503 em Cochim**;
4. **F4 — concluir e implementar Lopo Soares 1504**;
5. **F5 — documentar e implementar Francisco de Almeida 1505**;
6. fechar T1–T6 conforme as lacunas efetivamente demonstradas;
7. executar regressão integrada 1497–1505;
8. atingir **Python 1505 GREEN**;
9. produzir `domain-freeze-1505` e golden tests;
10. somente então iniciar a migração para Godot.

## Disciplina de memória

Ao final de cada gate relevante: registrar decisão, evidência, testes, issue/PR/commit e próximo passo no repositório; atualizar o espelho no Drive; somente então iniciar o gate seguinte.
