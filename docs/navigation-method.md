# Método de navegação v0.1

## Separação entre evidência e simulação

A navegação mantém quatro camadas distintas:

1. **observação histórica de viagem** — datas documentadas ou reconstruídas editorialmente de partida/chegada;
2. **geometria** — distância geodésica calculada entre âncoras cartográficas modernas;
3. **regra ambiental documentada** — regime geral de monções e episódios/limitações descritos nas fontes;
4. **parâmetro de simulação** — multiplicadores e ruído usados para produzir comportamento jogável.

Nenhuma distância geodésica é descrita como distância efetivamente navegada por uma embarcação histórica.

## Precedência das observações de viagem

Quando existe uma observação para a **mesma rota e a mesma data de partida**, o protótipo preserva a duração observada e não aplica ruído aleatório. Essa regra evita substituir uma cronologia conhecida por uma estimativa produzida a partir de outra rota.

Quando há mais de uma fonte para a mesma partida, as observações permanecem separadas em `voyage_observations.csv` e a duração-base usa a média apenas como convenção explícita de simulação. A divergência documental continua disponível nos dados.

Quando existe observação da rota, mas para outra data, a média observada pode servir como referência relativa e receber multiplicador sazonal e ruído. Somente rotas sem observação usam a taxa diária derivada da rota de referência.

## Âncora Melinde–Calecute, 1498

Subrahmanyam registra a partida de Melinde em 24 de abril de 1498 e a chegada a Calecute em 21 de maio. Prakash registra a chegada em 20 de maio. O projeto preserva as duas observações, correspondentes a 27 e 26 dias, sem escolher silenciosamente uma delas.

A distância geodésica entre as âncoras atuais de Melinde e Calecute é usada somente para derivar uma taxa de progresso diário de referência destinada às rotas que ainda não possuem observações próprias. Essa taxa não é uma medição da velocidade do navio de Gama nem deve ser aplicada como afirmação histórica universal.

## Segmentação da viagem de 1497–1498

O `Roteiro da primeira viagem de Vasco da Gama` passa a sustentar observações segmentadas para o itinerário inicial. A edição Ravenstein informa que palavras e datas ausentes do manuscrito foram colocadas entre colchetes; por isso essas datas são marcadas como reconstruções editoriais e recebem grau de evidência mais cauteloso quando apropriado.

A sequência operacional registrada é:

- Lisboa → São Thiago / baía de Santa Maria;
- São Thiago → baía de Santa Helena;
- baía de Santa Helena → Cabo da Boa Esperança;
- Cabo → angra de São Brás;
- São Brás → Rio do Cobre / Terra da Boa Gente;
- Rio do Cobre → Rio dos Bons Sinais;
- Rio dos Bons Sinais → Moçambique;
- Moçambique → Mombaça;
- Mombaça → Melinde;
- Melinde → Calecute.

A observação agregada Lisboa–Cabo de Subrahmanyam, 8 de julho a 19 de novembro de 1497, permanece no banco como `AGGREGATED_VOYAGE_LEG` para comparação historiográfica. `R_LIS_CGH` e `R_CGH_MOZ` permanecem no grafo como `STRATEGIC_AGGREGATE`, mas o domínio impede sua execução como viagens únicas.

Essa separação resolve dois problemas: não interpreta 134 dias como navegação contínua sem escalas e não força o sistema de provisões a representar, numa única aresta, reabastecimentos e reparos conhecidos.

## Permanências

`expedition_stops.csv` registra permanências separadamente de deslocamentos. A primeira base inclui:

- São Thiago: carne, água, madeira e reparo de vergas;
- baía de Santa Helena: limpeza dos navios, reparo de velas e madeira;
- São Brás: desmonte da nau de mantimentos, transferência de carga, água e troca por gado;
- Rio do Cobre: tomada de água;
- Rio dos Bons Sinais: água, carenagem, reparo do mastro e adoecimento de tripulantes.

