# F2 — Vasco da Gama 1502–1503 — auditoria fina do Malabar v0.1

Data: 2026-09-08
Issue: #122
Baseline F1: `24b6de7799f3ebb40c9a3401a73ddb5913d1190f`

## Objetivo

Reavaliar a sequência Cananor–Calecute–Cochim e a preparação da torna-viagem com fonte contemporânea, antes de ampliar o loop executável de `EXP_GAMA_1502`.

## Nova fonte incorporada

Foi incorporado ao corpus o ID `CALCOEN_1504`: *Calcoen*, relação flamenga contemporânea da segunda viagem de Vasco da Gama, impressa em Antuérpia c. 1504 e reproduzida com tradução por J. Ph. Berjeau em 1881.

A edição informa que o opúsculo de Antuérpia é contemporâneo à viagem e que o autor foi participante da expedição. O texto não nomeia Vasco da Gama, mas a sequência de datas, lugares e episódios identifica a armada de 1502–1503.

Regra de uso: as datas testemunhais de `CALCOEN_1504` são preservadas como evidência própria; divergências com EVE/FCSH ou outras sínteses não são harmonizadas silenciosamente.

## Divergência já identificada na partida

- EVE/FCSH: partida principal em 01/02/1502;
- `CALCOEN_1504`: partida de Lisboa em 10/02/1502.

Decisão: não reescrever neste subgate a âncora inicial já adotada em F2. A divergência fica registrada e exige gate específico caso se pretenda alterar o baseline de partida.

## Âncoras testemunhais do Malabar

A relação permite elevar a resolução dos seguintes marcos:

| Marco | Data | Classificação | Uso |
|---|---:|---|---|
| chegada/atuação inicial em Cananor | 11/09/1502 | `EXACT` | marco histórico; não vira automaticamente `expedition_stop` porque a perna `KIL→CAN` ainda não possui timing diário observado |
| contato comercial em Cananor | 20/10/1502 | `EXACT` | evento específico, sem criar novo serviço genérico |
| saída de Cananor rumo a Calecute | 27/10/1502 | `EXACT` | evento de movimento; pode futuramente funcionar como release cronológico se a chegada a Cananor for sincronizada de modo defensável |
| saída de Calecute rumo a Cochim | 02/11/1502 | `EXACT` | evento de movimento; não implica duração diária observada da perna |
| audiência/negociação com o rajá de Cochim | 28/11/1502 | `EXACT` | reforça a reorganização institucional/comercial já modelada |
| saída de Cochim para o sul | 03/01/1503 | `EXACT` | evento de partida; o destino seguinte referido é Quilon, ainda não materializado como nó operacional em F2 |
| combate ligado a Calecute | 12/02/1503 | `EXACT` | evento histórico específico; não autoriza combate geral |
| partida no dia seguinte para Cananor, em preparação do retorno | 13/02/1503 | `EXACT` | prova que a frota principal ainda estava no Malabar nessa data; limita inferiormente a separação final da força de Vicente Sodré |

## Sequência que passa a ser documentalmente firme

No nível de ordem histórica:

`CAN → CAL → COC → [QLN / circuito meridional] → CAL → CAN → retorno`

A parte entre a saída de Cochim em 03/01 e o combate de 12/02 não está suficientemente resolvida para um itinerário jogável contínuo. O texto menciona Quilon, mas o retorno ao teatro de Calecute não recebe sequência fina bastante para preencher todas as pernas sem interpolação.

## Consequência para a força de Vicente Sodré

O registro de 13/02/1503 mostra que a frota principal ainda opera no Malabar imediatamente antes da preparação final de retorno. Portanto, o intervalo amplo atualmente usado para `GAMA1502_E03` (`1503-01-01`–`1503-03-31`) é documentalmente conservador demais para representar a separação.

Neste subgate, porém, não se fixa ainda um dia exato para a bifurcação. A conclusão defensável é:

- separação não pode ser anterior a 13/02/1503;
- sínteses modernas situam a partida principal em fevereiro/inícios de 1503;
- o estado `FORCE_REMAINS` é estruturalmente correto, mas sua janela deve ser refinada somente após fechar a evidência da partida final.

## Decisão de implementação

1. incorporar em `expedition_events.csv` somente os marcos testemunhais que não exigem novas pernas executáveis;
2. manter `EXP_GAMA_1502` jogável, por ora, até Cananor;
3. não criar ainda `QLN`, `EXP_GAMA_RETURN_1503` ou `EXP_SODRE_1503`;
4. não adicionar linhas a `voyage_observations.csv` para movimentos cuja duração não é observada;
5. não transformar os episódios de Calecute em sistema geral de combate;
6. abrir o próximo subgate especificamente para a partida final do Malabar e o momento de bifurcação Gama/Sodré.

## Critério de saída

Este subgate estará concluído quando:

- os marcos exatos estiverem persistidos como eventos documentais;
- testes confirmarem datas, sequência e natureza não genérica desses eventos;
- CI integral permanecer verde;
- a próxima investigação ficar reduzida à partida final e à separação da força residente.
