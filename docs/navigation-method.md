# Método de navegação v0.1

## Separação entre evidência e simulação

A navegação mantém quatro camadas distintas:

1. **observação histórica de viagem** — datas documentadas de partida/chegada;
2. **geometria** — distância geodésica calculada entre âncoras cartográficas modernas;
3. **regra ambiental documentada** — regime geral de monções e episódios/limitações descritos nas fontes;
4. **parâmetro de simulação** — multiplicadores e ruído usados para produzir um comportamento jogável.

Nenhuma distância geodésica é descrita como distância efetivamente navegada por uma embarcação histórica.

## Precedência das observações de viagem

Quando existe uma observação documentada para a **mesma rota e a mesma data de partida**, o protótipo preserva a duração observada e não aplica ruído aleatório. Essa regra evita substituir uma cronologia conhecida por uma estimativa produzida a partir de outra rota.

Quando há mais de uma fonte para a mesma partida, as observações permanecem separadas em `voyage_observations.csv` e a duração-base usa a média apenas como convenção explícita de simulação. A divergência documental continua disponível nos dados e não é apagada.

Quando existe observação da rota, mas para outra data, a média observada pode servir como referência relativa e receber o multiplicador sazonal e o ruído de simulação. Somente rotas sem qualquer observação usam a taxa diária derivada da rota de referência.

## Âncora Melinde–Calecute, 1498

Subrahmanyam registra a partida de Melinde em 24 de abril de 1498 e a chegada a Calecute em 21 de maio. Prakash registra a chegada em 20 de maio. O projeto preserva as duas observações, correspondentes a 27 e 26 dias, sem escolher silenciosamente uma delas.

A distância geodésica calculada entre as âncoras cartográficas atuais de Melinde e Calecute é usada somente para derivar uma taxa de progresso diário de referência destinada às rotas que ainda não possuem observações próprias. Essa taxa não é uma medição da velocidade do navio de Gama nem deve ser aplicada como afirmação histórica a outras embarcações.

## Âncora Lisboa–Cabo, 1497

Para a perna agregada `R_LIS_CGH`, a base registra a saída do Tejo em 8 de julho de 1497 e a chegada ao Cabo da Boa Esperança em 19 de novembro segundo Subrahmanyam: 134 dias. A observação é classificada como `AGGREGATED_VOYAGE_LEG`, pois a viagem incluiu escalas e eventos intermediários e não corresponde a 134 dias de navegação ininterrupta.

Quando o cenário histórico parte exatamente em 8 de julho, essa observação tem precedência sobre a antiga extrapolação geodésica baseada em Melinde–Calecute. Isso corrige uma distorção importante: uma taxa calibrada no Índico não pode deslocar artificialmente a chegada ao Cabo para agosto.

A agregação ainda impõe uma limitação para o sistema de provisões: `R_LIS_CGH` não deve ser interpretada como uma única perna operacional sem reabastecimentos. A segmentação do itinerário de 1497 em escalas documentadas é um aprofundamento separado e necessário antes de usar essa aresta agregada como unidade final de jogabilidade.

## Monções

Alpers descreve o regime amplo do Índico da seguinte forma:

- novembro–janeiro: monção de nordeste;
- abril–agosto: monção de sudoeste;
- junho–julho: período em que a monção de sudoeste pode ser tão forte que grande parte da navegação de dhows é interrompida e alguns portos do oeste da Índia e da Malásia chegam a fechar;
- as monções são regulares em escala sazonal, mas continuam sujeitas a calmarias e variação.

A v0.1 converte apenas a forte interrupção de junho/julho em uma penalidade explícita para rotas já classificadas com alta ou média dependência monçônica. **Não** deduz automaticamente que toda rota leste/oeste ou norte/sul é favorecida ou prejudicada por uma determinada monção. Perfis direcionais por trecho só serão adicionados quando houver evidência regional suficiente.

## Pilotos e comando institucional

Subrahmanyam registra que, em Melinde, a armada de Vasco da Gama encontrou quatro navios provenientes de Cranganor e recebeu do governante local um piloto guzerate para a travessia até Calecute. O autor também adverte que esse piloto é frequentemente identificado de forma incorreta como Ahmad ibn Majid.

Por isso a v0.1 mantém `pilots.csv` e `pilot_routes.csv`: o piloto serve como base operacional específica de uma rota, sem bônus arbitrário de velocidade.

A camada de expedições adiciona `FLEET_COMMAND`, mas com função diferente. Um personagem pode participar da perna corrente de uma armada comandada por terceiros sem possuir, antes da viagem, conhecimento náutico pessoal `OPERATIONAL` daquela rota. O comando institucional não aumenta conhecimento individual, não substitui piloto documentado e não concede bônus quantitativo.

Assim, três bases permanecem distintas:

- `OWN_KNOWLEDGE` — o personagem sabe operar a rota;
- `PILOT` — um piloto documentado fornece a competência específica;
- `FLEET_COMMAND` — o personagem acompanha uma expedição cuja perna está institucionalmente definida.

Essa distinção preserva o princípio central do jogo: **saber que um porto existe, saber navegar até ele e participar de uma armada que o percorre são estados diferentes**.

## Provisões e desgaste

O corpus atual não fornece taxas suficientemente sólidas para converter a viagem de 1498 em consumo diário de água, alimento, tonelagem de mantimentos ou desgaste físico comparável entre classes de navio. Esses componentes entram na v0.1 somente como variáveis abstratas de jogabilidade:

- `provision_days`: dias-equivalentes de provisões;
- `condition`: escala abstrata de condição do navio de 0 a 100;
- `travel_rules.csv`: parâmetros de consumo e desgaste exclusivamente de simulação.

Assim, uma viagem de 25 dias de jogo pode consumir 25 dias-equivalentes de provisões sem que isso seja apresentado como uma quantidade histórica de comida ou água. Da mesma forma, a perda de pontos de condição não representa uma taxa histórica de deterioração do casco.

Para pernas agregadas que sabidamente incluíram reabastecimentos intermediários, como Lisboa–Cabo em 1497, o consumo abstrato não deve ser usado como se a aresta fosse uma travessia contínua. A correção preferida é segmentar a expedição em escalas documentadas, não inflar silenciosamente a capacidade do navio.

## Limitações regionais

O Mar Vermelho e o Golfo Pérsico têm condições próprias — ventos predominantes, baixios, marés e gargalos — e não devem ser reduzidos ao calendário monçônico geral. O mesmo vale para acessos portuários dependentes de maré e assoreamento.

## Próximas calibrações

A base deve crescer com observações de viagens cuja partida, chegada e itinerário sejam suficientemente claros. A prioridade imediata é decompor o itinerário de 1497 em escalas historicamente documentadas, permitindo que provisões, reparos e tempo sejam aplicados a pernas operacionais reais em vez de a uma aresta atlântica agregada.

Velocidades por classe de navio, capacidades físicas, taxas de consumo, reparos e efeitos quantitativos de pilotos só devem substituir as escalas abstratas quando houver documentação suficiente para separar esses componentes.
