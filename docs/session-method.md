# Método de sessão integrada v0.1

## Objetivo

Compor os módulos já existentes em um primeiro ciclo contínuo de jogo. `GameSessionModel` não cria nova evidência histórica: ele coordena conhecimento, aquisição de informação, acesso institucional, comércio, serviços portuários, expedições, permanências, eventos marítimos de simulação e viagem e aplica somente regras explícitas de simulação.

## Estado

`GameSessionState` é imutável e reúne:

- `VesselState`: localização, calendário, provisões e condição;
- `CommercialState`: capital, capacidade e carga abstratos;
- conhecimento do personagem por nó;
- conhecimento náutico do personagem por rota;
- `access_records`, com estado institucional por nó;
- `information_history`, com oportunidades informativas já consumidas;
- `voyage_event_history`, com eventos de simulação efetivamente aplicados às viagens;
- expedição ativa opcional e número da perna corrente;
- `chronology_mode` (`GUIDED` ou `COUNTERFACTUAL`);
- `active_stop_id`, quando a chegada corresponde a uma permanência documentada.

Conhecimento, acesso e capacidade de viajar são deliberadamente separados. Saber onde Calecute está, conhecer seu mercado ou chegar fisicamente ao porto não concede automaticamente autorização comercial. Do mesmo modo, participar de uma armada que percorre uma rota não torna o personagem conhecedor daquela rota antes da experiência.

## Conhecimento inicial e aquisição ativa

`RouteKnowledgeModel` lê `player_knowledge_default` e `crown_knowledge_1497` de `data/routes.csv` e converte esses estados usando `simulation/route_knowledge_rules.csv`. Personagem e Coroa permanecem perspectivas distintas.

`InformationModel` acrescenta uma segunda via de aprendizado, acionada pelo jogador. Ela não consulta nem copia o estado `CROWN`. Seus alvos provêm exclusivamente de rotas de saída já documentadas e excluem `STRATEGIC_AGGREGATE`.

Na v0.1:

- `RUMOR` pode elevar geografia/rota apenas até `RUMORED`;
- `MERCHANT_CONTACT` pode elevar geografia e mercado até `PARTIAL`, política e rota apenas até `RUMORED`;
- `PILOT_CONSULTATION` exige piloto historicamente registrado para a rota e pode elevá-la somente até `PARTIAL`.

Cada oportunidade possui ID estável e só pode ser usada uma vez por sessão. A escolha entre vários alvos é determinística para a mesma semente, nó, data e canal. A interface não expõe o alvo antes da ação.

Toda interação custa um dia na v0.1, segundo `simulation/information_rules.csv`. Esse valor é parâmetro de jogabilidade, não duração histórica de uma conversa. Ver `docs/information-method.md`.

## Acesso institucional e negociação

`AccessModel` lê `access_regime` de `nodes.csv` e o traduz por `simulation/access_rules.csv`. O estado de acesso não é conhecimento nem reputação.

A v0.1 distingue:

- `OPEN`;
- `NEGOTIATION_REQUIRED`;
- `NEGOTIATED`;
- `RESTRICTED`;
- `NONCOMMERCIAL`;
- `UNKNOWN`.

`OPEN_MARKET` e `CAPTAINCY` começam como `OPEN`. `FOREIGN_NEGOTIATED` começa como `NEGOTIATION_REQUIRED`. `ROYAL_MONOPOLY`, `ROYAL_MONOPOLY_LEASED` e `MILITARY_POST` permanecem `RESTRICTED`. `ANCHORAGE_CONTACT` e `NAVIGATION_ONLY` permanecem `NONCOMMERCIAL`.

`negotiate_access()` só atua sobre o gate `FOREIGN_NEGOTIATED`. Na v0.1 a ação não sorteia êxito: ela representa a conclusão abstrata da mediação institucional necessária e consome um dia de simulação. Não há taxa, valor de presente, comissão, suborno, tributo ou diálogo inventado.

A ausência de `broker_availability` não é interpretada como inexistência de intermediário. Quando o campo existe, pode ser exibido como contexto; o gate estrutural continua sendo `access_regime`.

O mercado conhecido pode ser consultado mesmo se o acesso não estiver concedido. `MarketView` expõe separadamente `knowledge_level`, `access_status` e `actionable`. Assim, `market_knowledge >= OPERATIONAL` permite conhecer a cesta/cotação da simulação, mas compra/venda continuam bloqueadas enquanto o acesso institucional não for `OPEN` ou `NEGOTIATED`.

`node_goods.restricted=TRUE` é um segundo bloqueio, independente. `TradeModel` rejeita diretamente esses bens. Portanto `scenario_set_access()` ou uma negociação portuária não transforma ouro de Arguim/Elmina em comércio ordinário. Ver `docs/access-method.md`.

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

`wait_for_stop_release()` avança apenas o relógio até a data de partida. Não altera provisões, condição, carga, capital, conhecimento ou acesso.

