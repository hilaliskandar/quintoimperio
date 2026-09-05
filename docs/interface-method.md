# Método da interface jogável v0.1

## Objetivo

A interface Pygame v0.1 expõe `GameSessionModel` sem duplicar regras econômicas, de conhecimento, serviços portuários, expedições ou viagem na camada gráfica.

A tela apresenta mapa conhecido, porto atual, data, condição e provisões do navio, capital e carga, serviços portuários, mercado, armada ativa quando houver e rotas de saída.

## Dois estados explicitamente distintos

### HISTORICAL

É o padrão. Abre em Lisboa em 8 de julho de 1497 com `EXP_GAMA_1497` ativa. A associação à armada não fixa identidade ou profissão do protagonista e não eleva seu conhecimento náutico.

O painel mostra a expedição e a perna corrente. Uma rota pode aparecer como disponível por `FLEET_COMMAND` mesmo quando o conhecimento pessoal ainda não é `OPERATIONAL`. O banner explicita: **comando institucional ≠ conhecimento pessoal**.

A cronologia documentada tem precedência quando existe observação da mesma rota e data. Assim, `R_LIS_CGH` parte em 8 de julho e usa a duração agregada observada de 134 dias até 19 de novembro, não a antiga extrapolação de velocidade derivada do Índico.

Essa primeira aresta continua inadequada como unidade final de provisões porque inclui escalas intermediárias. A interface preserva o eventual bloqueio por recursos em vez de inflar silenciosamente a capacidade do navio; o itinerário será segmentado em escalas documentadas.

### TECHNICAL

É um cenário de integração que começa em Calecute em 22 de maio de 1498 e aplica somente os overrides técnicos já documentados: mercado de Calecute operacional e rota Calecute–Aden operacional.

Ele permite testar `mercado -> compra -> viagem -> chegada -> venda`. Um banner informa que não representa o estado histórico inicial do personagem.

## Mapa

O mapa usa as coordenadas de `nodes.csv`. Somente nós com conhecimento geográfico pelo menos `RUMORED` aparecem. Linhas representam arestas do grafo, não derrotas históricas, correntes ou trajetos efetivamente navegados.

Uma rota pode ficar visível porque o personagem a conhece ou porque corresponde à perna corrente de uma expedição ativa. Isso não altera o estado de conhecimento pessoal.

A costa real permanece na ferramenta cartográfica de referência separada em `tools/render_cartographic_map.py`.

## Serviços portuários

O painel consulta `GameSessionModel.service_quote()` para provisões e reparo e mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` distintos.

- `Reabastecer +30` solicita 30 dias-equivalentes;
- `Reparar +20` solicita 20 pontos abstratos de condição.

Esses números são parâmetros de simulação. Nenhum custo monetário histórico é inventado.

## Mercado

O painel chama `GameSessionModel.market_view()`. Se `market_knowledge < OPERATIONAL`, nenhuma mercadoria acionável é mostrada. Compra e venda usam quantidade unitária abstrata e são delegadas ao domínio.

Capital, quantidade, capacidade e preço continuam índices de simulação.

## Viagem

Cada rota de saída é planejada pelo domínio. O painel exibe a base disponível:

- `OWN_KNOWLEDGE`;
- `PILOT`;
- `FLEET_COMMAND`;
- ou bloqueio.

Quando existe piloto documentado para porto, período e rota, a interface o fornece ao plano antes de recorrer ao comando institucional. Isso preserva o caso Melinde–Calecute de 1498.

A execução de uma viagem atualiza calendário, provisões, condição, aprendizagem e, quando aplicável, avança a expedição para a próxima perna.

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
