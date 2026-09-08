# Roteiro de produção

## Estado consolidado

O domínio histórico e funcional de 1497–1505 está integrado ao `main` até F5:

- MVP Lisboa–Calecute: `f308fb0e97687e34365fd23ed257a0114fd81613`;
- P1 retorno até BRG: `47fb82baad1289077c048576f3bc52815d6b192f`;
- P2 Cochim mínimo: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`;
- P3-func-A: merge do PR #117 em `1011507d5dd1332585b01cfd90351395952bb5f1`;
- F4/1504: merge do PR #131 em `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`, CI pós-merge `34189675875` verde;
- F5-doc/1505: merge do PR #133 em `5e10409fa10e4b412f3ffcb3232d9674c09c1773`, CI pós-merge `34192641101` verde;
- F5-func/1505: merge do PR #135 em `e982d5b83a1c8a8bfe77f512e354c63347004266`, CI pós-merge `34200338707` verde.

O objetivo de produção permanece explícito: **concluir e estabilizar em Python o domínio necessário para representar 1497–1505 antes de migrar o runtime de produção para Godot**.

Esse objetivo funcional foi atingido até F5. O gate corrente é agora o **freeze formal do domínio**, issue #136, necessário para declarar `Python 1505 GREEN`.

O Python permanece como laboratório de domínio, implementação de referência, ambiente de pesquisa histórica, diagnóstico e playtest sintético. Pygame continua apenas como interface suficiente para validação e smoke tests; não deve receber investimento de produção que será descartado na migração.

Princípio permanente: **dados históricos e parâmetros de simulação permanecem separados; fatos históricos não são recalibrados para resolver jogabilidade**.

## Método de execução

A partir de P3, cada tranche histórica segue obrigatoriamente:

`documentação suficiente → normalização mínima → implementação → testes/CI → playtest/diagnóstico → fechamento → próxima tranche`.

Nenhuma mecânica geral deve ser criada antes de um caso histórico demonstrar sua necessidade.

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

Resultados incorporados:

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

## Gate-mãe — P3-1505

Issue #118 — **Fechar domínio Python 1497–1505 e preparar freeze para Godot**.

A #110 permanece como guarda-chuva documental de 1500–1505. Todos os gates documentais e funcionais F1–F5 estão concluídos. O gate ativo é #136 — **Python 1505 GREEN — domain freeze e handoff para Godot**.

## F1 — João da Nova 1501–1502

**Status: CONCLUÍDO.**

Resultados estabilizados:

1. somente pernas e âncoras temporalmente sustentáveis foram normalizadas;
2. a partida de Lisboa não conhece retrospectivamente o desfecho de Cabral no Malabar;
3. a aquisição de informação em São Brás é evento próprio da expedição;
4. Cananor/Cochim e presença institucional correspondente foram integrados;
5. Ceilão permanece fora da rota enquanto a evidência for insuficiente;
6. confronto específico foi representado sem combate geral;
7. save/load, cronologia e informação foram testados sem vazamento retrospectivo;
8. regressão contra MVP/P1/P2/P3-func-A permanece preservada.

## F2 — Vasco da Gama 1502–1503

**Status: CONCLUÍDO.**

Resultados consolidados:

1. `EXP_GAMA_1502` integrado como unidade histórica;
2. rotas e marcos adicionados apenas quando documentalmente necessários;
3. reorganização de Cochim e Cananor aplicada por estados temporais;
4. mudanças de feitor/presença sem alteração de soberania local;
5. força residente de Vicente Sodré tratada sem generalizar múltiplas frotas simultâneas;
6. missão institucional distinguida de decisão operacional;
7. bloqueio e combate mantidos como eventos específicos;
8. persistência de efeitos mundiais preservada após separação da força residente.

## F3 — Ciclo de 1503 em Cochim

**Status: CONCLUÍDO.**

Resultados consolidados:

1. crise e retirada para Vaipim representadas sem criar nó jogável desnecessário;
2. Cochim restaurado no momento documentado;
3. fortificação e guarnição materializadas com temporalidade;
4. soberania do rajá preservada;
5. feitoria, fortificação, guarnição, acesso e relação mantidos como dimensões distintas;
6. estados de 1503 não contaminam campanhas anteriores.

## F4 — Lopo Soares 1504

**Status: CONCLUÍDO E INTEGRADO AO MAIN.**

Issue funcional #130 encerrada; PR #131 integrado em `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`; CI pós-merge `34189675875` verde.

Resultados consolidados:

1. `EXP_LOPO_SOARES_1504` registrado como unidade histórica sem pernas fictícias;
2. defesa de Cochim sob Duarte Pacheco estruturada como subcampanha residente documental;
3. cadeia defensiva de março–julho representada por eventos conservadores, sem microtática;
4. chegada da armada de Lopo Soares a Cochim em 14/09/1504 e saída em 26/12/1504 registradas sem fabricar itinerário intermediário;
5. fortificação, guarnição, feitoria, relação favorável e soberania local herdadas de 1503 preservadas;
6. saída da armada principal não elimina a presença residente em 31/12/1504;
7. Coulão, Cranganor e Pandarane permaneceram fora do grafo por ausência de necessidade funcional;
8. divergência `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` preservada sem harmonização prematura.

Decisão T4 de F4: `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`.

## F5 — Francisco de Almeida 1505

**Status: CONCLUÍDO E INTEGRADO AO MAIN.**

Gate documental #132 encerrado; PR #133 integrado em `5e10409fa10e4b412f3ffcb3232d9674c09c1773`; CI pós-merge `34192641101` verde.

Gate funcional #134 encerrado; PR #135 integrado em `e982d5b83a1c8a8bfe77f512e354c63347004266`; CI pós-merge `34200338707` integralmente verde.

Documentação canônica:

- `docs/f5-1505-evidence-matrix-v0.1.md`;
- `docs/f5-1505-authority-fleet-audit-v0.1.md`;
- `docs/f5-1505-route-chronology-audit-v0.1.md`;
- `docs/f5-1505-institutional-matrix-v0.1.md`;
- `docs/f5-1505-sofala-anhaia-anjediva-audit-v0.1.md`;
- `docs/f5-1505-cannanore-cochin-audit-v0.1.md`;
- `docs/f5-1505-minimal-normalization-proposal.md`;
- `docs/f5-1505-documentary-closeout.md`;
- `docs/f5-francisco-almeida-1505-handoff.md`.

Resultados funcionais consolidados:

1. `EXP_ALMEIDA_1505` registrado sem `fleet_size` factual único e sem pernas fictícias;
2. autoridade de Francisco de Almeida decomposta entre nomeação régia, Regimento, partida, exercício institucional no Índico e presença documental em Cochim;
3. `EXP_ANHAIA_1505` preservada como unidade histórica própria;
4. estados persistentes de Quiloa, Sofala, Anjediva e Cananor materializados com temporalidade conservadora;
5. Cochim herda fortificação e guarnição de 1503 sem duplicação;
6. soberanias locais permanecem explícitas;
7. Mombaça não recebe forte/guarnição persistente apenas pelo ataque de agosto;
8. golden state de 31/12/1505 é determinístico;
9. round-trip de persistência do contexto de freeze preserva a projeção histórica sem inventar campanha Almeida ativa;
10. nenhuma nova mecânica geral foi necessária em `src/` ou `simulation/`.

Decisões finais de F5:

- `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`;
- `NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO`;
- `MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO`.

Divergências preservadas:

- tamanho total da armada de Almeida: 20/21/22/23;
- Anjediva: 13/09 × 14/09;
- `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto`;
- chegada diária de Almeida a Cochim antes da âncora segura de 16/12/1505.

## Gates transversais T1–T6

### T1 — Estado mundial temporal

**Status no horizonte 1505: SATISFEITO.**

`node_state_events` e `expedition_events` constituem os contratos estáveis para soberania, acesso, relação, presença institucional, feitoria, fortificação, guarnição, eventos de expedição e aquisição de informação. Testes temporais impedem retroprojeção.

### T2 — Expedições, subcampanhas e forças residentes

**Status no horizonte 1505: SATISFEITO.**

`active_expedition_id` + campanhas/subcampanhas documentais são suficientes. Os casos de Sodré, Duarte Pacheco e Pêro de Anhaia não demonstraram necessidade de múltiplas frotas simultaneamente controláveis.

### T3 — Informação e latência

**Status no horizonte 1505: SATISFEITO.**

Estado objetivo/local, conhecimento institucional e conhecimento da expedição permanecem separados; João da Nova demonstra aquisição tardia sem vazamento retrospectivo. Não houve necessidade demonstrada de um sistema adicional de mensagens persistentes.

### T4 — Combate e violência

**Status no horizonte 1505: SATISFEITO.**

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`.

