# F4 — fontes dirigidas para a defesa de Cochim em 1504

Data: 2026-09-08
Issue: #130

Este registro introduz IDs estáveis de trabalho para as fontes adicionais usadas na tranche F4. A consolidação posterior em `docs/sources.md` deve ocorrer no closeout da tranche, sem alterar retrospectivamente a proveniência das linhas já existentes.

| source_id | Referência | Uso em F4 |
|---|---|---|
| `EVE_DUARTE_PACHECO` | Enciclopédia Virtual da Expansão Portuguesa, “Duarte Pacheco Pereira (?-1531/3)” | continuidade da força residente deixada em Cochim, comando de Duarte Pacheco em 1504, uso de terreno e artilharia, deslocamento posterior a Coulão e permanência até a chegada de Lopo Soares em setembro |
| `JESUS_LAND_WARFARE_2021` | Roger Lee de Jesus, “Reassessing Portuguese military superiority in Asia in the sixteenth century: the case of land warfare”, em Hélder Carvalhal, André Murteira e Roger Lee de Jesus (eds.), *The First World Empire: Portugal, War and Military Revolution*, Routledge, 2021, pp. 152–166, DOI 10.4324/9780429346965-13 | leitura crítica da defesa de Cochim, ataques sucessivos entre março e maio, relevância da geografia lagunar e cautela com cifras militares cronísticas |
| `ALVARO_VAZ_COCHIN_1504` | Álvaro Vaz a D. Manuel I, Cochim, 24/12/1504, publicada nas *Cartas de Affonso de Albuquerque*, vol. III, pp. 256–257 | testemunho contemporâneo usado por estudos especializados para confirmar a chegada de Lopo Soares a Cochim em 14/09/1504 e para o estado da presença portuguesa no fim do ano |
| `BOUCHON_LOPO_1976` | Geneviève Bouchon, “Le premier voyage de Lopo Soares en Inde (1504–1505)”, *Mare Luso-Indicum*, III, 1976, pp. 57–84; reeditado em *Inde découverte, Inde retrouvée* | reconstrução crítica da primeira viagem de Lopo Soares, sequência no Malabar, composição da armada e problemas onomásticos |
| `VICENTE_PORTUGAL_MADAGASCAR` | Manuel Alberto Carvalho Vicente, “Le Portugal et le Madagascar pendant le règne de D. Manuel Ier (1495–1521)” | síntese académica que fixa a entrada de Lopo Soares em Cochim em 14/09/1504 e remete à carta de Álvaro Vaz como confirmação documental |

## Regra cronológica

As datas diárias 16/03/1504 e 03/07/1504 aparecem em literatura secundária e reconstruções, mas não são promovidas a `EXACT` nesta tranche. A normalização funcional inicial usa apenas intervalos mensais sustentados: início em março, recorrência março–maio e encerramento da fase principal em julho.

A chegada de Lopo Soares a Cochim em 14/09/1504 é tratada de modo diferente: a data aparece em reconstrução académica e é explicitamente confirmada por carta contemporânea de Álvaro Vaz, de 24/12/1504. Esse marco pode ser normalizado como `EXACT` sem inferir as pernas anteriores da viagem.

## Divergência onomástica de 1504

A listagem EVE/FCSH registra `Manuel Teles Barreto` entre os capitães de 22/03/1504. A reconstrução especializada utilizada por Bouchon e por estudos posteriores distingue, porém, `Manuel Teles de Vasconcelos` na armada de 1504 e reserva `Manuel Teles Barreto` para uma armada posterior, de 1506.

F4 deve preservar essa divergência. Nenhuma transição de comando em Cochim será normalizada com identidade pessoal fechada até auditoria específica de documentação nominal. O catálogo de `EXP_LOPO_SOARES_1504` não precisa resolver essa divergência para representar a armada como unidade histórica.
