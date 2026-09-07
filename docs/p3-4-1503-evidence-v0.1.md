# P3.4-doc — armadas de 1503, Cochim, fortificação e guarnição — matriz v0.1

Data: 2026-09-07
Issues: #110, #114

## Objetivo

Reconstruir o ciclo de 1503 no nível necessário para distinguir transformação territorial, presença institucional e episódios militares, sem implementar combate ou ocupação territorial como sistemas gerais.

## Fontes de trabalho

- EVE/FCSH, entrada `Cochim`;
- EVE/FCSH, `Duarte Pacheco Pereira`;
- EVE/FCSH, listagem das Armadas da Índia do reinado de D. Manuel I;
- EVE/FCSH, `Pedro de Ataíde`;
- HPIP, entrada `Kochi [Cochim/Cochin/Santa Cruz de Cochim]`;
- documentação P3.3 sobre a força de Vicente Sodré.

## Sequência operacional mínima

| Momento | Evento | Efeito documental | Grau |
|---|---|---|---|
| início de 1503 | força de Vicente Sodré permanece no Índico depois do regresso de Vasco da Gama | existência de força naval portuguesa separada da frota de retorno | A/B |
| 1503 | Sodré desloca sua força para operações de presa no Mar Vermelho | Cochim fica sem a proteção naval esperada | B |
| abril de 1503 | Samorim de Calecute lança ofensiva contra Cochim | ruptura do equilíbrio local e ocupação/invasão do reino aliado | A |
| abril de 1503 | portugueses e rajá de Cochim retiram-se para Vaipim | Cochim deixa temporariamente de estar sob controle do aliado local; Vaipim funciona como refúgio | A |
| 06/04/1503 | parte de Lisboa a armada de Afonso de Albuquerque, com Duarte Pacheco Pereira e Fernão Martins de Almada | uma das componentes da força de 1503 | A |
| 14/04/1503 | parte a armada de Francisco de Albuquerque, acompanhada por capitães como Nicolau Coelho; a listagem EVE também registra Pedro Vaz da Veiga como capitão-mor | segunda componente principal | A |
| 15/04/1503 | parte a armada de António de Saldanha com Diogo Fernandes Pereira e Rui Lourenço Ravasco | terceira componente; missão própria deve permanecer separada quando não houver convergência operacional comprovada | A |
| 1503, antes de Cochim | sobreviventes/navios da antiga força de Sodré sob Pedro de Ataíde são encontrados em Anjediva e agregados à força de 1503 | conexão documental entre P3.3 e P3.4 | B |
| setembro de 1503 | chegada das armadas de Francisco e Afonso de Albuquerque ao Malabar | força portuguesa volta a atuar diretamente em apoio a Cochim | A |
| setembro de 1503 | forças de Calecute são expulsas de Cochim e a cidade é devolvida ao aliado local | restauração do rajá de Cochim; não transferência de soberania para Portugal | A |
| setembro de 1503 | decisão de construir fortificação portuguesa em Cochim | nasce presença militar permanente distinta da feitoria | A |
| 27/09/1503 | HPIP, com base cronística, situa o ato de fundação/definição do lugar do forte Manuel nessa data | data de trabalho para início da fortificação, explicitamente dependente de fonte cronística posterior | B |
| fim de 1503 | Duarte Pacheco Pereira permanece com duas caravelas e pequena força em Cochim | guarnição/força residente portuguesa para defesa do aliado | A |
| 1504 | defesa de Cochim por Duarte Pacheco ocorre em gate posterior | consequência do estado criado em 1503; fora do recorte operacional desta issue | — |

## Composição — regra de prudência

A listagem EVE identifica três partidas independentes em abril de 1503:

1. **Afonso de Albuquerque**, 06/04/1503, com Duarte Pacheco Pereira e Fernão Martins de Almada;
2. **Francisco de Albuquerque**, 14/04/1503, com Pedro Vaz da Veiga e Nicolau Coelho no registro de capitães;
3. **António de Saldanha**, 15/04/1503, com Diogo Fernandes Pereira e Rui Lourenço Ravasco.

Essas partidas não devem ser comprimidas desde Lisboa em uma única `expedition_id`. A convergência operacional no Índico deve ser representada somente onde documentada.

## Matriz territorial e institucional

