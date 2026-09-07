# F1 — João da Nova 1501–1502 — auditoria da torna-viagem v0.1

Data: 2026-09-07
Issue: #120
Gate-mãe: #118

## Objetivo

Determinar até que ponto a torna-viagem de João da Nova em 1502 pode ser normalizada sem preencher lacunas documentais com cronologia inventada.

## 1. Marco firme em Cananor

A síntese da Comissão Portuguesa de História Militar registra a armada em Cananor em 30/12/1501, pronta para iniciar a torna-viagem, quando a esquadra de Calecute bloqueia a saída. O combate começa em 31/12/1501 e prossegue até **02/01/1502**, quando a força de Calecute abandona a perseguição.

Classificação:

- 30/12/1501 — início do bloqueio: `EXACT`, já normalizado como `NOVA1501_E03`;
- 31/12/1501 — início do rompimento/combate: `EXACT`, documental, mas não exige evento funcional separado neste gate;
- 02/01/1502 — término do bloqueio/combate: `EXACT`, suficientemente sustentado para evento documental específico;
- natureza do episódio — evento histórico específico; **não demonstra por si só necessidade de sistema geral de combate**.

## 2. Partida efetiva da Índia

A documentação disponível não permite tratar 02/01/1502 como data automática de partida transoceânica. A bibliografia especializada apresenta reconstruções distintas sobre as atividades posteriores em Cananor e o momento de saída, inclusive referência a partida somente no fim de fevereiro para não perder a monção.

Decisão: **UNRESOLVED** para a data operacional `CAN → retorno transoceânico`.

Nenhuma rota de retorno será criada a partir de 02/01 apenas por conveniência do motor.

## 3. Chegada ao reino

Correspondência mercantil contemporânea conservada por Marino Sanuto e editada no corpus documental sobre Ceilão registra que cartas de Lunardo Nardi e Bartolomeo Marchionni, datadas de 20/09/1502, tratam do retorno a Lisboa, em **12/09/1502**, das quatro naus de João da Nova que haviam partido em março de 1501.

A data fornece um bom **terminus ad quem / marco de chegada**, mas não resolve a sequência das escalas do retorno.

Classificação de trabalho:

- chegada das quatro naus a Lisboa em 12/09/1502 — `EXACT`, evidência contemporânea indireta;
- rota Cananor–Lisboa — `UNRESOLVED` no nível necessário para pernas jogáveis;
- duração total entre saída efetiva da Índia e Lisboa — não deve ser inferida enquanto a saída permanecer incerta.

Por prudência, a chegada ainda não é inserida em `expedition_routes.csv` nem em `voyage_observations.csv`.

## 4. Santa Helena e outras atribuições insulares

A atribuição tradicional da descoberta de Santa Helena a João da Nova em 1502 é controvertida. A própria EVE registra versões concorrentes e menciona a possibilidade de a descoberta pertencer a Estêvão da Gama em 1503.

Decisão:

- não criar `ST_HELENA` como nó de F1;
- não usar a ilha para fechar artificialmente a rota de retorno;
- preservar a controvérsia documental para pesquisa posterior;
- descobertas/atribuições insulares não são necessárias para cumprir o loop funcional mínimo de F1.

## 5. Consequência para o domínio

F1 não precisa de uma segunda campanha jogável de retorno neste estágio.

O recorte funcional defensável permanece:

`LIS → SBR → KIL → MAL → ANJ → CAN → COC → CAN`

seguido de:

- marco de bloqueio em 30/12/1501;
- resolução documental em 02/01/1502;
- retorno ao reino conhecido documentalmente, mas sem sequência operacional suficientemente fina para normalização em pernas.

Isso é consistente com o princípio do projeto: **ordem histórica conhecida não equivale a cronologia diária suficiente para uma rota guiada**.

## 6. Decisão de implementação

1. acrescentar `NOVA1502_E04` em `expedition_events.csv` para o término do bloqueio em 02/01/1502;
2. não acrescentar novas linhas a `expedition_routes.csv` ou `voyage_observations.csv` para a torna-viagem;
3. manter 12/09/1502 documentado como chegada ao reino nesta auditoria, sem forçar o schema operacional;
4. não materializar Santa Helena;
5. usar o fechamento em Cananor como limite funcional da campanha F1, desde que testes, persistência e regressão permaneçam verdes.

## Critério de saída do subgate

O subgate da torna-viagem pode ser considerado resolvido quando:

- `NOVA1502_E04` estiver validado;
- testes provarem que o evento só está disponível em 02/01/1502;
- nenhuma perna fictícia de retorno tiver sido criada;
- CI integral permanecer verde.

Se esses critérios forem atendidos, F1 poderá ser preparada para fechamento e PR, registrando explicitamente que a chegada a Lisboa é documentalmente conhecida, mas que o percurso de retorno permanece fora do loop jogável por insuficiência de cronologia operacional.