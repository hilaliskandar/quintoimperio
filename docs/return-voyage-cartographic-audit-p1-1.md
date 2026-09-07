# P1.1 — Auditoria cartográfica dos candidatos do retorno, 1498–1499

Status: gate documental/cartográfico. Nenhuma coordenada desta nota deve ser incorporada a `data/nodes.csv` sem revisão final do P1.

Issue: #92.

## Critério

A classificação abaixo distingue: (a) identificação moderna suficientemente estável; (b) localização aproximada sustentada por rota/descrição, mas sem ponto moderno inequívoco; e (c) referência náutica histórica que não deve ser convertida em porto ou mercado.

Escala de confiança:

- `HIGH`: identificação moderna direta e estável;
- `MEDIUM`: identificação provável, mas ponto exato ou extensão espacial ainda discutível;
- `LOW`: apenas zona/feição aproximada; não autoriza coordenada pontual precisa.

## Resultado

| ID | Nome histórico | Identificação moderna de trabalho | Tipo recomendado | Confiança | Observação |
|---|---|---|---|---|---|
| SMI | Ilhéus de Santa Maria | arquipélago/ilhéus a oeste da costa do Malabar, tradicionalmente associados às Laquedivas/Lakshadweep | `NAVIGATION_ONLY` / marco náutico | `MEDIUM` | O `Roteiro` registra passagem e padrão; não há base para mercado ou escala logística plena. A identificação regional é consistente, mas o ilhéu exato não deve ser fixado sem fonte cartográfica especializada. |
| ANJ | Anjediva / Angediva | Anjadip (Anjediva) Island, costa de Karnataka/Goa | `ANCHORAGE_CONTACT` / escala logística | `HIGH` | Identificação moderna estável. O retorno documenta permanência, água, madeira, alimento e carena. Forte candidato a nó operacional. |
| BSR | Baixos de São Rafael | baixios na costa da África Oriental, no corredor entre Melinde/Mombaça e Zanzibar; tradição posterior associa o nome ao local em que a nau S. Rafael foi abandonada/queimada | `NAVIGATION_ONLY` + evento de campanha | `LOW-MEDIUM` | A feição é um banco/baixio, não porto. Fontes modernas divergem quanto à localização pontual; não deve receber coordenada de cidade. |
| SJO | Ilhas de São Jorge | ilhéus junto a Moçambique; síntese moderna identifica-os com o conjunto hoje associado às ilhas de Goa/Sena nas proximidades da Ilha de Moçambique | `NAVIGATION_ONLY` / parada ritual curta | `MEDIUM` | O `Roteiro` registra ancoragem muito breve e colocação de padrão. Não há evidência de mercado ou reabastecimento nessa passagem de retorno. |
| RGR | Baixos do Rio Grande | baixos do Rio Grande/Geba, atual Guiné-Bissau | `NAVIGATION_ONLY` / marco de sondagem | `MEDIUM-HIGH` para a região; `LOW` para ponto exato | O `Roteiro` não avista terra: a posição é inferida por sondagens e pilotos. Deve ser representada como área/banco, não como porto. |

## Evidência de estrutura da rota

O inventário do RUTTER Project descreve explicitamente o retorno em três blocos: Calecute → Ilhéus de Santa Maria → Angediva; Angediva → Melinde; Melinde → Baixos de São Rafael → Ilhas de São Jorge → Angra de São Brás; e, por fim, São Brás → Cabo da Boa Esperança → Baixos do Rio Grande. Essa estrutura confirma que São Rafael, São Jorge e Rio Grande são elementos do roteiro náutico, não necessariamente assentamentos ou mercados.

A edição de Ravenstein confirma que, em 25/04/1499, a frota tinha apenas sondagens de 20–35 braças e não via terra, sendo informada pelos pilotos de que estava próxima dos baixos do Rio Grande. Portanto, uma coordenada pontual de margem fluvial seria metodologicamente excessiva.

## Implicações para o modelo

1. `ANJ` é o único novo candidato que, nesta etapa, reúne evidência suficientemente forte para uma futura escala logística plena.
2. `SMI`, `BSR`, `SJO` e `RGR` devem permanecer como marcos/feições náuticas ou nós-evento até nova evidência.
3. `BSR` deve carregar o evento histórico específico de redução da frota, não uma mecânica genérica de porto.
4. `RGR` deve ser uma área de navegação por sondagem, e não um ponto terrestre preciso.
5. Nenhum destes candidatos deve receber `market=TRUE` por inferência.

## Fontes de controle

- Antonio Giurgevich, *Roteiros portugueses dos séculos XV e XVI (Manuscritos)*, RUTTER Project, inventário do roteiro de Vasco da Gama, especialmente a descrição da viagem de volta.
- E. G. Ravenstein (ed./trad.), *A Journal of the First Voyage of Vasco da Gama, 1497–1499*, Hakluyt Society, 1898.
- A. H. de Oliveira Marques, *Atlas histórico de Portugal e do Ultramar português*, mapa da viagem de Vasco da Gama, reproduzido pela Torre do Tombo.
- sínteses náuticas portuguesas usadas apenas como controle de identificação moderna; divergências de localização continuam preservadas.

## Gate seguinte

Antes de qualquer alteração em `nodes.csv`, falta auditar o trecho pós-25/04/1499 — separação do Bérrio e do S. Gabriel, passagem por São Tiago/Terceira e datas de chegada — em fontes posteriores identificáveis (Barros, Castanheda, Damião de Góis, Resende ou sínteses críticas que explicitem qual tradição estão usando).