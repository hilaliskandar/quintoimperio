# Método de aquisição de informação v0.1

## Objetivo

Transformar conhecimento em recurso ativo do jogo sem revelar automaticamente ao personagem o que a Coroa sabe e sem criar portos, rotas ou relações comerciais inexistentes na base histórica.

A v0.1 introduz três canais:

- `RUMOR`;
- `MERCHANT_CONTACT`;
- `PILOT_CONSULTATION`.

Os dois primeiros são **mecânicas genéricas de simulação**. Eles não afirmam que uma conversa específica, com determinado conteúdo ou interlocutor, ocorreu historicamente. O terceiro só existe quando há piloto e competência de rota registrados em `pilots.csv` e `pilot_routes.csv`.

## Regra de proveniência

Uma oportunidade de informação só pode apontar para:

- uma rota já existente em `routes.csv`;
- o nó de destino dessa rota;
- e, no caso de piloto, um registro histórico de competência da própria rota.

Rotas `STRATEGIC_AGGREGATE` são excluídas. Assim, a mecânica não transforma uma conexão estratégica de alto nível em conhecimento operacional ou rumor sobre uma viagem executável.

Nenhuma rotina de aquisição consulta `KnowledgeModel.initial_for_node(..., "CROWN")` ou copia o estado institucional para o personagem. O conhecimento da Coroa permanece uma perspectiva separada.

## Parâmetros de simulação

`simulation/information_rules.csv` registra custos de tempo e níveis mínimos obtidos. Esses números são escolhas de design auditáveis, não medidas históricas.

Na v0.1:

| Canal | Tempo | Geografia | Rota | Mercado | Política |
|---|---:|---|---|---|---|
| `RUMOR` | 1 dia | até `RUMORED` | até `RUMORED` | sem efeito | sem efeito |
| `MERCHANT_CONTACT` | 1 dia | até `PARTIAL` | até `RUMORED` | até `PARTIAL` | até `RUMORED` |
| `PILOT_CONSULTATION` | 1 dia | até `PARTIAL` | até `PARTIAL` | sem efeito | sem efeito |

“Até” significa mínimo alcançável: a ação nunca reduz conhecimento já superior.

`RUMOR` e `MERCHANT_CONTACT` não tornam uma rota `OPERATIONAL`. `PILOT_CONSULTATION` também para em `PARTIAL`: conversar com um piloto não equivale a adquirir experiência autônoma da rota. A capacidade efetiva de viajar com piloto continua sendo tratada separadamente por `TravelModel`.

## Disponibilidade dos canais

### RUMOR

Pode ocorrer em qualquer nó que não seja `NAVIGATION_POINT` puro e que possua rota documentada de saída capaz de acrescentar algum conhecimento.

Isso permite rumor durante um ancoradouro histórico sem transformar o ancoradouro em mercado. A interação pode representar conversa com tripulantes ou contatos costeiros e continua explicitamente classificada como simulação.

### MERCHANT_CONTACT

Exige `broker_availability` classificado como `LOW`, `MEDIUM` ou `HIGH` no nó atual. Campo vazio, `UNKNOWN` ou `NONE` não é interpretado como disponibilidade.

O contato pode melhorar informação geográfica/comercial, mas não confere conhecimento náutico operacional.

### PILOT_CONSULTATION

Exige simultaneamente:

- piloto historicamente registrado no nó e período;
- competência `CONFIRMED` para a rota específica.

Na base atual, o primeiro caso é o piloto guzerate de Melinde em 1498 para `R_MAL_CAL`.

## Seleção e repetição

Cada oportunidade possui ID estável por canal, origem e rota, acrescido de piloto quando aplicável. Uma oportunidade só pode ser usada uma vez por sessão.

Quando existem vários alvos possíveis, a escolha é determinística para a mesma combinação de estado temporal, nó, canal e semente. A semente serve à reprodutibilidade do protótipo; não representa aleatoriedade histórica mensurável.

A interface não mostra o alvo oculto antes da ação. Ela mostra apenas se o canal está disponível; o nó/rota revelado aparece na mensagem depois da interação.

## Relação com o calendário

Toda interação v0.1 custa um dia de jogo. O relógio é o mesmo de viagem, serviços e permanências.

Por isso uma interação executada durante uma escala `GUIDED` consome parte do intervalo até a partida documentada. Ela não concede nenhum efeito material adicional. Se as decisões do jogador o levarem a ultrapassar a cronologia histórica, as regras de `ChronologyMode` continuam responsáveis pela passagem para trajetória contrafactual.

## Limitações

A v0.1 não modela ainda:

- cartas persistentes ou mensagens transportadas entre portos;
- qualidade individual de informantes;
- idioma, tradução e mal-entendidos;
- pagamento por informação;
- espionagem;
- desinformação deliberada;
- redes pessoais de confiança;
- memória com validade temporal ou obsolescência de preços.

Esses sistemas só devem ser introduzidos depois que o loop básico mostrar que informação produz decisões interessantes sem simplesmente substituir exploração e experiência.
