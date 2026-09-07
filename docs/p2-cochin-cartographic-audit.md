# P2-doc — auditoria cartográfica de Cochim c. 1500

Issue: #107.

Data: 2026-09-07.

## Identificação

A identificação moderna de Cochim com Kochi, Kerala, é inequívoca. A incerteza não está na cidade, mas na escolha de um ponto que represente adequadamente o porto histórico sem sugerir reconstrução exata da barra, do ancoradouro, da feitoria ou da linha de costa de 1500.

## Fontes cartográficas/institucionais

### HPIP

O Heritage of Portuguese Influence/Património de Influência Portuguesa registra Kochi/Cochim/Santa Cruz de Cochim em aproximadamente:

- latitude: `9.9670833`
- longitude: `76.2440167`

O estudo urbano descreve Cochim como centro em costa baixa, lagunar e cortada por canais/backwaters. Para o período português inicial, situa a cidade sobre um dos canais principais, paralela ao litoral e aproximadamente 1,5 km da barra principal de ligação entre as águas interiores e o mar.

A área portuguesa posterior desenvolveu-se junto à barra, no setor hoje associado a Fort Kochi, enquanto a cidade local/centro do rajá se articulava com a área de Mattancherry. Essa distinção posterior é importante para não colapsar automaticamente cidade local, feitoria e fortificação num único sítio construído.

### Cochin Port Authority

A autoridade portuária situa o porto moderno em torno de `9°58′N, 76°16′E` e confirma que o porto ocupa o sistema de lagoa/backwaters, com entrada entre Vypeen e Fort Kochi.

Sua história institucional registra que a abertura portuária de Cochim se formou após grandes cheias de 1341 e que a transformação de um roadstead/porto natural no porto moderno navegável ocorreu sobretudo no século XX, com obras de Robert Bristow, dragagem/canal e criação de Willingdon Island.

Essa fonte é adequada para compreender a geomorfologia e rejeitar o uso acrítico do centro operacional portuário moderno como proxy do porto de 1500.

### EVE/FCSH

A EVE fornece referência regional próxima (`9°56′N, 76°15′E`) e caracteriza Cochim como porto do Malabar e entreposto já existente antes da chegada portuguesa.

## Decisão de coordenada

Âncora de trabalho recomendada para um futuro nó `COC`:

`9.9671, 76.2440`

Origem: HPIP, arredondada a quatro casas decimais para ser compatível com `nodes.csv`.

### Confiança

`coordinate_confidence = MEDIUM`

Justificativa:

- `HIGH` seria adequado para a identidade moderna Kochi=Cochim, mas poderia sugerir precisão excessiva para o ponto portuário de 1500;
- `MEDIUM` comunica corretamente que a coordenada é uma âncora urbana-histórica de trabalho em uma área estuarina transformada;
- `LOW` seria excessivamente cauteloso, pois não há dúvida regional comparável a RCO ou BSR.

## Tipo de nó

Para c. 1500, a classificação mínima recomendada é:

`node_type = FOREIGN_PORT`

Razões:

- Cochim é porto mercantil anterior à presença portuguesa;
- por volta de 1500, Prakash o coloca entre os portos menores do Malabar em relação a Calecute;
- embora a cidade tenha função de entreposto e distribuição, o primeiro P2-func não precisa elevá-la a `FOREIGN_ENTREPOT` equivalente a Calecute;
- a ascensão posterior de Cochim ao principal porto português de carregamento é processo histórico que não deve ser retroprojetado ao estado inicial.

`market_scale` recomendado inicialmente: `REGIONAL`.

## Acesso e soberania

A coordenada não deve ser associada ao Forte Manuel nem à futura cidade portuguesa de Santa Cruz como se essas estruturas existissem em dezembro de 1500.

O nó deve representar o porto/cidade sob autoridade local do Perumpadappu Swarupam. A presença portuguesa inicial é uma feitoria negociada; fortificação e guarnição surgem no ciclo de 1503.

## Nota histórica recomendada

> Porto de Cochim/Kochi no sistema lagunar de Vembanad. A coordenada usa a área histórica de Kochi/Fort Kochi–Mattancherry como âncora moderna de trabalho; não representa o ponto exato do ancoradouro ou da feitoria de 1500. A geomorfologia e a infraestrutura portuária foram profundamente transformadas, sobretudo na modernização do século XX.

## Não criar múltiplos nós no primeiro P2-func

Não há necessidade, nesta etapa, de separar:

- cidade/centro do rajá;
- porto;
- feitoria de 1500/1501;
- Forte Manuel de 1503;
- Santa Cruz de Cochim posterior.

Essas distinções podem ser tratadas por atores, eventos, períodos e notas. Múltiplos nós só seriam justificáveis caso um sistema urbano/militar posterior exija espacialização intraurbana.

## Gate

A #107 pode ser encerrada. A âncora cartográfica, confiança e tipo mínimo do nó estão suficientemente definidos para a proposta consolidada P2-doc, sem edição ainda de `data/nodes.csv`.
