# F5-doc — 1505 — auditoria de autoridade e composição da armada v0.1

Data: 2026-09-08
Issue: #132

## Objetivo

Separar três problemas frequentemente comprimidos em uma única formulação — nomeação de Francisco de Almeida, exercício do título vice-real e composição da armada — para impedir que o domínio transforme divergências documentais em fatos artificiais.

## 1. Nomeação e autoridade

### 27/02/1505 — carta de nomeação/poder

Sanjay Subrahmanyam remete à documentação da Torre do Tombo (`Gavetas XIV/3-14`, publicada por Silva Rego) para a carta de 27/02/1505 que nomeia D. Francisco de Almeida “capitão-mor” da frota/armada e determina que permaneça na Índia por três anos.

Essa é a âncora jurídica mais segura desta versão para a nomeação pessoal e duração prevista da missão.

### 03/03/1505 — Regimento

O Regimento de D. Manuel a Almeida, datado de 03/03/1505 na edição/documentação utilizada pela historiografia, define programa de ação: alianças, diplomacia, fortificações, coerção e organização permanente da presença portuguesa.

Estudo recente sobre império e consentimento interpreta 1505 como momento em que a Coroa cria uma estrutura permanente na Ásia sob comando unificado, embora a materialização dessa autoridade dependa da chegada ao Índico.

### Título de vice-rei

A documentação e a tradição cronística não autorizam a frase simplificada “vice-rei efetivo desde Lisboa” como único estado temporal.

Subrahmanyam distingue a nomeação como capitão-mor e as ordens para assumir o título vice-real no Oriente. A tradição cronística associa a adoção pública do título à fase de Cananor, mas as versões divergem sobre as condições exatas e sobre a relação com as fortalezas previstas.

### Decisão de normalização futura

Separar pelo menos conceitualmente:

1. `ROYAL_APPOINTMENT` — 27/02/1505, autoridade concedida pela Coroa;
2. `EXPEDITION_COMMAND` — comando da armada desde a partida;
3. `VICEROYAL_AUTHORITY_ACTIVE_IN_INDIA` — somente depois de chegada/assunção no Oriente, com data a fechar.

Nenhum destes eventos altera soberania dos reinos locais.

Não criar ainda schema global. Primeiro verificar se `expedition_events` + um eventual evento institucional datado são suficientes para todos os efeitos funcionais de 1505.

## 2. Partida da armada

A EVE/FCSH registra `25/03/1505` para D. Francisco de Almeida e os demais capitães da mesma armada. O marco é suficientemente estável para a cronologia documental.

A carta de nomeação de 27/02 não deve ser confundida com partida.

## 3. Número de navios — divergência preservada

A literatura não fornece um único total consensual.

### Relato contemporâneo associado a Hans Mayr / Manuscrito Valentim Fernandes

A tradição textual reproduz:

- 20 velas;
- 14 naus;
- 6 caravelas.

Esse testemunho é particularmente importante por ser contemporâneo da viagem.

### EVE/FCSH

A listagem de 25/03/1505 apresenta 21 nomes de capitães/comandos contando Francisco de Almeida.

A lista nominal não é automaticamente equivalente a 21 cascos independentes sem auditoria de função, substituições e embarcações auxiliares.

### Tradição cronística e estudos

- Castanheda: 20 navios para Almeida, além da força de Pêro de Anhaia;
- Gaspar Correia: 20;
- Barros: 22;
- Damião de Góis: 22;
- Livro das Armadas: 23 na reconstrução citada por estudos críticos;
- estudos modernos variam entre 20 e 21 como total de trabalho, enquanto algumas sínteses mantêm 22.

### Decisão

`fleet_size = UNRESOLVED`

A futura linha de `EXP_ALMEIDA_1505` não deve introduzir um campo quantitativo novo apenas para escolher uma dessas versões.

Se o tamanho da frota vier a afetar uma mecânica funcional, abrir auditoria específica de composição naval antes de parametrizar.

## 4. Armada de Pêro de Anhaia

A EVE registra separadamente:

`18/05/1505 — Pêro de Anhaia (capitão-mor)`

com outros cinco capitães na mesma data.

Essa força não deve ser comprimida na expedição de Almeida. Sua missão ligada a Sofala produz efeitos institucionais próprios na África Oriental.

### Decisão

F5 deve tratar `EXP_ANHAIA_1505` como candidata a unidade histórica separada, provavelmente sem pernas executáveis na primeira implementação, salvo se o estado de Sofala em 31/12/1505 for indispensável ao freeze.

## 5. Consequência arquitetural

Nenhuma das divergências deste documento exige novo motor de frota.

O schema atual de `expeditions.csv` permite:

- identidade da expedição;
- líder;
- período;
- tipo;
- notas de composição/financiamento;
- proveniência;
- ausência de pernas quando itinerário não estiver normalizado.

A autoridade vice-real é a lacuna potencialmente estrutural, mas somente deve gerar novo contrato de estado se os gates de Cananor/Cochim demonstrarem necessidade de consulta persistente fora da própria expedição.

## 6. Próximo subgate

Fechar cronologia operacional no Índico:

- Quiloa;
- Mombaça;
- Anjediva;
- Cananor;
- Cochim.

Em paralelo, auditar quando a fortificação de Cananor se torna efetiva e qual estado administrativo de Cochim realmente precisa persistir no domínio.
