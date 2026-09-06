# Evidência histórica e conhecimento do jogador sobre serviços

## Problema

Os playtests sintéticos pós-MVP mostraram que `SERVICE_AVAILABILITY_UNKNOWN` concentrava duas situações semanticamente diferentes: ausência de evidência histórica no campo `provisions`/`repair` de `nodes.csv` e eventual desconhecimento do jogador. A onda 3 confirmou que os canais de informação existentes não resolvem esse bloqueio, porque foram desenhados para conhecimento geográfico, comercial, político e de navegação.

## Regra

`PortServiceModel` continua sendo a única fonte da disponibilidade histórica bruta. `UNKNOWN` continua significando campo histórico indeterminado; nunca é convertido automaticamente em `NONE`, `LOW`, `MEDIUM` ou `HIGH`.

A nova camada `ServiceKnowledgeSessionModel` registra separadamente o estado epistêmico do personagem:

- `UNASSESSED`: o personagem ainda não observou o porto;
- `DOCUMENTED`: após presença física, a base possui evidência categorizada e a categoria pode ser apresentada;
- `EVIDENCE_INDETERMINATE`: após presença física, a própria base permanece inconclusiva.

Chegar fisicamente a um nó observa provisões e reparo no nível da evidência disponível, sem custo temporal adicional. O valor `LOCAL_OBSERVATION_TIME_DAYS=0` está explicitado em `simulation/service_knowledge_rules.csv` como parâmetro de simulação.

## Consequência material

A camada epistêmica não concede recursos. Quando a evidência histórica é indeterminada, reabastecimento ou reparo continuam não executáveis. O bloqueio apresentado pela sessão passa a ser `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`, distinguindo-o de indisponibilidade documentada (`SERVICE_UNAVAILABLE`).

Não há sorteio, imputação ou probabilidade de serviço. Uma regra futura de decisão sob incerteza, se vier a ser introduzida, deverá ser explicitamente classificada como simulação e testada separadamente.

## Persistência

O schema de save passa a v2 para registrar `service_knowledge_records`. Saves v1 permanecem legíveis, mas são migrados sem inventar conhecimento: os novos registros entram vazios (`UNASSESSED`) até nova observação pelo sistema.

## Interface

`prototype/game_service_knowledge.py` acrescenta uma leitura explícita do estado da evidência: “documentado”, “não avaliado pelo jogador” ou “evidência histórica indeterminada”. A interface não substitui o dado histórico e não torna serviços indeterminados acionáveis.

## Próximo teste

A próxima onda sintética deve usar essa distinção para avaliar se jogadores conseguem planejar com antecedência em torno de portos cuja evidência é indeterminada. Somente depois disso deve ser considerada qualquer nova mecânica de decisão sob incerteza.