O tempo de permanência não é automaticamente convertido em quantidade de recurso. Em especial, a declaração de 32 dias no Rio dos Bons Sinais é preservada como duração fornecida pela fonte mesmo que uma contagem aritmética de datas editoriais use convenção diferente.

## Monções

Alpers descreve o regime amplo do Índico da seguinte forma:

- novembro–janeiro: monção de nordeste;
- abril–agosto: monção de sudoeste;
- junho–julho: período em que a monção de sudoeste pode ser tão forte que grande parte da navegação de dhows é interrompida e alguns portos do oeste da Índia e da Malásia chegam a fechar;
- as monções são regulares em escala sazonal, mas continuam sujeitas a calmarias e variação.

A v0.1 converte apenas a forte interrupção de junho/julho em penalidade explícita para rotas já classificadas com alta ou média dependência monçônica. **Não** deduz automaticamente que toda rota leste/oeste ou norte/sul é favorecida ou prejudicada por uma determinada monção. Perfis direcionais por trecho só serão adicionados quando houver evidência regional suficiente.

## Pilotos e comando institucional

Subrahmanyam registra que, em Melinde, a armada de Vasco da Gama encontrou navios provenientes da costa indiana e recebeu do governante local um piloto guzerate para a travessia até Calecute. O projeto mantém esse piloto em `pilots.csv`/`pilot_routes.csv`, sem atribuir nome não sustentado nem bônus arbitrário de velocidade.

A camada de expedições adiciona `FLEET_COMMAND`, com função diferente. Um personagem pode participar da perna corrente de uma armada comandada por terceiros sem possuir, antes da viagem, conhecimento náutico pessoal `OPERATIONAL` daquela rota. O comando institucional não aumenta conhecimento individual, não substitui piloto documentado e não concede bônus quantitativo.

Assim, três bases permanecem distintas:

- `OWN_KNOWLEDGE` — o personagem sabe operar a rota;
- `PILOT` — um piloto documentado fornece a competência específica;
- `FLEET_COMMAND` — o personagem acompanha uma expedição cuja perna está institucionalmente definida.

## Provisões e desgaste

O corpus atual não fornece taxas suficientemente sólidas para converter a viagem em consumo diário de água, alimento, tonelagem de mantimentos ou desgaste físico comparável entre classes de navio. Esses componentes entram somente como variáveis abstratas:

- `provision_days`: dias-equivalentes de provisões;
- `condition`: escala abstrata de condição do navio de 0 a 100;
- `travel_rules.csv`: consumo e desgaste exclusivamente de simulação.

O limite máximo abstrato de provisões foi elevado de 90 para 120 dias-equivalentes para que a perna observada São Thiago–baía de Santa Helena, com 96 dias na cronologia usada, seja representável. **120 não é uma capacidade histórica**: não afirma tonelagem, peso de água, ração, autonomia física ou capacidade de uma nau específica.

## Incerteza espacial

Coordenadas de ancoradouros são âncoras cartográficas para mapa e distância geodésica. Não equivalem automaticamente à posição exata do fundeadouro de 1497. O Rio do Cobre é particularmente incerto e permanece `LOW`; sua associação moderna com Závora é tratada apenas como proxy regional.

## Limitações regionais

O Mar Vermelho e o Golfo Pérsico têm condições próprias — ventos predominantes, baixios, marés e gargalos — e não devem ser reduzidos ao calendário monçônico geral. O mesmo vale para acessos portuários dependentes de maré e assoreamento.

## Próximas calibrações

A próxima tarefa não é voltar a agregar as pernas, mas integrar as permanências documentadas ao calendário e às ações do jogador. Velocidades por classe de navio, capacidades físicas, taxas de consumo, reparos e efeitos quantitativos de pilotos só devem substituir as escalas abstratas quando houver documentação suficiente para separar esses componentes.
