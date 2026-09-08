# F4 — Lopo Soares 1504 — closeout funcional

Data: 2026-09-08
Issue: #130
Gate-mãe: #118
Baseline de partida: `fec3888679024868f321790d4f1d065dcf641914`

## Resultado

A tranche F4 representa o ciclo necessário de 1504 sem introduzir combate geral, múltiplas frotas ativas, novos nós ou itinerários não documentados.

A decisão T4 permanece:

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

A arquitetura efetivamente utilizada foi:

`EXPEDICOES_DOCUMENTAIS_SEM_PERNAS + EXPEDITION_EVENTS + NODE_STATE_EVENTS_HERDADOS`

## 1. Estado herdado de Cochim

F4 preserva o baseline de F3. Durante todo 1504, Cochim continua resolvendo como:

- soberania local;
- `FACTORY_RESTORED`;
- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- acesso `NEGOTIATED`;
- relação `FAVORABLE`.

Nenhum novo `node_state_event` foi necessário porque a campanha defensiva e a passagem da armada de Lopo não demonstraram transição institucional/territorial que justificasse sobrescrever essas dimensões.

## 2. Armada de Lopo Soares

Foi criada:

`EXP_LOPO_SOARES_1504`

A expedição existe como unidade histórica de catálogo, sem pernas em `expedition_routes.csv`. Testes exigem que `first_sequence()` recuse a ativação por ausência de pernas.

Assim, a existência da armada não foi convertida automaticamente em campanha jogável nem em itinerário Lisboa→Índia inventado.

## 3. Defesa residente de Cochim

A auditoria de propriedade dos eventos demonstrou que a defesa de março–julho não pode ser atribuída à armada de Lopo, que chega depois, nem à armada de Francisco de Albuquerque como se ela continuasse intacta em 1504.

Foi criada a unidade documental:

`EXP_DUARTE_PACHECO_DEFENSE_1504`

Tipo:

`RESIDENT_DEFENSE_SUBCAMPAIGN`

Também sem pernas executáveis.

Ela possui três eventos-resumo conservadores:

- `DPP1504_E01` — `DEFENSE_CAMPAIGN_BEGINS`, situado em março e seguramente disponível no limite superior 31/03;
- `DPP1504_E02` — `DEFENSIVE_OPERATIONS_REPEATED`, março–maio, seguramente disponível em 31/05;
- `DPP1504_E03` — `DEFENSE_CAMPAIGN_ENDS`, situado em julho e seguramente disponível em 31/07.

As datas 16/03 e 03/07 permanecem candidatos historiográficos e não foram promovidas a `EXACT`.

Nenhum dano, HP, moral, força, baixas, unidades táticas ou probabilidades de combate foi introduzido.

## 4. Chegada e saída de Lopo Soares em Cochim

A pesquisa dirigida permitiu estreitar dois marcos sem reconstruir as pernas anteriores/posteriores da viagem:

- `LS1504_E01` — `ROYAL_FLEET_ARRIVES_COCHIN`, `14/09/1504`, `EXACT`; origem imediata deixada vazia;
- `LS1504_E02` — `ROYAL_FLEET_DEPARTS_COCHIN`, `26/12/1504`, `EXACT`; destino imediato deixado vazio.

A chegada em 14/09 recebe sustentação reforçada pela referência à carta contemporânea de Álvaro Vaz, escrita em Cochim em 24/12/1504. A saída em 26/12 permanece sustentada, nesta tranche, por reconstrução académica especializada.

Os dois eventos comprovam a diferença entre presença transitória da grande armada e presença residente em Cochim. Em `31/12/1504`, após a saída de Lopo, a feitoria, o forte e a guarnição continuam resolvidos pelo estado temporal herdado.

## 5. Combates posteriores e novos nós

F4 não normalizou como mecânica ou novos nós:

- bombardeio de Calecute;
- ataque a Cranganor;
- Pandarane;
- Coulão.

