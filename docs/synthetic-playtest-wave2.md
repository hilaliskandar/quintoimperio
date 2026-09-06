# Playtest sintético pós-MVP — onda 2

## Objetivo

A onda 2 testa a hipótese gerada pela onda 1: a baixa taxa de conclusão decorreria principalmente da ausência de preparação pré-partida antes da espera pela data histórica.

Mantêm-se os mesmos 20 jogadores sintéticos, os mesmos cinco perfis e as mesmas seeds. A única intervenção é informacional: antes de esperar pela próxima partida guiada, cada jogador consulta `plan_current_leg`. Quando os próprios bloqueios públicos do domínio indicam insuficiência de provisões, tenta reabastecer ainda antes da espera. Nenhuma necessidade é inferida por acesso interno a parâmetros ocultos.

## Resultado agregado

- sessões: 20;
- conclusões: 1/20 (5%);
- entrada em `COUNTERFACTUAL`: 4/20 (20%), contra 20/20 na onda 1;
- jogadores com bloqueio: 20/20;
- recuperação após primeiro bloqueio: 19/20;
- mediana de consultas de prontidão: 3;
- mediana de ações tentadas: 15;
- mediana de bloqueios: 4;
- mediana de duração simulada: 131 dias;
- condição mínima observada: 59,85;
- provisões mínimas observadas: 0;
- capital final mediano: 100.

A única conclusão ocorreu no perfil `DISCIPLINED`, seed 103. A sessão terminou em Calecute em 22 de maio de 1498, ainda em `GUIDED`, após 10 viagens, 8 esperas, 6 reabastecimentos, negociação de acesso e uma compra comercial.

## Mudança no padrão de bloqueios

O principal bloqueio deixou de ser `INSUFFICIENT_PROVISIONS` e passou a ser `SERVICE_AVAILABILITY_UNKNOWN`:

1. `SERVICE_AVAILABILITY_UNKNOWN`: 43 ocorrências;
2. `INSUFFICIENT_PROVISIONS`: 22;
3. `HISTORICAL_DEPARTURE_NOT_REACHED`: 14;
4. `HISTORICAL_STOP_NOT_RELEASED`: 11;
5. `SERVICE_UNAVAILABLE`: 5;
6. `NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED`: 2.

Na onda 1, `INSUFFICIENT_PROVISIONS` havia ocorrido 51 vezes e todos os jogadores haviam entrado em `COUNTERFACTUAL`. A onda 2, portanto, confirma que a preparação antes da espera resolve grande parte da ruptura cronológica, mas revela uma segunda barreira: o jogador ainda não sabe, em vários portos, se um serviço necessário está disponível.

## Posição final das sessões

- São Brás (`SHB`): 14;
- Rio do Cobre (`RCO`): 2;
- Melinde (`MAL`): 2;
- Calecute (`CAL`): 1;
- Cabo da Boa Esperança (`CGH`): 1.

Dezessete sessões terminaram com o objetivo de progresso ainda apresentado como `Estabelecer contato com ator documentado`, duas com `Chegar a Calecute` e uma com a campanha concluída.

## Interpretação

A comparação sustenta duas conclusões distintas.

Primeiro, há evidência forte de que a onda 1 media uma lacuna informacional real: permitir a inspeção da próxima perna antes da espera reduziu `COUNTERFACTUAL` de 100% para 20% e tornou possível uma conclusão completa sem alterar balanceamento.

Segundo, informação sobre provisões não é suficiente. O novo gargalo dominante é o conhecimento da disponibilidade de serviços. Isso sugere que a interface pode precisar comunicar melhor, antes de decisões irreversíveis de espera ou partida, quais serviços são conhecidos, desconhecidos ou indisponíveis e por quais canais esse conhecimento pode ser adquirido.

O resultado não justifica ainda alterar parâmetros de simulação. O experimento seguinte mais informativo é uma onda 3 que mantenha a inspeção pré-partida da onda 2 e permita aos jogadores buscar informação sobre serviços quando `SERVICE_AVAILABILITY_UNKNOWN` for o bloqueio relevante. Assim será possível separar uma barreira de informação sobre serviços de eventual indisponibilidade estrutural real.

## Limites

Estas sessões continuam sendo jogadores sintéticos. O experimento mede robustez decisória e acessibilidade sistêmica, não compreensão humana, frustração, interesse ou qualidade estética da interface.
