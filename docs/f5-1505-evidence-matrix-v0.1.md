# F5-doc — Francisco de Almeida 1505 — matriz de evidências v0.1

Data: 2026-09-08
Issue: #132
Baseline: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Objetivo

Inventariar as mudanças de 1505 que podem afetar o fechamento `Python 1505 GREEN`, distinguindo armada, autoridade institucional, fortificações/guarnições, itinerário e eventos militares sem antecipar implementação.

Esta versão é deliberadamente diagnóstica. Divergências de número de navios, datas finas e titulatura não são harmonizadas por conveniência.

## 1. Estado herdado de F4

Em `31/12/1504`, o domínio já deve resolver:

- Cochim sob soberania local;
- feitoria portuguesa restaurada;
- Forte Manuel;
- guarnição portuguesa residente;
- acesso negociado;
- relação favorável;
- armada de Lopo Soares já fora de Cochim desde 26/12/1504;
- ausência de combate geral;
- ausência de Coulão/Cranganor/Pandarane como nós;
- divergência aberta `Manuel Teles Barreto` × `Manuel Teles de Vasconcelos` para continuidade nominal da guarda de Cochim.

F5 não deve recriar esses estados.

## 2. Fontes de trabalho iniciais

| source_id | Fonte | Uso inicial |
|---|---|---|
| `EVE_ARMADAS_MANUEL` | EVE/FCSH, “Armadas da Índia do Reinado de D. Manuel I (1495–1521)” | partida em 25/03/1505 e lista nominal dos capitães da armada de Francisco de Almeida; identifica também a partida separada de Pêro de Anhaia em 18/05/1505 |
| `REGIMENTO_ALMEIDA_1505` | Regimento de D. Manuel a D. Francisco de Almeida, 03/03/1505, publicado na documentação portuguesa e analisado pela historiografia recente | programa régio, jurisdição, diplomacia, fortificações e estrutura de comando permanente no Oriente |
| `EVE_COCHIN` | EVE/FCSH, “Cochim” | centralidade administrativa de Cochim com a chegada do primeiro vice-rei e continuidade da presença oficial portuguesa |
| `EVE_CANNANORE` | EVE/FCSH, “Cananor” | tensão local, negociação para fortificação e início da construção da fortaleza em 1505 |
| `POHLE_PEUTINGER` | Jürgen Pohle / EVE, coleção Conrad Peutinger | existência de cópia de relato sobre a viagem de Francisco de Almeida em 1505 e documentação contemporânea sobre a armada e seu financiamento |
| `VALENTIM_FINANCE_1505` | Carlos Manuel Baptista Valentim, estudo sobre o investimento financeiro na armada do primeiro vice-rei | composição/financiamento da grande armada; útil para conferir divergências no número de navios |
| `JESUS_CONSENT_2024` | estudo “Whether it pleases the locals or not: Empire and Consent in Portuguese Asia during the Sixteenth Century” | leitura do Regimento de 1505 como criação de estrutura permanente e unificada, com instruções diplomáticas e fortificações estratégicas |

## 3. Armada principal — núcleo seguro

### Partida

A listagem EVE/FCSH registra:

`25/03/1505 — D. Francisco de Almeida (capitão-mor)`

seguido de vinte outros capitães na mesma data.

A partida pode ser tratada como `EXACT` no inventário documental, mas a implementação futura deve distinguir “data da partida” de “data/forma jurídica da nomeação vice-real”.

### Composição

A EVE lista 21 comandantes/capitães na saída de 25/03, contando Francisco de Almeida. Literatura secundária varia entre 20, 21 e 22 navios, conforme critério de contagem, componentes privados e embarcações auxiliares.

**Decisão v0.1:** não fixar ainda `fleet_size` no domínio. A identidade de `EXP_ALMEIDA_1505` pode ser normalizada sem escolher um número controverso.

### Financiamento

Fontes sobre Lucas Rem/Welser registram participação de consórcio alemão-italiano em três navios da armada e investimento privado relevante.

**Relevância ao loop:** histórica, mas não demonstra necessidade de sistema financeiro novo nesta tranche. Manter como documentação enquanto o loop não consumir propriedade/financiamento de navios.

## 4. Autoridade vice-real — mudança estrutural

O Regimento de 03/03/1505 constitui a principal mudança institucional do horizonte F5.

A historiografia recente o interpreta como parte da decisão manuelina de criar uma estrutura permanente na Ásia sob comando unificado de vice-rei/governador, com jurisdição sobre forças portuguesas e programa explícito de alianças, fortificações e coerção seletiva.

### Hipótese arquitetural

1505 pode exigir uma dimensão de **autoridade global/institucional da presença portuguesa** que não se confunde com:

- soberania de um nó;
- feitoria local;
- fortificação;
- guarnição;
- `active_expedition_id`.

Antes de criar schema, deve-se verificar se a autoridade de Almeida pode permanecer:

1. metadado da expedição + eventos institucionais; ou
2. estado mundial global derivado por data.

