# Método de eventos marítimos v0.1

## Objetivo

Introduzir risco marítimo no primeiro loop sem transformar hipóteses de balanceamento em acontecimentos históricos. Os eventos desta versão são sempre `SIMULATION`: eles não afirmam que uma calmaria, tempestade ou avaria específica ocorreu em uma viagem histórica determinada.

## Regra de precedência documental

A evidência de viagem continua acima da aleatoriedade. `NavigationModel` preserva observações exatas de rota e data de partida. `TravelModel.plan_voyage()` recebe `preserve_observed_timing`:

- quando verdadeiro e existe observação histórica exata para rota/data, nenhum evento aleatório é aplicado;
- quando falso, ou quando não existe observação exata, o sistema pode selecionar um evento de simulação;
- o evento nunca substitui a observação histórica na base; apenas modifica o plano contrafactual ou não observado.

Assim, Melinde → Calecute em 24/4/1498 continua em 26/27 dias quando a cronologia observada deve ser preservada. Uma simulação contrafactual pode usar a mesma rota/data com `preserve_observed_timing=False` e receber atraso ou avaria abstrata.

## Eventos disponíveis

`simulation/voyage_event_rules.csv` contém quatro hipóteses iniciais:

- `CALM_DELAY`: atraso sem dano adicional;
- `ROUGH_WEATHER`: atraso e perda abstrata de condição;
- `MINOR_RIGGING_DAMAGE`: avaria menor de aparelho, com dano abstrato e pouco ou nenhum atraso;
- `JUNE_JULY_DISRUPTION`: possibilidade adicional limitada a junho/julho em rotas já classificadas como `MEDIUM` ou `HIGH` em dependência de monção.

As probabilidades, limites de dias e perdas de condição são parâmetros de jogo. Não representam frequências históricas medidas.

## Seleção e auditabilidade

A seleção é determinística por semente, rota e data. No máximo um evento é selecionado por viagem na v0.1.

Cada `VoyageEvent` registra:

- identificador da regra;
- tipo do evento;
- rota;
- data de partida;
- dias adicionais;
- perda adicional de condição;
- marcador `simulation_only=True`.

`VoyagePlan` mantém `events` e `events_suppressed_by_observation`, permitindo auditar se a ausência de evento decorreu da precedência documental.

## Efeitos permitidos

Na v0.1 um evento pode somente:

1. acrescentar dias ao tempo total da viagem;
2. aumentar o consumo de provisões por causa desses dias adicionais;
3. reduzir a condição abstrata do navio.

O desgaste normal continua calculado sobre os dias-base de navegação; perdas adicionais vêm explicitamente do evento.

Não existem nesta camada mortes, doença, perda de tripulação, perda de carga, combate, captura, encalhe, naufrágio ou mudança de rota. Esses efeitos exigiriam modelos próprios e evidência/metodologia adicionais.

## Monções

A camada não inventa direção de vento. A única especialização sazonal adicional usa a categoria de dependência de monção que já existe em `routes.csv` e os meses de junho/julho já tratados na navegação v0.1. Portanto, o evento sazonal significa apenas maior possibilidade abstrata de perturbação dentro dessa classificação já existente.

## Limites

Os eventos genéricos servem para criar incerteza operacional, não para reconstruir meteorologia histórica. Quando houver fonte para um incidente específico, ele deverá ser registrado separadamente como evidência histórica e receber precedência sobre esta camada aleatória.
