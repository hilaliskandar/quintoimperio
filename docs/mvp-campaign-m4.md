# M4 — objetivos e encerramento da campanha

## Objetivo

O M4 transforma a vertical slice Lisboa–Calecute em uma campanha com progresso reconhecível e condição explícita de encerramento. A camada não introduz fatos históricos, recompensas, pontuação ou uma sequência rígida de quests.

## Regra arquitetural

`CampaignProgressModel` é uma projeção do estado existente. Ele lê localização, expedição, conhecimento, relações, acesso e estado comercial; não substitui nem duplica as regras de viagem, informação, relações, acesso ou comércio.

Os marcos apresentados ao jogador são:

- participação na armada de 1497;
- contato com ator documentado;
- chegada a Calecute;
- conhecimento operacional do mercado de Calecute;
- acesso comercial negociado em Calecute;
- primeira compra comercial em Calecute.

A ordem visual desses marcos serve para tornar o progresso legível. Ela não cria autorização própria para ações: a elegibilidade continua sendo decidida pelos modelos de domínio correspondentes.

## Condição de encerramento

Chegar a Calecute não encerra a campanha por si só. O encerramento exige simultaneamente:

1. chegada a Calecute com a expedição histórica encerrada;
2. conhecimento operacional do mercado;
3. acesso comercial concedido pelas regras existentes;
4. carga comercial positiva resultante de compra explícita em Calecute.

No MVP histórico, a campanha começa sem carga comercial. Por isso, carga positiva após a chegada e o acesso é usada como evidência derivada da primeira compra. Serviços portuários não alteram `CommercialState`.

## Resumo final

`CampaignSummary` expõe somente informações presentes no estado da sessão:

- data e local finais;
- modo cronológico `GUIDED` ou `COUNTERFACTUAL`;
- quantidade de nós com algum conhecimento do jogador;
- atores documentados contatados;
- capital em índice abstrato de simulação;
- carga usada e capacidade total em índices abstratos;
- mercadorias e quantidades abstratas em posse.

Nenhum desses índices é apresentado como moeda, peso, volume ou preço histórico.

## Cronologia contrafactual

O encerramento também é possível em `COUNTERFACTUAL`, desde que as condições de domínio sejam satisfeitas. O resumo preserva explicitamente essa divergência; a camada M4 não tenta restaurar a cronologia histórica.

## Validação

Os testes do M4 verificam que:

- chegada isolada não encerra a campanha;
- acesso sem comércio não encerra a campanha;
- primeira compra elegível em Calecute encerra a campanha;
- o resumo final contém relações, capital/carga e cronologia;
- conclusão contrafactual permanece identificada como tal;
- o smoke Lisboa–Calecute passa pelas mesmas ações da interface e só encerra após acesso e comércio.
