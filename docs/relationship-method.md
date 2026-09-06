# Método de relações por atores v0.2

## Objetivo

Evitar uma reputação global abstrata e modelar apenas relações com atores historicamente identificáveis. `data/actors.csv` registra atores/comunidades sustentados pelo corpus; `data/node_actors.csv` associa cada ator a um nó, papel e período. `RelationshipModel` consulta essas associações e nunca fabrica uma autoridade ou comunidade mercantil para preencher lacunas de jogabilidade.

A v0.2 acrescenta ao registro de contato uma consequência local mínima necessária ao MVP, sem transformar relação em pontuação, desconto, crédito ou bônus genérico.

## Primeiro recorte histórico

A base contém três atores:

- a autoridade institucional do Samudri Raja de Calecute;
- os mercadores muçulmanos/pardesi de Calecute como comunidade mercantil agregada;
- a autoridade local de Melinde em 1498, que Subrahmanyam registra como responsável por enviar o piloto guzerate à armada.

Alpers sustenta, para Calecute, o patronato do Samudri Raja sobre mercadores muçulmanos e a presença destes em funções portuárias e estruturas comunitárias próprias. Prakash permite distinguir, no começo da presença portuguesa, a relação com o Samudri da relação com os mercadores pardesi. Por isso os dois não são comprimidos em uma única “facção de Calecute”.

A comunidade mercantil de Calecute é deliberadamente agregada apenas no nível que o corpus atual sustenta. Ela não significa que todos os mercadores muçulmanos/pardesi tinham interesses, posições políticas ou estratégias idênticos.

## Estados relacionais

A v0.2 continua definindo somente:

- `UNESTABLISHED`: nenhuma interação explícita do personagem com aquele ator foi registrada pelo loop;
- `CONTACTED`: ocorreu uma interação explícita que pode ser associada àquele ator.

Não se acrescenta `COOPERATIVE`, confiança, hostilidade ou reputação porque nenhum desses estados é necessário para o efeito mínimo deste gate. Os valores internos do `IntEnum` são apenas implementação, não pontos de reputação.

## Contato explícito com autoridade

`RelationshipSessionModel.contact_authority()` cria uma ação relacional própria para a autoridade documentada do nó/período atual. Quando não há `AUTHORITY` normalizada, a ação é bloqueada por `NO_DOCUMENTED_AUTHORITY_ACTOR` e nenhum ator genérico é criado.

O contato consome um dia segundo `simulation/relationship_rules.csv`. Esse número é parâmetro de jogo e não duração histórica de audiência, negociação ou cerimônia.

A ação altera somente:

- o estado daquele ator para `CONTACTED`;
- o `GameClock` pelo custo temporal de simulação.

Ela não altera acesso ao porto, conhecimento, preços, capital, carga, provisões, condição do navio, informação ou eventos.

A negociação de acesso existente continua sendo uma ação institucional separada. Assim, contatar a autoridade de Melinde não equivale a obter autorização comercial, e negociar acesso não é redefinido como diplomacia histórica detalhada.

## Consequência local em Melinde

A única consequência relacional nova da v0.2 é a atribuição do piloto guzerate ao personagem.

`data/pilots.csv` registra que o piloto foi enviado pelo governante de Melinde. `simulation/relationship_rules.csv` traduz esse vínculo em uma regra de jogabilidade: `PIL_MAL_GUJ_1498` só é recomendado/atribuído ao personagem depois que `ACT_MAL_RULER_1498` está em `CONTACTED`.

Essa regra não apaga a disponibilidade histórica do piloto para a armada. `TravelModel.pilot_can_guide()` continua respondendo à evidência histórica de período, nó e rota. A nova camada distingue duas perguntas:

1. o piloto historicamente podia guiar aquela rota naquele momento?
2. o personagem estabeleceu a relação necessária para que o piloto seja atribuído à sua camada pessoal de navegação?

Sem o contato, a participação na armada pode continuar oferecendo `FLEET_COMMAND`; isso permanece um estado institucional separado e não converte o piloto em conhecimento pessoal. Depois do contato, `HistoricalCampaignModel.recommended_pilot_id()` pode selecionar o piloto e a perna Melinde–Calecute passa a registrar `NavigationBasis.PILOT` para o personagem.

O piloto não recebe bônus quantitativo de velocidade, segurança, consumo, desgaste ou êxito.

## Separação entre sistemas

Relação com ator permanece distinta de:

- conhecimento geográfico, náutico, comercial ou político;
- acesso institucional ao porto;
- participação em armada;
- disponibilidade histórica de piloto;
- preço ou disponibilidade de mercadoria;
- capital, crédito e capacidade de carga.

Uma ação `MERCHANT_CONTACT` em Calecute continua registrando contato com a comunidade mercantil documentada quando aplicável. `RUMOR` não cria esse contato. A negociação de acesso continua podendo registrar contato com autoridade quando a interação pode ser associada de modo não ambíguo, mas o novo `contact_authority()` permite estabelecer a relação sem confundir isso com acesso comercial.

## Política contra atores inventados

`RelationshipModel.actor_for_role()` retorna `None` quando a base não possui ator para o nó/papel/período. Isso é intencional. `broker_availability=HIGH`, por exemplo, não autoriza criar silenciosamente uma comunidade histórica nomeada.

Aden permanece sem ator normalizado neste gate. Uma negociação genérica de acesso em Aden pode funcionar segundo `AccessModel`, mas `contact_authority()` não cria relação fictícia. A lacuna deve ser preenchida por pesquisa histórica.

## Temporalidade

Os vínculos respeitam `period_from` e `period_to`. A autoridade local de Melinde está normalizada apenas para 1498 porque o uso jogável decorre diretamente do episódio documentado da armada de Gama. O modelo não estende silenciosamente esse ator ou o efeito do piloto a outros anos.

## Interface e não vazamento

A interface continua mostrando somente relações já estabelecidas. Na campanha histórica, quando existe uma autoridade normalizada ainda não contatada, uma ação explícita de contato pode ser exibida. O nome do ator não é revelado no botão antes da interação; a interface mostra apenas que há uma “autoridade local documentada”. Depois do contato, o ator pode aparecer em `Relações estabelecidas`.

## Validação

Os testes cobrem:

- contato alterando somente relação e relógio;
- acesso comercial permanecendo inalterado;
- ausência de ação relacional onde não há autoridade normalizada;
- idempotência de contato repetido;
- distinção entre disponibilidade histórica do piloto e atribuição ao personagem;
- piloto de Melinde indisponível ao personagem antes do contato e disponível depois;
- campanha Lisboa–Calecute usando o piloto após a interação explícita;
- manutenção de apenas `UNESTABLISHED` e `CONTACTED` como estados necessários neste gate.

## Próximo gate

Estados mais ricos — confiança, hostilidade, privilégios, crédito, descontos ou influência política — continuam fora do MVP enquanto não forem necessários para uma decisão jogável específica e sustentados por regras explícitas. O próximo gate funcional é tornar o comércio da campanha operacional sem usar relações como modificadores genéricos de preço.
