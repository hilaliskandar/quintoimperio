# P1.1 — Auditoria cartográfica dos candidatos do retorno, 1498–1499

Status: gate documental/cartográfico concluído, com adendo P1-func para Santa Maria em 2026-09-07.

Issue original: #92. Revisão funcional: #100.

## Critério

A classificação abaixo distingue: (a) identificação moderna suficientemente estável; (b) localização aproximada sustentada por rota/descrição, mas sem ponto moderno inequívoco; e (c) referência náutica histórica que não deve ser convertida em porto ou mercado.

Escala de confiança:

- `HIGH`: identificação moderna direta e estável;
- `MEDIUM`: identificação provável, mas ponto exato ou extensão espacial ainda discutível;
- `LOW`: apenas zona/feição aproximada; não autoriza coordenada pontual precisa.

## Resultado

| ID | Nome histórico | Identificação moderna de trabalho | Tipo recomendado | Confiança | Observação |
|---|---|---|---|---|---|
| SMI | Ilhéus de Santa Maria | Netrani / Pigeon Island como âncora de trabalho; tradição alternativa junto a Mulpy/Malpe preservada | `NAVIGATION_ONLY` / marco náutico | `MEDIUM` | Ravenstein associa o padrão a Netrani/Pigeon Island e a edição anotada de Jeremy Lawrance repete essa identificação, mas a tradição alternativa não permite elevar a equivalência histórica a `HIGH`. O `Roteiro` registra padrão e contato com barcos trazendo peixe; não há base para mercado ou escala logística plena. |
| ANJ | Anjediva / Angediva | Anjadip (Anjediva) Island, costa de Karnataka/Goa | `ANCHORAGE_CONTACT` / escala logística | `HIGH` | Identificação moderna estável. O retorno documenta permanência, água, madeira, alimento e carena. Forte candidato a nó operacional. |
| BSR | Baixos de São Rafael | baixios na costa da África Oriental, no corredor entre Melinde/Mombaça e Zanzibar; tradição posterior associa o nome ao local em que a nau S. Rafael foi abandonada/queimada | `NAVIGATION_ONLY` + evento de campanha | `LOW-MEDIUM` | A feição é um banco/baixio, não porto. Fontes modernas divergem quanto à localização pontual; não deve receber coordenada de cidade. |
| SJO | Ilhas de São Jorge | ilhéus junto a Moçambique; síntese moderna identifica-os com o conjunto hoje associado às ilhas de Goa/Sena nas proximidades da Ilha de Moçambique | `NAVIGATION_ONLY` / parada ritual curta | `MEDIUM` | O `Roteiro` registra ancoragem muito breve e colocação de padrão. Não há evidência de mercado ou reabastecimento nessa passagem de retorno. |
| RGR | Baixos do Rio Grande | baixos do Rio Grande/Geba, atual Guiné-Bissau | `NAVIGATION_ONLY` / marco de sondagem | `MEDIUM-HIGH` para a região; `LOW` para ponto exato | O `Roteiro` não avista terra: a posição é inferida por sondagens e pilotos. Deve ser representada como área/banco, não como porto. |

## Adendo P1-func — revisão de Santa Maria

A identificação preliminar de SMI com Laquedivas/Lakshadweep mostrou-se excessivamente ampla quando o ponto passou de referência narrativa a candidato necessário para a continuidade jogável. A revisão dirigida encontrou suporte mais específico para Netrani/Pigeon Island:

- Ravenstein identifica o candidato com Netrani/Pigeon Island em sua anotação do trecho;
- a edição anotada de Jeremy Lawrance, de 2004, também usa Netrani/Pigeon Island;
- permanece registrada uma tradição alternativa que desloca os ilhéus para a área de Mulpy/Malpe.

Por isso, a coordenada moderna de Netrani pode ser usada como âncora cartográfica de trabalho, mas a **equivalência histórica** continua `MEDIUM`. A segurança da coordenada moderna não deve ser confundida com segurança da identificação do topônimo histórico.

A materialização de `SMI` no P1-func decorre de necessidade demonstrada de segmentação: a narrativa registra contatos alimentares em 11/09 e, em 15/09, barcos trazendo peixe nos Ilhéus de Santa Maria antes da continuação para Anjediva. Essa evidência permite representar um contato alimentar específico sem inventar abastecimento em Calecute.

## Evidência de estrutura da rota

O inventário do RUTTER Project descreve explicitamente o retorno em três blocos: Calecute → Ilhéus de Santa Maria → Angediva; Angediva → Melinde; Melinde → Baixos de São Rafael → Ilhas de São Jorge → Angra de São Brás; e, por fim, São Brás → Cabo da Boa Esperança → Baixos do Rio Grande. Essa estrutura confirma que São Rafael, São Jorge e Rio Grande são elementos do roteiro náutico, não necessariamente assentamentos ou mercados.

A edição de Ravenstein confirma que, em 25/04/1499, a frota tinha apenas sondagens de 20–35 braças e não via terra, sendo informada pelos pilotos de que estava próxima dos baixos do Rio Grande. Portanto, uma coordenada pontual de margem fluvial seria metodologicamente excessiva.

## Implicações para o modelo

1. `ANJ` permanece o único novo candidato a escala logística plena.
2. `SMI` pode ser materializado como `NAVIGATION_POINT` porque a continuidade funcional passou a exigir o marco, sem convertê-lo em porto ou mercado.
3. A ação alimentar em SMI deriva da passagem documental específica e não altera `market_scale=NONE` nem cria serviço portuário genérico.
4. `BSR` deve carregar o evento histórico específico de redução da frota, não uma mecânica genérica de porto.
5. `RGR` deve ser uma área de navegação por sondagem, e não um ponto terrestre preciso.
6. Nenhum destes candidatos deve receber `market=TRUE` por inferência.

## Fontes de controle

- Antonio Giurgevich, *Roteiros portugueses dos séculos XV e XVI (Manuscritos)*, RUTTER Project, inventário do roteiro de Vasco da Gama, especialmente a descrição da viagem de volta.
- E. G. Ravenstein (ed./trad.), *A Journal of the First Voyage of Vasco da Gama, 1497–1499*, Hakluyt Society, 1898.
- Jeremy Lawrance (ed./trad.), *Relato da viagem de Vasco da Gama*, edição anotada, 2004, para a identificação de Santa Maria/Netrani e suas notas.
- A. H. de Oliveira Marques, *Atlas histórico de Portugal e do Ultramar português*, mapa da viagem de Vasco da Gama, reproduzido pela Torre do Tombo.
- Survey of India e bases cartográficas oficiais indianas para a posição moderna de Netrani; usadas apenas para a âncora moderna, não como prova da equivalência histórica.

## Situação do gate

A auditoria cartográfica original foi concluída no P1 documental. O adendo atual corrige apenas a identificação de trabalho de SMI necessária ao P1-func. O trecho pós-25/04/1499 permanece tratado separadamente nos documentos de auditoria do epílogo e não é reaberto por esta correção.