# Dados históricos e de simulação

Este diretório contém tabelas pequenas, versionadas e legíveis, destinadas a alimentar o protótipo.

## Convenções

- IDs são estáveis, curtos e sem espaços.
- Datas devem usar `YYYY-MM-DD` quando exatas ou apenas o ano quando a fonte não permite maior precisão.
- Campos históricos e de simulação não devem ser misturados.
- Toda linha historicamente relevante deve possuir proveniência mínima em `source_id` ou nota equivalente.
- Valores ausentes permanecem vazios; não usar `0` para significar desconhecido.

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

## Campos de evidência

`evidence_grade` usa `A`, `B`, `C` ou `D`, conforme `docs/historical-method.md`.

`evidence_scope` usa preferencialmente:

- `NODE_DIRECT`
- `REGIONAL`
- `NETWORK`
- `LATER_PERIOD_ANALOGY`

## Regra para coordenadas

Coordenadas representam uma âncora cartográfica do nó e não necessariamente a posição exata do cais no século XV. O campo `coordinate_confidence` registra essa incerteza.
