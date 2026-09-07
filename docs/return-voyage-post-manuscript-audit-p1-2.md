# P1.2 — Auditoria do trecho pós-manuscrito do retorno, 1499

Status: gate documental. Este documento classifica a evidência posterior ao encerramento abrupto do `Roteiro`; não autoriza ainda alteração de dados executáveis.

Issue: #92.

## Quebra de proveniência

O corpo do `Roteiro` termina quando a armada está nos baixos do Rio Grande, em fins de abril de 1499. A continuação apresentada por Ravenstein é explicitamente editorial e combina tradições posteriores. A base deve, portanto, distinguir `PRIMARY_NARRATIVE` de `EDITORIAL_SYNTHESIS` e, quando possível, registrar a tradição cronística subjacente.

## Eventos pós-25/04

| Evento | Evidência / tradição explicitada por Ravenstein | Grau de segurança | Tratamento recomendado |
|---|---|---|---|
| Separação entre Vasco da Gama e Nicolau Coelho | Ravenstein atribui a separação por tempestade a Resende | `MEDIUM-HIGH` como tradição cronística; não primária | evento pós-manuscrito, sem data diária inventada |
| Bérrio/Nicolau Coelho chega a Cascais | 10/07/1499 em Ravenstein; nota registra variante 11/07 no `Paesi` | `HIGH` para julho; `MEDIUM` para dia exato | preservar 10/07 como valor editorial preferido + variante 11/07 |
| Vasco espera um dia pelo consorte e segue para São Tiago | síntese editorial de Ravenstein | `MEDIUM` | São Tiago pode ser escala pós-manuscrito, mas deve carregar `EDITORIAL_SYNTHESIS` |
| João de Sá assume o S. Gabriel | Ravenstein informa que Barros, Góis e Castanheda sustentam essa tradição | `HIGH` como convergência cronística posterior | mudança de comando específica da expedição |
| Vasco freta caravela para levar Paulo da Gama à Terceira | Barros, Góis e Castanheda segundo a discussão editorial | `HIGH` como convergência posterior | troca de embarcação do capitão-mor; não inferir mecânica genérica de fretamento |
| Paulo da Gama morre na Terceira | Ravenstein informa morte um dia após desembarque em Angra e sepultamento no convento de S. Francisco | `MEDIUM-HIGH` | evento narrativo pós-manuscrito; data exata depende da cronologia de chegada |
| S. Gabriel chega a Lisboa sob João de Sá | necessariamente antes de 28/08/1499, pois carta régia dessa data já incorpora informação do retorno | `HIGH` para limite ante quem; data exata desconhecida | usar `before=1499-08-28`, não inventar data única |
| Vasco da Gama chega a Lisboa | Barros, Góis e Resende: 29/08; Castanheda: 08/09; manuscrito da Torre do Tombo citado por Teixeira de Aragão: 18/09; Herculano: fim de agosto/início de setembro | `HIGH` para divergência; `LOW` para qualquer dia único | armazenar intervalo/tradições, nunca harmonizar silenciosamente |

## Contradição documental adicional

Ravenstein discute uma carta associada a Peutinger que parece dizer que Vasco da Gama regressou no próprio navio de 90 tonéis. O editor considera essa formulação difícil de conciliar com Barros, Góis e Castanheda, que dizem que João de Sá levou o S. Gabriel a Lisboa enquanto Vasco seguiu numa caravela para a Terceira. Ravenstein prefere entender a carta como informação imprecisa ou combinação de dois eventos próximos.

Essa divergência deve ser preservada. Para a implementação futura, a tradição convergente Barros–Góis–Castanheda pode ser adotada como cenário-base, mas com `confidence=MEDIUM-HIGH` e nota explícita da alternativa documental.

## Proposta de estados de evidência pós-manuscrito

- `RGR → separation_at_sea`: `EDITORIAL_SYNTHESIS`, fonte-tradição Resende.
- `BERRIO → CASCAIS/LIS`: `EDITORIAL_SYNTHESIS`, data 10/07 com variante 11/07.
- `SGABRIEL → STG`: `EDITORIAL_SYNTHESIS`.
- `STG → LIS` sob João de Sá: `EDITORIAL_SYNTHESIS`, chegada anterior a 28/08.
- `STG → TER` por caravela fretada, Vasco + Paulo: `EDITORIAL_SYNTHESIS`.
- `TER → LIS` Vasco da Gama: data incerta, intervalo fim de agosto–18/09, com tradições concorrentes.

## Consequência para o jogo

O retorno terminal deixa de ser uma campanha de frota única. Depois do Rio Grande, ao menos duas trajetórias são necessárias: Bérrio/Nicolau Coelho e S. Gabriel/João de Sá; a trajetória pessoal de Vasco da Gama se separa ainda do S. Gabriel em São Tiago. A interface futura deve distinguir `expedition vessel trajectory` de `character trajectory`.

Isso não exige imediatamente um sistema geral de personagens viajando independentemente; pode ser representado como fechamento narrativo específico da primeira expedição até que a expansão pós-MVP demande uma abstração reutilizável.

## Gate P1.2

Considera-se documentalmente seguro avançar para uma proposta de dados somente se:

1. datas pós-manuscrito forem marcadas como síntese/tradição posterior;
2. 29/08, 08/09 e 18/09 não forem fundidos em uma data artificial;
3. o limite `S. Gabriel chegou antes de 28/08` for preservado sem preenchimento arbitrário;
4. a divergência da carta associada a Peutinger for mantida nas notas;
5. o modelo de dados puder separar trajetória da embarcação e trajetória do personagem.