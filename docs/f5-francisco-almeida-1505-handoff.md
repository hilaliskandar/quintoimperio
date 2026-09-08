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

## Primeiro incremento recomendado

Implementar em sequência estreita, com CI a cada gate:

1. registrar `EXP_ALMEIDA_1505` no catálogo histórico sem depender de `fleet_size` e sem tornar automaticamente toda a rota jogável;
2. adicionar testes que provem existência no catálogo sem ativação acidental e preservação dos baselines anteriores;
3. materializar somente estados persistentes de 1505 com evidência suficiente, começando por Sofala e Cananor;
4. tratar Quiloa e Anjediva em gates próprios, separando evento de tomada/construção do estado persistente final;
5. representar a centralidade administrativa de Cochim como evento institucional sem alterar soberania;
6. fechar teste de estado em `1505-12-31` e save/load;
7. executar regressão integral; somente depois avaliar necessidade de campanha jogável adicional.

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
