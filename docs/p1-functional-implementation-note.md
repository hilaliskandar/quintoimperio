# P1-func — nota de implementação

Issue: #99.

A implementação funcional foi iniciada após a auditoria de arquitetura registrada em `docs/p1-functional-design-v01.md`. O desenho preserva `HistoricalCampaignModel` e introduz uma fachada opt-in para o retorno, de forma que o MVP Lisboa–Calecute continue encerrando em Calecute sem alteração de comportamento.

O primeiro incremento implementará apenas a ativação explícita de `EXP_GAMA_RETURN_1498`, reabastecimento específico de permanência documentada parametrizado como `SIMULATION` e um smoke canônico até BRG. Nenhum mercado ou serviço genérico será criado em `nodes.csv`; doença, mortalidade e frota física permanecem fora de escopo.