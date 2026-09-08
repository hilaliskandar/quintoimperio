# F5-doc — Francisco de Almeida 1505 — auditoria cronológica da rota v0.1

Data: 2026-09-08
Issue: #132
Baseline: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Objetivo

Reconstruir a sequência operacional da armada de Francisco de Almeida em 1505 separando âncoras contemporâneas/fortes de datas transmitidas apenas por reconstruções posteriores. Nenhuma perna é autorizada para implementação por esta auditoria isoladamente.

## 1. Fonte contemporânea principal para a costa africana

O relato conhecido como *The Voyage and Acts of Dom Francisco*, associado a Hans Mayr e ao Manuscrito Valentim Fernandes, é contemporâneo da viagem e informa ter sido redigido a bordo do `São Rafael` do Porto.

O extrato publicado por E. Axelson e reproduzido por Freeman-Grenville, atualmente acessível pelo Internet History Sourcebooks Project, permite fechar com grande precisão o trecho Lisboa–África Oriental, mas o extrato disponível termina em Melinde e não alcança a Índia.

### Âncoras fortes do relato

| Data | Marco | Classificação F5 |
|---|---|---|
| 25/03/1505 | partida da armada | `EXACT`, testemunho contemporâneo e convergente com EVE |
| 20/06/1505 | dobra do Cabo da Boa Esperança | `EXACT`, relato contemporâneo |
| 02/07/1505 | temporal severo | `EXACT`, relato contemporâneo; evento narrativo, não necessariamente nó |
| 18/07/1505 | primeiro avistamento de terra após o Cabo, próximo às “Ylhas Darradeiras” | `EXACT`, relato contemporâneo; identificação moderna ainda requer auditoria |
| 19/07/1505 | armada à vista de Moçambique | `EXACT`, relato contemporâneo; não equivale automaticamente a escala no porto |
| 21/07/1505 | passagem pelos baixos de São Rafael | `EXACT`, relato contemporâneo |
| 22/07/1505 | entrada no porto de Quiloa ao meio-dia, com oito navios | `EXACT`, relato contemporâneo |
| 24/07/1505 | desembarque/ocupação de Quiloa | `EXACT`, relato contemporâneo |
| 09/08/1505 | saída de Quiloa para Mombaça | `EXACT`, relato contemporâneo |
| 13/08/1505 | chegada de Francisco de Almeida com o núcleo da força a Mombaça | `EXACT`, inferência direta do relato: o São Rafael chega em 14/08 e o capitão-mor com os outros dez navios chegara um dia antes |
| 14/08/1505 | chegada do `São Rafael` a Mombaça | `EXACT`, relato contemporâneo |
| agosto de 1505 | saída posterior em direção a Melinde | sequência segura, mas o extrato acessível não fornece nesta versão uma data única de chegada a Melinde |

## 2. Divergências corrigidas pela fonte contemporânea

Sínteses posteriores frequentemente situam Quiloa em 23 ou 24/07. O relato contemporâneo distingue claramente:

- `22/07`: entrada da armada no porto;
- `24/07`: desembarque/ocupação.

Esses eventos não devem ser harmonizados em uma única “chegada a Quiloa em 24/07”.

Também é necessário distinguir em Mombaça:

- `13/08`: chegada do capitão-mor e de dez navios;
- `14/08`: chegada do `São Rafael`.

A pluralidade de chegadas mostra por que a cronologia de uma expedição não deve presumir que toda a frota ocupa sempre uma única posição simultânea no mesmo dia.

## 3. Consequências institucionais na África Oriental

O relato contemporâneo registra em Quiloa:

- substituição do soberano local após a tomada da cidade;
- construção/adaptação imediata de uma fortificação portuguesa;
- artilharia instalada;
- Pêro Ferreira deixado no comando com força residente.

Esses fatos são candidatos a estado temporal persistente em `KIL` no horizonte 31/12/1505, mas esta auditoria não normaliza números de guarnição nem cria novo `node_state_event` antes da proposta mínima.

Mombaça aparece como episódio de ataque, saque e incêndio. Até aqui, não foi demonstrado que o estado de Mombaça em 31/12/1505 exija uma dimensão persistente do domínio comparável à fortificação de Quiloa.

## 4. Limite da fonte para a Índia

O extrato acessível do relato de Hans Mayr termina em Melinde. Ele não fornece, nesta forma publicada consultada:

- chegada a Anjediva;
- chegada/estadia em Cananor;
- chegada a Cochim.

Por isso, essas datas não devem herdar automaticamente grau `A/EXACT` apenas porque aparecem de forma estável em sínteses posteriores.

## 5. Matriz provisória da Índia

| Marco | Data recorrente em reconstruções | Situação F5 v0.1 |
|---|---|---|
| Anjediva | 13/09/1505 | `CANDIDATE_EXACT`; necessita fonte crítica/primária identificada |
| Cananor — chegada/negociação | 22–23/10/1505 | `UNRESOLVED_DAILY`; EVE sustenta demora em outubro |
| Cananor — autorização/início da fortificação | 23–24/10/1505 em sínteses | `MONTH_SECURE`; EVE sustenta negociação e início da fortificação em outubro/1505, sem fixar dia na entrada consultada |
| Cochim — chegada | 31/10 ou 01/11/1505 | `UNRESOLVED_DAILY`; convergência secundária forte, mas ainda sem equivalente contemporâneo auditado |

## 6. Regra para futura normalização de rotas

F5 não deve converter automaticamente todas as âncoras acima em `expedition_routes.csv`.

Antes disso, é necessário decidir:

1. se a campanha de Almeida precisa ser executável no loop Python 1505 GREEN;
2. se o schema atual suporta as separações da frota sem inventar simultaneidade;
3. quais trechos podem usar observações históricas e quais precisariam permanecer `SIMULATION`;
4. se Quiloa/Mombaça precisam de loop controlável ou apenas eventos/estados persistentes.

O trecho africano já possui cronologia suficiente para eventual normalização. A Índia ainda não.

## 7. Próximo subgate

Prioridades:

1. localizar a fonte ou edição crítica usada para 13/09 em Anjediva;
2. fechar a temporalidade da fortificação de Cananor em outubro de 1505 sem depender de Wikipedia;
3. buscar fonte contemporânea ou cronologia crítica para a chegada a Cochim;
4. em seguida produzir matriz institucional comparando `KIL`, `CAN` e `COC` em 31/12/1505.

## Fonte principal deste gate

- Hans Mayr [atrib.], *The Voyage and Acts of Dom Francisco, 1505–*, relato contemporâneo associado ao Manuscrito Valentim Fernandes; extrato publicado por E. Axelson, “South East Africa”, 1940, e reproduzido em G. S. P. Freeman-Grenville, *The East African Coast: Selected Documents*, 1974.
