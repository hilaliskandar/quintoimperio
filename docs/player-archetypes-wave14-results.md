# Playtest sintético por arquétipos — onda 14

## Objetivo

Repetir a bateria de 200 sessões depois da introdução da cauda rara de risco da v0.4, preservando a resolução estocástica somente na execução. Foram mantidas as políticas comportamentais dos dez arquétipos e as mesmas faixas de seeds usadas nas ondas anteriores para cada arquétipo.

## Resultado agregado

A onda 14 concluiu **128/200 campanhas (64,0%)**, contra 141/200 (70,5%) na onda 13, 142/200 (71,0%) na onda 12 e 143/200 (71,5%) na onda 11. Foram registrados 130 eventos positivos de provisões, 172 negativos e 31 eventos de timing em trajetórias sem proteção cronológica.

| Arquétipo | Onda 11 | Onda 12 | Onda 13 | Onda 14 |
|---|---:|---:|---:|---:|
| GRAND_STRATEGIST | 20/20 | 20/20 | 20/20 | 18/20 |
| SURVIVALIST | 20/20 | 20/20 | 20/20 | 19/20 |
| MERCHANT | 20/20 | 20/20 | 20/20 | 17/20 |
| SPEEDRUNNER | 0/20 | 0/20 | 0/20 | 0/20 |
| ROGUELIKE | 0/20 | 0/20 | 0/20 | 0/20 |
| ROLEPLAYER | 20/20 | 20/20 | 20/20 | 17/20 |
| EXPLORER | 3/20 | 2/20 | 1/20 | 0/20 |
| OPTIMIZER | 20/20 | 20/20 | 20/20 | 20/20 |
| COMPLETIONIST | 20/20 | 20/20 | 20/20 | 18/20 |
| CASUAL | 20/20 | 20/20 | 20/20 | 19/20 |

## Interpretação

A cauda rara produziu o efeito procurado no gate anterior: a conclusão deixou de ser virtualmente garantida para a maior parte dos perfis que antes faziam 20/20. GRAND_STRATEGIST, SURVIVALIST, MERCHANT, ROLEPLAYER, COMPLETIONIST e CASUAL agora apresentam dispersão entre seeds, enquanto OPTIMIZER permaneceu em 20/20. A taxa agregada caiu 6,5 pontos percentuais em relação à onda 13.

Os bloqueios por `INSUFFICIENT_PROVISIONS` chegaram a 168 ocorrências. Entre os perfis orientados por planejamento, as falhas finais por provisões foram raras, mas presentes: 1 em CASUAL e SURVIVALIST; 2 em GRAND_STRATEGIST e COMPLETIONIST; 3 em MERCHANT e ROLEPLAYER. Isso é compatível com a finalidade da v0.4: criar uma cauda de consequências que possa atravessar uma preparação normalmente suficiente sem tornar o fracasso dominante.

O risco estrutural também passa a alterar a condição final sem violar o timing histórico observado. Os mínimos de condição dos perfis que completam com alta frequência ficaram aproximadamente entre 33 e 40 pontos, ainda acima do limiar abstrato de partida de 20. Portanto, nesta bateria, a dimensão estrutural funciona principalmente como desgaste acumulado e não como principal causa de bloqueio.

EXPLORER caiu para 0/20 e SPEEDRUNNER e ROGUELIKE permanecem em 0/20. Esses três perfis continuam pouco informativos para calibração da faixa superior de dificuldade.

## Limitação metodológica identificada

A bateria atual preserva as mesmas seeds **entre ondas**, mas não usa as mesmas seeds **entre arquétipos**: cada política recebe uma faixa própria (`11001–11020`, `12001–12020`, ..., `20001–20020`). Isso é adequado para comparar cada arquétipo consigo mesmo ao longo das versões, mas impede atribuir com segurança diferenças entre arquétipos exclusivamente à política de jogo. Por exemplo, o 20/20 de OPTIMIZER não pode ser interpretado diretamente como superior ao 17/20 de MERCHANT, pois os dois grupos enfrentaram realizações estocásticas distintas.

Antes de qualquer nova recalibração de probabilidades ou severidade, o próximo gate deve executar um desenho pareado: **as mesmas 20 seeds para todos os dez arquétipos**, mantendo a v0.4 congelada. Isso permitirá separar efeito de política de efeito da amostra estocástica.

## Decisão do gate

A v0.4 deve ser preservada sem nova alteração de parâmetros neste momento. A onda 14 mostra que a cauda rara atingiu o objetivo mínimo de quebrar o 20/20 generalizado sem colapsar os perfis prudentes. O próximo passo não deve ser aumentar dificuldade, mas melhorar a identificação causal do playtest com uma bateria pareada por seed.
