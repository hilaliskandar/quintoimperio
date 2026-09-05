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
- `pilots.csv` e `pilot_routes.csv` para competência náutica historicamente documentada;
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

## Fase 2 — Navegação, calendário, conhecimento e viagem

Status: **núcleo v0.1 concluído**.

Implementado:

- calendário do jogo;
- fases gerais da monção de nordeste, sudoeste e transições;
- distância geodésica entre nós com coordenadas disponíveis;
- preservação de observações documentadas de viagem e divergências entre fontes;
- primeira calibração de duração com Melinde–Calecute em 1498;
- ruído determinístico de duração;
- penalidade explícita de junho/julho para rotas com dependência monçônica, tratada como parâmetro de simulação;
- `geo_knowledge`, `nav_knowledge`, `market_knowledge` e `political_knowledge`;
- estados separados para personagem e Coroa;
- piloto histórico guzerate de Melinde associado somente à rota documentada até Calecute;
- habilitação de rota por conhecimento náutico próprio ou piloto competente;
- estado imutável do navio;
- dias-equivalentes de provisões;
- condição abstrata do navio em escala 0–100;
- planejamento e execução de viagem;
- bloqueio de partida por falta de provisões, baixa condição ou ausência de base de navegação;
- testes determinísticos e relatórios textuais de navegação/viagem.

Próximos aprofundamentos, sem bloquear a interface:

- eventos de risco marítimo;
- regras para transformar conhecimento parcial em rotas rumoreadas, localizadas e navegáveis;
- perfis direcionais de vento apenas quando documentados por trecho;
- substituição progressiva das escalas abstratas por parâmetros históricos quando houver evidência suficiente.

A implementação continua independente de Pygame.

## Fase 3 — Primeiro mapa e loop jogável

Status: **mapa e serviços portuários v0.1 implementados; comércio jogável em construção**.

Implementado:

- `WorldMapModel` independente de Pygame;
- projeção equiretangular simples de coordenadas reais de `nodes.csv`;
- exclusão automática de nós sem coordenadas defensáveis;
- visibilidade de nós condicionada ao conhecimento geográfico do personagem/Coroa;
- visibilidade de rotas sem revelar conexões classificadas como `UNKNOWN`;
- linhas de rota tratadas como arestas do grafo, não como reconstrução do percurso navegado;
- protótipo Pygame capaz de abrir janela ou renderizar PNG em modo headless;
- ausência deliberada de costa até incorporar dado cartográfico real;
- serviços mínimos de reabastecimento e reparo a partir de `provisions` e `repair` de `nodes.csv`;
- distinção operacional entre serviço desconhecido (`UNKNOWN`) e explicitamente ausente (`NONE`);
- capacidades, limites e duração de serviços isolados em `simulation/port_rules.csv`;
- serviços aplicados ao `VesselState` com avanço do calendário;
- smoke test cartográfico e suíte de 51 testes no GitHub Actions.

Próximo incremento do loop:

1. estado comercial do jogador e capacidade de carga abstrata;
2. consulta de mercado condicionada ao conhecimento comercial;
3. compra e venda apenas de bens documentados no nó/período;
4. seleção de destino navegável no mapa;
5. viagem utilizando o `TravelModel`;
6. chegada, venda e atualização do conhecimento.

A costa de fundo só pode ser incorporada a partir de dados cartográficos reais, com origem, licença e versão documentadas. Não usar mapas geográficos inventados por IA.

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
- conhecimento dividido em quatro dimensões e separado entre personagem e Coroa;
- provisões representadas provisoriamente por dias-equivalentes, não por unidades físicas inventadas;
- desgaste representado provisoriamente por escala abstrata de condição;
- piloto documentado habilita rota específica sem bônus quantitativo não sustentado;
- primeiro mapa usa somente coordenadas reais disponíveis e não inventa costa;
- linhas do mapa representam conexões abstratas do grafo, não derrotas históricas;
- serviço portuário desconhecido não é convertido silenciosamente em serviço ausente ou disponível;
- reabastecimento e reparo usam efeitos abstratos de simulação enquanto faltarem parâmetros históricos defensáveis.

## Decisões ainda abertas

- granularidade temporal final do loop jogável;
- unidade física/abstrata de carga;
- classes de navio e velocidades relativas;
- grau de controle direto do jogador sobre navio e tripulação;
- protagonista e enquadramento exato da campanha;
- conjunto cartográfico real e nível de detalhe da costa;
- modelo de eventos marítimos e avarias;
- unidade monetária/contábil do primeiro protótipo comercial.

Essas decisões devem ser tomadas com protótipos pequenos e testes, não por documentação especulativa.
