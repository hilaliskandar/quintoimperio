# P3 — inventário documental preliminar das expedições 1500–1505

Data: 2026-09-07
Issue-mãe: #110
Status: inventário v0.1; ainda não autoriza alterações em `data/` ou código jogável.

## Objetivo

Estabelecer a sequência mínima de expedições/armadas que precisa ser auditada antes de propor P3-func. Este arquivo registra apenas fatos iniciais de alta ou média confiança e as principais lacunas; composição detalhada, rotas finas, perdas e efeitos institucionais serão tratados em subgates.

## Sequência preliminar

| Ano | Expedição/comando | Evidência inicial | Relevância para o loop | Status |
|---|---|---|---|---|
| 1500–1501 | Armada de Pedro Álvares Cabral | EVE/FCSH; corpus P2 | ruptura em Calecute, deslocamento comercial para Cochim/Cananor, primeira presença portuguesa residente em Cochim | AUDITAR EM DETALHE |
| 1501–1502 | Armada de João da Nova | Ministério da Defesa/CPHM; corpus de síntese | expedição pequena predominantemente comercial; Cochim e Cananor como pontos de carregamento; necessidade de distinguir informação recebida em viagem da intenção original | AUDITAR EM DETALHE |
| 1502–1503 | Segunda viagem de Vasco da Gama | E-Dicionário de Escrita de Viagens Portuguesa; Subrahmanyam | grande armada, coerção marítima, negociação em Cananor/Cochim e reorganização de feitorias | AUDITAR EM DETALHE |
| 1503–1504 | Esquadras de Afonso e Francisco de Albuquerque; esquadra de António de Saldanha | EVE/FCSH; Revista da Armada | recuperação de Cochim, fortificação/guarnição e múltiplas trajetórias; forte risco de exigir segmentação por esquadra | AUDITAR EM DETALHE |
| 1504–1505 | Armada de Lopo Soares de Albergaria | RTP Ensina; Revista da Armada | reforço militar de Cochim/Cananor, operações contra Calecute e integração de forças remanescentes de 1503 | AUDITAR EM DETALHE |
| 1505 | Armada de D. Francisco de Almeida | História da Marinha Portuguesa; sínteses institucionais | mudança institucional de escala: vice-reinado, fortalezas e presença permanente; provável limite superior natural do primeiro P3 | AUDITAR EM DETALHE |

## Evidência inicial por expedição

### 1500 — Cabral

A Enciclopédia Virtual da Expansão Portuguesa registra armada de 13 navios, chegada a Calecute em 1500, ruptura após ataque à feitoria e deslocamento para Cochim. A armada chegou a Cochim em 24/12/1500; o carregamento ocorreu em cerca de duas semanas e foram deixados agentes portugueses, entre eles Gonçalo Gil Barbosa como feitor. O retorno iniciou-se após passagem por Cananor em janeiro de 1501.

Implicação metodológica: Cabral é a primeira candidata a nova campanha, mas sua integração não deve começar por combate. Primeiro é necessário reconstruir a sequência operacional Lisboa → Brasil → Cabo/África Oriental → Calecute → Cochim → Cananor → retorno e identificar quais eventos realmente alteram estado do jogador.

### 1501 — João da Nova

Fonte institucional do Ministério da Defesa caracteriza a terceira armada como quatro naus, com finalidade predominantemente comercial. A armada partiu sem conhecimento pleno da ruptura ocorrida sob Cabral; em São Brás recebeu informação deixada pela armada anterior e seguiu para Cochim/Cananor, evitando Calecute.

Implicação metodológica: esta expedição é especialmente útil para testar persistência de informação entre campanhas. Antes de criar sistema novo de mensagens, deve-se verificar se o estado atual de conhecimento/information_history já consegue representar informação herdada de uma expedição anterior.

### 1502 — Vasco da Gama

A segunda viagem de Vasco da Gama partiu em fevereiro de 1502 com grande força naval. Fontes de síntese registram negociação com Cananor e Cochim e reorganização de feitorias, além de ações coercitivas no mar.

Implicação metodológica: separar duas perguntas: (1) o que a campanha precisa representar para comércio/acesso; (2) quais episódios violentos são indispensáveis ao estado da campanha. Não abrir sistema geral de combate até demonstrar que uma representação por eventos específicos é insuficiente.

### 1503 — Afonso/Francisco de Albuquerque e António de Saldanha

