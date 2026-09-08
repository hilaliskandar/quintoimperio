# Quinto Império

Projeto de jogo histórico de comércio e navegação inspirado na expansão ultramarina portuguesa e na inserção portuguesa em redes atlânticas e do Oceano Índico já existentes.

## Objetivo

Construir um jogo pequeno, baseado em dados e historicamente documentado, cujo núcleo seja comércio, navegação, informação, relações políticas e adaptação a redes mercantis preexistentes. O ponto de partida é a infraestrutura atlântica portuguesa formada antes de 1497; a chegada ao Índico introduz um sistema econômico mais amplo e complexo.

## Princípios

- separar evidência histórica, inferência e parâmetro de simulação;
- não inventar mapas, portos, preços ou cronologias;
- tratar porto, hinterland e rota de abastecimento como dimensões distintas;
- distinguir mercados, ancoradouros logísticos e marcos náuticos;
- tratar conhecimento geográfico, náutico, comercial e político como recursos distintos;
- separar conhecimento do personagem, conhecimento institucional, acesso comercial, relações com atores e capacidade de participar de uma expedição;
- representar monções, risco, intermediação, tributação e regimes de acesso sem atribuir precisão documental inexistente;
- manter pessoas escravizadas fora da tabela de mercadorias ordinárias, com modelagem histórica própria.

## Estado atual

O domínio Python necessário ao horizonte **1497–1505 está implementado até F5 e integrado ao `main`**. O PR #135 integrou a tranche funcional de Francisco de Almeida em 1505 no commit `e982d5b83a1c8a8bfe77f512e354c63347004266`; a CI pós-merge `34200338707` ficou integralmente verde.

O projeto está agora no gate final **Python 1505 GREEN**, issue #136. Nesta etapa não se acrescentam novas mecânicas históricas: são congelados contratos de dados/estado, golden tests, divergências preservadas e critérios de paridade para a futura migração a Godot. O documento canônico desse gate é `docs/domain-freeze-1505.md`.

O **MVP Lisboa–Calecute** permanece a vertical slice canônica. Seu fluxo é:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`.

O **retorno P1** permanece opt-in e estabilizado até os Baixos do Rio Grande:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`.

O arco posterior foi incorporado por tranches documentais e funcionais:

- 1500: Cabral, Vera Cruz, ruptura de Calecute e presença inicial em Cochim/Cananor;
- 1501–1502: João da Nova, incluindo aquisição tardia de informação em São Brás;
- 1502–1503: Vasco da Gama e força residente de Vicente Sodré, sem generalizar múltiplas frotas ativas;
- 1503: crise, restauração, fortificação e guarnição de Cochim com soberania local preservada;
- 1504: Lopo Soares e defesa de Cochim sob Duarte Pacheco, representada por eventos específicos sem combate geral;
- 1505: Francisco de Almeida, Pêro de Anhaia e estados persistentes de Quiloa, Sofala, Anjediva, Cananor e Cochim.

As decisões arquiteturais consolidadas até 31/12/1505 são:

- `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`;
- `NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO`;
- `MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO`.

Essas decisões não proíbem evolução posterior; apenas impedem que sistemas gerais sejam introduzidos antes de um caso histórico/jogável demonstrar sua necessidade.

A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada. Também permanecem abertas, sem harmonização artificial, as variantes 20/21/22/23 para o tamanho da armada de Almeida, 13/09 × 14/09 em Anjediva, `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` e a chegada diária de Almeida a Cochim antes da âncora documental segura de 16/12/1505.

O fechamento do MVP está em `docs/mvp-gate.md`; o retorno P1 em `docs/p1-closeout.md`; o desenvolvimento 1500–1505 e seus gates estão documentados no `docs/roadmap.md`; e o contrato final do domínio está em `docs/domain-freeze-1505.md`.

### O domínio já oferece

