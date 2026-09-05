# Método de acesso institucional v0.1

## Objetivo

Separar três coisas que antes podiam ser confundidas no loop: conhecer um mercado, estar fisicamente no porto e possuir autorização institucional suficiente para operar comercialmente. `AccessModel` não cria nova evidência histórica; ele traduz o campo `access_regime` de `data/nodes.csv` em estados jogáveis por regras explícitas de `simulation/access_rules.csv`.

## Estados

A v0.1 usa:

- `OPEN`: acesso comercial inicial permitido no protótipo;
- `NEGOTIATION_REQUIRED`: o mercado pode ser conhecido, mas compra/venda exige uma ação institucional explícita;
- `NEGOTIATED`: o gate institucional genérico foi satisfeito na sessão;
- `RESTRICTED`: o regime não é desbloqueado por negociação portuária genérica;
- `NONCOMMERCIAL`: o nó não é tratado como mercado;
- `UNKNOWN`: não existe regra suficiente para afirmar disponibilidade.

Esses estados não são classificações historiográficas autônomas. São a tradução operacional das categorias já armazenadas na base.

## Mapeamento inicial

Na v0.1:

- `OPEN_MARKET` e `CAPTAINCY` → `OPEN`;
- `FOREIGN_NEGOTIATED` → `NEGOTIATION_REQUIRED`;
- `ROYAL_MONOPOLY`, `ROYAL_MONOPOLY_LEASED` e `MILITARY_POST` → `RESTRICTED`;
- `ANCHORAGE_CONTACT` e `NAVIGATION_ONLY` → `NONCOMMERCIAL`.

A regra evita dois atalhos incorretos: uma ancoragem de contato não vira mercado, e um monopólio régio não se torna comércio ordinário apenas porque o personagem clicou em “negociar”.

## Negociação genérica

A negociação v0.1 existe apenas para nós classificados como `FOREIGN_NEGOTIATED` que já possuem mercado na base. Ela consome um dia de simulação e transforma `NEGOTIATION_REQUIRED` em `NEGOTIATED`.

Esse dia é um parâmetro de jogabilidade. Não é duração documentada de audiência, protocolo diplomático, barganha ou espera portuária. Não há sorteio de sucesso nesta primeira versão, porque atribuir probabilidades sem base acrescentaria uma precisão falsa.

Também não há débito monetário, valor de presentes, tributo, imposto, comissão ou suborno. Esses elementos exigem documentação ou uma camada de simulação separada e explicitamente justificada.

`broker_availability` é mostrado como contexto quando conhecido, mas sua ausência não é convertida em inexistência de intermediário. O próprio `FOREIGN_NEGOTIATED` já é o gate estrutural utilizado nesta versão.

## Mercado conhecido versus mercado acessível

`MarketView` mantém conhecimento e acesso separados. Se `market_knowledge < OPERATIONAL`, a cesta comercial continua oculta. Se o conhecimento é operacional mas o acesso ainda não foi negociado, as cotações já conhecidas podem ser consultadas, porém `actionable=False` e compra/venda são bloqueadas.

Assim, a chegada física pode melhorar conhecimento de Calecute sem conceder automaticamente autorização para comerciar.

## Restrições específicas de mercadorias

`node_goods.restricted=TRUE` é independente do gate portuário. `TradeModel` bloqueia diretamente esses bens com `GOOD_RESTRICTED_BY_HISTORICAL_ACCESS_REGIME`.

Portanto uma autorização portuária genérica — ou mesmo um override técnico de acesso — não transforma ouro de Arguim ou Elmina em mercadoria ordinariamente disponível ao personagem. Uma futura mecânica de licença, concessão ou participação régia deverá ser modelada separadamente.

## Calecute e 1498

Calecute é um bom teste porque `nodes.csv` o classifica como `FOREIGN_NEGOTIATED`, mas o botão genérico não pretende reconstruir a audiência de Vasco da Gama com o Samudri/Zamorin. A v0.1 não atribui valor aos presentes portugueses, não reproduz falas, não define uma taxa de sucesso diplomático e não afirma que a negociação durou um dia.

O mecanismo representa apenas a necessidade estrutural de mediação/autorização antes de converter conhecimento mercantil em operação comercial.

## Relação com cronologia e permanências

A negociação usa o mesmo `GameClock` dos demais sistemas. Se realizada durante uma permanência histórica guiada, consome parte do intervalo antes da partida documentada. Não concede provisões, reparos, conhecimento náutico, reputação ou mercadorias por si só.

## Cenários técnicos

`scenario_set_access()` existe para testes e demonstrações. Ele é explicitamente contrafactual e não altera o regime histórico do nó. O cenário técnico Calecute → Aden usa esse override apenas na origem para começar o teste comercial; em Aden a negociação pode ser exercitada como ação normal.

## Próximo passo

Acesso e negociação ainda não são reputação. A próxima camada deve introduzir relações com autoridades e comunidades mercantis sem reduzir todos os atores a uma única pontuação global e sem retroagir automaticamente sobre fatos já documentados.