A decisão só deverá ser reaberta quando horizonte posterior introduzir ação militar controlável que exija resolução funcional.

### T5 — Persistência e interface Python

**Status no horizonte 1505: SATISFEITO.**

Save/load versionado cobre estado de sessão e transições necessárias; golden state e freeze de 31/12/1505 possuem round-trip dedicado. Pygame permanece ferramenta de validação.

### T6 — Regressão e playtests

**Status no horizonte 1505: SATISFEITO PARA O FREEZE.**

CI integral, smokes, baterias por arquétipos, `RANDOM_PER_LEG` e seeds sentinela permanecem no repositório. A CI pós-F5 no `main` (`34200338707`) passou todos os testes, smokes, diagnósticos, persistência e mapas.

## Sistemas que permanecem fora por ausência de necessidade demonstrada

- doença e mortalidade sistêmica;
- tripulação individual;
- classes detalhadas de navio;
- naufrágio/encalhe gerais;
- combate geral;
- crédito, câmbio e contratos complexos;
- reputação/diplomacia global;
- economia monetária histórica completa.

## Gate final — Python 1505 GREEN

**Status: EM FECHAMENTO — issue #136.**

O baseline funcional `e982d5b83a1c8a8bfe77f512e354c63347004266` já satisfaz os critérios funcionais e não apresenta lacuna `BLOCKING` conhecida. O trabalho corrente é congelar e integrar os contratos em `docs/domain-freeze-1505.md` e sincronizar a documentação.

