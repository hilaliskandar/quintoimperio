# Método cartográfico v0.2

## Regra principal

O mapa do jogo não pode inventar costa, posição de porto ou trajeto marítimo. As posições de nós continuam vindo exclusivamente de `data/nodes.csv`; quando uma coordenada histórica não é suficientemente defensável, o nó não é desenhado.

## Duas camadas distintas

O projeto passa a separar explicitamente:

1. **mapa de runtime em Pygame**, usado para o primeiro loop jogável e filtrado pelo conhecimento do personagem;
2. **mapa cartográfico de referência**, gerado por `tools/render_cartographic_map.py` com costa real para validação visual das posições.

O gerador cartográfico é uma ferramenta de desenvolvimento e não uma dependência obrigatória do runtime.

## Costa

A referência v0.2 usa a costa real distribuída com Basemap. Não são desenhadas fronteiras políticas modernas, porque elas seriam anacrônicas para 1497–1500. O fundo cartográfico serve apenas para posicionamento espacial e inspeção.

Instalação opcional:

```bash
python -m pip install -e ".[cartography]"
```

Renderização de referência:

```bash
python tools/render_cartographic_map.py --perspective REFERENCE --output build/map-reference.png
```

Também podem ser produzidas as perspectivas `PLAYER` e `CROWN`.

## Nós

- são desenhados apenas nós com latitude e longitude preenchidas;
- em `PLAYER` e `CROWN`, somente nós cujo `geo_knowledge` seja pelo menos `RUMORED` para a perspectiva escolhida;
- em `REFERENCE`, todos os nós georreferenciados são exibidos para inspeção de desenvolvimento.

Mpinda/Soyo e Sofala permanecem fora da referência atual porque `nodes.csv` ainda não fixa coordenadas históricas suficientemente seguras para esses nós.

## Projeção

A referência cartográfica usa projeção cilíndrica/equiretangular para preservar leitura simples de latitude e longitude na escala Atlântico–Índico. Essa escolha é de visualização e não reproduz uma carta histórica específica.

## Rotas

Linhas entre dois nós representam **arestas do grafo comercial/náutico**. Não representam a derrota efetivamente navegada, não seguem correntes, não identificam escalas intermediárias e não podem ser usadas como medida de distância histórica.

Na referência de desenvolvimento, as conexões de exploração portuguesa e as redes preexistentes são diferenciadas graficamente. Nas perspectivas `PLAYER` e `CROWN`, uma rota só é mostrada quando o estado inicial dessa própria rota não é `UNKNOWN` e os dois extremos são visíveis.

## Estética histórica

A aparência de pergaminho, cartas portulanas, rosas-dos-ventos ou outros elementos de época pode ser adicionada como camada estética, mas nunca deve substituir a geometria cartográfica real. Qualquer camada decorativa deve permanecer separada dos dados geográficos e não alterar posição de costa, nós ou arestas.

## Conhecimento

O mapa reforça a separação entre mundo real e mundo conhecido. Um porto pode aparecer como localização parcial sem que sua rota seja navegável. Calecute, por exemplo, pode ser conhecido indiretamente pelo personagem antes de 1498, enquanto Melinde permanece desconhecida no estado inicial.
