# Parâmetros de simulação

Este diretório contém **parâmetros de balanceamento**, não dados históricos.

Os arquivos em `data/` registram evidência histórica e inferências explicitamente marcadas. Os arquivos em `simulation/` traduzem essa estrutura em índices e regras para testar economia, navegação, conhecimento e viagem. Nenhum número deste diretório deve ser citado como preço, produção, alíquota, frete, velocidade, consumo, desgaste ou probabilidade histórica.

## Escalas

A versão `v0.1` usa principalmente escalas ordinais de 1 a 5:

- `1` — muito baixo;
- `2` — baixo;
- `3` — médio;
- `4` — alto;
- `5` — muito alto.

A volatilidade usa frações entre `0` e `1`. Os valores são hipóteses de modelagem e podem ser recalibrados.

Para conhecimento, os índices `0..4` significam intensidade crescente: desconhecido, rumor, parcial, operacional e confirmado. Eles não são porcentagens de conhecimento.

A condição do navio usa uma escala abstrata `0..100`. Provisões são expressas em **dias-equivalentes de viagem**, sem conversão para rações, barris, peso ou volume histórico enquanto o corpus não sustentar essas relações.

## Arquivos

- `goods_params.csv`: volume relativo, valor-base, importância estratégica, perecibilidade e função de troca por mercadoria.
- `rules.csv`: regras econômicas para papel comercial, origem do estoque, regime de acesso, tipo de rota e dependência de monção.
- `navigation_rules.csv`: parâmetros mínimos para converter distância geodésica e observações históricas de viagem em duração relativa. A v0.1 só aplica uma penalidade explícita de junho/julho; não inventa perfis direcionais de vento para rotas ainda não documentadas.
- `knowledge_rules.csv`: mapeamento entre os estados textuais documentados em `nodes.csv` e quatro dimensões de conhecimento do personagem/Coroa.
- `travel_rules.csv`: consumo em dias-equivalentes, desgaste abstrato por tipo de rota e condição mínima de partida. Esses valores existem somente para fazer o primeiro loop de viagem funcionar e permanecem separados da evidência histórica.

## Princípio

A simulação deve reproduzir **ordens e relações plausíveis** antes de buscar números finais. Exemplo: um estoque de trânsito em Moçambique deve ser mais volátil que uma oferta sustentada pelo hinterland do Malabar; isso não significa que conhecemos a variância histórica de ambos.

Da mesma forma, a taxa diária derivada da viagem Melinde–Calecute serve apenas para calibrar a primeira ordem de grandeza da duração. Ela não é tratada como velocidade universal das embarcações do século XV.

Pilotos documentados não recebem automaticamente bônus numéricos. Na v0.1, um piloto habilita uma rota quando seu conhecimento específico está documentado; efeitos sobre velocidade, segurança, consumo ou desgaste só serão acrescentados com justificativa histórica ou marcados explicitamente como hipótese de balanceamento.
