# Playtest pareado por arquétipos — onda 16

## Objetivo

Testar agência sobre a mesma distribuição estocástica da onda 15, sem alterar probabilidades ou severidades dos eventos da v0.4. As mesmas seeds `21001–21020` foram aplicadas aos dez arquétipos. A única mudança de política foi permitir que alguns perfis pagassem por uma reserva segregada de provisões já embarcadas, capaz de mitigar exclusivamente `MAJOR_PROVISION_LOSS`.

A reserva é `SIMULATION`: não representa serviço portuário documentado, não aumenta o estoque de provisões e não revela antecipadamente o evento. O custo experimental é 0,25 ponto de capital por dia protegido em cada partida.

## Políticas de proteção

| Arquétipo | Reserva protegida por viagem |
|---|---:|
| SURVIVALIST | 20 dias |
| COMPLETIONIST | 15 dias |
| GRAND_STRATEGIST | 10 dias |
| ROLEPLAYER | 5 dias |
| MERCHANT | 0 |
| OPTIMIZER | 0 |
| CASUAL | 0 |
| EXPLORER | 0 |
| ROGUELIKE | 0 |
| SPEEDRUNNER | 0 |

## Resultado agregado

A onda 16 concluiu **133/200 campanhas (66,5%)**, contra **126/200 (63,0%)** na onda 15 pareada. A melhora agregada é secundária; o resultado decisivo é a separação entre políticas sob as mesmas seeds.

| Arquétipo | Onda 15 | Onda 16 | Reserva |
|---|---:|---:|---:|
| GRAND_STRATEGIST | 18/20 | **20/20** | 10 |
| SURVIVALIST | 18/20 | **20/20** | 20 |
| COMPLETIONIST | 18/20 | **20/20** | 15 |
| ROLEPLAYER | 18/20 | **19/20** | 5 |
| MERCHANT | 18/20 | **18/20** | 0 |
| OPTIMIZER | 18/20 | **18/20** | 0 |
| CASUAL | 18/20 | **18/20** | 0 |
| EXPLORER | 0/20 | 0/20 | 0 |
| ROGUELIKE | 0/20 | 0/20 | 0 |
| SPEEDRUNNER | 0/20 | 0/20 | 0 |

As duas seeds que eram fatais para todos na onda 15 tornaram-se discriminantes:

- `21010`: GRAND_STRATEGIST, COMPLETIONIST e SURVIVALIST concluem; ROLEPLAYER e todos os perfis sem reserva falham.
- `21014`: GRAND_STRATEGIST, COMPLETIONIST, ROLEPLAYER e SURVIVALIST concluem; os perfis sem reserva falham.

Isso fornece evidência direta de agência: diante da mesma contingência, decisões preparatórias distintas passaram a produzir resultados diferentes.

## Custo estratégico

A mitigação não é gratuita. Como a reserva é preparada por viagem, perfis mais prudentes terminam com menos capital disponível. Nas 20 seeds, a mediana aproximada do capital final foi:

- SURVIVALIST: **48,10**;
- COMPLETIONIST: **57,75**;
- GRAND_STRATEGIST: **70,15**;
- ROLEPLAYER: **85,08**;
- CASUAL/OPTIMIZER sem proteção: cerca de **97,58**.

Portanto, a v0.5 cria o trade-off procurado: robustez logística versus capital comercial. Não há evidência para tornar a reserva obrigatória nem para aumentar a margem logística geral.

## Interpretação

A onda 15 havia mostrado que a cauda rara introduzia contingência, mas duas seeds funcionavam como derrotas praticamente inevitáveis. A onda 16 mostra que não é necessário reduzir a severidade desses eventos para resolver o problema. Uma ação de mitigação limitada pode preservar a cauda de risco e, simultaneamente, devolver agência ao jogador.

O gradiente também é informativo. Cinco dias de proteção resolvem uma das duas seeds severas; dez dias resolvem ambas no conjunto testado. Isso sugere que a escolha da quantidade protegida pode ser estratégica, em vez de um botão binário de segurança.

## Próximo gate

Antes de qualquer nova calibração probabilística, recomenda-se:

1. manter as probabilidades e amplitudes da v0.4 congeladas;
2. integrar a preparação da reserva como escolha explícita na interface pré-partida;
3. apresentar custo, quantidade protegida e natureza `SIMULATION`, sem revelar qual evento ocorrerá;
4. registrar no feedback pós-viagem quanto da perda foi mitigada;
5. repetir a bateria pareada depois da integração de interface para verificar que a escolha continua produzindo o mesmo gradiente de resultados.

A implementação experimental deve permanecer separada de qualquer afirmação histórica sobre técnicas específicas de preservação ou segregação de mantimentos.