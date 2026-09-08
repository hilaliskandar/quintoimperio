# F5-doc — 1505 — matriz institucional v0.1

Data: 2026-09-08
Issue: #132
Baseline: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Objetivo

Identificar quais mudanças de 1505 precisam persistir no estado mundial até `31/12/1505`, distinguindo autoridade vice-real, fortificação, guarnição, feitoria, centralidade administrativa e soberania.

## 1. Princípio de modelagem

F5 não deve usar “Estado da Índia” como sinônimo de soberania territorial portuguesa sobre portos aliados.

A documentação de 1505 indica uma estrutura de comando português mais permanente e unificada, mas os portos de Cochim e Cananor continuam inseridos em soberanias locais. Portanto, a futura normalização deve manter separadas:

- autoridade institucional portuguesa no Oriente;
- autoridade/soberania política local do nó;
- feitoria;
- fortificação;
- guarnição;
- acesso/relação diplomática;
- sede ou centralidade administrativa.

## 2. Quiloa — mudança física e política persistente

O relato contemporâneo associado a Hans Mayr é especialmente forte para Quiloa.

Em `22/07/1505`, a armada entra no porto. Em `24/07`, ocorre o desembarque/ocupação. O relato registra em seguida:

- substituição do soberano local;
- adaptação/construção de uma fortificação portuguesa usando uma das melhores casas;
- instalação de artilharia;
- permanência de Pêro Ferreira no comando de força residente.

### Classificação

| Dimensão | Estado anterior | Mudança em 1505 | Persistência provável em 31/12/1505 |
|---|---|---|---|
| soberania/política local | sultanato/cidade-Estado suaíli | intervenção portuguesa na sucessão | sim, mas não equivale automaticamente a `PORTUGUESE_SOVEREIGNTY` |
| feitoria/presença | relação comercial/diplomática | presença residente reforçada | sim |
| fortificação | não portuguesa | fortificação portuguesa criada | sim |
| guarnição | nenhuma portuguesa permanente | força residente deixada | sim |
| relação | negociada/tributária instável | coerção e soberano apoiado por Portugal | mudança real, mas sem classificação final nesta versão |

### Consequência provável

`KIL` é forte candidato a novos `node_state_events` em 1505 para fortificação e guarnição. A dimensão política local precisa ser tratada com cautela: apoiar/substituir soberano não significa anexação territorial.

Os números de homens e artilharia do relato não devem virar parâmetros de simulation sem necessidade funcional.

## 3. Mombaça — violência sem estado persistente demonstrado

O relato contemporâneo documenta claramente:

- chegada do núcleo de Almeida em 13/08;
- chegada do `São Rafael` em 14/08;
- bombardeio;
- incêndio/saque;
- ocupação episódica e retirada posterior.

### Decisão

Até aqui, Mombaça exige `expedition_events`, não necessariamente `node_state_events`.

Não há nesta matriz evidência suficiente de:

- fortificação portuguesa permanente em 1505;
- guarnição residente portuguesa no fim do ano;
- anexação territorial.

Portanto o ataque não deve produzir automaticamente novo estado persistente de nó.

## 4. Anjediva — fortificação candidata, cronologia ainda insuficiente

O Regimento e a tradição da viagem fazem de Anjediva um ponto estratégico para fortificação. Fontes secundárias convergem em setembro de 1505 para a chegada e construção de forte.

Entretanto, a fonte contemporânea acessível nesta rodada não alcança a Índia.

### Decisão

Anjediva é candidata a mudança persistente de:

- fortificação;
- guarnição/presença residente.

Mas a temporalidade e a duração efetiva do forte precisam de auditoria crítica antes da proposta mínima. Não normalizar `13/09` como `EXACT` apenas pela convergência de sínteses.

## 5. Cananor — fortificação persistente segura em 1505

A EVE/FCSH sustenta que:

- em outubro de 1505 a armada de Almeida se demora em Cananor;
- diante da tensão entre portugueses e Mappilas, Almeida negocia com o soberano local a construção de fortaleza para proteger a feitoria;
- a fortificação começa a ser erguida ainda em 1505;
- o conjunto fortificado de Santo Ângelo torna-se núcleo duradouro da presença portuguesa.

### Estado herdado de F1/F2

Antes de 1505, `CAN` já possui:

- soberania local de Kolathunad/Kolathiri;
- feitoria portuguesa desde 1501;
- presença reorganizada em 1502;
- **sem fortificação portuguesa retroativa**.

### Mudança de 1505

| Dimensão | Mudança |
|---|---|
| soberania | permanece local |
| feitoria | permanece |
| fortificação | `PORTUGUESE_FORT` passa a existir em 1505 |
| guarnição | provavelmente residente; comando e número precisam de fonte auditada |
| acesso/relação | negociado, sob tensão; não converter automaticamente em hostilidade total |

### Consequência provável

Cananor requer ao menos um novo `node_state_event` de fortificação em 1505. A janela segura na fonte EVE é `outubro de 1505`; datas diárias 23–24/10 permanecem candidatas até fechamento crítico.

