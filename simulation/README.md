# Parâmetros de simulação

Este diretório contém **parâmetros de balanceamento**, não dados históricos.

Os arquivos em `data/` registram evidência histórica e inferências explicitamente marcadas. Os arquivos em `simulation/` traduzem essa estrutura em índices e regras para testar economia, navegação, conhecimento, viagem, serviços portuários, comércio e aprendizagem da sessão. Nenhum número deste diretório deve ser citado como preço, produção, alíquota, frete, velocidade, consumo, desgaste, capacidade portuária, margem comercial ou probabilidade histórica.

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

Capital, capacidade de carga e quantidades comerciais também são índices abstratos na v0.1. Não equivalem a cruzados, xerafins, toneladas, tonéis, quintais ou outras unidades históricas.

## Arquivos

- `goods_params.csv`: volume relativo, valor-base, importância estratégica, perecibilidade e função de troca por mercadoria.
- `rules.csv`: regras econômicas para papel comercial, origem do estoque, regime de acesso, tipo de rota e dependência de monção.
- `navigation_rules.csv`: parâmetros mínimos para converter distância geodésica e observações históricas de viagem em duração relativa. A v0.1 só aplica uma penalidade explícita de junho/julho; não inventa perfis direcionais de vento para rotas ainda não documentadas.
- `knowledge_rules.csv`: mapeamento entre os estados textuais documentados em `nodes.csv` e quatro dimensões de conhecimento do personagem/Coroa.
- `route_knowledge_rules.csv`: conversão separada dos estados textuais de `routes.csv` em conhecimento náutico de cada rota. Conhecer um nó não habilita automaticamente suas conexões.
- `session_rules.csv`: níveis mínimos de conhecimento adquiridos após chegar fisicamente a um porto e após completar uma rota. São regras de jogabilidade, não medições históricas.
- `travel_rules.csv`: consumo em dias-equivalentes, desgaste abstrato por tipo de rota e condição mínima de partida. Esses valores existem somente para fazer o primeiro loop de viagem funcionar e permanecem separados da evidência histórica.
- `port_rules.csv`: capacidades abstratas de reabastecimento, taxas abstratas de reparo, duração do serviço e limite provisório de provisões embarcadas. As categorias `LOW`, `MEDIUM` e `HIGH` vêm da base histórica; os valores numéricos que as tornam jogáveis pertencem apenas à simulação.
- `trade_rules.csv`: multiplicadores abstratos de compra e venda usados para criar um spread mínimo de simulação. Não representam margens, impostos, comissão ou prática mercantil histórica.

## Princípio

A simulação deve reproduzir **ordens e relações plausíveis** antes de buscar números finais. Exemplo: um estoque de trânsito em Moçambique deve ser mais volátil que uma oferta sustentada pelo hinterland do Malabar; isso não significa que conhecemos a variância histórica de ambos.

Da mesma forma, a taxa diária derivada da viagem Melinde–Calecute serve apenas para calibrar a primeira ordem de grandeza da duração. Ela não é tratada como velocidade universal das embarcações do século XV.

Pilotos documentados não recebem automaticamente bônus numéricos. Na v0.1, um piloto habilita uma rota quando seu conhecimento específico está documentado; efeitos sobre velocidade, segurança, consumo ou desgaste só serão acrescentados com justificativa histórica ou marcados explicitamente como hipótese de balanceamento.

Nos serviços portuários, campo histórico vazio continua `UNKNOWN`: a simulação não o converte em `LOW` e tampouco em `NONE`. Um serviço desconhecido permanece bloqueado até que a base histórica seja refinada.

No comércio, ausência de uma relação porto–mercadoria em `data/node_goods.csv` permanece ausência de mercado no protótipo. O modelo não cria oferta ou demanda apenas para tornar uma rota jogável.

Na sessão, presença física e experiência produzem aprendizado segundo regras explícitas. O protótipo não transforma automaticamente informação indireta em domínio náutico ou comercial; a passagem entre níveis ocorre por chegada, viagem ou por um cenário técnico explicitamente marcado como tal.
