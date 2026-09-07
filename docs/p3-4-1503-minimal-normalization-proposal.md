# P3.4-doc — proposta mínima de normalização para 1503

Data: 2026-09-07
Issue: #114

## Finalidade

Definir o menor conjunto de dados historicamente defensável para representar o ciclo de 1503 sem ainda implementar campanha jogável, combate genérico ou sistema territorial amplo.

## 1. Expedições

Propor, em futura branch P3-func, três registros separados em `expeditions.csv`:

- `EXP_AFONSO_ALBUQUERQUE_1503`;
- `EXP_FRANCISCO_ALBUQUERQUE_1503`;
- `EXP_SALDANHA_1503`.

Não fundir as três partidas em uma única armada desde Lisboa. A convergência operacional deve ser registrada por rotas/eventos apenas quando documentada.

Os remanescentes da força de Vicente Sodré/Pedro de Ataíde não precisam virar uma quarta armada de origem independente; podem ser tratados como trajetória herdada de P3.3 que se agrega à força de 1503 em Anjediva.

## 2. Nós

### Reuso

- `COC` — Cochim;
- `CAL` — Calecute;
- `CAN` — Cananor, quando normalizado pelo P3.2 funcional;
- `ANJ` — Anjediva.

### Vaipim

Não criar nó jogável no primeiro incremento. Registrar `VAIPIM` como local associado ao evento de retirada/refúgio. Só materializar nó se houver necessidade operacional demonstrada.

### Coulão

A viagem diplomática e a feitoria de Coulão aparecem no ciclo de 1503, mas devem ser tratadas em subgate próprio ou no fechamento P3 se forem necessárias ao roadmap. Não ampliar #114 além de Cochim/fortificação/guarnição.

## 3. Estado temporal de Cochim

Criar futuramente tabela documental mínima `node_state_events.csv` (nome de trabalho) com pelo menos:

| event_id | node_id | data/período | tipo | efeito |
|---|---|---|---|---|
| `EV_COC_CALICUT_OFFENSIVE_1503` | COC | 1503-04 | `POLITICAL_CONTROL_CRISIS` | forças de Calecute ocupam/invadem Cochim; aliado recua |
| `EV_COC_RAJA_RETREAT_VAIPIM_1503` | COC | 1503-04 | `LOCAL_AUTHORITY_DISPLACED` | rajá e portugueses retiram-se para Vaipim |
| `EV_COC_RESTORED_1503` | COC | 1503-09 | `LOCAL_AUTHORITY_RESTORED` | rajá reassume a cidade após expulsão das forças de Calecute |
| `EV_COC_FORT_MANUEL_1503` | COC | 1503-09 | `FORTIFICATION_ESTABLISHED` | construção da fortificação portuguesa é iniciada/autorizada |
| `EV_COC_GARRISON_1503` | COC | fim de 1503 | `GARRISON_ESTABLISHED` | Duarte Pacheco permanece com força e duas caravelas |

Os nomes dos tipos são de modelagem e podem ser refinados; os fatos históricos e proveniência devem permanecer separados.

## 4. Atores

Candidatos mínimos:

- manter `ACT_COC_RAJA_1500` como autoridade local, estendendo sua relevância temporal se a documentação permitir;
- `ACT_DUARTE_PACHECO_1503` — somente se o projeto decidir que indivíduos comandantes precisam de ator explícito na camada relacional;
- preferencialmente `ACT_COC_PORTUGUESE_GARRISON_1503` como ator institucional agregado para a presença militar residente, se a mecânica futura precisar consultar a guarnição.

Não criar atores individuais para todos os capitães ou soldados apenas para preencher dados.

## 5. Fortaleza

Não alterar estaticamente `nodes.csv` para marcar Cochim como fortificada desde 1500. O campo `fortification` atual deve continuar refletindo o baseline anterior ao evento de 1503 enquanto não existir resolução temporal.

Quando o novo estado temporal for consumido pelo domínio, a leitura efetiva de fortificação deve resultar de:

`baseline do nó + eventos históricos aplicáveis à data da sessão`.

## 6. Soberania e relação

Em nenhum momento do gate 1503 Cochim deve ser convertida automaticamente em posse portuguesa.

O estado correto combina:

- soberania/autoridade local do rajá;
- aliança portuguesa;
- feitoria comercial portuguesa;
- fortificação portuguesa;
- guarnição residente.

Essas dimensões devem ser independentes.

Para Calecute, a hostilidade permanece relação política/militar; não há mudança territorial portuguesa.

## 7. Eventos militares

Registrar como eventos específicos:

- ofensiva de Calecute;
- retirada para Vaipim;
- recuperação de Cochim;
- eventual combate associado à recuperação.

O resultado histórico pode ser aplicado em modo `GUIDED` sem introduzir sistema geral de combate. Nenhum parâmetro de força, dano, moral ou baixas deve ser inventado neste estágio.

## 8. Duarte Pacheco e a passagem para 1504

O P3.4 termina com Duarte Pacheco Pereira deixado em Cochim no comando de duas caravelas e pequena força. As campanhas defensivas de 1504 pertencem ao próximo gate e devem partir desse estado persistido.

Isso cria uma fronteira limpa:

- P3.4 cria **fortificação + guarnição + força residente**;
- P3.5 testa como esse estado opera durante as ofensivas de 1504.

## 9. Critérios para futuro P3-func

A implementação só deve começar quando:

1. `node_state_events.csv` ou equivalente tiver schema definido e validação própria;
2. houver testes garantindo que Cochim em 1500–1502 continua sem fortificação portuguesa;
3. sessões em datas posteriores ao evento de setembro de 1503 consigam consultar fortificação/guarnição sem alterar soberania;
4. o baseline P1/P2 permaneça integralmente verde;
5. nenhum sistema de combate seja introduzido apenas para reproduzir um resultado histórico guiado.

## Decisão

O P3.4 documental pode ser considerado concluído com uma lacuna técnica explícita e limitada: **estado temporal de nó**. O primeiro passo funcional futuro não é combate; é representar de forma temporalmente correta a transformação institucional de Cochim em 1503.