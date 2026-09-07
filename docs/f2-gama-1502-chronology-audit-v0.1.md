# F2 — Vasco da Gama 1502–1503 — auditoria cronológica v0.1

Data: 2026-09-07
Issue: #122
Baseline: `24b6de7799f3ebb40c9a3401a73ddb5913d1190f`

## Objetivo

Classificar o grau de resolução cronológica do recorte funcional mínimo de `EXP_GAMA_1502` antes de normalizar novas pernas. A classificação não converte referências mensais em datas diárias e não usa timing de simulação como evidência histórica.

## Regra de classificação

- `EXACT`: data diária diretamente sustentada pela documentação consolidada.
- `INTERVAL`: sequência/localização sustentada, mas apenas dentro de mês, faixa ou período.
- `DERIVED`: marco obtido por inferência explícita a partir de evidência documental; não equivale a testemunho independente.
- `UNRESOLVED`: evidência atual insuficiente para fixar o marco necessário sem interpolação silenciosa.

## Auditoria

| Marco/perna | Classificação | Evidência atualmente consolidada | Decisão funcional |
|---|---|---|---|
| partida de Lisboa | `INTERVAL` | matriz #113 registra fevereiro de 1502; documentação da composição registra a partida principal em 01/02/1502, mas a ficha consolidada ainda mistura formulação mensal e diária e deve ser reconciliada antes de promover a data a `EXACT` | preservar 1502 e não criar observação diária até reconciliar a fonte primária/secundária citada |
| `LIS → SOF` | `INTERVAL` | chegada a Sofala em junho de 1502; sequência documental firme | perna candidata à normalização, sem chegada diária inventada |
| `SOF → KIL` | `INTERVAL` | Quiloa/Kilwa em julho de 1502, após Sofala | perna candidata à normalização, sem chegada/partida diária inventada |
| `KIL → Malabar` | `INTERVAL` | chegada à zona de Cananor em setembro de 1502; não há, no material consolidado, resolução suficiente das escalas intermediárias para uma sequência diária | normalizar apenas o destino operacional comprovado; não materializar Melinde por analogia |
| chegada/atuação em Cananor | `INTERVAL` | zona de Cananor em setembro de 1502 | `CAN` é âncora operacional defensável; data diária permanece aberta |
| reorganização da feitoria de Cochim | `INTERVAL` | evento já normalizado em `GAMA1502_E01`, janela 1502-11-01 a 1502-12-31 | manter como evento institucional temporal, sem alterar soberania |
| reorganização da feitoria de Cananor | `INTERVAL` | evento já normalizado em `GAMA1502_E02`, janela 1502-11-01 a 1502-12-31 | manter como evento institucional temporal, sem fortificação retroativa |
| bombardeio/bloqueio de Calecute | `INTERVAL` | ocorrência e sequência sustentadas; cronologia fina ainda não consolidada no gate | evento histórico específico; não criar combate geral nem perna comercial para `CAL` por inferência |
| separação/permanência de Vicente Sodré | `INTERVAL` | `GAMA1502_E03` registra `FORCE_REMAINS` entre 1503-01-01 e 1503-03-31 | suficiente para testar subcampanha/força residente; insuficiente para fixar dia de separação |
| retorno de Vasco da Gama | `UNRESOLVED` | a matriz #113 identifica explicitamente como pendência reconstruir com maior precisão a torna-viagem | não criar `EXP_GAMA_RETURN_1503` nem pernas de retorno nesta etapa |
| desvio posterior de Sodré para o Mar Vermelho | `UNRESOLVED` para cronologia funcional fina | fato e distinção missão/decisão estão documentados, mas o recorte atual não fixa cronologia operacional suficiente | preservar como requisito futuro de world-state; não inventar rota/data nesta etapa |

## Sequência mínima defensável nesta etapa

A sequência funcional que passa o gate documental atual é:

`LIS → SOF → KIL → CAN`

Cochim deve entrar como escala/estado operacional apenas quando a ordem entre Cananor, Cochim e os episódios de Calecute estiver suficientemente reconciliada para não transformar uma cronologia parcial em itinerário diário fictício.

## Decisões de modelagem

1. Não promover a partida a `EXACT` antes de reconciliar a aparente diferença entre a formulação “fevereiro de 1502” e o registro 01/02/1502 na documentação consolidada.
2. Não introduzir Melinde como escala observada por analogia com 1498, 1500 ou 1501.
3. Não transformar Calecute em escala comercial normal: bloqueio/bombardeio permanecem eventos específicos.
4. Não criar ainda `EXP_GAMA_RETURN_1503`; a torna-viagem é uma pendência documental expressa de #113.
5. `EXP_SODRE_1503` pode ser preparado como subcampanha somente até o grau necessário para testar a persistência de uma força residente não controlada.
6. A arquitetura de um único `active_expedition_id` continua suficiente até prova funcional em contrário.

## Próximo gate

Normalizar somente as pernas `LIS → SOF → KIL → CAN` com notas explícitas de precisão, verificar se as rotas correspondentes já existem em `routes.csv` e, em seguida, implementar um smoke mínimo de `EXP_GAMA_1502`. A expansão para Cochim, retorno e subcampanha de Sodré depende de novos gates de evidência/arquitetura, não de interpolação.