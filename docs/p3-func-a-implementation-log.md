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

## Vera Cruz e correção da passagem pelo Cabo

A escala `CABRAL1500_VCR` foi normalizada de 22/04 a 02/05/1500. O modo guiado bloqueia a partida antes de 02/05 por `HISTORICAL_STOP_NOT_RELEASED`, sem conceder mercado, assentamento ou abastecimento genérico em Vera Cruz.

Uma primeira tentativa operacional segmentou a sequência como `VCR → CGH`. A CI `34133197779` revelou apenas dois erros de teste — chamadas a APIs inexistentes — e não falha de dados ou domínio. Os testes foram corrigidos no commit `dd75a80375ea157f6eb4c8d72e458bd05cbd9d78`; a CI `34133817081` fechou integralmente verde.

A auditoria posterior do modo guiado mostrou, porém, que `CGH` não deve ser endpoint operacional: não há data segura de partida do Cabo para 1500. Sem observação, `guided_departure_date()` retornaria `None` e a campanha poderia sair do marco sem vínculo cronológico. Para não fabricar uma escala, `R_VCR_CGH_CAB` foi reclassificada como `STRATEGIC_AGGREGATE` e a perna executável passou a ser `R_VCR_MOZ_CAB`.

A observação `CABRAL1500_VCR_MOZ` usa 02/05 → 20/07/1500, 79 dias, como agregação operacional. As perdas de quatro embarcações e a separação de Diogo Dias permanecem em `expedition_events.csv`, localizadas no marco `CGH`, sem sistema geral de naufrágio. O run `34134148269`, commit `01cdd1ed53480c5423e227a834b444a88eb8c84e`, passou integralmente, inclusive interfaces, persistência e cartografia.

## Moçambique e Quiloa

A campanha foi estendida por `R_MOZ_KIL_CAB`, com observação 20/07 → 26/07/1500. Não foi criada escala em Moçambique: o nó funciona aqui como referência/passagem da cronologia especializada.

Em Quiloa foi criada a escala `CABRAL1500_KIL`, de 26/07 a 29/07, com atividade mínima `FLEET_REUNION`. A linha registra apenas a reunião documentada de seis embarcações; não infere mercado, abastecimento ou efeitos diplomáticos.

O teste da campanha percorre Lisboa → Vera Cruz → Moçambique → Quiloa, exige 44, 79 e 6 dias respectivamente e verifica a ativação da escala em Quiloa. O run `34134459694`, commit `c4a6da0bc81a208f33f754819e86bbbf6163607d`, passou integralmente.

## Melinde e os dois pilotos guzerates

A matriz documental registra chegada a Melinde em 02/08/1500, obtenção de dois pilotos guzerates em 06/08 e partida em 07/08. O modelo atual trata `pilot_id` como entidade operacional individual e `recommended_pilot_id()` retorna um único piloto elegível.

Por isso, não será reutilizado `PIL_MAL_GUJ_1498` e não será criado um falso “piloto coletivo”. No próximo incremento, a chegada e permanência em Melinde podem ser normalizadas e a obtenção dos dois pilotos registrada inicialmente como evento documental. A transformação desses dois indivíduos não identificados em entidades operacionais ficará condicionada à normalização da rota específica que efetivamente guiaram.

## Próximos gates da implementação

1. normalizar `KIL → MAL`, escala de Melinde 02–07/08 e evento documental dos dois pilotos guzerates em 06/08;
2. auditar a cronologia fina Melinde → costa indiana → Anjediva antes de criar uma perna guiada, evitando derivar uma data de chegada a Anjediva apenas da expressão “cerca de duas semanas”;
3. avançar para Calecute e projetar a ruptura de dezembro a partir das camadas temporais, sem combate genérico;
4. completar Cochim, Cananor e o retorno principal de Cabral mantendo perdas e trajetórias assíncronas em `expedition_events.csv`;
5. integrar João da Nova e demonstrar em teste que a informação de São Brás não existe no estado inicial em Lisboa;
6. integrar Gama 1502 e a bifurcação de Vicente Sodré como subcampanha separada, se o modelo atual continuar suficiente;
7. executar smoke reproduzível da tranche 1500–1503, regressão integral e somente então preparar merge.

## Regra de continuidade

P3.5/1504 permanece aberto documentalmente, mas não bloqueia esta tranche. A pesquisa de 1504–1505 deve ser retomada depois que P3-func-A mostrar quais estruturas de conflito, fortificação e presença residente são efetivamente necessárias ao jogo.