# Diagnóstico de campanha — STRUCTURAL_STRAIN v0.6

## Objetivo

Verificar se `STRUCTURAL_STRAIN` produz becos sem saída ou derrotas inevitáveis por condição do navio ao longo da campanha Lisboa–Calecute antes de acrescentar qualquer mecânica de mitigação estrutural.

Nenhuma regra de `simulation/voyage_event_rules.csv` foi alterada. O teste utiliza apenas instrumentação diagnóstica.

## Desenho

Foram executadas 7.000 campanhas: sete arquétipos competentes × 1.000 seeds pareadas (`30001–31000`). Os perfis foram `GRAND_STRATEGIST`, `SURVIVALIST`, `MERCHANT`, `ROLEPLAYER`, `OPTIMIZER`, `COMPLETIONIST` e `CASUAL`.

A instrumentação registra a resolução tardia real do evento, isto é, compara `voyage_event_history` antes e depois da execução da perna. Isso é necessário porque o planejamento não antecipa ao jogador o evento sorteado.

Para cada ocorrência de `STRUCTURAL_STRAIN` foram registrados rota, condição antes e depois, perda estrutural do evento e presença de `VESSEL_CONDITION_TOO_LOW` na próxima perna.

## Resultados

- campanhas: `7.000`;
- campanhas que chegaram a Calecute: `6.624`;
- campanhas com pelo menos um `STRUCTURAL_STRAIN`: `2.597`;
- ocorrências de `STRUCTURAL_STRAIN`: `3.274`;
- condição mínima observada em qualquer campanha: `21,8817`;
- ocorrências que terminaram abaixo de condição `40`: `185`;
- ocorrências que terminaram abaixo de condição `20`: `0`;
- bloqueios `VESSEL_CONDITION_TOO_LOW` na perna seguinte: `0`.

Por arquétipo, a condição mínima foi a mesma (`21,8817`) e nenhum dos sete perfis apresentou blocker por condição. A diferença de chegada a Calecute permaneceu associada às políticas e às outras contingências já conhecidas, não a um bloqueio estrutural observado neste teste.

A maior concentração de eventos que deixam o navio abaixo de condição 40 ocorreu na perna `R_MAL_CAL`: 130 de 372 ocorrências nessa rota. Mesmo assim, essa é a perna terminal do recorte e nenhuma ocorrência cruzou o limiar 20. Em pernas intermediárias também não houve cruzamento de 20 nem blocker subsequente por condição.

## Interpretação

O diagnóstico dirigido não sustenta a criação de manutenção preventiva, sobressalentes ou proteção específica contra `STRUCTURAL_STRAIN` neste estágio. O evento introduz variância e desgaste, mas, na distribuição atual e nas políticas competentes testadas, não gera o tipo de derrota estocástica inevitável que justificou a reserva segregada de provisões.

A decisão de design é preservar `STRUCTURAL_STRAIN` com probabilidade e severidade atuais e não adicionar mitigação estrutural enquanto não surgir evidência de problema de agência.

## Controle metodológico

A primeira execução do script revelou um erro de instrumentação: perfis sem reserva segregada apareciam sem eventos porque o diagnóstico lia o plano pré-resolução, enquanto eventos são resolvidos somente na execução. O script foi corrigido para ler os novos itens de `voyage_event_history`. Também se substituiu `CampaignProgress.completed` por chegada física a `CAL` como indicador auxiliar, pois o diagnóstico não executa o pós-chegada comercial completo.

Somente a execução corrigida deve ser utilizada como evidência.

## Rastreabilidade

- issue `#87`;
- ferramenta: `tools/diagnose_structural_strain_campaign.py`;
- workflow: `.github/workflows/structural-strain-campaign-v06.yml`;
- run corrigido: `34107964442`;
- artefato: `structural-strain-campaign-v06`, ID `10013165888`.
