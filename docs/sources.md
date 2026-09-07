# Corpus histórico inicial

Este arquivo registra o corpus de partida usado para estruturar a base histórica. Ele não substitui referências bibliográficas completas em futuras fichas de evidência.

## IDs de fonte

Os arquivos de dados usam IDs estáveis de proveniência. Quando uma linha depende de mais de uma obra, os IDs são separados por `|`.

| source_id | Referência curta | Uso principal |
|---|---|---|
| `ROTEIRO_GAMA_1497` | *Roteiro da primeira viagem de Vasco da Gama à Índia*, relato de participante da expedição; edição/tradução de E. G. Ravenstein, Hakluyt Society, 1898 | itinerário 1497–1499, escalas, abastecimento, reparos, encontros e cronologia fina |
| `CAMINHA_1500_ANTT` | Pêro Vaz de Caminha, carta a D. Manuel I, Porto Seguro/Vera Cruz, 1 de maio de 1500; ANTT, PT/TT/GAV/8/2/8, transcrição paleográfica e contemporânea | cronologia testemunhal da armada de Cabral entre Lisboa e Vera Cruz, desaparecimento de Vasco de Ataíde, sinais/avistamento de terra, contactos e permanência até a véspera da retomada da viagem |
| `NEWITT_PEW` | Malyn Newitt, *Portugal in European and World History* | expansão atlântica, ilhas, África Ocidental, Mina, Kongo e Cabo |
| `NEWITT_WA` | Malyn Newitt, *The Portuguese in West Africa, 1415–1670: A Documentary History* | África Ocidental e fontes documentais |
| `VILASANTA_KE` | Nuno Vila-Santa, *Knowledge Exchanges Between Portugal and Europe* | pilotos, cartografia, circulação e proteção do conhecimento náutico |
| `NEWITT_ZAMBEZI` | M. D. D. Newitt, *Portuguese Settlement on the Zambesi* | contexto da África Oriental; uso cronológico cauteloso |
| `PRAKASH_ECE` | Om Prakash, *European Commercial Enterprise in Pre-Colonial India* | comércio da Índia, mercadorias, portos e redes intra-asiáticas |
| `SUBRAHMANYAM_PEA` | Sanjay Subrahmanyam, *The Portuguese Empire in Asia, 1500–1700* | primeiras expedições, política, instituições e redes portuguesas na Ásia |
| `ALPERS_IOWH` | Edward A. Alpers, *The Indian Ocean in World History* | monções, costa suaíli, portos e geografia social do Índico |
| `IOH_PEARSON` | *Indian Ocean Histories: The Many Worlds of Michael Naylor Pearson* | enquadramento comparativo e oceânico |
| `OLIVEIRA_COSTA_CABRAL_1500` | João Paulo Oliveira e Costa, cronologia da Armada da Índia de 1500 em *Descobridores do Brasil. Exploradores do Atlântico e Construtores do Estado da Índia*; reprodução EVE/FCSH | cronologia Cabral 1500–1501, composição e fragmentação da armada, perdas, chegada e permanência no Malabar e retorno |
| `EVE_COCHIN` | José Luís Ferreira, “Cochim”, Enciclopédia Virtual da Expansão Portuguesa, FCSH, 2009 | Cochim 1500–1503, feitoria, carregamento de pimenta, contexto político e comunidades locais |
| `HPIP_COCHIN` | entrada Kochi/Cochim/Santa Cruz de Cochim, Heritage of Portuguese Influence / Património de Influência Portuguesa | âncora cartográfica e morfologia urbana-portuária histórica de Cochim |
| `CANAVARRO_GGB_2000` | Ana Rita Canavarro, “Gonçalo Gil Barbosa”, em *Descobridores do Brasil*, 2000 | primeiro feitor de Cochim e sucessão Barbosa–Diogo Fernandes Correia |

## Expansão atlântica portuguesa

