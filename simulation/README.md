# Parâmetros de simulação

Este diretório contém **parâmetros de balanceamento**, não dados históricos.

Os arquivos em `data/` registram evidência histórica e inferências explicitamente marcadas. Os arquivos em `simulation/` traduzem essa estrutura em índices ordinais para testar comportamento econômico. Nenhum número deste diretório deve ser citado como preço, produção, alíquota, frete ou probabilidade histórica.

## Escalas

A versão `v0.1` usa principalmente escalas ordinais de 1 a 5:

- `1` — muito baixo;
- `2` — baixo;
- `3` — médio;
- `4` — alto;
- `5` — muito alto.

A volatilidade usa frações entre `0` e `1`. Os valores são hipóteses de modelagem e podem ser recalibrados.

## Arquivos

- `goods_params.csv`: volume relativo, valor-base, importância estratégica, perecibilidade e função de troca por mercadoria.
- `rules.csv`: regras que convertem papel comercial, origem do estoque, regime de acesso, tipo de rota e dependência de monção em índices da simulação.

## Princípio

A simulação deve reproduzir **ordens e relações plausíveis** antes de buscar números finais. Exemplo: um estoque de trânsito em Moçambique deve ser mais volátil que uma oferta sustentada pelo hinterland do Malabar; isso não significa que conhecemos a variância histórica de ambos.