Critérios:

1. campanhas e estados necessários de 1497 a 1505 representados no grau definido neste roadmap — **SATISFEITO**;
2. nenhuma lacuna arquitetural conhecida bloqueante — **SATISFEITO**;
3. CI integralmente verde no `main` — **SATISFEITO, run `34200338707`**;
4. regressão canônica integrada 1497–1505 — **SATISFEITO pelos testes e smokes inventariados no freeze**;
5. cronologia `GUIDED` validada onde há evidência e incerteza explícita onde não há — **SATISFEITO**;
6. save/load cobrindo campanhas, estados temporais e transições relevantes — **SATISFEITO**;
7. baterias sintéticas e seeds sentinela consolidadas — **SATISFEITO no horizonte em que são funcionalmente aplicáveis**;
8. zero blockers artificiais conhecidos no runner/telemetria — **SATISFEITO no baseline corrente**;
9. divergências históricas preservadas e rastreáveis — **SATISFEITO**;
10. `README`, roadmap, docs metodológicas e Diário do Drive sincronizados — **EM FECHAMENTO NA #136**;
11. `docs/domain-freeze-1505.md` criado com contratos de dados e estado — **CRIADO NA BRANCH #136**;
12. golden states/golden tests suficientes para futura implementação em outro engine — **INVENTARIADOS NO FREEZE**.

## Freeze e migração para Godot

Somente depois de `Python 1505 GREEN` ser integrado ao `main` e a issue #118 ser encerrada será aberta a frente Godot.

No freeze:

- Python deixa de ser o runtime de produção alvo, mas permanece implementação de referência;
- `data/` e `simulation/` continuam fontes canônicas;
- golden tests passam a definir paridade de domínio;
- Godot receberá interface, mapa, UX, animação, áudio e distribuição;
- a migração deverá portar contratos e comportamento, não copiar literalmente a arquitetura Pygame.

## Ordem de execução imediata

1. concluir issue #136 com `docs/domain-freeze-1505.md`;
2. sincronizar README, roadmap e Diário do Drive;
3. executar CI integral da branch do freeze;
4. abrir e validar PR de `Python 1505 GREEN`;
5. integrar o PR e confirmar CI pós-merge no `main`;
6. encerrar #136 e #118 sem lacuna `BLOCKING`;
7. somente então abrir a frente de migração para Godot.

## Disciplina de memória

Ao final de cada gate relevante: registrar decisão, evidência, testes, issue/PR/commit e próximo passo no repositório; atualizar o espelho no Drive; somente então iniciar o gate seguinte.
