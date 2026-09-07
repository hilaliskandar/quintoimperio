# P1 — Matriz de evidências do retorno da primeira viagem, 1498–1499

Status: gate documental inicial. Nenhuma alteração de domínio, mapa, dados históricos ou parâmetros de `simulation/` é autorizada por este documento.

Issue de referência: #92.

Commit de referência do MVP Lisboa–Calecute: `f308fb0e97687e34365fd23ed257a0114fd81613`.

## Objetivo

Reconstruir o itinerário de retorno da primeira viagem de Vasco da Gama depois da saída de Calecute, distinguindo explicitamente:

- fatos narrados no `Roteiro`/Journal;
- datas inseridas ou harmonizadas pelo editor Ravenstein;
- sínteses editoriais posteriores ao ponto em que o manuscrito termina;
- inferências operacionais que ainda precisam de validação antes de se tornarem `data/`.

A matriz abaixo é deliberadamente mais conservadora do que um roteiro de implementação. Um lugar mencionado não se torna automaticamente nó operacional; uma parada não se torna mercado; um alimento adquirido não implica regra genérica de reabastecimento; uma perda humana não autoriza ainda um sistema de tripulação.

## Fonte primária de trabalho

E. G. Ravenstein (trad./ed.), *A Journal of the First Voyage of Vasco da Gama, 1497–1499*, Hakluyt Society, 1898, disponibilizado integralmente pelo Project Gutenberg:

- https://www.gutenberg.org/files/46440/46440-h/46440-h.htm
- https://www.gutenberg.org/cache/epub/46440/pg46440-images.html

Para o retorno, o corpo narrativo cobre a saída de Calecute até os baixios do Rio Grande, em 25/04/1499. A partir daí o `Roteiro` termina abruptamente; Ravenstein acrescenta uma síntese editorial baseada em autores posteriores. Essa mudança de estatuto deve permanecer visível na base.

## Matriz cronológica preliminar

