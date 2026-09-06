# Playtest sintético — onda 1

Data: 2026-09-06

Workflow: `Synthetic MVP playtest`, run `34010942622`.

Amostra: 20 sessões independentes em runners isolados, cinco perfis comportamentais com quatro seeds por perfil. Os jobs fizeram checkout limpo, instalaram o projeto e executaram uma campanha nova sem compartilhar estado.

## Resultado agregado

- sessões: 20;
- conclusões: 0/20 (0%);
- sessões que entraram em `COUNTERFACTUAL`: 20/20 (100%);
- sessões com ao menos um bloqueio: 20/20;
- sessões que executaram alguma ação válida depois do primeiro bloqueio: 19/20;
- ações tentadas: mediana 13,5; média 15,15; intervalo 9–32;
- bloqueios: mediana 4,5; média 4,5; máximo 7;
- duração simulada: mediana 127 dias; média 139,45; intervalo 120–208;
- capital final: 100 em todas as sessões, pois nenhuma alcançou a fase comercial;
- menor provisão observada: 0;
- menor condição observada: 54,47.

Bloqueios mais frequentes:

1. `INSUFFICIENT_PROVISIONS`: 51 ocorrências;
2. `SERVICE_AVAILABILITY_UNKNOWN`: 21;
3. `SERVICE_UNAVAILABLE`: 13;
4. `NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED`: 5;
5. `HISTORICAL_DEPARTURE_NOT_REACHED`: 4;
6. `HISTORICAL_STOP_NOT_RELEASED`: 4.

## Resultado por perfil

| Perfil | n | Conclusão | Mediana ações | Mediana bloqueios | Mediana reabastecimentos | COUNTERFACTUAL |
|---|---:|---:|---:|---:|---:|---:|
| CAUTIOUS | 4 | 0% | 15,5 | 3,5 | 4,0 | 4/4 |
| DISCIPLINED | 4 | 0% | 17,5 | 5,0 | 3,5 | 4/4 |
| FRUGAL | 4 | 0% | 16,5 | 4,5 | 3,0 | 4/4 |
| IMPATIENT | 4 | 0% | 13,0 | 5,0 | 2,0 | 4/4 |
| TRADER | 4 | 0% | 11,0 | 4,0 | 2,0 | 4/4 |

## Leitura técnica

O resultado não contradiz o gate M7, no qual a trajetória canônica `GUIDED` chega a Calecute. A diferença é comportamental: o teste M7 prepara provisões nos momentos necessários antes da liberação histórica; os jogadores sintéticos da onda 1 decidem com heurísticas genéricas de estoque.

O padrão dominante observado foi:

`chegada à escala → espera/liberação histórica → tentativa de próxima perna → provisões insuficientes → reabastecimento tardio → partida depois da data histórica → COUNTERFACTUAL`.

A partir da divergência, os eventos de simulação passam a incidir e aumentam a variabilidade de provisões, condição e duração. A recuperação local é alta — 19 jogadores fizeram alguma ação válida após o primeiro bloqueio — mas a recuperação global da campanha foi nula.

Isso sugere uma lacuna de orientação operacional no MVP: a campanha é vencível quando o jogador sabe antecipadamente quanto preparar antes de cada partida, mas políticas genéricas plausíveis não descobrem essa necessidade a tempo. O ponto mais crítico não é um crash nem corrupção de estado; é a combinação entre calendário histórico rígido, planejamento de viagem e decisão de reabastecimento.

## Hipótese a testar em seguida

Antes de alterar balanceamento, convém testar uma onda 2 em que os agentes possam consultar, antes de esperar pela data de partida, a viabilidade da próxima perna e seus bloqueios sem efetivamente partir. Se essa informação já for acessível pela interface, o runner deve ser adaptado para utilizá-la; se não for, isso constitui candidato claro a melhoria de interface.

A onda 1 deve ser preservada como baseline de descoberta não assistida.

## Limitação metodológica

Estes resultados medem robustez sistêmica sob políticas sintéticas, não experiência humana. Não permitem inferir diversão, compreensão visual, frustração percebida ou probabilidade real de abandono por pessoas.
