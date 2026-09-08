# F5 — handoff funcional de Francisco de Almeida em 1505

Data: 2026-09-08
Issue funcional: #134
Baseline integrado: `5e10409fa10e4b412f3ffcb3232d9674c09c1773`
CI pós-merge do gate documental: `34192641101` — verde

## Estado de partida

O gate documental F5 (#132) foi concluído e integrado pelo PR #133. A implementação funcional parte exclusivamente das decisões consolidadas na documentação F5, em especial `docs/f5-1505-minimal-normalization-proposal.md` e as auditorias específicas de autoridade/frota, rota, Sofala/Anhaia/Anjediva e Cananor/Cochim.

## Decisões fechadas

1. `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO` para o horizonte 1505.
2. Não criar schema global de vice-reinado/governo enquanto não houver consumidor funcional que o exija.
3. `node_state_events.csv` é a camada de fortificação, guarnição, presença institucional, acesso, relação e soberania.
4. A autoridade de Francisco de Almeida permanece decomposta entre nomeação régia, Regimento, comando expedicionário e exercício institucional no Índico; não é retroprojetada como estado único desde Lisboa.
5. O tamanho da armada permanece `UNRESOLVED` diante das variantes 20/21/22/23.
6. Soberania local permanece explícita mesmo com fortificação/guarnição portuguesa.
7. Sofala/Pêro de Anhaia permanece unidade histórica própria.
8. Anjediva usa janela conservadora em setembro; 13/09 × 14/09 não é resolvido artificialmente.
9. A chegada diária de Almeida a Cochim não é fixada; 16/12/1505 é a presença documental segura usada no freeze.
10. A divergência `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` permanece aberta.

## Checkpoints funcionais concluídos

### Catálogo de Almeida

- `EXP_ALMEIDA_1505` registrado sem `fleet_size` factual único e sem pernas jogáveis;
- teste em `tests/test_f5_almeida_registry.py`;
- CI `34192932424` verde.

### Estados persistentes — Sofala e Cananor

- `SOF1505_E01`: presença institucional/capitania em `04/09/1505`, sem antecipar forte ou guarnição;
- `SOF1505_E02`: fortificação e guarnição em `21/09/1505`;
- `CAN1505_E01`: janela conservadora `23–31/10/1505`, efetiva em 31/10;
- soberanias locais e acesso negociado preservados;
- correção `5ee221d8428a8f50c2a4fbe7b084a10f0e59d46c` estabeleceu que campos vazios em `node_state_events` preservam baseline quando um evento não deve alterar aquela dimensão;
- CI `34193403253` verde.

### Expedição separada de Pêro de Anhaia

- `EXP_ANHAIA_1505` registrado como `ROYAL_FORTIFICATION_MISSION`, período 1505–1506 e partida em `18/05/1505`;
- sem pernas executáveis e sem exigir múltiplas frotas simultâneas;
- teste em `tests/test_f5_anhaia_registry.py`;
- CI `34193505777` verde.

### Estados persistentes — Quiloa e Anjediva

- `KIL1505_E01`: janela `22–24/07/1505`, estado persistente aplicado em 24/07;
- `ANJ1505_E01`: janela `01–30/09/1505`, estado aplicado em 30/09;
- ambos preservam a distinção entre presença fortificada e soberania territorial;
- teste em `tests/test_f5_kilwa_anjediva_states.py`;
- CI `34193613911` verde.

### Eventos institucionais de Almeida

- `ALM1505_E01 — ROYAL_APPOINTMENT`: 27/02/1505, `EXACT`;
- `ALM1505_E02 — ROYAL_REGIMENT_ISSUED`: 03/03/1505, `EXACT`;
- `ALM1505_E03 — FLEET_DEPARTURE`: Lisboa, 25/03/1505, `EXACT`, destino não normalizado;
- `ALM1505_E04 — VICEROYAL_AUTHORITY_ACTIVE_IN_INDIA`: Cananor, janela `01–31/10/1505`, `RANGE`, efetiva conservadoramente em 31/10;
- `ALM1505_E05 — PRESENCE_IN_COCHIN`: Cochim, 16/12/1505, `EXACT`, baseada em presença documental segura e sem promover 31/10 a chegada factual;
- nenhuma dessas linhas cria schema global de governo ou altera soberania de nó;
- commits `a05d3d4b7fe13b650534369d95f4750689bf3e97` e `4bddbc64c2056e69aa8360b10edefafd58e865f4`;
- teste em `tests/test_f5_almeida_authority_events.py`;
- CI `34194481126` integralmente verde.

### Golden state documental de 31/12/1505

- teste `tests/test_f5_1505_golden_state.py` fixa consultas determinísticas para `KIL`, `SOF`, `ANJ`, `CAN`, `COC` e `MOM` em `31/12/1505`;
- Quiloa, Sofala, Anjediva e Cananor resolvem forte + guarnição portugueses conforme seus gates temporais;
- Cochim herda forte e guarnição de 1503, sem duplicação em 1505;
- Mombaça não recebe fortificação/guarnição persistente apenas por causa do ataque de agosto;
- a sequência institucional completa de Almeida está disponível no freeze e termina com presença documental em Cochim;
- duas instâncias independentes de `NodeStateEventModel` resolvem exatamente o mesmo estado, provando determinismo da projeção documental;
- commit `243083930138354f54ac59dd48713c41eeca3732`;
- CI `34194546533` integralmente verde.

## Próximos incrementos

1. provar explicitamente o round-trip save/load no contexto do freeze, sem inventar campanha jogável de Almeida;
2. decidir se a centralidade administrativa de Cochim precisa de qualquer representação adicional; a presunção atual é **não**, pois `ALM1505_E05` já satisfaz o consumidor documental e não há consulta global de sede;
3. executar regressão integral final da branch e auditar o diff contra o baseline integrado;
4. preparar fechamento da issue #134 e handoff `domain-freeze-1505` / `Python 1505 GREEN`.

## Restrições

Não implementar por antecipação combate geral, múltiplas frotas simultâneas, sistema global de governo/autoridade, itinerários diários reconstruídos por analogia, novos nós sem necessidade demonstrada ou resolução artificial de divergências documentais.

## Critério de fechamento F5

A tranche pode ser encerrada quando o estado de `31/12/1505` estiver também coberto pelo contrato de persistência/save-load aplicável, a regressão integral permanecer verde e o diff final não introduzir mecânica geral não demonstrada. O fechamento deve produzir `domain-freeze-1505` ou handoff explícito para o gate final do Python 1505 GREEN.
