# Método de sessão integrada v0.1

## Objetivo

Compor os módulos já existentes em um primeiro ciclo contínuo de jogo. `GameSessionModel` não cria nova evidência histórica: ele coordena conhecimento, aquisição de informação, comércio, serviços portuários, expedições, permanências, eventos marítimos de simulação e viagem e aplica somente regras explícitas de simulação.

## Estado

`GameSessionState` é imutável e reúne:

- `VesselState`: localização, calendário, provisões e condição;
- `CommercialState`: capital, capacidade e carga abstratos;
- conhecimento do personagem por nó;
- conhecimento náutico do personagem por rota;
- `information_history`, com oportunidades informativas já consumidas;
- `voyage_event_history`, com eventos de simulação efetivamente aplicados às viagens;
- expedição ativa opcional e número da perna corrente;
- `chronology_mode` (`GUIDED` ou `COUNTERFACTUAL`);
- `active_stop_id`, quando a chegada corresponde a uma permanência documentada.

O conhecimento de rota é deliberadamente separado do conhecimento do porto. Saber onde Calecute está ou conhecer seu mercado não torna automaticamente operacional uma ligação marítima Calecute–Aden, Calecute–Hurmuz ou Calecute–Melaka. Do mesmo modo, participar de uma armada que percorre uma rota não torna o personagem conhecedor daquela rota antes da experiência.

## Conhecimento inicial e aquisição ativa

`RouteKnowledgeModel` lê `player_knowledge_default` e `crown_knowledge_1497` de `data/routes.csv` e converte esses estados usando `simulation/route_knowledge_rules.csv`. Personagem e Coroa permanecem perspectivas distintas.

`InformationModel` acrescenta uma segunda via de aprendizado, acionada pelo jogador. Ela não consulta nem copia o estado `CROWN`. Seus alvos provêm exclusivamente de rotas de saída já documentadas e excluem `STRATEGIC_AGGREGATE`.

Na v0.1:

- `RUMOR` pode elevar geografia/rota apenas até `RUMORED`;
- `MERCHANT_CONTACT` pode elevar geografia e mercado até `PARTIAL`, política e rota apenas até `RUMORED`;
- `PILOT_CONSULTATION` exige piloto historicamente registrado para a rota e pode elevá-la somente até `PARTIAL`.

Cada oportunidade possui ID estável e só pode ser usada uma vez por sessão. A escolha entre vários alvos é determinística para a mesma semente, nó, data e canal. A interface não expõe o alvo antes da ação.

Toda interação custa um dia na v0.1, segundo `simulation/information_rules.csv`. Esse valor é parâmetro de jogabilidade, não duração histórica de uma conversa. Ver `docs/information-method.md`.

## Expedições e comando institucional

`ExpeditionModel` lê `data/expeditions.csv` e `data/expedition_routes.csv`. A primeira expedição normalizada é `EXP_GAMA_1497`, com dez pernas operacionais até Calecute. As conexões Lisboa–Cabo e Cabo–Moçambique permanecem apenas como `STRATEGIC_AGGREGATE` e são bloqueadas para execução como uma única viagem.

Uma sessão pode possuir `active_expedition_id` e `expedition_leg_sequence`. Quando a rota escolhida coincide com a perna corrente, o período é válido e a tabela histórica registra `FLEET_COMMAND`, a viagem recebe essa base institucional.

As bases de viagem são distintas:

1. `OWN_KNOWLEDGE` quando o personagem possui conhecimento operacional;
2. `PILOT` quando um piloto historicamente registrado é competente para a rota e o conhecimento próprio não basta;
3. `FLEET_COMMAND` quando a perna corrente da expedição autoriza participação sob comando institucional.

Assim, o piloto guzerate de Melinde continua sendo a base específica da travessia Melinde–Calecute quando fornecido ao plano, mesmo se a armada estiver ativa. Uma simples `PILOT_CONSULTATION` não equivale a essa base operacional: ela ensina apenas até `PARTIAL`.

Depois de completar uma perna da expedição, a sessão avança para a próxima. Ao concluir a última, os campos de expedição ativa voltam a `None`. A camada não fixa identidade, profissão, navio ou estatuto social do protagonista.

## Permanências e cronologia

`ExpeditionStopModel` lê `data/expedition_stops.csv`. Quando uma perna institucional termina em um nó com permanência registrada, a sessão guarda `active_stop_id`.

O modo histórico inicia como `ChronologyMode.GUIDED`. A regra v0.1 é estrita e auditável: para continuar guiada, a data de chegada precisa coincidir com `arrival_date` da escala. Não existe tolerância silenciosa de alguns dias.

Enquanto uma escala guiada está ativa e a data atual é anterior à partida documentada, `plan_voyage()` acrescenta o bloqueio `HISTORICAL_STOP_NOT_RELEASED`.

`wait_for_stop_release()` avança apenas o relógio até a data de partida. Não altera provisões, condição, carga, capital ou conhecimento.

Reabastecimento, reparo e aquisição de informação avançam o mesmo calendário. Assim, uma dessas ações pode consumir parte da permanência documentada sem receber efeito automático apenas porque a fonte registra `WATER`, `CARENING` ou `MAST_REPAIR`.

