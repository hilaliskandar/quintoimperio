# Quinto Império

Projeto de jogo histórico de comércio e navegação inspirado na expansão ultramarina portuguesa e na inserção portuguesa em redes atlânticas e do Oceano Índico já existentes.

## Objetivo

Construir um jogo pequeno, baseado em dados e historicamente documentado, cujo núcleo seja comércio, navegação, informação, relações políticas e adaptação a redes mercantis preexistentes. O ponto de partida é a infraestrutura atlântica portuguesa formada antes de 1497; a chegada ao Índico introduz um sistema econômico muito mais amplo e complexo.

## Princípios

- separar evidência histórica, inferência e parâmetro de simulação;
- não inventar mapas, portos, preços ou cronologias;
- tratar porto, hinterland e rota de abastecimento como dimensões distintas;
- distinguir mercados, ancoradouros logísticos e marcos náuticos;
- tratar conhecimento geográfico, náutico, comercial e político como recursos distintos;
- separar conhecimento do personagem, conhecimento institucional e capacidade de participar de uma expedição;
- representar monções, risco, intermediação, tributação e regimes de acesso;
- manter pessoas escravizadas fora da tabela de mercadorias ordinárias, com modelagem histórica própria.

## Estado atual

A fundação histórica, economia relativa, navegação/viagem, serviços portuários, comércio, conhecimento/informação, cartografia, sessão integrada e a primeira interface jogável Pygame v0.1 estão operacionais.

A base contém atualmente **25 nós, 14 bens, 41 relações nó–bem, 19 rotas, 15 fluxos de mercadorias, 12 observações de viagem, 1 piloto histórico, 1 expedição com 10 pernas normalizadas e 5 permanências logísticas documentadas**. Mpinda/Soyo e Sofala permanecem com âncoras cartográficas provisórias de confiança `MEDIUM`; o Rio do Cobre usa uma âncora `LOW`, porque sua identificação moderna é discutida. A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada.

O domínio já oferece:

- economia relativa com estoques estruturais e de trânsito;
- calendário, monções e distâncias geodésicas de referência;
- observações de viagem com precedência sobre extrapolações quando rota e data coincidem;
- Melinde–Calecute em 1498 preservada em 26/27 dias;
- itinerário de 1497–1498 segmentado operacionalmente em Lisboa → São Thiago → baía de Santa Helena → Cabo → São Brás → Rio do Cobre → Rio dos Bons Sinais → Moçambique → Mombaça → Melinde → Calecute;
- Lisboa–Cabo e Cabo–Moçambique preservadas apenas como conexões estratégicas agregadas e explicitamente não executáveis;
- permanências históricas em São Thiago, baía de Santa Helena, São Brás, Rio do Cobre e Rio dos Bons Sinais, com água, madeira, carenagem, reparos e transferência de carga registrados separadamente;
- `ChronologyMode.GUIDED` e `ChronologyMode.COUNTERFACTUAL`, distinguindo campanha ainda alinhada à cronologia documentada de trajetória já divergente;
- bloqueio de partida antes da data documentada quando há escala guiada ativa;
- ação explícita de espera até a partida documentada, sem conceder automaticamente provisões, reparos, carga ou dinheiro;
- serviços portuários e interações informativas consumindo o mesmo calendário da permanência;
- quatro dimensões de conhecimento por nó e conhecimento náutico separado por rota;
- estados separados para personagem e Coroa;
- aquisição ativa por `RUMOR`, `MERCHANT_CONTACT` e `PILOT_CONSULTATION`, sem copiar silenciosamente o conhecimento institucional;
- rumor limitado a `RUMORED`, contato mercantil sem navegação operacional e consulta a piloto limitada a `PARTIAL`;
- oportunidades de informação derivadas apenas de nós/rotas documentados, com repetição bloqueada por sessão e seleção determinística por semente;
- piloto guzerate de Melinde associado somente à rota documentada até Calecute;
- `ExpeditionModel` com a armada de Vasco da Gama de 1497–1499;
- `FLEET_COMMAND`, que permite participação na perna corrente sem transformar comando institucional em conhecimento pessoal;
- `OWN_KNOWLEDGE`, `PILOT` e `FLEET_COMMAND` como bases distintas de viagem;
- `GameSessionState` imutável reunindo navio, comércio, conhecimento, histórico de informação, expedição ativa, cronologia e escala ativa;
- provisões/condição abstratas, reabastecimento e reparo;
- compra/venda somente em mercados documentados;
- aprendizagem explícita por chegada e conclusão de rota;
- mapa de runtime em Pygame e referência cartográfica programática com costa real;
- interface Pygame com mapa conhecido, porto/data/navio, capital/carga, serviços, informação, mercado, armada ativa, escala histórica, espera e rotas;
- modo `HISTORICAL` iniciado em Lisboa em 8/7/1497 com `EXP_GAMA_1497`;
- modo `TECHNICAL` separado para testes de integração;
- testes automatizados, smoke tests e capturas de interface no GitHub Actions.

