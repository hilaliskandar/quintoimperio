# Método de permanências históricas v0.1

## Objetivo

Integrar `data/expedition_stops.csv` ao loop jogável sem converter automaticamente atividades históricas em quantidades físicas inventadas.

A permanência é uma dimensão própria da viagem. Chegar a um ancoradouro, permanecer nele e executar serviços são operações distintas.

## Evidência preservada

Cada `ExpeditionStop` mantém separadamente:

- data de chegada registrada;
- data de partida registrada;
- `observed_stay_days`, isto é, a duração declarada pela narrativa;
- atividades documentadas;
- grau, escopo e fonte da evidência.

`observed_stay_days` não é recalculado a partir das datas. Isso é necessário porque datas reconstruídas editorialmente e contagens narrativas inclusivas podem produzir diferenças aritméticas distintas. A baía de Santa Helena é o caso de teste: a base mantém permanência narrada de oito dias e datas editoriais 7–16 de novembro, cuja diferença aritmética é nove dias.

## Atividades não são efeitos automáticos

Entradas como `WATER`, `WOOD`, `CARENING`, `MAST_REPAIR` ou `CARGO_TRANSFER` significam apenas que a atividade está documentada para aquela escala.

A chegada não concede automaticamente:

- dias-equivalentes de provisões;
- pontos de condição do navio;
- mercadorias;
- dinheiro;
- bônus de navegação.

Reabastecimento e reparo continuam exigindo ações explícitas de `PortServiceModel`. O tempo dessas ações avança o mesmo calendário usado pela permanência e, portanto, pode consumir parte do intervalo antes da partida histórica.

## Cronologia guiada e contrafactual

`ChronologyMode` possui dois estados:

- `GUIDED`: a campanha ainda acompanha a cronologia documentada;
- `COUNTERFACTUAL`: escolhas ou atrasos já afastaram a sessão da sequência temporal registrada.

A regra v0.1 é deliberadamente estrita e auditável: uma chegada a escala permanece `GUIDED` somente quando a data simulada coincide com a data registrada em `expedition_stops.csv`. Não existe tolerância oculta de alguns dias.

Enquanto uma escala está `GUIDED` e a data atual é anterior à partida documentada, uma nova viagem recebe o bloqueio `HISTORICAL_STOP_NOT_RELEASED`.

A ação `wait_for_stop_release()` avança apenas o relógio até a data de partida. Ela não altera provisões, condição, carga ou capital.

Se o jogador permanecer além da partida documentada e então navegar, a cronologia passa para `COUNTERFACTUAL`. A mudança é permanente para essa sessão v0.1: a interface pode continuar mostrando que a escala possui precedente histórico, mas deixa de impor espera para reproduzir datas documentadas.

## Exemplo São Thiago

No cenário histórico:

1. Lisboa → São Thiago parte em 8 de julho de 1497;
2. a observação da própria rota leva à chegada em 27 de julho;
3. `GAMA1497_STG` torna-se a escala ativa;
4. a partida documentada é 3 de agosto;
5. serviços executados entre 27 de julho e 3 de agosto consomem dias desse intervalo;
6. `wait_for_stop_release()` pode consumir somente o restante;
7. nenhuma água, carne, madeira ou reparo é concedido automaticamente pelo simples ato de esperar.

## Escalas sem mercado

A integração de permanências não altera a regra cartográfica e econômica: ancoradouros logísticos não se tornam mercados. `market_scale=NONE` continua impedindo que uma escala seja tratada como entreposto comercial ordinário.

## Limitações

A v0.1 não modela ainda simultaneidade de trabalhos, número de homens empregados, produtividade de carenagem, quantidades de água/comida, mortalidade, doença ou capacidade física por classe de navio.

Também não tenta reconciliar silenciosamente cronologias editoriais conflitantes. Quando a fonte ou a edição é incerta, essa incerteza permanece nos dados e nas notas.