A EVE lista múltiplos capitães e partidas em abril de 1503. A documentação disponível indica que as forças não formam uma trajetória única simples: há esquadras separadas, atrasos e junções posteriores. Afonso/Francisco de Albuquerque participaram da recuperação de Cochim e da implantação de fortificação/guarnição; António de Saldanha seguiu trajetória própria na África Oriental e entrada do Mar Vermelho.

Implicação metodológica: provável necessidade de modelo de `expedition_group`/subexpedições ou de múltiplas expedições coordenadas, mas isso ainda é hipótese de arquitetura. Primeiro é preciso reconstruir cronologia e dependências.

### 1504 — Lopo Soares

A armada de 1504 foi organizada em resposta às informações trazidas pela expedição de 1502 e reforçou a posição portuguesa no Malabar. A documentação institucional também registra integração de forças remanescentes de 1503.

Implicação metodológica: esta armada pode testar continuidade institucional e estado persistente entre campanhas; não deve ser tratada apenas como repetição de uma viagem Lisboa–Índia.

### 1505 — Francisco de Almeida

A expedição de 1505 marca mudança de escala institucional, com D. Francisco de Almeida como primeiro vice-rei e instruções para criar/reforçar posições fortificadas e presença permanente. Fontes da história naval portuguesa também registram transporte de componentes de embarcações para montagem no Oriente.

Implicação metodológica: 1505 deve ser tratado como possível fronteira de fase, não automaticamente como mais uma campanha do mesmo tipo. O gate P3 precisa decidir se termina com a chegada de Almeida ou se incorpora a primeira institucionalização permanente como epílogo/estado de transição.

## Questões a abrir como subgates

1. P3.1 — Cabral 1500–1501: cronologia, composição, perdas, escalas e ruptura Calecute–Cochim.
2. P3.2 — João da Nova 1501–1502: rota, caráter comercial e transmissão de informação da armada anterior.
3. P3.3 — Gama 1502–1503: segmentação de frota, coerção marítima, Cananor/Cochim e feitorias.
4. P3.4 — 1503: múltiplas esquadras, Albuquerque/Saldanha, Cochim e fortificação.
5. P3.5 — 1504: Lopo Soares e consolidação militar/comercial.
6. P3.6 — 1505: Almeida e transição de expedições anuais para estrutura político-militar permanente.
7. P3.CART — cartografia dos novos nós/rotas somente depois de cada cronologia estar estabilizada.
8. P3.ARCH — auditoria de arquitetura somente depois das matrizes documentais, para decidir se eventos específicos bastam ou se é necessário generalizar frota/subexpedições.

## Fontes iniciais já localizadas

- Sanjay Subrahmanyam, *The Portuguese Empire in Asia, 1500–1700* — arquivo completo no Drive do projeto.
- Om Prakash, *European Commercial Enterprise in Pre-Colonial India* — arquivo completo no Drive.
- Francisco Bethencourt e Diogo Ramada Curto, *A Expansão Marítima Portuguesa, 1400–1800* — arquivo e fichamento no Drive.
- Enciclopédia Virtual da Expansão Portuguesa/FCSH — entradas de Armada da Índia de 1500, armadas manuelinas, Cochim, Cananor e biografias associadas.
- Ministério da Defesa/Comissão Portuguesa de História Militar — síntese sobre as primeiras armadas e a evolução militar no Índico.
- Revista da Armada / Marinha Portuguesa — série histórica sobre armadas manuelinas e documentação técnica/naval.
- RTP Ensina — síntese biográfica de Lopo Soares de Albergaria.
- História da Marinha Portuguesa — documentação sobre 1502 e 1505, inclusive montagem de embarcações no Oriente.

## Regras para o próximo passo

- não normalizar navio/capitão individual enquanto a matriz de cada armada não estiver estabilizada;
- não transformar todos os conflitos em sistema de combate;
- não projetar instituições de 1505 para 1500–1502;
- não usar números de frota de uma síntese única quando houver divergência entre fontes;
- não introduzir novas rotas apenas porque aparecem em mapas modernos;
- sempre separar percurso português efetivo de rede comercial preexistente;
- preservar P1 e P2 como regressão obrigatória.

## Próxima ação

Executar P3.1 — Cabral 1500–1501 — como primeiro subgate documental, porque já há corpus forte e porque essa expedição conecta diretamente o baseline atual de Calecute/Cochim à expansão subsequente.