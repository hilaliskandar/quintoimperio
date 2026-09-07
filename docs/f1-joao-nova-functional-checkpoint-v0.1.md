# F1 — João da Nova 1501–1502 — checkpoint funcional v0.1

Data: 2026-09-07
Issue: #120
Gate-mãe: #118

## Estado do checkpoint

Primeira tranche funcional estabilizada até o marco do bloqueio de Cananor em 30/12/1501.

CI de referência: GitHub Actions run `34164256752` — `success`.

## Implementado

1. auditoria cronológica com classes `EXACT`, `INTERVAL`, `DERIVED` e `UNRESOLVED`;
2. ordem funcional da expedição:
   `LIS → SBR → KIL → MAL → ANJ → CAN → COC → CAN`;
3. sete rotas específicas de João da Nova, sem reutilizar datas de Cabral;
4. nenhuma nova linha em `voyage_observations.csv` para pernas sem timing diário defensável;
5. duração dessas pernas calculada pelo motor como simulação, mantendo `ChronologyMode.GUIDED`;
6. aviso de Cabral em São Brás como aquisição one-shot de informação da expedição;
7. `SBR→KIL` bloqueada em modo guiado enquanto o aviso não tiver sido adquirido;
8. Calecute ausente da sequência operacional após o aviso;
9. feitoria de Cananor preservada como estado temporal de fim de 1501, sem fortificação, guarnição ou soberania portuguesa;
10. `NOVA1501_E03` registra apenas o início exato do bloqueio naval em Cananor em 30/12/1501, sem sistema geral de combate;
11. sincronização explícita com 30/12 após a sequência comercial simulada, sem tratar essa data como chegada a Cananor;
12. round-trip de persistência preserva aviso, progresso de expedição, data e cronologia.

## Decisões metodológicas

- ordem histórica de escalas não equivale a cronologia diária;
- ausência de `voyage_observation` não converte automaticamente a campanha em contrafactual;
- timing calculado pelo motor nessas pernas é `SIMULATION` e não observação histórica;
- o marco 30/12 representa presença da armada em Cananor e início do bloqueio, não uma data inventada de chegada;
- a feitoria é aplicada conservadoramente no limite superior da janela de fim de 1501, 31/12;
- Ceilão permanece fora;
- confronto de Cananor continua evento específico, sem combate geral.

## Testes acrescentados

- primeira perna sem observação diária permanece `GUIDED` e usa `FLEET_COMMAND`;
- chegada simulada a São Brás cai dentro da janela documental do aviso;
- segunda perna é bloqueada até aquisição do aviso;
- ordem das sete pernas evita Calecute;
- temporalidade da feitoria de Cananor não retroage;
- bloqueio de Cananor só aparece em 30/12;
- smoke da sequência comercial completa até Cananor;
- sincronização ao marco de 30/12;
- persistência do aviso e do estado final do checkpoint.

## Próximo subgate F1

Auditar a torna-viagem de 1502. O retorno só deve ser normalizado no grau em que houver sequência e timing defensáveis. Descobertas/atribuições atlânticas controversas não devem ser materializadas por conveniência. Se a documentação não sustentar uma campanha guiada diária de retorno, F1 pode encerrar funcionalmente no marco de Cananor e registrar o retorno a Lisboa como epílogo/intervalo, preservando a lacuna para pesquisa posterior.