| Local | Antes da crise | Abril/1503 | Após chegada portuguesa em setembro | Interpretação correta |
|---|---|---|---|---|
| Calecute | potência regional adversária dos portugueses | origem da ofensiva contra Cochim | permanece adversária; não conquistada | relação hostil, sem mudança de soberania |
| Cochim | reino aliado; feitoria portuguesa desde Cabral e reorganizada em 1502 | cidade ocupada/invadida pelas forças de Calecute; rajá e portugueses retiram-se | rajá restaurado; feitoria continua; fortaleza e guarnição portuguesas surgem | coexistência de soberania local + instalação portuguesa fortificada |
| Vaipim | ilha/refúgio ligado ao espaço político de Cochim | refúgio do rajá e portugueses durante a ofensiva | deixa de ser centro do episódio após recuperação de Cochim | evento/refúgio; não há necessidade demonstrada de novo mercado |
| Cananor | feitoria portuguesa reorganizada em 1502 | não é o centro da crise de abril | continua ponto comercial português no Malabar | não deve herdar automaticamente fortificação/guarnição de Cochim |
| Anjediva | escala/ancoradouro | abriga remanescentes da força de Sodré sob Pedro de Ataíde | ponto de reunião com a armada de 1503 | escala/evento, não posse portuguesa |

## Feitoria × fortaleza × guarnição × soberania

Essas categorias não são sinônimas:

- **feitoria**: instalação comercial/residência de agentes; já existe em Cochim antes de 1503;
- **fortaleza**: estrutura defensiva autorizada/construída a partir de setembro de 1503;
- **guarnição/força residente**: homens e meios militares portugueses que permanecem para defender a posição e o aliado;
- **soberania**: continua pertencendo ao rajá de Cochim; a fortificação não deve transformar `COC` em território português.

A formulação do HPIP é particularmente útil: o Forte Manuel é concebido como instrumento para "segurar Cochim e o seu soberano", não como prova de anexação do reino.

## Duarte Pacheco Pereira

A EVE sustenta com segurança:

- sua participação na armada de 1503;
- comando de nau vinculada à força de Francisco de Albuquerque;
- participação na expulsão das forças de Calecute;
- decisão de deixá-lo no Oriente;
- comando de **duas caravelas** e pequena força para auxiliar a defesa de Cochim.

Para P3.4, ele deve ser tratado como comandante de uma presença militar residente específica. Seus combates de 1504 pertencem ao gate seguinte e não são usados aqui para criar um sistema geral de combate.

## Vicente Sodré como causa de contexto

A força de Sodré pertence à expedição de 1502, mas seus efeitos entram em 1503: ao deslocar-se para o Mar Vermelho, a força deixa Cochim exposta. Após os naufrágios de Vicente e Brás Sodré, Pedro de Ataíde assume o comando dos remanescentes e tenta regressar ao Malabar; o mau tempo leva-os a Anjediva, onde são encontrados e incorporados às forças de 1503.

P3.4 deve representar essa continuidade como **estado herdado/evento entre campanhas**, não como uma nova origem independente da crise.

## Eventos militares específicos

Os seguintes fatos podem ser documentados sem sistema genérico de combate:

- ofensiva de Calecute contra Cochim;
- retirada para Vaipim;
- expulsão das forças de Calecute após a chegada portuguesa;
- implantação da fortificação;
- permanência de força sob Duarte Pacheco.

A recorrência de confrontos em 1503–1504 demonstra crescente importância militar, mas ainda não define por si só qual abstração de combate é adequada ao jogo.

## Lacunas preservadas

1. dimensão exata de cada componente da armada de 1503 não deve ser inferida apenas da listagem de capitães;
2. cronologia diária da recuperação de Cochim exige fonte narrativa especializada adicional se for necessária para o loop;
3. a data de 27/09/1503 para a fundação do forte é adequada como data editorial de trabalho, mas depende de tradição cronística compilada pelo HPIP;
4. Vaipim ainda não justifica nó jogável próprio; sua necessidade deve ser testada contra a proposta funcional;
5. não se fixa número abstrato de soldados da guarnição sem fonte direta suficiente.

## Resultado preliminar

O ciclo de 1503 exige modelar **mudanças temporais de estado de um mesmo nó**. `COC` permanece Cochim e permanece sob soberania do rajá, mas passa por pelo menos três estados: aliado com feitoria → ocupado/crise e retirada para Vaipim → restaurado com feitoria + fortaleza + guarnição portuguesa.

Isso não cabe adequadamente em uma simples alteração estática de `nodes.csv` sem destruir a leitura de 1500–1502.