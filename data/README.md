# Dados historicos

Este diretorio contem tabelas pequenas, versionadas e legiveis que registram a base historica do projeto. Parametros de balanceamento ficam separadamente em `simulation/`.

## Convencoes

- IDs sao estaveis, curtos e sem espacos.
- Datas devem usar `YYYY-MM-DD` quando exatas ou apenas o ano quando a fonte nao permite maior precisao.
- Campos historicos e de simulacao nao devem ser misturados.
- Toda linha historicamente relevante deve possuir proveniencia minima em `source_id` ou nota equivalente.
- Valores ausentes permanecem vazios; nao usar `0` para significar desconhecido.
- Divergencias entre fontes sao preservadas em linhas distintas quando alteram um dado observavel.
- Datas reconstruidas editorialmente em fontes primarias devem ser identificadas nas notas em vez de promovidas silenciosamente a certeza documental equivalente.
- Atores e comunidades nao sao criados para preencher lacunas de jogabilidade: so entram nas tabelas quando o corpus permite identifica-los em no, papel e periodo adequados.

## Arquivos

### `nodes.csv`
Nos maritimos e portuarios. Inclui portos, feitorias, pracas militares, colonias insulares, mercados estrangeiros, ancoradouros logisticos e pontos nauticos. Um ancoradouro documentado nao se transforma automaticamente em mercado.

### `goods.csv`
Bens comerciais ordinarios. Pessoas escravizadas nao entram nesta tabela.

### `node_goods.csv`
Relacoes entre nos e mercadorias, distinguindo producao, hinterland, importacao, exportacao, transito e demanda. `restricted=TRUE` registra uma restricao especifica que nao e anulada por acesso portuario generico.

### `actors.csv`
Atores institucionais ou comunidades historicamente identificaveis que podem participar de relacoes com o personagem. O primeiro recorte normaliza a autoridade do Samudri Raja e os mercadores muculmanos/pardesi de Calecute, alem da autoridade local de Melinde em 1498. Um ator agregado nao deve ser interpretado como bloco politico homogeneo.

### `node_actors.csv`
Associacoes temporais entre atores, nos e papeis como `AUTHORITY` e `MERCHANT_COMMUNITY`. A ausencia de linha e uma lacuna de dados, nao autorizacao para criar um ator generico em tempo de execucao.

### `routes.csv`
Conexoes navegaveis ou historicamente relevantes, sem pressupor que sejam conhecidas pelo jogador. Rotas com `route_origin=STRATEGIC_AGGREGATE` existem apenas para leitura de rede em escala ampla e nao devem ser executadas como uma unica perna quando ha itinerario historico segmentado.

### `route_goods.csv`
Fluxos de mercadorias associados a rotas.

### `voyage_observations.csv`
Observacoes documentadas de viagens usadas como ancoras de calibracao. Datas observadas sao fatos de fonte; qualquer velocidade ou parametro derivado pertence a camada de simulacao. A base preserva as duas chegadas divergentes a Calecute em 20 e 21 de maio de 1498 registradas por Prakash e Subrahmanyam e mantem a observacao agregada Lisboa-Cabo de Subrahmanyam para comparacao historiografica. O itinerario de Gama passa a ter observacoes segmentadas desde Lisboa ate Melinde com base no `Roteiro`; datas colocadas entre colchetes na edicao Ravenstein sao marcadas como reconstrucoes editoriais. Observacao da mesma rota e data de partida tem precedencia sobre extrapolacao geodesica no prototipo.

### `pilots.csv`
Pessoas ou registros historicos de pilotos que podem ser associados a um local e periodo. O primeiro registro e o piloto guzerate fornecido pelo governante de Melinde a armada de Vasco da Gama em abril de 1498. O corpus atual nao sustenta seu nome e registra explicitamente essa incerteza.

### `pilot_routes.csv`
Competencias de piloto documentadas por rota e periodo. Esta tabela nao atribui bonus de velocidade ou consumo: apenas registra que a fonte sustenta capacidade de guia em determinada conexao.

