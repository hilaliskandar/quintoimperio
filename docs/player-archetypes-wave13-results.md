# Playtest sintético por arquétipos — onda 13

## Objetivo

Repetir as mesmas 200 sessões da onda 12 depois de separar o planejamento da resolução estocástica. As probabilidades e amplitudes dos eventos foram mantidas: a única mudança substantiva foi ocultar o evento específico até a execução da viagem.

## Resultado agregado

A onda 13 concluiu **141/200 campanhas (70,5%)**, contra 142/200 (71,0%) na onda 12 e 143/200 (71,5%) na onda 11. Foram registrados 136 eventos positivos de provisões, 138 negativos e 36 eventos de timing em trajetórias sem proteção cronológica.

| Arquétipo | Onda 11 | Onda 12 | Onda 13 |
|---|---:|---:|---:|
| GRAND_STRATEGIST | 20/20 | 20/20 | 20/20 |
| SURVIVALIST | 20/20 | 20/20 | 20/20 |
| MERCHANT | 20/20 | 20/20 | 20/20 |
| SPEEDRUNNER | 0/20 | 0/20 | 0/20 |
| ROGUELIKE | 0/20 | 0/20 | 0/20 |
| ROLEPLAYER | 20/20 | 20/20 | 20/20 |
| EXPLORER | 3/20 | 2/20 | 1/20 |
| OPTIMIZER | 20/20 | 20/20 | 20/20 |
| COMPLETIONIST | 20/20 | 20/20 | 20/20 |
| CASUAL | 20/20 | 20/20 | 20/20 |

## Interpretação

A mudança v0.3 corrigiu a antecipação indevida da contingência: um evento negativo já não pode ser conhecido e neutralizado antes da partida. Os testes específicos confirmam que o plano jogável contém `events=()` e `events_resolved=False`, enquanto a execução resolve e registra o evento de forma reproduzível.

Entretanto, a bateria mostra que essa correção, isoladamente, **não é suficiente para quebrar a taxa de sucesso total dos perfis competentes**. Sete arquétipos continuam em 20/20. O motivo agora é de magnitude e diversidade dos riscos, não mais de vazamento de informação: a margem logística recomendada de 20 dias absorve confortavelmente perdas máximas de 8 dias-equivalentes, e os eventos compatíveis com timing observado afetam principalmente provisões.

Há sinal de efeito sobre políticas frágeis. EXPLORER caiu de 3/20 para 2/20 e agora para 1/20. SPEEDRUNNER e ROGUELIKE permanecem em 0/20, portanto não servem para calibrar a faixa superior da dificuldade.

## Diagnóstico para o próximo gate

Não há evidência para voltar a revelar eventos no planejamento. A resolução tardia deve ser preservada. O próximo incremento deve ampliar a distribuição de consequências sem transformar toda viagem em loteria.

Recomenda-se introduzir uma **cauda rara de alta severidade** e, preferencialmente, uma segunda dimensão de risco além de provisões. A ordem proposta é:

1. manter `PROVISION_SPOILAGE` comum com perdas moderadas;
2. acrescentar evento raro de contaminação/perda extensa de mantimentos, capaz de consumir grande parte da margem de 20 dias;
3. acrescentar evento raro de dano estrutural sem alteração obrigatória do timing observado;
4. manter eventos positivos compensatórios de menor frequência/magnitude;
5. repetir as mesmas 200 seeds antes de alterar novamente probabilidades.

O objetivo não é uma taxa agregada arbitrária, mas gerar dispersão entre seeds nos perfis que atualmente fazem 20/20. Um bom sinal será que alguns perfis prudentes continuem muito robustos, enquanto perfis apenas adequados deixem de ser virtualmente garantidos.
