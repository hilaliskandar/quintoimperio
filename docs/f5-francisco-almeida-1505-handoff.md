# F5 — handoff funcional de Francisco de Almeida em 1505

Data: 2026-09-08
Issue funcional: #134
Baseline integrado: `5e10409fa10e4b412f3ffcb3232d9674c09c1773`
CI pós-merge do gate documental: `34192641101` — verde

## Estado de partida

O gate documental F5 (#132) foi concluído e integrado pelo PR #133. A implementação funcional deve partir exclusivamente das decisões consolidadas em:

- `docs/f5-1505-minimal-normalization-proposal.md`;
- `docs/f5-1505-documentary-closeout.md`;
- `docs/f5-1505-evidence-matrix-v0.1.md`;
- `docs/f5-1505-institutional-matrix-v0.1.md`;
- `docs/f5-1505-authority-fleet-audit-v0.1.md`;
- `docs/f5-1505-route-chronology-audit-v0.1.md`;
- `docs/f5-1505-sofala-anhaia-anjediva-audit-v0.1.md`;
- `docs/f5-1505-cannanore-cochin-audit-v0.1.md`.

## Decisões fechadas

1. `COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO` para o horizonte 1505.
2. Não criar schema global de vice-reinado/governo enquanto não houver consumidor funcional que o exija.
3. `node_state_events.csv` é a camada preferencial para fortificação, guarnição, presença institucional, acesso, relação e soberania.
4. A autoridade de Francisco de Almeida deve permanecer decomposta entre nomeação régia, comando expedicionário e exercício institucional no Índico; não deve ser retroprojetada como estado único desde Lisboa.
5. O tamanho da armada permanece `UNRESOLVED` diante das variantes 20/21/22/23 e não deve virar parâmetro factual único.
6. Soberania local deve permanecer explícita em Cananor e Cochim mesmo com fortificação/guarnição portuguesa.
7. Sofala/Pêro de Anhaia deve permanecer unidade histórica própria quando necessário; não deve ser comprimida na armada principal.
8. Anjediva deve usar janela conservadora em setembro enquanto a divergência 13/09 × 14/09 não for resolvida.
9. A chegada diária de Almeida a Cochim não deve ser fixada sem evidência melhor; para o freeze de 31/12/1505 basta o terminus ante quem documentalmente seguro.
10. A divergência `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` permanece aberta e não deve ser harmonizada silenciosamente.

## Checkpoints funcionais concluídos

### Catálogo de Almeida

- `EXP_ALMEIDA_1505` registrado sem `fleet_size` factual único e sem pernas jogáveis;
- teste de catálogo/não ativação em `tests/test_f5_almeida_registry.py`;
- CI `34192932424` integralmente verde.

### Estados persistentes — Sofala e Cananor

- `SOF1505_E01`: presença institucional/capitania em `04/09/1505`, sem antecipar forte ou guarnição;
- `SOF1505_E02`: fortificação e guarnição em `21/09/1505`, mantendo soberania local explícita;
- `CAN1505_E01`: janela conservadora `23–31/10/1505`; forte e guarnição só se tornam efetivos em `31/10` pela semântica do modelo; feitoria e acesso negociado são preservados e a relação passa a `TENSE`, não `HOSTILE`;
- teste em `tests/test_f5_1505_node_states.py` cobre ordem temporal, não retroprojeção e soberania local;
- a primeira CI do teste (`34193339030`) falhou porque `SOF1505_E01` escrevia `NONE` sobre o baseline `LOW` de fortificação de Sofala;
- correção `5ee221d8428a8f50c2a4fbe7b084a10f0e59d46c`: campos de fortificação/guarnição do evento inicial ficam vazios, preservando o baseline até a tranqueira;
- CI corrigida `34193403253` integralmente verde.

### Expedição separada de Pêro de Anhaia

- `EXP_ANHAIA_1505` registrado como `ROYAL_FORTIFICATION_MISSION`, período 1505–1506 e partida documentada em `18/05/1505`;
- permanece unidade documental separada de `EXP_ALMEIDA_1505`, sem pernas executáveis e sem exigir múltiplas frotas simultâneas;
- teste em `tests/test_f5_anhaia_registry.py` comprova separação de catálogo e não ativação;
- commits `6b69463431498905d503ff1dd9fec397f7becdbf` e `11fbfd2c509d2af8def3be2dc753cb8889c9d908`;
- CI `34193505777` integralmente verde.

### Estados persistentes — Quiloa e Anjediva

- `KIL1505_E01`: janela `22–24/07/1505`; o estado persistente de presença fortificada e guarnição só é aplicado em `24/07`, preservando a diferença entre entrada e ocupação;
- a soberania não é convertida automaticamente em portuguesa e o evento não cria mecânica geral de combate;
- `ANJ1505_E01`: janela mensal `01–30/09/1505`; 13/09 e 14/09 continuam candidatos historiográficos e não são promovidos a `EXACT`;
- em Anjediva, fortificação e guarnição só se tornam efetivas em `30/09`, pela regra conservadora de `NodeStateEventModel`;
- teste em `tests/test_f5_kilwa_anjediva_states.py` cobre limites temporais e não anexação automática;
- commits `33ab2b7a201ffdb2ba71d9334736d72433c5fcd1` e `7ae93ec8a38457cd06b8f3b84f303d95f258c3c7`;
- CI `34193613911` integralmente verde.

## Próximos incrementos

Implementar em sequência estreita, com CI a cada gate:

1. representar nomeação, Regimento, partida, exercício institucional no Índico e presença segura em Cochim como eventos da expedição de Almeida;
2. representar a centralidade administrativa de Cochim sem alterar soberania nem duplicar fortificação/guarnição herdadas de 1503;
3. fechar teste de estado em `1505-12-31` e save/load;
4. executar regressão integral; somente depois avaliar necessidade de campanha jogável adicional.

## Restrições

Não implementar por antecipação:

- combate geral, microtática, HP, dano, moral ou baixas;
- múltiplas frotas simultâneas;
- sistema global de governo/autoridade;
- itinerários diários reconstruídos por analogia;
- novos nós sem necessidade demonstrada;
- resolução artificial das divergências documentais.

## Critério de fechamento F5

A tranche pode ser encerrada quando o estado de `31/12/1505` for determinístico, reproduzível por save/load, preservar as soberanias locais e passar CI/regressão integral sem introduzir nova mecânica geral não demonstrada. O fechamento deve produzir `domain-freeze-1505` ou handoff explícito para o gate final do Python 1505 GREEN.