- economia relativa com estoques estruturais e de trânsito;
- calendário, monções e distâncias geodésicas de referência;
- observações de viagem com precedência sobre extrapolações quando rota e data coincidem;
- itinerário da ida segmentado operacionalmente em dez pernas;
- retorno segmentado em sete pernas até o limite do corpo primário do `Roteiro`;
- Lisboa–Cabo e Cabo–Moçambique preservadas apenas como conexões estratégicas agregadas e não executáveis;
- permanências históricas e atividades documentadas registradas separadamente dos seus efeitos de simulação;
- `ChronologyMode.GUIDED` e `ChronologyMode.COUNTERFACTUAL`;
- fase simulada de preparação anterior à partida histórica de 8/7/1497;
- bloqueio de partida antes da data documentada quando há escala guiada ativa;
- espera explícita até partidas documentadas sem concessão automática de recursos;
- planejamento logístico por horizonte até o próximo abastecimento documentado, com margem heurística rotulada como `SIMULATION`;
- serviços, informação e negociação institucional consumindo o mesmo calendário;
- quatro dimensões de conhecimento por nó e conhecimento náutico separado por rota;
- estados separados para personagem e Coroa;
- aquisição ativa por `RUMOR`, `MERCHANT_CONTACT` e `PILOT_CONSULTATION`;
- `AccessModel` separado de conhecimento e relações;
- `RelationshipModel` com estado por ator, sem reputação global inventada;
- piloto guzerate de Melinde associado somente à rota documentada até Calecute;
- `ExpeditionModel`, `FLEET_COMMAND`, `OWN_KNOWLEDGE` e `PILOT` como bases distintas de viagem;
- `ExpeditionEventModel` para acontecimentos documentais que não devem virar automaticamente mecânicas gerais;
- `NodeStateEventModel` para projeção temporal de presença institucional, fortificação, guarnição, acesso, relação e soberania;
- eventos marítimos `SIMULATION` com seleção determinística por semente e resolução tardia;
- precedência documental: em `GUIDED`, observações históricas exatas preservam o timing documentado;
- reserva segregada opcional contra `MAJOR_PROVISION_LOSS`, sem criação de provisões;
- `GameSessionState` imutável reunindo navio, comércio, conhecimento, acesso, relações, históricos, expedição e cronologia;
- provisões e condição abstratas, reabastecimento e reparo por ação explícita;
- compra/venda somente em mercados documentados e institucionalmente acessíveis;
- objetivos e encerramento explícito do MVP em Calecute;
- persistência JSON versionada e round-trip de save/load;
- estado histórico objetivo derivado de dados temporais + data da sessão, sem duplicação artificial no save;
- golden state determinístico de 31/12/1505;
- mapa de runtime em Pygame e referência cartográfica programática com costa real;
- interface Pygame com mapa, porto/data/navio, capital/carga, serviços, acesso, informação, relações, mercado, armada, escala, espera, rotas, planejamento logístico, proteção de provisões e eventos;
- modo `HISTORICAL` e modo `TECHNICAL` separado para testes de integração;
- testes automatizados, smoke tests, baterias sintéticas por arquétipos, seeds sentinela e capturas de interface no GitHub Actions.

### Retorno P1

O retorno é uma expansão **opt-in**. Quando não é ativado, o comportamento do MVP Lisboa–Calecute permanece inalterado.

A pesquisa documental posterior refinou a antiga perna agregada `CAL→ANJ` em `CAL→SMI→ANJ`. `SMI` representa os Ilhéus de Santa Maria como marco náutico de passagem; não recebe mercado nem serviço portuário genérico.

Durante o retorno:

- em SMI existe uma única oportunidade alimentar específica do contato narrado, com efeito abstrato rotulado `SIMULATION` e sem consumo de um dia inteiro;
- em ANJ, provisões e carena derivam da permanência documentada, sem transformar o nó em serviço genérico; a carena mínima de referência validada é +2 pontos abstratos de condição;
- em BSR, abandono/queima do S. Rafael e transferência de carga permanecem registros específicos da expedição, sem sistema geral de frota/tripulação;
- o epílogo posterior a BRG não é apresentado como continuação operacional certa.

As ações one-shot do retorno reutilizam `information_history`, já persistido no schema v2. Assim, save/load preserva seu uso sem introduzir schema novo ou estado paralelo de interface.

A wave19 concluiu **18/18 estados elegíveis, com zero blockers, todos em `GUIDED` até BRG em 25/04/1499**. O baseline funcional pós-retorno é o commit `47fb82baad1289077c048576f3bc52815d6b192f`; a validação pós-integração no `main` foi integralmente verde no GitHub Actions run `34118123204`.

### Estado temporal 1500–1505

A expansão do domínio após o retorno não é uma campanha única artificial. `expedition_events.csv` registra acontecimentos documentais por expedição e `node_state_events.csv` projeta efeitos persistentes por data.

O contrato temporal preserva três regras centrais:

1. transições posteriores não podem retroagir para campanhas anteriores;
2. campos não alterados por um evento preservam o estado anterior;
3. eventos `RANGE` tornam-se seguramente disponíveis no limite superior da janela quando usados por consultas conservadoras.

No freeze de 31/12/1505, Quiloa, Sofala, Anjediva e Cananor apresentam as presenças fortificadas/guarnições documentadas pelas respectivas tranches; Cochim herda forte e guarnição de 1503 sem duplicação; Mombaça não recebe presença fortificada persistente apenas pelo ataque de agosto de 1505. Em todos esses casos, presença portuguesa e soberania territorial permanecem dimensões distintas.

## Arquitetura

O jogável de referência utiliza **Python 3.12 + pygame-ce**, com núcleo de domínio independente da camada gráfica. Dados históricos ficam em `data/`; parâmetros experimentais ficam em `simulation/`.

A permanência em escala não produz efeitos materiais por simples passagem do tempo. Uma atividade documentada como `WATER`, `FOOD`, `CARENING` ou `MAST_REPAIR` registra evidência; seu efeito jogável exige ação explícita e, quando quantificado sem medida histórica, permanece identificado como simulação.

O acesso institucional é distinto do conhecimento. A chegada a um mercado pode torná-lo conhecido sem conceder automaticamente permissão para comerciar. Relações também são independentes: um contato documentado não concede amizade, desconto, crédito ou influência sem evidência própria.

