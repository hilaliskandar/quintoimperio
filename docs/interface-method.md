# Método da interface jogável v0.1

## Objetivo

A interface Pygame v0.1 expõe `GameSessionModel` sem duplicar regras econômicas, de conhecimento, serviços portuários, expedições ou viagem na camada gráfica.

A tela apresenta mapa conhecido, porto atual, data, condição e provisões do navio, capital e carga, serviços portuários, mercado, armada ativa quando houver e rotas de saída.

## Dois estados explicitamente distintos

### HISTORICAL

É o padrão. Abre em Lisboa em 8 de julho de 1497 com `EXP_GAMA_1497` ativa. A associação à armada não fixa identidade ou profissão do protagonista e não eleva seu conhecimento náutico.

O painel mostra a expedição e a perna corrente. Uma rota pode aparecer como disponível por `FLEET_COMMAND` mesmo quando o conhecimento pessoal ainda não é `OPERATIONAL`. O banner explicita: **comando institucional ≠ conhecimento pessoal**.

A primeira perna operacional é agora `R_LIS_STG`, Lisboa → São Thiago/baía de Santa Maria. A observação documentada da mesma rota e data produz a chegada em 27 de julho de 1497. A antiga aresta `R_LIS_CGH` permanece somente como conexão `STRATEGIC_AGGREGATE` e o domínio a bloqueia para execução.

A segmentação prossegue por baía de Santa Helena, Cabo, São Brás, Rio do Cobre, Rio dos Bons Sinais e Moçambique antes da costa suaíli setentrional e da travessia Melinde–Calecute. Ancoradouros logísticos não são transformados em mercados para tornar o loop mais conveniente.

### TECHNICAL

É um cenário de integração que começa em Calecute em 22 de maio de 1498 e aplica somente os overrides técnicos já documentados: mercado de Calecute operacional e rota Calecute–Aden operacional.

Ele permite testar `mercado -> compra -> viagem -> chegada -> venda`. Um banner informa que não representa o estado histórico inicial do personagem.

## Mapa

O mapa usa as coordenadas de `nodes.csv`. Somente nós com conhecimento geográfico pelo menos `RUMORED` aparecem. Linhas representam arestas do grafo, não derrotas históricas, correntes ou trajetos efetivamente navegados.

Uma rota pode ficar visível porque o personagem a conhece ou porque corresponde à perna corrente de uma expedição ativa. Isso não altera o estado de conhecimento pessoal. Conexões estratégicas agregadas podem continuar visíveis para leitura do grafo, mas o domínio não permite executá-las como viagem única.

A costa real permanece na ferramenta cartográfica de referência separada em `tools/render_cartographic_map.py`.

## Serviços portuários

O painel consulta `GameSessionModel.service_quote()` para provisões e reparo e mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` distintos.

- `Reabastecer +30` solicita 30 dias-equivalentes;
- `Reparar +20` solicita 20 pontos abstratos de condição.

Esses números são parâmetros de simulação. O limite abstrato de provisões foi ampliado para comportar a longa perna São Thiago–baía de Santa Helena; isso não é apresentado como tonelagem, ração ou capacidade histórica. Nenhum custo monetário histórico é inventado.

## Mercado

O painel chama `GameSessionModel.market_view()`. Se `market_knowledge < OPERATIONAL`, nenhuma mercadoria acionável é mostrada. Compra e venda usam quantidade unitária abstrata e são delegadas ao domínio.

Capital, quantidade, capacidade e preço continuam índices de simulação. Nós logísticos com `market_scale=NONE` não recebem mercadorias apenas por terem sido escalas da expedição.

## Viagem

Cada rota de saída é planejada pelo domínio. O painel exibe a base disponível:

- `OWN_KNOWLEDGE`;
- `PILOT`;
- `FLEET_COMMAND`;
- ou bloqueio.

Quando existe piloto documentado para porto, período e rota, a interface o fornece ao plano antes de recorrer ao comando institucional. Isso preserva o caso Melinde–Calecute de 1498.

A execução de uma viagem atualiza calendário, provisões, condição, aprendizagem e, quando aplicável, avança a expedição para a próxima perna. As permanências documentadas em `expedition_stops.csv` ainda não são executadas automaticamente; sua integração ao calendário jogável é o próximo incremento.

## Interação

- `Reabastecer +30` e `Reparar +20` acionam serviços do porto atual;
- clique em mercadoria, depois `Comprar 1` ou `Vender 1`;
- clique em rota ou destino conectado e use `Executar viagem`;
- `R` reinicia;
- `Tab` alterna `HISTORICAL`/`TECHNICAL`;
- `Esc` encerra.

## Inspeção visual e teste reprodutível

As duas telas são renderizadas no CI:

```bash
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario HISTORICAL --output /tmp/game-historical.png
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario TECHNICAL --output /tmp/game-technical.png
```

O GitHub Actions executa os smoke tests e publica as capturas como artefato para inspeção visual.
