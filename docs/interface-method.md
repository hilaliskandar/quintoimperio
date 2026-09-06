# Método da interface jogável v0.1

## Objetivo

A interface Pygame v0.1 expõe `GameSessionModel` sem duplicar regras econômicas, de conhecimento, informação, acesso institucional, relações, serviços portuários, expedições, permanências, eventos marítimos ou viagem na camada gráfica.

A tela apresenta mapa conhecido, porto atual, data, condição e provisões do navio, capital e carga, estado de acesso, serviços portuários, canais de informação, relações já estabelecidas, mercado, armada ativa quando houver, cronologia, escala histórica ativa, rotas de saída e o último evento `SIM` de viagem quando houver.

A vertical slice histórica possui uma extensão em `prototype/historical_campaign.py`. Ela reutiliza o mesmo painel e acrescenta apenas a orquestração de campanha e, no gate relacional v0.2, a ação explícita de contato com autoridade documentada.

## Dois estados explicitamente distintos

### HISTORICAL

É o padrão. Abre em Lisboa em 8 de julho de 1497 com `EXP_GAMA_1497` ativa. A associação à armada não fixa identidade ou profissão do protagonista e não eleva seu conhecimento náutico.

O painel mostra a expedição, a perna corrente e `ChronologyMode`. Uma rota pode aparecer como disponível por `FLEET_COMMAND` mesmo quando o conhecimento pessoal ainda não é `OPERATIONAL`. O banner explicita: **comando institucional ≠ conhecimento pessoal**.

A primeira perna operacional é `R_LIS_STG`, Lisboa → São Thiago/baía de Santa Maria. A antiga aresta `R_LIS_CGH` permanece somente como conexão `STRATEGIC_AGGREGATE` e o domínio a bloqueia para execução.

Quando a chegada ativa uma permanência documentada, o painel mostra o nó da escala, `observed_stay_days`, atividades documentadas, data de partida e um botão `Esperar N dia(s)` enquanto a cronologia ainda é `GUIDED`.

Quando uma rota/data possui observação histórica exata e a sessão está em `GUIDED`, a mensagem de chegada explicita que eventos aleatórios foram suprimidos pela observação. A interface não inventa um incidente para tornar a viagem mais dramática.

### TECHNICAL

É um cenário de integração que começa em Calecute em 22 de maio de 1498. O override técnico concede conhecimento do mercado, rota Calecute–Aden e acesso inicial a Calecute para permitir a compra. Após a viagem, Aden volta a obedecer ao regime normal `FOREIGN_NEGOTIATED`, de modo que a sequência testável passa a ser `mercado -> compra -> viagem -> chegada -> negociação -> venda`.

O banner informa que esse cenário não representa o estado histórico inicial do personagem. Ele usa cronologia `COUNTERFACTUAL`.

## Acesso institucional

O painel consulta `GameSessionModel.access_view()` e mostra o estado e o `access_regime` do nó atual.

Quando `AccessView.negotiable=True`, aparece `Negociar acesso (Nd)`. A ação é delegada a `GameSessionModel.negotiate_access()` e a interface apenas mostra o resultado. Ela não calcula probabilidade de sucesso, não cobra taxa, não atribui valor a presente e não inventa diálogo.

O botão genérico existe somente para o gate `FOREIGN_NEGOTIATED`. `ROYAL_MONOPOLY`, `ROYAL_MONOPOLY_LEASED` e `MILITARY_POST` não recebem botão de abertura comercial comum. `ANCHORAGE_CONTACT` e `NAVIGATION_ONLY` permanecem não comerciais.

A interface separa conhecimento e autorização. Quando o mercado é conhecido operacionalmente mas o acesso ainda está bloqueado, as cotações da simulação podem ser exibidas com `actionable=False`, e os botões `Comprar`/`Vender` permanecem desabilitados. Isso permite representar a situação “sei o que circula aqui, mas ainda não posso operar”.

