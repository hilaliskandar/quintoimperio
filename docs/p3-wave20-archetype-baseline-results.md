# P3 wave20 — playtests por arquétipos até Cananor

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`
Workflow: `.github/workflows/p3-archetypes-wave20.yml`
Baseline original: run `34138068399`
Baseline corrigido: run `34143322113`
Commit funcional validado: `3333de41002ca314dc018b6edae0b5afa625c17a`
CI integral validada: run `34143322093`

## Desenho

A wave20 executa 220 sessões pareadas nas seeds `24001–24020`:

- 10 arquétipos fixos × 20 sessões = 200 sessões;
- `RANDOM_PER_LEG` × 20 sessões = 20 sessões adicionais.

`RANDOM_PER_LEG` sorteia, com reposição, um dos dez arquétipos no início de cada perna alcançada. O sorteio usa fluxo pseudoaleatório separado da seed utilizada pelo motor de risco/viagem, preservando o pareamento dos eventos marítimos. Cada JSON registra `archetype_sequence` e `archetype_switches`.

## Baseline original — diagnóstico estrutural

O run `34138068399` produziu `0/220` conclusões. Esse resultado foi preservado como baseline diagnóstico e levou à investigação do runner, da capacidade abstrata de provisões e das oportunidades documentadas de abastecimento.

O diagnóstico mostrou que o resultado não representava a dificuldade real da campanha. O runner esperava um blocker da perna corrente antes de usar uma oportunidade documental e, em outros caminhos, tentava serviço genérico onde a expedição dispunha de ação material específica. Também havia tentativas redundantes de serviço sem mudança de estado.

## Correções aplicadas

A correção foi deliberadamente restrita ao comportamento do runner e à telemetria. Não foram recalibrados os valores documentais nem reduzidas durações históricas.

1. O planejamento P3 passou a usar horizonte logístico e margem da política para decidir se deve aproveitar uma oportunidade documental antes de a perna ficar bloqueada.
2. O piso preventivo passou a reconhecer a ação documental específica da escala.
3. Quando Cabral já está no teto específico de provisões, o runner não tenta uma reposição impossível apenas porque a recomendação excede a capacidade.
4. Tentativas genéricas determinísticas são deduplicadas dentro da mesma perna/estado.
5. Depois de consumida a ação documental one-shot de Cabral numa escala, o runner não tenta um segundo serviço genérico sem evidência histórica apenas para completar a margem desejada.

Parâmetros preservados:

- Vera Cruz: `+5` dias-equivalentes;
- Moçambique: `+10`;
- Melinde: `+15`;
- teto específico da expedição de Cabral: `150`;
- teto genérico do MVP: `120`.

## Baseline corrigido

O run `34143322113`, com as mesmas 220 sessões e as mesmas seeds, produziu:

- conclusões: `144/220`;
- taxa de conclusão: `65,45%`.

Por grupo:

| Arquétipo | Conclusões |
|---|---:|
| SURVIVALIST | 19/20 |
| COMPLETIONIST | 18/20 |
| GRAND_STRATEGIST | 16/20 |
| MERCHANT | 16/20 |
| OPTIMIZER | 16/20 |
| INTERPRETIVE | 16/20 |
| CASUAL | 16/20 |
| EXPLORER | 15/20 |
| RANDOM_PER_LEG | 12/20 |
| ROGUELIKE | 0/20 |
| SPEEDRUNNER | 0/20 |

A diferenciação é agora substantiva. Políticas que consultam e seguem o horizonte logístico têm maior robustez; o Explorador se beneficia do piso preventivo, mas continua menos robusto por não seguir a margem recomendada; Roguelike e Speedrunner permanecem incapazes de concluir a campanha neste recorte.

A seed `24019` permanece sem conclusão por qualquer arquétipo. As seeds `24001`, `24002` e `24010` distinguem políticas com reservas/margens maiores. A auditoria dessas seeds mostrou perdas adversas de provisões compatíveis com a cauda estocástica dos eventos, e não perda de uma oportunidade documental pelo runner.

## Auditoria de telemetria

A investigação reduziu `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE` de `1.918` ocorrências intermediárias para `723` no estado final, sem alterar a regra epistêmica: a primeira tentativa real de serviço genérico sem evidência continua bloqueada.

No estado final, essas 723 tentativas estão somente em nós sem ação documental específica de abastecimento no modelo:

- KIL: `176`;
- ANJ: `206`;
- CAL: `171`;
- COC: `170`;
- MOZ: `0`;
- MAL: `0`.

Não restam estados falhos idênticos repetidos. `ONBOARD_PROVISION_CAP_REACHED`, que aparecia artificialmente 153 vezes, caiu para zero sem mudar a taxa de conclusão.

## Validação

O commit funcional `3333de41002ca314dc018b6edae0b5afa625c17a` passou nos três gates:

1. wave20 corrigida: `144/220`;
2. diagnóstico genérico: 723 tentativas válidas, nenhuma repetição idêntica e nenhuma tentativa genérica em MOZ/MAL após consumo da ação documental;
3. CI `34143322093`: validação de dados, testes de domínio e todos os smoke tests concluídos com sucesso.

## Interpretação e regra de continuidade

O blocker estrutural de `0/220` está resolvido. A configuração corrigida passa a ser a baseline operacional da wave20; o run original permanece como evidência do defeito diagnosticado.

Não há evidência, neste gate, para aumentar novamente provisões, alterar os valores `VCR/MOZ/MAL`, ampliar o teto de Cabral ou introduzir serviço genérico nos nós sem documentação.

O próximo gate é qualitativo: analisar sucessos e falhas por arquétipo e seed, identificar quais decisões e eventos explicam a diferença de robustez e verificar se existe algum comportamento anômalo remanescente antes de expandir o P3.

## Artefatos

O workflow gera:

- `p3-archetypes-wave20.csv`;
- `p3-archetypes-wave20-summary.json`;
- `p3-archetypes-wave20-paired.csv`;
- artefatos individuais para cada um dos 11 grupos.

O diagnóstico de serviços genéricos é mantido em `.github/workflows/p3-generic-reprovision-diagnostic.yml` como controle de regressão da telemetria.