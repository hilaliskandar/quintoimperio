# P3.4-doc — auditoria de schema para fortificação e guarnição v0.1

Data: 2026-09-07
Issue: #114

## Pergunta

O schema atual consegue representar a transformação de Cochim em 1503 sem reescrever retrospectivamente o estado de 1500–1502 e sem criar desde já um sistema territorial geral?

## Estado atual

### `nodes.csv`

O arquivo possui campos estáticos como:

- `political_status`;
- `royal_presence`;
- `fortification`;
- `access_regime`;
- `active_from`.

Esses campos descrevem bem um baseline de nó, mas não têm dimensão temporal suficiente para um mesmo nó mudar repetidamente de estado ao longo da campanha.

Para `COC`, o registro atual documenta corretamente o período inicial: porto do Perumpadappu Swarupam, acesso estrangeiro negociado, sem fortificação portuguesa assumida. Alterar simplesmente `fortification` para `HIGH` ou equivalente apagaria o estado anterior a setembro de 1503.

### `actors.csv` + `node_actors.csv`

Esses arquivos já permitem:

- atores institucionais;
- associações por período;
- autoridade local;
- comunidades mercantis.

Portanto, um ator institucional como `ACT_COC_PORTUGUESE_GARRISON_1503` ou uma associação militar equivalente pode ser representado documentalmente sem biografar todos os soldados. Ainda assim, a presença do ator não basta para expressar construção/ativação temporal da fortificação.

### `expeditions.csv` + `expedition_routes.csv`

Conseguem representar as armadas separadas de Afonso de Albuquerque, Francisco de Albuquerque e António de Saldanha, bem como uma futura subcampanha de força residente. Não são o lugar adequado para persistir o estado territorial de Cochim depois que a expedição termina.

### `expedition_epilogue_events.csv`

Fornece precedente metodológico importante: quando um fato histórico relevante não cabe no loop operacional existente, o projeto prefere criar uma camada documental estreita e não generalizar prematuramente o domínio. Contudo, esse arquivo é semanticamente específico do epílogo da primeira viagem e não deve ser reutilizado como tabela universal de estados territoriais.

## Lacuna real

A lacuna mínima é **estado temporal de nó/instituição**.

O ciclo 1503 exige registrar, por exemplo:

1. `COC` — feitoria portuguesa ativa antes de abril de 1503;
2. abril de 1503 — ofensiva/ocupação por forças de Calecute e retirada do aliado para Vaipim;
3. setembro de 1503 — restauração do rajá;
4. setembro de 1503 em diante — fortificação portuguesa em construção/ativa;
5. fim de 1503 em diante — força/guarnição portuguesa residente.

Nenhuma dessas transições altera a identidade geográfica de `COC` nem transfere soberania para Portugal.

## Opções avaliadas

### A. Sobrescrever `nodes.csv`

**Rejeitada.**

Perde a temporalidade e introduz anacronismo em campanhas anteriores.

### B. Criar versões duplicadas de Cochim por período

Ex.: `COC_1500`, `COC_1503`.

**Rejeitada.**

Fragmentaria artificialmente a identidade do mesmo porto e complicaria rotas, mercado e atores.

### C. Codificar tudo como atores

**Insuficiente.**

Uma guarnição pode ser ator, mas a fortificação é estado/infraestrutura e a ocupação/restauração é evento político-territorial.

### D. Criar camada histórica temporal mínima de estados/eventos de nó

**Preferida para futura implementação.**

Uma tabela estreita como `node_state_events.csv` ou `historical_node_events.csv` pode registrar transições sem tornar o domínio imediatamente genérico.

Campos candidatos:

- `event_id`;
- `node_id`;
- `event_date` ou `period_from`/`period_to`;
- `event_type`;
- `state_dimension`;
- `state_before`;
- `state_after`;
- `actor_id` opcional;
- `evidence_grade`;
- `evidence_scope`;
- `source_id`;
- `notes`.

Tipos inicialmente necessários poderiam ser limitados a:

- `POLITICAL_CONTROL_CRISIS`;
- `LOCAL_AUTHORITY_RESTORED`;
- `FORTIFICATION_ESTABLISHED`;
- `GARRISON_ESTABLISHED`.

Esses nomes são propostas de schema, não fatos históricos.

## Vaipim

Não há necessidade demonstrada de criar `VAI` como nó comercial ou de navegação. Para o ciclo 1503, Vaipim pode ser registrado primeiro como localização associada a um evento de retirada/refúgio. Um nó separado só deve ser criado se a campanha futura exigir deslocamento navegável, decisão logística ou interação própria ali.

## Guarnição

A guarnição pode ser representada em duas camadas:

1. **histórica**: ator institucional agregado associado a Cochim a partir de 1503;
2. **funcional**: somente se o loop precisar consultar presença militar como condição de ação.

Não é necessário criar controle individual de soldados, folha de pagamento ou capacidade de combate neste gate.

## Fortaleza

A fortificação deve ser um estado temporal do nó e não redefinir `node_type`. `COC` continua sendo porto estrangeiro sob autoridade local, ainda que passe a conter instalação militar portuguesa.

## Soberania

A auditoria documental não sustenta converter Cochim em `PORTUGUESE_POSSESSION` em 1503. O schema futuro deve permitir combinar:

- autoridade/soberania local;
- instalação portuguesa fortificada;
- guarnição portuguesa residente;
- aliança/relação política.

Essas dimensões devem permanecer independentes.

## Combate

Mesmo após 1503, o schema documental não exige ainda sistema geral de combate. Eventos militares podem alterar estados por dados históricos em campanhas guiadas. Um sistema de combate só deve ser aberto se o futuro P3-func demonstrar necessidade de agência contrafactual ou resolução variável desses confrontos.

## Decisão

Existe uma lacuna real de schema, mas ela é estreita: **eventos/estados temporais de nó**. Não há justificativa para refatoração territorial geral, múltiplas versões de nós ou sistema de combate neste momento.

A futura implementação deve começar por tabela documental mínima, não por comportamento complexo.