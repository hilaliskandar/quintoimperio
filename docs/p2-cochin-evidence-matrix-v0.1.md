# P2-doc — matriz de evidências de Cochim v0.1

Issue: #103.

Data: 2026-09-07.

Status: leitura inicial do corpus já incorporado. Nenhuma linha desta matriz autoriza ainda alteração em `data/` ou no domínio jogável.

## Regra temporal

O gate distingue pelo menos três estratos:

1. **c. 1500** — estrutura portuária do Malabar e deslocamento de Cabral após a ruptura em Calecute;
2. **1502–1505** — instalação portuguesa mais estável, segunda viagem de Gama e fase anterior ao vice-reinado;
3. **1510 em diante** — dados quantitativos e institucionais posteriores, úteis para trajetória histórica mas não retroprojetáveis automaticamente para 1500–1502.

Informação posterior deve permanecer marcada como tal, mesmo quando ajuda a explicar a ascensão de Cochim.

## Matriz inicial

| Tema | Evidência inicial | Recorte | Força | Fonte | Implicação provisória | Limite |
|---|---|---:|---|---|---|---|
| posição relativa no Malabar | Calecute é descrita como principal porto; Cannanore, Cochim e Kollam aparecem como portos menores | c. 1500 | A | `PRAKASH_ECE`, cap. 1 | Cochim pode ser tratado como porto real da rede pré-portuguesa, mas não como equivalente funcional de Calecute | ainda falta cesta portuária específica de c. 1500 |
| conectividade regional | a costa do Malabar se liga ao Mar Vermelho, Golfo Pérsico, Gujarat, Sri Lanka, litoral oriental da Índia e Malaca | c. 1500 | A regional | `PRAKASH_ECE`, cap. 1 | Cochim pertence a uma rede costeira e oceânica anterior à presença portuguesa | a fonte descreve a costa; não atribuir todas as conexões diretamente a Cochim sem evidência por porto |
| mudança portuguesa após Calecute | Cabral desloca-se para Cochim em dezembro de 1500 depois da destruição da feitoria portuguesa em Calecute e da abertura de hostilidades | dez. 1500 | A | `SUBRAHMANYAM_PEA`, cap. 3, p. 64 | evento forte para um futuro gate cronológico pós-MVP/P2 | requer reconstrução mais fina do itinerário e das ações de Cabral antes de virar rota jogável |
| papel inicial de Cochim | Subrahmanyam caracteriza o período até 1505 como fortemente centrado em Cochim e o porto como principal candidato a centro administrativo antes de Goa | 1500–1505 | A/B | `SUBRAHMANYAM_PEA`, cap. 3 | Cochim ganha importância portuguesa rapidamente após 1500 | não retroprojetar a centralidade administrativa de 1502–1505 para 1498 |
| feitoria portuguesa | Subrahmanyam situa a instalação da feitoria de Cochim na segunda viagem de Vasco da Gama e identifica Diogo Fernandes Correia como primeiro feitor | 1502 | A | `SUBRAHMANYAM_PEA`, cap. 3, p. 64 | existe marco cronológico específico para presença institucional portuguesa | conferir fonte primária/especializada antes de modelar estrutura, pessoal ou privilégios da feitoria |
| autoridade local | Prakash refere-se ao rajá de Cochim como dependente e cooperante com os portugueses na política de aquisição de pimenta | início séc. XVI | B | `PRAKASH_ECE`, cap. 2 | há base para pesquisar um ator político local separado de Calecute | o trecho sintetiza processo de início do século; nome, titulatura, dependência e situação exata em 1500 requerem fonte especializada |
| intermediação mercantil | Prakash registra uso de mercadores Mappila e cristãos sírios como brokers/intermediários em Cochim | início séc. XVI | B | `PRAKASH_ECE`, cap. 2 | candidatos a comunidades/atores distintos, não uma categoria genérica de “mercadores” | não normalizar atores em 1500 antes de fixar cronologia e evidência mais direta |
| pimenta | a mudança do centro português de aquisição de pimenta para Cochim é associada à ruptura com Calecute | início séc. XVI | A/B | `PRAKASH_ECE`, cap. 2 | pimenta é candidata forte a mercadoria documentada no futuro nó de Cochim | não usar volumes/preços posteriores como valores de 1500 |
| hinterland da pimenta | o rajá não controlava efetivamente as áreas produtoras nem todas as rotas de transporte de pimenta | início séc. XVI | A/B | `PRAKASH_ECE`, cap. 2 | separar porto, autoridade política, produção e rotas de abastecimento; acesso ao porto não equivale a monopólio efetivo do hinterland | requer espacialização posterior das áreas produtoras somente se necessária ao jogo |
| apoio material/político | Prakash atribui ao rajá proteção a embarcações fluviais de pimenta, garantias de empréstimos e empréstimos próprios aos portugueses | início séc. XVI | B | `PRAKASH_ECE`, cap. 2 | evidencia cooperação concreta e potencial consequência relacional local | crédito não deve virar sistema genérico neste gate; cronologia específica precisa ser refinada |
| função comercial posterior | dados de 1510–1518 mostram forte peso da pimenta na feitoria e importação de metais europeus, especialmente cobre e prata/especie | 1510–1518 | A para o período | `PRAKASH_ECE`, cap. 2 | útil como trajetória e controle de plausibilidade | **não usar como cesta quantitativa ou preço de 1500–1502** |
| ascensão portuária | Prakash descreve ascensão de Cochim e declínio relativo de Calecute/Cannanore ao longo do século XVI, em grande medida associados à intervenção portuguesa | meados séc. XVI | A para processo posterior | `PRAKASH_ECE`, cap. 2 | P2 deve modelar Cochim como porto em transformação, não como entreposto já dominante em 1500 | não retroprojetar resultado de meados do século ao início do processo |

