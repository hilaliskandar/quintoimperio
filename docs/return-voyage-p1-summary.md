# P1 — Síntese do gate documental do retorno 1498–1499

Issue: #92.

Documentos produzidos neste gate:

1. `docs/return-voyage-evidence-p1.md` — matriz cronológica do retorno e quebra de proveniência no fim do `Roteiro`.
2. `docs/return-voyage-cartographic-audit-p1-1.md` — auditoria de Santa Maria, Anjediva, Baixos de São Rafael, Ilhas de São Jorge e Rio Grande.
3. `docs/return-voyage-post-manuscript-audit-p1-2.md` — auditoria do trecho posterior a 25/04/1499 e das tradições cronísticas divergentes.
4. `docs/return-voyage-data-proposal-p1-3.md` — tradução documental proposta para dados, ainda sem alteração de `data/`.

## Conclusão

O retorno está documentalmente reconstruído em nível suficiente para iniciar um gate técnico de schema, mas ainda não para inserir coordenadas ou rotas diretamente.

A sequência primária proposta até o fim do manuscrito é:

`CAL → SMI → ANJ → MAL → BSR → SJO → SBR → CGH → RGR`

Somente `ANJ` é, nesta etapa, novo candidato forte a escala logística plena. `SMI`, `BSR`, `SJO` e `RGR` devem permanecer marcos náuticos/nós-evento ou observações até que o motor demonstre necessidade de materializá-los como nós.

Depois de `RGR`, a evidência muda para síntese editorial e tradições cronísticas. O retorno final deve preservar as trajetórias divergentes de Bérrio, S. Gabriel e Vasco da Gama e as datas concorrentes de chegada a Lisboa.

## Próximo gate recomendado

Auditar o schema atual antes de qualquer alteração de dados. A pergunta técnica é se os modelos existentes conseguem representar:

- camada de evidência (`PRIMARY_NARRATIVE` / `EDITORIAL_SYNTHESIS`);
- datas alternativas ou intervalos;
- redução de frota e mudança de comando;
- trajetória de personagem separada de embarcação;
- marcos náuticos sem mercado/serviços.

Se puderem, inserir os dados em pequeno PR. Se não puderem, abrir uma issue técnica de schema isolada, sem ampliar o escopo.