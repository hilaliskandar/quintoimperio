# Godot G0 — fechamento arquitetural e paridade inicial

Data: 2026-09-08
Issue: #138
Baseline Python congelado: `f4fd140677b7fda49a6f97456fa0b9e6ff83a735`
HEAD G0 auditado: `0c20153dbc294780b17684092135f1fb48dc4fac`

## Resultado

O gate G0 atingiu seu objetivo: existe um projeto Godot mínimo inicializável, o engine está fixado, os dados canônicos são lidos sem duplicação factual e dois contratos do domain freeze 1505 já possuem paridade executável em CI headless.

Nenhuma expansão histórica, novo sistema de combate, governo global, múltiplas frotas ativas ou alteração em `data/`/`simulation/` foi introduzida.

## Runtime fixado

Godot `4.7.2-stable`.

Artefato CI Linux x86_64:

`Godot_v4.7.2-stable_linux.x86_64.zip`

SHA-256:

`cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`

A política de atualização está em `docs/adr/0002-godot-version-policy.md`.

## Shell criado

O diretório `godot/` contém:

- `project.godot` e cena mínima `scenes/bootstrap.tscn`;
- `autoload/canonical_data.gd`, leitor CSV read-only da raiz do repositório;
- `domain/node_state.gd`, primeira projeção temporal portada;
- `domain/expedition_event.gd`, contrato documental de eventos portado;
- `parity/parity_cli.gd`, harness headless;
- fixtures JSON de NodeState e da sequência institucional de Almeida.

O workflow `.github/workflows/godot-parity.yml` baixa o binário oficial, verifica SHA-256, importa o projeto headless e executa o harness. A regressão Python continua independente.

## Paridade 1 — NodeStateEventModel

Commit: `75e2f3093d13bb2f277869fb701ae2c99cce3cf3`.

CI Godot: `34201735220` — verde.

O golden state de `31/12/1505` coincide com a referência Python para:

- `ANJ`;
- `CAN`;
- `COC`;
- `KIL`;
- `MOM`;
- `SOF`.

Também foram testados os limites conservadores dos eventos `RANGE`:

- `ANJ1505_E01` não se aplica em 29/09 e se aplica em 30/09;
- `CAN1505_E01` não se aplica em 30/10 e se aplica em 31/10.

Saída sentinela:

`NODE_STATE_PARITY={... "status":"ok"}`.

## Paridade 2 — ExpeditionEventModel

Commit: `64ffac12b1247712de397a6d1bc9053caed48045`.

CI Godot: `34201957764` — verde.

`EXP_ALMEIDA_1505` foi reproduzida com ordenação:

`ALM1505_E01 → E02 → E03 → E04 → E05`.

Foram validados checkpoints de disponibilidade em:

- 26/02;
- 27/02;
- 03/03;
- 25/03;
- 30/10;
- 31/10;
- 15/12;
- 16/12 de 1505.

O evento `ALM1505_E04` só se torna seguramente disponível no limite superior de outubro; a presença documental em Cochim entra em 16/12.

Saída sentinela:

`EXPEDITION_EVENT_PARITY={... "status":"ok"}`.

## Dados canônicos

O primeiro smoke em Godot, commit `e42c0ffe65232a1e520f8934c2852d49d48ae373`, CI `34201530974`, comprovou:

- abertura do projeto em Godot 4.7.2 headless;
- leitura direta de `data/node_state_events.csv`;
- 15 linhas de eventos;
- 5 eventos identificados no horizonte 1505;
- resolução correta da raiz do repositório.

Não existe cópia manual dos CSVs em `.tres`, cena ou script.

## ADRs fechados

Commit: `0c20153dbc294780b17684092135f1fb48dc4fac`.

- ADR 0002 — versão fixa do Godot e política de atualização;
- ADR 0003 — dados canônicos e recursos derivados;
- ADR 0004 — determinismo intra-engine e `decision tape` para paridade estocástica;
- ADR 0005 — persistência Godot por compatibilidade semântica, sem duplicar estado histórico objetivo;
- ADR 0006 — harness de paridade headless e regra para diferenças entre engines.

A estratégia de aleatoriedade não promete identidade bit a bit entre PRNGs nativos. Casos estocásticos de paridade deverão reproduzir uma fita explícita de decisões extraída da referência Python; seeds continuam determinísticas dentro de cada runtime/versionamento.

## Regressão Python

A introdução do shell Godot e das primeiras portas de domínio não alterou a referência Python. A CI Python continuou integralmente verde, inclusive após a paridade temporal (`34201735216`) e após os ADRs (`34202159730`).

## Auditoria do diff

Comparação `f4fd140677b7fda49a6f97456fa0b9e6ff83a735...0c20153dbc294780b17684092135f1fb48dc4fac`:

- 5 commits à frente;
- 0 commits atrás;
- alterações somente em novo workflow Godot, documentação e diretório `godot/`;
- nenhum arquivo em `src/quintoimperio/domain/`, `data/` ou `simulation/` alterado.

## Critérios de saída G0

1. versão do engine fixada e documentada — **SATISFEITO**;
2. projeto mínimo abre em CI headless — **SATISFEITO**;
3. dados canônicos consumidos sem cópia factual manual — **SATISFEITO**;
4. golden state de 31/12/1505 passa em paridade — **SATISFEITO**;
5. contrato de `ExpeditionEvent` passa em paridade — **SATISFEITO**;
6. determinismo e persistência registrados em ADR — **SATISFEITO**;
7. CI Python permanece verde — **SATISFEITO**;
8. nenhum desvio de domínio não classificado — **SATISFEITO**.

## Próximo gate recomendado

Abrir G1 como migração do **estado mínimo de sessão e calendário**, ainda sem UI de produção. O objetivo deve ser reproduzir um fluxo determinístico pequeno do MVP, acrescentando `DomainClock`/`SessionState` e persistência mínima sob o contrato dos ADRs antes de iniciar telas, mapa ou animação.
