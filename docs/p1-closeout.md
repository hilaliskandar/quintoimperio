# P1 — fechamento documental do retorno 1498–1499

Issue: #92.

Data de fechamento documental: 2026-09-07.

## Objetivo deste gate

Confrontar os critérios originais da issue #92 com os documentos, dados e testes já incorporados após o commit de referência do MVP Lisboa–Calecute e decidir se ainda existe lacuna documental que impeça o avanço para integração funcional do retorno.

## Matriz de verificação

| Critério da #92 | Evidência incorporada | Resultado |
|---|---|---|
| reconstruir itinerário e cronologia do retorno | `docs/return-voyage-evidence-p1.md`, `data/expedition_routes.csv`, `data/voyage_observations.csv` | ATENDIDO |
| distinguir datas documentadas de reconstruções editoriais | matriz P1, auditoria pós-manuscrito e `expedition_epilogue_events.csv` | ATENDIDO |
| preservar divergências entre fontes | variantes 10/11-07 do Bérrio e 29-08/08-09/18-09 de Vasco da Gama permanecem separadas | ATENDIDO |
| composição da frota, perdas e mudanças de comando apenas quando sustentadas | queima do S. Rafael registrada como evento específico; João de Sá e trajetórias divergentes registradas no epílogo | ATENDIDO |
| escalas, reparos e reabastecimentos sustentados por fonte | Anjediva, Melinde, Baixos de São Rafael e São Brás registrados em `expedition_stops.csv` com atividades separadas | ATENDIDO |
| não converter ancoradouros em mercados sem evidência | novos nós do retorno mantêm `market_scale=NONE`; BSR/BRG são `NAVIGATION_POINT`; Anjediva não recebe mercado | ATENDIDO |
| classificação cartográfica dos novos candidatos | `docs/return-voyage-cartographic-audit-p1-1.md` | ATENDIDO |
| produzir matriz de evidências por perna e proposta de segmentação | `docs/return-voyage-evidence-p1.md` e `docs/return-voyage-data-proposal-p1-3.md` | ATENDIDO |
| registrar lacunas que exijam pesquisa adicional | lacunas documentadas e schema auditado; a única lacuna estrutural relevante foi isolada na #93 | ATENDIDO |
| somente depois do gate documental alterar o recorte executável | inserção de dados ocorreu após auditorias e preserva o MVP de dez pernas por teste de regressão | ATENDIDO |

## Resultado da auditoria

Não foi encontrada lacuna documental residual que justifique manter P1/#92 aberto como frente de pesquisa ampla.

O retorno até 25/04/1499 está representado como subcampanha documental contínua até os Baixos do Rio Grande, preservando a assimetria em relação à ida. O trecho posterior ao fim do manuscrito permanece separado em uma camada de epílogo documental, em vez de ser forçado para uma única sequência operacional.

A solução para o pós-manuscrito é deliberadamente mínima. `data/expedition_epilogue_events.csv` registra trajetórias independentes de Bérrio/Nicolau Coelho, S. Gabriel/João de Sá e Vasco da Gama; datas alternativas e limites temporais permanecem explícitos. Isso atende ao problema identificado na #93 sem exigir ainda um sistema geral de personagens ou frota.

## Não regressão

`tests/test_return_voyage_data.py` exige que a expedição de ida `EXP_GAMA_1497` permaneça com exatamente dez pernas e que a nova subcampanha do retorno seja contínua até BRG. O mesmo teste impede a criação implícita de mercados nos novos nós e valida a queima do S. Rafael como evento específico da expedição.

## Decisão

O gate documental P1 está concluído. A issue #92 pode ser encerrada como `completed`.

O próximo gate não é nova pesquisa ampla do retorno. É **P1 funcional — integração jogável mínima do retorno**, utilizando somente os dados já auditados e mantendo o epílogo divergente fora do loop jogável até existir necessidade demonstrada de generalizar trajetórias/personagens.

## Próximo gate funcional

1. auditar quais estruturas do domínio atual já consomem a nova `EXP_GAMA_RETURN_1498` sem alteração;
2. definir o menor estado de transição Calecute → retorno que preserve o encerramento atual do MVP como baseline;
3. habilitar as seis pernas do retorno até BRG sem mexer em fatos históricos ou introduzir doença/tripulação genéricas;
4. representar eventos documentais específicos por projeções do estado existente sempre que possível;
5. acrescentar smoke test do retorno e regressão integral Lisboa–Calecute;
6. executar pequena bateria sintética com seeds reproduzíveis para detectar blockers e inconsistências antes de balancear;
7. sincronizar README, roadmap, diário e espelho no Drive ao fechar o gate funcional.

## Regra de memória

Cada gate posterior deve deixar no repositório: decisão, evidência utilizada, testes, issue/PR/commit e próximo passo; o Drive deve permanecer como espelho de acompanhamento. O arquivo `docs/p1-roadmap-handoff-2026-09-07.md` registra o procedimento geral de retomada e continuidade.