### `expeditions.csv`
Expedicoes ou armadas historicamente documentadas. A primeira linha registra a armada de Vasco da Gama de 1497-1499, sua autoridade, lideranca e o carater misto do financiamento documentado. P3 acrescenta as armadas de Cabral, Joao da Nova e Vasco da Gama 1502 como unidades documentais; a existencia de uma linha nao implica que toda a campanha ja esteja jogavel. A tabela nao fixa a identidade do protagonista.

### `expedition_routes.csv`
Sequencia de pernas operacionais associadas a uma expedicao. `FLEET_COMMAND` registra uma base institucional de participacao na viagem; nao e conhecimento nautico individual e nao concede bonus quantitativo. Para a armada de 1497, as antigas pernas agregadas Lisboa-Cabo e Cabo-Mocambique foram substituidas por escalas documentadas no `Roteiro`. P3 amplia a tabela de forma incremental, apenas quando uma perna entra efetivamente no recorte executavel.

### `expedition_stops.csv`
Permanencias documentadas da expedicao em pontos de escala. Registra duracao declarada, atividades como agua, madeira, carenagem, reparos e transferencia de carga, e proveniencia. A duracao declarada pela fonte nao precisa coincidir aritmeticamente com datas editoriais reconstruidas quando a propria fonte usa contagem inclusiva.

### `expedition_epilogue_events.csv`
Eventos historicos de fechamento cuja evidencia nao cabe com seguranca numa unica sequencia de pernas operacionais. A tabela foi introduzida para o trecho posterior ao fim do manuscrito do `Roteiro`, quando as embarcacoes se separam, o comando do S. Gabriel muda e a trajetoria pessoal de Vasco da Gama deixa de coincidir com a do navio. `trajectory_id` separa linhas narrativas sem criar ainda um sistema geral de personagens ou frota. `date_precision` admite `EXACT`, `BEFORE`, `AFTER` e `RANGE`; datas concorrentes usam linhas distintas no mesmo `variant_group`. `preferred_for_simulation` so pode selecionar uma variante quando existe uma escolha editorial de trabalho defensavel; quando a divergencia permanece irresolvida, todas as variantes ficam `FALSE`. A tabela e historica/documental e nao e consumida ainda pelo loop jogavel.

### `expedition_events.csv`
Eventos historicos reutilizaveis durante uma campanha, e nao apenas em seu epilogo. P3 usa esta camada para perdas e separacoes de embarcacoes, destacamentos, aquisicao de informacao e mudancas institucionais. Os eventos podem ser consultados pelo dominio, mas nao produzem automaticamente efeitos materiais, combate ou alteracoes de frota. `preferred_for_simulation` indica apenas que a variante documental pode servir de referencia de trabalho quando a evidencia permite.

### `node_state_events.csv`
Transicoes temporais documentadas de um no. A tabela existe para impedir que uma feitoria, fortificacao, guarnicao, crise de acesso ou mudanca relacional seja retroprojetada para todo o periodo coberto por `nodes.csv`. O modelo aplica intervalos incertos de forma conservadora: uma transicao so integra o estado efetivo quando a data consultada alcanca o limite superior documentado. Fortificacao ou guarnicao portuguesa nao implica mudanca de soberania, que permanece explicitada em `sovereignty_note`.

## Campos de evidencia

`evidence_grade` usa `A`, `B`, `C` ou `D`, conforme `docs/historical-method.md`.

`evidence_scope` usa preferencialmente:

- `NODE_DIRECT`
- `REGIONAL`
- `NETWORK`
- `LATER_PERIOD_ANALOGY`
- `EDITORIAL_SYNTHESIS` para continuacoes editoriais explicitamente posteriores ao corpo da fonte primaria.

## Regra para coordenadas

Coordenadas representam uma ancora cartografica do no e nao necessariamente a posicao exata do cais no seculo XV. O campo `coordinate_confidence` registra essa incerteza. Distancias calculadas a partir dessas coordenadas sao distancias geodesicas de referencia, nao a reconstrucao automatica do caminho historico navegado.