Reabastecimento, reparo, aquisição de informação e negociação de acesso avançam o mesmo calendário. Assim, uma ação pode consumir parte da permanência documentada sem receber efeito automático apenas porque a fonte registra `WATER`, `CARENING` ou `MAST_REPAIR`.

Se o jogador permanece além da partida documentada e então executa nova viagem, a sessão muda para `ChronologyMode.COUNTERFACTUAL`. A partir daí as escalas históricas podem continuar sendo exibidas como contexto, mas deixam de impor espera para reproduzir datas documentadas.

A distinção entre duração narrada e cronologia editorial é preservada: `observed_stay_days` não é recalculado a partir das datas. Ver `docs/stop-method.md`.

## Mercado e serviços portuários

Se `market_knowledge < OPERATIONAL`, a sessão não expõe cotações nem permite compra/venda. Quando o conhecimento é operacional, as cotações podem ser consultadas; a operação comercial ainda depende de `AccessModel` e das restrições específicas de `TradeModel`.

Ancoradouros logísticos com `market_scale=NONE` não recebem mercado apenas por serem escalas documentadas.

`PortServiceModel` mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` separados. Reabastecimento e reparo alteram calendário e estado do navio apenas pelas regras de simulação correspondentes. Nenhum custo monetário histórico é inventado.

O limite máximo abstrato de provisões foi ampliado para comportar a perna observada São Thiago–baía de Santa Helena. Esse valor não representa tonelagem, ração diária, água por tripulante ou capacidade histórica de uma embarcação.

## Navegação, observações e eventos marítimos

A sessão delega duração e execução ao `TravelModel`/`NavigationModel`. Observações documentadas para a rota e data exatas têm precedência sobre extrapolações geodésicas.

A partida histórica inicial é `R_LIS_STG`: 8 de julho de 1497 até São Thiago/baía de Santa Maria. O itinerário segue depois por baía de Santa Helena, Cabo, São Brás, Rio do Cobre, Rio dos Bons Sinais e Moçambique. Datas reconstruídas entre colchetes pela edição Ravenstein do `Roteiro` são marcadas como editoriais nas notas de evidência.

A observação agregada Lisboa–Cabo de Subrahmanyam continua preservada para comparação historiográfica, mas `R_LIS_CGH` não é executável como uma única viagem.

`GameSessionModel.plan_voyage()` conecta explicitamente cronologia e risco marítimo:

- em `GUIDED`, `preserve_observed_timing=True`; se rota/data tiver observação exata, `TravelModel` marca `events_suppressed_by_observation=True` e não aplica evento aleatório;
- em `COUNTERFACTUAL`, `preserve_observed_timing=False`; mesmo uma rota/data historicamente observada pode receber evento de simulação;
- quando não há observação exata, eventos podem ocorrer em ambos os modos.

Os eventos vêm de `VoyageEventModel` e `simulation/voyage_event_rules.csv`. A v0.1 permite somente tempo adicional, consumo correspondente de provisões e perda abstrata de condição. O plano registra os eventos e a sessão os acrescenta a `voyage_event_history`. Eles permanecem marcados como `simulation_only=True`. Ver `docs/voyage-event-method.md`.

## Aprendizagem por experiência

`simulation/session_rules.csv` contém os mínimos de aprendizagem aplicados após uma chegada física e após completar uma rota. Na v0.1:

- localização do destino torna-se `CONFIRMED`;
- conhecimento náutico do nó torna-se pelo menos `PARTIAL`;
- mercado do destino torna-se pelo menos `OPERATIONAL`;
- conhecimento político torna-se pelo menos `PARTIAL`;
- a rota efetivamente completada torna-se pelo menos `OPERATIONAL`.

Esses níveis continuam distintos dos canais de informação e do acesso institucional. Chegar a Calecute pode produzir conhecimento comercial `OPERATIONAL`, mas o estado de acesso continua `NEGOTIATION_REQUIRED` até uma ação separada.

## Cenário técnico e interface

O protótipo Calecute → Aden concede explicitamente conhecimento/rota e acesso inicial de Calecute por métodos `scenario_*`. Esse cenário existe somente para testar integração e não representa o estado histórico inicial do personagem. Na chegada a Aden, o acesso volta a obedecer à regra normal `FOREIGN_NEGOTIATED`, permitindo exercitar `negotiation → sale` no mesmo loop.

A interface Pygame chama diretamente os métodos desta sessão para acesso, informação, mercado, compra, venda, reabastecimento, reparo, espera, planejamento e execução de viagem. O painel mostra o estado de acesso e só oferece `Negociar acesso` quando `AccessView.negotiable=True`. Mercados conhecidos mas bloqueados por acesso podem ser lidos, porém os botões de compra/venda permanecem desabilitados.

## Próximos passos

Com itinerário, permanências, aquisição de informação, acesso institucional e risco marítimo inicial integrados, a próxima camada é relação/reputação diferenciada com autoridades e comunidades mercantis. Cartas persistentes, desinformação, perdas materiais severas, tripulação, combate e naufrágio ficam para camadas posteriores.
