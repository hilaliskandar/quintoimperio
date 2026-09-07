# P3.3-doc — auditoria de schema: frota de retorno × força residente v0.1

Data: 2026-09-07
Issue: #113

## Pergunta

A arquitetura atual consegue representar a bifurcação histórica de 1502 entre a frota que regressa com Vasco da Gama e a força naval de Vicente Sodré que permanece no Índico sem criar imediatamente um novo sistema geral de frotas?

## Estado atual do domínio

`GameSessionState` possui apenas um `active_expedition_id` e uma única `expedition_leg_sequence`. Portanto, uma sessão de jogador segue uma expedição ativa por vez.

`ExpeditionModel` é genérico por `expedition_id`, lê `data/expeditions.csv` e `data/expedition_routes.csv`, e autoriza a perna corrente por `FLEET_COMMAND`. Ao concluir a sequência, `advance()` mantém a mesma expedição ou encerra a participação ativa.

O schema de `expeditions.csv` já admite unidades de modelagem historicamente relacionadas mas separadas. O retorno de Gama de 1498 está registrado como `EXP_GAMA_RETURN_1498`, explicitamente descrito como subcampanha documental da mesma expedição histórica.

## Conclusão arquitetural

Não é necessário introduzir, no primeiro P3-func, um sistema geral de múltiplas frotas simultaneamente controláveis.

A bifurcação de 1502 pode ser representada de maneira mínima como:

1. uma expedição principal de Vasco da Gama até o ponto documentado de separação;
2. uma unidade de retorno de Vasco da Gama, se a divisão do itinerário for necessária para preservar o loop;
3. uma expedição/subcampanha separada de Vicente Sodré a partir do momento em que sua força permanece no Índico.

A escolha do jogador pode seguir apenas uma dessas trajetórias por sessão. O fato de a outra força continuar existindo no mundo deve ser registrado por efeitos de estado/eventos históricos, e não por uma segunda `active_expedition_id` silenciosa.

## Lacuna real

A lacuna não é principalmente 'duas frotas controláveis'. É a persistência de **forças/expedições não controladas pelo jogador** como estado objetivo do mundo enquanto outra trajetória continua.

Se o primeiro P3-func exigir que ações posteriores de Sodré alterem automaticamente o mundo durante a viagem de retorno de Gama, será necessária uma camada de eventos históricos datados ou outro mecanismo de world-state independente da expedição ativa. Isso deve ser testado antes de qualquer alteração em `GameSessionState`.

## Regra de implementação futura

- não adicionar coleção `active_expeditions` ao save sem necessidade demonstrada;
- preferir subcampanhas documentais separadas, padrão já validado em P1;
- efeitos da força não escolhida devem entrar como eventos/estado histórico com data e evidência;
- somente criar sistema de múltiplas frotas se um gate funcional demonstrar que a representação por subcampanhas + eventos é insuficiente.

## Evidência de código

- `src/quintoimperio/domain/session.py`: um único `active_expedition_id` e `expedition_leg_sequence` no estado persistível;
- `src/quintoimperio/domain/expedition.py`: modelo genérico por `expedition_id`, uma sequência ativa por sessão;
- `data/expeditions.csv`: precedente `EXP_GAMA_RETURN_1498` para separar unidade de modelagem sem afirmar expedição histórica independente.

## Decisão

P3.3 não justifica, por si só, refatoração estrutural do estado de sessão. A proposta mínima deve usar expedições/subcampanhas separadas e identificar explicitamente a necessidade de eventos mundiais datados como a única possível extensão de schema ainda não demonstrada.