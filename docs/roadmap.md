# Roteiro de produção

## Fase 0 — Fundação histórica e de dados

Objetivo: estabilizar a primeira representação do mundo de 1497–1500 antes de programar mecânicas definitivas.

Entregas:

- `nodes.csv` com nós atlânticos e primeiros nós do Índico;
- `goods.csv` com conjunto mínimo de bens;
- `node_goods.csv` distinguindo produção, hinterland, importação, exportação e trânsito;
- `routes.csv` com conexões históricas e propriedades de navegação;
- `route_goods.csv` com fluxos por mercadoria;
- documentação de proveniência e incerteza;
- lista explícita de lacunas bibliográficas.

Critério de conclusão: todas as relações usadas no protótipo devem ser classificadas por evidência e período.

## Fase 1 — Protótipo econômico sem interface final

Objetivo: testar se a rede produz circuitos plausíveis sem impor lucros manualmente.

Sistemas mínimos:

- inventário e capacidade de carga;
- classes relativas de oferta e demanda;
- custos de provisões, frete e tributação;
- estoques estruturais e estoques dependentes de trânsito;
- calendário;
- sementes determinísticas para testes.

Testes históricos esperados:

- ouro africano possuir utilidade como poder de compra;
- pimenta ser estruturalmente abundante no Malabar e cara em mercados distantes;
- mercadorias em trânsito terem estoque mais volátil;
- tecidos indianos funcionarem como mercadoria de troca em circuitos orientais.

## Fase 2 — Navegação e conhecimento

Objetivo: transformar o mapa em sistema histórico, não em simples grafo de distâncias.

Sistemas:

- vento, monção e sazonalidade;
- duração probabilística de viagem;
- provisões e desgaste;
- pilotos;
- `geo_knowledge`, `nav_knowledge`, `market_knowledge` e `political_knowledge`;
- nós desconhecidos, rumoreados, localizados e navegáveis;
- eventos de risco marítimo.

## Fase 3 — Portos, instituições e relações

Sistemas:

- regimes de acesso;
- feitorias, capitanias, praças, mercados estrangeiros e pontos náuticos;
- intermediários e comunidades mercantis;
- reputação com autoridades e grupos comerciais;
- impostos, monopólios, privilégios e presentes diplomáticos;
- contratos e crédito.

## Fase 4 — Campanha 1497–1505

Recorte inicial recomendado:

1. Lisboa e rede atlântica conhecida;
2. travessia do Cabo;
3. Moçambique, Mombasa e Malindi;
4. chegada a Calecute;
5. retorno e reconfiguração após a primeira viagem;
6. expansão inicial até Cochim e primeiras estruturas portuguesas.

O jogo deve permitir que o jogador compreenda a diferença entre a rede atlântica portuguesa já estabelecida e a rede índica preexistente.

## Fase 5 — Expansão 1505–1540

Somente após estabilizar o núcleo:

- Goa;
- Ormuz;
- Malaca;
- carreiras intra-asiáticas;
- cartaz;
- comércio privado e casados;
- Coromandel, Bengala e Sudeste Asiático.

## Decisões ainda abertas

- motor do protótipo e da versão final;
- granularidade temporal;
- unidade de carga;
- modelo de preços relativos;
- grau de controle direto do jogador sobre navio e tripulação;
- escopo exato do protagonista e da campanha.

Essas decisões devem ser tomadas com protótipos pequenos, não por documentação especulativa.
