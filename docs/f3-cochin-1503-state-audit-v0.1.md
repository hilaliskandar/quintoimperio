# F3 — Cochim 1503 — auditoria de estados temporais v0.1

Data: 2026-09-08
Issue: #127
Baseline: `318f27c9a101f55626d2fc9e18cc8c85cffe9e89`

## Objetivo

Confrontar `node_state_events.csv` e `NodeStateEventModel` com a matriz documental de #114 antes de criar novas estruturas funcionais.

## Resultado arquitetural

O schema atual já representa separadamente:

- presença institucional;
- fortificação;
- guarnição;
- acesso;
- relação;
- soberania;
- aplicação conservadora de intervalos no limite superior.

Portanto, F3 não demonstra neste ponto necessidade de novo schema territorial nem de duplicar `COC` por período.

## Estados já normalizados

### Crise de abril

`COC1503_E01` representa a ofensiva de Calecute e o deslocamento temporário do rajá/portugueses, com `FACTORY_DISPLACED`, acesso `DISRUPTED` e `HOSTILE_PRESSURE`. O evento é uma janela de abril e só se torna efetivo em 30/04, preservando a regra conservadora.

Vaipim permanece na nota histórica como local de refúgio. Isso é suficiente enquanto nenhuma ação do jogador exigir navegação, mercado ou decisão própria naquele local.

### Restauração de setembro

`COC1503_E02` representa a restauração da autoridade local em setembro, com soberania explicitamente mantida pelo rajá. A janela termina em 30/09 e o efeito só é aplicado nessa data.

### Fortificação

`COC1503_E03` estava codificado como `27/09–31/12/1503`. Com a regra conservadora do resolver, isso fazia o Forte Manuel aparecer apenas em 31/12, apesar de a matriz documental situar decisão/fundação em setembro e registrar 27/09 como referência cronística de trabalho.

A data de 27/09 não deve ser tratada como testemunho primário equivalente a fonte contemporânea, mas também não há fundamento para postergar a fortificação até 31/12.

Decisão: usar janela `27/09–30/09/1503`, `RANGE`, evidência B. Assim:

1. não se afirma que 27/09 seja data primária exata;
2. a fortificação não antecede conservadoramente o limite superior da janela de restauração;
3. em 30/09, a ordenação por `event_id` aplica primeiro `COC1503_E02` e depois `COC1503_E03`, resultando em autoridade local restaurada + feitoria + fortificação portuguesa;
4. soberania continua local.

### Guarnição

`COC1503_E04` permanece `01/10–31/12/1503`, `RANGE`, e só se torna efetivo em 31/12. Isso é coerente com a evidência disponível de “fim de 1503” para Duarte Pacheco permanecer com pequena força e duas caravelas.

## Sequência de estado esperada

- `1503-04-29`: estado anterior à crise ainda prevalece;
- `1503-04-30`: crise/deslocamento efetivos;
- `1503-09-29`: crise ainda prevalece pela regra conservadora da janela de restauração;
- `1503-09-30`: autoridade local restaurada + feitoria restaurada + Forte Manuel estabelecido; sem guarnição consolidada ainda;
- `1503-12-30`: forte permanece, guarnição ainda não consolidada pelo intervalo documental;
- `1503-12-31`: forte + guarnição portuguesa sob soberania local.

## Persistência

Esses estados são funções determinísticas de `node_id + data` sobre dados históricos versionados. Não precisam ser duplicados no save enquanto não houver decisões contrafactuais que modifiquem o estado objetivo do mundo. O teste correto de persistência é provar que uma sessão salva/restaurada conserva a data e, ao consultar o mesmo `NodeStateEventModel`, resolve o mesmo estado histórico.

## Próximo subgate

1. corrigir somente a janela de `COC1503_E03`;
2. criar testes de transição para as datas sentinela acima;
3. testar resolução idêntica antes/depois de save/load;
4. somente depois auditar se as três armadas de 1503 precisam ser campanhas executáveis ou se seus efeitos podem permanecer em `expedition_events`/`node_state_events`.