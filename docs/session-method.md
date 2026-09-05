# Método de sessão integrada v0.1

## Objetivo

Compor os módulos já existentes em um primeiro ciclo contínuo de jogo. `GameSessionModel` não cria nova evidência histórica: ele coordena conhecimento, comércio, serviços portuários, expedições, permanências e viagem e aplica somente regras explícitas de simulação.

## Estado

`GameSessionState` é imutável e reúne:

- `VesselState`: localização, calendário, provisões e condição;
- `CommercialState`: capital, capacidade e carga abstratos;
- conhecimento do personagem por nó;
- conhecimento náutico do personagem por rota;
- expedição ativa opcional e número da perna corrente;
- `chronology_mode` (`GUIDED` ou `COUNTERFACTUAL`);
- `active_stop_id`, quando a chegada corresponde a uma permanência documentada.

O conhecimento de rota é deliberadamente separado do conhecimento do porto. Saber onde Calecute está ou conhecer seu mercado não torna automaticamente operacional uma ligação marítima Calecute–Aden, Calecute–Hurmuz ou Calecute–Melaka. Do mesmo modo, participar de uma armada que percorre uma rota não torna o personagem conhecedor daquela rota antes da experiência.

## Conhecimento inicial de rota

`RouteKnowledgeModel` lê `player_knowledge_default` e `crown_knowledge_1497` de `data/routes.csv` e converte esses estados usando `simulation/route_knowledge_rules.csv`.

A conversão é parâmetro de simulação. Na v0.1:

- `PLAYER/MEDIUM` produz conhecimento `PARTIAL`;
- `PLAYER/UNKNOWN` permanece `UNKNOWN`;
- `CROWN/HIGH` produz conhecimento `OPERATIONAL`;
- estados `LOW` e `INDIRECT` da Coroa permanecem abaixo do nível operacional.

## Expedições e comando institucional

`ExpeditionModel` lê `data/expeditions.csv` e `data/expedition_routes.csv`. A primeira expedição normalizada é `EXP_GAMA_1497`, com dez pernas operacionais até Calecute. As conexões Lisboa–Cabo e Cabo–Moçambique permanecem apenas como `STRATEGIC_AGGREGATE` e são bloqueadas para execução como uma única viagem.

Uma sessão pode possuir `active_expedition_id` e `expedition_leg_sequence`. Quando a rota escolhida coincide com a perna corrente, o período é válido e a tabela histórica registra `FLEET_COMMAND`, a viagem recebe essa base institucional.

Isso não altera o conhecimento pessoal antes da partida. As bases de viagem são distintas:

1. `OWN_KNOWLEDGE` quando o personagem possui conhecimento operacional;
2. `PILOT` quando um piloto historicamente registrado é competente para a rota e o conhecimento próprio não basta;
3. `FLEET_COMMAND` quando a perna corrente da expedição autoriza participação sob comando institucional.

Assim, o piloto guzerate de Melinde continua sendo a base específica da travessia Melinde–Calecute quando fornecido ao plano, mesmo se a armada estiver ativa.

Depois de completar uma perna da expedição, a sessão avança para a próxima. Ao concluir a última, os campos de expedição ativa voltam a `None`. A camada não fixa identidade, profissão, navio ou estatuto social do protagonista.

## Permanências e cronologia

`ExpeditionStopModel` lê `data/expedition_stops.csv`. Quando uma perna institucional termina em um nó com permanência registrada, a sessão guarda `active_stop_id`.

O modo histórico inicia como `ChronologyMode.GUIDED`. A regra v0.1 é estrita e auditável: para continuar guiada, a data de chegada precisa coincidir com `arrival_date` da escala. Não existe tolerância silenciosa de alguns dias.

Enquanto uma escala guiada está ativa e a data atual é anterior à partida documentada, `plan_voyage()` acrescenta o bloqueio `HISTORICAL_STOP_NOT_RELEASED`.

`wait_for_stop_release()` avança apenas o relógio até a data de partida. Não altera provisões, condição, carga, capital ou conhecimento.

Reabastecimento e reparo continuam sendo ações independentes e avançam o mesmo calendário. Assim, um serviço pode consumir parte da permanência documentada sem receber efeito automático apenas porque a fonte registra `WATER`, `CARENING` ou `MAST_REPAIR`.

Se o jogador permanece além da partida documentada e então executa nova viagem, a sessão muda para `ChronologyMode.COUNTERFACTUAL`. A partir daí as escalas históricas podem continuar sendo exibidas como contexto, mas deixam de impor espera para reproduzir datas documentadas.

