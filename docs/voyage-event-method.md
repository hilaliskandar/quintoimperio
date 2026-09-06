# Método de eventos marítimos v0.2

## Objetivo

Introduzir contingência operacional suficiente para que preparação reduza risco sem tornar o resultado garantido. Todos os eventos desta camada continuam sendo `SIMULATION`: não afirmam que calmaria, tempestade, avaria, deterioração de provisões ou racionamento eficiente ocorreram historicamente em uma viagem determinada.

## Precedência documental e cronologia

A evidência histórica continua acima da aleatoriedade. Quando `preserve_observed_timing=True` e existe observação exata para rota/data, eventos que adicionariam dias são excluídos da seleção. Eventos explicitamente marcados como `observed_timing_safe` podem, porém, alterar recursos sem deslocar a chegada observada.

Assim, Melinde → Calecute em 24/4/1498 preserva seus 26/27 dias no modo guiado, mas a autonomia restante pode variar por um evento de provisões. Em trajetórias contrafactuais, a mesma rota pode também receber atrasos e danos abstratos.

`VoyagePlan` distingue duas situações para evitar ambiguidade:

- `timing_events_suppressed_by_observation=True`: a observação histórica restringiu a seleção a eventos que não alteram o timing;
- `events_suppressed_by_observation=True`: além dessa restrição, nenhum evento aleatório foi efetivamente selecionado para a perna.

Portanto, uma perna guiada pode ter `timing_events_suppressed_by_observation=True`, `events_suppressed_by_observation=False` e ainda assim registrar um evento de provisões compatível com a data histórica.

## Eventos disponíveis

`simulation/voyage_event_rules.csv` contém seis hipóteses de simulação:

- `CALM_DELAY`: atraso sem dano adicional;
- `ROUGH_WEATHER`: atraso e perda abstrata de condição;
- `MINOR_RIGGING_DAMAGE`: avaria menor de aparelho;
- `JUNE_JULY_DISRUPTION`: perturbação adicional em junho/julho para rotas já classificadas com dependência de monção `MEDIUM` ou `HIGH`;
- `PROVISION_SPOILAGE`: perda de 3 a 8 dias-equivalentes por deterioração/armazenamento, sem alterar timing observado;
- `EFFICIENT_RATIONING`: ganho de 2 a 5 dias-equivalentes de autonomia por consumo mais eficiente, sem alterar timing observado.

As probabilidades e amplitudes são parâmetros de jogo sujeitos a calibração por playtest. Não representam frequências históricas medidas.

## Seleção e auditabilidade

A seleção é determinística por seed, rota, data e modo de preservação do timing. No máximo um evento é aplicado por viagem nesta versão.

Cada `VoyageEvent` registra identificador, tipo, rota, data de partida, dias adicionais, perda de condição, delta de provisões, marca `observed_timing_safe` e `simulation_only=True`. O estado persistido conserva esses campos para que uma campanha possa ser reproduzida e auditada.

## Efeito sobre recursos

O consumo normal continua sendo calculado pelos dias de viagem. Depois disso, aplica-se `provision_delta` do evento:

`provisões finais = provisões iniciais - consumo da viagem + delta do evento`

Um delta negativo pode tornar inviável uma viagem que estivesse planejada exatamente no limite; uma reserva logística absorve essa perda. Um delta positivo pode preservar autonomia extra. Dessa forma, a margem deixa de ser mera fórmula determinística e passa a funcionar como proteção contra contingência.

O desgaste normal continua calculado sobre os dias-base; `condition_loss` do evento é adicional.

## Limites da v0.2

Ainda não existem mortes, doença, perda individual de tripulação, perda de carga comercial, combate, captura, encalhe, naufrágio ou perda de embarcação. Esses efeitos exigem modelos próprios e serão avaliados somente depois que a bateria de arquétipos mostrar que a variância atual é insuficiente.

A camada também não inventa meteorologia histórica. Eventos são mecanismos probabilísticos de simulação e permanecem separados da base documental.

## Critério de calibração

Após CI verde, a bateria fixa de arquétipos deve ser repetida com as mesmas seeds. Espera-se que estilos prudentes continuem com alta taxa de conclusão, mas deixem de apresentar sucesso quase obrigatório; estilos agressivos devem apresentar maior dispersão. Se a aleatoriedade dominar decisões e reduzir excessivamente os perfis de planejamento, as probabilidades devem ser reduzidas antes de qualquer expansão de severidade.
