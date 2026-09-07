# P1-func — sensibilidade da carena documentada em Anjediva

Issue: #101.

Run de referência: `34116111181`.
Commit: `72e2451a721eb5eb9791e026bcc7df1b213ba7fe`.

## Problema

Na wave17, cinco casos da seed `23004` herdaram do MVP condição `47,49` e, sem eventos estocásticos adicionais no retorno, chegaram a São Brás com `19,99`, bloqueando a continuação por `VESSEL_CONDITION_TOO_LOW`.

A permanência em Anjediva registra `CARENING` no `Roteiro`. A atividade documental já estava em `expedition_stops.csv`, mas não tinha efeito jogável. A implementação mantém `nodes.csv` com `repair=UNKNOWN` e projeta a carena somente como ação específica da permanência ativa. Existência da ação = evidência histórica; magnitude e duração = `SIMULATION`.

## Sensibilidade

Foram repetidos os cinco arquétipos competentes na mesma seed `23004`, congelando todas as demais regras. Testaram-se restaurações abstratas de `0`, `1`, `2`, `5` e `10` pontos na carena de Anjediva.

| Restauração | Conclusões até BRG | Resultado |
|---:|---:|---|
| 0 | 0/5 | bloqueio em São Brás |
| 1 | 0/5 | ultrapassa São Brás, mas bloqueia no Cabo |
| 2 | 5/5 | conclui em BRG |
| 5 | 5/5 | sem ganho de conclusão adicional |
| 10 | 5/5 | sem ganho de conclusão adicional |

Com 2 pontos, todos chegam a BRG em `1499-04-25`, mantendo `GUIDED`. A condição final pode ficar abaixo do limiar de nova partida, o que não interfere neste gate porque BRG é o limite jogável da narrativa primária.

## Decisão

A referência mínima para os próximos testes é **2 pontos abstratos de condição** em uma ação explícita de carena documentada em Anjediva. Esse número não é apresentado como intensidade histórica de reparo; é o menor parâmetro de simulação testado que restaura agência no conjunto crítico.

A implementação não altera:

- `nodes.csv`;
- disponibilidade portuária genérica de reparo;
- desgaste das rotas;
- probabilidades ou severidades de eventos;
- limiar `VESSEL_CONDITION_TOO_LOW`;
- cronologia documentada.

## Próximo controle

Executar o painel completo da wave17 com as mesmas seeds e arquétipos, aplicando a carena mínima de 2 pontos quando a permanência documental a oferecer. O esperado é eliminar exclusivamente os cinco blockers estruturais, deixando visível a lacuna independente Calecute→Anjediva.