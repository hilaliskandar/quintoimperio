# Método da interface jogável v0.1

## Objetivo

A interface Pygame v0.1 expõe `GameSessionModel` sem duplicar regras econômicas, de conhecimento, informação, serviços portuários, expedições, permanências ou viagem na camada gráfica.

A tela apresenta mapa conhecido, porto atual, data, condição e provisões do navio, capital e carga, serviços portuários, canais de informação, mercado, armada ativa quando houver, cronologia, escala histórica ativa e rotas de saída.

## Dois estados explicitamente distintos

### HISTORICAL

É o padrão. Abre em Lisboa em 8 de julho de 1497 com `EXP_GAMA_1497` ativa. A associação à armada não fixa identidade ou profissão do protagonista e não eleva seu conhecimento náutico.

O painel mostra a expedição, a perna corrente e `ChronologyMode`. Uma rota pode aparecer como disponível por `FLEET_COMMAND` mesmo quando o conhecimento pessoal ainda não é `OPERATIONAL`. O banner explicita: **comando institucional ≠ conhecimento pessoal**.

A primeira perna operacional é `R_LIS_STG`, Lisboa → São Thiago/baía de Santa Maria. A antiga aresta `R_LIS_CGH` permanece somente como conexão `STRATEGIC_AGGREGATE` e o domínio a bloqueia para execução.

Quando a chegada ativa uma permanência documentada, o painel mostra o nó da escala, `observed_stay_days`, atividades documentadas, data de partida e um botão `Esperar N dia(s)` enquanto a cronologia ainda é `GUIDED`.

### TECHNICAL

É um cenário de integração que começa em Calecute em 22 de maio de 1498. Permite testar `mercado -> compra -> viagem -> chegada -> venda` e também os canais informativos em um grande entreposto. Um banner informa que não representa o estado histórico inicial do personagem. Esse cenário usa cronologia `COUNTERFACTUAL`.

## Informação

O painel apresenta três botões compactos:

- `Ouvir rumor` → `RUMOR`;
- `Falar mercador` → `MERCHANT_CONTACT`;
- `Consultar piloto` → `PILOT_CONSULTATION`.

O botão só aparece acionável quando `GameSessionModel.information_opportunities()` encontra ao menos uma oportunidade que acrescenta conhecimento.

A interface **não mostra o alvo antes do clique**. Portanto não usa a própria UI para vazar um porto ou uma rota que o personagem ainda desconhece. Depois da ação, a mensagem informa o nó/rota revelado e o tempo gasto.

`RUMOR` pode ocorrer em portos e ancoradouros, mas não em `NAVIGATION_POINT` puro. Isso não transforma o ancoradouro em mercado. `MERCHANT_CONTACT` depende de `broker_availability`; `PILOT_CONSULTATION` depende de piloto historicamente registrado e competência específica de rota.

Cada interação custa um dia na v0.1 e usa o mesmo calendário de viagem, serviços e permanência. Em uma escala guiada, portanto, pode reduzir o tempo restante até a partida documentada. Nenhum canal concede provisões, condição, carga ou capital.

Os limites de conhecimento são definidos no domínio e em `simulation/information_rules.csv`: a interface não pode elevar rumor/contato/consulta a conhecimento de rota `OPERATIONAL`.

## Mapa

O mapa usa as coordenadas de `nodes.csv`. Somente nós com conhecimento geográfico pelo menos `RUMORED` aparecem. Linhas representam arestas do grafo, não derrotas históricas, correntes ou trajetos efetivamente navegados.

Uma rota pode ficar visível porque o personagem a conhece ou porque corresponde à perna corrente de uma expedição ativa. Isso não altera o estado de conhecimento pessoal. Conexões estratégicas agregadas podem continuar visíveis para leitura do grafo, mas o domínio não permite executá-las como viagem única.

A costa real permanece na ferramenta cartográfica de referência separada em `tools/render_cartographic_map.py`.

## Serviços portuários, permanência e mercado

O painel consulta `GameSessionModel.service_quote()` para provisões e reparo e mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` distintos.

`Reabastecer +30` solicita 30 dias-equivalentes e `Reparar +20` solicita 20 pontos abstratos de condição. Esses números são parâmetros de simulação. Em uma escala guiada, o tempo dessas ações conta contra o mesmo intervalo até a partida documentada.

O mercado usa `GameSessionModel.market_view()`. Se `market_knowledge < OPERATIONAL`, nenhuma mercadoria acionável é mostrada. Nós logísticos com `market_scale=NONE` não recebem mercadorias apenas por terem sido escalas da expedição.

## Viagem

Cada rota de saída é planejada pelo domínio. O painel exibe `OWN_KNOWLEDGE`, `PILOT`, `FLEET_COMMAND` ou bloqueio.

Quando existe piloto documentado para porto, período e rota, a interface o fornece ao plano antes de recorrer ao comando institucional. Isso preserva o caso Melinde–Calecute de 1498. Uma consulta prévia ao piloto não substitui esse papel operacional: ela só pode ensinar a rota até `PARTIAL`.

Em `GUIDED`, uma rota de saída é bloqueada por `HISTORICAL_STOP_NOT_RELEASED` enquanto a data estiver antes da partida da escala ativa. Se o jogador permanece além da partida e depois navega, o domínio muda para `COUNTERFACTUAL`; a interface exibe essa condição e não força novas esperas históricas.

## Interação

- `Ouvir rumor`, `Falar mercador` e `Consultar piloto` executam aquisição ativa de informação sem mostrar o alvo previamente;
- `Reabastecer +30` e `Reparar +20` acionam serviços do porto atual;
- `Esperar N dia(s)` avança somente o restante da permanência histórica guiada;
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
