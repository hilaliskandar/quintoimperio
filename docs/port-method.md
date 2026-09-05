# Método de serviços portuários v0.1

## Separação entre evidência e regra de jogo

A primeira camada de serviços portuários usa dois campos já presentes em `data/nodes.csv`:

- `provisions`;
- `repair`.

Esses campos podem assumir `LOW`, `MEDIUM`, `HIGH`, `NONE` ou permanecer vazios. Campo vazio significa **evidência insuficiente na base atual** e é convertido pelo domínio em `UNKNOWN`. Ele não pode ser tratado como sinônimo de `NONE`.

Essa distinção é deliberada. Um porto histórico importante não recebe automaticamente capacidade de reparo ou reabastecimento apenas porque seria plausível que tais serviços existissem.

## Parâmetros de simulação

`simulation/port_rules.csv` converte categorias documentadas em efeitos jogáveis. Na v0.1:

- reabastecimento acrescenta dias-equivalentes de provisões;
- existe um limite abstrato de provisões embarcadas;
- reparo restaura pontos da escala abstrata de condição `0..100`;
- serviços consomem tempo no calendário do jogo.

Nenhuma dessas conversões é uma quantidade histórica. `HIGH` não significa cinquenta dias históricos de mantimentos, e uma taxa de dez pontos de condição por dia não representa produtividade histórica de um estaleiro.

## Serviços desconhecidos e inexistentes

O domínio diferencia explicitamente:

- `UNKNOWN` — a base atual não sustenta afirmar disponibilidade;
- `NONE` — a base registra ausência do serviço;
- `LOW`, `MEDIUM`, `HIGH` — a base contém uma classificação que pode ser convertida em capacidade de simulação.

Na v0.1, tanto `UNKNOWN` quanto `NONE` impedem a execução do serviço, mas produzem bloqueios diferentes. Isso permite que pesquisas futuras substituam `UNKNOWN` por uma categoria documentada sem alterar a lógica do jogo.

## Estado do navio

Os serviços atuam sobre `VesselState`, já usado pela navegação:

- reabastecer aumenta `provision_days` e avança o relógio;
- reparar aumenta `condition` e avança o relógio;
- nenhuma ação pode ser executada se o navio não estiver no nó solicitado.

A operação retorna um novo estado imutável, preservando o estado anterior para testes e reprodutibilidade.

## Limitações atuais

A v0.1 ainda não modela:

- custo monetário do serviço;
- água e alimentos separadamente;
- tonelagem ou volume físico de provisões;
- materiais, mão de obra ou componentes de reparo;
- docagem, calafetagem ou tipos específicos de avaria;
- acesso político ao serviço;
- diferença entre infraestrutura portuária permanente e compra ad hoc junto a moradores/mercadores.

Esses elementos só devem ser acrescentados quando puderem ser separados entre evidência histórica e hipótese explícita de simulação.

## Lacuna histórica imediatamente visível

Na base atual, Melinde possui evidência direta para a disponibilidade do piloto guzerate de 1498, mas os campos de provisões e reparo permanecem vazios. O protótipo, portanto, permite usar o piloto documentado sem inventar automaticamente serviços de reabastecimento ou reparo no porto. Essa assimetria é intencional e transforma a ausência de evidência numa lacuna de pesquisa verificável.
