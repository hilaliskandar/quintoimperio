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

## Limitações regionais

O Mar Vermelho e o Golfo Pérsico têm condições próprias — ventos predominantes, baixios, marés e gargalos — e não devem ser reduzidos ao calendário monçônico geral. O mesmo vale para acessos portuários dependentes de maré e assoreamento.

## Próximas calibrações

A base deve crescer com observações de viagens cuja partida, chegada e itinerário sejam suficientemente claros. Cada observação deve manter fonte e incerteza. O modelo só ganhará velocidades por classe de navio, duração de escala, desgaste e consumo de provisões depois de existir evidência suficiente para separar esses componentes.
