# F4 — defesa de Cochim 1504 — auditoria de propriedade e temporalidade v0.1

Data: 2026-09-08
Issue: #130
Baseline da branch: `fec3888679024868f321790d4f1d065dcf641914`

## Problema

A proposta documental de F4 prevê uma cadeia curta de eventos defensivos antes da chegada da armada de Lopo Soares. `expedition_events.csv`, porém, exige `expedition_id` normalizado e `ExpeditionEventModel.available_by()` considera um evento seguramente ocorrido apenas quando `date_to <= on_date`.

Há dois riscos de modelagem:

1. atribuir a defesa de março–julho a `EXP_LOPO_SOARES_1504`, embora a armada só chegue ao Malabar em setembro;
2. atribuir a defesa a `EXP_FRANCISCO_ALBUQUERQUE_1503`, confundindo a armada que parte com a força residente deixada sob Duarte Pacheco Pereira.

Ambas as opções são semanticamente inadequadas.

## Evidência de continuidade da força residente

A EVE/FCSH registra que Duarte Pacheco Pereira seguiu na armada de Francisco de Albuquerque em 1503 e, após a restauração de Cochim e construção da fortificação, foi mandado permanecer no Oriente no comando de uma pequena unidade militar, incluindo duas caravelas, para a defesa de Cochim. Ao longo de 1504 liderou forças portuguesas e cochinenses contra as investidas do Samorim.

Roger Lee de Jesus (2021), em estudo crítico de história militar, trata a defesa de Cochim como caso próprio e destaca que vários ataques ocorreram entre março e maio, com a geografia lagunar e os acessos estreitos condicionando as operações. O estudo é útil sobretudo para causalidade e cautela quantitativa; não autoriza importar números das crônicas como parâmetros.

## Decisão de propriedade

Criar uma unidade histórica documental separada:

`EXP_DUARTE_PACHECO_DEFENSE_1504`

Tipo proposto:

`RESIDENT_DEFENSE_SUBCAMPAIGN`

Características:

- líder: Duarte Pacheco Pereira;
- período: 1504–1504;
- autoridade: Coroa portuguesa, em aliança com o rajá de Cochim;
- protagonista não fixo;
- **sem pernas em `expedition_routes.csv`**;
- finalidade exclusiva: possuir documentalmente a sequência defensiva e permitir consulta temporal sem transformar a força residente em frota simultânea jogável.

Essa unidade é de modelagem, assim como outras subcampanhas do projeto, mas corresponde a uma força histórica efetivamente separada da armada que regressou.

## Auditoria temporal

### Início da campanha

A matriz interna sustentava apenas “março–julho”. Pesquisa dirigida encontrou uma síntese acadêmica que adota 16/03/1504 para a chegada das forças do Samorim a Edappalli, mas a cronologia tradicional apresenta divergências entre cronistas e reconstruções.

Decisão: **não promover 16/03 a `EXACT`** nesta tranche.

Para o contrato conservador do modelo, normalizar apenas o nível mensal firmemente sustentado:

- `date_from = 1504-03-01`;
- `date_to = 1504-03-31`;
- `date_precision = RANGE`;
- sem alegar que a campanha começou em 01/03 ou 31/03; o intervalo significa somente “início situado em março”.

Assim, `available_by()` considera o início seguramente ocorrido apenas ao fim do mês, que é coerente com a regra conservadora do projeto.

### Operações repetidas

Jesus (2021) registra ataques sucessivos entre março e maio e enfatiza posição, terreno e armas de fogo. Isso sustenta um evento-resumo de recorrência, não uma batalha artificial por mês.

Proposta:

- `DEFENSIVE_OPERATIONS_REPEATED`;
- intervalo `1504-03-01`–`1504-05-31`;
- o evento significa que, até o fim de maio, a defesa repetida está documentalmente estabelecida;
- nenhuma quantificação de dano, força, moral ou baixas.

### Encerramento da fase principal

Sínteses especializadas situam o fim da ofensiva principal em julho. A data 03/07 aparece em literatura secundária, mas não é elevada aqui a testemunho diário.

Proposta conservadora:

- `DEFENSE_CAMPAIGN_ENDS`;
- `1504-07-01`–`1504-07-31`;
- `RANGE`;
- efeito narrativo: fracasso da ofensiva principal e preservação de Cochim;
- **nenhuma mudança de soberania, fortificação ou guarnição**, pois o estado herdado permanece.

## Estado do nó

A campanha defensiva não exige novos `node_state_events` no primeiro incremento. Em 1504, durante e depois da fase principal:

- soberania local permanece;
- `FACTORY_RESTORED` permanece;
- `PORTUGUESE_FORT` permanece;
- `PORTUGUESE_GARRISON` permanece;
- acesso e relação permanecem conforme o baseline, salvo evidência posterior específica.

A cadeia de eventos registra o processo histórico, não uma falsa transição territorial.

## Lopo Soares

`EXP_LOPO_SOARES_1504` continua separada e sem pernas. Eventos de sua chegada só serão incorporados quando a janela de setembro estiver suficientemente fechada para o contrato temporal. A defesa de março–julho não será atribuída a essa armada.

## Decisão de implementação

Autorizado no próximo incremento:

1. registrar `EXP_DUARTE_PACHECO_DEFENSE_1504` sem pernas;
2. registrar três eventos-resumo: início em março, operações repetidas março–maio e fim em julho, todos com limites mensais conservadores;
3. testar ordenação por `available_by()` e continuidade do estado de Cochim;
4. não criar combate geral, Coulão, novas rotas ou novos `node_state_events`.

## Fontes externas dirigidas

- Enciclopédia Virtual da Expansão Portuguesa, entrada “Duarte Pacheco Pereira (?-1531/3)”.
- Roger Lee de Jesus, “Reassessing Portuguese military superiority in Asia in the sixteenth century: the case of land warfare”, em *The First World Empire: Portugal, War and Military Revolution*, Routledge, 2021, pp. 152–166, DOI 10.4324/9780429346965-13.

As datas diárias 16/03 e 03/07 permanecem candidatos historiográficos e não são tratadas como `EXACT` nesta versão.
