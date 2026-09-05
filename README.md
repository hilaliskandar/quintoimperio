# Quinto Império

Projeto de jogo histórico de comércio e navegação inspirado na expansão ultramarina portuguesa e na inserção portuguesa em redes atlânticas e do Oceano Índico já existentes.

## Objetivo

Construir um jogo pequeno, baseado em dados e historicamente documentado, cujo núcleo seja comércio, navegação, informação, relações políticas e adaptação a redes mercantis preexistentes. O ponto de partida é a infraestrutura atlântica portuguesa formada antes de 1497; a chegada ao Índico introduz um sistema econômico muito mais amplo e complexo.

## Princípios

- separar evidência histórica, inferência e parâmetro de simulação;
- não inventar mapas, portos, preços ou cronologias quando a documentação não sustentar precisão;
- modelar portos como nós de funções distintas: porto metropolitano, praça militar, colônia, feitoria, mercado estrangeiro e ponto náutico;
- tratar conhecimento geográfico, náutico e comercial como recursos distintos;
- representar monções, sazonalidade, risco, intermediação, tributação e regimes de acesso;
- distinguir produção local, hinterland, importação, trânsito e reexportação;
- manter pessoas escravizadas fora da tabela de mercadorias ordinárias, com modelagem histórica própria.

## Estado atual

A fundação histórica, a economia relativa, navegação/viagem, serviços portuários, comércio, cartografia e o **primeiro estado de sessão integrado v0.1** estão operacionais.

A base validada contém 20 nós, 14 bens, 41 relações nó–bem, 12 rotas, 15 fluxos de mercadorias, 2 observações de viagem e o primeiro piloto histórico normalizado. Todos os 20 nós possuem uma âncora cartográfica explícita. **Mpinda/Soyo** e **Sofala** permanecem marcados como coordenadas provisórias de confiança `MEDIUM`, sem pretensão de localizar exatamente o cais medieval. A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada em linhas distintas.

O domínio já oferece:

- economia relativa com estoques estruturais e de trânsito;
- calendário, monções, distâncias geodésicas e duração determinística por semente;
- calibração inicial Melinde–Calecute e propagação da confiança espacial da rota;
- quatro dimensões independentes de conhecimento por nó;
- conhecimento náutico de rota separado do conhecimento do porto;
- estados separados para personagem e Coroa;
- piloto histórico guzerate de Melinde associado somente à rota documentada até Calecute;
- estado imutável do navio, provisões abstratas e condição 0–100;
- reabastecimento e reparo com distinção entre `UNKNOWN` e `NONE`;
- capital, capacidade de carga e inventário abstratos;
- compra e venda somente em mercados documentados em `node_goods.csv`;
- `GameSessionState` imutável reunindo navio, comércio e conhecimento;
- mercado condicionado ao `market_knowledge`;
- viagem condicionada ao conhecimento **da rota** ou a piloto competente;
- aprendizagem explícita por chegada e por conclusão de rota;
- cenário técnico determinístico que executa `mercado → compra → viagem → chegada → venda` sem ser apresentado como estado histórico inicial;
- mapa de runtime em Pygame e referência cartográfica programática com costa real e sem fronteiras políticas modernas;
- estética náutica procedural sem alterar a geometria real;
- testes automatizados e smoke tests no GitHub Actions.

A arquitetura do primeiro jogável foi definida no ADR 0001: **Python 3.12 + pygame-ce**, com núcleo de domínio independente da interface gráfica.

Próximo incremento: expor o `GameSessionState` em uma **interface Pygame mínima**, conectando mapa, painel do porto, mercado, carga e seleção de viagem sem duplicar regras de domínio.

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
  roadmap.md
  sources.md
  evidence/
    pilot-malindi-1498.md
    provisional-coordinates.md
  adr/
    0001-runtime-and-engine.md

src/quintoimperio/
  data/
  domain/
    calendar.py
    economy.py
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

tools/
  render_cartographic_map.py

tests/
  test_economy.py
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

Com Pygame:

```bash
python -m pip install -e ".[game]"
```

Com ferramentas cartográficas:

```bash
python -m pip install -e ".[cartography]"
```

Validação manual:

```bash
python scripts/validate_data.py
python -m unittest discover -s tests -v
python prototype/economy.py
python prototype/navigation.py
python prototype/travel.py
python prototype/port.py
python prototype/trade.py
python prototype/session.py
python prototype/map.py
```

Mapa de runtime sem janela interativa:

```bash
SDL_VIDEODRIVER=dummy python prototype/map.py --output /tmp/quintoimperio-map.png
```

Referência cartográfica programática:

```bash
python tools/render_cartographic_map.py --perspective REFERENCE --output build/map-reference.png
```

O GitHub Actions executa essas verificações automaticamente.

## Fontes de dados

As tabelas em `data/` mantêm campos de proveniência e grau de evidência. Os números em `simulation/` são índices de balanceamento e não devem ser apresentados como dados históricos. A costa usada pela ferramenta de referência pertence somente à camada cartográfica de desenvolvimento; a posição dos nós continua vindo de `data/nodes.csv`. A justificativa específica para as âncoras provisórias de Mpinda/Soyo e Sofala está em `docs/evidence/provisional-coordinates.md`.

## Licença

GPL-3.0. Consulte `LICENSE`.
