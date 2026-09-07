# P1-func — wave19 com Santa Maria e carena mínima

Issues: #99, #100, #101.

Run: `34117146711`.
Commit validado: `dac49c0d6f1461e34c45621bc51ad69fd0719d4b` e estado documental subsequente sem alteração de regras executáveis.

## Alterações em relação à wave18

A primeira perna agregada `CAL→ANJ` foi dividida em:

- `CAL→SMI`, 30/08/1498 a 15/09/1498, 16 dias;
- `SMI→ANJ`, 15/09/1498 a 20/09/1498, 5 dias.

Nos Ilhéus de Santa Maria, o `Roteiro` registra barcos trazendo peixe. `SMI` foi materializado como `NAVIGATION_POINT`, sem mercado nem serviço portuário genérico. A ação alimentar específica tem capacidade máxima de 5 dias-equivalentes e duração de 0 dias inteiros, ambos parâmetros de `SIMULATION`. Nos diagnósticos, ela é usada uma única vez.

A carena de Anjediva permanece como ação explícita de restauração mínima de 2 pontos abstratos de condição, selecionada pela sensibilidade anterior.

## Painel

Mantiveram-se os mesmos cinco arquétipos competentes e quatro seeds (`23001–23004`), totalizando 20 casos. Cada sessão percorre primeiro o MVP real; somente estados que satisfazem o gate do MVP seguem para o retorno.

- casos totais: **20**;
- MVP concluído: **18/20**;
- elegíveis para o retorno: **18**.

## Controle sem carena

Com Santa Maria incorporada, mas sem usar a carena:

- retorno concluído: **13/18**;
- blockers de provisões: **0**;
- blockers de condição: **5 `VESSEL_CONDITION_TOO_LOW`**, todos associados à seed `23004` e concentrados em `R_SBR_CGH_RET`.

Isso mostra que a segmentação por Santa Maria elimina exclusivamente o problema logístico identificado na wave17. O caso antes bloqueado com `19,366` dias-equivalentes consegue alcançar Santa Maria, executar a oportunidade alimentar específica e prosseguir para Anjediva.

## Controle completo com carena mínima

Aplicando também a carena de 2 pontos em Anjediva:

- retorno concluído: **18/18 (100%)**;
- blockers: **0**;
- `COMPLETIONIST`: 4/4;
- `GRAND_STRATEGIST`: 4/4;
- `SURVIVALIST`: 4/4;
- `MERCHANT`: 3/3 elegíveis;
- `ROLEPLAYER`: 3/3 elegíveis;
- todas as conclusões chegam a `BRG` em **1499-04-25**;
- todas permanecem `GUIDED`.

A seed `23004`, que herda condição `47,49` do MVP, conclui com condição final `13,59`. Isso não invalida o gate: BRG é o limite jogável atual da narrativa primária, e a condição baixa continua visível para qualquer expansão futura em vez de ser artificialmente restaurada.

## Não regressão

O run `34117146711` passou integralmente:

- validação dos CSVs;
- **241 testes de domínio**;
- protótipos de economia, navegação, viagem, porto, comércio e sessão;
- smoke do retorno `CAL→SMI→ANJ→MAL→BSR→SBR→CGH→BRG`;
- diagnósticos wave19;
- interface histórica e técnica;
- interface v0.2;
- persistência M6;
- mapa de coordenadas;
- mapa cartográfico de referência.

O teste do MVP continua exigindo exatamente dez pernas para `EXP_GAMA_1497`. O retorno permanece subcampanha opt-in independente.

## Decisão

A lacuna de agência logística #100 está resolvida de forma historicamente sustentada e pode ser encerrada. A #101 já está concluída.

A #99 continua aberta somente porque o retorno ainda precisa ser exposto como experiência efetivamente jogável na interface e ter save/load testado durante a subcampanha, não apenas no baseline do MVP.

## Próximo gate

Abrir uma issue específica de interface/persistência para:

1. oferecer continuação explícita para o retorno após o gate do MVP em Calecute;
2. mostrar Santa Maria como marco náutico e disponibilizar a oportunidade alimentar uma única vez;
3. expor a carena documentada em Anjediva com efeito rotulado como simulação;
4. preservar indisponibilidade genérica de mercado/serviços nesses pontos;
5. salvar e restaurar uma sessão durante `EXP_GAMA_RETURN_1498` sem mudar seed, cronologia, stop ou perna corrente;
6. executar smoke de interface até BRG.
