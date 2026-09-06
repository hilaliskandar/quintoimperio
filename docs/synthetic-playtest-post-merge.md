# Validação sintética pós-merge da preparação logística

## Objetivo

Este registro documenta a revalidação da preparação pré-partida e da margem logística de 20 dias-equivalentes após a integração da issue #58 e da frota física experimental da issue #59.

A validação preserva o painel de 20 sessões independentes: cinco perfis (`DISCIPLINED`, `CAUTIOUS`, `IMPATIENT`, `FRUGAL`, `TRADER`) e quatro seeds por perfil. Os jogadores sintéticos usam apenas ações e informações públicas do domínio. Nenhum teste imputa provisões em nós `UNKNOWN`, concede recursos automaticamente ou altera datas, eventos, comércio ou preços.

## Referência experimental

A onda 8 havia estabelecido, com janela simulada de dois dias antes da partida de 1497-07-08:

- reserva 10: 12/20 conclusões;
- reserva 20: 20/20 conclusões e 0 `COUNTERFACTUAL`;
- reserva 30: 20/20 conclusões e 0 `COUNTERFACTUAL`.

A margem de 20 permanece, portanto, uma heurística de robustez do jogo e não um dado histórico.

## Controle pós-merge 1 — adesão livre

A onda 9 abriu a campanha por `initial_playable_state()` e expôs `logistics_planning_view()` aos jogadores. `FRUGAL` e `IMPATIENT` podiam ignorar deliberadamente a recomendação.

Resultado:

- 12/20 conclusões;
- 8/20 `COUNTERFACTUAL`;
- `DISCIPLINED`, `CAUTIOUS` e `TRADER`: 4/4 conclusões;
- `FRUGAL` e `IMPATIENT`: 0/4 conclusões.

Os oito desvios concentraram-se exatamente nos perfis programados para ignorar a recomendação. Esse controle não indicou regressão do domínio; mostrou apenas que a recomendação continuava opcional e que a não adesão tinha custo.

## Controle pós-merge 2 — política equivalente antes do horizonte

Na primeira execução da onda 10, todos os perfis tentaram seguir a margem de 20. `IMPATIENT` preservou apenas a tentativa precoce antes de corrigir a ação por meio do bloqueio público.

Resultado:

- 12/20 conclusões;
- 0/20 `COUNTERFACTUAL`;
- os oito casos não concluídos (`FRUGAL` e `IMPATIENT`) chegaram a Melinde em 1498-04-24, ainda em cronologia `GUIDED`.

Esse resultado isolou o problema: o indicador avaliava a margem apenas depois da próxima perna. Em Melinde, a evidência histórica de provisões é indeterminada, logo já era tarde para constituir a reserva necessária para Melinde–Calecute. A reserva da onda 8 havia sido formada em momentos elegíveis anteriores.

## Correção — horizonte até abastecimento documentado

A issue #68 introduziu um horizonte logístico explícito. O `LogisticsPlanningView` passou a distinguir:

- requisito da próxima perna;
- requisito cumulativo do horizonte até o próximo destino com provisões historicamente documentadas e acionáveis;
- nó-limite do horizonte;
- margem restante após esse horizonte.

`UNKNOWN` permanece indeterminado e `NONE` permanece indisponível. O cálculo não cria serviço e não concede provisões.

No Rio dos Bons Sinais, último ponto elegível antes da cadeia oriental, o horizonte cobre:

`RBS → MOZ → MOM → MAL → CAL`

As durações observadas preservadas para essas pernas totalizam 43 dias-equivalentes de viagem (6 + 9 + 1 + 27). A recomendação de 20 dias passa, portanto, a sinalizar 63 dias-equivalentes de autonomia como referência de planejamento naquele ponto. Esse valor é uma composição do modelo: 43 dias derivados das observações de viagem preservadas mais a margem heurística de 20; não é uma quantidade histórica documentada de mantimentos.

## Controle pós-merge 3 — política equivalente com horizonte

A onda 10 foi repetida, sem alterar perfis, seeds ou parâmetros, usando apenas a nova leitura do horizonte.

Resultado final:

- **20/20 conclusões**;
- **0/20 `COUNTERFACTUAL`**;
- `DISCIPLINED`: 4/4;
- `CAUTIOUS`: 4/4;
- `IMPATIENT`: 4/4;
- `FRUGAL`: 4/4;
- `TRADER`: 4/4;
- todas as sessões chegaram a Calecute em 1498-05-22 sob cronologia `GUIDED`.

O resultado reproduz a referência experimental da onda 8 na implementação integrada e mostra que a informação decisiva não é apenas a margem de 20, mas a combinação entre margem e horizonte até o próximo abastecimento historicamente documentado.

## Conclusão

A revalidação sustenta três distinções do desenho:

1. a janela de dois dias resolve o problema temporal sem reescrever a partida histórica de 1497-07-08;
2. a margem de 20 continua sendo recomendação heurística, não requisito rígido nem recurso automático;
3. a recomendação só é operacionalmente equivalente à evidência da onda 8 quando aplicada ao horizonte de navegação que atravessa escalas sem abastecimento documentado.

A CI geral, os testes de domínio, a interface histórica, a persistência e os smokes permaneceram verdes após a correção.
