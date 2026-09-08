# F5-doc — Francisco de Almeida 1505 — proposta mínima de normalização

Data: 2026-09-08
Issue: #132
Baseline F4: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`
Gate-mãe: #118

## Objetivo

Definir o menor conjunto de expedições, eventos e estados temporais necessário para representar o horizonte até `31/12/1505` e preparar `Python 1505 GREEN`, sem transformar 1505 em justificativa automática para combate geral, frota quantitativa ou novo sistema de governo.

## 1. Decisões arquiteturais

### Autoridade vice-real

`NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO`

A autoridade de Francisco de Almeida deve ser representada por:

- metadados da expedição;
- eventos institucionais por data;
- estados locais já suportados por `node_state_events`.

Criar um estado global permanente de governo só seria justificável se o loop precisasse consultar, fora da própria expedição/eventos, quem exerce competência portuguesa sobre múltiplos nós. Essa necessidade não foi demonstrada até `31/12/1505`.

### Combate

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

Quiloa, Mombaça, Quilon e outras ações militares de 1505 podem permanecer:

- eventos históricos específicos;
- transições de fortificação/guarnição quando produzem estado persistente.

O jogador não recebeu uma nova decisão militar funcional cujo resultado exija resolução de combate. Portanto T4 fecha, para o horizonte 1505, sem motor geral de combate.

### Múltiplas frotas simultâneas

`MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO`

A armada de Almeida e a expedição separada de Pêro de Anhaia podem coexistir como unidades históricas distintas sem exigir duas `active_expedition_id` no mesmo save, desde que permaneçam documentais/sem pernas quando não houver loop controlável.

## 2. Expedições mínimas

### `EXP_ALMEIDA_1505`

Criar em `expeditions.csv`:

- líder: D. Francisco de Almeida;
- autoridade: Coroa portuguesa;
- período: 1505–1509 ou, se o catálogo preferir horizonte da viagem inicial, 1505–1506; decidir conforme convenção já usada em `period_to`;
- tipo: `ROYAL_EXPEDITION_VICEROYAL_MISSION` ou equivalente sem criar enum rígido de governo;
- partida: 25/03/1505 documentada em eventos/notas;
- `fleet_size`: **não normalizar**; divergência 20 × 21 × 22 × 23 preservada;
- financiamento privado: registrar em notas/proveniência, sem novo sistema econômico;
- protagonista não fixo.

### `EXP_ANHAIA_1505`

Criar separadamente:

- líder: Pêro de Anhaia;
- partida: 18/05/1505;
- missão: Sofala;
- período: 1505–1506;
- tipo: `ROYAL_FORTIFICATION_MISSION` ou equivalente;
- sem pernas executáveis na primeira implementação, salvo necessidade posterior.

## 3. Eventos de autoridade de Almeida

### `ALM1505_E01 — ROYAL_APPOINTMENT`

- data: 27/02/1505;
- sujeito: Francisco de Almeida;
- função: nomeação/poder régio como capitão-mor e missão por três anos;
- não altera nenhum nó.

### `ALM1505_E02 — ROYAL_REGIMENT_ISSUED`

- data: 03/03/1505;
- função: Regimento/programa de governo, diplomacia e fortificação;
- documental; não cria automaticamente todos os fortes previstos.

### `ALM1505_E03 — FLEET_DEPARTURE`

- data: 25/03/1505;
- origem: `LIS`;
- destino vazio até que a campanha seja normalizada;
- `EXACT`.

### `ALM1505_E04 — VICEROYAL_AUTHORITY_ACTIVE_IN_INDIA`

- janela: outubro de 1505;
- `RANGE`, não `EXACT`, enquanto a adoção/titulação em Cananor permanecer dependente de tradição cronística divergente;
- efeito institucional narrativo, sem schema global novo.

### `ALM1505_E05 — PRESENCE_IN_COCHIN`

- data segura: 16/12/1505;
- destino/local: `COC`;
- `EXACT` para presença documental, com base em carta de Almeida escrita em Cochim;
- não precisa representar a chegada diária se 31/10 continuar apenas candidato cronístico.

## 4. Cronologia operacional de Almeida — o que pode ser normalizado

### África Oriental — forte

O relato contemporâneo de Hans Mayr permite eventos exatos:

- 20/06 — dobra do Cabo;
- 18/07 — avistamento de terra pós-Cabo;
- 19/07 — à vista de Moçambique;
- 21/07 — baixos de São Rafael;
- 22/07 — entrada em Quiloa;
- 24/07 — desembarque/ocupação em Quiloa;
- 09/08 — saída de Quiloa;
- 13/08 — chegada do capitão-mor a Mombaça;
- 14/08 — chegada do `São Rafael` a Mombaça.

Esses marcos podem entrar em `expedition_events.csv` sem necessariamente criar pernas jogáveis.

### Índia — prudência

- Anjediva: setembro seguro; 13/09 permanece candidato diário;
- Cananor: outubro seguro; início da fortificação em 23/10 é candidato forte sustentado por cronologia crítica de Góis;
- Cochim: presença segura até 16/12; chegada 31/10 permanece candidato até fonte contemporânea equivalente.

Nenhum `voyage_observation` diário deve ser criado apenas para preencher a travessia Índia/Malabar.

## 5. Estados persistentes de nó

O schema atual `node_state_events.csv` é suficiente.

### `KIL` — Quiloa

Adicionar estados temporais a partir da fase de 22–24/07/1505, preferencialmente aplicados após o marco de 24/07 se a intenção for representar o resultado consolidado:

- presença institucional portuguesa residente;
- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- relação política alterada/coerciva, sem converter automaticamente em soberania portuguesa;
- soberania/autoridade local deve registrar soberano apoiado/imposto, mas não anexação.

Não normalizar número de homens ou peças de artilharia.

### `MOM` — Mombaça

Não criar estado persistente novo nesta tranche.

O ataque/saque/incêndio pertence a `expedition_events`; não há fortificação ou guarnição portuguesa permanente demonstrada em `31/12/1505`.

### `SOF` — Sofala

Adicionar estados temporais:

- presença institucional/feitoria portuguesa;
- fortificação portuguesa;
- guarnição residente;
- soberania local não convertida automaticamente em portuguesa.

Âncoras:

- 04/09/1505 — Pêro de Anhaia como Capitão de Sofala, EVE;
- 21/09/1505 — início da tranqueira, HPIP.

A divergência 21/09 × 25/09 deve permanecer documentada; preferir 21/09 na primeira normalização por fonte patrimonial especializada, salvo revisão posterior.

### `ANJ` — Anjediva

Adicionar estados temporais ainda em setembro de 1505:

- fortificação portuguesa;
- presença/guarnição portuguesa.

Como os dias 13–14/09 ainda não possuem, nesta auditoria, sustentação equivalente às âncoras de Sofala/Quiloa, usar inicialmente uma janela conservadora:

`1505-09-01 → 1505-09-30`, `RANGE`.

Pela regra do modelo, o estado ficará seguramente efetivo em 30/09.

Não transformar Anjediva em soberania territorial portuguesa sem auditoria específica; registrar presença fortificada.

### `CAN` — Cananor

Adicionar:

- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- manutenção da feitoria já existente;
- soberania local preservada;
- acesso negociado;
- relação sob tensão, sem `HOSTILE` automático.

Temporalidade proposta:

- fortificação: 23/10/1505 `EXACT` **se** a implementação aceitar a cronologia crítica de Góis como suficiente;
- alternativa conservadora: 23–31/10 `RANGE`;
- guarnição: mesma janela ou janela separada de fim de outubro, sem número de homens.

### `COC` — Cochim

Não criar nova fortificação/guarnição: ambas já existem desde 1503.

Não alterar soberania.

Centralidade administrativa de 1505 deve ser registrada como evento institucional ligado a Almeida, não como novo campo do nó nesta primeira implementação.

## 6. Sucessão nominal em Cochim

Preservar explicitamente:

`Manuel Teles de Vasconcelos × Manuel Teles Barreto = UNRESOLVED`

Não criar comandante nominal no estado do nó se o domínio não o consome.

A divergência não bloqueia o freeze porque o estado funcional relevante é a existência da guarnição, já resolvida desde 1503.

## 7. Pêro de Anhaia e a independência de Sofala

`EXP_ANHAIA_1505` deve possuir seus próprios eventos:

- partida em 18/05;
- assunção como Capitão de Sofala em 04/09;
- início da fortificação em 21/09;
- consolidação da presença até o fim de 1505.

Não atribuir esses efeitos à expedição de Almeida apenas porque ambas pertencem ao programa régio de 1505.

## 8. Eventos militares guiados

Manter como eventos específicos, sem combate geral:

- tomada de Quiloa;
- ataque/saque de Mombaça;
- ações em Quilon/Coulão;
- patrulhas e ações navais de Lourenço de Almeida;
- outros confrontos somente se necessários ao estado final.

Não criar:

- HP;
- dano;
- moral;
- baixas como parâmetros;
- força quantitativa;
- microtática;
- sistema probabilístico de batalha.

## 9. Novos nós

Nenhum novo nó é indispensável para o primeiro F5 funcional.

Reutilizar:

- `KIL`;
- `MOM`;
- `SOF`;
- `ANJ`;
- `CAN`;
- `COC`.

Quilon/Coulão continua fora do grafo salvo necessidade funcional demonstrada por algum evento que não possa ser representado documentalmente.

## 10. Estado alvo de `31/12/1505`

O freeze deve conseguir resolver, no mínimo:

### Cochim

- soberania local;
- feitoria portuguesa;
- Forte Manuel;
- guarnição portuguesa;
- centralidade/base da autoridade de Almeida representada documentalmente;
- sem anexação territorial.

### Cananor

- soberania local;
- feitoria portuguesa;
- fortificação portuguesa nova de 1505;
- guarnição portuguesa;
- acesso negociado.

### Anjediva

- fortificação portuguesa;
- presença/guarnição portuguesa;
- sem necessidade de mercado/serviços novos por inferência.

### Quiloa

- fortificação portuguesa;
- força residente;
- soberano local sob intervenção/apoio português, sem converter automaticamente a ilha em posse territorial plena no schema.

### Sofala

- feitoria/presença institucional portuguesa;
- fortificação/tranqueira;
- guarnição/capitania de Pêro de Anhaia;
- soberania local/hinterland não apagada.

### Mombaça

- sem fortificação/guarnição portuguesa persistente apenas por efeito do ataque de agosto.

## 11. Testes mínimos da futura F5 funcional

1. nenhuma fortificação de 1505 aparece em campanhas anteriores;
2. `KIL`, `SOF`, `ANJ`, `CAN` resolvem os novos estados apenas após suas janelas;
3. `COC` mantém soberania local e estados de 1503;
4. `MOM` não ganha fortificação/guarnição por causa do saque;
5. `EXP_ALMEIDA_1505` e `EXP_ANHAIA_1505` podem existir sem pernas se a rota não for jogável;
6. autoridade vice-real não vaza retroativamente para fevereiro/janeiro ou para outras campanhas;
7. save/load em `31/12/1505` produz o mesmo estado mundial;
8. regressão integral 1497–1504 verde;
9. nenhum sistema de combate é introduzido;
10. golden state de `31/12/1505` pode ser gerado para o freeze.

## 12. Decisão T4 final para Python 1505 GREEN

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

O horizonte 1500–1505 demonstrou violência e campanhas militares crescentes, mas não demonstrou ainda uma decisão controlável do jogador que exija resolução sistêmica de combate para reproduzir os estados históricos necessários.

Combate permanece candidato pós-freeze somente se o desenho de jogo posterior decidir tornar o comando militar uma camada controlável.

## 13. Critério de fechamento do F5-doc

O gate documental pode ser encerrado quando:

- esta proposta mínima for revisada contra os documentos anteriores;
- fontes e divergências estiverem registradas;
- issue #132 receber checkpoint de fechamento;
- Diário do Drive estiver sincronizado;
- branch documental for integrada sem alteração em `data/`, `simulation/` ou `src/`;
- somente então abrir F5 funcional.
