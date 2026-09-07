# P1-func — diagnóstico do retorno a partir de estados concluídos do MVP

Issue: #99.

Execução: workflow `Validate historical data and simulation`, run `34115653625`, commit `59c98b4c25882419352b942113c6379400ec3240`.

## Desenho

Foram reproduzidos 20 casos: cinco arquétipos competentes (`GRAND_STRATEGIST`, `SURVIVALIST`, `MERCHANT`, `ROLEPLAYER`, `COMPLETIONIST`) × quatro seeds fixas (`23001–23004`). Cada caso percorreu primeiro o MVP Lisboa–Calecute pelas políticas existentes. Somente estados que satisfizeram o gate de conclusão do MVP foram encaminhados para `ReturnCampaignModel`.

No retorno, a política diagnóstica foi deliberadamente simples: ativar explicitamente `EXP_GAMA_RETURN_1498`; usar reabastecimento apenas nas permanências documentadas que registram provisões/alimentos; respeitar datas guiadas; e tentar as seis pernas até BRG. Nenhuma condição, provisão ou probabilidade foi recalibrada para o teste.

## Resultado agregado

- casos totais: **20**;
- MVP concluído: **18/20**;
- entre os 18 estados elegíveis, retorno concluído até BRG: **12/18 (66,7%)**;
- blockers no retorno: **1 `INSUFFICIENT_PROVISIONS`** e **5 `VESSEL_CONDITION_TOO_LOW`**.

Por arquétipo:

| Arquétipo | MVP concluído | Retorno concluído |
|---|---:|---:|
| GRAND_STRATEGIST | 4/4 | 2/4 |
| SURVIVALIST | 4/4 | 3/4 |
| MERCHANT | 3/4 | 2/3 |
| ROLEPLAYER | 3/4 | 2/3 |
| COMPLETIONIST | 4/4 | 3/4 |

## Achado 1 — ponte logística Calecute → Anjediva

O horizonte corrigido reconhece Anjediva como o próximo ponto de decisão de provisões específico da expedição. Assim, na partida de Calecute:

- requisito da primeira perna: **21 dias-equivalentes**;
- horizonte até nova permanência documental com provisões: **21 dias-equivalentes**.

Um estado real do MVP chegou a Calecute com **19,366** dias-equivalentes e ficou inevitavelmente bloqueado na partida do retorno. `nodes.csv` mantém corretamente a disponibilidade portuária genérica de provisões de Calecute sem preenchimento inventado. Portanto, não há atualmente uma ação documentada que permita recuperar os 1,634 dias-equivalentes faltantes durante a longa permanência antes de 30/08.

Esse caso é um problema de agência/continuidade a ser pesquisado; não deve ser resolvido concedendo provisões automaticamente ou alterando a duração documentada da perna.

## Achado 2 — condição estrutural no retorno

Cinco casos — todos associados à seed `23004`, independentemente do arquétipo — chegaram a São Brás em 12/03/1499 e não puderam iniciar a perna seguinte por `VESSEL_CONDITION_TOO_LOW`. O fato de o bloqueio se concentrar na mesma seed e no mesmo ponto indica um problema estocástico/estrutural do prolongamento da campanha, não uma diferença de política de provisões.

A regra consolidada do projeto continua válida: **medir antes de mitigar**. Nenhum reparo, sobressalente, aumento de condição ou redução de severidade deve ser acrescentado até identificar a condição herdada do MVP, a sequência de eventos do retorno e o evento específico que produz o blocker.

## Achado 3 — o retorno é tecnicamente percorrível

Doze estados reais concluíram as seis pernas mantendo `GUIDED` e chegaram aos Baixos do Rio Grande em **25/04/1499**. O smoke canônico com estado controlado também passou integralmente. Isso valida a arquitetura opt-in e a ação de provisões específica de permanência documental.

## Decisão

A #99 não deve ser encerrada ainda. O gate funcional básico existe e passa pela CI, mas a robustez de continuidade revela duas lacunas residuais:

1. agência logística na ponte Calecute → Anjediva para estados do MVP com provisões inferiores a 21;
2. diagnóstico dirigido da seed 23004 e da condição estrutural antes da partida São Brás → Cabo.

Essas duas lacunas devem ser tratadas separadamente. O primeiro problema exige retorno às fontes para verificar se há suporte documental para uma ação de preparação/provisões durante a permanência em Calecute ou aquisição costeira imediatamente anterior/durante a primeira perna. O segundo exige apenas instrumentação e análise do estado/eventos antes de qualquer nova mecânica.

Arquivo bruto reproduzível: artefato `return-from-mvp-wave17.json` do run `34115653625`.