| ID provisório | Partida | Origem | Chegada | Destino / referência | Evidência logística e material | Frota / perdas | Estatuto da evidência | Implicação preliminar |
|---|---|---|---|---|---|---|---|---|
| P1-R01 | 30/08/1498 | costa de Calecute | 15/09/1498 | ilhas de Santa Maria | navegação costeira lenta, tacking com brisas de terra e mar; contatos costeiros e pesca/comércio episódico | três navios ainda no retorno | narrativa direta do `Roteiro`; data de 30/08 explícita | trecho costeiro, não deve ser colapsado automaticamente em salto direto até Anjediva |
| P1-R02 | 15/09/1498 | ilhas de Santa Maria | 20/09/1498 | Anjediva | ereção de padrão em Santa Maria; em Anjediva, água, madeira e gêneros alimentares; permanência para carena | três navios | narrativa direta; cabeçalho editorial marca Anjediva 20/09–05/10 | Anjediva é forte candidata a escala logística operacional, mas não a mercado pleno |
| P1-S01 | 20/09/1498 | Anjediva | 05/10/1498 | Anjediva | permanência de doze dias contados pelo texto a partir de 24/09; peixe, abóboras, pepinos, água; carena dos navios; desmonte de embarcação capturada | a frota portuguesa permanece com três navios; embarcação capturada é destruída | narrativa direta; há diferença entre chegada em 20/09 e os doze dias de permanência associados ao período 24/09–05/10 | modelar permanência separadamente da viagem; não inferir automaticamente reabastecimento quantitativo |
| P1-R03 | 05/10/1498 | Anjediva | 02–03/01/1499 | costa da África Oriental, próximo a Mogadíscio | travessia muito longa com calmarias e ventos contrários; escorbuto severo; quase colapso da capacidade de manobra; ausência de piloto capaz de localizar a posição na carta | 30 mortos durante a travessia; só 7–8 homens aptos por navio segundo o relato | narrativa direta; Ravenstein resume a travessia como 94 dias Anjediva–Melinde, chegando a Melinde em 07/01 | este trecho exige gate próprio antes de qualquer modelo de doença/tripulação; mecanicamente, por ora, só registra evidência e risco |
| P1-R04 | 03/01/1499 aprox. | costa de Mogadíscio | 07/01/1499 | Melinde | navegação costeira; incidente em Pate; busca deliberada por Melinde | S. Rafael ainda navegável, mas danificada em temporal em 05/01 | narrativa direta | Mogadíscio e Pate são referências de passagem/incidente, não automaticamente escalas jogáveis |
| P1-S02 | 07/01/1499 | Melinde | 11/01/1499 | Melinde | frutas, especialmente laranjas, aves e ovos; repouso; intercâmbio diplomático; marfim e jovem enviado para Portugal | novas mortes entre os doentes durante a estadia | narrativa direta; texto diz permanência de cinco dias | escala logística e diplomática claramente documentada; qualquer efeito de saúde exige modelo separado |
| P1-R05 | 11/01/1499 | Melinde | 13/01/1499 | Baixos de São Rafael | passagem por Mombaça em 12/01; ancoragem nos baixos em 13/01 | frota chega com três navios | narrativa direta | provável perna curta de transição; Mombaça aparece como passagem, sem parada operacional documentada neste retorno |
| P1-S03 | 13/01/1499 | Baixos de São Rafael | 27/01/1499 | Baixos de São Rafael | permanência prolongada; aves obtidas por venda/troca a partir de Tamugate | S. Rafael é queimado por falta de tripulação; conteúdo transferido aos outros dois navios | narrativa direta; texto diz quinze dias | evento estrutural de campanha: redução definitiva de três para dois navios. Não transformar ainda em sistema genérico de descarte de navio |
| P1-R06 | 27/01/1499 | Baixos de São Rafael | 01/02/1499 | ilha de São Jorge, junto a Moçambique | passa próximo a Zanzibar em 28/01; ancoragem tardia em 01/02; partida imediata; padrão erguido em 02/02 | dois navios | narrativa direta | Zanzibar é passagem; São Jorge é parada brevíssima/ritual, não evidência de mercado ou reabastecimento |
| P1-R07 | 02/02/1499 | ilha de São Jorge / Moçambique | 03/03/1499 | Angra de São Brás | nenhum contato com a cidade de Moçambique; longa navegação para sul | dois navios | narrativa direta; quadro editorial resume 30 dias | evitar fazer a volta reutilizar automaticamente o mesmo padrão de escala da ida |
| P1-S04 | 03/03/1499 | Angra de São Brás | 12/03/1499 e nova tentativa | Angra de São Brás | pesca de anchovas, focas e pinguins, salgados para a viagem; tentativa de partida em 12/03 frustrada por vento oeste e retorno à baía | dois navios | narrativa direta | permanência logística forte, com alimento preparado explicitamente para viagem; retorno forçado à escala deve ser representável sem inventar datas adicionais |
| P1-R08 | após 12/03/1499 | Angra de São Brás | 20/03/1499 | Cabo da Boa Esperança | nova partida quando o vento cede; dobragem do Cabo em 20/03 | dois navios | narrativa direta; data da partida final não é explicitada com precisão após o retorno de 12/03 | não fixar `departure_date` exata antes de resolver a lacuna documental |
| P1-R09 | 20/03/1499 | Cabo da Boa Esperança | 25/04/1499 | baixos do Rio Grande | 27 dias iniciais com vento favorável, depois calmarias e ventos contrários; navegação por sondagens sem avistar terra | dois navios | narrativa direta; 25/04 explícito | ponto final seguro do manuscrito do `Roteiro`; qualquer continuação deve mudar de camada de evidência |
| P1-R10 | após 25/04/1499 | baixos do Rio Grande | 10/07/1499 | Cascais/Lisboa, navio de Nicolau Coelho | continuação independente após separação dos navios | Berrio chega primeiro; separação atribuída por Ravenstein a fontes posteriores | síntese editorial pós-`Roteiro`; data de 10/07 para Coelho | tratar como evidência secundária/compilada até conferir a fonte de origem |
| P1-R11 | após 25/04/1499 | baixos do Rio Grande | antes de 28/08/1499 | Lisboa, S. Gabriel sob João de Sá | João de Sá assume o S. Gabriel depois de escala de Vasco da Gama em São Thiago | S. Gabriel retorna separadamente | síntese editorial pós-`Roteiro` | não fixar data precisa sem fonte adicional; requer reconstrução própria |
| P1-R12 | após 25/04/1499 | baixos do Rio Grande | fim de ago./set. 1499 | São Thiago → Terceira → Lisboa, Vasco da Gama | Vasco da Gama teria seguido via São Thiago, fretado caravela para levar Paulo da Gama a Terceira; Paulo morre após desembarque | separação de comando e troca de embarcação | síntese editorial; Ravenstein registra datas divergentes para a chegada de Vasco a Lisboa: 29/08, 08/09, 18/09, além de formulações mais vagas | manter explicitamente uma faixa/incerteza, não escolher uma data única para a campanha sem novo gate |

## Achados que já alteram o desenho pós-MVP

### 1. O retorno não é a ida invertida