Guarnição deve ser normalizada separadamente somente quando a evidência temporal/comando estiver fechada.

## 6. Cochim — centralidade administrativa sem mudança de soberania

A EVE registra que, com a chegada do primeiro vice-rei Francisco de Almeida em 1505, Cochim assume papel central na administração da presença portuguesa no Oriente.

Esse desenvolvimento ocorre sobre um estado já existente:

- soberania local;
- feitoria restaurada;
- Forte Manuel;
- guarnição portuguesa;
- relação favorável;
- acesso negociado.

### O que muda

A principal mudança é institucional em escala supra-local: Cochim passa a servir como residência/base central da autoridade portuguesa de Almeida.

### O que NÃO muda

- soberania de Cochim não se torna portuguesa;
- Forte Manuel não começa em 1505; já existe desde 1503;
- guarnição não começa em 1505; já existe desde 1503.

### Questão arquitetural

Há duas opções mínimas:

**A. Evento institucional ligado a Almeida**

Registrar a chegada/assunção e a escolha de Cochim como base administrativa como `expedition_event` ou evento institucional, sem adicionar dimensão permanente nova ao estado do nó.

**B. Novo estado institucional temporal**

Criar algo como `ADMINISTRATIVE_SEAT` apenas se algum comportamento funcional de F5/freeze precisar consultar “onde está a sede portuguesa” independentemente da expedição ativa.

### Decisão v0.1

Preferir **A**. Não criar novo campo/schema de `ADMINISTRATIVE_SEAT` sem caso funcional demonstrado.

## 7. Autoridade vice-real — estado global ou evento?

A carta de 27/02/1505, o Regimento de 03/03 e a posterior atuação de Almeida mostram uma autoridade que ultrapassa um único porto.

Entretanto, o domínio até F4 já consegue representar:

- líder/autoridade da expedição;
- eventos institucionais por data;
- estados locais de nó;
- efeitos persistentes de fortificação/guarnição.

### Teste de necessidade

Um novo `global_authority_state` só seria necessário se F5 precisasse responder, independentemente da expedição ativa:

- quem possui competência portuguesa sobre múltiplos nós em determinada data;
- qual autoridade deve resolver ações institucionais após a passagem da armada;
- transição Almeida→Albuquerque como contrato persistente do freeze.

### Decisão v0.1

`NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_DEMONSTRADO`

Proposta preferida: representar nomeação/assunção de Almeida como eventos institucionais e manter a autoridade nominal na expedição/documentação. Reavaliar apenas no closeout se golden states de `31/12/1505` exigirem consulta global.

## 8. Pêro de Anhaia / Sofala

A armada de Pêro de Anhaia parte separadamente em 18/05/1505 e está associada ao estabelecimento fortificado em Sofala.

A relevância é estrutural porque Sofala já existe como nó `SOF`.

### Candidato F5

Se a fortificação/guarnição de Sofala estiver estabelecida até `31/12/1505`, o freeze precisa refletir essa mudança temporal, ainda que `EXP_ANHAIA_1505` permaneça sem pernas jogáveis.

### Próximo passo

Abrir auditoria específica da cronologia Anhaia/Sofala antes de decidir normalização.

## 9. Matriz consolidada — candidatos ao estado de 31/12/1505

| Nó | Fortificação portuguesa | Guarnição portuguesa | Nova presença institucional | Soberania portuguesa? | Situação documental |
|---|---|---|---|---|---|
| `KIL` | forte candidata/forte | forte candidata/forte | sim | **não presumir** | cronologia contemporânea forte |
| `MOM` | não demonstrada | não demonstrada | episódica | não | evento militar específico |
| `ANJ` | provável | provável | provável | não demonstrada | cronologia crítica pendente |
| `CAN` | **sim, em 1505** | provável, auditar | feitoria já anterior | não | mês seguro: outubro |
| `COC` | já existe desde 1503 | já existe desde 1503 | centralidade administrativa nova | não | mudança supra-local, sem schema novo por ora |
| `SOF` | provável via Anhaia | provável | sim | não presumir | auditoria separada necessária |

## 10. T4 — combate após matriz institucional

Nada nesta matriz demonstra necessidade de combate funcional mínimo.

Mesmo Quiloa e Mombaça podem ser representadas como:

- eventos de expedição;
- transições institucionais/fortificação/guarnição quando persistentes.

A decisão permanece:

`COMBATE_FUNCIONAL_MINIMO = AINDA_NAO_DEMONSTRADO`

## 11. Próximos subgates bloqueantes

1. cronologia e fortificação de Anjediva;
2. cronologia detalhada de Cananor, especialmente fortificação/guarnição;
3. chegada e assunção institucional de Almeida em Cochim;
4. Pêro de Anhaia e Sofala;
5. sucessão nominal da guarda de Cochim no limiar 1504–1505;
6. somente depois: proposta mínima de normalização e decisão final T4.
