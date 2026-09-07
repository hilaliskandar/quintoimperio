# P3-func-A — checkpoint Cabral até Calecute

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`

## Recorte executável

A campanha de Pedro Álvares Cabral está executável em modo `GUIDED` de Lisboa até Calecute:

1. `LIS → VCR`: 09/03 → 22/04/1500, 44 dias;
2. escala de Vera Cruz: 22/04 → 02/05;
3. `VCR → MOZ`: 02/05 → 20/07, 79 dias, com o Cabo preservado como marco documental intermediário;
4. `MOZ → KIL`: 20/07 → 26/07, 6 dias;
5. escala de Quiloa: 26/07 → 29/07;
6. `KIL → MAL`: 29/07 → 02/08, 4 dias;
7. escala de Melinde: 02/08 → 07/08;
8. `MAL → ANJ`: 07/08 → 22/08, 15 dias;
9. escala de Anjediva: 22/08 → 05/09, 14 dias;
10. `ANJ → CAL`: 05/09 → 13/09, 8 dias.

## Tratamento de Anjediva

A cronologia de Oliveira e Costa fixa 22/08 para a chegada à costa indiana e cerca de duas semanas em Anjediva. Greenlee identifica Anjediva como a terra alcançada. A combinação permite usar 22/08 como chegada de trabalho com grau B.

A data de 05/09 não é apresentada como data primária. Ela é uma **derivação operacional explícita** de 14 dias a partir de 22/08, necessária ao modo guiado. A chegada a Calecute em 13/09 permanece documentalmente firme.

A regra correspondente foi acrescentada a `docs/sources.md`: reconstruções operacionais desse tipo devem permanecer identificadas como tais e não recebem automaticamente grau A.

## Pilotos de 1500

Os dois pilotos guzerates recebidos em Melinde continuam registrados em `CABRAL1500_E08` como evento documental. Não foi reutilizado o piloto de 1498 e não foi criada entidade coletiva artificial. A perna `MAL → ANJ` continua autorizada por `FLEET_COMMAND`, preservando a existência dos pilotos sem obrigar o domínio a escolher arbitrariamente um indivíduo não identificado.

## Preservação do baseline

Durante as edições foi detectada e restaurada uma alteração mecânica não intencional em uma nota antiga de `expedition_routes.csv`. Também foi restaurado imediatamente o `observation_scope` original de `GAMA1499_RET_BSR_SBR`. Esses reparos não mudaram regras ou dados históricos do baseline; foram feitos para impedir deriva documental durante a expansão.

## CI

O run `34135764925`, commit `3c360f03f8ef287b4dc83dfe513504b82de8ddac`, passou integralmente:

- validação dos CSVs;
- testes de domínio;
- protótipos;
- regressão MVP Lisboa–Calecute;
- retorno até BRG e diagnósticos;
- interfaces;
- persistência;
- cartografia.

A campanha chega a Calecute em 13/09/1500 ainda em `ChronologyMode.GUIDED`.

## Próximo gate

A ruptura de dezembro será projetada em duas camadas já existentes:

1. `expedition_events.csv` conserva ataque à feitoria, perdas, retaliação e bombardeio como eventos históricos específicos;
2. `node_state_events.csv` deve representar perda da presença institucional portuguesa e relação/acesso hostis em Calecute sem criar sistema geral de combate.

A próxima perna será `CAL → COC` apenas com cronologia explicitamente justificada. A chegada a Cochim em 24/12 é firme; eventual data operacional de saída de Calecute deverá ser marcada como reconstrução se derivada da janela da crise.
