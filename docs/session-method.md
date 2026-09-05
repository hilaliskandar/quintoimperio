# Método de sessão integrada v0.1

## Objetivo

Compor os módulos já existentes em um primeiro ciclo contínuo de jogo. `GameSessionModel` não cria nova evidência histórica: ele coordena conhecimento, comércio, serviços portuários, expedições e viagem e aplica somente regras explícitas de simulação.

## Estado

`GameSessionState` é imutável e reúne:

- `VesselState`: localização, calendário, provisões e condição;
- `CommercialState`: capital, capacidade e carga abstratos;
- conhecimento do personagem por nó;
- conhecimento náutico do personagem por rota;
- expedição ativa opcional e número da perna corrente.

O conhecimento de rota é deliberadamente separado do conhecimento do porto. Saber onde Calecute está ou conhecer seu mercado não torna automaticamente operacional uma ligação marítima Calecute–Aden, Calecute–Hurmuz ou Calecute–Melaka.

Do mesmo modo, participar de uma armada que percorre uma rota não torna o personagem conhecedor daquela rota antes da experiência.

## Conhecimento inicial de rota

`RouteKnowledgeModel` lê `player_knowledge_default` e `crown_knowledge_1497` de `data/routes.csv` e converte esses estados usando `simulation/route_knowledge_rules.csv`.

A conversão é parâmetro de simulação. Na v0.1:

- `PLAYER/MEDIUM` produz conhecimento `PARTIAL`;
- `PLAYER/UNKNOWN` permanece `UNKNOWN`;
- `CROWN/HIGH` produz conhecimento `OPERATIONAL`;
- estados `LOW` e `INDIRECT` da Coroa permanecem abaixo do nível operacional.

## Expedições e comando institucional

`ExpeditionModel` lê `data/expeditions.csv` e `data/expedition_routes.csv`. A primeira expedição normalizada é `EXP_GAMA_1497`, com cinco arestas agregadas de saída até Calecute.

Uma sessão pode possuir `active_expedition_id` e `expedition_leg_sequence`. Quando a rota escolhida coincide com a perna corrente, o período é válido e a tabela histórica registra `FLEET_COMMAND`, a viagem recebe essa base institucional.

Isso não altera o conhecimento pessoal antes da partida. As bases de viagem são hierarquicamente distintas:

1. `OWN_KNOWLEDGE` quando o personagem possui conhecimento operacional;
2. `PILOT` quando um piloto historicamente registrado é competente para a rota e o conhecimento próprio não basta;
3. `FLEET_COMMAND` quando a perna corrente da expedição autoriza participação sob comando institucional.

Assim, o piloto guzerate de Melinde continua sendo a base específica da travessia Melinde–Calecute quando fornecido ao plano, mesmo se a armada estiver ativa.

Depois de completar uma perna da expedição, a sessão avança para a próxima. Ao concluir a última, os campos de expedição ativa voltam a `None`.

A camada não fixa identidade, profissão, navio ou estatuto social do protagonista.

## Mercado

O mercado do porto atual só é operacional quando `market_knowledge >= OPERATIONAL`. Antes disso a sessão não expõe cotações nem permite compra/venda. Isso evita que a interface revele toda a cesta comercial histórica a um personagem que apenas ouviu falar do lugar.

Quando operacional, a sessão delega cotações e operações ao `TradeModel`; nenhuma mercadoria ausente de `node_goods.csv` é criada para completar o loop.

## Serviços portuários

`GameSessionModel` compõe `PortServiceModel`. A sessão expõe a disponibilidade documentada de provisões e reparo no porto atual e devolve um novo `GameSessionState` quando uma ação é executada.

As regras continuam as mesmas do módulo portuário:

- campo histórico vazio permanece `UNKNOWN`;
- `UNKNOWN` não é convertido em `NONE` nem em serviço disponível;
- `NONE` é ausência explicitamente registrada;
- `LOW`, `MEDIUM` e `HIGH` podem ser transformados em capacidades ou taxas somente pelas regras de simulação de `port_rules.csv`;
- reabastecimento altera provisões e calendário;
- reparo altera condição e calendário;
- o estado comercial e o conhecimento permanecem inalterados por esses serviços na v0.1;
- nenhum custo monetário é inventado enquanto o corpus não sustentar uma regra histórica ou uma hipótese de balanceamento separada.

`SessionPortServiceResult` preserva o estado antes/depois, bloqueios, efeito e dias gastos.

## Navegação e observações históricas

A sessão delega duração e execução ao `TravelModel`/`NavigationModel`. Observações documentadas para a rota e data exatas têm precedência sobre extrapolações geodésicas.

Por isso a partida de Lisboa em 8 de julho de 1497 usa a observação agregada de 134 dias até o Cabo registrada para `R_LIS_CGH`, em vez de aplicar a taxa derivada de Melinde–Calecute. A chegada correspondente é 19 de novembro segundo a observação usada.

A aresta permanece agregada: ela não implica 134 dias sem escalas e ainda não deve ser a unidade final para contabilizar provisões. A segmentação pelas escalas documentadas da viagem é um aprofundamento separado.

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

A interface Pygame chama diretamente os métodos desta sessão para mercado, compra, venda, reabastecimento, reparo, planejamento e execução de viagem.

No modo `HISTORICAL`, a sessão começa em 8 de julho de 1497 associada a `EXP_GAMA_1497`. O painel identifica a armada e a perna corrente e distingue visualmente `FLEET_COMMAND` de conhecimento pessoal. O modo `TECHNICAL` continua explicitamente não histórico.

## Próximos passos

O próximo problema imediato é operacional, não de autorização: a aresta agregada Lisboa–Cabo inclui escalas e reabastecimentos documentados, mas o modelo de provisões a trata como uma única perna. O itinerário deve ser segmentado antes de transformar essa aresta em unidade final de jogabilidade.

Depois disso, a próxima camada institucional é aquisição de informação: rumor, conversa, carta, contato mercantil e piloto devem produzir mudanças distintas de conhecimento sem revelar automaticamente o estado da Coroa ao personagem.
