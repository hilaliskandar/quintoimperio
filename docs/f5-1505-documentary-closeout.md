# F5-doc — Francisco de Almeida 1505 — closeout documental

Data: 2026-09-08
Issue: #132
Gate-mãe: #118
Guarda-chuva documental: #110
Baseline F4: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Resultado

O gate documental de 1505 reuniu evidência suficiente para abrir uma tranche funcional mínima sem criar novo schema global de governo, combate geral ou múltiplas frotas simultâneas.

A estrutura documental consolidada distingue:

- armada principal de Francisco de Almeida;
- expedição separada de Pêro de Anhaia;
- nomeação régia, Regimento, comando expedicionário e exercício vice-real no Índico;
- eventos militares específicos;
- fortificações/guarnições que produzem estado persistente;
- centralidade administrativa de Cochim sem transferência de soberania.

## 1. Decisões finais de arquitetura

### Autoridade

`NEW_GLOBAL_AUTHORITY_SCHEMA = NAO_NECESSARIO`

A autoridade de Almeida pode ser representada por metadados da expedição e eventos institucionais. Nenhum comportamento funcional até `31/12/1505` demonstrou necessidade de consultar um estado global de governo independente da expedição/eventos.

### Combate

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

O horizonte 1500–1505 contém violência crescente, mas os estados históricos necessários podem ser produzidos por eventos específicos e transições temporais. O loop não demonstrou decisão militar controlável pelo jogador que exija resolução sistêmica de batalha.

### Frotas simultâneas

`MULTI_ACTIVE_FLEET_SCHEMA = NAO_NECESSARIO`

Almeida e Anhaia devem existir como expedições históricas separadas, mas isso não obriga o save a controlar duas frotas simultâneas. Expedições sem pernas continuam sendo precedente suficiente quando o itinerário não faz parte do loop.

## 2. Armada de Francisco de Almeida

### Âncoras institucionais

- `27/02/1505` — carta de poder/nomeação como capitão-mor, missão prevista por três anos;
- `03/03/1505` — Regimento;
- `25/03/1505` — partida da armada;
- outubro de 1505 — fase em que a autoridade vice-real passa a estar materialmente exercida no Índico, sem dia único fechado nesta documentação;
- `16/12/1505` — presença documental de Almeida em Cochim por carta escrita no porto.

A fórmula “vice-rei efetivo desde Lisboa” foi rejeitada como simplificação anacrônica.

### Composição

O número de embarcações permanece divergente:

- Hans Mayr / tradição contemporânea: 20 velas, 14 naus e 6 caravelas;
- EVE: 21 comandos/capitães na partida;
- Barros/Góis: 22;
- Livro das Armadas em reconstruções críticas: 23.

Decisão: `fleet_size = UNRESOLVED`. Nenhum valor será parametrizado no domínio sem necessidade funcional.

## 3. Cronologia africana forte

O relato contemporâneo associado a Hans Mayr fixa:

- 25/03 — partida;
- 20/06 — Cabo da Boa Esperança;
- 18/07 — primeiro avistamento de terra pós-Cabo;
- 19/07 — à vista de Moçambique;
- 21/07 — baixos de São Rafael;
- 22/07 — entrada em Quiloa;
- 24/07 — desembarque/ocupação de Quiloa;
- 09/08 — saída de Quiloa;
- 13/08 — chegada do capitão-mor a Mombaça;
- 14/08 — chegada do `São Rafael` a Mombaça.

Esses marcos podem ser usados como eventos históricos `EXACT` sem transformar automaticamente o percurso em campanha jogável.

## 4. Estados persistentes em 31/12/1505

### Quiloa — `KIL`

Mudanças necessárias:

- presença portuguesa residente;
- fortificação portuguesa;
- guarnição portuguesa;
- mudança política local sob forte intervenção portuguesa, sem traduzir automaticamente em soberania territorial portuguesa.

A fonte contemporânea é forte para 22–24/07 e para a instalação da fortificação/força residente.

### Sofala — `SOF`

Mudanças necessárias:

- feitoria/presença institucional portuguesa;
- fortificação/tranqueira;
- guarnição residente;
- Pêro de Anhaia como autoridade portuguesa local.

Âncoras fortes:

- `04/09/1505` — início da capitania de Pêro de Anhaia segundo EVE;
- `21/09/1505` — início da tranqueira segundo HPIP.

A variante `25/09` permanece registrada em reconstruções secundárias, sem substituir silenciosamente a ficha especializada.

### Anjediva — `ANJ`

Mudanças necessárias:

