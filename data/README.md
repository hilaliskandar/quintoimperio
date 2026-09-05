# Dados históricos

Este diretório contém tabelas pequenas, versionadas e legíveis que registram a base histórica do projeto. Parâmetros de balanceamento ficam separadamente em `simulation/`.

## Convenções

- IDs são estáveis, curtos e sem espaços.
- Datas devem usar `YYYY-MM-DD` quando exatas ou apenas o ano quando a fonte não permite maior precisão.
- Campos históricos e de simulação não devem ser misturados.
- Toda linha historicamente relevante deve possuir proveniência mínima em `source_id` ou nota equivalente.
- Valores ausentes permanecem vazios; não usar `0` para significar desconhecido.
- Divergências entre fontes são preservadas em linhas distintas quando alteram um dado observável.

## Arquivos

### `nodes.csv`
Nós marítimos e portuários. Inclui portos, feitorias, praças militares, colônias insulares, mercados estrangeiros e pontos náuticos.

### `goods.csv`
Bens comerciais ordinários. Pessoas escravizadas não entram nesta tabela.

### `node_goods.csv`
Relações entre nós e mercadorias, distinguindo produção, hinterland, importação, exportação, trânsito e demanda.

### `routes.csv`
Conexões navegáveis ou historicamente relevantes, sem pressupor que sejam conhecidas pelo jogador.

### `route_goods.csv`
Fluxos de mercadorias associados a rotas.

### `voyage_observations.csv`
Observações documentadas de viagens usadas como âncoras de calibração. Datas observadas são fatos de fonte; qualquer velocidade ou parâmetro derivado dessas datas pertence à camada de simulação. A primeira âncora preserva separadamente as chegadas a Calecute em 20 e 21 de maio de 1498 registradas por Prakash e Subrahmanyam.

## Campos de evidência

`evidence_grade` usa `A`, `B`, `C` ou `D`, conforme `docs/historical-method.md`.

`evidence_scope` usa preferencialmente:

- `NODE_DIRECT`
- `REGIONAL`
- `NETWORK`
- `LATER_PERIOD_ANALOGY`

## Regra para coordenadas

Coordenadas representam uma âncora cartográfica do nó e não necessariamente a posição exata do cais no século XV. O campo `coordinate_confidence` registra essa incerteza. Distâncias calculadas a partir dessas coordenadas são distâncias geodésicas de referência, não a reconstrução automática do caminho histórico navegado.
