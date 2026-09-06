# Frota física experimental v0.1

Esta camada existe para testar a plausibilidade material da armada de 1497 sem substituir o `VesselState` abstrato do MVP.

## Regra epistemológica

Os valores são classificados por natureza de evidência:

- `DOCUMENTED`: diretamente sustentado pela documentação usada no projeto;
- `RECONSTRUCTION`: reconstrução historiográfica ou arqueológica;
- `ANALOGY`: valor posterior usado apenas como analogia quantitativa;
- `SIMULATION`: regra introduzida exclusivamente para teste.

Nenhum valor desta camada deve ser apresentado ao jogador como fato histórico sem que sua classificação permita isso.

## Cenário-base v0.1

| Embarcação | Arqueação base | Faixa de sensibilidade | Pessoas | Natureza |
| --- | ---: | ---: | ---: | --- |
| São Gabriel | 100 tonéis | 90–120 | 70 | reconstrução |
| São Rafael | 90 tonéis | 90–100 | 50 | reconstrução |
| Bérrio | 50 tonéis | 50 | 30 | reconstrução |
| Navio de mantimentos | 110 tonéis | 110–200 | 20 | reconstrução |

O total-base é 170 pessoas e 350 tonéis. `Tonel` permanece unidade histórica de arqueação/capacidade e não é convertido automaticamente em tonelada métrica.

## Consumo experimental

A analogia tardia usada para o primeiro smoke adota, por pessoa/dia:

- água: 2,738 L;
- vinho: 1,006 L;
- biscoito: 0,989 kg;
- carne: 0,250 kg.

Com densidade de cálculo de 1 kg/L para os líquidos, esses quatro componentes somam 4,983 kg por pessoa/dia. Para 170 pessoas, a ordem de grandeza é 847,11 kg/dia.

Esses valores são `ANALOGY`, não rações documentadas para 1497. O primeiro intervalo de sensibilidade recomendado é ±20%.

## Smoke de estiva

O cenário de pesquisa inicial carrega:

- 60 dias dos quatro consumíveis principais para a população de cada navio;
- 30 dias-equivalentes adicionais para toda a armada concentrados no navio de mantimentos.

Isso produz cerca de 76,24 t métricas dos quatro consumíveis principais. A massa não inclui outros alimentos, embalagens, lenha, armamento, munição, aprestos, sobressalentes, lastro, presentes ou carga comercial.

Usando apenas como controle uma equivalência experimental de 1 tonel de arqueação para 1,14 m³ de volume nominal, os líquidos do cenário ocupam cerca de 14,4% do volume nominal agregado e 18,8% do navio de mantimentos. Essa conta é um piso volumétrico, pois alimentos secos e recipientes também ocupam espaço.

## Invariantes

A camada experimental deve obedecer aos seguintes invariantes:

1. arqueação em tonéis é independente de massa em kg/t;
2. transferências entre embarcações conservam cada consumível individualmente;
3. não há criação de provisões por transferência;
4. retirar mais recurso que o existente é inválido;
5. o navio de mantimentos é uma unidade auxiliar com reserva transferível;
6. a camada não altera viagem, comércio, eventos, portos ou a cronologia do MVP.

## Relação com a issue #58

A margem de 20 dias-equivalentes descoberta pelos playtests anteriores continua sendo uma heurística do modelo abstrato. Ela não deve ser incorporada como ajuda definitiva até que a nova camada física seja testada em trajetórias Lisboa–Calecute e comparada com o comportamento do MVP atual.
