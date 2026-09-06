# Método de eventos marítimos v0.3

## Objetivo

Introduzir contingência operacional suficiente para que preparação reduza risco sem tornar o resultado garantido. Todos os eventos desta camada continuam sendo `SIMULATION`: não afirmam que calmaria, tempestade, avaria, deterioração de provisões ou racionamento eficiente ocorreram historicamente em uma viagem determinada.

A principal mudança da v0.3 não é aumentar a severidade dos eventos, mas separar o que o jogador pode conhecer antes da partida daquilo que só é resolvido durante a viagem.

## Previsão e resolução

A onda 12 mostrou que eventos resolvidos em `plan_voyage()` eram, na prática, conhecidos antes da confirmação. Uma perda de provisões podia tornar o plano inviável e o jogador reabastecia antes de partir. A contingência passava a funcionar como uma restrição determinística adicional.

Na camada jogável v0.3:

1. `plan_voyage()` expõe somente o cenário-base conhecido: duração estimada, consumo-base, desgaste-base e bloqueios já presentes antes da partida;
2. o `VoyagePlan` preserva a `simulation_seed`, mas mantém `events=()` e `events_resolved=False`;
3. `resolve_voyage()` seleciona o evento somente quando a viagem é confirmada/executada;
4. o evento resolvido é então aplicado ao estado e registrado em `voyage_event_history`.

O domínio genérico de viagem mantém resolução antecipada por padrão para compatibilidade com testes e usos técnicos. A sessão jogável `ServiceKnowledgeSessionModel` converte o plano para a forma diferida antes de expô-lo ao jogador e resolve a contingência na execução.

## Precedência documental e cronologia

A evidência histórica continua acima da aleatoriedade. Quando existe observação exata de rota/data em cronologia `GUIDED`, `timing_events_suppressed_by_observation=True` restringe a resolução a eventos `observed_timing_safe`. Portanto, um evento de provisões pode ocorrer sem deslocar uma chegada historicamente observada.

Em trajetórias contrafactuais ou sem timing observado, eventos de atraso e dano podem ser resolvidos somente depois da confirmação e alterar a duração efetiva em relação à previsão exibida.

## Eventos disponíveis

`simulation/voyage_event_rules.csv` mantém as seis hipóteses da v0.2:

- `CALM_DELAY`: atraso sem dano adicional;
- `ROUGH_WEATHER`: atraso e perda abstrata de condição;
- `MINOR_RIGGING_DAMAGE`: avaria menor de aparelho;
- `JUNE_JULY_DISRUPTION`: perturbação adicional em junho/julho para rotas já classificadas com dependência de monção `MEDIUM` ou `HIGH`;
- `PROVISION_SPOILAGE`: perda de 3 a 8 dias-equivalentes por deterioração/armazenamento, sem alterar timing observado;
- `EFFICIENT_RATIONING`: ganho de 2 a 5 dias-equivalentes de autonomia por consumo mais eficiente, sem alterar timing observado.

As probabilidades e amplitudes continuam parâmetros de jogo sujeitos a calibração por playtest. Não representam frequências históricas medidas.

## Efeito sobre provisões

Antes da partida, a viabilidade usa apenas:

`provisões iniciais >= consumo-base conhecido`

Depois da confirmação, a resolução calcula:

`provisões finais = provisões iniciais - consumo efetivo da viagem + delta do evento`

Se uma deterioração consumir a margem restante, a viagem já ocorreu: o sistema não retroage para impedir a partida. Nesta versão, o estoque ao chegar é limitado a zero. A consequência aparece nas decisões posteriores, especialmente em sequências de escalas sem abastecimento documentado.

Essa regra é uma abstração transitória. A v0.3 ainda não modela fome, mortalidade ou interrupção em mar aberto; portanto, déficit durante a própria perna não produz naufrágio automático nem nó artificial no oceano.

## Auditabilidade

A seed continua determinística. O mesmo estado, rota e `simulation_seed` produz a mesma resolução. `VoyagePlan` registra:

- `simulation_seed`;
- `events_resolved`;
- `timing_events_suppressed_by_observation`;
- `events_suppressed_by_observation` após a resolução;
- efeitos efetivamente resolvidos.

A persistência continua registrando os `VoyageEvent` já ocorridos, não previsões de eventos futuros.

## Limites

Ainda não existem mortes, doença, perda individual de tripulação, perda de carga comercial, combate, captura, encalhe, naufrágio ou perda de embarcação. Esses efeitos exigem modelos próprios.

A camada também não inventa meteorologia histórica. Eventos são mecanismos probabilísticos de simulação e permanecem separados da base documental.

## Próximo teste

A bateria fixa de 10 arquétipos × 20 seeds deve ser repetida como onda 13 sem alterar as probabilidades da v0.2. O objetivo é isolar o efeito da mudança informacional: se a dispersão aumentar, a causa será a resolução tardia e não uma punição artificialmente maior.
