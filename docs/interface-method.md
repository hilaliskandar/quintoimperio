# Método da interface jogável v0.1

## Objetivo

A interface Pygame v0.1 expõe o núcleo já implementado em `GameSessionModel` sem duplicar regras econômicas, de conhecimento ou de viagem na camada gráfica.

A tela apresenta mapa conhecido, porto atual, data, condição e provisões do navio, capital e carga, mercado do porto e rotas de saída. Compra, venda e viagem chamam diretamente os métodos do domínio.

## Dois estados explicitamente distintos

A interface oferece dois cenários porque o estado histórico inicial ainda não contém todos os mecanismos institucionais necessários para reproduzir a partida da armada de Vasco da Gama a partir de Lisboa.

### HISTORICAL

É o padrão. Abre em Lisboa em 8 de julho de 1497 usando `GameSessionModel.initial_state()` sem elevar conhecimento náutico ou mercantil para tornar ações possíveis. Se uma rota estiver bloqueada por conhecimento insuficiente, a interface mostra o bloqueio.

Esse comportamento é deliberado: uma limitação atual do modelo não deve ser ocultada por um parâmetro inventado.

### TECHNICAL

É um cenário de integração que começa em Calecute em 22 de maio de 1498 e reaplica somente os mesmos overrides explicitamente documentados no protótipo de sessão: mercado de Calecute operacional e rota Calecute–Aden operacional.

O cenário existe para permitir testar de forma interativa o ciclo `mercado -> compra -> viagem -> chegada -> venda`. Um banner vermelho informa que ele não representa o estado histórico inicial do personagem.

## Mapa

O mapa usa as coordenadas de `nodes.csv`. Somente nós com conhecimento geográfico pelo menos `RUMORED` aparecem. Linhas representam arestas do grafo cuja rota possui algum conhecimento náutico no estado atual; não representam derrotas históricas, correntes ou trajetos efetivamente navegados.

A v0.1 da interface continua usando fundo esquemático. A costa real permanece na ferramenta cartográfica de referência separada em `tools/render_cartographic_map.py`.

## Mercado

O painel chama `GameSessionModel.market_view()`. Se `market_knowledge` for inferior a `OPERATIONAL`, nenhuma mercadoria acionável é mostrada. Compra e venda usam `GameSessionModel.buy()` e `GameSessionModel.sell()` com quantidade unitária abstrata.

Capital, quantidade, capacidade, preço e volume continuam índices de simulação. A interface não os apresenta como cruzados, xerafins, quintais, toneladas ou preços históricos.

## Viagem

O painel lista rotas cuja origem coincide com o porto atual. Cada rota é planejada por `GameSessionModel.plan_voyage()`.

Quando o conhecimento próprio não basta, a interface procura um piloto apenas entre os pilotos historicamente registrados em `pilots.csv` e `pilot_routes.csv` que estejam ativos no porto, período e rota. Nenhum bônus de velocidade é atribuído ao piloto.

Uma viagem só é executada se o `VoyagePlan` for viável. A chegada chama `GameSessionModel.execute_voyage()` e portanto atualiza data, provisões, condição e aprendizagem de nó/rota segundo as regras já separadas em `simulation/`.

## Interação

- clique em uma mercadoria para selecioná-la;
- `Comprar 1` e `Vender 1` executam operações unitárias abstratas;
- clique em uma rota da lista ou em um porto de destino conectado no mapa para selecionar a rota;
- `Executar viagem` aplica o plano quando viável;
- `R` reinicia o cenário atual;
- `Tab` alterna entre `HISTORICAL` e `TECHNICAL`;
- `Esc` encerra.

## Teste reprodutível

A interface pode ser renderizada sem janela:

```bash
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario HISTORICAL --output /tmp/game-historical.png
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario TECHNICAL --output /tmp/game-technical.png
```

O GitHub Actions executa os dois smoke tests e publica as capturas como artefato do workflow para inspeção visual.
