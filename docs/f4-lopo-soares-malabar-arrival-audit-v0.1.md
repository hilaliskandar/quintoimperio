# F4 — Lopo Soares 1504 — auditoria de chegada ao Malabar v0.1

Data: 2026-09-08
Issue: #130

## Objetivo

Separar os marcos de entrada da armada no Índico, passagem pela costa do Malabar e chegada a Cochim, normalizando somente o que possui resolução documental suficiente e evitando construir uma rota Lisboa→Índia a partir de sínteses retrospectivas.

## 1. Estado das evidências

### Anjediva

Reconstruções secundárias situam a armada em Anjediva em agosto de 1504 e registram ali o encontro com embarcações remanescentes de António de Saldanha e Rui Lourenço Ravasco. O gate ainda não dispõe de data diária primária suficientemente fechada.

Decisão: manter Anjediva como contexto documental nesta etapa; não criar perna ou `voyage_observation` de Lopo Soares.

### Cananor / Calecute

A sequência Anjediva→Cananor→Calecute é sustentada em sínteses da viagem. A data 07/09/1504 para a presença diante de Calecute é recorrente em reconstruções secundárias, mas não foi ainda amarrada neste gate a uma fonte contemporânea comparável à carta de Álvaro Vaz.

Decisão: não normalizar 07/09 como `EXACT` nesta versão e não criar `CALICUT_BOMBARDMENT` até fechar sua proveniência.

### Cochim

A entrada de Lopo Soares em Cochim em `14/09/1504` possui grau distinto de sustentação. Manuel Alberto Carvalho Vicente registra a data e remete à carta de Álvaro Vaz a D. Manuel, escrita em Cochim em 24/12/1504, como confirmação documental. Estudos especializados da viagem de Lopo Soares utilizam a mesma tradição documental.

Decisão: `14/09/1504` pode ser normalizado como `EXACT` para a chegada a Cochim.

## 2. Normalização mínima autorizada

Adicionar a `EXP_LOPO_SOARES_1504`:

`LS1504_E01`

- `event_type`: `ROYAL_FLEET_ARRIVES_COCHIN`;
- sujeito: armada de Lopo Soares de Albergaria;
- `origin_node`: vazio, para não inferir uma perna executável ou uma origem imediata ainda não consolidada;
- `destination_node`: `COC`;
- `date_from = date_to = 1504-09-14`;
- `date_precision = EXACT`;
- `source_id = ALVARO_VAZ_COCHIN_1504|VICENTE_PORTUGAL_MADAGASCAR`;
- sem efeito automático sobre soberania, fortificação ou guarnição.

O evento representa chegada/reforço objetivo da presença portuguesa, mas não cria quantitativo de força nem nova dimensão de `node_state_events`.

## 3. Relação com a defesa residente

A sequência temporal esperada fica explicitamente separada:

- até 31/07: fase principal da defesa residente de Duarte Pacheco seguramente encerrada;
- 01/08–13/09: intervalo sem novo evento normalizado nesta versão; deslocamentos de Duarte Pacheco e aproximação da armada permanecem documentais;
- 14/09: armada de Lopo Soares chega a Cochim.

Isso impede que a armada europeia seja tratada como causa retrospectiva da defesa de março–julho.

## 4. Divergência nominal

A auditoria da viagem revelou conflito entre a listagem EVE, que apresenta Manuel Teles Barreto entre os capitães de 1504, e reconstrução especializada que distingue Manuel Teles de Vasconcelos nessa armada e Manuel Teles Barreto em 1506.

Essa divergência afeta a futura transição de comando, não o marco de chegada de Lopo Soares. Nenhum comandante sucessor será gravado em `node_state_events` nesta etapa.

## 5. Próximo passo

Após testar `LS1504_E01`, o gate seguinte deverá verificar:

1. se o bombardeio de Calecute pode receber data/proveniência suficientemente forte;
2. se o ataque a Cranganor é necessário ao estado de 31/12/1504 ou pode permanecer documental;
3. qual é o estado institucional relevante após a chegada de Lopo sem introduzir quantitativos de força;
4. a divergência Manuel Teles de Vasconcelos × Manuel Teles Barreto antes de qualquer normalização de sucessão.
