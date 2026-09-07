# P3 wave20 — playtests por arquétipos até Cananor

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`
Workflow: `.github/workflows/p3-archetypes-wave20.yml`
Run: `34138068399`

## Desenho

A wave20 executou 220 sessões pareadas nas seeds `24001–24020`:

- 10 arquétipos fixos × 20 sessões = 200 sessões;
- `RANDOM_PER_LEG` × 20 sessões = 20 sessões adicionais.

`RANDOM_PER_LEG` sorteia, com reposição, um dos dez arquétipos no início de cada perna alcançada. O sorteio usa fluxo pseudoaleatório separado da seed utilizada pelo motor de risco/viagem, de modo que a sequência de políticas é reproduzível sem alterar o pareamento dos eventos marítimos. Cada JSON registra `archetype_sequence` e `archetype_switches`.

## Resultado agregado

- sessões: `220`;
- conclusões até Cananor: `0`;
- taxa de conclusão: `0%`;
- todos os 11 grupos tiveram `0/20` conclusões.

Principais blockers agregados:

1. `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`: 416;
2. `INSUFFICIENT_PROVISIONS`: 240;
3. `ONBOARD_PROVISION_CAP_REACHED`: 153;
4. `HISTORICAL_DEPARTURE_NOT_REACHED`: 20;
5. `HISTORICAL_STOP_NOT_RELEASED`: 20.

O grupo `RANDOM_PER_LEG` também teve `0/20` conclusões; mediana de `1` troca de arquétipo antes do bloqueio, porque as sessões não alcançam número suficiente de pernas para produzir mistura longa de políticas.

## Interpretação

A wave20 não deve ser usada ainda para ranquear arquétipos. O resultado demonstra um bloqueio estrutural anterior à diferenciação comportamental.

A sequência operacional atualmente contém `LIS→VCR` seguida por `VCR→MOZ` agregada. Vera Cruz não possui serviço histórico genérico de reprovisionamento e a capacidade máxima de provisões embarcadas impede que as políticas competentes carreguem em Lisboa recursos suficientes para absorver a primeira travessia, a permanência em Vera Cruz e a perna agregada de 79 dias até Moçambique.

O fato de GRAND_STRATEGIST, SURVIVALIST, COMPLETIONIST e demais perfis orientados à preparação falharem juntamente com SPEEDRUNNER/ROGUELIKE indica que o problema não é escolha subótima do jogador. É uma incompatibilidade entre:

- o recorte operacional agregado `VCR→MOZ`;
- a ausência deliberada de abastecimento genérico em Vera Cruz;
- o limite atual de provisões a bordo;
- e o horizonte logístico necessário à campanha de Cabral.

## Regra de continuidade

Não aumentar a capacidade de provisões, inventar abastecimento em Vera Cruz ou reduzir arbitrariamente a duração histórica para obter conclusões.

O próximo gate deve investigar, nesta ordem:

1. se a documentação de Cabral sustenta pontos intermediários de abastecimento/reabastecimento entre Vera Cruz e Moçambique que foram agregados fora do loop;
2. se o modelo de provisões usado no MVP representa adequadamente uma armada maior e uma viagem longa de 1500, ou se `capacity/provision_days` precisa distinguir escala da frota de capacidade abstrata do navio representativo;
3. se a perna `VCR→MOZ` deve ser segmentada por pontos documentais sem transformar marcos náuticos em portos fictícios;
4. somente depois, se existe necessidade demonstrada de calibrar parâmetros de simulação.

A wave20 deve ser preservada como baseline diagnóstico de `0/220`, não descartada. Após resolver o blocker estrutural por uma solução historicamente/arquiteturalmente defensável, a mesma matriz de 11 grupos e as mesmas seeds `24001–24020` deve ser repetida para comparação pareada.

## Artefatos

O workflow gerou:

- `p3-archetypes-wave20.csv`;
- `p3-archetypes-wave20-summary.json`;
- `p3-archetypes-wave20-paired.csv`;
- artefatos individuais para cada um dos 11 grupos.

Artifact agregado do run: `10024779381`.
