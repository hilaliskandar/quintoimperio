# F3 — convergência das forças de 1503 no Índico v0.1

Data: 2026-09-08
Issue: #127
Baseline: `318f27c9a101f55626d2fc9e18cc8c85cffe9e89`

## Pergunta

A convergência das armadas de Afonso de Albuquerque, Francisco de Albuquerque e dos remanescentes de Pêro de Ataíde exige normalizar itinerários jogáveis em F3?

## Evidência

A EVE/FCSH sustenta a seguinte cadeia mínima:

1. os remanescentes da força de Vicente Sodré, já sob Pêro de Ataíde, não conseguem regressar imediatamente ao Malabar e permanecem em Anjediva;
2. em Anjediva, Ataíde é encontrado pelas armadas de 1503 comandadas por Francisco e Afonso de Albuquerque;
3. os navios remanescentes são incorporados à força dos Albuquerque;
4. essa força participa da expulsão das tropas de Calecute que haviam invadido o reino de Cochim;
5. a chegada das armadas de Francisco e Afonso em setembro de 1503 permite recuperar Cochim;
6. em seguida inicia-se a construção de uma fortaleza e é preparada uma força residente sob Duarte Pacheco Pereira.

A biografia de Duarte Pacheco Pereira confirma sua presença na armada de 1503, a chegada ao contexto de Cochim ocupado pelas forças do Samorim, a expulsão do adversário, a restituição da cidade ao aliado local e o início da fortificação. Registra ainda que Duarte Pacheco permanece no Oriente com duas caravelas.

## Grau de resolução

- encontro Ataíde–Albuquerque em Anjediva: `INTERVAL`, ordem e local firmes, sem dia consolidado neste gate;
- chegada das armadas de Francisco/Afonso ao Malabar/Cochim em setembro: `INTERVAL`;
- expulsão das forças de Calecute e restauração da autoridade local: `INTERVAL`, já representada em `COC1503_E02`;
- início do Forte Manuel em setembro: `INTERVAL`, já representado por `COC1503_E03` com janela conservadora 27–30/09;
- permanência de Duarte Pacheco com duas caravelas ao fim de 1503: `INTERVAL`, já representada por `COC1503_E04`.

## Decisão funcional

F3 **não precisa normalizar rotas executáveis para as três armadas de 1503** para representar corretamente o ciclo de Cochim.

A cadeia causal necessária ao jogo está suficientemente expressa por:

- registros históricos distintos em `expeditions.csv`;
- documentação da convergência em Anjediva;
- estados temporais de Cochim em abril, setembro e dezembro;
- soberania local preservada separadamente de fortificação/guarnição portuguesas.

Não será criado evento `ANJ→COC` com duração ou data diária arbitrária apenas para conectar visualmente os registros. Também não será criado um `EXP_1503_COMBINED`, pois isso apagaria a distinção entre as partidas independentes.

## António de Saldanha

A armada de Saldanha permanece registrada como expedição histórica separada, mas não é necessária para a cadeia funcional mínima que explica a recuperação e fortificação de Cochim neste gate. Sua missão não será comprimida artificialmente no loop dos Albuquerque.

## Combate

A expulsão das forças de Calecute é um resultado histórico necessário à transição de estado, mas a F3 não demonstrou necessidade de:

- resolução probabilística de batalha;
- unidades táticas;
- parâmetros de força/dano/moral;
- escolha de combate que altere o resultado histórico no modo guiado.

Logo, o episódio permanece evento/estado histórico específico. A decisão sobre combate funcional deve ser reavaliada em F4, onde a defesa de Cochim em 1504 é prolongada e repetida.

## Conclusão arquitetural

F3 fecha a questão das campanhas de 1503 com uma distinção explícita:

- **catálogo histórico**: três expedições separadas;
- **trajetória documental**: convergência de Afonso/Francisco + remanescentes de Ataíde;
- **estado mundial funcional**: crise → restauração → forte → guarnição;
- **campanha jogável**: não necessária nesta tranche.

Isso preserva a arquitetura de um único `active_expedition_id` e evita criar rotas ou mecânicas gerais sem necessidade demonstrada.

## Fontes complementares

- EVE/FCSH, “Pedro de Ataíde”;
- EVE/FCSH, “Cochim”;
- EVE/FCSH, “Duarte Pacheco Pereira”;
- `docs/p3-4-1503-evidence-v0.1.md` e proposta mínima associada.

## Gate seguinte

Se a CI do registro das armadas permanecer verde, F3 pode avançar para closeout: consolidar testes sentinela de estado, persistência e ausência de campanhas executáveis 1503; auditar o diff contra `main`; integrar e entregar a F4/#115 o baseline de 31/12/1503 com Cochim sob soberania local, forte e guarnição portugueses.