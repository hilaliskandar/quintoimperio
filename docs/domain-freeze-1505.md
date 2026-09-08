# Domain freeze 1497–1505

Data do gate: 2026-09-08
Issue: #136
Parent: #118
Baseline integrado: `e982d5b83a1c8a8bfe77f512e354c63347004266`
CI pós-merge F5: `34200338707` — verde

## Finalidade

Este documento congela os contratos do domínio Python necessários para representar o horizonte histórico de 1497–1505. O freeze não transforma Python/Pygame no runtime final de produção: Python permanece implementação de referência, ambiente de pesquisa, diagnóstico, validação e geração de golden states; a futura implementação em Godot deverá reproduzir os contratos e invariantes aqui definidos.

O freeze não autoriza a criação de fatos históricos ausentes, a conversão de divergências documentais em valores únicos, nem a promoção de parâmetros de simulação a evidência histórica.

## Princípios invariantes

1. Dados históricos e parâmetros de simulação permanecem separados.
2. Datas exatas só são usadas quando documentalmente defensáveis; intervalos permanecem intervalos.
3. Estado objetivo do mundo, conhecimento da Coroa, conhecimento da expedição e conhecimento do jogador não são equivalentes.
4. Soberania, acesso, relação, presença institucional, feitoria, fortificação e guarnição permanecem dimensões independentes.
5. Presença, forte ou guarnição portuguesa não implicam soberania portuguesa automática.
6. Eventos históricos específicos não criam, por si, mecânicas gerais de combate, governo, frota, naufrágio, doença ou mortalidade.
7. Forças e subcampanhas históricas podem existir documentalmente sem se tornarem simultaneamente controláveis pelo jogador.
8. Estado histórico persistente é derivado de dados temporais e da data da sessão; não deve ser duplicado artificialmente dentro do save.
9. A mesma seed aplicada ao mesmo estado de simulação deve permanecer determinística.
10. Godot deverá portar o comportamento observável do domínio, não copiar a arquitetura interna de Pygame.

## Contratos canônicos de dados

### Núcleo histórico

Os contratos canônicos permanecem em `data/`, incluindo, entre outros:

- `nodes.csv`: nós históricos/operacionais;
- `goods.csv`, `node_goods.csv`, `route_goods.csv`: bens e presença/fluxos documentados;
- `routes.csv`: conexões normalizadas e seus limites operacionais;
- `voyage_observations.csv`: observações de viagem com precedência documental;
- `pilots.csv`, `pilot_routes.csv`: pilotos e escopo de conhecimento náutico;
- `expeditions.csv`, `expedition_routes.csv`, `expedition_stops.csv`: expedições e sequências executáveis quando existentes;
- `expedition_events.csv`: eventos documentais de expedição que não devem ser convertidos automaticamente em mecânicas;
- `node_state_events.csv`: transições temporais persistentes de presença institucional, fortificação, guarnição, acesso, relação e soberania;
- `actors.csv`, `node_actors.csv`: atores históricos e vínculos locais;
- `expedition_epilogue_events.csv`: epílogos documentais fora do loop executável quando aplicável.

### Parâmetros de simulação

Os parâmetros experimentais permanecem em `simulation/`. Eles podem controlar economia relativa, logística, navegação, risco, serviços e interface, mas não constituem evidência histórica. Qualquer migração para outro engine deve manter essa separação de proveniência.

## Contratos de estado do domínio

### Sessão

`GameSessionState` é o contrato agregado de sessão. Ele reúne, de forma imutável, estado do navio, comércio, conhecimento, acesso, relações, expedição ativa quando houver, cronologia, escala ativa e históricos persistidos.

A ausência de uma campanha executável é um estado válido. Expedições documentais sem pernas normalizadas, como `EXP_ALMEIDA_1505`, não devem ser ativadas artificialmente apenas para representar o contexto histórico.

### Cronologia

`ChronologyMode.GUIDED` preserva âncoras históricas quando existe evidência suficiente. `ChronologyMode.COUNTERFACTUAL` admite simulação fora dessas âncoras sem alterar os fatos históricos armazenados.

Janelas `RANGE` tornam-se seguramente disponíveis apenas no seu limite superior quando consultadas por modelos temporais conservadores.

### Estado mundial temporal

