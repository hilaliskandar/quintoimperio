# P2-doc — auditoria do rajá e da relação Cochim–Calecute, 1500–1503

Issue: #105.

Data: 2026-09-07.

## Problema

A documentação inicial sustenta claramente a existência de uma autoridade régia/local em Cochim com a qual Cabral negociou em dezembro de 1500. O problema não é a existência do ator, mas a forma segura de nomeá-lo e de representar a relação política entre o Perumpadappu Swarupam/Cochim e o Samudri de Calecute.

## Titulatura portuguesa: Trimumpara

Fontes portuguesas e sínteses derivadas usam `Trimumpara` para o rei de Cochim. A tradição historiográfica e genealógica de Cochim associa essa forma a `Thirumalpad`/`Tirumulpadu`, isto é, a uma titulatura ligada ao governante, e não a um nome pessoal autônomo.

Consequência metodológica: `Trimumpara` não deve virar um `actor_id` pessoal como se fosse nome próprio. É mais seguro tratá-lo como forma portuguesa de título.

## Variantes do nome pessoal

Foram encontradas duas tradições concorrentes para o governante recebido por Cabral:

### Tradição A — Unni Goda Varma

A história da família real de Cochim identifica o governante de 1500 como `Unni Goda Varma Koil Thirumalpad`, da Elaya Thavazhi do Perumpadappu Swaroopam, e associa explicitamente `Trimumpara` à forma portuguesa de `Thirumalpad`.

A síntese patrimonial Sahapedia também identifica `King Unni Goda Varma Tirumulpadu` como o governante que apoiou os portugueses contra o Samudri após o tratado de 1500.

### Tradição B — Unni Rama/Raman Koil I

Fontes oficiais contemporâneas de divulgação histórica de Kerala, inclusive Kerala Tourism e material do Department of Archaeology, usam `Unni Rama Koil I`/`Raman Koil I` para o governante associado à chegada portuguesa, distinguindo-o de `Unni Rama Koil II`, ligado ao ciclo posterior de 1505.

### Decisão

Nesta fase, não existe base suficiente para demonstrar que `Unni Goda Varma` e `Unni Rama Koil I` são simples variantes do mesmo nome, nem para escolher uma delas como única forma historicamente segura.

Portanto:

- o futuro ator deve ser normalizado inicialmente pelo **papel documentado**, não por nome pessoal;
- rótulo de trabalho recomendado: `Rajá de Cochim / Trimumpara (Thirumalpad), c. 1500`;
- um eventual `actor_id` deve ser neutro, por exemplo `ACT_COCHIN_RAJA_1500`, sem codificar `GODA` ou `RAMA`;
- as variantes `Unni Goda Varma Koil Thirumalpad` e `Unni Rama/Raman Koil I` devem constar de nota de evidência com status `UNRESOLVED_NAME_VARIANT`;
- a identidade pessoal não deve ser apresentada ao jogador como fato fechado até existir fonte genealógica/especializada suficiente para resolver a equivalência ou sucessão.

## Estrutura política: Perumpadappu Swarupam

Há convergência suficiente para tratar Cochim como centro do `Perumpadappu Swarupam`, uma formação política local anterior à presença portuguesa.

Não se deve modelar Cochim como criação política portuguesa, nem como simples distrito de Calecute.

## Relação com Calecute

O corpus usa termos variados: `dependent raja`, vassalagem, hegemonia, suzerania e dependência tributária. A literatura regional descreve uma trajetória em que a expansão do Samudri reduziu direitos e autonomia dos governantes de Cochim e explorou divisões entre os ramos (`thavazhi`) do Perumpadappu Swarupam.

Algumas reconstruções atribuem à subordinação anterior à chegada portuguesa:

- tributo anual ao Samudri;
- obrigação de fornecer contingentes;
- interferência do Samudri nas disputas sucessórias;
- restrições favoráveis a Calecute na circulação/comercialização de pimenta.

Esses elementos são úteis para caracterizar a assimetria, mas não devem ser comprimidos em uma noção moderna de soberania territorial integral.

### Formulação recomendada

Para o recorte de 1500, a relação deve ser descrita como:

> **polidade local autônoma em assuntos internos, porém politicamente subordinada à hegemonia/suzerania do Samudri de Calecute, com obrigações tributárias e forte interferência externa, em tensão com essa dependência.**

A aliança com Cabral deve ser entendida como tentativa de ampliar a margem de autonomia de Cochim e alterar a correlação regional, não como transferência imediata de soberania para Portugal.

## Mudança 1500–1503

A relação não é estática:

- 1500: Cabral encontra uma autoridade local disposta a cooperar contra a hegemonia de Calecute;
- 1501–1502: a presença da feitoria e a reafirmação dos acordos aprofundam a ligação portuguesa;
- 1503: a ofensiva do Samudri contra Cochim e a intervenção portuguesa transformam o conflito em confronto militar aberto; fortificação e guarnição são estágio posterior.

Logo, um único campo estático de `political_status` pode ser insuficiente para todo o período 1500–1505. O P2-func deverá decidir se usa status temporalmente delimitados ou se mantém o nó com status local e projeta a mudança pelos eventos/atores.

## Decisão documental

Para a futura proposta mínima de normalização:

- `polity`: `Perumpadappu Swarupam / Cochim`;
- autoridade local: sim, documentada;
- actor label inicial: `Rajá de Cochim / Trimumpara (Thirumalpad)`;
- nome pessoal: **não fechado**;
- relação com Calecute: `SUBORDINATE_HEGEMONIC_RELATION` em descrição conceitual, sem assumir enum de domínio ainda;
- relação com Portugal em dezembro de 1500: `FOREIGN_NEGOTIATED`/aliança comercial-política como hipótese de futura projeção, sem converter Cochim em posse portuguesa;
- fortificação/presença militar portuguesa: somente a partir do ciclo de 1503, fora do estado inicial de dezembro de 1500.

## Fontes utilizadas

- Om Prakash, `PRAKASH_ECE`: referência ao `dependent raja of Cochin` e aos limites do seu controle sobre o hinterland da pimenta.
- EVE/FCSH: verbetes “Cochim” e “Armada da Índia de 1500”.
- Sahapedia, história do Perumpadappu Swarupam/Cochin Royal Family.
- Cochin Royal Family historical project: tradição genealógica `Unni Goda Varma Koil Thirumalpad` e interpretação de `Trimumpara`.
- Kerala Tourism / Kerala Department of Archaeology: tradição `Unni Rama/Raman Koil I` para o governante da fase inicial portuguesa.
- literatura regional sobre os Zamorins e o Perumpadappu Swarupam, usada para caracterizar a relação de hegemonia/suzerania, sem adotar automaticamente toda a sua terminologia como fato jurídico preciso.

## Gate

A #105 pode ser encerrada metodologicamente: o ator político e a relação regional podem ser modelados sem resolver artificialmente a variante do nome pessoal. A incerteza onomástica deve continuar explícita em nota de evidência e não bloquear o restante da matriz P2-doc.
