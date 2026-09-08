# F2 — Vasco da Gama 1502–1503 — checkpoint funcional v0.1

Data: 2026-09-08
Issue: #122
PR draft: #126
Baseline de origem: `24b6de7799f3ebb40c9a3401a73ddb5913d1190f`

## Escopo já validado

A primeira fatia funcional de F2 foi mantida deliberadamente estreita:

`LIS → SOF → KIL → CAN`

A partida principal em Lisboa é `EXACT` em 01/02/1502. Sofala, Quiloa e Cananor permanecem âncoras `INTERVAL`, sem fabricação de datas diárias. `voyage_observations.csv` não recebeu observações de Gama 1502.

## Rotas

- `R_LIS_SOF_GAMA1502`: nova aresta agregada, com partida documental e chegada apenas mensal; timing executável é `SIMULATION`;
- `R_SOF_KIL`: conexão da rede suaíli preexistente, reutilizada sem reclassificação como criação portuguesa; período estendido para cobrir 1502;
- `R_KIL_CAN_GAMA1502`: nova aresta agregada, sem materializar Melinde ou escalas intermediárias por analogia.

## Domínio

Foi criado `Gama1502CampaignModel` sobre `P3CampaignModel`, sem segundo motor de campanha.

O modelo:

- abre `EXP_GAMA_1502` em Lisboa em 01/02/1502;
- usa uma única `active_expedition_id`;
- expõe o evento `GAMA1502_E03 / FORCE_REMAINS` como estado histórico da força de Vicente Sodré;
- consulta os estados institucionais temporais de Cochim e Cananor por `NodeStateEventModel`;
- não cria `EXP_GAMA_RETURN_1503` nem `EXP_SODRE_1503` jogável neste checkpoint.

## Estados institucionais

A reorganização de Cochim e Cananor em 1502 já cabe no schema temporal existente:

- `COC1502_E01`: Diogo Fernandes Correia substitui Gonçalo Gil Barbosa;
- `CAN1502_E01`: Gonçalo Gil Barbosa assume Cananor.

A regra conservadora permanece: por serem intervalos 01/11–31/12/1502, os novos estados só se tornam efetivos em 31/12/1502. Os testes verificam que 30/12 ainda não aplica a reorganização e que as soberanias locais de Perumpadappu e Kolathunad são preservadas.

## Força residente

A força de Vicente Sodré é, neste gate, um evento histórico objetivo do mundo e não uma segunda frota ativa controlada pelo jogador.

`GAMA1502_E03` preserva:

- `trajectory_id=SODRE_FORCE`;
- `event_type=FORCE_REMAINS`;
- janela 01/01–31/03/1503.

O teste confirma que a sessão continua com `active_expedition_id=EXP_GAMA_1502` e que nenhum `EXP_SODRE_1503` é criado silenciosamente.

## Persistência

Foi acrescentado teste de round-trip após a primeira perna. O save deve preservar:

- seed;
- localização em Sofala;
- relógio;
- `active_expedition_id=EXP_GAMA_1502`;
- `expedition_leg_sequence=2`;
- `ChronologyMode.GUIDED`;
- capacidade de planejar `R_SOF_KIL` após recarga.

A força de Sodré continua fora do estado ativo do jogador e permanece consultável pela camada de eventos.

## CI

- primeiro gate funcional: push run `34185169750` — verde;
- pull request run `34185181343` — verde;
- gate de estados temporais COC/CAN: run `34185502124` — verde;
- teste de persistência: commit `f67c558e78836969cf399848a8f0dd2eb2e3e183`, CI disparada no run `34185542705`.

## Pendências antes de fechar F2

1. validar integralmente o round-trip de persistência;
2. reconstruir com maior precisão a ordem operacional Cananor–Cochim–Calecute na fase final de 1502;
3. determinar se Cochim precisa entrar no loop executável principal ou se a reorganização temporal do mundo é suficiente para o gate;
4. reconstruir a torna-viagem de Gama e o ponto de separação de Sodré somente até o grau documental defensável;
5. decidir, com base na implementação, se `EXP_SODRE_1503` precisa existir como subcampanha jogável ou se eventos/world-state são suficientes;
6. executar regressão integral e CI do PR final antes de merge.

## Decisão arquitetural provisória

Até este checkpoint, não há evidência de necessidade para múltiplas frotas simultâneas no save. `active_expedition_id` único + expedições/subcampanhas opcionais + `expedition_events` + `node_state_events` continuam suficientes. Qualquer ampliação de schema deve depender de uma lacuna funcional demonstrada, não de antecipação abstrata.