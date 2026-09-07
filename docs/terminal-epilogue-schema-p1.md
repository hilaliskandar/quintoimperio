# P1-tech — representação mínima do epílogo divergente de 1499

Issue: #93.

## Decisão

As três lacunas identificadas após 25/04/1499 não justificam, neste estágio, uma refatoração de `ExpeditionModel`, `GameSessionState` ou persistência. O fechamento da primeira viagem pode ser representado como uma camada histórica de epílogo, separada do loop jogável, por meio de `data/expedition_epilogue_events.csv`.

A tabela registra eventos ordenados por `trajectory_id`, sem pressupor que toda a expedição continue unida. Isso permite documentar:

- Bérrio/Nicolau Coelho como trajetória própria;
- S. Gabriel como trajetória própria e mudança de comando para João de Sá;
- Vasco da Gama como trajetória pessoal que se separa do S. Gabriel em São Tiago e passa pela Terceira.

## Datas incertas

`date_precision` evita escolher uma falsa precisão:

- `EXACT`: `date_from == date_to`;
- `BEFORE`: somente limite superior preenchido;
- `AFTER`: somente limite inferior preenchido;
- `RANGE`: ambos os limites preenchidos.

Reivindicações concorrentes usam linhas separadas no mesmo `variant_group`. A chegada de Vasco da Gama a Lisboa mantém 29/08, 08/09 e 18/09 como três variantes sem `preferred_for_simulation`. Para Nicolau Coelho, 10/07 é mantido como preferência editorial de trabalho e 11/07 como variante registrada no `Paesi`; ambas continuam visíveis.

## Frota e comando

O novo arquivo não cria uma frota operacional genérica. `subject_type`, `subject_label`, `vessel_label` e `event_type` registram eventos documentais como `COMMAND_CHANGE` e `TRAJECTORY_SPLIT`. Isso é suficiente para um epílogo narrativo e preserva a possibilidade de um modelo naval mais rico posteriormente.

## Persistência e não regressão

A tabela não é consumida por `GameSessionState` nem pelo save schema atual. Portanto:

- saves existentes continuam compatíveis;
- as dez pernas do MVP não mudam;
- a subcampanha até os Baixos do Rio Grande permanece independente;
- o epílogo pode ser renderizado futuramente por uma camada de apresentação sem alterar o estado jogável retroativamente.

## Critério para futura generalização

Somente generalizar esta representação para um sistema de trajetórias/personagens se a expansão 1500–1505 exigir recorrência de:

1. múltiplas embarcações divergindo dentro da mesma expedição;
2. personagens mudando de embarcação;
3. comando de navio como estado jogável;
4. datas historicamente incertas afetando decisões durante o loop, e não apenas o epílogo.

Até lá, a solução específica é preferível porque registra a evidência sem criar abstrações que ainda não têm uso demonstrado.