A sequência material é assimétrica. Na volta aparecem:

- permanência de carena em Anjediva;
- travessia do Índico muito mais longa e com mortalidade severa;
- retorno a Melinde por necessidade de recuperação;
- destruição deliberada do S. Rafael por falta de tripulação;
- passagem por Moçambique sem contato com a cidade;
- nova permanência forte em São Brás;
- separação final das embarcações e trajetórias distintas até Portugal.

Portanto, reutilizar simplesmente as mesmas pernas e paradas da ida produziria uma reconstrução historicamente falsa.

### 2. A redução da frota é um fato de campanha, não ainda uma mecânica genérica

O S. Rafael é queimado em 13/01/1499 nos baixos que já levavam seu nome, porque o número de homens remanescentes não permitia navegar três navios. A carga é transferida aos dois restantes. Isso pode ser representado como evento histórico específico de `EXP_GAMA_1497`, sem exigir desde já um sistema universal de frota, tripulação e abandono de navios.

### 3. Doença e mortalidade são essenciais à narrativa, mas ainda não ao domínio

A travessia Anjediva–África Oriental contém o caso mais forte encontrado até aqui de degradação humana: trinta mortes na travessia e somente sete ou oito homens aptos a trabalhar em cada navio. O dado é historicamente central, mas introduzir doença, tripulação individual ou mortalidade como sistema antes de um modelo próprio violaria a disciplina metodológica do projeto. P1 registra a evidência; não implementa a mecânica.

### 4. A fonte muda de natureza em 25/04/1499

Até os baixos do Rio Grande, o itinerário deriva do corpo do `Roteiro`. Depois disso, o manuscrito cessa e Ravenstein passa a resumir outros autores. A futura base precisa guardar essa quebra de proveniência, por exemplo por `source_layer = PRIMARY_NARRATIVE` versus `EDITORIAL_SYNTHESIS`.

## Proposta de segmentação operacional — apenas para teste documental

Ainda não deve ser convertida em `expedition_routes.csv`. A hipótese mínima de trabalho é:

`CAL → SMI → ANJ → MAL → BSR → SJO → SBR → CGH → RGR`

onde:

- `SMI` = ilhas de Santa Maria, candidato fraco: marco de passagem/padrão;
- `ANJ` = Anjediva, candidato forte: água, madeira, alimento e carena;
- `MAL` = Melinde, já existente e fortemente documentado;
- `BSR` = Baixos de São Rafael, candidato forte como nó-evento/logístico específico da campanha;
- `SJO` = ilha de São Jorge, candidato fraco: parada ritual muito curta;
- `SBR` = São Brás, já existente e fortemente documentado;
- `CGH` = Cabo da Boa Esperança, marco náutico já existente;
- `RGR` = baixos do Rio Grande, candidato a marco náutico de confiança ainda a determinar.

Mogadíscio, Pate, Mombaça e Zanzibar aparecem no retorno, mas a leitura inicial não justifica promovê-los automaticamente a escalas operacionais nessa trajetória.

## Lacunas para o próximo subgate

1. Conferir, em fonte secundária de alta qualidade, a identificação moderna e a confiança cartográfica de Santa Maria, Anjediva, Baixos de São Rafael, São Jorge e Rio Grande.
2. Conferir a cronologia pós-25/04/1499 em Barros, Goes, Castanheda, Resende e/ou síntese moderna que cite explicitamente essas tradições.
3. Verificar se a partida efetiva após o retorno forçado a São Brás em 12/03 pode ser datada sem inferência.
4. Separar mortalidade total da viagem de mortalidade especificamente atribuível à travessia de retorno, sem harmonizar silenciosamente os números divergentes das fontes.
5. Verificar se existe documentação suficiente para representar aquisição de alimentos em Anjediva, Melinde, Baixos de São Rafael e São Brás como atividades distintas, sem converter o registro histórico em uma disponibilidade portuária genérica.
6. Só depois disso propor linhas novas para `nodes.csv`, `routes.csv`, `expedition_routes.csv` e `expedition_stops.csv`.

## Gate de saída documental P1.1

Este subgate pode ser considerado concluído quando:

- cada perna do retorno até 25/04 estiver associada a fonte e estatuto de evidência;
- o trecho pós-25/04 estiver explicitamente separado da narrativa primária;
- os cinco candidatos cartográficos novos estiverem classificados por confiança;
- as paradas logísticas estiverem separadas de simples passagens;
- nenhuma data editorial tiver sido convertida silenciosamente em fato primário;
- houver proposta de segmentação operacional pronta para revisão antes de alterar dados executáveis.