`NodeStateEventModel` projeta o estado histórico de um nó em uma data. Campos vazios em um evento significam "preservar a dimensão anterior", não zerar automaticamente o baseline.

O modelo deve impedir retroprojeção: estados adquiridos em 1503, 1504 ou 1505 não podem contaminar campanhas anteriores.

### Eventos de expedição

`ExpeditionEventModel` registra acontecimentos históricos reutilizáveis sem transformá-los automaticamente em sistemas gerais. `available_by()` usa o limite superior da fonte para determinar quando um evento é seguramente ocorrido.

### Persistência

`CampaignPersistence` mantém JSON versionado. O save persiste o estado pertencente à sessão e a seed; o estado histórico objetivo do mundo continua sendo derivado dos dados canônicos e da data após o round-trip.

## Arco congelado 1497–1505

### 1497–1499 — MVP e retorno P1

Fluxo de ida canônico:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`

Retorno estabilizado:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`

O retorno permanece opt-in. A divergência da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada. O epílogo posterior a 25/04/1499 não é promovido a continuação jogável certa.

### 1500 — Cabral

`EXP_CABRAL_1500` introduz Vera Cruz, a ruptura de Calecute e o início de presença portuguesa em Cochim e Cananor conforme evidência disponível. Eventos específicos de separação, perda, retorno informacional e presença institucional permanecem eventos documentais, não sistemas genéricos.

### 1501–1502 — João da Nova

A campanha preserva a aquisição tardia da informação sobre Cabral em São Brás. Cananor/Cochim e o bloqueio documentado são representados sem vazamento retrospectivo de informação e sem combate geral.

### 1502–1503 — Vasco da Gama

`EXP_GAMA_1502` preserva reorganização institucional de Cochim/Cananor, eventos navais específicos e a força residente de Vicente Sodré sem exigir schema geral de múltiplas frotas simultâneas.

### 1503 — Cochim

Crise, restauração, fortificação e guarnição são estados temporais independentes. A soberania do rajá permanece local. Vaipim não se torna nó jogável apenas por aparecer na narrativa da crise.

### 1504 — Lopo Soares e Duarte Pacheco

A defesa de Cochim é representada como cadeia de eventos históricos específicos. `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`. A saída da armada principal não elimina a presença residente já estabelecida.

### 1505 — Francisco de Almeida

`EXP_ALMEIDA_1505` permanece sem `fleet_size` factual único e sem pernas jogáveis artificiais. A autoridade é decomposta em eventos: nomeação régia, Regimento, partida, exercício institucional no Índico e presença documental segura em Cochim.

`EXP_ANHAIA_1505` permanece unidade documental separada para Sofala.

Estados persistentes congelados até 31/12/1505 incluem:

- Quiloa: presença fortificada/guarnição conforme `KIL1505_E01`, sem anexação automática;
- Sofala: presença em 04/09 e fortificação/guarnição em 21/09, preservando soberania local;
- Anjediva: janela conservadora de setembro; 13/09 × 14/09 permanece divergência aberta;
- Cananor: forte/guarnição em janela conservadora 23–31/10, com acesso negociado e soberania de Kolathunad preservada;
- Cochim: forte e guarnição herdados de 1503, sem duplicação de estado em 1505;
- Mombaça: não recebe forte/guarnição persistente apenas em razão do ataque de agosto.

A presença documental de Almeida em Cochim em 16/12/1505 é a âncora segura usada no freeze. A chegada cronística candidata de 31/10 não é promovida a fato exato.

## Decisões arquiteturais congeladas

Até 31/12/1505:

- `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`;
- `NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO`;
- `MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO`.

Essas decisões podem ser reabertas em horizonte posterior somente quando uma ação controlável pelo jogador demonstrar necessidade funcional real.

Também permanecem fora do freeze como sistemas gerais: doença/mortalidade sistêmica, tripulação individual, classes detalhadas de navio, naufrágio/encalhe geral, crédito/câmbio complexos, reputação global e economia monetária histórica completa.

## Golden tests e contratos de paridade

A futura implementação em outro engine deve preservar, no mínimo, os comportamentos cobertos por:

