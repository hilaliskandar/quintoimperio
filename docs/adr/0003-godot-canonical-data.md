# ADR 0003 — Dados canônicos e recursos derivados no Godot

Status: **aceito**

Data: 2026-09-08

## Contexto

O domínio congelado separa evidência histórica em `data/` de parâmetros de simulação em `simulation/`. A migração para Godot não pode introduzir uma segunda fonte manual em cenas, scripts ou recursos `.tres`, pois isso criaria divergência silenciosa entre pesquisa, referência Python e runtime de produção.

## Decisão

`data/` e `simulation/` permanecem as fontes canônicas do projeto durante e após a migração.

O Godot deve:

- ler os CSVs canônicos diretamente durante G0, como faz `CanonicalData`;
- preservar strings identificadoras e campos vazios sem coerção implícita;
- validar cabeçalhos necessários antes de consumir uma tabela;
- manter a distinção de proveniência entre fato histórico e parâmetro de simulação.

Recursos Godot derivados são permitidos apenas quando forem:

1. gerados de forma reprodutível a partir das fontes canônicas;
2. descartáveis e regeneráveis;
3. rastreáveis ao arquivo e versão de origem;
4. verificados por paridade antes de substituir leitura direta no runtime.

É proibida a manutenção manual paralela do mesmo fato em CSV e `.tres`/cena/script.

## Consequências

- pesquisadores continuam editando a mesma camada de dados independentemente do engine;
- o runtime Godot não passa a ser uma base histórica concorrente;
- otimizações futuras de importação são possíveis sem alterar a fonte de verdade;
- qualquer pipeline de assets derivados deverá ser tratado como build, não como autoria factual.
