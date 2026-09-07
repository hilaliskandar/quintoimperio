# P3.1-doc — latência de informação Cabral → João da Nova v0.1

Data: 2026-09-07
Issues: #110, #111

## Problema

A reconstrução de Cabral não pode transferir automaticamente para a armada seguinte todo o conhecimento produzido em 1500–1501. É necessário distinguir **quando** uma informação existe no teatro do Índico, **quando** ela chega à Coroa em Lisboa e **quando** uma nova expedição pode efetivamente adquiri-la.

A listagem de armadas da EVE/FCSH data a partida de João da Nova em **05/03/1501**. Nessa data, Cabral já havia deixado Cananor em 16/01/1501, mas ainda regressava pelo Índico/África. A `Anunciada`, primeiro navio do retorno de Cabral registrado pela cronologia crítica como chegado ao Restelo, somente alcança Lisboa em **24/06/1501**; as demais embarcações chegam em sequência no fim de julho e Diogo Dias ainda mais tarde.

Consequência: João da Nova **não pode iniciar sua campanha com conhecimento da Coroa sobre a ruptura em Calecute, a alternativa comercial de Cochim, a feitoria ali deixada ou o acolhimento de Cananor**, salvo se surgir fonte específica demonstrando comunicação anterior por outra via.

Há, porém, uma exceção importante: a EVE/FCSH registra que Gaspar de Lemos regressou a Lisboa com cartas e objetos de Vera Cruz e chegou ao reino em **junho de 1500**. Assim, o conhecimento da descoberta atlântica já podia integrar o estado da Coroa antes da partida de João da Nova.

## Linha temporal mínima

| Momento | Informação/evento | Onde existe | Disponível à Coroa em Lisboa? | Disponível a João da Nova na partida? |
|---|---|---|---|---|
| 1499 | resultados da primeira viagem de Gama | Lisboa/Portugal | SIM | SIM |
| maio de 1500 | notícia/documentação de Vera Cruz enviada por Gaspar de Lemos | circuito Atlântico → Lisboa | em trânsito | ainda não |
| junho de 1500 | Gaspar de Lemos chega a Lisboa com cartas e objetos | Lisboa | SIM | SIM em princípio; conteúdo detalhado deve respeitar o que foi efetivamente comunicado |
| 16/12/1500 | ruptura da feitoria em Calecute | Calecute/Índico | NÃO | NÃO |
| 24/12/1500–09/01/1501 | carregamento e residentes portugueses em Cochim | Cochim/Índico | NÃO | NÃO |
| 15/01/1501 | acolhimento e compra em Cananor | Cananor/Índico | NÃO | NÃO |
| 16/01/1501 | Cabral inicia retorno | Índico | NÃO | NÃO |
| 05/03/1501 | João da Nova parte de Lisboa | Lisboa | resultados de Gama + notícia de Vera Cruz; não os resultados do Malabar de Cabral | baseline de partida |
| 24/06/1501 | `Anunciada` chega ao Restelo | Lisboa | SIM para o conjunto de notícias que ela efetivamente transporta | tarde demais para alterar o estado inicial da armada já no mar |
| fim jul. 1501 | outras embarcações de Cabral chegam | Lisboa | SIM, ampliando/confirmando informação | somente para decisões posteriores da Coroa, não retroativamente para João da Nova |

## Três camadas de estado

### 1. Estado objetivo/local

Eventos ocorridos no Índico alteram o mundo independentemente de Lisboa saber deles. Em março de 1501:

- a feitoria de Calecute já havia sido destruída e a relação com o Samorim estava em ruptura;
- havia residentes portugueses em Cochim;
- Cochim havia funcionado como alternativa efetiva de carregamento;
- Cananor havia recebido Cabral favoravelmente.

Esses são estados locais do mundo.

### 2. Conhecimento da Coroa

A Coroa só deve receber uma informação quando houver uma trajetória documental plausível de transmissão até Lisboa. A chegada posterior de Cabral não pode retroagir conhecimento para 05/03/1501. A notícia de Vera Cruz é um caso positivo de transmissão anterior, via Gaspar de Lemos em junho de 1500.

### 3. Conhecimento da expedição seguinte

João da Nova parte com o conhecimento disponível em Lisboa no momento da partida. Durante a viagem, pode adquirir estados locais por agentes, cartas, encontros ou residentes no teatro asiático. O momento dessa aquisição deve ser documentado quando relevante.

## Implicação arquitetural

A arquitetura existente já separa conhecimento do personagem e da Coroa e impede cópia silenciosa de conhecimento institucional. P3 deve preservar esse princípio entre expedições.

Não é necessário criar desde já um sistema genérico de correio. Para o primeiro P3-func, pode bastar uma tabela documental de **eventos de transmissão/availability**, com pelo menos:

- `information_id`;
- evento/fato conhecido;
- `available_from_date`;
- `holder_scope` (`LOCAL`, `CROWN`, `EXPEDITION` ou equivalente);
- origem/veículo de transmissão quando documentado;
- evidência e fonte;
- notas/limites.

A existência dessa necessidade deve ser auditada contra os schemas atuais antes de implementar qualquer arquivo.

## Efeito sobre a #111

A formulação anterior de que os resultados de Cabral “devem persistir para João da Nova” precisa ser qualificada:

- **persistem no mundo local**, sim;
- **não persistem automaticamente como conhecimento inicial da Coroa ou da armada de João da Nova**;
- **a notícia de Vera Cruz é exceção documentada**, pois chegou a Lisboa em junho de 1500;
- os fatos do Malabar podem ser descobertos por João da Nova quando alcançar o teatro do Índico, conforme a documentação de sua própria viagem.

## Próximas verificações

1. determinar que informações a `Anunciada` efetivamente trouxe em 24/06/1501;
2. reconstruir o primeiro contacto de João da Nova no Malabar e quando ele toma conhecimento da situação de Calecute/Cochim/Cananor;
3. verificar se o modelo atual de `information_history` e conhecimento por ator já suporta esse comportamento sem novo schema;
4. manter como erro de modelagem qualquer transferência de fatos de Cabral para João da Nova apenas porque cronologicamente ocorreram antes da chegada deste à Índia.

## Decisão provisória

P3 deverá tratar **latência e titularidade da informação** como parte da cronologia, não como metadado opcional. Isso é mais importante para a continuidade entre campanhas do que adicionar novas mercadorias ou sistemas de combate neste estágio.