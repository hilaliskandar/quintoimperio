# Roteiro de produção

## Fase 0 — Fundação histórica e de dados

Status: **v0.1 concluída; aprofundamento histórico contínuo**.

Objetivo: estabilizar a primeira representação do mundo de 1497–1500 antes de programar mecânicas definitivas.

Entregas já existentes:

- `nodes.csv` com nós atlânticos e primeiros nós do Índico;
- `goods.csv` com conjunto mínimo de bens;
- `node_goods.csv` distinguindo produção, hinterland, importação, exportação e trânsito;
- `routes.csv` com conexões históricas e propriedades de navegação;
- `route_goods.csv` com fluxos por mercadoria;
- `voyage_observations.csv` para âncoras documentadas de viagem;
- documentação de proveniência e incerteza;
- validação automática dos CSVs;
- lista explícita de lacunas bibliográficas.

A pesquisa continua refinando relações e cronologias sem bloquear o protótipo.

## Fase 1 — Protótipo econômico sem interface final

Status: **v0.1 concluída**.

O protótipo atual já inclui:

- classes relativas de oferta e demanda derivadas do papel comercial documentado;
- volume, valor e função de troca como parâmetros separados em `simulation/`;
- custos relativos de provisões, frete, acesso/tributação e intermediação;
- estoques estruturais e estoques dependentes de trânsito;
- choques determinísticos por semente;
- testes automatizados;
- relatório textual de inspeção.

Invariantes validadas:

- ouro possui alta função de troca no modelo;
- pimenta é estruturalmente mais disponível no Malabar que em Lisboa no estado inicial;
- mercadorias em trânsito em Moçambique são mais voláteis que a oferta de hinterland no Malabar;
- tecidos indianos habilitam o circuito Gujarat–Melaka.

Nenhum índice da simulação é tratado como preço ou quantidade histórica.

## Fase 2 — Navegação, calendário e conhecimento

Status: **núcleo v0.1 implementado; logística de viagem em andamento**.

Já implementado:

- calendário do jogo;
- fases gerais da monção de nordeste, sudoeste e transições;
- distância geodésica entre nós com coordenadas disponíveis;
- preservação de observações documentadas de viagem e divergências entre fontes;
- primeira calibração de duração com Melinde–Calecute em 1498;
- ruído determinístico de duração;
- penalidade explícita de junho/julho para rotas com dependência monçônica, tratada como parâmetro de simulação;
- `geo_knowledge`, `nav_knowledge`, `market_knowledge` e `political_knowledge`;
- estados separados para personagem e Coroa;
- testes determinísticos e relatório textual de navegação.

Próximo incremento da fase:

- provisões e consumo diário;
- desgaste do navio;
- pilotos e competência regional;
- estado de viagem e chegada;
- eventos de risco marítimo;
- regras para transformar conhecimento parcial em rotas rumoreadas, localizadas e navegáveis;
- perfis direcionais de vento apenas quando documentados por trecho.

A implementação continua independente de Pygame.

## Fase 3 — Primeiro mapa e loop jogável

Objetivo: colocar o domínio validado numa interface 2D mínima.

Arquitetura definida pelo ADR 0001: Python 3.12 + pygame-ce.

Loop mínimo:

1. consultar mapa e informações conhecidas;
2. entrar em um porto;
3. consultar mercado;
4. comprar carga dentro da capacidade;
5. escolher destino navegável;
6. consumir tempo e provisões na viagem;
7. processar risco/evento;
8. chegar e vender;
9. atualizar conhecimento e relações.

O mapa deve partir de coordenadas reais e, quando houver costa de fundo, de dados cartográficos reais. Não usar mapas geográficos inventados por IA.

## Fase 4 — Portos, instituições e relações

Sistemas:

- regimes de acesso;
- feitorias, capitanias, praças, mercados estrangeiros e pontos náuticos;
- intermediários e comunidades mercantis;
- reputação com autoridades e grupos comerciais;
- impostos, monopólios, privilégios e presentes diplomáticos;
- contratos e crédito.

## Fase 5 — Campanha 1497–1505

Recorte inicial recomendado:

1. Lisboa e rede atlântica conhecida;
2. travessia do Cabo;
3. Moçambique, Mombaça e Melinde;
4. chegada a Calecute;
5. retorno e reconfiguração após a primeira viagem;
6. expansão inicial até Cochim e primeiras estruturas portuguesas.

O jogo deve deixar clara a diferença entre a rede atlântica portuguesa já estabelecida e a rede índica preexistente.

## Fase 6 — Expansão 1505–1540

Somente após estabilizar o núcleo:

- Goa;
- Ormuz;
- Malaca;
- carreiras intra-asiáticas;
- cartaz;
- comércio privado e casados;
- Coromandel, Bengala e Sudeste Asiático.

## Decisões resolvidas

- motor do primeiro jogável: Python 3.12 + pygame-ce;
- lógica de domínio independente da camada gráfica;
- CSVs históricos separados dos parâmetros de simulação;
- ausência de preços históricos fictícios na calibração inicial;
- distância de rota calculada como geodésica de referência, não confundida com percurso histórico efetivo;
- conhecimento dividido em quatro dimensões e separado entre personagem e Coroa.

## Decisões ainda abertas

- granularidade temporal final do loop jogável;
- unidade física/abstrata de carga;
- modelo de provisões e desgaste;
- classes de navio e velocidades relativas;
- grau de controle direto do jogador sobre navio e tripulação;
- protagonista e enquadramento exato da campanha;
- formato definitivo do mapa costeiro e nível de detalhe cartográfico.

Essas decisões devem ser tomadas com protótipos pequenos e testes, não por documentação especulativa.
