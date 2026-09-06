# Playtest sintético por arquétipos — onda 12

## Objetivo

Repetir a bateria fixa de 10 arquétipos × 20 sessões depois da introdução dos eventos marítimos estocásticos v0.2, mantendo as mesmas políticas comportamentais e as mesmas faixas de seeds da onda 11. O objetivo é medir se a nova contingência reduz a concentração de sucessos sem substituir decisão por sorte.

## Resultado agregado

Foram executadas 200 sessões. A bateria concluiu 142/200 campanhas (71,0%), contra 143/200 (71,5%) na onda 11. Houve 139 eventos positivos de provisões, 136 eventos negativos de provisões e 35 eventos capazes de alterar duração em trajetórias não protegidas pela cronologia observada.

A mudança agregada de conclusão foi, portanto, mínima. O sistema estocástico está ativo e produz variação de recursos por seed, mas ainda não produz variância material de sucesso entre os arquétipos que seguem planejamento logístico e aceitam recuperação após bloqueios.

## Resultado por arquétipo

| Arquétipo | Onda 11 | Onda 12 | Eventos +provisões | Eventos -provisões | Eventos de timing |
|---|---:|---:|---:|---:|---:|
| GRAND_STRATEGIST | 20/20 | 20/20 | 16 | 15 | 0 |
| SURVIVALIST | 20/20 | 20/20 | 16 | 18 | 0 |
| MERCHANT | 20/20 | 20/20 | 20 | 24 | 0 |
| SPEEDRUNNER | 0/20 | 0/20 | 11 | 1 | 17 |
| ROGUELIKE | 0/20 | 0/20 | 1 | 1 | 0 |
| ROLEPLAYER | 20/20 | 20/20 | 18 | 18 | 0 |
| EXPLORER | 3/20 | 2/20 | 4 | 8 | 18 |
| OPTIMIZER | 20/20 | 20/20 | 16 | 14 | 0 |
| COMPLETIONIST | 20/20 | 20/20 | 14 | 18 | 0 |
| CASUAL | 20/20 | 20/20 | 23 | 19 | 0 |

## Diagnóstico

A v0.2 demonstra que a camada estocástica é reproduzível e consegue alterar provisões durante pernas históricas sem deslocar o timing observado. Porém, o resultado revela uma limitação de desenho mais importante do que a amplitude atual dos deltas.

Os eventos são selecionados no momento de `plan_voyage()`. Consequentemente, o plano já conhece `event_provision_delta`, incorpora esse efeito à viabilidade e pode bloquear a partida antes de o jogador executar a viagem. Arquétipos com política de recuperação respondem ao bloqueio reabastecendo, isto é, a contingência torna-se informação antecipada. Na prática, o risco é convertido em mais uma restrição de planejamento determinística.

Isso explica por que GRAND_STRATEGIST, SURVIVALIST, MERCHANT, ROLEPLAYER, OPTIMIZER, COMPLETIONIST e CASUAL continuam em 20/20 mesmo sofrendo numerosos eventos negativos. O OPTIMIZER, por exemplo, recebeu 14 eventos negativos e ainda concluiu 20/20; MERCHANT recebeu 24 e também concluiu 20/20.

O efeito material aparece sobretudo em perfis que já ignoravam planejamento ou abandonavam recuperação: EXPLORER cai de 3/20 para 2/20, enquanto SPEEDRUNNER e ROGUELIKE permanecem em 0/20. Não há, portanto, dispersão nova suficiente entre políticas competentes.

## Implicação de implementação

O próximo gate não deve ser simplesmente aumentar `PROVISION_SPOILAGE` de -8 para um valor mais severo. Isso aumentaria bloqueios previsíveis sem resolver a questão estrutural. O próximo modelo deve separar:

1. **previsão**, que estima duração, consumo e margem sem revelar qual evento ocorrerá;
2. **resolução**, que sorteia/aplica o evento somente quando a viagem é confirmada/executada;
3. **consequência**, que pode consumir a margem durante a travessia e produzir chegada em estado degradado ou, em casos extremos, falha operacional tratada por regra própria.

A seed deve permanecer determinística para reprodutibilidade. A interface pode comunicar risco agregado ou faixa de incerteza, mas não o evento específico antes da partida.

## Critério para a próxima onda

A onda 12 passa a ser o baseline da contingência revelada no planejamento. Uma onda 13 deve manter as mesmas 200 seeds e políticas, deslocando a resolução do evento para a execução. O objetivo de balanceamento é obter dispersão entre seeds sem tornar o resultado arbitrário: perfis prudentes devem permanecer robustos, mas não necessariamente 20/20; perfis agressivos devem exibir maior variância e eventos positivos devem ocasionalmente resgatar estratégias arriscadas.
