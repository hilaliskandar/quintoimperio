# Roteiro de produção

## Fase 0 — Fundação histórica e de dados

Status: **v0.1 concluída; aprofundamento histórico contínuo**.

Objetivo: estabilizar a primeira representação do mundo de 1497–1500 antes de programar mecânicas definitivas.

Entregas já existentes:

- nós atlânticos e primeiros nós do Índico;
- mercadorias, relações nó–mercadoria, rotas e fluxos;
- observações documentadas de viagem;
- pilotos e competências por rota;
- expedições/armadas e sequência de pernas;
- proveniência, confiança e incerteza explícitas;
- validação automática e testes de domínio.

A pesquisa continua refinando relações e cronologias sem bloquear o protótipo.

## Fase 1 — Protótipo econômico sem interface final

Status: **v0.1 concluída**.

Implementado:

- oferta/demanda relativas derivadas do papel comercial documentado;
- volume, valor e função de troca separados em `simulation/`;
- custos relativos de provisões, frete, acesso/tributação e intermediação;
- estoques estruturais e dependentes de trânsito;
- choques determinísticos por semente;
- testes automatizados.

Nenhum índice é tratado como preço ou quantidade histórica.

## Fase 2 — Navegação, calendário, conhecimento e viagem

Status: **núcleo v0.1 concluído; calibração histórica contínua**.

Implementado:

- calendário e fases gerais da monção;
- distância geodésica de referência e confiança espacial da rota;
- observações documentadas de viagem e divergências entre fontes;
- precedência de observação da mesma rota/data sobre extrapolação geodésica;
- Melinde–Calecute 1498 preservada em 26/27 dias;
- Lisboa–Cabo 1497 registrada como perna agregada de 134 dias segundo a observação usada;
- ruído determinístico somente quando não há observação exata da partida;
- quatro dimensões de conhecimento por nó;
- conhecimento náutico de rota separado de conhecimento de nó;
- estados separados para personagem e Coroa;
- piloto guzerate de Melinde associado somente à rota documentada;
- bases `OWN_KNOWLEDGE`, `PILOT` e `FLEET_COMMAND`;
- provisões e condição abstratas;
- planejamento/execução de viagem e bloqueios explícitos.

Próximos aprofundamentos:

1. segmentar o itinerário de 1497 em escalas documentadas para não tratar Lisboa–Cabo como uma única perna operacional de provisões;
2. eventos de risco marítimo;
3. perfis direcionais de vento apenas quando documentados por trecho;
4. substituir escalas abstratas somente quando houver evidência suficiente.

## Fase 3 — Primeiro mapa e loop jogável

Status: **interface jogável v0.1 concluída; campanha histórica em refinamento**.

Implementado:

- mapa de runtime independente da lógica de domínio;
- referência cartográfica programática com costa real e sem fronteiras políticas modernas;
- visibilidade de nós/rotas condicionada ao conhecimento;
- serviços portuários com `UNKNOWN` distinto de `NONE`;
- estado comercial imutável;
- compra/venda apenas em mercados documentados;
- `GameSessionState` reunindo navio, comércio, conhecimento e expedição ativa;
- mercado bloqueado até conhecimento operacional;
- reabastecimento/reparo integrados à sessão;
- aprendizagem por chegada e conclusão de rota;
- cenário técnico Calecute → Aden para integração `mercado → compra → viagem → chegada → venda`;
- interface `prototype/game.py` com mapa, porto, data, navio, capital, carga, serviços, mercado, armada ativa e rotas;
- modo `HISTORICAL` iniciado em Lisboa em 8/7/1497 com `EXP_GAMA_1497`;
- modo `TECHNICAL` claramente identificado como não histórico;
- `FLEET_COMMAND` visível sem elevar conhecimento pessoal;
- piloto documentado preservado como base específica quando aplicável;
- smoke tests e capturas no GitHub Actions.

Próximos incrementos do loop:

1. decompor a primeira viagem em escalas operacionais documentadas;
2. introduzir aquisição de informação por rumor, conversa, carta, piloto e contato mercantil;
3. expor diferença entre conhecimento pessoal e institucional sem revelar informação oculta;
4. acrescentar eventos/avarias com regras auditáveis;
5. refinar a interface sem sacrificar a separação entre cartografia e domínio.

## Fase 4 — Portos, instituições e relações

Status: **fundação institucional iniciada**.

Já implementado:

- participação em expedição/armada separada do conhecimento individual;
- sequência de pernas por expedição;
- comando institucional como base de viagem específica;
- piloto como competência distinta do comando;
- serviços portuários mínimos.

Ainda por implementar:

- regimes de acesso e negociação;
- intermediários e comunidades mercantis;
- reputação com autoridades e grupos comerciais;
- impostos, monopólios, privilégios e presentes diplomáticos;
- contratos e crédito;
- aquisição/transferência de informação;
- hierarquia mais detalhada de capitães, mestres, pilotos, escrivães, marinheiros e soldados, apenas se necessária ao jogo e sustentada pela documentação.

## Fase 5 — Campanha 1497–1505

Recorte inicial:

1. Lisboa e rede atlântica conhecida;
2. viagem de 1497 com escalas e aprendizagem progressiva;
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

- Python 3.12 + pygame-ce no primeiro jogável;
- domínio independente da interface;
- dados históricos separados dos parâmetros de simulação;
- preços históricos não são inventados;
- linhas do mapa são arestas do grafo, não derrotas;
- conhecimento de nó, conhecimento de rota e comando institucional são estados distintos;
- personagem e Coroa possuem estados de conhecimento separados;
- piloto documentado não recebe bônus quantitativo não sustentado;
- `FLEET_COMMAND` não aumenta conhecimento pessoal antes da viagem;
- observação exata de viagem tem precedência sobre ruído/extrapolação;
- serviço desconhecido não é tratado como ausente nem disponível;
- cenários técnicos permanecem explicitamente separados do estado histórico;
- identidade/profissão do protagonista continua não fixada.

## Decisões ainda abertas

- segmentação operacional final do itinerário de 1497;
- unidade física/abstrata de carga definitiva;
- classes de navio e velocidades relativas;
- grau de controle direto do jogador sobre navio e tripulação;
- protagonista e enquadramento exato da campanha;
- eventos marítimos e avarias;
- unidade monetária posterior ao protótipo;
- aquisição de informação por conversa, contrato, rumor, carta e espionagem;
- desenho visual definitivo da interface.

Essas decisões devem ser tomadas com protótipos pequenos e testes, não por documentação especulativa.