## Primeiras conclusões defensáveis

1. **Cochim existe como porto mercantil relevante antes da aliança portuguesa**, mas é secundário em relação a Calecute no quadro de c. 1500.
2. **Dezembro de 1500 é um turning point português**, quando Cabral se desloca para Cochim após a ruptura em Calecute.
3. A **presença institucional portuguesa mais estável deve ser datada com cuidado**: Subrahmanyam coloca a feitoria na segunda viagem de Gama, em 1502.
4. Pimenta é central para a relação luso-cochinense, porém **porto, produção e transporte não devem ser colapsados**. O rajá de Cochim não controlava automaticamente o hinterland produtor.
5. Há indícios de **pluralidade de intermediários**, incluindo Mappila e cristãos sírios, que justificam pesquisa específica antes de qualquer `actor_id`.
6. Os dados quantitativos de 1505/1510–1518 são importantes para a evolução posterior, mas não podem fornecer preços, volumes ou estoque inicial de 1500.

## Lacunas prioritárias antes de normalizar `COC`

### L1 — autoridade política de Cochim em 1500–1503

Identificar nome/titulatura do governante, natureza da relação com o Samudri de Calecute e alcance efetivo de sua autoridade. Evitar usar a categoria sintética “dependent raja” como modelo político suficiente.

### L2 — Cabral em Cochim, dezembro de 1500

Reconstruir chegada, negociação, permanência, comércio, presentes/garantias, eventual representação portuguesa e saída. Distinguir o que ocorreu em 1500 do que foi instituído em 1502.

### L3 — segunda viagem de Gama e feitoria, 1502

Confirmar cronologia, primeiro feitor, função inicial e condições políticas/comerciais da feitoria em fonte primária ou estudo especializado.

### L4 — cesta comercial de Cochim c. 1500

Separar mercadorias produzidas no hinterland, mercadorias transportadas ao porto e reexportações. Pimenta é confirmada como eixo, mas as demais mercadorias precisam de evidência contemporânea ao recorte.

### L5 — atores mercantis

Determinar se Mappila e cristãos sírios podem ser normalizados como comunidades historicamente atuantes em Cochim já no recorte 1500–1503, e com quais papéis.

### L6 — cartografia

Fixar âncora moderna de Kochi/Cochin e registrar limitações decorrentes das transformações costeiras/estuarinas. A coordenada moderna não deve afirmar a posição exata do porto de 1500.

## Fontes lidas nesta versão

- `SUBRAHMANYAM_PEA`: Sanjay Subrahmanyam, *The Portuguese Empire in Asia, 1500–1700*, 2ª ed., especialmente cap. 3, seção sobre as primeiras expedições.
- `PRAKASH_ECE`: Om Prakash, *European Commercial Enterprise in Pre-Colonial India*, especialmente caps. 1–2.

## Próximo subgate

Pesquisar L1–L3 primeiro, porque autoridade, cronologia de Cabral e instalação da feitoria condicionam qualquer decisão posterior sobre `node_type`, `political_status`, `access_regime`, atores e relações. Mercadorias e cartografia devem ser refinadas em seguida, sem alteração de `data/` antes do fechamento da matriz documental.
