# Diagnóstico de `STRUCTURAL_STRAIN` — v0.5

## Objetivo

Verificar se a perda rara de condição criada por `STRUCTURAL_STRAIN` justifica uma nova mecânica de mitigação. O diagnóstico antecede qualquer mudança de probabilidade, severidade ou regra de preparação.

A regra de referência permanece em `simulation/voyage_event_rules.csv`: probabilidade `0.05`, perda de condição entre `8` e `14`, sem alteração de timing e com `observed_timing_safe=TRUE`.

## Evidência da onda 16

Nos 200 playtests pareados da onda 16:

- condição mínima global: `36,79`;
- sessões com condição mínima abaixo de `40`: `8/200`;
- sessões abaixo do limiar de partida `20`: `0/200`;
- blockers `VESSEL_CONDITION_TOO_LOW`: `0`;
- somente uma das oito sessões abaixo de `40` falhou, sem evidência de causalidade estrutural.

Isso não sustenta, por si só, a criação de uma segunda mitigação.

## Superfície controlada de estresse

A issue `#87` abriu um diagnóstico dirigido. O PR `#88` adicionou `tools/diagnose_structural_strain.py` e o workflow `.github/workflows/structural-strain-diagnostic-v05.yml`.

O ensaio usa `R_MAL_CAL`, partida em `1498-04-24`, com `preserve_observed_timing=True`, porque essa combinação mantém os 27 dias observados enquanto permite eventos de recurso marcados como seguros para o timing. Os níveis de condição inicial são cenários de estresse de `SIMULATION`, não estados históricos reconstruídos.

Foram executadas `10.000` seeds para cada condição inicial: `100`, `60`, `40`, `36,79`, `30` e `25`.

## Resultado

`STRUCTURAL_STRAIN` ocorreu em `499/10.000` seeds, ou `4,99%`, compatível com a probabilidade declarada de `5%`.

| Condição inicial | Eventos `STRUCTURAL_STRAIN` | Cruzamentos abaixo de 20 | Mínimo pós-evento |
|---:|---:|---:|---:|
| 100 | 499 | 0 | 80,62 |
| 60 | 499 | 0 | 40,62 |
| 40 | 499 | 0 | 20,62 |
| 36,79 | 499 | 231 | 17,41 |
| 30 | 499 | 499 | 10,62 |
| 25 | 499 | 499 | 5,62 |

Nenhum blocker `VESSEL_CONDITION_TOO_LOW` é criado na própria perna. O limiar é relevante para uma partida posterior. Portanto, o ensaio não mede sozinho o risco de encalhe de campanha; ele identifica a faixa de condição em que esse risco pode surgir.

## Interpretação

A superfície controlada mostra que `STRUCTURAL_STRAIN` não leva a condição abaixo do limiar quando a viagem começa com condição `>=40`. O risco de cruzamento aparece na faixa próxima a `36,79`, valor que já foi observado como mínimo na onda 16, e se torna sistemático em estados ainda mais degradados.

Isso justifica aprofundar o diagnóstico de campanha em pernas intermediárias, mas ainda não justifica manutenção preventiva, sobressalentes ou proteção estrutural específica. A próxima pergunta é causal: quando `STRUCTURAL_STRAIN` ocorre antes da última perna, ele produz blockers posteriores ou o sistema existente de reparos permite recuperação razoável?

## Decisão de gate

- manter `simulation/voyage_event_rules.csv` congelado;
- não introduzir mitigação estrutural neste momento;
- preservar a issue `#87` aberta para diagnóstico em trajetória completa;
- usar a instrumentação do PR `#88` como baseline reproduzível;
- considerar nova mecânica somente se houver concentração de derrotas inevitáveis ou becos sem saída entre políticas competentes.

PR `#88` foi integrado após CI completa verde. Commit de merge: `470e1fbb09826320fd643fd80eceafcafe114cc3`.
