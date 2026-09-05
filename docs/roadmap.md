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

Todos os 20 nós da base inicial possuem uma âncora cartográfica explícita. Mpinda/Soyo e Sofala usam coordenadas provisórias de confiança `MEDIUM`, documentadas separadamente para não serem confundidas com localização arqueológica exata.

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
- propagação da confiança espacial mínima da rota;
- preservação de observações documentadas de viagem e divergências entre fontes;
- primeira calibração de duração com Melinde–Calecute em 1498;
- ruído determinístico de duração;
- penalidade explícita de junho/julho para rotas com dependência monçônica;
- `geo_knowledge`, `nav_knowledge`, `market_knowledge` e `political_knowledge`;
- estados separados para personagem e Coroa;
- conhecimento náutico de rota separado do conhecimento de nó;
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
- aquisição de rumores e informação comercial por interação;
- perfis direcionais de vento apenas quando documentados por trecho;
- substituição progressiva das escalas abstratas por parâmetros históricos quando houver evidência suficiente.

## Fase 3 — Primeiro mapa e loop jogável

Status: **interface jogável v0.1 concluída; refinamento do loop em andamento**.

Implementado:

- `WorldMapModel` independente de Pygame;
- projeção equiretangular de runtime;
- referência cartográfica programática com costa real e sem fronteiras políticas modernas;
- estética náutica procedural sobre a geometria real;
- âncoras provisórias de Mpinda/Soyo e Sofala identificadas e documentadas;
- visibilidade de nós e rotas condicionada ao conhecimento;
- serviços mínimos de reabastecimento e reparo;
- distinção operacional entre serviço `UNKNOWN` e `NONE`;
- `CommercialState` imutável com capital, capacidade e inventário abstratos;
- compra e venda somente em mercados documentados;
- bloqueio por falta de capital, capacidade ou inventário;
- `RouteKnowledgeModel` separado de `KnowledgeModel`;
- `GameSessionState` reunindo navio, estado comercial, conhecimento por nó e conhecimento por rota;
- mercado do porto atual bloqueado até `market_knowledge >= OPERATIONAL`;
- planejamento de viagem usando conhecimento da rota ou piloto historicamente documentado;
- aprendizagem por chegada e por conclusão de rota definida em `simulation/session_rules.csv`;
- teste histórico de aprendizagem Melinde → Calecute com piloto guzerate;
- cenário técnico determinístico Calecute → Aden capaz de executar `mercado → compra → viagem → chegada → venda`;
- cenário técnico explicitamente separado do estado histórico inicial;
- interface `prototype/game.py` mostrando mapa conhecido, porto, data, navio, capital, carga, mercado e rotas de saída;
- compra e venda unitárias abstratas acionáveis por clique;
- seleção de rota pela lista ou pelo destino no mapa;
- execução de viagem delegada ao `GameSessionModel`;
- busca automática somente de piloto documentado, ativo no porto/período/rota;
- modo `HISTORICAL` que preserva bloqueios do estado inicial e modo `TECHNICAL` claramente marcado como não histórico;
- reinício por `R`, alternância de cenário por `Tab` e encerramento por `Esc`;
- renderização headless dos dois cenários e publicação das capturas como artefato do GitHub Actions;
- suíte automatizada e smoke tests no GitHub Actions.

Próximos incrementos do loop:

1. integrar reabastecimento e reparo ao `GameSessionModel`, para que serviços portuários sejam acionáveis pela mesma sessão;
2. modelar a forma institucional de participação do personagem numa armada comandada pela Coroa, evitando transformar conhecimento náutico individual em requisito para toda viagem histórica;
3. introduzir aquisição de informação por conversa, rumor, carta, piloto e contato mercantil;
4. expor diferenças entre conhecimento do personagem e conhecimento institucional da Coroa sem revelar informação oculta diretamente;
5. acrescentar eventos marítimos e avarias somente depois de estabelecer regras auditáveis;
6. refinar a interface e incorporar, quando tecnicamente adequado, a costa real também ao runtime sem criar dependência cartográfica pesada no núcleo.

A cartografia visual deve continuar programática e reprodutível. Elementos decorativos podem evocar cartas náuticas, mas não podem alterar costa, coordenadas ou trajetos do grafo.

## Fase 4 — Portos, instituições e relações

Status: **fundação conceitual pronta; implementação ainda não iniciada como sistema integrado**.

Sistemas:

- regimes de acesso;
- feitorias, capitanias, praças, mercados estrangeiros e pontos náuticos;
- intermediários e comunidades mercantis;
- reputação com autoridades e grupos comerciais;
- impostos, monopólios, privilégios e presentes diplomáticos;
- contratos e crédito;
- cadeia de comando e participação em armadas;
- acesso a informação, pilotos e corretores como relações institucionais.

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
- distância de rota calculada como geodésica de referência;
- confiança espacial da rota acompanha a menor confiança entre seus pontos extremos;
- conhecimento de nó e conhecimento de rota são dimensões distintas;
- conhecimento é separado entre personagem e Coroa;
- provisões e desgaste permanecem escalas abstratas;
- piloto documentado habilita rota específica sem bônus quantitativo não sustentado;
- todos os nós da base inicial possuem âncora cartográfica com incerteza explícita quando necessário;
- mapa de referência usa costa real e não desenha fronteiras políticas modernas;
- estética histórica do mapa é procedural e separada da geometria;
- linhas do mapa representam conexões abstratas do grafo, não derrotas históricas;
- serviço portuário desconhecido não é convertido silenciosamente em serviço ausente ou disponível;
- comércio v0.1 usa capital, carga e preço como índices de simulação;
- mercadoria ausente de `node_goods.csv` não é criada artificialmente no mercado;
- presença física em porto e conclusão de rota produzem aprendizado apenas por regras explícitas de simulação;
- cenários técnicos podem conceder conhecimento por override apenas quando identificados como não históricos;
- a interface não cria permissões ou conhecimento para contornar bloqueios do domínio;
- o estado `HISTORICAL` e o cenário `TECHNICAL` permanecem visivelmente distintos na interface.

## Decisões ainda abertas

- granularidade temporal final do loop jogável;
- unidade física/abstrata de carga definitiva;
- classes de navio e velocidades relativas;
- grau de controle direto do jogador sobre navio e tripulação;
- protagonista e enquadramento exato da campanha;
- refinamento arqueológico/cartográfico de Mpinda/Soyo e Sofala;
- modelo de eventos marítimos e avarias;
- unidade monetária/contábil histórica ou abstrata da versão posterior ao protótipo;
- forma de aquisição de informação por conversa, contrato, rumor, carta e espionagem;
- cadeia de comando e relação entre conhecimento pessoal, piloto, capitão e ordem da Coroa;
- desenho visual definitivo da interface.

Essas decisões devem ser tomadas com protótipos pequenos e testes, não por documentação especulativa.
