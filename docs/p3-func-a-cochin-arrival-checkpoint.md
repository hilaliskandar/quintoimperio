# P3-func-A — checkpoint Cabral em Cochim

Data: 2026-09-07  
Issue: #116  
Branch: `p3-func-a-116`

## Estado estabilizado

A campanha guiada de Pedro Álvares Cabral está executável de Lisboa até Cochim:

`LIS → VCR → MOZ → KIL → MAL → ANJ → CAL → COC`.

A ruptura de Calecute não introduz sistema geral de combate. O resultado documental é representado por `CAL1500_E01` em `node_state_events.csv`: perda da presença institucional portuguesa, acesso `RESTRICTED` e relação `HOSTILE`, preservando a soberania do Samorim.

A transição é conservadora. A janela documental é 16–18/12/1500 e o novo estado só se torna efetivo no limite superior, 18/12. A mesma data é usada como âncora operacional de partida para a perna `R_CAL_COC`; não é tratada como data testemunhal independente.

A chegada a Cochim em 24/12/1500 é documental. A observação `CABRAL1500_CAL_COC` registra seis dias de viagem e grau B por combinar uma chegada firme com uma partida operacional derivada.

## Testes

Foi criado `tests/test_p3_calicut_cochin.py`, que verifica:

- bloqueio da saída de Calecute antes do limite da ruptura;
- liberação em 18/12/1500;
- perna `R_CAL_COC` sob `FLEET_COMMAND`;
- duração de seis dias e chegada em 24/12/1500;
- permanência da cronologia em `GUIDED`;
- encerramento da sequência de pernas ao chegar a Cochim;
- ausência de `CAL1500_E01` em 17/12;
- aplicação de `CAL1500_E01` em 18/12;
- estado `NONE / RESTRICTED / HOSTILE` sem fortificação ou guarnição;
- preservação explícita da soberania do Samorim.

A primeira CI do gate, run `34136313555`, encontrou apenas uma expectativa obsoleta em `test_p3_campaign.py`: o teste anterior ainda esperava que a expedição terminasse ao chegar a Calecute. O novo teste de Cochim já passava.

A expectativa antiga foi atualizada para exigir `EXP_CABRAL_1500`, sequência 7 e escala `CABRAL1500_CAL`. O run `34136411609`, commit `03cf3a4e80cf4f20ca82ae391946450190abd5b8`, fechou integralmente verde: validação dos CSVs, 271 testes de domínio, protótipos, regressão do MVP e retorno, interfaces, persistência e cartografia.

## Próximo gate

Auditar a permanência de Cabral em Cochim entre 24/12/1500 e o início de janeiro de 1501, distinguindo:

1. chegada e negociação;
2. estabelecimento da presença residente inicial, já representada por `COC1500_E01`;
3. carregamento/comércio sem inventar preços;
4. saída e contato em Cananor;
5. decisão de onde encerrar a campanha principal de Cabral antes da torna-viagem.

Nenhuma nova mecânica deve ser criada enquanto essas transições puderem ser representadas por escalas, eventos temporais e regras de acesso existentes.
