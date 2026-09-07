# P3-func-A — diário de implementação da tranche 1500–1503

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`

## Finalidade

Este documento registra as decisões de implementação tomadas ao transformar os gates documentais P3.1–P3.4 em software. A regra adotada é intercalar documentação e programação por tranche histórica: normalizar apenas o que já foi auditado, testar o domínio, identificar lacunas reais e somente então ampliar o recorte.

## Baseline preservado

- MVP Lisboa–Calecute: `f308fb0e97687e34365fd23ed257a0114fd81613`;
- retorno P1 estabilizado: `47fb82baad1289077c048576f3bc52815d6b192f`;
- P2 Cochim integrado: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`.

Nenhuma alteração desta tranche deve modificar o comportamento desses recortes quando P3 não estiver acionado.

## Primeira lacuna real: temporalidade dos nós

`nodes.csv` é uma fotografia estrutural e não consegue representar corretamente que Cochim tinha presença portuguesa desde 1500, reorganização em 1502 e fortificação/guarnição apenas em 1503. Alterar diretamente `COC.fortification` faria a fortaleza existir retroativamente.

Foi criada `data/node_state_events.csv` e o modelo somente-leitura `NodeStateEventModel`. A resolução temporal é conservadora: quando a fonte fornece intervalo, o evento só integra o estado efetivo depois do limite superior documentado. Isso evita antecipar feitorias, fortificações ou guarnições.

A tabela também mantém `sovereignty_note`, de modo que fortificação ou guarnição portuguesa não seja confundida com soberania portuguesa sobre Cochim.

## Segunda lacuna real: trajetórias e eventos durante a expedição

`expedition_epilogue_events.csv` resolvia apenas o trecho final do retorno de Gama. Cabral exige separações, perdas, destacamentos e consequências institucionais durante a própria campanha.

Foi criada `data/expedition_events.csv` e o modelo somente-leitura `ExpeditionEventModel`. A camada registra eventos documentais, variantes, trajetórias e aquisição de informação, mas não produz automaticamente efeitos materiais, combate, naufrágio ou múltiplas frotas simuladas.

Isso permite adiar sistemas gerais até que a execução demonstre necessidade real.

## Nós acrescentados

- `VCR`: Terra de Vera Cruz / Porto Seguro, como `ANCHORAGE`, âncora regional de confiança `MEDIUM`, sem mercado;
- `CAN`: Cananor/Kannur, como `FOREIGN_PORT`, soberania local e sem fortificação portuguesa retroativa.

## Expedições documentais normalizadas

Foram acrescentadas a `expeditions.csv`:

- `EXP_CABRAL_1500`;
- `EXP_JOAO_NOVA_1501`;
- `EXP_GAMA_1502`.

A presença no arquivo não significa que toda a campanha já seja executável. A expansão das pernas é incremental.

## Primeiro gate verde da camada temporal

O run `34131516997`, commit `34a8fafc2b3a605fea18e882520ea5a59432ce4c`, passou integralmente: validação dos dados, 257 testes de domínio, protótipos, retorno, diagnósticos, interfaces, persistência e cartografia.

Esse run fixa o primeiro baseline da arquitetura temporal P3.

## Primeira campanha P3 executável

Foi criada a fachada `P3CampaignModel`, que reutiliza integralmente `HistoricalCampaignModel`. Não existe segundo motor de campanha.

A primeira perna normalizada é:

`EXP_CABRAL_1500 / 1: LIS → VCR`, rota `R_LIS_VCR_CAB`.

A autorização usa `FLEET_COMMAND`: a participação na armada permite navegar a perna sem conceder conhecimento náutico operacional antes da partida. Após completar a viagem, o domínio existente eleva corretamente a experiência da rota a `OPERATIONAL`.

O run `34132142727`, commit `dcc09234cdaf760f561ed599e8bdeb3cbf5b3216`, passou integralmente após corrigir um teste que confundia autorização institucional com aprendizagem posterior à viagem.

## Cronologia Lisboa–Vera Cruz ancorada

A documentação sustenta partida em `1500-03-09` e avistamento de Vera Cruz em `1500-04-22`, diferença operacional de 44 dias. A primeira tentativa de escrever essa linha em `voyage_observations.csv` pela API de conteúdo foi bloqueada antes de chegar ao GitHub.

A pendência foi resolvida sem mudar o schema: o arquivo foi reconstruído como blob Git, preservando todas as observações anteriores e acrescentando `CABRAL1500_LIS_VCR`. O commit `5deefbd83835d68f9d9793de0b99e6a0f0f7b57c` passou a fornecer a duração documental à rota.

O teste P3 exige agora explicitamente `travel_days == 44`, `arrival_date == 1500-04-22` e relógio da sessão em 22/04 após a execução. O run `34132527761`, commit `6a6a0713ca0de670c6c79635760f80cd1b8428a3`, passou integralmente.

A duração Lisboa–Vera Cruz deixa, portanto, de ser provisória. Continua sendo uma observação histórica específica da viagem de Cabral, não uma velocidade universal para travessias atlânticas.

## Próximos gates da implementação

1. normalizar a permanência em Vera Cruz até 02/05/1500 para impedir partida guiada prematura;
2. expandir Cabral por incrementos: `VCR → CGH → MOZ → KIL → MAL → ANJ → CAL`, usando datas observadas apenas onde o corpus sustenta precisão suficiente;
3. projetar a ruptura de Calecute e os estados de Cochim/Cananor a partir das novas camadas temporais, sem combate genérico;
4. completar o retorno principal de Cabral mantendo perdas e trajetórias assíncronas em `expedition_events.csv`;
5. integrar João da Nova e demonstrar em teste que a informação de São Brás não existe no estado inicial em Lisboa;
6. integrar Gama 1502 e a bifurcação de Vicente Sodré como subcampanha separada, se o modelo atual continuar suficiente;
7. executar smoke reproduzível da tranche 1500–1503, regressão integral e somente então preparar merge.

## Regra de continuidade

P3.5/1504 permanece aberto documentalmente, mas não bloqueia esta tranche. A pesquisa de 1504–1505 deve ser retomada depois que P3-func-A mostrar quais estruturas de conflito, fortificação e presença residente são efetivamente necessárias ao jogo.