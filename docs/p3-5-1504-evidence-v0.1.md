# P3.5-doc — Lopo Soares 1504 e defesa de Cochim — matriz v0.1

Data: 2026-09-07
Issues: #110, #115

## Objetivo

Reconstruir o ciclo de 1504 a partir do estado criado em 1503 — Cochim sob soberania local, com feitoria, fortificação e força portuguesa residente — e verificar se os confrontos de 1504 exigem nova mecânica ou ainda podem ser representados como eventos históricos guiados.

## Fontes de trabalho

- EVE/FCSH, `Cochim`;
- EVE/FCSH, `Calicute`;
- EVE/FCSH, `Duarte Pacheco Pereira`;
- EVE/FCSH, listagem das Armadas da Índia do reinado de D. Manuel I;
- EVE/FCSH, biografias de capitães da armada de 1504;
- EVE/FCSH, entrada sobre a coleção documental de Conrad Peutinger, que registra a existência de descrição contemporânea do percurso da armada de Lopo Soares em 1504;
- documentação P3.4.

## Armada de Lopo Soares

A listagem EVE registra partida em **22/03/1504** sob Lopo Soares de Albergaria, com um conjunto numeroso de capitães. Entre os nomes explicitamente listados estão Leonel Coutinho, Lopo Mendes de Vasconcelos, Afonso Lopes da Costa, Filipe de Castro, Tristão da Silva, Vasco da Silveira, Vasco de Carvalho, Pêro Dinis, Lopo de Abreu, Manuel Teles Barreto, Pedro de Mendonça e Pedro Afonso de Aguiar.

Essa listagem serve para composição nominal da armada, mas não deve ser convertida automaticamente em quantidade de navios distinta sem conferir duplicidades de função/comando e fontes específicas.

## Sequência histórica mínima

| Momento | Evento | Efeito | Grau |
|---|---|---|---|
| início de 1504 | Duarte Pacheco permanece em Cochim com duas caravelas e força residente deixadas em 1503 | continuidade da guarnição/defesa portuguesa | A |
| 1504 | forças do Samorim lançam sucessivas investidas contra Cochim | crise militar recorrente; soberania local de Cochim permanece defendida, não substituída por Portugal | A/B |
| 1504 | Duarte Pacheco comanda forças portuguesas e cochinenses, utilizando terreno favorável e artilharia superior | defesa luso-cochinense sustentada | B |
| após a defesa principal | Duarte Pacheco desloca as caravelas para sul em socorro da feitoria de Coulão | ampliação operacional da força residente, sem mudança automática de soberania em Coulão | B |
| setembro de 1504 | chegada da armada de Lopo Soares de Albergaria | reforço externo à presença já estabelecida | A |
| fim de 1504 | defensores luso-cochinenses, agora apoiados pela armada de Lopo Soares, derrotam decisivamente as forças adversárias | encerramento do ciclo de grandes ofensivas sobre Cochim neste recorte | A/B |
| após chegada de Lopo Soares | Duarte Pacheco regressa ao Reino com a armada | termina seu comando residente em Cochim | A/B |

## Cochim como estado persistente

O ponto central de 1504 é que a fortificação de 1503 não é um evento encerrado: ela se torna **estado persistente** que condiciona a defesa de 1504.

Assim, o futuro modelo temporal precisa permitir que:

- `COC` em 1500–1502 não tenha fortificação portuguesa;
- `COC` após setembro de 1503 tenha fortificação e guarnição/força residente;
- essas propriedades continuem presentes em 1504 até serem alteradas por evento posterior;
- nenhuma dessas propriedades altere a soberania do rajá.

## Relação Cochim–Calecute

A EVE registra que o conflito iniciado pela ofensiva do Samorim continuou até o final de 1504. O resultado não deve ser interpretado como conquista de Calecute pelos portugueses. O que muda é a capacidade de Cochim, com apoio português, sustentar-se frente às ofensivas do rival.

Portanto:

- `CAL` permanece soberano e adversário;
- `COC` permanece soberano sob o rajá aliado;
- a relação bilateral/hostilidade e o estado defensivo de Cochim se alteram;
- não há transferência territorial entre nós.

## Duarte Pacheco

Seu papel pode ser decomposto em três estados:

1. **1503** — comandante deixado em Cochim com duas caravelas;
2. **1504** — comandante das forças portuguesas/cochinenses durante as ofensivas;
3. **após chegada de Lopo Soares** — retorna ao Reino com a armada.

Isso favorece tratar o comando residente como estado/ator temporal, não como propriedade fixa do nó.

## Coulão

Coulão aparece de forma operacional em 1504: Duarte Pacheco desloca suas caravelas para socorrer a feitoria e capitães da armada de Lopo Soares também são enviados a carregar especiarias ali.

Coulão passa, portanto, a ser candidato mais forte a nó futuro do que em P3.4. Ainda assim, sua normalização deve distinguir:

- feitoria/comércio;
- eventual conflito local;
- rota navegável Cochim–Coulão;
- ausência de fortificação portuguesa equivalente à de Cochim neste momento.

## Cananor

Uma passagem importante da EVE sobre Gonçalo Gil Barbosa registra que Lopo Soares chegou a Cananor em 1504 com instruções régias para solicitar autorização de construção de uma fortaleza. O pedido não foi feito naquele momento devido às circunstâncias políticas e só seria apresentado posteriormente.

Consequência metodológica: **ordem régia não equivale a estado realizado**. Cananor não deve ser marcado como fortificado em 1504 apenas porque a instrução existia.

Esse caso reforça a necessidade de separar:

- intenção/ordem;
- negociação/autorização;
- construção efetiva;
- estado persistente.

## Combate — diagnóstico preliminar

O ciclo de 1504 é a primeira sequência em que há confrontos repetidos ao longo de vários meses, e não apenas um episódio isolado. Isso aumenta a pressão para uma abstração funcional futura, mas ainda não prova necessidade de um sistema geral de combate.

Antes de qualquer implementação, deve-se perguntar:

1. as batalhas precisam produzir resultados variáveis para haver agência do jogador?
2. ou o loop inicial pode representá-las como eventos históricos guiados condicionados a estados prévios — fortificação, guarnição, apoio local e chegada de reforço?
3. quais decisões do jogador realmente existiriam antes/durante os confrontos sem inventar tática detalhada?

Até essa auditoria, não devem ser criados pontos de força, moral, artilharia ou baixas.

## Divergências e lacunas

1. cronologia diária das múltiplas batalhas de 1504 ainda precisa ser consolidada em fonte narrativa especializada;
2. dimensão numérica das forças não será normalizada sem fonte adequada;
3. a composição nominal da armada de Lopo Soares é ampla, mas o número operacional de embarcações exige checagem adicional;
4. a data exata da saída de Duarte Pacheco do teatro oriental deve ser refinada se for necessária ao loop;
5. o status institucional que sucede ao comando de Duarte Pacheco em Cochim precisa ser reconstruído antes do baseline de 1505.

## Próximas verificações

1. localizar e fichar a descrição contemporânea da viagem de Lopo Soares mencionada na coleção Peutinger;
2. reconstruir a cronologia das principais ofensivas de 1504 e suas localizações;
3. definir se Coulão entra já na normalização P3.5;
4. identificar quem assume ou estrutura a presença militar em Cochim após a partida de Duarte Pacheco;
5. preparar auditoria explícita: `EVENTOS GUIADOS` versus `NECESSIDADE DE COMBATE FUNCIONAL`;
6. produzir proposta mínima de normalização para 1504 antes de qualquer edição em `data/`.