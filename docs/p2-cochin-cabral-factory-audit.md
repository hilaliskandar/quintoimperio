# P2-doc — auditoria Cabral–feitoria de Cochim, 1500–1502

Issue: #104.

Data: 2026-09-07.

## Pergunta

Quando começa a presença institucional portuguesa em Cochim e como deve ser interpretada a formulação de que Vasco da Gama teria estabelecido a feitoria em 1502?

## Hierarquia de evidência

### 1. Reconstrução de João Paulo Oliveira e Costa para a armada de 1500

A entrada “Armada da Índia de 1500”, da Enciclopédia Virtual da Expansão Portuguesa/FCSH, reproduz a introdução de *Descobridores do Brasil. Exploradores do Atlântico e Construtores do Estado da Índia* (2000). O autor declara que a cronologia é construída prioritariamente com documentos produzidos pelos próprios protagonistas e testemunhas oculares, evitando harmonizar silenciosamente crónicas posteriores contraditórias.

Para Cochim, a sequência reconstruída é precisa:

- 24/12/1500: a armada de Cabral chega a Cochim;
- recebe excelente acolhimento e carrega especiarias durante aproximadamente 12–15 dias;
- Cabral decide deixar sete homens, com Gonçalo Gil Barbosa como feitor;
- são nomeados também os escrivães Lourenço Moreno e Sebastião Álvares e o intérprete Gonçalo Madeira de Tânger, além de degredados entre os que ficaram;
- 09/01/1501: ao sair para enfrentar uma esquadra de Calecute, a armada não regressa ao porto;
- 15/01/1501: já em Cananor, Cabral escreve ao rei de Cochim e a Gonçalo Gil Barbosa para explicar a saída súbita;
- 16/01/1501: inicia o regresso.

Essa reconstrução oferece evidência forte de que havia um responsável mercantil português residente em Cochim desde janeiro de 1501 e que a sua permanência não é uma projeção retrospectiva de 1502.

### 2. Gonçalo Gil Barbosa na EVE/FCSH

O verbete biográfico “Gonçalo Gil Barbosa” explicita que, depois das mortes dos principais oficiais da feitoria de Calecute, Barbosa ganhou precedência; em Cochim, participou das negociações e foi nomeado feitor da primeira feitoria portuguesa ali aberta. O verbete afirma ainda que ocupou o cargo por cerca de dois anos.

Quando Vasco da Gama regressou à Índia em 1502, levava instruções para substituir Gonçalo Gil Barbosa por Diogo Fernandes Correia em Cochim e transferir Barbosa para a nova feitoria de Cananor.

A sequência é internamente coerente com a cronologia da armada de 1500: Barbosa não surge como feitor apenas em 1502; em 1502 ocorre uma substituição institucional.

### 3. Carta régia de 1502 aos reis de Cochim e Cananor

A documentação publicada das missões do Padroado conserva uma carta de D. Manuel de 1502 dirigida aos reis de Cochim e Cananor. O texto recorda que o capitão-mor e os capitães da armada anterior haviam informado a Coroa sobre a boa recepção e sobre o estabelecimento de paz, trato e resgate, além do carregamento das naus.

A carta não basta, isoladamente, para nomear o primeiro feitor, mas confirma que o vínculo político-comercial com Cochim já estava estabelecido antes da segunda viagem de Vasco da Gama.

### 4. Confirmação especializada posterior

O estudo publicado nos *Anais de História de Além-Mar* sobre a última carta de Francisco de Albuquerque, ao discutir Gonçalo Gil Barbosa, remete expressamente a Ana Rita Canavarro, “Gonçalo Gil Barbosa”, em *Descobridores do Brasil* (2000), e afirma que ele havia sido feitor em Cochim, sendo substituído em 1502 por Diogo Fernandes Correia e transferido então para Cananor.

Essa referência especializada reforça que a leitura Barbosa→Correia é uma sucessão de feitores, e não a criação ex novo da instituição em 1502.

## A divergência com Subrahmanyam