A distinção entre duração narrada e cronologia editorial é preservada: `observed_stay_days` não é recalculado a partir das datas. A baía de Santa Helena, por exemplo, mantém oito dias narrados e uma diferença aritmética de nove dias entre as datas editoriais 7–16 de novembro. Ver `docs/stop-method.md`.

## Mercado

O mercado do porto atual só é operacional quando `market_knowledge >= OPERATIONAL`. Antes disso a sessão não expõe cotações nem permite compra/venda. Isso evita que a interface revele toda a cesta comercial histórica a um personagem que apenas ouviu falar do lugar.

Quando operacional, a sessão delega cotações e operações ao `TradeModel`; nenhuma mercadoria ausente de `node_goods.csv` é criada para completar o loop. Ancoradouros logísticos com `market_scale=NONE` não recebem mercado apenas por serem escalas documentadas.

## Serviços portuários

`GameSessionModel` compõe `PortServiceModel`. A sessão expõe a disponibilidade documentada de provisões e reparo no nó atual e devolve um novo `GameSessionState` quando uma ação é executada.

As regras continuam as mesmas do módulo portuário:

- campo histórico vazio permanece `UNKNOWN`;
- `UNKNOWN` não é convertido em `NONE` nem em serviço disponível;
- `NONE` é ausência explicitamente registrada;
- `LOW`, `MEDIUM` e `HIGH` podem ser transformados em capacidades ou taxas somente pelas regras de simulação de `port_rules.csv`;
- reabastecimento altera provisões e calendário;
- reparo altera condição e calendário;
- o estado comercial e o conhecimento permanecem inalterados por esses serviços na v0.1;
- nenhum custo monetário é inventado enquanto o corpus não sustentar uma regra histórica ou uma hipótese de balanceamento separada.

O limite máximo abstrato de provisões foi ampliado para comportar a perna observada São Thiago–baía de Santa Helena. Esse valor não representa tonelagem, ração diária, água por tripulante ou capacidade histórica de uma embarcação.

## Navegação e observações históricas

A sessão delega duração e execução ao `TravelModel`/`NavigationModel`. Observações documentadas para a rota e data exatas têm precedência sobre extrapolações geodésicas.

A partida histórica inicial é `R_LIS_STG`: 8 de julho de 1497 até São Thiago/baía de Santa Maria. O itinerário segue depois por baía de Santa Helena, Cabo, São Brás, Rio do Cobre, Rio dos Bons Sinais e Moçambique. Datas reconstruídas entre colchetes pela edição Ravenstein do `Roteiro` são marcadas como editoriais nas notas de evidência.

A observação agregada Lisboa–Cabo de Subrahmanyam continua preservada para comparação historiográfica, mas `R_LIS_CGH` não é executável como uma única viagem.

## Aprendizagem por experiência

`simulation/session_rules.csv` contém os mínimos de aprendizagem aplicados após uma chegada física e após completar uma rota. Na v0.1:

- localização do destino torna-se `CONFIRMED`;
- conhecimento náutico do nó torna-se pelo menos `PARTIAL`;
- mercado do destino torna-se pelo menos `OPERATIONAL`;
- conhecimento político torna-se pelo menos `PARTIAL`;
- a rota efetivamente completada torna-se pelo menos `OPERATIONAL`.

Esses níveis são regras de jogo e não medidas historiográficas. O objetivo é codificar a diferença entre rumor, presença física e experiência de navegação.

## Cenário técnico de integração

O protótipo também executa Calecute → Aden com conhecimento operacional concedido explicitamente por métodos `scenario_*`. Esse cenário existe somente para testar a cadeia:

```text
mercado → compra → viagem → chegada → venda
```

Ele **não representa o estado histórico inicial do personagem** e não altera os valores iniciais de `nodes.csv` ou `routes.csv`.

## Interface

A interface Pygame chama diretamente os métodos desta sessão para mercado, compra, venda, reabastecimento, reparo, espera, planejamento e execução de viagem.

No modo `HISTORICAL`, a sessão começa em 8 de julho de 1497 associada a `EXP_GAMA_1497`. O painel identifica a armada, a perna corrente, o modo cronológico e, quando houver, a escala ativa com atividades e data de partida. O modo `TECHNICAL` continua explicitamente não histórico.

## Próximos passos

Com itinerário e permanências integrados, a próxima camada do loop é aquisição de informação. Rumor, conversa, carta, contato mercantil e piloto devem produzir mudanças distintas de conhecimento sem revelar automaticamente o estado institucional da Coroa ao personagem.
