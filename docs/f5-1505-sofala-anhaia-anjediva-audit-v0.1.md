# F5-doc — 1505 — auditoria Sofala / Pêro de Anhaia / Anjediva v0.1

Data: 2026-09-08
Issue: #132
Baseline: `0a75006a5097c7b5f2cf04ab83fbf5312a53fca6`

## Objetivo

Determinar quais mudanças em Sofala e Anjediva precisam persistir no estado de `31/12/1505`, preservando a separação entre a armada principal de Francisco de Almeida e a expedição própria de Pêro de Anhaia.

## 1. Pêro de Anhaia é uma expedição separada

A EVE/FCSH registra a saída de Pêro de Anhaia como capitão-mor em `18/05/1505`, após a partida da armada principal de Francisco de Almeida em 25/03.

A entrada biográfica da EVE confirma que Anhaia deveria inicialmente integrar a armada do vice-rei, mas, após naufrágio ainda no Tejo, saiu posteriormente com frota própria e missão específica de construir a fortaleza de Sofala.

### Decisão documental

F5 deve tratar como unidade própria:

`EXP_ANHAIA_1505`

Não comprimir a expedição na `EXP_ALMEIDA_1505`.

A primeira implementação poderá registrá-la sem pernas executáveis se a cronologia completa Lisboa→Sofala não for necessária ao loop.

## 2. Sofala — cronologia forte

A EVE fornece uma âncora institucional particularmente útil:

`04/09/1505 – 04/05/1506 — Pedro Anhaia, Capitão de Sofala`.

A entrada de Sofala registra que o rei Yusuf negociou com Pêro de Anaia a construção da fortaleza e identifica-o como primeiro capitão de Sofala a partir de setembro de 1505.

O HPIP, em ficha da Fortaleza de São Caetano, fornece data ainda mais fina para a obra:

`21/09/1505` — início da tranqueira de madeira ordenada por Pêro de Anaia.

A fortificação primitiva é descrita como estrutura de madeira; a obra de pedra e cal pertence a 1506 e não deve ser retroprojetada para 1505.

### Estado candidato de `SOF` em 31/12/1505

| Dimensão | Estado proposto documentalmente |
|---|---|
| soberania local | não presumir soberania portuguesa sobre o hinterland/território |
| presença institucional | portuguesa residente |
| feitoria | estabelecida no contexto da missão de Anhaia |
| fortificação | tranqueira/fortificação portuguesa existente desde setembro de 1505 |
| guarnição | força residente existente; quantidade não precisa ser normalizada |
| autoridade portuguesa local | capitão de Sofala — Pêro de Anhaia |

### Consequência de schema

`SOF` é forte candidato a `node_state_events` em 1505 para:

- presença institucional/feitoria;
- fortificação;
- guarnição.

Não é necessário criar novo nó: `SOF` já existe.

## 3. Divergência de data da construção de Sofala

Reconstruções secundárias amplamente difundidas usam `25/09/1505` para o início da construção.

O HPIP usa `21/09/1505`.

### Decisão

Para futura normalização, dar precedência ao HPIP como ficha patrimonial especializada enquanto não houver fonte primária mais fina auditada.

Registrar a divergência `21/09 × 25/09` na proposta mínima; não harmonizar silenciosamente.

## 4. Anjediva — evidência de função e presença

A EVE registra múltiplos elementos fortes para Anjediva em 1505:

- Gaspar da Índia participou ativamente no planeamento e construção da fortaleza da ilha;
- Gonçalo de Paiva e Rodrigo Rebelo receberam função naval junto a Angediva para bloquear comércio muçulmano;
- João Homem Godinho foi enviado da ilha com cartas para os feitores de Cananor, Cochim e Coulão.

Isso demonstra que Anjediva não foi simples passagem: em 1505 houve fortificação e força/presença operacional portuguesa.

## 5. Anjediva — problema cronológico

Sínteses posteriores convergem em:

- chegada em 13/09/1505;
- início da construção em 14/09/1505.

Nesta rodada, porém, não foi localizado equivalente contemporâneo/HPIP/EVE que fixe esses dois dias com a mesma força documental obtida para Sofala.

### Decisão v0.1

O estado de `ANJ` em 31/12/1505 provavelmente precisa refletir:

- `PORTUGUESE_FORT` ou equivalente histórico temporal;
- presença/guarnição portuguesa.

Mas a data de aplicação não deve ser fixada como 13 ou 14/09 antes de fonte crítica adicional.

A proposta mínima poderá usar uma janela conservadora de setembro se nenhum testemunho diário melhor for localizado, desde que a fortificação esteja seguramente estabelecida até o fim do mês.

## 6. Comparação Sofala × Anjediva

| Critério | Sofala | Anjediva |
|---|---|---|
| expedição própria | sim — Anhaia | não; vinculada à armada de Almeida |
| fortificação em 1505 | segura | segura |
| data diária forte | 21/09 HPIP | ainda não fechada criticamente |
| presença residente | segura | forte/provável |
| nó já existente | sim | sim |
| nova rota necessária | não demonstrada | não demonstrada |
| combate geral necessário | não | não |

## 7. Consequência para Python 1505 GREEN

O freeze de `31/12/1505` não pode manter `SOF` e `ANJ` exatamente como estavam em 1498–1504 se as fortalezas/presenças de 1505 forem consideradas parte do horizonte histórico necessário.

A arquitetura atual de `node_state_events` parece suficiente para ambas.

Não há necessidade demonstrada de:

- novo schema territorial;
- múltiplas frotas simultâneas;
- combate geral;
- novos nós;
- valores quantitativos de guarnição.

## 8. Próximo subgate

1. fechar Cananor em outubro: fortificação, guarnição e comando;
2. fechar chegada/assunção de Almeida em Cochim;
3. tentar melhorar a data de Anjediva;
4. então produzir proposta mínima consolidada F5 com os estados de `KIL`, `SOF`, `ANJ`, `CAN` e `COC` em 31/12/1505.
