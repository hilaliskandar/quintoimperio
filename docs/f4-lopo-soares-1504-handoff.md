# F4 — Lopo Soares 1504 — handoff funcional

Data: 2026-09-08
Baseline: `b086f657b12281016570ac168771e99ca200f0f0`
Gate documental encerrado: #115
Gate-mãe: #118

## Decisão de arquitetura

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

A F4 deve usar eventos guiados estruturados e estados temporais. Não criar combate geral, microtática, HP, moral, dano, baixas ou força quantitativa.

## Estado herdado

Em 31/12/1503, Cochim deve preservar soberania local, feitoria restaurada, Forte Manuel, guarnição portuguesa, acesso negociado e relação favorável.

## Primeiro incremento recomendado

1. registrar `EXP_LOPO_SOARES_1504` como expedição histórica sem pernas executáveis;
2. provar em teste que o catálogo reconhece a expedição e que ela não pode ser ativada sem pernas;
3. carregar o estado de Cochim de 1503 para 1504 sem duplicação;
4. somente depois normalizar a cadeia defensiva de 1504 com janelas documentais conservadoras;
5. Coulão permanece fora do grafo até necessidade funcional demonstrada;
6. nenhuma bateria de arquétipos enquanto não houver nova decisão jogável.

## Documentos de referência

- `docs/p3-5-lopo-soares-1504-evidence-v0.1.md`;
- `docs/p3-5-1504-defense-decision-matrix-v0.1.md`;
- `docs/p3-5-1504-minimal-normalization-proposal.md`;
- `docs/p3-5-lopo-soares-1504-closeout.md`.

## Gate de saída

F4 deve encerrar com estado de 1504 reproduzível por data, soberania local preservada, armada de Lopo registrada sem itinerário inventado, defesa representada sem combate sistêmico, save/load íntegro e regressão completa verde.
