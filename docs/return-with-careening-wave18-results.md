# P1-func — controle pareado wave18 com carena mínima

Issues: #99, #101.

Run: `34116258033`.
Commit: `6977a7ed4dabc8652f67fca12f7bde511583ba86`.

## Desenho

Repete exatamente os cinco arquétipos e quatro seeds da wave17. A única mudança é aplicar, quando disponível na permanência documental de Anjediva, uma ação explícita de carena com restauração de **2 pontos abstratos de condição**, valor mínimo selecionado pela sensibilidade `0/1/2/5/10`.

Nenhuma outra regra foi alterada: desgaste por viagem, probabilidades e severidades de eventos, limiar de condição, provisões, cronologia e dados históricos permanecem congelados.

## Resultado

- casos totais: **20**;
- MVP concluído: **18/20**;
- retorno concluído entre elegíveis: **17/18 (94,4%)**;
- blockers estruturais: **0**;
- blocker residual: **1 `INSUFFICIENT_PROVISIONS`**, no estado GRAND_STRATEGIST/seed `23002`, ainda em Calecute.

Por arquétipo:

| Arquétipo | MVP concluído | Retorno concluído |
|---|---:|---:|
| GRAND_STRATEGIST | 4/4 | 3/4 |
| SURVIVALIST | 4/4 | 4/4 |
| MERCHANT | 3/4 | 3/3 |
| ROLEPLAYER | 3/4 | 3/3 |
| COMPLETIONIST | 4/4 | 4/4 |

## Interpretação

A intervenção elimina exclusivamente os cinco blockers `VESSEL_CONDITION_TOO_LOW` observados na wave17. Isso sustenta a interpretação de que a carena documentada em Anjediva oferece uma decisão de agência historicamente ancorada, enquanto os 2 pontos são apenas a menor projeção de `SIMULATION` suficiente no painel testado.

O único caso restante confirma que a lacuna Calecute→Anjediva é independente da condição estrutural. Ele parte de condição `59,85`, mas possui apenas `19,366` dias-equivalentes para uma perna agregada de 21 dias.

## Decisão

A #101 pode ser encerrada. A #99 permanece aberta apenas por problemas independentes ainda não resolvidos, principalmente a agência logística no primeiro trecho do retorno e a futura exposição do retorno na interface jogável.

A solução logística não deve ser feita por provisões automáticas em Calecute. A pesquisa da #100 já encontrou compra/oferta de peixe durante a navegação em 11/09 e nos Ilhéus de Santa Maria em 15/09, justificando reexaminar a segmentação `CAL→SMI→ANJ` antes de qualquer alteração quantitativa.