# Método de navegação v0.1

## Separação entre evidência e simulação

A navegação mantém quatro camadas distintas:

1. **observação histórica de viagem** — datas documentadas de partida/chegada;
2. **geometria** — distância geodésica calculada entre âncoras cartográficas modernas;
3. **regra ambiental documentada** — regime geral de monções e episódios/limitações descritos nas fontes;
4. **parâmetro de simulação** — multiplicadores e ruído usados para produzir um comportamento jogável.

Nenhuma distância geodésica é descrita como distância efetivamente navegada por uma embarcação histórica.

## Primeira âncora: Melinde–Calecute, 1498

Subrahmanyam registra a partida de Melinde em 24 de abril de 1498 e a chegada a Calecute em 21 de maio. Prakash registra a chegada em 20 de maio. O projeto preserva as duas observações em `data/voyage_observations.csv`, correspondentes a 27 e 26 dias, sem escolher silenciosamente uma delas.

A distância geodésica calculada entre as âncoras cartográficas atuais de Melinde e Calecute é usada apenas para derivar uma taxa de progresso diário de referência do protótipo. Essa taxa não é uma medição da velocidade do navio de Gama nem deve ser aplicada como afirmação histórica a outras embarcações.

## Monções

Alpers descreve o regime amplo do Índico da seguinte forma:

- novembro–janeiro: monção de nordeste;
- abril–agosto: monção de sudoeste;
- junho–julho: período em que a monção de sudoeste pode ser tão forte que grande parte da navegação de dhows é interrompida e alguns portos do oeste da Índia e da Malásia chegam a fechar;
- as monções são regulares em escala sazonal, mas continuam sujeitas a calmarias e variação.

A v0.1 converte apenas a forte interrupção de junho/julho em uma penalidade explícita para rotas já classificadas com alta ou média dependência monçônica. **Não** deduz automaticamente que toda rota leste/oeste ou norte/sul é favorecida ou prejudicada por uma determinada monção. Perfis direcionais por trecho só serão adicionados quando houver evidência regional suficiente.

## Pilotos

Subrahmanyam registra que, em Melinde, a armada de Vasco da Gama encontrou quatro navios provenientes de Cranganor e recebeu do governante local um piloto guzerate para a travessia até Calecute. O autor também adverte que esse piloto é frequentemente identificado de forma incorreta como Ahmad ibn Majid.

Por isso a v0.1 introduz duas tabelas históricas específicas:

- `data/pilots.csv` — identidade, origem, local de disponibilidade e período;
- `data/pilot_routes.csv` — competência documentada por rota.

O primeiro piloto é registrado como pessoa não nomeada no corpus atual. Sua competência é ligada somente a `R_MAL_CAL`, em 1498. O modelo não transforma esse dado em bônus arbitrário de velocidade. O piloto serve, por ora, para fornecer a base operacional de navegação necessária a uma rota que o personagem ainda conhece apenas por rumor ou informação parcial.

Essa distinção preserva o princípio central do jogo: **saber que um porto existe não equivale a saber navegar até ele**.

## Provisões e desgaste

O corpus atual não fornece taxas suficientemente sólidas para converter a viagem de 1498 em consumo diário de água, alimento, tonelagem de mantimentos ou desgaste físico comparável entre classes de navio. Esses componentes entram na v0.1 somente como variáveis abstratas de jogabilidade:

- `provision_days`: dias-equivalentes de provisões;
- `condition`: escala abstrata de condição do navio de 0 a 100;
- `travel_rules.csv`: parâmetros de consumo e desgaste exclusivamente de simulação.

Assim, uma viagem de 25 dias de jogo pode consumir 25 dias-equivalentes de provisões sem que isso seja apresentado como uma quantidade histórica de comida ou água. Da mesma forma, a perda de pontos de condição não representa uma taxa histórica de deterioração do casco.

O objetivo desta camada é permitir que o jogador enfrente custo de oportunidade, necessidade de reabastecimento e risco de operar um navio degradado, mantendo totalmente explícita a diferença entre evidência histórica e regra de jogo.

## Limitações regionais

O Mar Vermelho e o Golfo Pérsico têm condições próprias — ventos predominantes, baixios, marés e gargalos — e não devem ser reduzidos ao calendário monçônico geral. O mesmo vale para acessos portuários dependentes de maré e assoreamento.

## Próximas calibrações

A base deve crescer com observações de viagens cuja partida, chegada e itinerário sejam suficientemente claros. Cada observação deve manter fonte e incerteza. Velocidades por classe de navio, capacidades físicas, taxas de consumo, reparos e efeitos quantitativos de pilotos só devem substituir as escalas abstratas quando houver documentação suficiente para separar esses componentes.
