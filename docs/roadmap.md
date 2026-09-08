# Roteiro de produção

## Estado consolidado

O projeto possui os baselines históricos e funcionais de 1497–1504 integrados ao `main`, e o gate documental de 1505 também está concluído:

- MVP Lisboa–Calecute: `f308fb0e97687e34365fd23ed257a0114fd81613`;
- P1 retorno até BRG: `47fb82baad1289077c048576f3bc52815d6b192f`;
- P2 Cochim mínimo: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`;
- P3-func-A: merge do PR #117 em `1011507d5dd1332585b01cfd90351395952bb5f1`;
- F4/1504: merge do PR #131 em `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`, CI pós-merge `34189675875` verde;
- F5-doc/1505: merge do PR #133 em `5e10409fa10e4b412f3ffcb3232d9674c09c1773`, CI pós-merge `34192641101` verde.

O objetivo de produção permanece explícito: **concluir e estabilizar em Python o domínio necessário para representar 1497–1505 antes de migrar o runtime de produção para Godot**.

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

A #110 permanece como guarda-chuva documental de 1500–1505. Os gates documentais até 1505 estão concluídos; o gate funcional corrente é F5, issue #134.

## F1 — João da Nova 1501–1502

**Status: CONCLUÍDO.**

Objetivos estabilizados:

1. completar somente as pernas e âncoras temporais documentalmente sustentáveis;
2. manter a partida em Lisboa sem conhecimento do desfecho de Cabral no Malabar;
3. aplicar a aquisição de informação em São Brás como evento próprio da expedição;
4. integrar Cananor/Cochim e a presença institucional correspondente;
5. preservar Ceilão fora da rota enquanto a evidência permanecer insuficiente;
6. representar confronto específico sem combate geral;
7. testar save/load, cronologia e informação sem vazamento retrospectivo;
8. manter regressão integral contra MVP/P1/P2/P3-func-A.

Resultado: campanha representável até seu limite documental, com informação correta por data/local e sem introdução de combate geral.

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

**Status: GATE DOCUMENTAL CONCLUÍDO; IMPLEMENTAÇÃO FUNCIONAL EM ANDAMENTO NA ISSUE #134.**

Gate documental #132 encerrado; PR #133 integrado em `5e10409fa10e4b412f3ffcb3232d9674c09c1773`; CI pós-merge `34192641101` verde.

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

Decisões documentais fechadas:

1. `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO` permanece válido para o horizonte 1505;
2. não criar schema global de vice-reinado/governo enquanto não houver consumidor funcional;
3. `node_state_events` é suficiente para presença institucional, fortificação, guarnição, acesso, relação e soberania;
4. autoridade de Francisco de Almeida deve permanecer decomposta entre nomeação régia, comando expedicionário e exercício institucional no Índico;
5. composição da armada permanece `UNRESOLVED` diante das variantes 20/21/22/23;
6. Sofala/Pêro de Anhaia deve ser preservada como unidade histórica própria quando necessário;
7. Anjediva deve usar janela conservadora em setembro enquanto 13/09 × 14/09 não for resolvido;
8. chegada diária de Almeida a Cochim não deve ser fixada sem evidência melhor;
9. soberania local deve permanecer explícita em Cananor e Cochim apesar de fortificações/guarnições portuguesas;
10. a divergência `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` continua aberta.

Objetivos funcionais da issue #134:

1. registrar Francisco de Almeida/armada de 1505 sem fixar `fleet_size` factual único;
2. representar somente os estados persistentes de Quiloa, Sofala, Anjediva, Cananor e Cochim necessários ao horizonte de 31/12/1505;
3. usar preferencialmente os schemas já existentes;
4. preservar soberanias locais e separação entre fortificação, guarnição e domínio;
5. provar estado de 31/12/1505 por data e após save/load;
6. executar regressão integral antes de qualquer generalização de nova mecânica.

Critério de verde de F5: estado do mundo em 31/12/1505 determinístico e reproduzível, sem lacuna arquitetural bloqueante, com CI/regressão integral verdes e sem nova mecânica geral não demonstrada.

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

O gate decisório 1504–1505 está, até o baseline atual, resolvido a favor de eventos guiados específicos:

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`.

A decisão deve ser reaberta somente se uma nova ação controlável pelo jogador demonstrar necessidade real de resolução militar funcional.

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

1. **F5 funcional — issue #134: implementar Francisco de Almeida e estados persistentes de 1505**;
2. executar regressão integrada 1497–1505;
3. fechar os pontos transversais T1–T6 que permanecerem efetivamente abertos após F5;
4. atingir **Python 1505 GREEN**;
5. produzir `docs/domain-freeze-1505.md`;
6. gerar golden states/golden tests para paridade futura;
7. sincronizar `README`, roadmap, docs metodológicas e Diário do Drive;
8. somente então iniciar a migração para Godot.

## Disciplina de memória

Ao final de cada gate relevante: registrar decisão, evidência, testes, issue/PR/commit e próximo passo no repositório; atualizar o espelho no Drive; somente então iniciar o gate seguinte.
