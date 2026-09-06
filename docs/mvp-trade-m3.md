# Comércio operacional do MVP — gate M3

## Objetivo

O gate M3 transforma o comércio já implementado no domínio em uma decisão utilizável pela interface da campanha. Não altera a base histórica, não introduz moeda histórica e não amplia a geografia ou a cesta documental de mercadorias.

## Implementação

A interface `prototype/game_m3.py` estende a interface v0.1 e mantém `GameSessionModel` e `TradeModel` como fontes exclusivas das regras comerciais.

Foram acrescentados:

- quantidade comercial selecionável entre 1 e 20 unidades abstratas de simulação;
- compra e venda usando a quantidade selecionada;
- indicação de carga usada, capacidade total e capacidade livre;
- indicação da quantidade em posse da mercadoria selecionada;
- mensagens legíveis para bloqueios de acesso, restrição de mercadoria, capital, capacidade, inventário e quantidade inválida;
- atualização visual dos botões de compra e venda para a quantidade corrente.

## Limites metodológicos

`capital_index`, `unit_price_index`, `bulk_index`, capacidade e quantidade continuam parâmetros abstratos da simulação. Não correspondem a cruzados, xerafins, quintais, toneladas ou outra unidade histórica.

A existência de uma mercadoria no mercado continua dependendo exclusivamente de `data/node_goods.csv`. Restrições específicas registradas nessa tabela permanecem independentes do acesso portuário genérico.

O gate não introduz:

- crédito ou *commenda*;
- câmbio ou juros;
- moeda histórica;
- estoque dinâmico;
- impacto marginal da quantidade sobre preços;
- novos mercados ou mercadorias;
- descontos ou crédito derivados de relações.

## Validação

`tests/test_interface_trade_m3.py` cobre seleção e limites de quantidade, execução de compra/venda com quantidade variável, redução de capacidade livre, inventário, tradução de bloqueios e presença dos controles no render headless.

A campanha histórica continua sendo validada pelos testes existentes de Lisboa a Calecute. A integração M3 deve preservar a separação entre conhecimento do mercado, acesso institucional e relações com atores.
