# Roteiro de produção

## Fase 0 — Fundação histórica e de dados

Status: **v0.1 concluída; aprofundamento histórico contínuo**.

Objetivo: estabilizar a primeira representação do mundo de 1497–1500 antes de programar mecânicas definitivas.

Entregas já existentes:

- nós atlânticos e primeiros nós do Índico;
- mercadorias, relações nó–mercadoria, rotas e fluxos;
- observações documentadas de viagem;
- pilotos e competências por rota;
- expedições/armadas, sequência de pernas e permanências logísticas;
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
- itinerário inicial de Gama segmentado em pernas operacionais entre Lisboa, São Thiago, baía de Santa Helena, Cabo, São Brás, Rio do Cobre, Rio dos Bons Sinais, Moçambique, Mombaça, Melinde e Calecute;
- conexões Lisboa–Cabo e Cabo–Moçambique mantidas apenas como `STRATEGIC_AGGREGATE`, bloqueadas para execução;
- permanências logísticas registradas separadamente do tempo de navegação;
- `ChronologyMode.GUIDED` e `COUNTERFACTUAL` para separar reprodução temporal da campanha de trajetórias divergentes;
- bloqueio de partida antes da data documentada numa escala guiada;
- espera explícita até a partida sem efeitos materiais automáticos;
- serviços portuários consumindo o mesmo calendário da permanência;
- ruído determinístico somente quando não há observação exata da partida;
- quatro dimensões de conhecimento por nó;
- conhecimento náutico de rota separado de conhecimento de nó;
- estados separados para personagem e Coroa;
- piloto guzerate de Melinde associado somente à rota documentada;
- bases `OWN_KNOWLEDGE`, `PILOT` e `FLEET_COMMAND`;
- provisões e condição abstratas;
- planejamento/execução de viagem e bloqueios explícitos.

Próximos aprofundamentos:

1. eventos de risco marítimo;
2. perfis direcionais de vento apenas quando documentados por trecho;
3. substituir escalas abstratas somente quando houver evidência suficiente;
4. refinar cronologias editoriais do `Roteiro` quando novas edições/fontes permitirem.

## Fase 3 — Primeiro mapa e loop jogável

Status: **interface jogável v0.1 concluída; campanha histórica em refinamento**.

Implementado:

- mapa de runtime independente da lógica de domínio;
- referência cartográfica programática com costa real e sem fronteiras políticas modernas;
- visibilidade de nós/rotas condicionada ao conhecimento;
- serviços portuários com `UNKNOWN` distinto de `NONE`;
- estado comercial imutável;
- compra/venda apenas em mercados documentados;
- `GameSessionState` reunindo navio, comércio, conhecimento, expedição ativa, cronologia e escala ativa;
- mercado bloqueado até conhecimento operacional;
- reabastecimento/reparo integrados à sessão;
- aprendizagem por chegada e conclusão de rota;
- cenário técnico Calecute → Aden para integração `mercado → compra → viagem → chegada → venda`;
- interface `prototype/game.py` com mapa, porto, data, navio, capital, carga, serviços, mercado, armada ativa, escala, espera e rotas;
- modo `HISTORICAL` iniciado em Lisboa em 8/7/1497 com `EXP_GAMA_1497` e cronologia `GUIDED`;
- modo `TECHNICAL` claramente identificado como não histórico e `COUNTERFACTUAL`;
- `FLEET_COMMAND` visível sem elevar conhecimento pessoal;
- piloto documentado preservado como base específica quando aplicável;
- primeira perna histórica executável Lisboa → São Thiago;
- rotas estratégicas agregadas bloqueadas no domínio;
- escalas guiadas impedindo partida precoce e oferecendo espera apenas pelo tempo restante;
- mudança para cronologia contrafactual quando o jogador ultrapassa a partida histórica e prossegue;
- smoke tests e capturas no GitHub Actions.

Próximos incrementos do loop:

1. introduzir aquisição de informação por rumor, conversa, carta, piloto e contato mercantil;
2. expor diferença entre conhecimento pessoal e institucional sem revelar informação oculta;
3. acrescentar eventos/avarias com regras auditáveis;
4. refinar a interface sem sacrificar a separação entre cartografia e domínio.

## Fase 4 — Portos, instituições e relações

Status: **fundação institucional iniciada**.

Já implementado:

- participação em expedição/armada separada do conhecimento individual;
- sequência de pernas por expedição;
- permanências logísticas documentadas separadas de mercados;
- comando institucional como base de viagem específica;
- piloto como competência distinta do comando;
- serviços portuários mínimos;
- permanência histórica sem efeitos materiais automáticos.

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
2. viagem de 1497 com escalas, permanências e aprendizagem progressiva;
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
- itinerário Lisboa–Moçambique é segmentado para execução e as conexões agregadas ficam apenas como camada estratégica;
- ancoradouro logístico não é convertido automaticamente em mercado;
- datas editoriais do `Roteiro` são marcadas como reconstruções;
- `observed_stay_days` permanece distinto da diferença aritmética entre datas editoriais;
- espera histórica avança apenas o relógio e não concede recursos automaticamente;
- atraso além da partida documentada converte a sessão em cronologia contrafactual em vez de forçar datas históricas;
- limite de provisões continua parâmetro abstrato mesmo quando calibrado para acomodar uma perna histórica longa;
- serviço desconhecido não é tratado como ausente nem disponível;
- cenários técnicos permanecem explicitamente separados do estado histórico;
- identidade/profissão do protagonista continua não fixada.

## Decisões ainda abertas

- unidade física/abstrata de carga definitiva;
- classes de navio e velocidades relativas;
- grau de controle direto do jogador sobre navio e tripulação;
- protagonista e enquadramento exato da campanha;
- eventos marítimos e avarias;
- unidade monetária posterior ao protótipo;
- aquisição de informação por conversa, contrato, rumor, carta e espionagem;
- desenho visual definitivo da interface.

Essas decisões devem ser tomadas com protótipos pequenos e testes, não por documentação especulativa.
