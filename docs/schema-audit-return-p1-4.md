# P1.4 — Auditoria de schema para o retorno

Status: concluída no nível documental. Nenhuma alteração de código ou dados neste arquivo.

## Resultado

| Item | Estado | Diagnóstico |
|---|---|---|
| Camada de evidência | `SUPPORTED_WITH_NOTES` | `expedition_routes.csv`, `expedition_stops.csv`, `routes.csv` e `voyage_observations.csv` já possuem `evidence_grade`, `evidence_scope`, `source_id` e `notes`. Não existe campo explícito `source_layer`, mas a distinção `PRIMARY_NARRATIVE`/`EDITORIAL_SYNTHESIS` pode ser inicialmente codificada em `evidence_scope` ou em um valor controlado novo desse campo, sem mudar schema. |
| Datas alternativas / intervalos | `SCHEMA_GAP` | `expedition_stops.csv` e `voyage_observations.csv` usam uma única `arrival_date`/`departure_date`. Não há estrutura para variantes 29/08, 08/09 e 18/09 nem para `before 1499-08-28` sem escolher arbitrariamente uma data. |
| Redução da frota | `SCHEMA_GAP` | `ExpeditionLeg` contém somente expedição, sequência, rota, período e `command_basis`; não há composição de frota por perna. O evento histórico da queima do S. Rafael não cabe como estado estrutural da expedição. |
| Mudança de comando | `SCHEMA_GAP` | o modelo de expedição não possui embarcação nem comandante por perna. João de Sá assumir o S. Gabriel não pode ser representado estruturalmente. |
| Trajetória do personagem separada do navio | `SCHEMA_GAP` | o domínio atual autoriza pernas da expedição, mas não modela uma trajetória própria do personagem que se separe da embarcação. O trecho São Tiago → Terceira de Vasco/Paulo e o S. Gabriel → Lisboa sob João de Sá exigem representação adicional ou fechamento narrativo específico. |
| Nó náutico sem mercado/serviço | `SUPPORTED` | `nodes.csv` já representa `NAVIGATION_POINT`, `ANCHORAGE` e `RIVER_ANCHORAGE`, com `market_scale=NONE` e serviços `NONE/UNKNOWN`. CGH, SHB, SBR, RCO e RBS demonstram que BSR/SJO/Rio Grande podem ser representados sem mercado inventado. |
| Parada ritual / sondagem sem nó operacional pleno | `SUPPORTED_WITH_NOTES` | `voyage_observations.csv` exige `departure_node` e `arrival_node`, portanto uma observação de viagem ainda depende de nós; porém eventos/paradas muito curtos podem permanecer em `notes`/evidência da rota se não houver necessidade mecânica. Não é obrigatório materializar SMI/SJO imediatamente. |
| Isolamento do MVP | `SUPPORTED` | a expansão pode ser adicionada depois da sequência 10 da expedição ou em uma nova camada/campanha sem alterar as pernas existentes Lisboa–Calecute. |

## Achado adicional de integridade

O identificador provisório `RGR` não pode ser usado para os Baixos do Rio Grande: `nodes.csv` já usa `RGR` para **Ribeira Grande de Santiago / Cidade Velha**. Qualquer novo nó deverá usar outro ID, por exemplo `BRG` ou outro identificador aprovado no gate de dados.

## Consequência técnica

Há três lacunas estruturais reais e relacionadas:

1. datas incertas/variantes;
2. composição/comando da frota por trecho;
3. trajetória de personagem independente da embarcação.

Não convém resolver as três com uma grande refatoração antes de saber qual delas é necessária para o primeiro incremento jogável do retorno.

A proposta mínima é dividir a implementação:

### Gate A — retorno até os Baixos do Rio Grande

Pode ser implementado com o schema atual, desde que:

- as novas pernas usem apenas datas suficientemente seguras ou editoriais já explicitadas;
- a queima do S. Rafael seja inicialmente um evento histórico específico registrado em stop/event history, sem pretender atualizar uma frota estrutural que o domínio ainda não representa;
- SMI/SJO permaneçam opcionais como nós se não forem necessários à jogabilidade;
- ANJ seja o principal novo nó logístico.

### Gate B — fechamento pós-Rio Grande

Exige decisão de schema antes da implementação, porque as trajetórias se separam e as datas entram em conflito.

## Issue técnica recomendada

Abrir uma issue pequena e separada para decidir a representação mínima de `uncertain_date` e `split_trajectory`, sem misturar isso com a inserção dos dados históricos do retorno até 25/04/1499.

A regra permanece: somente `SCHEMA_GAP` justifica alteração estrutural; os demais casos devem reutilizar o modelo atual.