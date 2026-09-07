# P3-func-A — checkpoint funcional de Melinde

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`

## Estado alcançado

A campanha de Pedro Álvares Cabral está executável, em modo guiado, de Lisboa até Melinde:

1. `LIS → VCR`, 09/03/1500 → 22/04/1500, 44 dias;
2. permanência em Vera Cruz até 02/05/1500;
3. `VCR → MOZ`, 02/05/1500 → 20/07/1500, 79 dias, agregando operacionalmente a passagem pelo Cabo sem criar escala artificial;
4. `MOZ → KIL`, 20/07/1500 → 26/07/1500, 6 dias;
5. permanência em Quiloa até 29/07/1500;
6. `KIL → MAL`, 29/07/1500 → 02/08/1500, 4 dias;
7. permanência em Melinde até 07/08/1500.

## Correção de baseline

Durante a atualização de `data/expedition_routes.csv`, uma nota antiga da perna `R_RCO_RBS` foi alterada mecanicamente sem necessidade. O texto original foi restaurado no commit `2433c73652160ec765b4f3562b2787b8f3e4d212`. Nenhuma regra ou dado histórico do baseline foi modificado por essa correção.

## Melinde

A escala `CABRAL1500_MAL` registra:

- chegada em 02/08/1500;
- desembarque de dois degredados em 06/08;
- obtenção de dois pilotos guzerates em 06/08;
- partida em 07/08.

O evento `CABRAL1500_E08` preserva a formulação plural `Dois pilotos guzerates` e o tipo `PILOTS_PROVIDED`.

Os dois pilotos **não** foram convertidos em uma única entidade operacional. O domínio atual trata `pilot_id` como indivíduo e `recommended_pilot_id()` seleciona apenas um piloto elegível. Também não foi reutilizado `PIL_MAL_GUJ_1498`, cujo período e contexto pertencem à viagem de Vasco da Gama de 1498.

A eventual normalização dos pilotos de 1500 depende da identificação da rota que efetivamente guiaram e de uma decisão explícita sobre como representar duas pessoas não identificadas sem escolha arbitrária de uma delas pelo mecanismo de recomendação.

## Teste e CI

O teste P3 percorre agora Lisboa → Vera Cruz → Moçambique → Quiloa → Melinde e verifica:

- bloqueio de partidas antes da liberação das escalas documentadas;
- cronologias observadas de 44, 79, 6 e 4 dias;
- ativação das escalas de Vera Cruz, Quiloa e Melinde;
- ausência de uso do piloto de 1498 na perna de 1500;
- permanência dos dois pilotos de Cabral como evento documental.

O run `34135150929`, commit `957b930b1388a338243c476ae6b8236c1a17acd4`, terminou integralmente verde: validação dos dados, testes de domínio, regressões do MVP e retorno, interfaces, persistência e cartografia.

## Próxima lacuna real

O corpus interno sustenta:

- partida de Melinde em 07/08/1500;
- costa da Índia alcançada em 22/08/1500;
- cerca de duas semanas em Anjediva no fim de agosto/início de setembro;
- chegada a Calecute em 13/09/1500.

Ele **não** fornece ainda datas suficientemente firmes de chegada e partida em Anjediva. Não se deve inferi-las por aritmética reversa a partir da chegada a Calecute ou da expressão `cerca de duas semanas`.

## Próximo gate

1. pesquisar apenas a lacuna cronológica Melinde → costa indiana → Anjediva → Calecute em fontes já selecionadas e, se necessário, em fonte especializada adicional;
2. se não houver datas firmes para Anjediva, preservar a escala como evento intermediário e escolher uma agregação operacional explicitamente documentada, sem datas inventadas;
3. somente depois conectar a chegada a Calecute e projetar a ruptura de dezembro nas camadas temporais existentes;
4. manter combate, naufrágio e múltiplas frotas como eventos específicos até necessidade funcional demonstrada.
