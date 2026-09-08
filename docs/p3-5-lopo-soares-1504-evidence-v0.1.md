# P3.5-doc — Lopo Soares 1504 — matriz de evidências v0.1

Data: 2026-09-08
Issue: #115
Baseline funcional herdado: `1a4f43822446a77d5bb79a76c14fab8a879a50d1`

## Escopo

Reconstrução inicial do ciclo de 1504 a partir do estado consolidado de Cochim em 31/12/1503: soberania local, feitoria restaurada, Forte Manuel e guarnição portuguesa residente. O foco é separar a defesa prolongada comandada por Duarte Pacheco Pereira da chegada posterior da armada de Lopo Soares de Albergaria e determinar quais fatos exigem apenas estados/eventos e quais podem demonstrar necessidade funcional de conflito.

## 1. Armada de Lopo Soares

A listagem EVE/FCSH registra em `22/03/1504` a partida sob Lopo Soares de Albergaria como capitão-mor e os seguintes capitães no mesmo dia:

- Leonel Coutinho;
- Lopo Mendes de Vasconcelos;
- Afonso Lopes da Costa;
- Filipe de Castro;
- Tristão da Silva;
- Vasco da Silveira;
- Vasco de Carvalho;
- Pêro Dinis;
- Lopo de Abreu;
- Manuel Teles Barreto;
- Pedro de Mendonça;
- Pedro Afonso de Aguiar.

Classificação:

- partida de Lisboa em 22/03/1504: `EXACT` na listagem EVE;
- composição nominal acima: evidência A/B para catálogo de trabalho;
- sequência fina Lisboa→Índia: ainda `UNRESOLVED` neste gate;
- chegada ao Malabar em setembro de 1504: `INTERVAL`, sustentada pelas biografias/entradas EVE;
- nenhuma rota deve ser normalizada apenas a partir da data de partida e do mês de chegada.

## 2. Estado herdado de 1503

F3 já demonstrou, por `node_state_events`, que em 31/12/1503 Cochim deve resolver como:

- soberania local do rajá;
- `FACTORY_RESTORED`;
- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- acesso negociado e relação favorável.

Esse é o estado inicial documental de F4 e não deve ser recriado em tabelas paralelas.

## 3. Defesa de Cochim sob Duarte Pacheco Pereira

A EVE registra de forma inequívoca que, ao longo de 1504, Duarte Pacheco liderou forças portuguesas e cochinenses contra investidas numericamente superiores do Samorim, explorando terreno favorável e superioridade de artilharia.

A literatura de síntese situa a fase principal das ofensivas entre março e julho de 1504. Neste primeiro gate, essa delimitação é tratada como `INTERVAL`, não como autorização automática para converter 16/03 e 03/07 em datas exatas do domínio.

Elementos funcionalmente relevantes já sustentados:

1. defesa prolongada, e não um único choque;
2. repetição de investidas;
3. comando persistente de Duarte Pacheco;
4. participação conjunta portuguesa e cochinense;
5. relevância do terreno/canais/passagens;
6. relevância da artilharia;
7. resultado histórico: preservação de Cochim e fracasso das ofensivas do Samorim.

Esses elementos fazem de 1504 um caso mais exigente que os confrontos específicos de 1500–1503.

## 4. Coulão após a defesa principal

A EVE registra que, após a vitória defensiva, Duarte Pacheco levou suas caravelas para sul em auxílio da feitoria de Coulão, ameaçada por muçulmanos locais, permanecendo ali até a chegada de Lopo Soares em setembro.

Classificação:

- deslocamento Cochim→Coulão: sequência sustentada, timing diário `UNRESOLVED`;
- permanência em Coulão até setembro: `INTERVAL`;
- função de Coulão: apoio a feitoria já existente no contexto histórico;
- decisão cartográfica: **não criar ainda nó/rota funcional de Coulão** até verificar se a movimentação precisa ser jogável ou se basta como evento de trajetória.

## 5. Chegada de Lopo Soares e encerramento do ciclo defensivo