A arquitetura do primeiro jogável é **Python 3.12 + pygame-ce**, com núcleo de domínio independente da camada gráfica.

A segmentação do itinerário corrige um problema importante da primeira versão: 134 dias Lisboa–Cabo não são mais tratados como uma única perna operacional. O `Roteiro` passa a ser a fonte primária de cronologia fina; datas reconstruídas entre colchetes na edição Ravenstein são explicitamente marcadas como editoriais. O limite de provisões da simulação foi ampliado somente para comportar a longa perna São Thiago–baía de Santa Helena e continua sendo um índice abstrato, não capacidade histórica de um navio.

A permanência em escala também não produz efeitos materiais por simples passagem do tempo. Uma atividade documentada como `WATER`, `CARENING` ou `MAST_REPAIR` registra evidência; seus efeitos jogáveis continuam exigindo ação explícita. Se o jogador ultrapassa a data documentada de partida e prossegue, a sessão passa para cronologia contrafactual em vez de forçar artificialmente o calendário histórico.

A informação passou a ser um recurso acionável, mas de forma conservadora. Os canais genéricos de rumor e contato mercantil são mecânicas de simulação, não diálogos históricos inventados. Consulta a piloto só existe onde `pilots.csv`/`pilot_routes.csv` sustentam a competência. Nenhum desses canais torna automaticamente uma rota operacional.

Próximos sistemas: eventos marítimos/avarias e relações institucionais mais detalhadas; cartas persistentes, desinformação e redes pessoais de confiança permanecem para incrementos posteriores.

## Estrutura

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

simulation/
  README.md
  goods_params.csv
  rules.csv
  navigation_rules.csv
  knowledge_rules.csv
  route_knowledge_rules.csv
  information_rules.csv
  session_rules.csv
  travel_rules.csv
  port_rules.csv
  trade_rules.csv

docs/
  historical-method.md
  navigation-method.md
  map-method.md
  port-method.md
  trade-method.md
  session-method.md
  stop-method.md
  information-method.md
  interface-method.md
  roadmap.md
  sources.md
  evidence/
    pilot-malindi-1498.md
    expedition-gama-1497.md
    provisional-coordinates.md
  adr/
    0001-runtime-and-engine.md

src/quintoimperio/domain/
  calendar.py
  economy.py
  expedition.py
  information.py
  knowledge.py
  navigation.py
  port.py
  route_knowledge.py
  session.py
  stop.py
  trade.py
  travel.py
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

tools/
  render_cartographic_map.py

tests/
  test_economy.py
  test_expedition.py
  test_expedition_data.py
  test_information.py
  test_knowledge.py
  test_navigation.py
  test_port.py
  test_port_data.py
  test_session.py
  test_stop.py
  test_trade.py
  test_travel.py
  test_world_map.py
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

Interface histórica:

```bash
python prototype/game.py --scenario HISTORICAL
```

Cenário técnico de integração:

```bash
python prototype/game.py --scenario TECHNICAL
```

`R` reinicia, `Tab` alterna os modos e `Esc` encerra. Em uma escala histórica guiada, a interface expõe a data de partida e a ação de espera correspondente. Os botões de informação mostram apenas o canal disponível; o alvo só é revelado depois da interação.

Renderização sem janela:

```bash
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario HISTORICAL --output /tmp/game-historical.png
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario TECHNICAL --output /tmp/game-technical.png
```

Referência cartográfica:

```bash
python tools/render_cartographic_map.py --perspective REFERENCE --output build/map-reference.png
```

## Fontes de dados

As tabelas em `data/` mantêm proveniência e grau de evidência. Os números em `simulation/` são parâmetros de balanceamento e não devem ser apresentados como dados históricos. A costa usada pela ferramenta cartográfica pertence à camada de desenvolvimento; a posição dos nós continua vindo de `data/nodes.csv`.

## Licença

GPL-3.0. Consulte `LICENSE`.
