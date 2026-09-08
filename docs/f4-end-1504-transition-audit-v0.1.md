# F4 — transição de fim de 1504 em Cochim — auditoria v0.1

Data: 2026-09-08
Issue: #130

## Objetivo

Definir o menor fechamento temporal da F4 depois da chegada de Lopo Soares a Cochim em 14/09/1504, separando a presença transitória da armada régia da presença institucional/guarnição que permanece no porto.

## 1. Saída da armada de Cochim

Manuel Alberto Carvalho Vicente, em estudo académico sobre a expansão manuelina no Índico, registra que Lopo Soares deixou Cochim em `26/12/1504`. A mesma sequência situa antes dessa partida as operações posteriores no Malabar e a decisão de deixar uma pequena força de guarda em Cochim.

A data é suficientemente precisa para um marco documental de partida, mas não autoriza inferir destino operacional imediato como perna do grafo.

### Normalização autorizada

`LS1504_E02`

- `expedition_id = EXP_LOPO_SOARES_1504`;
- `event_type = ROYAL_FLEET_DEPARTS_COCHIN`;
- `origin_node = COC`;
- `destination_node = vazio`;
- `date_from = date_to = 1504-12-26`;
- `date_precision = EXACT`;
- evidência de trabalho `B`, por depender nesta tranche de reconstrução académica especializada;
- nenhum efeito automático sobre soberania, feitoria, fortificação ou guarnição.

## 2. Cranganor e ações posteriores

A documentação sustenta a operação de Cranganor e outros confrontos após a chegada de Lopo. Esses episódios são historicamente relevantes, mas não demonstram, para o estado de `31/12/1504`, uma nova dimensão territorial/institucional em Cochim que exija normalização funcional.

Decisão nesta tranche:

- manter Cranganor como evento/documentação narrativa, sem novo nó;
- não criar combate geral;
- não criar dano, força, moral ou baixas;
- não criar evento separado apenas para acumular batalhas quando o estado persistente de Cochim não muda.

## 3. Estado de Cochim após 26/12

A saída da armada de Lopo não remove automaticamente:

- `FACTORY_RESTORED`;
- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- acesso negociado;
- relação favorável;
- soberania local.

Essas dimensões continuam resolvidas por `node_state_events` herdados de F3.

A F4 deve testar explicitamente `31/12/1504` para provar que o reforço transitório não foi confundido com a presença residente.

## 4. Sucessão de comando

A documentação consultada apresenta divergência nominal:

- a listagem EVE/FCSH associa `Manuel Teles Barreto` à armada de 1504;
- reconstrução especializada distingue `Manuel Teles de Vasconcelos` nessa armada e associa `Manuel Teles Barreto` a 1506.

A saída de Lopo em 26/12 não resolve essa divergência. Portanto:

- F4 não normaliza comandante nominal da guarnição em `node_state_events`;
- a guarnição permanece como estado institucional abstrato;
- a divergência é entregue a F5 como pendência historiográfica explícita.

## 5. Consequência para o fechamento F4

Se `LS1504_E02` e o estado de `31/12/1504` passarem em CI, a F4 terá os marcos mínimos necessários:

1. estado herdado de 1503;
2. campanha defensiva residente de março–julho;
3. chegada exata de Lopo Soares a Cochim em 14/09;
4. saída exata da armada de Cochim em 26/12;
5. continuidade da presença residente sob soberania local no fim do ano.

Isso é suficiente para um handoff limpo a 1505 sem criar combate sistêmico, Coulão, Cranganor ou itinerário Lisboa→Índia como nós/pernas artificiais.
