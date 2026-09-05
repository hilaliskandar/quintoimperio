# Parâmetros de simulação

Este diretório contém **parâmetros de balanceamento**, não dados históricos.

Os arquivos em `data/` registram evidência histórica e inferências explicitamente marcadas. Os arquivos em `simulation/` traduzem essa estrutura em índices e regras para testar economia, navegação, conhecimento, informação, acesso institucional, viagem, eventos marítimos, serviços portuários, comércio e aprendizagem da sessão. Nenhum número deste diretório deve ser citado como preço, produção, alíquota, frete, velocidade, consumo, desgaste, capacidade portuária, margem comercial, probabilidade histórica, frequência histórica de avarias, duração histórica de uma conversa ou duração histórica de uma negociação.

## Escalas

A versão `v0.1` usa principalmente escalas ordinais de 1 a 5 para a economia. A volatilidade usa frações entre `0` e `1`. Os valores são hipóteses de modelagem e podem ser recalibrados.

Para conhecimento, os índices `0..4` significam intensidade crescente: desconhecido, rumor, parcial, operacional e confirmado. Eles não são porcentagens de conhecimento.

A condição do navio usa uma escala abstrata `0..100`. Provisões são expressas em **dias-equivalentes de viagem**, sem conversão para rações, barris, peso ou volume histórico enquanto o corpus não sustentar essas relações.

Capital, capacidade de carga e quantidades comerciais também são índices abstratos na v0.1. Não equivalem a cruzados, xerafins, toneladas, tonéis, quintais ou outras unidades históricas.

## Arquivos

- `goods_params.csv`: volume relativo, valor-base, importância estratégica, perecibilidade e função de troca por mercadoria.
- `rules.csv`: regras econômicas para papel comercial, origem do estoque, regime de acesso, tipo de rota e dependência de monção.
- `navigation_rules.csv`: parâmetros mínimos para converter distância geodésica e observações históricas de viagem em duração relativa. A v0.1 só aplica uma penalidade explícita de junho/julho; não inventa perfis direcionais de vento para rotas ainda não documentadas.
- `knowledge_rules.csv`: mapeamento entre os estados textuais documentados em `nodes.csv` e quatro dimensões de conhecimento do personagem/Coroa.
- `route_knowledge_rules.csv`: conversão separada dos estados textuais de `routes.csv` em conhecimento náutico de cada rota. Conhecer um nó não habilita automaticamente suas conexões.
- `information_rules.csv`: custos de tempo e limites mínimos dos canais `RUMOR`, `MERCHANT_CONTACT` e `PILOT_CONSULTATION`. São escolhas de jogabilidade e não registros de conversas históricas.
- `access_rules.csv`: tradução dos `access_regime` de `nodes.csv` em `OPEN`, `NEGOTIATION_REQUIRED`, `RESTRICTED` ou `NONCOMMERCIAL`, além do tempo abstrato de negociação. Não define impostos, valor de presentes ou protocolo diplomático histórico.
- `session_rules.csv`: níveis mínimos de conhecimento adquiridos após chegar fisicamente a um porto e após completar uma rota. São regras de jogabilidade, não medições históricas.
- `travel_rules.csv`: consumo em dias-equivalentes, desgaste abstrato por tipo de rota e condição mínima de partida. Esses valores existem somente para fazer o primeiro loop de viagem funcionar e permanecem separados da evidência histórica.
- `voyage_event_rules.csv`: probabilidades e limites de efeitos para calmaria, mau tempo, avaria menor de aparelho e perturbação de junho/julho. Todos os eventos são hipóteses `SIMULATION`, não incidentes históricos documentados.
- `port_rules.csv`: capacidades abstratas de reabastecimento, taxas abstratas de reparo, duração do serviço e limite provisório de provisões embarcadas. As categorias `LOW`, `MEDIUM` e `HIGH` vêm da base histórica; os valores numéricos que as tornam jogáveis pertencem apenas à simulação.
- `trade_rules.csv`: multiplicadores abstratos de compra e venda usados para criar um spread mínimo de simulação. Não representam margens, impostos, comissão ou prática mercantil histórica.

## Princípio

A simulação deve reproduzir **ordens e relações plausíveis** antes de buscar números finais. Exemplo: um estoque de trânsito em Moçambique deve ser mais volátil que uma oferta sustentada pelo hinterland do Malabar; isso não significa que conhecemos a variância histórica de ambos.

Da mesma forma, a taxa diária derivada da viagem Melinde–Calecute serve apenas para calibrar a primeira ordem de grandeza da duração. Ela não é tratada como velocidade universal das embarcações do século XV.

Pilotos documentados não recebem automaticamente bônus numéricos. Na v0.1, um piloto pode habilitar uma rota quando seu conhecimento específico está documentado; efeitos sobre velocidade, segurança, consumo ou desgaste só serão acrescentados com justificativa histórica ou marcados explicitamente como hipótese de balanceamento. Uma consulta a piloto melhora conhecimento da rota apenas até `PARTIAL`: conversar com o especialista não equivale a dominar autonomamente a navegação.

Nos serviços portuários, campo histórico vazio continua `UNKNOWN`: a simulação não o converte em `LOW` e tampouco em `NONE`. Um serviço desconhecido permanece bloqueado até que a base histórica seja refinada.

No comércio, ausência de uma relação porto–mercadoria em `data/node_goods.csv` permanece ausência de mercado no protótipo. O modelo não cria oferta ou demanda apenas para tornar uma rota jogável. Além disso, `restricted=TRUE` é agora um bloqueio próprio do `TradeModel`: uma autorização portuária genérica não torna um bem historicamente restrito uma mercadoria ordinária.

Na aquisição de informação, oportunidades só apontam para nós e rotas já documentados. `RUMOR` não ultrapassa `RUMORED`, contato mercantil não produz navegação operacional e `PILOT_CONSULTATION` não ultrapassa `PARTIAL`. O estado de conhecimento da Coroa nunca é copiado silenciosamente para o personagem. Uma interação custa um dia de simulação na v0.1 e pode consumir parte de uma permanência histórica, mas não concede recursos materiais.

No acesso institucional, `FOREIGN_NEGOTIATED` exige uma ação explícita antes da compra/venda. O custo de um dia é apenas uma regra de loop; não representa uma audiência de duração conhecida. A v0.1 não cobra taxas, não avalia presentes, não atribui probabilidade de êxito diplomático e não converte monopólio régio em acesso comum. Ancoradouros e marcos náuticos continuam não comerciais.

Nos eventos marítimos, probabilidades e intensidades pertencem inteiramente à simulação. Uma observação histórica exata de rota e data pode suprimir a camada aleatória quando o plano deve preservar a cronologia documentada. Fora desse caso, o sistema seleciona no máximo um evento por viagem e limita seus efeitos a dias adicionais, provisões correspondentes e condição abstrata. Nenhum evento genérico implica morte, perda de carga, combate ou naufrágio.

Na sessão, presença física e experiência produzem aprendizado segundo regras explícitas. O protótipo não transforma automaticamente informação indireta em domínio náutico ou comercial; a passagem entre níveis ocorre por chegada, viagem, interação ativa ou por um cenário técnico explicitamente marcado como tal. Conhecer um mercado também não equivale a possuir autorização institucional para comerciar nele.