- *Roteiro da primeira viagem de Vasco da Gama à Índia* — fonte primária para o itinerário de 1497–1499; a edição Ravenstein explicita que palavras e datas ausentes do manuscrito foram colocadas entre colchetes, distinção que deve ser preservada nas notas de evidência.
- Pêro Vaz de Caminha, carta de 1 de maio de 1500 — fonte primária para a cronologia atlântica inicial de Cabral; usar a transcrição do Arquivo Nacional da Torre do Tombo e dar precedência às datas explícitas do documento quando divergirem de sínteses posteriores.
- Malyn Newitt, *Portugal in European and World History*.
- Malyn Newitt, *The Portuguese in West Africa, 1415–1670: A Documentary History*.
- Nuno Vila-Santa, *Knowledge Exchanges Between Portugal and Europe*.
- M. D. D. Newitt, *Portuguese Settlement on the Zambesi* — usado apenas quando pertinente e com cuidado cronológico.

## Oceano Índico e comércio asiático

- Om Prakash, *European Commercial Enterprise in Pre-Colonial India*.
- Sanjay Subrahmanyam, *The Portuguese Empire in Asia, 1500–1700*.
- Edward A. Alpers, *The Indian Ocean in World History*.
- *Indian Ocean Histories: The Many Worlds of Michael Naylor Pearson* — enquadramento comparativo e oceânico.
- João Paulo Oliveira e Costa, cronologia da Armada da Índia de 1500, para a sequência documental Cabral–Cochim.
- José Luís Ferreira, “Cochim”, EVE/FCSH, para o porto, feitoria inicial e contexto local.
- HPIP, entrada Kochi/Cochim, para a âncora cartográfica e a leitura da paisagem estuarina histórica.

## Regras de uso

1. Evidência do século XVII não deve ser retroprojetada para 1497–1500 sem marcação explícita como analogia posterior.
2. Sínteses modernas podem estruturar a base; eventos, diálogos e detalhes finos devem preferencialmente ser conferidos em fontes primárias ou estudos especializados.
3. Divergências cronológicas entre autores devem ser registradas em vez de harmonizadas silenciosamente.
4. Toda associação entre porto e mercadoria deve distinguir produção de simples circulação.
5. Coordenadas em `nodes.csv` são âncoras cartográficas modernas. Elas não afirmam a posição exata do cais ou assentamento no século XV.
6. Datas entre colchetes na edição Ravenstein do `Roteiro` são reconstruções editoriais e devem ser identificadas como tal; não recebem automaticamente o mesmo grau de evidência de uma data explícita no manuscrito.
7. Para Cochim, a instalação inicial de agentes portugueses sob Cabral em 1500–1501 e a reorganização/substituição do feitor por Vasco da Gama em 1502 permanecem distinguidas; a formulação divergente de Subrahmanyam sobre a feitoria em 1502 é preservada na documentação do P2.
8. Para Cabral, datas explícitas da Carta de Caminha prevalecem sobre datas divergentes em sínteses: sinais de terra em 21/04/1500 e avistamento em 22/04/1500 devem ser preservados como cronologia testemunhal.

## Lacunas prioritárias

- georreferenciamento histórico de Mpinda/Soyo;
- cesta comercial específica de Cabo Verde em 1497;
- cesta comercial de Mombasa e Malindi no final do século XV;
- documentação fina de Arguim e das redes saarianas;
- cronologia e situação de São Tomé entre 1493 e 1500;
- refinamento espacial do Rio do Cobre/Terra da Boa Gente, cuja identificação moderna permanece discutida;
- preços e unidades históricas: somente após consolidar circuitos e conversões documentais;
- identidade nominal `Diogo Dias` × `Pêro Dias` na armada de 1500, antes de normalização de pessoa/embarcação;
- cronologia fina das chegadas ao reino em 1501, necessária para controlar quando informações de Cabral se tornam disponíveis às campanhas seguintes.
