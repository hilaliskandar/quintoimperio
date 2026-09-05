# Método cartográfico v0.1

## Regra principal

O mapa do jogo não pode inventar costa, posição de porto ou trajeto marítimo. A primeira versão usa somente coordenadas presentes em `data/nodes.csv` e conhecimento geográfico do personagem.

## O que é desenhado

- nós com latitude e longitude preenchidas;
- somente nós cujo `geo_knowledge` seja pelo menos `RUMORED` para a perspectiva escolhida;
- arestas de rota apenas quando a própria rota já possui conhecimento inicial diferente de `UNKNOWN` e os dois extremos são visíveis.

Nós historicamente relevantes mas ainda sem coordenadas defensáveis, como Mpinda/Soyo na base atual, permanecem fora do mapa em vez de receber coordenadas aproximadas inventadas.

## Projeção

A v0.1 usa projeção equiretangular simples apenas para transformar latitude/longitude em coordenadas de tela. Essa escolha é de interface e não implica reconstrução cartográfica histórica. A extensão do mapa é calculada a partir dos pontos visíveis, com margem proporcional.

## Rotas

Linhas entre dois nós representam **arestas do grafo comercial/náutico**. Não representam a derrota efetivamente navegada, não seguem correntes, não identificam escalas intermediárias e não podem ser usadas como medida de distância histórica.

## Costa e relevo

Nenhuma costa é desenhada na v0.1. O fundo permanece deliberadamente esquemático até que um conjunto cartográfico real, com origem e licença registradas, seja incorporado ao projeto. Quando isso ocorrer, a geometria deverá ser versionada ou baixada por script reprodutível com fonte e versão fixadas.

## Conhecimento

O mapa reforça a separação entre mundo real e mundo conhecido. Um porto pode aparecer como localização parcial sem que sua rota seja navegável. Calecute, por exemplo, pode ser conhecido indiretamente pelo personagem antes de 1498, enquanto Melinde permanece desconhecida no estado inicial.
