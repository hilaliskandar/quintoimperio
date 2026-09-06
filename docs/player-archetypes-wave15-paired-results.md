# Playtest sintético por arquétipos — onda 15 pareada

## Objetivo

Executar o primeiro desenho pareado do playtest da v0.4: as mesmas 20 seeds (`21001–21020`) foram aplicadas aos dez arquétipos, mantendo congelados os parâmetros dos eventos e as políticas comportamentais. O objetivo é separar efeito de política de efeito da realização estocástica.

## Resultado agregado

A bateria concluiu **126/200 campanhas (63,0%)**. O resultado agregado é próximo dos 128/200 (64,0%) da onda 14, mas o pareamento altera de forma importante a interpretação das diferenças entre arquétipos.

| Arquétipo | Conclusões pareadas |
|---|---:|
| GRAND_STRATEGIST | 18/20 |
| SURVIVALIST | 18/20 |
| MERCHANT | 18/20 |
| ROLEPLAYER | 18/20 |
| OPTIMIZER | 18/20 |
| COMPLETIONIST | 18/20 |
| CASUAL | 18/20 |
| EXPLORER | 0/20 |
| ROGUELIKE | 0/20 |
| SPEEDRUNNER | 0/20 |

## Resultado por seed

Em **18 das 20 seeds**, exatamente os mesmos sete arquétipos orientados por planejamento concluem e os mesmos três perfis frágeis falham. Em duas seeds — `21010` e `21014` — **nenhum dos dez arquétipos conclui**.

Esse padrão demonstra que as diferenças observadas entre os sete perfis competentes na onda 14 eram majoritariamente efeito das diferentes amostras de seeds, não das políticas. Quando submetidos à mesma contingência, GRAND_STRATEGIST, SURVIVALIST, MERCHANT, ROLEPLAYER, OPTIMIZER, COMPLETIONIST e CASUAL tornam-se indistinguíveis pela métrica de conclusão: todos fazem 18/20.

Os sete perfis também apresentam medianas iguais de provisão mínima (**15 dias-equivalentes**) e condição mínima (**59,85 pontos**). Há diferenças no número e no tipo de ações e bloqueios, mas elas não se convertem em diferença de robustez terminal sob o desenho atual.

## Diagnóstico das duas seeds fatais

A inspeção das sessões do perfil SURVIVALIST mostra que as duas falhas não decorrem de comportamento imprudente:

- na seed `21010`, uma perda rara de provisões de **-24,29 dias-equivalentes** deixa a campanha em `CGH`, em 22/11/1497, com provisões zeradas; a próxima progressão fica bloqueada por `INSUFFICIENT_PROVISIONS`;
- na seed `21014`, uma perda rara de **-18,81 dias-equivalentes** deixa a campanha em `SHB`, em 16/11/1497, com apenas 5,19 dias-equivalentes; a progressão também fica bloqueada por provisões insuficientes.

O SURVIVALIST já havia executado três ações de reabastecimento, totalizando 79 dias-equivalentes adicionais, e encontra também o limite `ONBOARD_PROVISION_CAP_REACHED`. Portanto, aumentar prudência dentro das regras atuais não evita essas falhas.

## Interpretação

A onda 15 confirma duas conclusões simultâneas.

Primeiro, a cauda rara da v0.4 é suficientemente forte para quebrar a conclusão garantida. Segundo, **ela ainda não produz diferenciação estratégica entre os perfis competentes**. As duas seeds adversas funcionam, na prática, como derrotas universais: a contingência é severa, mas não é mitigável pelas diferenças de política já existentes.

Isso significa que o próximo problema de design não é mais a frequência bruta dos eventos. A questão é a relação entre risco e agência do jogador. Aumentar ou reduzir simplesmente as probabilidades apenas mudaria quantas seeds são fatais, sem criar decisão estratégica adicional.

## Decisão do gate

A v0.4 deve continuar congelada até que exista um mecanismo de mitigação testável. O próximo incremento deve transformar pelo menos parte da cauda rara de um resultado puramente estocástico em um risco **consequencial, porém mitigável** por preparação ou decisão, sem reintroduzir conhecimento antecipado do evento específico e sem fabricar disponibilidade histórica de serviços.

O critério de aceitação para o próximo gate deve ser pareado: sob algumas mesmas seeds adversas, políticas mais prudentes precisam ter probabilidade ou capacidade de recuperação maior que políticas apenas suficientes. Só depois disso faz sentido voltar a calibrar probabilidades e severidade.
