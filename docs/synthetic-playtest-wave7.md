# Playtest sintético pós-MVP — onda 7

## Pergunta

Quantos dias de preparação simulada antes da partida histórica são necessários para que ações logísticas temporalmente custosas não penalizem automaticamente o jogador prudente como `COUNTERFACTUAL`?

## Base histórica e de simulação

A data histórica de partida permanece 1497-07-08, conforme `voyage_observations.csv`. O experimento não desloca essa data. Apenas inicia o relógio N dias antes, como fase de preparação simulada, porque `reprovision` consome um dia por ação e o MVP atual começa exatamente em 1497-07-08.

Foram testadas janelas de 1, 2 e 3 dias, com os mesmos 20 perfis/seeds. A política logística manteve margem experimental de 30 dias-equivalentes e foi aplicada antes de toda partida elegível.

## Resultados

### Janela de 1 dia

- 17/20 conclusões (85%);
- 4/20 `COUNTERFACTUAL`;
- os quatro casos `COUNTERFACTUAL` são do perfil `CAUTIOUS`;
- `CAUTIOUS`: 1/4 conclusão;
- todos os demais perfis: 4/4 conclusões.

A janela de um dia absorve uma ação logística inicial, mas não duas. O perfil cauteloso primeiro eleva seu estoque para a meta própria e depois tenta constituir reserva; a segunda ação ultrapassa 8 de julho.

### Janela de 2 dias

- **20/20 conclusões (100%)**;
- **0/20 `COUNTERFACTUAL`**;
- todos os cinco perfis: 4/4 conclusões;
- todas as 20 sessões chegam a Calecute em 1498-05-22.

### Janela de 3 dias

- **20/20 conclusões (100%)**;
- **0/20 `COUNTERFACTUAL`**;
- resultados substantivos idênticos aos da janela de 2 dias.

## Interpretação

Entre os valores testados, **2 dias é a menor janela suficiente** para eliminar a penalização temporal da preparação inicial sob a política avaliada. O terceiro dia não produz ganho mensurável.

O resultado não demonstra que a armada historicamente iniciou preparativos em 6 de julho, nem que dois dias correspondam à preparação histórica real. A janela deve ser tratada como camada de jogo anterior à partida observada, equivalente a uma fase de preparação/tutoria que termina em 8 de julho de 1497.

## Limite do experimento

A onda 7 mantém fixa uma reserva de 30 dias-equivalentes. Portanto, resolve a pergunta temporal, mas não identifica a menor margem logística adequada. A onda 6 tentou medir 10/20/30 sem janela pré-partida e ficou contaminada pelo deslocamento automático da partida. A comparação de margens deve ser repetida com a janela de 2 dias fixada.

## Encaminhamento

1. considerar a questão temporal da issue #57 empiricamente respondida: 2 dias simulados são suficientes no desenho testado;
2. repetir a sensibilidade de reserva (10, 20 e 30 dias-equivalentes) com janela pré-partida fixa de 2 dias;
3. somente depois decidir o desenho de interface e eventual parâmetro recomendado.