Mercadorias marcadas `restricted=TRUE` aparecem com `*` quando conhecidas. Mesmo depois de acesso portuário, a tentativa de operação é rejeitada pelo domínio; a interface não possui atalho para contornar a restrição específica.

## Relações

A interface não enumera atores apenas porque eles existem em `actors.csv`. Ela chama `GameSessionModel.contacted_relationships()` e exibe a seção `Relações estabelecidas` somente quando existe pelo menos um ator em `CONTACTED`.

Assim, um ator ainda `UNESTABLISHED` permanece invisível. Em Calecute, `MERCHANT_CONTACT` pode tornar visível a comunidade mercantil muçulmana/pardesi sem revelar automaticamente a autoridade do Samudri Raja. A negociação de acesso pode registrar contato com a autoridade sem tornar a comunidade mercantil conhecida por esse simples fato.

Na campanha histórica, `HistoricalCampaignPrototype` pode exibir `Contatar autoridade local documentada` quando o domínio encontra uma associação `AUTHORITY` válida para o nó/período e o ator ainda está `UNESTABLISHED`. O botão deliberadamente não revela o nome do ator antes do contato. A ação chama `RelationshipSessionModel.contact_authority()`; a UI não cria ator, não resolve sucesso e não concede acesso por conta própria.

Depois do contato, o ator pode aparecer em `Relações estabelecidas`. Em Melinde, o domínio passa a poder atribuir ao personagem o piloto guzerate historicamente documentado. A interface apenas reflete essa disponibilidade; não cria bônus de velocidade, segurança, consumo ou desgaste.

A relação continua sem alterar preço, crédito, acesso adicional, amizade ou hostilidade por simples existência.

## Informação

O painel apresenta três botões compactos:

- `Ouvir rumor` → `RUMOR`;
- `Falar mercador` → `MERCHANT_CONTACT`;
- `Consultar piloto` → `PILOT_CONSULTATION`.

O botão só aparece acionável quando `GameSessionModel.information_opportunities()` encontra ao menos uma oportunidade que acrescenta conhecimento.

A interface **não mostra o alvo antes do clique**. Portanto não usa a própria UI para vazar um porto ou uma rota que o personagem ainda desconhece. Depois da ação, a mensagem informa o nó/rota revelado e o tempo gasto.

`RUMOR` pode ocorrer em portos e ancoradouros, mas não em `NAVIGATION_POINT` puro. Isso não transforma o ancoradouro em mercado. `MERCHANT_CONTACT` depende de `broker_availability`; `PILOT_CONSULTATION` depende de piloto historicamente registrado e competência específica de rota.

Cada interação custa um dia na v0.1 e usa o mesmo calendário de viagem, serviços, negociação e permanência. Nenhum canal concede provisões, condição, carga ou capital.

## Mapa

O mapa usa as coordenadas de `nodes.csv`. Somente nós com conhecimento geográfico pelo menos `RUMORED` aparecem. Linhas representam arestas do grafo, não derrotas históricas, correntes ou trajetos efetivamente navegados.

Uma rota pode ficar visível porque o personagem a conhece ou porque corresponde à perna corrente de uma expedição ativa. Isso não altera o estado de conhecimento pessoal. Conexões estratégicas agregadas podem continuar visíveis para leitura do grafo, mas o domínio não permite executá-las como viagem única.

A posição dos pontos nunca é deslocada para melhorar a legibilidade. Para evitar sobreposição textual em regiões de nós próximos, apenas os rótulos recebem deslocamentos de apresentação e, quando necessário, uma linha-guia discreta até a coordenada real do nó. Testes de regressão verificam que os rótulos dos cenários padrão `HISTORICAL` e `TECHNICAL` não se sobreponham.

A costa real permanece na ferramenta cartográfica de referência separada em `tools/render_cartographic_map.py`.

## Serviços portuários, permanência e mercado

O painel consulta `GameSessionModel.service_quote()` para provisões e reparo e mantém `UNKNOWN`, `NONE`, `LOW`, `MEDIUM` e `HIGH` distintos.