- `tests/test_campaign.py` e `tests/test_mvp_robustness.py` — fluxo e invariantes do MVP;
- `tests/test_return_campaign.py`, `tests/test_return_persistence.py`, `tests/test_return_voyage_data.py` — retorno P1;
- `tests/test_p3_campaign.py`, `tests/test_p3_event_models.py`, `tests/test_p3_temporal_data.py` — P3 e estado temporal;
- `tests/test_p3_wave20_sentinels.py` — seeds sentinela da wave20;
- `tests/test_f1_joao_nova_smoke.py`, `tests/test_f1_joao_nova_persistence.py` — João da Nova;
- `tests/test_f2_gama_1502_smoke.py`, `tests/test_f2_gama_1502_persistence.py` — Gama 1502–1503;
- `tests/test_f3_cochin_1503_persistence.py`, `tests/test_f3_armadas_1503_registry.py` — ciclo de 1503;
- `tests/test_f4_cochin_1504_state.py`, `tests/test_f4_cochin_defense_events.py`, `tests/test_f4_end_1504_transition.py`, `tests/test_f4_lopo_soares_arrival.py` — 1504;
- `tests/test_f5_1505_node_states.py`, `tests/test_f5_almeida_authority_events.py`, `tests/test_f5_kilwa_anjediva_states.py` — transições de 1505;
- `tests/test_f5_1505_golden_state.py` — golden state de 31/12/1505;
- `tests/test_f5_1505_freeze_persistence.py` — persistência do contexto de freeze;
- `tests/test_persistence.py` e `tests/test_interface_m6.py` — contrato geral de save/load.

Paridade em Godot não significa reproduzir classes Python. Significa que, para entradas equivalentes, os estados observáveis, bloqueios, datas, disponibilidade de ações e golden states devem ser equivalentes dentro dos contratos definidos.

## Golden state de 31/12/1505

A projeção documental congelada para `31/12/1505` é determinística. Duas instâncias independentes de `NodeStateEventModel` devem produzir o mesmo resultado para os nós testados.

O round-trip de uma sessão datada de `31/12/1505` em Cochim deve preservar:

- data;
- local;
- seed;
- ausência de expedição Almeida ativa fictícia;
- modo cronológico;
- identidade da projeção histórica antes/depois da persistência.

## Divergências que permanecem abertas

As seguintes divergências não bloqueiam o freeze e não podem ser harmonizadas silenciosamente:

- chegada de Vasco da Gama a Calecute: 20/21 de maio de 1498;
- tamanho total da armada de Almeida: variantes 20/21/22/23;
- Anjediva: 13/09 × 14/09 para o marco cronístico discutido;
- `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto`;
- chegada diária de Almeida a Cochim antes da âncora documental de 16/12/1505.

Classificação: `NON_BLOCKING` para o freeze; devem continuar rastreáveis na documentação histórica.

## Lacunas conhecidas

### BLOCKING

Nenhuma identificada no baseline `e982d5b83a1c8a8bfe77f512e354c63347004266` após a CI pós-merge `34200338707`.

### NON_BLOCKING

- README ainda precisa ser sincronizado com o estado 1505;
- roadmap precisa marcar F5 como integrado e #136 como gate corrente;
- documentação do freeze precisa ser integrada ao `main` e espelhada no Diário do Drive.

### DEFERRED_GODOT

- interface/UX final;
- animação, áudio e distribuição;
- portabilidade visual do mapa;
- arquitetura de cenas e recursos do engine;
- eventual telemetria própria do runtime Godot.

## Evidência de integração

F5 foi integrado pelo PR #135 no commit `e982d5b83a1c8a8bfe77f512e354c63347004266`.

A CI pós-merge `34200338707` concluiu com sucesso validação dos CSVs, suíte de testes de domínio, protótipos de economia/navegação/viagem/serviços/comércio, sessão integrada, smoke do retorno, diagnósticos logísticos, interfaces, persistência e mapas.

## Critério para declarar Python 1505 GREEN

A issue #136 poderá ser encerrada quando:

1. este documento estiver integrado ao `main`;
2. README e roadmap estiverem sincronizados com F5 integrado e o freeze;
3. a CI do PR de freeze e a CI pós-merge permanecerem verdes;
4. o Diário do Drive registrar o baseline final, contratos e próximo passo;
5. a issue #118 puder ser encerrada sem lacuna `BLOCKING`.

Somente então poderá ser aberta a frente de migração para Godot.
