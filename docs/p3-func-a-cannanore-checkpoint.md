# P3-func-A — checkpoint Cabral em Cananor

Data: 2026-09-07  
Issue: #116  
Branch: `p3-func-a-116`

## Estado estabilizado

A campanha guiada principal de Pedro Álvares Cabral está executável de Lisboa até Cananor:

`LIS → VCR → MOZ → KIL → MAL → ANJ → CAL → COC → CAN`.

Após a chegada a Cochim em 24/12/1500, a escala `CABRAL1500_COC` mantém a campanha bloqueada até 09/01/1501. A escala registra apenas fatos específicos da passagem: contacto diplomático, carregamento de especiarias e permanência de residentes portugueses. Não cria preços históricos, estoque automático, fortificação ou soberania portuguesa.

A presença residente persistente continua sendo resolvida temporalmente por `COC1500_E01`, que se torna efetiva conservadoramente em 09/01/1501. Até 08/01, o evento não integra o estado efetivo do nó.

A perna `R_COC_CAN_CAB` usa a cronologia documental 09/01 → 15/01/1501, seis dias, sob `FLEET_COMMAND`. Em Cananor, `CABRAL1501_CAN` registra acolhimento favorável, compra limitada de especiarias e preparação da torna-viagem até 16/01. Essas atividades não ampliam automaticamente o mercado genérico do nó.

`CAN1501_E01` permanece a transição mundial específica: contacto favorável, acesso negociado e relação favorável em 15/01, sem presença institucional portuguesa retroativa. A feitoria posterior continua separada.

## Testes e CI

`tests/test_p3_calicut_cochin.py` foi ampliado para verificar:

- escala de Cochim até 09/01;
- carregamento e residentes como atividades documentais;
- bloqueio de saída antecipada;
- perna `R_COC_CAN_CAB`, seis dias e chegada em 15/01;
- permanência em `ChronologyMode.GUIDED`;
- encerramento da sequência principal de pernas em Cananor;
- escala `CABRAL1501_CAN` até 16/01;
- aplicação conservadora de `COC1500_E01` somente em 09/01;
- aplicação de `CAN1501_E01` em 15/01;
- ausência de fortificação/soberania portuguesa inferida.

O run `34136897610`, commit `e878d6a60a3226059d0dfce25faa4dcf267032f5`, passou integralmente: validação dos CSVs, testes de domínio, protótipos, regressão do MVP e retorno de Gama, interfaces, persistência e cartografia.

## Próximo gate

A torna-viagem de Cabral começa em 16/01/1501 e deve ser tratada como subgate próprio. A matriz documental já indica perda específica da nau de Sancho de Tovar em 12/02, reparos em Moçambique, missão destacada a Sofala, uma embarcação desgarrada antes do Cabo e retornos assíncronos ao reino. Antes de normalizar pernas, deve ser auditado se o padrão de subcampanha usado em `EXP_GAMA_RETURN_1498` é suficiente para representar esse retorno sem sistema geral de múltiplas frotas.