- fortificação portuguesa;
- presença/guarnição portuguesa.

A função estratégica e a construção em 1505 são fortes. A data diária 13–14/09 continua menos bem sustentada nesta auditoria que Quiloa/Sofala/Cananor.

Decisão: primeira implementação pode usar `setembro de 1505` como janela conservadora, sem elevar 13/09 ou 14/09 a `EXACT`.

### Cananor — `CAN`

Mudanças necessárias:

- manutenção da feitoria;
- nova fortificação portuguesa;
- guarnição portuguesa;
- soberania local preservada;
- acesso negociado e relação sob tensão, sem hostilidade automática.

A EVE fixa outubro; cronologia crítica baseada em Damião de Góis fixa `23/10/1505` para início da fortaleza. A implementação pode usar essa data como `EXACT` com proveniência explícita ou uma janela 23–31/10 se preferir conservadorismo.

### Cochim — `COC`

O estado herdado de 1503–1504 permanece:

- soberania local;
- feitoria;
- Forte Manuel;
- guarnição portuguesa;
- acesso negociado;
- relação favorável.

A novidade de 1505 é a centralidade administrativa/residencial da autoridade de Almeida. Isso deve ser evento institucional, não novo campo de soberania/fortificação.

A chegada em 31/10 aparece de modo convergente em tradição secundária, mas a âncora contemporânea segura usada nesta documentação é a carta de Almeida em Cochim em 16/12.

### Mombaça — `MOM`

O saque/bombardeio de agosto não produz fortificação ou guarnição portuguesa persistente demonstrada para 31/12/1505.

Decisão: evento de expedição, sem novo estado persistente.

## 5. Expedição separada de Pêro de Anhaia

A EVE registra partida em `18/05/1505`, separada da armada de Almeida.

A futura implementação deve criar `EXP_ANHAIA_1505` separadamente e pode mantê-la sem pernas executáveis. Seus efeitos em Sofala pertencem a essa expedição, não à de Almeida.

## 6. Divergências preservadas

### Comando de Cochim

`Manuel Teles de Vasconcelos × Manuel Teles Barreto = UNRESOLVED`

A divergência não bloqueia o freeze porque o domínio precisa da existência da guarnição, não necessariamente do nome do comandante.

### Armada

`20 × 21 × 22 × 23 embarcações = UNRESOLVED`

### Anjediva

`13/09 × 14/09 = candidato historiográfico; mês de setembro seguro`

### Cochim

`31/10 × 01/11 = candidato cronístico/secundário; presença em 16/12 documentalmente segura`

### Cananor

`23/10` é candidato forte com base em cronologia crítica; EVE oferece segurança mensal independentemente.

## 7. Proposta funcional autorizada

O primeiro F5 funcional deve limitar-se a:

1. registrar `EXP_ALMEIDA_1505`;
2. registrar `EXP_ANHAIA_1505`;
3. registrar eventos institucionais de nomeação/Regimento/partida/autoridade no Índico;
4. registrar apenas os eventos exatos africanos indispensáveis;
5. criar estados temporais em `KIL`, `SOF`, `ANJ` e `CAN` usando o schema existente;
6. manter `COC` sob soberania local e registrar centralidade de Almeida como evento institucional;
7. manter `MOM` sem forte/guarnição persistente;
8. não criar combate, novo schema global, nova economia ou novos nós;
9. testar save/load e gerar golden state de `31/12/1505`.

## 8. Documentos do gate

- `docs/f5-1505-evidence-matrix-v0.1.md`;
- `docs/f5-1505-authority-fleet-audit-v0.1.md`;
- `docs/f5-1505-route-chronology-audit-v0.1.md`;
- `docs/f5-1505-institutional-matrix-v0.1.md`;
- `docs/f5-1505-sofala-anhaia-anjediva-audit-v0.1.md`;
- `docs/f5-1505-cannanore-cochin-audit-v0.1.md`;
- `docs/f5-1505-minimal-normalization-proposal.md`;
- este closeout.

## 9. Critério de integração do gate documental

A branch F5-doc deve ser integrada somente se:

- o diff permanecer exclusivamente documental;
- CI integral verde;
- PR sem pendências materiais;
- CI pós-merge verde;
- Diário do Drive sincronizado.

Somente após isso deve ser aberta F5 funcional.

## 10. Handoff para Python 1505 GREEN

F5 funcional será a última tranche histórica antes do gate transversal/freeze. Ao final dela, deve-se auditar T1–T6, executar regressão integrada 1497–1505, gerar golden state(s) de `31/12/1505` e produzir `docs/domain-freeze-1505.md`.