A EVE registra que a armada de Lopo Soares chega em setembro de 1504 e que Duarte Pacheco prossegue com ela os combates vitoriosos. As entradas de Cochim e Calecute situam no fim de 1504 a derrota decisiva das forças adversárias com apoio da nova armada.

Classificação:

- chegada da armada em setembro: `INTERVAL`;
- reforço ao sistema defensivo luso-cochinense: fato firme;
- encerramento decisivo do ciclo no fim de 1504: `INTERVAL`;
- cronologia diária das ações posteriores à chegada: ainda insuficiente para normalização fina neste gate.

## 6. Transição de comando

A biografia EVE de Manuel Teles Barreto registra que ele partiu em 1504 como capitão da armada de Lopo Soares e estava nomeado capitão da armada de guarda da costa de Cochim, embora tenha regressado ao Reino na torna-viagem.

Isso demonstra uma questão institucional real para o fechamento de 1504: a presença/guarda costeira e o comando local não podem ser presumidos apenas pela continuidade de Duarte Pacheco. A identificação do sucessor efetivamente deixado em Cochim e da força residente precisa de auditoria adicional antes da proposta mínima.

## 7. Fontes de alta prioridade para aprofundamento

A entrada EVE sobre Conrad Peutinger registra a existência de documentação contemporânea ou quase contemporânea particularmente valiosa:

- descrição do percurso da armada de Lopo Soares de Lisboa a Calecute em 1504;
- carta/fragmento comercial de 1504;
- relatos da expedição anterior de 1503/04.

Esses documentos devem ser priorizados para a cronologia fina da armada antes de recorrer a reconstruções tardias.

## 8. Grau de evidência provisório

| Questão | Estado | Classificação |
|---|---|---|
| partida de Lopo Soares | 22/03/1504 | `EXACT` |
| composição nominal da armada | 13 capitães/capitão-mor na listagem | A/B |
| estado de Cochim no início de 1504 | feitoria + forte + guarnição sob soberania local | já normalizado / A-B |
| ofensivas do Samorim | defesa prolongada em 1504, fase principal mar.–jul. | `INTERVAL` |
| comando defensivo | Duarte Pacheco Pereira | A/B |
| terreno e artilharia como fatores | explicitamente relevantes | A/B |
| ida de Duarte Pacheco a Coulão | após fase principal da defesa | `INTERVAL` |
| chegada de Lopo Soares | setembro de 1504 | `INTERVAL` |
| derrota decisiva do adversário | fim de 1504 | `INTERVAL` |
| sucessão/comando residente após Duarte Pacheco | ainda não fechado | `UNRESOLVED` |
| rotas finas da armada | ainda não fechadas | `UNRESOLVED` |

## 9. Consequência para o gate de combate

F3 demonstrou que resultados militares isolados podiam permanecer eventos guiados. F4 apresenta pela primeira vez um conjunto repetido em que **posição, preparação e uso de meios defensivos são causalmente relevantes ao resultado**.

Isso ainda não autoriza combate geral. O próximo subgate deve responder se existe uma escolha abstrata, documentável e testável do jogador — por exemplo, postura defensiva/uso de posição/emprego de embarcações — cujo resultado precise ser resolvido funcionalmente. Se não houver agência necessária no loop histórico, a sequência poderá permanecer uma cadeia de eventos guiados e mudanças de estado.

## Próximos passos documentais

1. refinar a cronologia das ofensivas de março–julho sem adotar datas tardias como `EXACT` por conveniência;
2. identificar quais decisões de Duarte Pacheco são repetidas e estruturalmente relevantes, distinguindo narrativa heroica de elementos modeláveis;
3. fechar Coulão: localização, função e necessidade ou não de nó;
4. reconstruir a chegada/ações de Lopo Soares no Malabar com prioridade a documentação Peutinger;
5. fechar a sucessão de comando/força residente no fim de 1504;
6. produzir matriz `eventos guiados` × `combate funcional mínimo` antes de editar `data/` ou `simulation/`.