`SUBRAHMANYAM_PEA`, cap. 3, formula que “The Cochin factory was set up by Vasco da Gama on his second voyage to Asia in 1502” e identifica Diogo Fernandes Correia como primeiro feitor.

Essa formulação deve permanecer registrada como divergência bibliográfica. Contudo, tomada literalmente como data da primeira instalação portuguesa e do primeiro feitor, ela entra em tensão com uma reconstrução documental mais granular da armada de Cabral e com estudos especializados sobre Gonçalo Gil Barbosa.

Não é metodologicamente adequado apagar a formulação de Subrahmanyam ou qualificá-la simplesmente como erro. A hipótese mais conservadora é que a síntese esteja tratando 1502 como momento de formalização, reafirmação ou reorganização da feitoria sob instruções régias mais estáveis. O corpus consultado nesta auditoria, porém, não demonstra diretamente que essa seja a intenção específica do autor; portanto essa interpretação deve permanecer rotulada como hipótese explicativa.

## Decisão documental para P2

Para a base histórica futura, quando P2-doc for fechado:

1. **primeira presença mercantil portuguesa residente em Cochim:** documentável a partir da passagem de Cabral, dezembro de 1500/janeiro de 1501;
2. **primeiro feitor de trabalho:** Gonçalo Gil Barbosa, confiança `HIGH` para o recorte da armada de 1500;
3. **substituição por Diogo Fernandes Correia:** 1502, associada à segunda viagem de Vasco da Gama, confiança `HIGH`;
4. **“fundação da feitoria em 1502”:** não usar como único marco de início; preservar em nota como formulação de `SUBRAHMANYAM_PEA` e possível marco de reorganização/formalização;
5. **nenhuma implicação automática de soberania portuguesa:** a presença de feitor/feitoria é comercial e negociada no território de uma autoridade local; não autoriza `PORTUGUESE_POSSESSION` nem `ROYAL_FACTORY` sem semântica cuidadosamente definida para o período.

## Consequência para a matriz v0.1

A linha que dizia apenas que Subrahmanyam situava a instalação da feitoria em 1502 deve ser refinada. O gate passa a distinguir:

- `1500-12/1501-01`: instalação inicial/residência de feitor sob Cabral;
- `1502`: reafirmação dos acordos por Gama e substituição de Barbosa por Diogo Fernandes Correia;
- `1503+`: fortificação e presença militar, que pertencem a estágio institucional posterior e não devem retroagir para 1500.

## Limites remanescentes

- ainda falta identificar, se necessário, a peça primária específica que nomeia Gonçalo Gil Barbosa no ato de permanência em Cochim; a reconstrução de Oliveira e Costa declara basear-se em documentos contemporâneos e fornece suporte crítico em obra especializada, mas esse documento individual não foi transcrito diretamente nesta auditoria;
- não se normaliza ainda pessoal auxiliar como atores jogáveis;
- não se normaliza o estatuto político da feitoria até a conclusão da #105.

## Fontes de controle

- João Paulo Oliveira e Costa, “Armada da Índia de 1500”, EVE/FCSH, derivado de *Descobridores do Brasil. Exploradores do Atlântico e Construtores do Estado da Índia* (2000).
- verbete “Gonçalo Gil Barbosa”, EVE/FCSH.
- *Documentação para a história das Missões do Padroado Português do Oriente: Índia*, vol. I, carta de D. Manuel aos reis de Cochim e Cananor, 1502.
- Ana Rita Canavarro, “Gonçalo Gil Barbosa”, em *Descobridores do Brasil* (2000), confirmada por referência especializada em estudo dos *Anais de História de Além-Mar*.
- Sanjay Subrahmanyam, *The Portuguese Empire in Asia, 1500–1700*, 2ª ed., cap. 3.

## Gate

A #104 pode ser encerrada como resolvida para fins de modelagem mínima, preservando explicitamente a divergência de formulação de Subrahmanyam. A próxima dependência crítica continua sendo #105: identidade/titulatura do rajá e natureza da relação política Cochim–Calecute.