Se o jogador permanece além da partida documentada e então executa nova viagem, a sessão muda para `ChronologyMode.COUNTERFACTUAL`. A partir daí as escalas históricas podem continuar sendo exibidas como contexto, mas deixam de impor espera para reproduzir datas documentadas.

A distinção entre duração narrada e cronologia editorial é preservada: `observed_stay_days` não é recalculado a partir das datas. A baía de Santa Helena, por exemplo, mantém oito dias narrados e uma diferença aritmética de nove dias entre as datas editoriais 7–16 de novembro. Ver `docs/stop-method.md`.

## Mercado e serviços portuários

O mercado do porto atual só é operacional quando `market_knowledge >= OPERATIONAL`. Antes disso a sessão não expõe cotações nem permite compra/venda. Quando operacional, a sessão delega cotações e operações ao `TradeModel`; nenhuma mercadoria ausente de `node_goods.csv` é criada para completar o loop. Ancoradouros logísticos com `market_scale=NONE` não recebem mercado apenas por serem escalas documentadas.

`PortServiceModel` mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` separados. Reabastecimento e reparo alteram calendário e estado do navio apenas pelas regras de simulação correspondentes. Nenhum custo monetário histórico é inventado.

O limite máximo abstrato de provisões foi ampliado para comportar a perna observada São Thiago–baía de Santa Helena. Esse valor não representa tonelagem, ração diária, água por tripulante ou capacidade histórica de uma embarcação.

## Navegação, observações e eventos marítimos

A sessão delega duração e execução ao `TravelModel`/`NavigationModel`. Observações documentadas para a rota e data exatas têm precedência sobre extrapolações geodésicas.

A partida histórica inicial é `R_LIS_STG`: 8 de julho de 1497 até São Thiago/baía de Santa Maria. O itinerário segue depois por baía de Santa Helena, Cabo, São Brás, Rio do Cobre, Rio dos Bons Sinais e Moçambique. Datas reconstruídas entre colchetes pela edição Ravenstein do `Roteiro` são marcadas como editoriais nas notas de evidência.

A observação agregada Lisboa–Cabo de Subrahmanyam continua preservada para comparação historiográfica, mas `R_LIS_CGH` não é executável como uma única viagem.

`GameSessionModel.plan_voyage()` conecta explicitamente cronologia e risco marítimo:

- em `GUIDED`, `preserve_observed_timing=True`; se rota/data tiver observação exata, `TravelModel` marca `events_suppressed_by_observation=True` e não aplica evento aleatório;
- em `COUNTERFACTUAL`, `preserve_observed_timing=False`; mesmo uma rota/data historicamente observada pode receber evento de simulação, porque a sessão já não está obrigada a reproduzir a cronologia documental;
- quando não há observação exata, eventos podem ocorrer em ambos os modos.

Os eventos vêm de `VoyageEventModel` e `simulation/voyage_event_rules.csv`. A v0.1 permite somente tempo adicional, consumo correspondente de provisões e perda abstrata de condição. O plano registra os eventos e a sessão os acrescenta a `voyage_event_history`. Eles permanecem marcados como `simulation_only=True`; não são tratados como tempestades, calmarias ou avarias historicamente atestadas. Ver `docs/voyage-event-method.md`.

## Aprendizagem por experiência

`simulation/session_rules.csv` contém os mínimos de aprendizagem aplicados após uma chegada física e após completar uma rota. Na v0.1:

- localização do destino torna-se `CONFIRMED`;
- conhecimento náutico do nó torna-se pelo menos `PARTIAL`;
- mercado do destino torna-se pelo menos `OPERATIONAL`;
- conhecimento político torna-se pelo menos `PARTIAL`;
- a rota efetivamente completada torna-se pelo menos `OPERATIONAL`.

Esses níveis continuam distintos dos canais de informação: experiência física pode produzir `OPERATIONAL`, enquanto rumor, contato mercantil e consulta a piloto permanecem deliberadamente abaixo desse patamar.

## Cenário técnico e interface

O protótipo também executa Calecute → Aden com conhecimento operacional concedido explicitamente por métodos `scenario_*`. Esse cenário existe somente para testar a cadeia `mercado → compra → viagem → chegada → venda` e não representa o estado histórico inicial do personagem.

A interface Pygame chama diretamente os métodos desta sessão para informação, mercado, compra, venda, reabastecimento, reparo, espera, planejamento e execução de viagem. No modo `HISTORICAL`, a sessão começa em 8 de julho de 1497 associada a `EXP_GAMA_1497`; no modo `TECHNICAL`, continua explicitamente contrafactual. Quando uma viagem recebe evento de simulação, a mensagem de chegada e o painel podem exibir o último evento como `SIM`; quando a observação histórica suprimiu a aleatoriedade, a mensagem de chegada explicita essa precedência.

## Próximos passos

Com itinerário, permanências, aquisição básica de informação e risco marítimo inicial integrados, a próxima camada do loop é regime de acesso/negociação institucional e reputação. Cartas persistentes, desinformação, perdas materiais severas, tripulação, combate e naufrágio ficam para camadas posteriores.
