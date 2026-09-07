# P1-ui — interface histórica do retorno 1498–1499

Issue: #102.

## Objetivo

Expor na interface histórica v0.2 a continuidade opt-in do MVP Calecute até os Baixos do Rio Grande, preservando o encerramento original Lisboa–Calecute e sem transformar atos específicos da expedição em serviços portuários genéricos.

## Implementação

- `M5HistoricalCampaignPrototype` passou a orquestrar `ReturnCampaignModel`, que herda integralmente o baseline de `HistoricalCampaignModel`.
- O MVP continua concluído pela primeira operação comercial elegível em Calecute. A subcampanha de retorno só é ativada por ação explícita do jogador.
- A interface apresenta a sequência documental `CAL→SMI→ANJ→MAL→BSR→SBR→CGH→BRG`.
- Em SMI, a interface oferece uma única aquisição alimentar específica do contato registrado no Roteiro. A regra continua `SIMULATION`, limitada a 5 dias-equivalentes e sem consumo de dia inteiro.
- Em ANJ, a interface expõe provisões específicas da permanência e carena documental. A ação de carena usa a referência mínima testada de 2 pontos abstratos de condição.
- Serviços genéricos de `nodes.csv` permanecem inalterados; SMI não recebe mercado e ANJ continua com disponibilidade genérica de provisões/reparo `UNKNOWN`.
- O epílogo posterior a BRG/25-04-1499 continua fora do loop jogável.

## Persistência

Ações one-shot não exigiram alteração de schema. Identificadores `RETURN_ACTION:<stop_id>:<action>` são registrados no `information_history`, campo já persistido no schema v2. Assim, save/load conserva o uso da oportunidade alimentar de Santa Maria e da carena de Anjediva sem criar estado paralelo de interface.

O teste `tests/test_return_persistence.py` verifica, durante o retorno, preservação de:

- seed;
- `active_expedition_id`;
- `expedition_leg_sequence`;
- `active_stop_id`;
- `chronology_mode`;
- localização;
- indisponibilidade pós-load de uma ação one-shot já utilizada.

## Validação

O run 34117947847 validou a interface com smoke completo até BRG, além de validação de dados, testes de domínio, diagnósticos do retorno, interface histórica anterior, M6, mapa e cartografia.

A workflow passou a executar também:

`python prototype/game_m5.py --return-smoke --output /tmp/quintoimperio-interface-v02-brg.png`

O smoke percorre a campanha do MVP, ativa explicitamente o retorno pela mesma fachada da interface, executa as ações documentais contextuais e exige término em BRG em 1499-04-25 mantendo `GUIDED`.

## Critérios de aceite da #102

1. continuação opt-in em Calecute: atendido;
2. sete pernas do retorno na interface: atendido;
3. SMI como oportunidade alimentar específica, sem mercado/serviço genérico: atendido;
4. ANJ com provisões e carena específica: atendido;
5. ação de SMI não repetível, inclusive após save/load: atendido;
6. `UNKNOWN/NONE` genérico preservado: atendido;
7. epílogo pós-BRG fora do loop: atendido;
8. save/load durante o retorno: atendido por teste dedicado;
9. smoke de interface completo até BRG: atendido;
10. documentação GitHub/Drive: este documento e atualização do diário de desenvolvimento.

## Decisão

Com CI final verde da branch `p1-ui-102`, a #102 pode ser encerrada e a branch integrada ao `main`. O gate funcional #99 passa então a ter critérios suficientes para encerramento, mantendo doença/mortalidade sistêmica, frota geral, epílogo pós-BRG e P2/Cochim fora deste escopo.
