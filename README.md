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

A fundação histórica, a economia relativa e o núcleo de navegação/viagem v0.1 estão operacionais.

A base validada contém 20 nós, 14 bens, 41 relações nó–bem, 12 rotas, 15 fluxos de mercadorias, 2 observações de viagem e o primeiro piloto histórico normalizado. A divergência documental da chegada de Vasco da Gama a Calecute em 20/21 de maio de 1498 é preservada em linhas distintas.

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
- 33 testes automatizados no GitHub Actions.

A arquitetura do primeiro jogável foi definida no ADR 0001: **Python 3.12 + pygame-ce**, com núcleo de domínio independente da interface gráfica.

Próximo incremento: serviços portuários mínimos e primeiro mapa 2D baseado em coordenadas reais; a costa de fundo só será adicionada a partir de dados cartográficos reais.

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

docs/
  historical-method.md
  navigation-method.md
  roadmap.md
  sources.md
  evidence/
    pilot-malindi-1498.md
  adr/
    0001-runtime-and-engine.md

src/quintoimperio/
  data/
  domain/
    calendar.py
    economy.py
    knowledge.py
    navigation.py
    travel.py

prototype/
  economy.py
  navigation.py
  travel.py

tests/
  test_economy.py
  test_knowledge.py
  test_navigation.py
  test_travel.py
```

## Desenvolvimento

Instalação do núcleo sem dependências gráficas:

```bash
python -m pip install -e .
```

Instalação com a futura camada de jogo em Pygame:

```bash
python -m pip install -e ".[game]"
```

Validação manual:

```bash
python scripts/validate_data.py
python -m unittest discover -s tests -v
python prototype/economy.py
python prototype/navigation.py
python prototype/travel.py
```

O GitHub Actions executa essas verificações automaticamente.

## Fontes de dados

As tabelas em `data/` mantêm campos de proveniência e grau de evidência. Os números em `simulation/` são índices de balanceamento e não devem ser apresentados como dados históricos.

## Licença

GPL-3.0. Consulte `LICENSE`.
