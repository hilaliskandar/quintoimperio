# Método histórico e proveniência

## Regra central

O projeto mantém três camadas explicitamente separadas:

1. **Evidência histórica** — afirmação diretamente sustentada por fonte identificável.
2. **Inferência histórica** — interpretação plausível derivada de uma ou mais evidências, registrada como tal.
3. **Parâmetro de simulação** — valor criado para produzir comportamento de jogo coerente; nunca deve ser apresentado como dado histórico.

## Escala de evidência

- `A` — evidência direta, contemporânea ou muito próxima do período e específica para o nó, rota ou mercadoria.
- `B` — evidência forte, mas regional, comparativa ou ligeiramente posterior/anterior.
- `C` — inferência fundamentada que exige validação adicional.
- `D` — hipótese de desenho; não deve alimentar conteúdo histórico definitivo.

## Escopo da evidência

- `NODE_DIRECT` — evidência específica para o nó.
- `REGIONAL` — evidência válida para uma região e aplicada cautelosamente ao nó.
- `NETWORK` — evidência sobre o circuito comercial, sem atribuição necessária de produção local.
- `LATER_PERIOD_ANALOGY` — analogia posterior; não usar como prova de condição em 1497–1500.

## Regras para mercadorias

Toda associação entre nó e bem deve distinguir:

- `PRODUCE` — produção local;
- `HINTERLAND` — chega de área produtora interior associada ao porto;
- `IMPORT` — importado para consumo ou redistribuição;
- `EXPORT` — exportado pelo nó;
- `TRANSIT` — observado em circulação/reexportação;
- `DEMAND` — procurado como bem de troca;
- `UNKNOWN` — presença documentada sem direção segura.

Uma mercadoria observada num porto não deve ser marcada automaticamente como produção local.

## Rotas

Toda rota deve registrar se pertence a:

- `PREEXISTING_NETWORK` — circuito anterior à presença portuguesa;
- `PORTUGUESE_EXPLORATION` — itinerário exploratório;
- `PORTUGUESE_INSTITUTIONAL` — carreira, rota ou ligação formalizada posteriormente.

Também devem ser separados:

- existência histórica da conexão;
- navegabilidade sazonal;
- conhecimento da Coroa;
- conhecimento do personagem;
- acesso comercial efetivo.

## Conhecimento

O modelo deve distinguir pelo menos:

- `geo_knowledge` — localização;
- `nav_knowledge` — como chegar;
- `market_knowledge` — funcionamento comercial;
- `political_knowledge` — autoridades, alianças e protocolos.

Conhecer a existência de Calecute, por exemplo, não implica conhecer a rota segura, o preço da pimenta ou os intermediários necessários.

## Pessoas escravizadas

O tráfico de pessoas escravizadas é historicamente central para a expansão atlântica portuguesa, mas não será tratado como mercadoria ordinária em `goods.csv`. Deve possuir estrutura própria capaz de registrar coerção, captura, compra, transporte forçado, mortalidade, destino, legislação, atores e consequências sociais.

## Preços

O projeto não atribuirá números monetários a 1497–1500 sem documentação adequada. A primeira modelagem econômica usará classes relativas e parâmetros de simulação. Esses valores deverão ficar identificados como `SIMULATION`, nunca como `HISTORICAL`.

## Corpus de partida

O corpus de pesquisa inicial inclui, entre outros, Malyn Newitt, Nuno Vila-Santa, Om Prakash, Sanjay Subrahmanyam e Edward A. Alpers, complementados por fontes primárias e estudos especializados à medida que surgirem lacunas.
