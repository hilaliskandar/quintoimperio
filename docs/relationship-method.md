# Método de relações por atores v0.1

## Objetivo

Evitar uma reputação global abstrata e começar por atores historicamente identificáveis. A camada v0.1 separa a existência histórica do ator de qualquer estado relacional do personagem.

`data/actors.csv` registra atores/comunidades sustentados pelo corpus. `data/node_actors.csv` associa cada ator a um nó, papel e período. `RelationshipModel` apenas consulta essas associações; ele não fabrica uma autoridade ou comunidade mercantil para preencher lacunas de jogabilidade.

## Primeiro recorte histórico

A base inicial contém três atores:

- a autoridade institucional do Samudri Raja de Calecute;
- os mercadores muçulmanos/pardesi de Calecute como comunidade mercantil agregada;
- a autoridade local de Melinde em 1498, que Subrahmanyam registra como responsável por enviar o piloto guzerate à armada.

Alpers sustenta, para Calecute, o patronato do Samudri Raja sobre mercadores muçulmanos e a presença destes em funções portuárias e estruturas comunitárias próprias. Prakash permite distinguir, no começo da presença portuguesa, a relação com o Samudri da relação com os mercadores pardesi. Por isso os dois não são comprimidos em uma única “facção de Calecute”.

A comunidade mercantil de Calecute é deliberadamente agregada apenas no nível que o corpus atual sustenta. Ela não significa que todos os mercadores muçulmanos/pardesi tinham interesses, posições políticas ou estratégias idênticos.

## Estados relacionais

A v0.1 define somente:

- `UNESTABLISHED`: nenhuma interação explícita do personagem com aquele ator foi registrada pelo loop;
- `CONTACTED`: ocorreu uma interação explícita que pode ser associada àquele ator.

Os valores internos do `IntEnum` servem apenas à implementação. Eles não são pontos de reputação. Não existem ainda `+10`, confiança percentual, amizade, hostilidade ou alinhamento político.

## Separação entre sistemas

Relação com ator é distinta de:

- conhecimento geográfico, náutico, comercial ou político;
- acesso institucional ao porto;
- participação em armada;
- disponibilidade de intermediário;
- competência de piloto;
- preço ou disponibilidade de mercadoria.

Uma futura integração poderá registrar que uma negociação de acesso colocou o personagem em contato com uma autoridade documentada, ou que `MERCHANT_CONTACT` estabeleceu contato com uma comunidade mercantil documentada. Esse registro, por si só, não deverá conceder desconto, crédito, informação adicional ou sucesso diplomático.

## Política contra atores inventados

`RelationshipModel.actor_for_role()` retorna `None` quando a base não possui ator para aquele nó/papel/período. Isso é intencional. `broker_availability=HIGH`, por exemplo, indica possibilidade estrutural de intermediação, mas não autoriza criar silenciosamente uma comunidade histórica nomeada.

Aden permanece sem ator normalizado neste primeiro gate, embora seja um porto conhecido do modelo. A lacuna deve ser preenchida por pesquisa histórica, não por uma entidade genérica criada para completar a interface.

## Temporalidade

Os vínculos respeitam `period_from` e `period_to`. A autoridade local de Melinde foi normalizada apenas para 1498 porque o primeiro uso jogável decorre diretamente do episódio documentado da armada de Gama. O modelo não estende silenciosamente esse registro para 1499 ou décadas posteriores.

## Próximo gate

Depois de validar a normalização histórica dos atores, a integração seguinte será estritamente conservadora: ações já existentes poderão mudar apenas `UNESTABLISHED -> CONTACTED` quando houver associação não ambígua entre nó, papel e ator. Modificadores de reputação, confiança, acesso, preços, crédito ou privilégios ficam fora até que sejam definidos e justificados separadamente.