Só criar estrutura nova se algum comportamento funcional até 31/12/1505 depender da consulta persistente a essa autoridade fora da própria expedição.

## 5. Itinerário — primeira matriz

| Marco | Estado da evidência v0.1 | Uso proposto |
|---|---|---|
| Lisboa — 25/03 | forte / EVE | `EXACT` documental |
| Quiloa — julho | forte em sínteses e estudos; data diária varia 22–24/07 conforme fonte | não fixar dia antes de auditoria fina |
| Mombaça — agosto | forte; data diária aparece 13–14/08 conforme reconstrução | preservar divergência |
| Anjediva — setembro | forte; 12–13/09 aparecem em fontes distintas | auditoria necessária antes de `EXACT` |
| Cananor — outubro | forte; EVE confirma demora em outubro e início da fortificação em 1505 | dia exato ainda não fechado pelo corpus principal |
| Cochim — fim de outubro/início de novembro | forte; fontes secundárias divergem entre 31/10 e 01/11 | prioridade para fonte contemporânea/cronologia crítica |

Nenhuma perna deve ser escrita em `expedition_routes.csv` antes da auditoria de datas e da necessidade funcional.

## 6. África Oriental

A viagem de Almeida está ligada a mudanças em Quiloa e Mombaça. A documentação secundária registra intervenção política/fortificação em Quiloa e ataque a Mombaça.

Há também uma armada separada de Pêro de Anhaia, partida em `18/05/1505`, relacionada a Sofala.

### Decisão v0.1

Não comprimir Almeida e Anhaia numa única expedição.

O gate deve decidir se as mudanças de Quiloa/Sofala precisam estar no baseline de 31/12/1505 para `Python 1505 GREEN` ou se podem permanecer eventos institucionais documentais sem loop jogável.

## 7. Cananor — fortificação nova em 1505

A EVE/FCSH registra que, em outubro de 1505, diante da tensão entre portugueses e Mappilas, Francisco de Almeida negociou com o soberano local a construção de fortaleza para proteção da feitoria. A fortificação começou a ser erguida ainda em 1505.

### Consequência provável

Este é um forte candidato a novo `node_state_event` em `CAN`, pois o estado anterior distingue:

- feitoria desde 1501;
- nenhuma fortificação portuguesa anterior.

A data fina e eventual guarnição/comando devem ser auditadas separadamente. Não usar automaticamente os números de homens/navios da literatura secundária como parâmetros.

## 8. Cochim — centralidade administrativa

A EVE registra que, com a chegada do primeiro vice-rei em 1505, Cochim passou a assumir papel central na administração portuguesa no Oriente.

Isso **não altera soberania local**.

### Questão de schema

É preciso distinguir:

- sede/residência de autoridade portuguesa;
- feitoria;
- forte;
- guarnição;
- soberania.

Se “centralidade administrativa” tiver efeito funcional persistente, pode exigir novo estado institucional. Se for apenas contexto da presença de Almeida, pode permanecer evento/expedição sem novo campo.

## 9. Coulão/Quilon

Fontes secundárias registram morte de portugueses em Quilon em 1505 e resposta armada de Lourenço de Almeida. A EVE também registra João Homem Godinho em ação ligada a Coulão.

### Decisão v0.1

Não criar `COL`/Quilon como nó antes de demonstrar necessidade funcional. O episódio pode ser evento específico se não produzir estado persistente necessário ao freeze.

## 10. T4 — combate

F5 é o gate final para reavaliar combate antes do freeze.

Até esta matriz, os casos identificados — Quiloa, Mombaça, Quilon e ações navais — ainda podem ser registrados como eventos históricos específicos sem sistema geral, porque o loop controlável ainda não foi definido como comando tático.

**Status T4 v0.1:** `COMBATE_FUNCIONAL_MINIMO = AINDA_NAO_DEMONSTRADO`.

A decisão só muda se a proposta funcional de F5 introduzir escolha militar do jogador cujo resultado precise ser resolvido pelo domínio.

## 11. Principais lacunas para v0.2

1. forma jurídica e cronologia da nomeação de Almeida: carta, Regimento e momento de exercício efetivo;
2. confirmar composição da armada e explicar 20 × 21 × 22 navios;
3. reconstruir cronologia crítica Lisboa→Quiloa→Mombaça→Anjediva→Cananor→Cochim sem harmonização artificial;
4. temporalidade exata da fortificação de Cananor e identificação do comando/guarnição;
5. estado institucional de Cochim após a chegada de Almeida;
6. resolver ou preservar definitivamente `Manuel Teles de Vasconcelos` × `Manuel Teles Barreto` no limiar 1504–1505;
7. papel e destino da armada separada de Pêro de Anhaia/Sofala;
8. identificar quais mudanças africanas e indianas precisam persistir em `31/12/1505`;
9. decidir se autoridade vice-real exige schema global ou apenas eventos;
10. fechar decisão T4 e proposta mínima antes de qualquer edição em `data/`.
