# F3 — armadas de 1503 — auditoria de registro e jogabilidade v0.1

Data: 2026-09-08
Issue: #127
Baseline: `318f27c9a101f55626d2fc9e18cc8c85cffe9e89`

## Pergunta

As partidas de Afonso de Albuquerque, Francisco de Albuquerque e António de Saldanha em abril de 1503 devem ser registradas em `expeditions.csv` e, se registradas, precisam receber pernas/loops jogáveis nesta tranche?

## Evidência

A listagem `EVE_ARMADAS_MANUEL` distingue três partidas:

- 06/04/1503 — Afonso de Albuquerque, capitão-mor; Duarte Pacheco Pereira e Fernão Martins de Almada como capitães;
- 14/04/1503 — Francisco de Albuquerque, capitão-mor; a listagem também registra Pedro Vaz da Veiga como capitão-mor e Nicolau Coelho como capitão;
- 15/04/1503 — António de Saldanha, capitão-mor; Diogo Fernandes Pereira e Rui Lourenço Ravasco como capitães.

A matriz P3.4 já determina que essas partidas não sejam comprimidas desde Lisboa numa única armada. A convergência deve ser representada apenas onde houver documentação suficiente.

## Leitura funcional

`ExpeditionModel` permite que uma expedição exista no registro histórico sem possuir linhas em `expedition_routes.csv`. Nesse estado:

- a expedição pode ser consultada no catálogo histórico;
- nenhuma rota é autorizada por `FLEET_COMMAND`;
- `first_sequence()` falha explicitamente como “Expedição sem pernas”;
- portanto, o registro não cria acidentalmente uma campanha jogável.

Essa separação é útil para F3: identidade da armada não equivale a itinerário normalizado.

## Decisão por armada

### Afonso de Albuquerque

**Registrar em `expeditions.csv`, sem pernas por enquanto.**

A armada é diretamente relevante para a recuperação de Cochim e para a transformação institucional/militar de setembro de 1503. A existência e comando devem integrar o domínio histórico, mas não há necessidade demonstrada de simular Lisboa→Índia como campanha nesta tranche.

### Francisco de Albuquerque

**Registrar em `expeditions.csv`, sem pernas por enquanto.**

Também é diretamente relevante para a chegada ao Malabar e recuperação de Cochim. Deve permanecer distinta de Afonso desde a partida. Nenhuma rota compartilhada será inferida apenas porque ambas convergem depois no Índico.

### António de Saldanha

**Registrar em `expeditions.csv`, sem pernas por enquanto.**

A partida é historicamente distinta e pertence ao horizonte de 1503, mas sua missão própria não precisa ser comprimida no ciclo de Cochim. O registro evita apagar a armada sem obrigar F3 a expandir o loop para sua trajetória.

## Granularidade temporal

`expeditions.csv` registra `period_from/period_to` apenas por ano. As datas exatas 06/04, 14/04 e 15/04 permanecem no documento de evidência e no `source_id`; não serão convertidas em eventos de rota enquanto origem/destino operacional suficiente não estiver normalizado.

## O que não será criado neste gate

- nenhuma linha nova em `expedition_routes.csv`;
- nenhuma `voyage_observation`;
- nenhuma fusão das três armadas;
- nenhuma rota direta `LIS→ANJ` ou `LIS→COC`;
- nenhum evento de partida com destino fictício apenas para armazenar a data;
- nenhuma campanha selecionável/ativa na interface.

## Critério de saída

O subgate está satisfeito se:

1. as três expedições existirem como registros distintos e rastreáveis;
2. nenhuma possuir pernas executáveis;
3. testes demonstrarem que o domínio as reconhece como catálogo histórico, mas recusa ativação sem pernas;
4. a CI integral permanecer verde.

O próximo subgate deve então examinar somente a **convergência no Índico necessária ao ciclo de Cochim**, especialmente Anjediva e a chegada/restauração de setembro, sem reconstruir a travessia inteira por conveniência.