# F1 — João da Nova 1501–1502 — auditoria cronológica v0.1

Data: 2026-09-07
Issue: #120
Gate-mãe: #118

## Objetivo

Classificar o grau de precisão cronológica disponível para a integração funcional de `EXP_JOAO_NOVA_1501`, impedindo que o modo `GUIDED` transforme sequência histórica ou meses aproximados em datas diárias inventadas.

## Fontes de partida

Corpus já normalizado:

- `docs/p3-2-joao-da-nova-evidence-v0.1.md`;
- `docs/p3-2-information-acquisition-v0.1.md`;
- `docs/p3-2-cannanore-institution-v0.1.md`;
- `docs/p3-2-joao-da-nova-minimal-normalization-proposal.md`;
- `data/expeditions.csv`;
- `data/expedition_events.csv`.

Verificação dirigida complementar:

- Revista Portuguesa de História Militar / Comissão Portuguesa de História Militar — confirma partida em março de 1501, escala de São Brás para aguada e aviso, sequência posterior Quiloa → Melinde → Anjediva → Cananor → Cochim, e Cananor em 30/12/1501 antes da torna-viagem;
- EVE/FCSH — confirma estabelecimento da feitoria de Cananor ao final de 1501;
- Sanjay Subrahmanyam — situa a costa oriental africana em agosto e a chegada à costa indiana/Cananor em novembro, sem oferecer cronologia diária suficiente para todas as pernas.

Reconstruções secundárias que fornecem dias exatos não são promovidas automaticamente a observações `EXACT` quando a base primária/especializada usada pelo projeto não explicita esses dias.

## Classificação

Classes usadas neste gate:

- `EXACT`: data diária diretamente sustentada pelo corpus preferido;
- `INTERVAL`: mês ou janela suficientemente sustentados, sem dia seguro;
- `DERIVED`: data operacional calculada a partir de duração/intervalo explicitamente documentado, sempre marcada como derivação;
- `UNRESOLVED`: sequência conhecida, mas sem data/duração suficiente para cronologia guiada diária.

## Matriz cronológica

| Marco/perna | Evidência disponível | Classe F1 | Decisão funcional |
|---|---|---|---|
| partida de Lisboa | 05/03/1501 pela EVE/listagem já adotada | `EXACT` | preservar como estado inicial documental |
| `LIS → SBR` | São Brás ocorre depois da partida; evento de aviso já normalizado em janela 01/05–31/08; reconstruções secundárias sugerem julho | `INTERVAL` | não criar observação diária; chegada exata permanece não resolvida |
| aviso em São Brás | fato e local firmes; data diária não suficientemente firme | `INTERVAL` | manter `NOVA1501_E01`; aquisição elegível apenas na janela documentada |
| `SBR → KIL` | sequência confirmada pela fonte oficial; cronologia diária ausente | `UNRESOLVED` | rota pode ser normalizada, mas sem `voyage_observation` diária |
| `KIL → MAL` | sequência confirmada; costa oriental africana situada em agosto em síntese especializada | `INTERVAL` | não inventar dia de saída/chegada |
| `MAL → ANJ` | sequência confirmada; chegada à costa indiana/Anjediva situada em novembro em tradição cronística/sínteses | `INTERVAL` | mês pode ser usado como contexto, não como timing diário |
| `ANJ → CAN` | Cananor é escala anterior a Cochim; chegada ao Malabar em novembro é defensável em nível mensal | `INTERVAL` | sem observação diária |
| `CAN → COC` | sequência e função comercial firmes | `UNRESOLVED` | normalizar conexão de campanha sem timing diário inventado |
| `COC → CAN` | retorno a Cananor antes da torna-viagem é firme | `UNRESOLVED` | normalizar sequência; duração permanece aberta |
| Cananor pronto para retorno | 30/12/1501 pela fonte oficial portuguesa | `EXACT` | usar como marco cronológico firme de fim da fase comercial |
| bloqueio/confronto | esquadra de Calecute surge em 30/12; combate subsequente atravessa a virada para 1502 | `EXACT` para início / `INTERVAL` para resolução | evento específico; não criar combate geral neste gate |
| torna-viagem / Lisboa | retorno em 1502 é firme; data diária final permanece divergente/menos segura | `INTERVAL` | não fechar `GUIDED` diário até Lisboa nesta tranche sem nova evidência |

## Consequência arquitetural

A ausência de datas diárias não justifica preencher `voyage_observations.csv` com estimativas apresentadas como história. F1 deve separar:

1. **ordem histórica das pernas** — pode ser registrada em `expedition_routes.csv`;
2. **timing observado** — somente entra em `voyage_observations.csv` quando houver data/duração defensável;
3. **timing de simulação** — pode continuar sendo calculado pelo motor a partir da rota, mas deve ser identificado como simulação e não como observação histórica;
4. **marcos firmes** — 05/03/1501 e 30/12/1501 devem permanecer testes sentinela do recorte.

Isso permite tornar João da Nova funcional sem degradar a disciplina de evidência.

## Primeira tranche programável

O próximo incremento deve ser pequeno:

1. normalizar a ordem `LIS → SBR → KIL → MAL → ANJ → CAN → COC → CAN` em `expedition_routes.csv`, reutilizando rotas existentes quando semanticamente válidas e criando somente conexões indispensáveis;
2. não adicionar observações diárias onde a matriz acima é `INTERVAL` ou `UNRESOLVED`;
3. testar que o aviso de São Brás não existe na partida e só pode ser adquirido em `SBR` dentro da janela;
4. testar que a rota histórica evita `CAL` depois do aviso;
5. aplicar a presença institucional de Cananor somente no fim de 1501, sem fortificação ou soberania retroativas;
6. manter o bloqueio de 30/12 como evento específico.

## Gate para nova pesquisa

Nova pesquisa documental só volta a bloquear implementação se o motor atual não conseguir representar uma perna ordenada sem observação diária ou se uma decisão jogável depender de um dia exato ainda desconhecido. Nesse caso, a lacuna deve ser aberta como questão estreita; não se deve ampliar novamente a pesquisa de toda a viagem.