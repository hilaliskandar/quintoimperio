# Gate final do MVP Lisboa–Calecute

Status: candidato a MVP após o fechamento do M7.

Base auditada: `main` no commit `52e17c80738a10b55160b16cedb3bc1c01326b32`.

## Escopo do MVP

O MVP é a vertical slice da primeira viagem portuguesa de 1497–1498, iniciada em Lisboa em 8 de julho de 1497 e encerrada após a primeira estadia jogável em Calecute. O objetivo deste gate é apenas verificar o estado integrado do projeto; nenhuma mecânica nova é introduzida aqui.

## Matriz de verificação M8

| Critério do roadmap | Evidência atual | Resultado |
|---|---|---|
| Campanha inicia em Lisboa e chega a Calecute pela interface comum | `HistoricalCampaignModel`, `prototype/historical_campaign.py`, testes de campanha e smoke da interface histórica | ATENDE |
| Nenhuma etapa exige `TECHNICAL` ou override de teste | campanha histórica usa `EXP_GAMA_1497`; overrides `scenario_*` permanecem separados e não são usados no fluxo canônico | ATENDE |
| Divergências históricas mudam para `COUNTERFACTUAL` | testes de campanha cobrem partida tardia e permanência do modo contrafactual | ATENDE |
| Mercado, acesso e relações permanecem estados distintos | `GameSessionState` mantém conhecimento, `AccessRecord` e `RelationshipRecord` separados; compra/venda consulta conhecimento e acesso explicitamente | ATENDE |
| Existe ao menos uma decisão comercial real | M3 integrou quantidade selecionável e compra/venda; campanha em Calecute negocia acesso e executa operação comercial elegível | ATENDE |
| Existem objetivos e condição explícita de encerramento | `CampaignProgressModel` deriva marcos do estado e conclui após a primeira operação comercial elegível em Calecute | ATENDE |
| Save/load preserva o estado | `CampaignPersistence` usa schema JSON versionado e testes de round-trip por igualdade estrutural | ATENDE |
| CI integralmente verde | M7 passou com validação de dados, domínio, protótipos, interfaces, persistência e mapas | ATENDE |
| Smoke tests de interface e mapas aprovados | workflow executa interface histórica, interface v0.2, persistência M6, mapa de coordenadas e referência cartográfica | ATENDE |
| Revisão automática sem achado concreto bloqueador | último PR funcional M7 não registrou thread de revisão bloqueadora após CI verde | ATENDE |
| Documentação sincronizada com o comportamento real | este documento consolida o estado final e delimita o pós-MVP; README/roadmap devem apontar para este gate na próxima revisão editorial | ATENDE COM OBSERVAÇÃO EDITORIAL |

## Robustez consolidada no M7

A suíte `tests/test_mvp_robustness.py` registra os invariantes necessários antes do gate final:

- a campanha `GUIDED` chega a Calecute nas seeds `0`, `1`, `7`, `42` e `1498` com o mesmo estado terminal;
- observações históricas exatas suprimem eventos de simulação em `GUIDED`;
- em `COUNTERFACTUAL`, o mesmo estado e a mesma seed produzem o mesmo plano;
- eventos genéricos permanecem limitados a um por viagem, até três dias adicionais e até cinco pontos abstratos de condição;
- compra e venda repetidas no mesmo mercado não geram capital gratuito;
- mercados desconhecidos não revelam mercadorias e atores não contatados permanecem ocultos;
- espera histórica avança o relógio sem criar provisões, condição, capital, conhecimento ou relações.

Nenhum parâmetro em `simulation/` precisou ser alterado para fechar M7.

## Estado funcional consolidado

O MVP inclui:

1. campanha contínua Lisboa → Calecute pelas dez pernas normalizadas;
2. cronologia `GUIDED` e `COUNTERFACTUAL`;
3. provisões, condição, espera, reabastecimento e reparo por ações explícitas;
4. conhecimento por nó e por rota;
5. aquisição de informação por canais parametrizados;
6. acesso institucional separado de conhecimento e relações;
7. relações por atores historicamente normalizados;
8. piloto de Melinde limitado à rota documentada;
9. mercado documentado, quantidade selecionável e compra/venda;
10. objetivos derivados do estado e encerramento explícito em Calecute;
11. interface v0.2 com confirmação de viagem, histórico curto e indicação de cronologia;
12. persistência JSON versionada em slot único;
13. validação automática, smoke tests e cartografia programática.

## Limites que permanecem pós-MVP

Não fazem parte desta versão:

- retorno a Lisboa;
- Cochim e expansão cronológica além da primeira estadia em Calecute;
- crédito, câmbio, juros, contratos mercantis complexos ou moeda histórica completa;
- reputação global, diplomacia geral ou sistema amplo de facções;
- combate, doença, perdas de tripulação, naufrágio e controle individual da tripulação;
- múltiplos slots, nuvem ou migrações sofisticadas de save;
- refinamento estético amplo da interface;
- novos fatos, atores, portos, mercados ou rotas sem base documental.

## Decisão do gate

Do ponto de vista funcional e metodológico, o conjunto M0–M7 satisfaz os critérios técnicos do M8. O único ponto restante após o merge deste gate é a marcação do commit final de `main` com uma tag de versão do MVP. A expansão cronológica só deve começar depois dessa marcação.
