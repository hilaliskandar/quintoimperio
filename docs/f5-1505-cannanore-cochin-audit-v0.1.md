# F5-doc — 1505 — auditoria Cananor e Cochim v0.1

Data: 2026-09-08
Issue: #132
Baseline: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Objetivo

Fechar as mudanças institucionais mínimas em Cananor e Cochim no último trimestre de 1505, distinguindo fortificação, guarnição, autoridade vice-real, centralidade administrativa e soberania local.

## 1. Cananor — fortificação

### Evidência convergente

A EVE/FCSH estabelece com segurança que:

- em outubro de 1505 a armada de Francisco de Almeida se demora em Cananor;
- diante da tensão entre portugueses e Mappilas, Almeida negocia com o soberano local a construção de fortaleza para defender a feitoria;
- a fortificação começa a ser erguida ainda em 1505;
- o Forte de Santo Ângelo torna-se núcleo duradouro da presença portuguesa.

Estudo crítico da cronologia das primeiras fortalezas portuguesas, apoiado explicitamente em Damião de Góis, fixa:

`23/10/1505` — início da construção da fortaleza de Cananor.

A mesma data aparece em reconstrução narrativa moderna baseada na crônica manuelina.

### Decisão documental

A proposta mínima pode tratar `23/10/1505` como candidato forte a `EXACT`, desde que a proveniência seja explicitamente ligada à cronologia de Góis/estudo crítico e não apenas a síntese enciclopédica.

Se a implementação preferir maior conservadorismo, uma janela `23–31/10/1505` também é defensável. Entretanto, a evidência atualmente reunida já é superior ao simples nível mensal.

## 2. Cananor — guarnição e comando

Reconstruções cronísticas associam a fortaleza recém-construída a:

- Lourenço de Brito como capitão;
- guarnição portuguesa residente;
- embarcações de apoio.

A EVE confirma a fortaleza e sua função defensiva, mas a entrada consultada não fixa nominalmente o primeiro capitão nem números de homens.

### Decisão

F5 deve normalizar **a existência da guarnição**, não seu tamanho.

O nome do comandante pode permanecer em notas/documentação se não houver comportamento funcional que consulte capitão local.

Não criar campo `garrison_size`.

## 3. Estado de Cananor antes e depois de outubro

### Antes de 23/10/1505

- soberania local: Kolathunad/Kolathiri;
- feitoria portuguesa: existente desde 1501;
- presença institucional: existente/reorganizada;
- fortificação portuguesa: não;
- guarnição fortificada: não.

### Depois da fortificação

- soberania local: **permanece**;
- feitoria: permanece;
- fortificação portuguesa: sim;
- guarnição portuguesa: sim;
- acesso: continua negociado;
- relação: tensionada, mas não deve ser convertida automaticamente em `HOSTILE` sem evento específico.

### Consequência

Cananor requer, na futura implementação, novos estados temporais de fortificação e guarnição. O schema `node_state_events` existente parece suficiente.

## 4. Cochim — chegada e presença de Almeida

A literatura secundária converge em chegada de Almeida a Cochim no fim de outubro, frequentemente em `31/10/1505`.

Nesta auditoria ainda não foi localizado testemunho contemporâneo direto da chegada nesse dia.

Entretanto, há evidência documental forte de presença posterior: Francisco de Almeida escreveu de Cochim a D. Manuel em `16/12/1505`, carta citada em edição/documentação especializada.

### Classificação

- `31/10/1505`: `CANDIDATE_EXACT`, forte em tradição cronística/secundária, ainda sem testemunho contemporâneo diretamente auditado;
- `16/12/1505`: `EXACT` para presença documentada de Almeida em Cochim.

A proposta mínima não precisa transformar 31/10 em observação de viagem se o loop não exigir chegada diária.

## 5. Cochim — centralidade administrativa

A EVE registra que, com a chegada do primeiro vice-rei em 1505, Cochim assume papel central na administração portuguesa no Oriente.

### Estado herdado

Antes de Almeida, Cochim já possui:

- soberania local;
- feitoria portuguesa;
- Forte Manuel;
- guarnição portuguesa;
- relação favorável;
- acesso negociado.

### Mudança de 1505

A mudança é de **escala institucional portuguesa**, não de soberania do nó.

Almeida passa a usar Cochim como base/residência principal da autoridade portuguesa no Oriente durante esse estágio.

### Decisão de schema

Não criar `ADMINISTRATIVE_SEAT` em `node_state_events` na primeira implementação.

Preferir:

- evento institucional da expedição/autoridade de Almeida;
- estado local herdado intacto.

Somente criar dimensão global/sede se golden tests do freeze precisarem consultar a sede independentemente da expedição.

## 6. Autoridade vice-real — quando considerar ativa

A documentação já distingue:

- 27/02 — nomeação/poder como capitão-mor e missão por três anos;
- 03/03 — Regimento/programa;
- 25/03 — partida;
- outubro — presença em Cananor e início da fortificação;
- até 16/12 — presença documental em Cochim.

A tradição cronística associa a adoção pública do título vice-real à fase de Cananor, mas as condições exatas variam entre versões.

### Decisão

A primeira proposta funcional pode usar um evento:

`VICEROYAL_AUTHORITY_ACTIVE_IN_INDIA`

com janela conservadora em outubro de 1505, se necessário para marcar a passagem de comando expedicionário a autoridade residente.

Mas esse evento **não deve criar novo schema global** enquanto nenhum comportamento funcional depender dele.

## 7. Divergência nominal herdada de F4

A divergência `Manuel Teles de Vasconcelos × Manuel Teles Barreto` permanece relevante para a guarda de Cochim no limiar 1504–1505.

F5 não precisa resolvê-la para modelar:

- fortificação de Cananor;
- autoridade de Almeida;
- centralidade de Cochim.

Se a proposta de freeze não consultar nominalmente o comandante local, preservar a divergência sem campo novo é metodologicamente preferível.

## 8. Matriz de normalização candidata

| Evento/estado | Data/janela | Precisão proposta | Schema provável |
|---|---|---|---|
| fortificação de Cananor | 23/10/1505 | `EXACT` candidato forte | `node_state_events` |
| guarnição de Cananor | outubro de 1505 | `RANGE`/mesmo gate da fortificação | `node_state_events` |
| autoridade vice-real ativa no Índico | outubro de 1505 | `RANGE` | `expedition_events` / evento institucional |
| presença de Almeida em Cochim | até 16/12/1505 | `EXACT` para presença nessa data | documentação/evento |
| centralidade administrativa de Cochim | fim de 1505 | sem dia obrigatório | evento institucional; sem novo schema por ora |

## 9. Consequência T4

Cananor e Cochim reforçam a conclusão de que F5 é, até aqui, predominantemente um problema de **estado institucional temporal**, não de resolução de combate.

`COMBATE_FUNCIONAL_MINIMO = AINDA_NAO_DEMONSTRADO`

## 10. Próximo passo

Com Quiloa, Sofala, Cananor e Cochim suficientemente caracterizados, o próximo documento deve consolidar a **proposta mínima de normalização F5**, deixando apenas Anjediva com janela temporal mais fraca e decidindo explicitamente quais estados entram no baseline `31/12/1505`.
