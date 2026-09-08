# F5 — handoff funcional de Francisco de Almeida em 1505

Data: 2026-09-08
Issue funcional: #134
Baseline integrado: `5e10409fa10e4b412f3ffcb3232d9674c09c1773`
CI pós-merge do gate documental: `34192641101` — verde

## Estado de partida

O gate documental F5 (#132) foi concluído e integrado pelo PR #133. A implementação funcional parte exclusivamente das decisões consolidadas na documentação F5, em especial `docs/f5-1505-minimal-normalization-proposal.md` e as auditorias específicas de autoridade/frota, rota, Sofala/Anhaia/Anjediva e Cananor/Cochim.

## Decisões fechadas

1. `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO` para o horizonte 1505.
2. `NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO` até 31/12/1505.
3. `MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO` até 31/12/1505.
4. `node_state_events.csv` é a camada de fortificação, guarnição, presença institucional, acesso, relação e soberania.
5. A autoridade de Francisco de Almeida permanece decomposta entre nomeação régia, Regimento, comando expedicionário e exercício institucional no Índico.
6. O tamanho da armada permanece `UNRESOLVED` diante das variantes 20/21/22/23.
7. Soberania local permanece explícita mesmo com fortificação/guarnição portuguesa.
8. Sofala/Pêro de Anhaia permanece unidade histórica própria.
9. Anjediva usa janela conservadora em setembro; 13/09 × 14/09 não é resolvido artificialmente.
10. A chegada diária de Almeida a Cochim não é fixada; 16/12/1505 é a presença documental segura usada no freeze.
11. A divergência `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` permanece aberta.
12. A centralidade administrativa de Cochim não recebe novo campo: o evento institucional de Almeida satisfaz o consumidor atual e não existe consulta global de sede que justifique schema adicional.

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
- `ALM1505_E05 — PRESENCE_IN_COCHIN`: Cochim, 16/12/1505, `EXACT`, sem promover 31/10 a chegada factual;
- nenhuma dessas linhas cria schema global de governo ou altera soberania de nó;
- commits `a05d3d4b7fe13b650534369d95f4750689bf3e97` e `4bddbc64c2056e69aa8360b10edefafd58e865f4`;
- teste em `tests/test_f5_almeida_authority_events.py`;
- CI `34194481126` integralmente verde.

### Golden state documental de 31/12/1505

- `tests/test_f5_1505_golden_state.py` fixa consultas determinísticas para `KIL`, `SOF`, `ANJ`, `CAN`, `COC` e `MOM`;
- Quiloa, Sofala, Anjediva e Cananor resolvem forte + guarnição conforme seus gates;
- Cochim herda forte e guarnição de 1503, sem duplicação em 1505;
- Mombaça não recebe estado persistente português apenas por causa do ataque de agosto;
- sequência institucional de Almeida termina com presença documental em Cochim;
- commit `243083930138354f54ac59dd48713c41eeca3732`;
- CI `34194546533` integralmente verde.

### Persistência do contexto de freeze

- `tests/test_f5_1505_freeze_persistence.py` cria uma sessão em Cochim em `31/12/1505`, sem campanha Almeida ativa fictícia;
- o round-trip `CampaignPersistence.dumps/loads` preserva data, local, seed, ausência de expedição ativa e modo cronológico;
- o estado histórico objetivo não é duplicado no save: ele continua derivado de data + `node_state_events`, e a projeção antes/depois do round-trip é idêntica;
- isso mantém o contrato existente de persistência sem elevar Almeida a campanha jogável sem pernas;
- commit `8cf7343b7c4a7da2d9eab16d0dbf23db6d98250c`;
- CI `34194659164` integralmente verde.

## Auditoria do diff funcional

Comparação do baseline integrado `5e10409fa10e4b412f3ffcb3232d9674c09c1773` com `8cf7343b7c4a7da2d9eab16d0dbf23db6d98250c`:

- branch 20 commits à frente, zero atrás;
- alterações funcionais limitadas a `data/expeditions.csv`, `data/expedition_events.csv`, `data/node_state_events.csv`, testes F5 e documentação;
- nenhum arquivo em `src/` ou `simulation/` foi alterado;
- nenhuma nova mecânica geral foi criada;
- `docs/roadmap.md` já havia sido atualizado no início da própria branch funcional após o fechamento documental, não sendo uma alteração incidental de mecânica.

## Estado de fechamento

Os critérios funcionais de F5 estão satisfeitos na branch:

- estado de `31/12/1505` determinístico;
- round-trip save/load validado;
- soberanias locais preservadas;
- divergências documentais mantidas;
- sem combate geral, schema global de governo ou múltiplas frotas ativas;
- regressão integral verde no HEAD funcional testado.

Próximo gate: preparar PR/merge de F5, executar CI pós-merge no `main` e então produzir o fechamento `domain-freeze-1505` / `Python 1505 GREEN` com contratos e golden states para a futura implementação em Godot.
