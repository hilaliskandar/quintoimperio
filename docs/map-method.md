# Método cartográfico do núcleo v0.1 — renderizador cartográfico v0.3

## Regra principal

O mapa do jogo não pode inventar costa, posição de porto ou trajeto marítimo. As posições de nós continuam vindo exclusivamente de `data/nodes.csv`. Quando a posição exata do sítio histórico não pode ser fixada, o projeto admite uma **âncora cartográfica provisória**, desde que:

1. haja um referente geográfico histórico e moderno defensável;
2. a incerteza seja explicitamente registrada;
3. `coordinate_confidence` não seja `HIGH`;
4. a interface deixe claro que o ponto é aproximado.

Este documento descreve o comportamento cartográfico do núcleo jogável **v0.1**. A marca **v0.3** usada abaixo refere-se exclusivamente à terceira iteração do renderizador cartográfico programático de referência; ela não altera a versão funcional do núcleo de jogo.

## Duas camadas distintas

O projeto separa explicitamente:

1. **mapa de runtime em Pygame**, usado para o primeiro loop jogável e filtrado pelo conhecimento do personagem;
2. **mapa cartográfico de referência**, gerado por `tools/render_cartographic_map.py` com costa real para validação visual das posições.

O gerador cartográfico é uma ferramenta de desenvolvimento e não uma dependência obrigatória do runtime.

## Costa

O renderizador cartográfico de referência v0.3 usa a costa real distribuída com Basemap. Não são desenhadas fronteiras políticas modernas, porque elas seriam anacrônicas para 1497–1500. O fundo cartográfico serve para posicionamento espacial, inspeção e produção de uma referência estética reprodutível.

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
- em `REFERENCE`, todos os nós georreferenciados são exibidos para inspeção de desenvolvimento;
- âncoras provisórias recebem marca gráfica adicional e asterisco no rótulo.

### Mpinda / Soyo

A base usa provisoriamente `-6.1981, 12.3933`, ancorada na área atual de Pinda/Soyo, na margem sul da foz do Congo. A escolha é compatível com a identificação histórica de Mpinda como porto de Soyo, mas **não afirma a posição exata do cais do século XV**. A coordenada permanece `MEDIUM` e deve ser refinada se surgir georreferenciamento arqueológico ou histórico mais preciso.

### Sofala

A base usa provisoriamente `-20.1562, 34.7383`, ancorada em Nova Sofala / sítio histórico de Sofala. A Enciclopédia Virtual da Expansão Portuguesa observa que o porto antigo ficava a sul da foz do Pungué e que hoje está submerso. Como a dinâmica estuarina e o assoreamento alteraram a costa, o ponto é uma referência espacial do sítio histórico, **não uma reconstrução do porto medieval exato**. A coordenada permanece `MEDIUM`.

A justificativa e as fontes de apoio dessas duas âncoras estão registradas em `docs/evidence/provisional-coordinates.md`.

## Projeção

A referência cartográfica usa projeção cilíndrica/equiretangular para preservar leitura simples de latitude e longitude na escala Atlântico–Índico. Essa escolha é de visualização e não reproduz uma carta histórica específica.

## Rotas

Linhas entre dois nós representam **arestas do grafo comercial/náutico**. Não representam a derrota efetivamente navegada, não seguem correntes, não identificam escalas intermediárias e não podem ser usadas como medida de distância histórica.

Na referência de desenvolvimento, as conexões de exploração portuguesa e as redes preexistentes são diferenciadas graficamente. Nas perspectivas `PLAYER` e `CROWN`, uma rota só é mostrada quando o estado inicial dessa própria rota não é `UNKNOWN` e os dois extremos são visíveis.

## Estética histórica programática

O renderizador cartográfico v0.3 adiciona uma camada estética procedural inspirada em cartas náuticas dos séculos XV–XVI:

- paleta de pergaminho;
- linhas de rumo decorativas;
- rosa-dos-ventos gerada por código;
- tipografia e caixas de rótulo discretas;
- grandes rótulos continentais e oceânicos apenas decorativos.

Esses elementos são desenhados **sobre a mesma geometria cartográfica real**. As linhas de rumo não representam ventos, correntes ou derrotas. Nenhuma textura ou ilustração pode deslocar a costa, os nós ou as arestas.

## Conhecimento

O mapa reforça a separação entre mundo real e mundo conhecido. Um porto pode aparecer como localização parcial sem que sua rota seja navegável. Calecute, por exemplo, pode ser conhecido indiretamente pelo personagem antes de 1498, enquanto Melinde permanece desconhecida no estado inicial.
