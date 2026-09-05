# Método da campanha histórica Lisboa–Calecute

## Escopo

Este documento descreve a camada mínima usada para tornar contínua a primeira viagem de 1497–1498 na vertical slice do MVP.

A sequência executável é:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`.

A campanha não acrescenta novas rotas, novas datas históricas, novas permanências ou novos recursos documentais. Ela apenas coordena dados que já existem em `expedition_routes.csv`, `expedition_stops.csv` e `voyage_observations.csv`.

## Três coisas que permanecem separadas

1. `expedition_routes.csv` define a ordem institucional das pernas da armada e a base `FLEET_COMMAND`.
2. `expedition_stops.csv` contém somente as permanências normalizadas como escalas históricas: São Thiago, baía de Santa Helena, São Brás, Rio do Cobre e Rio dos Bons Sinais.
3. `voyage_observations.csv` registra partidas, chegadas e durações observadas ou reconstruídas pelas fontes. Uma data de partida observada não transforma automaticamente o nó de origem em uma permanência normalizada.

Por isso, Moçambique, Mombaça e Melinde não são acrescentados a `expedition_stops.csv` neste gate. A interface pode aguardar até 29 de março, 13 de abril e 24 de abril porque essas datas já são partidas registradas em `voyage_observations.csv`; essa espera significa apenas sincronização do relógio em cronologia `GUIDED`.

## `HistoricalCampaignModel`

`src/quintoimperio/domain/campaign.py` compõe `GameSessionModel` e acrescenta apenas a orquestração necessária ao percurso histórico.

Responsabilidades:

- identificar a perna corrente da expedição;
- recuperar a data de partida observada da perna corrente quando ela é inequívoca;
- impedir partida anterior a essa data em `GUIDED`;
- esperar explicitamente até a partida observada sem conceder recursos;
- preservar `wait_for_stop_release` quando existe uma permanência normalizada;
- selecionar um piloto apenas quando `TravelModel.pilot_can_guide` confirma a competência histórica;
- converter a sessão para `COUNTERFACTUAL` quando a partida ocorre depois da data guiada.

A camada não altera preços, provisões, desgaste, acesso, conhecimento, relações ou duração de viagem.

## Espera guiada

`wait_for_guided_departure` tem duas semânticas deliberadamente distintas:

- quando existe `active_stop_id`, delega para a permanência normalizada e sua data de liberação;
- quando não existe permanência normalizada, avança somente o calendário até a próxima data de partida observada da perna corrente.

Nenhum dos casos concede provisões, reparos, mercadorias, capital, conhecimento, relação ou acesso. Serviços continuam ações explícitas e consomem o mesmo `GameClock`.

## Divergência histórica

Em `GUIDED`, partida precoce é bloqueada. Partida na data observada preserva a precedência da observação já implementada em `NavigationModel` e suprime eventos aleatórios quando aplicável.

Se o jogador utiliza o tempo para outras ações e parte depois da data observada, a viagem é permitida, mas a sessão passa a `COUNTERFACTUAL`. A partir daí a campanha não força retorno silencioso à cronologia histórica.

## Piloto de Melinde

Na perna `R_MAL_CAL`, `HistoricalCampaignModel` procura um piloto elegível por meio das regras existentes. Em 24 de abril de 1498, o piloto `PIL_MAL_GUJ_1498` é selecionado porque sua disponibilidade e competência estão documentadas na base.

O piloto fornece somente a base de navegação `PILOT`. Não recebe bônus quantitativo de velocidade, consumo, desgaste ou êxito.

## Provisões e serviços

A campanha de integração usa as mesmas regras abstratas de provisões já existentes. Para permanecer jogável sem concessões automáticas, o smoke test realiza ações explícitas de reabastecimento nos nós em que `nodes.csv` documenta disponibilidade suficiente e o serviço é acionável.

Isso é parâmetro de simulação e não reconstrução de quantidade histórica embarcada.

## Critérios de regressão

Os testes devem garantir:

- dez pernas percorridas na ordem normalizada;
- exatamente as cinco permanências de `expedition_stops.csv` reconhecidas como escalas normalizadas;
- ações durante uma escala consumindo o mesmo calendário e reduzindo a espera restante;
- bloqueio de partida precoce mesmo em nó sem permanência normalizada quando existe partida observada da perna guiada;
- atraso convertendo a sessão para `COUNTERFACTUAL` sem retorno automático a `GUIDED`;
- `STRATEGIC_AGGREGATE` permanecendo não executável;
- Melinde–Calecute usando o piloto documentado quando elegível;
- chegada a Calecute deixando conhecimento de mercado e acesso institucional como estados separados;
- smoke test Pygame percorrendo a campanha pela camada de ações da interface, sem cenário `TECHNICAL`.
