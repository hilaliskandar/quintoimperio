# Evidência — armada de Vasco da Gama, 1497–1499

## Escopo

Esta ficha sustenta a camada institucional e a primeira segmentação operacional da campanha: havia uma armada com comando nomeado, um itinerário documentado e permanências logísticas distintas antes da chegada ao Índico. Ela **não** define a identidade do protagonista, não afirma que Vasco da Gama pilotava pessoalmente cada trecho e não transforma cadeia de comando em conhecimento náutico individual.

## Fontes

### *Roteiro da primeira viagem de Vasco da Gama* — `ROTEIRO_GAMA_1497`

O relato de participante da viagem é a fonte primária usada para a cronologia fina das escalas. A edição/tradução de E. G. Ravenstein, Hakluyt Society, 1898, informa explicitamente que palavras e datas ausentes do manuscrito foram colocadas entre colchetes. Por isso, datas calendarizadas dessa forma são registradas como reconstruções editoriais e recebem cautela adicional na base.

O `Roteiro` permite distinguir deslocamento de permanência logística. Entre Lisboa e Moçambique, a base registra:

- Lisboa → São Thiago / baía de Santa Maria;
- São Thiago → baía de Santa Helena;
- baía de Santa Helena → Cabo da Boa Esperança;
- Cabo → angra de São Brás;
- São Brás → Rio do Cobre / Terra da Boa Gente;
- Rio do Cobre → Rio dos Bons Sinais;
- Rio dos Bons Sinais → Ilha de Moçambique.

Também sustenta permanências para carne, água, madeira, reparos, limpeza/carenagem, transferência da carga da nau de mantimentos e recuperação de avarias. Esses pontos são modelados como ancoradouros logísticos ou marcos náuticos quando a fonte não sustenta um mercado permanente.

### Malyn Newitt — `NEWITT_PEW`

Em *Portugal in European and World History*, Newitt descreve a preparação de uma pequena frota de quatro navios em 1497. Segundo a síntese, D. Manuel investiu relativamente pouco na expedição, uma embarcação foi fornecida pelo banco Marchioni e Vasco da Gama, juntamente com seu irmão Paulo, foi nomeado para o comando. Newitt observa também que a frota estava mal preparada para a missão diplomática que encontraria no Índico.

Uso no projeto:

- existência de uma expedição organizada em 1497;
- chefia nomeada de Vasco da Gama;
- financiamento não reduzido a uma operação puramente estatal;
- cautela contra representar a armada como máquina estatal plenamente preparada;
- enquadramento da grande volta do Atlântico Sul como resultado de conhecimento náutico acumulado, não como linha geodésica direta.

### Sanjay Subrahmanyam — `SUBRAHMANYAM_PEA`

Em *The Portuguese Empire in Asia, 1500–1700*, Subrahmanyam trata Vasco da Gama como capitão-mor e reconstrói a sequência agregada: saída do Tejo em 8 de julho de 1497, chegada ao Cabo em 19 de novembro, contato com Moçambique no início de março de 1498, passagem por Mombaça e Melinde e partida de Melinde em 24 de abril para Calecute. A discussão registra especialistas embarcados e a dependência de conhecimento local no trecho final.

A data de 19 de novembro para o Cabo é preservada como observação agregada de Subrahmanyam. O `Roteiro`, em contraste, permite separar avistamento, tentativa frustrada e dobragem do Cabo. A base não harmoniza silenciosamente essas formulações.

## Tradução para o domínio

`data/expeditions.csv` registra a expedição e sua chefia. `data/expedition_routes.csv` registra dez pernas operacionais:

1. `R_LIS_STG` — Lisboa → São Thiago;
2. `R_STG_SHB` — São Thiago → baía de Santa Helena;
3. `R_SHB_CGH` — baía de Santa Helena → Cabo da Boa Esperança;
4. `R_CGH_SBR` — Cabo → angra de São Brás;
5. `R_SBR_RCO` — São Brás → Rio do Cobre;
6. `R_RCO_RBS` — Rio do Cobre → Rio dos Bons Sinais;
7. `R_RBS_MOZ` — Rio dos Bons Sinais → Moçambique;
8. `R_MOZ_MOM` — Moçambique → Mombaça;
9. `R_MOM_MAL` — Mombaça → Melinde;
10. `R_MAL_CAL` — Melinde → Calecute.

`R_LIS_CGH` e `R_CGH_MOZ` permanecem em `routes.csv` apenas como `STRATEGIC_AGGREGATE`, úteis para leitura de rede e comparação historiográfica. O domínio bloqueia sua execução como uma única viagem.

`data/expedition_stops.csv` registra separadamente as permanências em São Thiago, baía de Santa Helena, São Brás, Rio do Cobre e Rio dos Bons Sinais. Isso impede que abastecimento, reparo e espera sejam confundidos com tempo de navegação.

## Regra de modelagem

A base `FLEET_COMMAND` significa somente: um personagem que esteja participando da expedição ativa pode acompanhar a perna corrente sob o comando institucional da armada mesmo sem possuir conhecimento náutico individual `OPERATIONAL` daquela rota.

A regra não:

- aumenta o conhecimento pessoal antes da partida;
- concede bônus de velocidade, segurança, consumo ou desgaste;
- substitui um piloto documentado quando ele existe;
- autoriza rotas fora da sequência da expedição;
- torna uma rota `STRATEGIC_AGGREGATE` executável;
- fixa ocupação, estatuto social ou biografia do protagonista.

Depois de completar a viagem, o aprendizado individual segue `simulation/session_rules.csv`, como em qualquer outra rota efetivamente percorrida.

## Provisões e permanências

O limite de provisões da simulação foi elevado para permitir a longa perna São Thiago–baía de Santa Helena. Esse valor é deliberadamente um índice abstrato: não representa tonelagem histórica, dieta, consumo diário, água por tripulante ou capacidade de uma nau específica.

As permanências históricas ainda não são automaticamente executadas como uma sequência fechada de ações do jogador. A v0.1 registra os fatos — duração, água, madeira, reparos, carenagem e transferência de carga — sem inventar quantidades físicas. A integração dessas permanências ao calendário jogável é um incremento posterior.

## Incerteza espacial

A identificação de alguns pontos é editorial ou discutida. São Thiago/baía de Santa Maria, baía de Santa Helena, São Brás e Rio dos Bons Sinais usam âncoras regionais modernas com confiança `MEDIUM`. O Rio do Cobre usa uma âncora `LOW`, porque sua associação moderna com Závora não é suficientemente segura para ser tratada como localização exata.

## Limitações

A camada atual não modela ainda hierarquia completa de capitães, mestres, pilotos, escrivães, marinheiros e soldados, nem ordens régias específicas por navio. Também não modela disciplina, remuneração, propriedade das embarcações, divisão de risco entre Coroa e financiadores ou quantidades físicas de mantimentos. Esses elementos exigem documentação adicional antes de virar mecânica.
