# Quinto Império

Projeto de jogo histórico de comércio e navegação inspirado na expansão ultramarina portuguesa e na inserção portuguesa em redes atlânticas e do Oceano Índico já existentes.

## Objetivo

Construir um jogo pequeno, baseado em dados e historicamente documentado, cujo núcleo seja comércio, navegação, informação, relações políticas e adaptação a redes mercantis preexistentes. O ponto de partida é a infraestrutura atlântica portuguesa formada antes de 1497; a chegada ao Índico introduz um sistema econômico muito mais amplo e complexo.

## Princípios

- separar evidência histórica, inferência e parâmetro de simulação;
- não inventar mapas, portos, preços ou cronologias;
- tratar porto, hinterland e rota de abastecimento como dimensões distintas;
- tratar conhecimento geográfico, náutico, comercial e político como recursos distintos;
- separar conhecimento do personagem, conhecimento institucional e capacidade de participar de uma expedição;
- representar monções, risco, intermediação, tributação e regimes de acesso;
- manter pessoas escravizadas fora da tabela de mercadorias ordinárias, com modelagem histórica própria.

## Estado atual

A fundação histórica, economia relativa, navegação/viagem, serviços portuários, comércio, cartografia, sessão integrada e a primeira interface jogável Pygame v0.1 estão operacionais.

A base contém atualmente **20 nós, 14 bens, 41 relações nó–bem, 12 rotas, 15 fluxos de mercadorias, 3 observações de viagem, 1 piloto histórico e 1 expedição com 5 pernas normalizadas**. Mpinda/Soyo e Sofala permanecem com âncoras cartográficas provisórias de confiança `MEDIUM`. A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada.

O domínio já oferece:

- economia relativa com estoques estruturais e de trânsito;
- calendário, monções e distâncias geodésicas de referência;
- observações de viagem com precedência sobre extrapolações quando rota e data coincidem;
- Melinde–Calecute em 1498 preservada em 26/27 dias;
- Lisboa–Cabo em 1497 registrada como observação agregada de 134 dias segundo a fonte usada;
- quatro dimensões de conhecimento por nó e conhecimento náutico separado por rota;
- estados separados para personagem e Coroa;
- piloto guzerate de Melinde associado somente à rota documentada até Calecute;
- `ExpeditionModel` com a armada de Vasco da Gama de 1497–1499;
- `FLEET_COMMAND`, que permite participação na perna corrente sem transformar comando institucional em conhecimento pessoal;
- `OWN_KNOWLEDGE`, `PILOT` e `FLEET_COMMAND` como bases distintas de viagem;
- `GameSessionState` imutável reunindo navio, comércio, conhecimento e expedição ativa;
- provisões/condição abstratas, reabastecimento e reparo;
- compra/venda somente em mercados documentados;
- aprendizagem explícita por chegada e conclusão de rota;
- mapa de runtime em Pygame e referência cartográfica programática com costa real;
- interface Pygame com mapa conhecido, porto/data/navio, capital/carga, serviços, mercado, armada ativa e rotas;
- modo `HISTORICAL` iniciado em Lisboa em 8/7/1497 com `EXP_GAMA_1497`;
- modo `TECHNICAL` separado para testes de integração;
- testes automatizados, smoke tests e capturas de interface no GitHub Actions.

A arquitetura do primeiro jogável é **Python 3.12 + pygame-ce**, com núcleo de domínio independente da camada gráfica.

A próxima correção histórica é decompor a aresta agregada Lisboa–Cabo em escalas documentadas. A viagem de 1497 incluiu reabastecimentos e reparos; portanto 134 dias não devem ser tratados como uma única perna operacional de provisões. Depois dessa segmentação, o próximo sistema será aquisição de informação por rumor, conversa, carta, piloto e contato mercantil.

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

simulation/
  README.md
  goods_params.csv
  rules.csv
  navigation_rules.csv
  knowledge_rules.csv
  route_knowledge_rules.csv
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
  knowledge.py
  navigation.py
  port.py
  route_knowledge.py
  session.py
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
  test_knowledge.py
  test_navigation.py
  test_port.py
  test_port_data.py
  test_session.py
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

`R` reinicia, `Tab` alterna os modos e `Esc` encerra.

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
