# Dados historicos

Este diretorio contem tabelas pequenas, versionadas e legiveis que registram a base historica do projeto. Parametros de balanceamento ficam separadamente em `simulation/`.

## Convencoes

- IDs sao estaveis, curtos e sem espacos.
- Datas devem usar `YYYY-MM-DD` quando exatas ou apenas o ano quando a fonte nao permite maior precisao.
- Campos historicos e de simulacao nao devem ser misturados.
- Toda linha historicamente relevante deve possuir proveniencia minima em `source_id` ou nota equivalente.
- Valores ausentes permanecem vazios; nao usar `0` para significar desconhecido.
- Divergencias entre fontes sao preservadas em linhas distintas quando alteram um dado observavel.

## Arquivos

### `nodes.csv`
Nos maritimos e portuarios. Inclui portos, feitorias, pracas militares, colonias insulares, mercados estrangeiros e pontos nauticos.

### `goods.csv`
Bens comerciais ordinarios. Pessoas escravizadas nao entram nesta tabela.

### `node_goods.csv`
Relacoes entre nos e mercadorias, distinguindo producao, hinterland, importacao, exportacao, transito e demanda.

### `routes.csv`
Conexoes navegaveis ou historicamente relevantes, sem pressupor que sejam conhecidas pelo jogador.

### `route_goods.csv`
Fluxos de mercadorias associados a rotas.

### `voyage_observations.csv`
Observacoes documentadas de viagens usadas como ancoras de calibracao. Datas observadas sao fatos de fonte; qualquer velocidade ou parametro derivado dessas datas pertence a camada de simulacao. A primeira ancora preserva separadamente as chegadas a Calecute em 20 e 21 de maio de 1498 registradas por Prakash e Subrahmanyam.

### `pilots.csv`
Pessoas ou registros historicos de pilotos que podem ser associados a um local e periodo. O primeiro registro e o piloto guzerate fornecido pelo governante de Melinde a armada de Vasco da Gama em abril de 1498. O corpus atual nao sustenta seu nome e registra explicitamente essa incerteza.

### `pilot_routes.csv`
Competencias de piloto documentadas por rota e periodo. Esta tabela nao atribui bonus de velocidade ou consumo: apenas registra que a fonte sustenta capacidade de guia em determinada conexao.

### `expeditions.csv`
Expedicoes ou armadas historicamente documentadas. A primeira linha registra a armada de Vasco da Gama de 1497-1499, sua autoridade, lideranca e o carater misto do financiamento documentado. A tabela nao fixa a identidade do protagonista.

### `expedition_routes.csv`
Sequencia de pernas agregadas associadas a uma expedicao. `FLEET_COMMAND` registra uma base institucional de participacao na viagem; nao e conhecimento nautico individual e nao concede bonus quantitativo. As arestas continuam sendo abstracoes do grafo e nao derrotas historicas exatas.

## Campos de evidencia

`evidence_grade` usa `A`, `B`, `C` ou `D`, conforme `docs/historical-method.md`.

`evidence_scope` usa preferencialmente:

- `NODE_DIRECT`
- `REGIONAL`
- `NETWORK`
- `LATER_PERIOD_ANALOGY`

## Regra para coordenadas

Coordenadas representam uma ancora cartografica do no e nao necessariamente a posicao exata do cais no seculo XV. O campo `coordinate_confidence` registra essa incerteza. Distancias calculadas a partir dessas coordenadas sao distancias geodesicas de referencia, nao a reconstrucao automatica do caminho historico navegado.
