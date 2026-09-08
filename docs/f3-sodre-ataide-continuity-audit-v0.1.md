# F3 — continuidade Vicente Sodré → Pêro de Ataíde → armadas de 1503 v0.1

Data: 2026-09-08
Issue: #127
Baseline: `318f27c9a101f55626d2fc9e18cc8c85cffe9e89`

## Pergunta

A trajetória herdada da força de Vicente Sodré exige `EXP_SODRE_1503` como campanha jogável ou múltiplas frotas ativas para que F3 represente corretamente a crise e a recuperação de Cochim?

## Evidência dirigida

A documentação especializada e a síntese EVE convergem nos pontos necessários ao gate:

1. após a partida da frota principal de Vasco da Gama no fim de fevereiro de 1503, a força de Vicente Sodré permanece no Índico com missão de proteção/interdição;
2. Sodré afasta-se da proteção do Malabar e opera na direção da entrada do Mar Vermelho;
3. em abril de 1503 a esquadra está nas ilhas Cúria-Múria, na costa de Omã;
4. em maio, tempestade destrói as naus dos irmãos Vicente e Brás Sodré; Vicente morre no naufrágio e Brás morre posteriormente;
5. Pêro de Ataíde assume o comando dos navios sobreviventes;
6. a tentativa de regressar ao Malabar é desviada por condições meteorológicas e os remanescentes invernam/ficam em Anjediva;
7. em Anjediva, a força é encontrada pelas armadas de Afonso e Francisco de Albuquerque e integrada à força de 1503;
8. Ataíde participa depois da expulsão das forças de Calecute do reino de Cochim.

A carta de Pêro de Ataíde de 1504 é a principal narrativa testemunhal do episódio dos naufrágios; estudo arqueológico moderno a utiliza como base primária para localizar e interpretar os destroços.

## Consequência funcional

A sequência é necessária como **causalidade e continuidade histórica**, mas não demonstra necessidade de uma segunda frota simultaneamente controlada pelo jogador.

O que F3 precisa saber é:

- a força de proteção deixada por Gama não permanece protegendo Cochim;
- a força sofre perdas e muda de comando;
- os remanescentes reaparecem em Anjediva e são agregados às forças de 1503;
- os efeitos territoriais em Cochim continuam resolvidos por `node_state_events`.

Esses requisitos podem ser representados por eventos documentais e estados temporais do mundo. Não exigem que o jogador navegue a força de Sodré até Cúria-Múria nem que o save mantenha duas frotas ativas.

## Limite do schema atual

`expedition_events.csv` exige nós normalizados para origem/destino. Cúria-Múria ainda não é nó do grafo, e criá-la apenas para localizar um naufrágio documental seria expansão cartográfica sem necessidade de loop demonstrada.

Por isso, F3 não deve forçar o naufrágio para uma localização errada como `ADE` nem criar um nó operacional artificial.

## Decisão

1. **não criar `EXP_SODRE_1503` jogável neste subgate**;
2. **não criar Cúria-Múria como nó jogável apenas para o naufrágio**;
3. preservar em documentação a sequência Sodré → naufrágios → Ataíde → Anjediva;
4. se a convergência em Anjediva for necessária para um smoke das armadas de 1503, normalizar somente o evento de reunião no nó já existente `ANJ`, sem inventar a rota precedente;
5. manter a ausência de proteção de Cochim como contexto causal da crise, sem convertê-la em parâmetro abstrato de “força” ou combate;
6. reabrir a necessidade de subcampanha somente se uma decisão jogável posterior depender da trajetória autônoma da força.

## Fontes complementares consultadas neste subgate

- David L. Mearns et al., estudo arqueológico dos naufrágios da armada de 1502–1503 em Al Hallaniyah, *International Journal of Nautical Archaeology*, 2016;
- EVE/FCSH, “Pedro de Ataíde”;
- documentação P3.4 já incorporada ao repositório.

## Próximo gate

Auditar as três partidas de 1503 — Afonso de Albuquerque, Francisco de Albuquerque e António de Saldanha — e separar:

- registro histórico da expedição;
- convergência efetivamente necessária ao ciclo de Cochim;
- necessidade ou não de loop jogável.

O critério continua sendo comportamento necessário ao jogo, não quantidade de armadas históricas.