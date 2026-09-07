# P1-func — desenho funcional mínimo v0.1

Issue: #99.

## Resultado da auditoria do domínio

O domínio existente já é genérico por `expedition_id`. `ExpeditionModel` lê qualquer sequência normalizada em `expedition_routes.csv`; `GameSessionState` já armazena expedição e perna ativas; `FLEET_COMMAND`, cronologia guiada, observações de viagem e `ExpeditionStopModel` não dependem de `EXP_GAMA_1497`.

Portanto, o retorno não exige refatorar o domínio central nem anexar as seis novas pernas à expedição de ida.

## Transição proposta

A expansão deve ser opt-in. O MVP continua encerrando em Calecute com `active_expedition_id=None`. Uma fachada pós-MVP ativa explicitamente `EXP_GAMA_RETURN_1498` sobre o mesmo estado somente quando:

- o personagem está em `CAL`;
- nenhuma expedição está ativa;
- a expansão do retorno é escolhida.

Se a ativação ocorrer depois da data documentada de partida de 30/08/1498, a cronologia passa a `COUNTERFACTUAL`; caso contrário, pode continuar `GUIDED` e a espera normal sincroniza a partida.

## Permanências documentadas sem serviço portuário genérico

Anjediva é o caso metodologicamente decisivo: `nodes.csv` preserva `provisions=UNKNOWN`, porque os atos de água, madeira, alimento e carena são específicos da expedição e não demonstram uma disponibilidade portuária geral. Logo, `PortServiceModel.reprovision()` deve continuar bloqueado em ANJ.

Para a campanha de retorno, uma ação separada pode usar `expedition_stops.csv` como autorização histórica específica. Essa ação:

- existe somente enquanto há `active_stop_id`;
- exige atividade documental de provisões/alimentos na escala;
- usa capacidade e duração exclusivamente de `simulation/return_rules.csv`;
- nunca altera `nodes.csv`;
- nunca converte `UNKNOWN` em LOW/MEDIUM/HIGH;
- nunca concede recursos automaticamente;
- continua sujeita ao limite abstrato de provisões embarcadas já usado no MVP.

Assim, fato histórico e efeito de jogo permanecem separados: a fonte autoriza que houve aquisição/preparação de mantimentos naquela permanência; a quantidade abstrata adicionada por ação continua sendo `SIMULATION`.

## Eventos fora deste incremento

A queima do S. Rafael continua registrada como atividade documental `SHIP_ABANDONMENT|CARGO_TRANSFER` no stop BSR. Ela não altera ainda um estado genérico de frota porque o loop atual opera com `VesselState` abstrato. Doença e mortalidade permanecem igualmente fora do domínio operacional.

## Gate técnico

O primeiro incremento deve acrescentar:

1. fachada `ReturnCampaignModel`, sem mudar `HistoricalCampaignModel`;
2. ativação explícita do retorno sobre estado concluído em Calecute;
3. ação de reabastecimento específica de permanência documentada, parametrizada em `simulation/return_rules.csv`;
4. testes que preservem o encerramento do MVP e provem que `nodes.csv` continua sem serviço genérico inventado;
5. smoke de seis pernas até BRG.

Depois desse incremento, uma bateria sintética deve testar a continuidade a partir de estados reais de conclusão do MVP, em vez de recalibrar antecipadamente a logística.