`Reabastecer +30` solicita 30 dias-equivalentes e `Reparar +20` solicita 20 pontos abstratos de condição. Esses números são parâmetros de simulação. Em uma escala guiada, o tempo dessas ações — assim como informação, negociação e contato relacional — conta contra o mesmo intervalo até a partida documentada.

O mercado usa `GameSessionModel.market_view()`. Se `market_knowledge < OPERATIONAL`, a cesta permanece oculta. Se o conhecimento é operacional mas o acesso não está concedido, a cesta pode ser lida e a operação fica bloqueada. Nós logísticos com `market_scale=NONE` não recebem mercadorias apenas por terem sido escalas da expedição.

## Viagem e eventos marítimos

Cada rota de saída é planejada pelo domínio. O painel exibe `OWN_KNOWLEDGE`, `PILOT`, `FLEET_COMMAND` ou bloqueio.

A campanha histórica distingue a disponibilidade documentada do piloto de sua atribuição ao personagem. Em Melinde, `TravelModel` pode confirmar que o piloto guzerate está historicamente disponível para rota/período, mas `HistoricalCampaignModel.recommended_pilot_id()` só o fornece à camada pessoal depois do contato com a autoridade documentada que o enviou. Sem esse contato, `FLEET_COMMAND` continua sendo uma base institucional separada e pode permanecer a base da viagem.

Uma consulta prévia ao piloto não substitui esse papel operacional: ela só pode ensinar a rota até `PARTIAL`.

Em `GUIDED`, uma rota de saída é bloqueada por `HISTORICAL_STOP_NOT_RELEASED` enquanto a data estiver antes da partida da escala ativa. Se o jogador permanece além da partida e depois navega, o domínio muda para `COUNTERFACTUAL`; a interface exibe essa condição e não força novas esperas históricas.

Os eventos marítimos não são sorteados nem interpretados pela camada gráfica. `VoyagePlan.events` vem pronto do domínio. Quando há evento, a mensagem de chegada o identifica explicitamente como `evento SIM`, com dias adicionais e perda abstrata de condição. O painel mantém o último evento da sessão visível para auditoria. Quando `events_suppressed_by_observation=True`, a mensagem informa que a aleatoriedade foi suprimida pela observação histórica.

A interface não apresenta calmaria, mau tempo ou avaria genérica como fato histórico. Também não cria perdas de tripulação, carga, combate ou naufrágio, pois esses efeitos não existem na v0.1.

## Interação

- `Negociar acesso (Nd)` aparece somente onde o gate institucional é negociável;
- `Contatar autoridade local documentada` aparece na campanha somente quando há autoridade normalizada ainda não contatada;
- `Ouvir rumor`, `Falar mercador` e `Consultar piloto` executam aquisição ativa de informação sem mostrar o alvo previamente;
- relações já estabelecidas aparecem somente depois do contato correspondente;
- `Reabastecer +30` e `Reparar +20` acionam serviços do porto atual;
- `Esperar N dia(s)` avança somente o restante da permanência histórica guiada;
- clique em mercadoria, depois `Comprar 1` ou `Vender 1` quando o mercado estiver acionável;
- clique em rota ou destino conectado e use `Executar viagem`;
- `R` reinicia;
- `Tab` alterna `HISTORICAL`/`TECHNICAL` no protótipo-base;
- `Esc` encerra.

## Inspeção visual e teste reprodutível

As telas-base e o smoke final da campanha são renderizados no CI:

```bash
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario HISTORICAL --output /tmp/game-historical.png
SDL_VIDEODRIVER=dummy python prototype/game.py --scenario TECHNICAL --output /tmp/game-technical.png
SDL_VIDEODRIVER=dummy python prototype/historical_campaign.py --campaign-smoke --output /tmp/campaign-calicut.png
```

O GitHub Actions executa os smoke tests e publica as capturas como artefato para inspeção visual. Além disso, testes específicos verificam o não vazamento de atores `UNESTABLISHED`, a separação entre contato e acesso, a atribuição relacional do piloto e a ausência de sobreposição entre rótulos cartográficos nos cenários padrão.
