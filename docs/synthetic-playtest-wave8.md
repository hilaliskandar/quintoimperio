# Playtest sintético pós-MVP — onda 8

## Pergunta

Com a janela pré-partida fixada em 2 dias, qual é a menor margem logística entre 10, 20 e 30 dias-equivalentes que produz trajetória robusta sem alterar dados históricos?

## Desenho

Foram executadas 60 sessões: os mesmos 20 perfis/seeds repetidos com reservas de 10, 20 e 30 dias-equivalentes. Todas as sessões começam dois dias simulados antes da partida histórica de 1497-07-08. A margem só é constituída por ações normais de reabastecimento em portos onde o serviço é historicamente documentado e acionável.

Nenhuma disponibilidade `UNKNOWN` é imputada e nenhum recurso é concedido gratuitamente.

## Resultados

### Reserva de 10 dias

- 12/20 conclusões (60%);
- 0/20 `COUNTERFACTUAL`;
- `CAUTIOUS`, `DISCIPLINED` e `TRADER`: 4/4;
- `FRUGAL` e `IMPATIENT`: 0/4;
- 8 sessões terminam em Melinde;
- `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`: 28;
- `INSUFFICIENT_PROVISIONS`: 12.

### Reserva de 20 dias

- **20/20 conclusões (100%)**;
- **0/20 `COUNTERFACTUAL`**;
- todos os cinco perfis: 4/4;
- todas as sessões terminam em Calecute;
- mínimo observado de provisões: 6 dias-equivalentes;
- `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`: 12;
- não há bloqueio residual por provisões insuficientes.

### Reserva de 30 dias

- **20/20 conclusões (100%)**;
- **0/20 `COUNTERFACTUAL`**;
- todos os cinco perfis: 4/4;
- todas as sessões terminam em Calecute;
- resultados substantivos equivalentes à reserva de 20 dias.

A reserva de 30 dias produz 2.491 dias-unidade acumulados de provisões adicionadas nas 20 sessões, contra 1.620 com a reserva de 20, sem ganho na taxa de conclusão.

## Conclusão

Entre os valores testados, **20 dias-equivalentes é a menor margem robusta**. A reserva de 10 dias é insuficiente para os perfis que não fazem abastecimento preventivo adicional; 30 dias não melhora a conclusão em relação a 20.

Esse resultado não transforma 20 dias em fato histórico. Trata-se de um parâmetro de planejamento do jogo, derivado de teste de robustez do modelo atual.

## Implicação para o produto

A evidência recomenda:

1. uma fase pré-partida simulada de 2 dias, encerrada na data histórica de 1497-07-08;
2. um indicador de autonomia e margem logística;
3. apresentação de 20 dias-equivalentes como **margem recomendada de planejamento**, não como obrigação, recurso automático ou dado histórico;
4. serviços continuam consumindo tempo e recursos normalmente;
5. o jogador pode deliberadamente ignorar a recomendação e aceitar risco/contrafactualidade.

A interface deve explicar que a recomendação é uma heurística de jogo obtida por robustez da simulação, enquanto datas, escalas e disponibilidades documentadas permanecem evidência histórica.