# F2 — Vasco da Gama 1502–1503 — auditoria cronológica v0.1

Data: 2026-09-08
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
| partida de Lisboa | `EXACT` | matriz #113 registra a partida principal em 01/02/1502 sob Vasco da Gama; a formulação resumida “fevereiro de 1502” não constitui evidência divergente | preservar 01/02/1502 como âncora diária da campanha, sem inferir a partir dela durações das pernas seguintes |
| partida da componente de Estêvão da Gama | `EXACT` | matriz #113 registra 01/04/1502 | manter como formação subordinada/reforço documental até necessidade funcional de subexpedição própria |
| `LIS → SOF` | `INTERVAL` com partida `EXACT` | partida em 01/02/1502 e chegada a Sofala em junho de 1502 | perna candidata à normalização, sem chegada diária inventada e sem `observed_days` histórico |
| `SOF → KIL` | `INTERVAL` | Quiloa/Kilwa em julho de 1502, após Sofala | perna candidata à normalização, sem chegada/partida diária inventada |
| `KIL → Malabar` | `INTERVAL` | chegada à zona de Cananor em setembro de 1502; não há, no material consolidado, resolução suficiente das escalas intermediárias para uma sequência diária | normalizar apenas o destino operacional comprovado; não materializar Melinde por analogia |
| chegada/atuação em Cananor | `INTERVAL` | zona de Cananor em setembro de 1502 | `CAN` é âncora operacional defensável; data diária permanece aberta |
| reorganização da feitoria de Cochim | `INTERVAL` | evento já normalizado em `GAMA1502_E01`, janela 1502-11-01 a 1502-12-31 | manter como evento institucional temporal, sem alterar soberania |
| reorganização da feitoria de Cananor | `INTERVAL` | evento já normalizado em `GAMA1502_E02`, janela 1502-11-01 a 1502-12-31 | manter como evento institucional temporal, sem fortificação retroativa |
| bombardeio/bloqueio de Calecute | `INTERVAL` | ocorrência e sequência sustentadas; cronologia fina ainda não consolidada no gate | evento histórico específico; não criar combate geral nem perna comercial para `CAL` por inferência |
| separação/permanência de Vicente Sodré | `INTERVAL` quanto ao estado resultante; `UNRESOLVED` quanto ao dia da separação | `GAMA1502_E03` registra `FORCE_REMAINS` entre 1503-01-01 e 1503-03-31 | suficiente para testar world-state/força residente; insuficiente para fixar data de bifurcação |
| retorno de Vasco da Gama | `UNRESOLVED` | a matriz #113 identifica explicitamente como pendência reconstruir com maior precisão a torna-viagem | não criar `EXP_GAMA_RETURN_1503` nem pernas de retorno nesta etapa |
| desvio posterior de Sodré para o Mar Vermelho | `UNRESOLVED` para cronologia funcional fina | fato e distinção missão/decisão estão documentados, mas o recorte atual não fixa cronologia operacional suficiente | preservar como requisito futuro de world-state; não inventar rota/data nesta etapa |

## Sequência mínima defensável nesta etapa

A sequência funcional que passa o gate documental atual é:

`LIS → SOF → KIL → CAN`

Cochim deve entrar como escala/estado operacional apenas quando a ordem entre Cananor, Cochim e os episódios de Calecute estiver suficientemente reconciliada para não transformar uma cronologia parcial em itinerário diário fictício.

## Auditoria preliminar de `routes.csv`

- `R_SOF_KIL` já existe como conexão costeira da rede suaíli preexistente. Ela pode ser reutilizada se o período for estendido de forma documentalmente justificada para 1502; não se deve duplicar a aresta apenas para torná-la “portuguesa”.
- não foi localizada aresta executável específica `LIS → SOF` no baseline;
- não foi localizada aresta agregada `KIL → CAN` no baseline;
- a conectividade Cananor–Cochim existe no domínio herdado de F1, mas não deve ser promovida automaticamente à sequência de Gama sem fechar a ordem operacional de 1502;
- `voyage_observations.csv` não contém observações de Gama 1502 e deve permanecer assim enquanto não houver datas de partida e chegada suficientes para duração histórica defensável.

## Decisões de modelagem

1. Preservar 01/02/1502 como `EXACT` para a partida principal; não usar essa precisão isolada para fabricar datas posteriores.
2. Não introduzir Melinde como escala observada por analogia com 1498, 1500 ou 1501.
3. Não transformar Calecute em escala comercial normal: bloqueio/bombardeio permanecem eventos específicos.
4. Não criar ainda `EXP_GAMA_RETURN_1503`; a torna-viagem é uma pendência documental expressa de #113.
5. Não criar ainda `EXP_SODRE_1503` como campanha jogável. Primeiro testar se `expedition_events` e estado temporal do mundo representam adequadamente a força não controlada.
6. A arquitetura de um único `active_expedition_id` continua suficiente até prova funcional em contrário.
7. Não adicionar linhas a `voyage_observations.csv` com datas escolhidas dentro de meses documentados.

## Próximo gate

Preparar a normalização mínima de `LIS → SOF → KIL → CAN`: criar apenas as arestas ausentes indispensáveis, reutilizar a rede preexistente quando semanticamente correta, registrar explicitamente que timing não observado é parâmetro de simulação e implementar smoke mínimo de `EXP_GAMA_1502`. A expansão para Cochim, retorno e subcampanha de Sodré depende de gates posteriores de evidência/arquitetura.