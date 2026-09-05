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

Fase 0 — fundação histórica e arquitetura de dados.

O corpus inicial cobre expansão atlântica portuguesa anterior a Vasco da Gama, costa suaíli, Malabar, Gujarat e redes do Índico. A programação do protótipo começa somente após estabilizar um subconjunto mínimo de nós, bens, rotas e regras de navegação.

## Estrutura

```text
data/
  README.md
  nodes.csv
  goods.csv
  node_goods.csv
  routes.csv
  route_goods.csv

docs/
  historical-method.md
  roadmap.md

src/
  (reservado ao protótipo)
```

## Fontes de dados

As tabelas em `data/` devem manter campos de proveniência e grau de evidência. Nenhum valor de simulação deve ser apresentado como dado histórico sem fonte explícita.

## Licença

GPL-3.0. Consulte `LICENSE`.
