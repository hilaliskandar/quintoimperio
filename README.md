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

A fundação histórica, a economia relativa, o núcleo de navegação/viagem, o primeiro mapa 2D, os serviços portuários mínimos e a referência cartográfica programática estão operacionais.

A base validada contém 20 nós, 14 bens, 41 relações nó–bem, 12 rotas, 15 fluxos de mercadorias, 2 observações de viagem e o primeiro piloto histórico normalizado. Todos os 20 nós possuem agora uma âncora cartográfica explícita. **Mpinda/Soyo** e **Sofala** permanecem marcados como coordenadas provisórias de confiança `MEDIUM`, sem pretensão de localizar exatamente o cais medieval. A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 continua preservada em linhas distintas.

O domínio já oferece:

- economia relativa com estoques estruturais e de trânsito;
- calendário e fases gerais da monção;
- distâncias geodésicas de referência sem confundi-las com distâncias históricas navegadas;
- duração de viagem determinística por semente;
- calibração inicial Melinde–Calecute;
- quatro dimensões independentes de conhecimento do personagem e da Coroa;
- pilotos históricos associados a rotas e períodos específicos;
- bloqueio de rotas sem conhecimento náutico operacional ou piloto competente;
- estado imutável do navio, dias-equivalentes de provisões e condição abstrata 0–100;
- planejamento e execução de viagem com consumo de provisões e desgaste;
- reabastecimento e reparo baseados nos campos históricos de `nodes.csv`;
- distinção explícita entre serviço `UNKNOWN` e `NONE`;
- capacidades e tempos de serviço isolados em `simulation/port_rules.csv`;
- mapa 2D de runtime filtrado pelo conhecimento geográfico do personagem/Coroa;
- referência cartográfica programática com costa real e sem fronteiras políticas modernas;
- estética náutica procedural — paleta de pergaminho, linhas de rumo e rosa-dos-ventos — sem alterar a geometria real;
- identificação gráfica de âncoras espaciais provisórias;
- arestas de rota tratadas como relações do grafo, não como derrotas históricas;
- testes automatizados e smoke tests dos mapas no GitHub Actions.

A arquitetura do primeiro jogável foi definida no ADR 0001: **Python 3.12 + pygame-ce**, com núcleo de domínio independente da interface gráfica.

Próximo incremento: estado comercial do jogador, inventário/capacidade abstrata e primeiras operações de compra e venda usando apenas os mercados já documentados.

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
  travel_rules.csv
  port_rules.csv

docs/
  historical-method.md
  navigation-method.md
  map-method.md
  port-method.md
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
    travel.py
    world_map.py

prototype/
  economy.py
  navigation.py
  port.py
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
  test_travel.py
  test_world_map.py
```

## Desenvolvimento

Instalação do núcleo sem dependências gráficas:

```bash
python -m pip install -e .
```

Instalação com a camada de protótipo em Pygame:

```bash
python -m pip install -e ".[game]"
```

Instalação das ferramentas cartográficas de desenvolvimento:

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
