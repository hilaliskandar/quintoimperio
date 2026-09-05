# Método comercial v0.1

## Objetivo

Ligar a economia relativa já existente a um estado comercial do jogador sem introduzir preços, moedas, pesos ou volumes apresentados como históricos.

## Estado comercial

`CommercialState` registra três elementos:

- `capital_index`: unidade contábil abstrata de simulação;
- `capacity_total`: capacidade abstrata total da embarcação;
- `cargo`: quantidades abstratas por mercadoria.

O estado é imutável: cada operação produz um novo estado e preserva o anterior para testes e auditoria.

## Capacidade

Cada unidade de mercadoria consome capacidade segundo `bulk_index` em `simulation/goods_params.csv`. Esse índice é uma hipótese de balanceamento ordinal e não equivale a tonelada, tonel, quintal, volume de porão ou qualquer unidade histórica.

## Mercados elegíveis

Uma compra ou venda só é possível quando `EconomyModel.market_quote()` encontra uma relação ativa em `data/node_goods.csv` para o porto, mercadoria e ano. Ausência de linha não é convertida em disponibilidade presumida.

Exemplo: a primeira base documenta pimenta em Calecute e Aden, mas não em Lisboa. Portanto a v0.1 permite operar pimenta em Calecute/Aden e bloqueia uma compra de pimenta em Lisboa enquanto não houver uma relação histórica documentada correspondente.

## Preço relativo

O índice de mercado vem de `EconomyModel`. `simulation/trade_rules.csv` aplica um pequeno spread de compra e venda para impedir arbitragem imediata no mesmo porto:

- compra: `market_price_index * BUY_MULTIPLIER`;
- venda: `market_price_index * SELL_MULTIPLIER`.

Esses multiplicadores são puramente de simulação. Não representam margem mercantil, imposto, comissão ou costume histórico.

## Bloqueios

A compra é bloqueada quando:

- quantidade não é positiva;
- a mercadoria não está documentada no mercado;
- não há capacidade abstrata suficiente;
- não há capital abstrato suficiente.

A venda é bloqueada quando:

- quantidade não é positiva;
- a mercadoria não está documentada no mercado de destino;
- o inventário não contém a quantidade solicitada.

## Próximas extensões

A v0.1 ainda não modela:

- crédito;
- commenda;
- moeda por região;
- custos de corretagem específicos;
- impostos históricos;
- lotes com preço médio de aquisição;
- deterioração por viagem;
- contratos;
- restrições por comunidade mercantil ou reputação.

Essas camadas só devem ser acrescentadas depois que o ciclo mínimo `porto → compra → viagem → venda` estiver funcional e testado.