O risco marítimo é explicitamente uma camada de simulação. A mesma seed aplicada ao mesmo estado é reproduzível; seeds diferentes podem produzir resultados distintos. Em cronologia guiada, a evidência histórica controla as datas observadas e somente efeitos compatíveis com esse timing podem operar.

O estado histórico temporal não é copiado para dentro do save como um segundo mundo paralelo. A sessão persiste seu próprio estado e a data; os estados objetivos dos nós são recompostos a partir dos dados canônicos. Esse contrato foi validado pelo round-trip do freeze de 31/12/1505.

## Estrutura principal

```text
data/
  README.md
  nodes.csv
  goods.csv
  node_goods.csv
  routes.csv
  route_goods.csv
  voyage_observations.csv
  pilots.csv
  pilot_routes.csv
  expeditions.csv
  expedition_routes.csv
  expedition_stops.csv
  expedition_events.csv
  node_state_events.csv
  actors.csv
  node_actors.csv
  expedition_epilogue_events.csv

simulation/
  README.md
  goods_params.csv
  rules.csv
  navigation_rules.csv
  knowledge_rules.csv
  route_knowledge_rules.csv
  information_rules.csv
  access_rules.csv
  session_rules.csv
  travel_rules.csv
  voyage_event_rules.csv
  port_rules.csv
  trade_rules.csv
  return_rules.csv

docs/
  historical-method.md
  navigation-method.md
  map-method.md
  port-method.md
  trade-method.md
  session-method.md
  stop-method.md
  information-method.md
  access-method.md
  relationship-method.md
  voyage-event-method.md
  interface-method.md
  roadmap.md
  domain-freeze-1505.md
  mvp-gate.md
  p1-closeout.md
  p1-roadmap-handoff-2026-09-07.md
  return-p1-wave19-results.md
  santa-maria-logistics-p1-func.md
  p1-ui-return-interface-results.md
  f5-francisco-almeida-1505-handoff.md
  development-log.md
  sources.md
  evidence/
  adr/

src/quintoimperio/domain/
  access.py
  calendar.py
  campaign.py
  campaign_progress.py
  economy.py
  expedition.py
  expedition_event.py
  information.py
  knowledge.py
  navigation.py
  node_state_event.py
  persistence.py
  port.py
  relationship.py
  return_campaign.py
  risk_mitigation.py
  route_knowledge.py
  session.py
  stop.py
  trade.py
  travel.py
  voyage_event.py
  world_map.py

prototype/
  economy.py
  navigation.py
  port.py
  session.py
  trade.py
  travel.py
  map.py
  game.py
  historical_campaign.py
  game_m5.py
  game_m6.py
  return_campaign.py

tools/
  render_cartographic_map.py
  simulate_player_archetype.py
  diagnose_structural_strain.py
  diagnose_structural_strain_campaign.py
  diagnose_return_from_mvp.py
  diagnose_anjediva_careening.py
  diagnose_return_with_careening.py

tests/
  test_*.py
```

## Desenvolvimento

Instalação do núcleo:

```bash
python -m pip install -e .
```

Com Pygame e cartografia:

```bash
python -m pip install -e ".[game,cartography]"
```

Validação:

```bash
python scripts/validate_data.py
python -m unittest discover -s tests -v
python prototype/session.py
```

Interface histórica básica:

```bash
python prototype/game.py --scenario HISTORICAL
```

Interface histórica v0.2:

```bash
python prototype/game_m5.py
```

Smoke completo do retorno até BRG:

```bash
SDL_VIDEODRIVER=dummy python prototype/game_m5.py --return-smoke --output /tmp/quintoimperio-interface-v02-brg.png
```

Persistência:

```bash
SDL_VIDEODRIVER=dummy python prototype/game_m6.py --roundtrip-smoke --save-path /tmp/quintoimperio-save.json --output /tmp/quintoimperio-interface-m6.png
```

Cenário técnico de integração:

```bash
python prototype/game.py --scenario TECHNICAL
```

Referência cartográfica:

```bash
python tools/render_cartographic_map.py --perspective REFERENCE --output build/map-reference.png
```

## Próximo gate

O desenvolvimento funcional F1–F5 até 31/12/1505 está integrado. O gate corrente é **issue #136 — Python 1505 GREEN: domain freeze e handoff para Godot**.

A sequência obrigatória é:

`domain-freeze-1505 → sincronização README/roadmap/Diário → CI/PR do freeze → CI pós-merge no main → fechamento da #118 → abertura da frente Godot`.

A migração para Godot **ainda não começou**. Ela somente deverá ser aberta depois que a issue #136 e a issue-mãe #118 estiverem encerradas sem lacuna `BLOCKING`.

## Fontes de dados

As tabelas em `data/` mantêm proveniência e grau de evidência. Os números em `simulation/` são parâmetros de balanceamento e não devem ser apresentados como dados históricos. A costa usada pela ferramenta cartográfica pertence à camada de desenvolvimento; a posição dos nós continua vindo de `data/nodes.csv`.

## Licença

GPL-3.0. Consulte `LICENSE`.
