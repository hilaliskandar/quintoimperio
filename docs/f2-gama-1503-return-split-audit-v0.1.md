# F2 — Vasco da Gama 1503 — auditoria da partida final e separação de Vicente Sodré v0.1

Data: 2026-09-08
Issue: #122

## Pergunta

Qual é o intervalo documentalmente defensável para a partida final de Vasco da Gama do Malabar e, portanto, para a consolidação da separação entre a frota que regressa ao reino e a força de Vicente Sodré que permanece no Índico?

## Evidência

1. `CALCOEN_1504` registra combate naval em 12/02/1503 e partida no dia seguinte em direção a Cananor, deixando claro que a frota principal ainda operava no Malabar em 13/02.
2. Dois documentos de Vasco da Gama conservados na Torre do Tombo são datados e assinados em Cananor em 22/02/1503. Eles demonstram presença física/documental do almirante no porto nessa data e funcionam como `terminus post quem` para a partida final.
3. Sínteses especializadas situam a partida no fim de fevereiro de 1503; uma reconstrução historiográfica específica utiliza 28/02/1503. Como essa data não foi localizada neste gate em testemunho contemporâneo equivalente aos documentos de 22/02, ela não recebe classificação `EXACT`.

## Classificação

- presença de Vasco da Gama em Cananor em 22/02/1503: `EXACT`;
- partida final do Malabar: `INTERVAL`, operacionalmente `23/02/1503–28/02/1503`;
- 28/02/1503: limite superior de reconstrução, não testemunho diário independente neste gate;
- força de Vicente Sodré permanecendo no Índico após a partida: consequência documental firme, mas a transição deve ser aplicada conservadoramente apenas no limite superior do intervalo.

## Decisão de modelagem

1. estreitar `GAMA1502_E03/FORCE_REMAINS` de `1503-01-01–1503-03-31` para `1503-02-23–1503-02-28`;
2. acrescentar evento de partida da frota principal no mesmo intervalo, `CAN → LIS`, sem criar uma rota executável de retorno;
3. manter `date_precision=RANGE` e regra conservadora: o estado `FORCE_REMAINS` só é considerado consolidado em 28/02/1503;
4. não criar `EXP_GAMA_RETURN_1503` neste gate, pois a sequência transoceânica continua sem cronologia suficientemente fina e não é necessária para provar a bifurcação;
5. não criar `EXP_SODRE_1503` jogável apenas para representar permanência. O evento temporal já expressa o estado objetivo do mundo; uma subcampanha só será necessária quando as ações posteriores de Sodré precisarem de escolhas/rotas próprias no loop de F3.

## Consequência arquitetural

A arquitetura de um único `active_expedition_id` continua suficiente para F2. A bifurcação é representável por:

- trajetória controlada do jogador: `EXP_GAMA_1502`;
- estado mundial temporal: `SODRE_FORCE/FORCE_REMAINS`;
- eventual subcampanha posterior somente quando houver necessidade funcional real.

Isso evita introduzir múltiplas frotas simultâneas por antecipação.

## Gate de saída

F2 pode considerar resolvida a bifurcação Gama/Sodré se:

- os dois eventos usarem a janela `23–28/02/1503`;
- testes garantirem que o efeito residente não é aplicado antes de 28/02;
- save/load da campanha principal continuar verde;
- nenhuma rota de retorno inventada for criada;
- CI integral permanecer verde.
