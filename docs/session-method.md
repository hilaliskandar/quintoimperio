# Método de sessão integrada v0.1

## Objetivo

Compor os módulos já existentes em um primeiro ciclo contínuo de jogo sem antecipar a interface final. `GameSessionModel` não cria nova evidência histórica: ele coordena conhecimento, comércio e viagem e aplica somente regras explícitas de simulação.

## Estado

`GameSessionState` é imutável e reúne:

- `VesselState`: localização, calendário, provisões e condição;
- `CommercialState`: capital, capacidade e carga abstratos;
- conhecimento do personagem por nó;
- conhecimento náutico do personagem por rota.

O conhecimento de rota é deliberadamente separado do conhecimento do porto. Saber onde Calecute está ou conhecer seu mercado não torna automaticamente operacional uma ligação marítima Calecute–Aden, Calecute–Hurmuz ou Calecute–Melaka.

## Conhecimento inicial de rota

`RouteKnowledgeModel` lê `player_knowledge_default` e `crown_knowledge_1497` de `data/routes.csv` e converte esses estados usando `simulation/route_knowledge_rules.csv`.

A conversão é parâmetro de simulação. Na v0.1:

- `PLAYER/MEDIUM` produz conhecimento `PARTIAL`;
- `PLAYER/UNKNOWN` permanece `UNKNOWN`;
- `CROWN/HIGH` produz conhecimento `OPERATIONAL`;
- estados `LOW` e `INDIRECT` da Coroa permanecem abaixo do nível operacional.

## Mercado

O mercado do porto atual só é operacional quando `market_knowledge >= OPERATIONAL`. Antes disso a sessão não expõe cotações nem permite compra/venda. Isso evita que a interface revele toda a cesta comercial histórica a um personagem que apenas ouviu falar do lugar.

Quando operacional, a sessão delega cotações e operações ao `TradeModel`; nenhuma mercadoria ausente de `node_goods.csv` é criada para completar o loop.

## Viagem e piloto

A sessão delega planejamento e execução ao `TravelModel`, usando o conhecimento **da rota**. Um piloto histórico pode habilitar a viagem mesmo quando o personagem ainda não possui conhecimento operacional.

O caso documentado Melinde–Calecute em 1498 é o primeiro teste desta regra: o piloto guzerate de Melinde permite executar `R_MAL_CAL` com conhecimento inicial do personagem ainda `UNKNOWN`.

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

## Próximo passo

Depois de estabilizado este estado de sessão, a interface Pygame deve apenas apresentar e acionar essas operações. Regras de mercado, viagem ou aprendizagem não devem ser duplicadas na camada gráfica.
