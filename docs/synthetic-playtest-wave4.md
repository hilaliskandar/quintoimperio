# Playtest sintético pós-MVP — onda 4

## Pergunta

A separação entre evidência histórica de serviço e conhecimento do jogador, incorporada no PR #55, altera o desempenho da campanha ou apenas torna semanticamente correto o bloqueio observado nas ondas anteriores?

## Desenho

A onda 4 replica a política da onda 2, com os mesmos 20 perfis e as mesmas seeds. A única diferença é a versão do domínio: a execução ocorre após a incorporação de `ServiceKnowledgeSessionModel`.

Não há nova heurística, nova disponibilidade portuária, sorteio, imputação ou alteração de balanceamento.

## Resultado

- 20/20 sessões executadas tecnicamente com sucesso;
- 1/20 concluiu a campanha, igual à onda 2;
- 4/20 entraram em `COUNTERFACTUAL`, igual à onda 2;
- 20/20 encontraram algum bloqueio;
- 19/20 executaram ação válida após algum bloqueio;
- mediana de 15 ações tentadas;
- mediana de 4 bloqueios;
- `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`: 43 ocorrências;
- `INSUFFICIENT_PROVISIONS`: 22 ocorrências;
- `HISTORICAL_DEPARTURE_NOT_REACHED`: 14;
- `HISTORICAL_STOP_NOT_RELEASED`: 11;
- `SERVICE_UNAVAILABLE`: 5;
- `NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED`: 2.

A única conclusão foi novamente o perfil `DISCIPLINED`, seed 103, em Calecute em 1498-05-22, ainda em modo `GUIDED`.

## Comparação com a onda 2

Os indicadores substantivos permanecem invariantes. A principal mudança é semântica e rastreável:

- onda 2: `SERVICE_AVAILABILITY_UNKNOWN` = 43;
- onda 4: `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE` = 43.

Isso demonstra que a separação epistêmica não alterou silenciosamente a dificuldade nem criou recursos. Ela apenas deixou explícito que o bloqueio decorre da indeterminação da evidência histórica, e não de uma suposta falta de informação recuperável pelo jogador.

## Localização do gargalo

A trajetória modal continua interrompida em `SHB` (Santa Helena), onde a documentação sustenta reparos/limpeza e obtenção de madeira, mas não permite afirmar reabastecimento de provisões. Os jogadores da política comparável chegam a esse nó com margem pequena de provisões porque preparam apenas a perna corrente.

## Interpretação

A issue #54 pode ser considerada resolvida no plano semântico: evidência histórica, conhecimento do jogador e indisponibilidade documentada são agora estados distintos. A onda 4 mostra, porém, que existe um problema posterior e independente: **planejamento logístico sob incerteza**.

A próxima hipótese testável não deve atribuir serviço a `SHB`. Deve avaliar se uma política de reserva logística, constituída em portos onde o reabastecimento é documentado, permite atravessar escalas cuja capacidade de provisão é historicamente indeterminada. Isso é diferente de resolver `UNKNOWN`: trata-se de preparar o navio para não depender dessa hipótese.

## Encaminhamento

Executar uma onda 5 controlada, mantendo dados históricos e regras materiais intactos, mas acrescentando ao agente uma política explícita de reserva de provisões antes de partir de portos documentadamente capazes de reabastecer. Se a taxa de conclusão aumentar, haverá evidência para desenhar uma ajuda de planejamento na interface; se não aumentar, o gargalo deverá ser procurado em outra regra da campanha.