Esses episódios permanecem historicamente documentados, mas não alteram o estado mínimo necessário de Cochim em `31/12/1504` de modo que justifique ampliar o grafo ou criar combate geral nesta tranche.

O marco secundário de 07/09 diante de Calecute também não foi elevado a `EXACT` sem fechamento documental comparável ao de 14/09 em Cochim.

## 6. Divergência onomástica

A pesquisa revelou conflito que deve permanecer explícito:

- a listagem EVE/FCSH apresenta `Manuel Teles Barreto` entre os capitães da armada de 1504;
- reconstrução especializada distingue `Manuel Teles de Vasconcelos` nessa armada e associa `Manuel Teles Barreto` a 1506.

Por isso, F4 não normaliza o nome do comandante sucessor da guarda de Cochim em `node_state_events` nem em novo campo de domínio.

Essa divergência deve ser carregada para F5, onde a continuidade institucional de 1505 poderá demonstrar se a identidade nominal precisa ou não de representação funcional.

## 7. Fontes dirigidas

Foram registradas em `docs/f4-1504-sources.md`:

- `EVE_DUARTE_PACHECO`;
- `JESUS_LAND_WARFARE_2021`;
- `ALVARO_VAZ_COCHIN_1504`;
- `BOUCHON_LOPO_1976`;
- `VICENTE_PORTUGAL_MADAGASCAR`.

Esses IDs documentais sustentam as decisões F4 sem reescrever silenciosamente o corpus anterior.

## 8. Testes e CIs

Gates integrais verdes durante a tranche:

- registro documental de Lopo + estado herdado/save-load: `34188845985`;
- subcampanha residente + cadeia defensiva: `34189124746`;
- chegada de Lopo em 14/09: `34189323487`;
- saída em 26/12 + estado de fim de ano: `34189467853`.

A suíte cobre:

- expedições documentais sem pernas;
- recusa de ativação acidental;
- semântica conservadora de `available_by()`;
- continuidade de feitoria, fortificação, guarnição e soberania;
- chegada/saída exatas sem inventar rotas;
- save/load do estado temporal;
- regressão MVP/P1/P2/P3/F1/F2/F3;
- interfaces e cartografia.

## 9. Escopo final

O diff F4 está restrito a:

- `data/expeditions.csv`;
- `data/expedition_events.csv`;
- documentação F4;
- testes F4.

Não há alterações em:

- `src/`;
- `simulation/`;
- `expedition_routes.csv`;
- `voyage_observations.csv`;
- `nodes.csv`;
- `node_state_events.csv`.

As aparentes substituições da última linha dos dois CSVs resultam apenas da inclusão de quebra de linha antes dos novos registros; não alteram materialmente os eventos/expedições anteriores.

## 10. Handoff para F5

F5 — Francisco de Almeida 1505 — deve partir do seguinte estado em `31/12/1504`:

- Cochim segue soberania local;
- feitoria, forte e guarnição portuguesas persistem;
- a armada principal de Lopo já deixou Cochim em 26/12;
- a identidade nominal do comando residente permanece historiograficamente divergente;
- combate geral continua não demonstrado como necessário;
- Coulão, Cranganor e Pandarane não são nós do grafo por efeito de F4.

O primeiro gate de F5 deve ser documental e responder, antes de implementar:

1. composição, partida, itinerário e chegada da armada de Francisco de Almeida;
2. quais mudanças de governo/autoridade de 1505 precisam existir no domínio;
3. fortificações e guarnições novas somente quando documentadas e necessárias;
4. continuidade ou mudança real do comando em Cochim;
5. se os casos de 1505 finalmente demonstram necessidade de generalizar combate, governo, frota ou força residente;
6. qual estado final de 1505 será usado no freeze `Python 1505 GREEN`.

## Critério de integração

A F4 pode ser integrada após:

- CI do HEAD final verde;
- auditoria do diff contra `main` sem contaminação;
- PR mergeável e sem threads abertas;
- CI pós-merge verde no `main`;
- sincronização do Diário do Drive;
- encerramento da issue #130.
