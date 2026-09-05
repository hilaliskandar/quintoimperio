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

A fundação histórica v0.1 e o primeiro protótipo econômico estão operacionais.

A base validada contém 20 nós, 14 bens, 41 relações nó–bem, 12 rotas e 15 fluxos de mercadorias. O protótipo econômico possui oito testes determinísticos e mantém parâmetros de balanceamento separados da evidência histórica.

A arquitetura do primeiro jogável foi definida no ADR 0001: **Python 3.12 + pygame-ce**, com núcleo de domínio independente da interface gráfica.

Próxima fase: navegação, calendário, monções e conhecimento do jogador, seguida por um mapa 2D mínimo construído a partir de coordenadas reais.

## Estrutura

```text
data/
  README.md
  nodes.csv
  goods.csv
  node_goods.csv
  routes.csv
  route_goods.csv

simulation/
  README.md
  goods_params.csv
  rules.csv

docs/
  historical-method.md
  roadmap.md
  sources.md
  adr/
    0001-runtime-and-engine.md

src/quintoimperio/
  data/
  domain/

prototype/
  economy.py

tests/
  test_economy.py
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
```

O GitHub Actions executa essas verificações automaticamente.

## Fontes de dados

As tabelas em `data/` mantêm campos de proveniência e grau de evidência. Os números em `simulation/` são índices de balanceamento e não devem ser apresentados como dados históricos.

## Licença

GPL-3.0. Consulte `LICENSE`.
