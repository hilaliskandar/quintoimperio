# Diário de desenvolvimento — balanceamento, agência e risco

Este arquivo registra decisões de desenvolvimento que alteram a jogabilidade ou a interpretação dos testes sem confundir parâmetros de simulação com evidência histórica. O código e os testes do repositório permanecem a fonte executável; o diário registra a sequência decisória e os gates.

## 2026-09-07 — ondas pareadas 15 e 16

A onda 15 introduziu uma cauda rara de risco sob seeds pareadas. As mesmas seeds foram aplicadas aos dez arquétipos, permitindo separar diferenças de política de diferenças de sorte. Duas seeds severas funcionavam como derrotas praticamente inevitáveis quando nenhuma preparação específica estava disponível.

A onda 16 manteve probabilidades e severidades congeladas e acrescentou apenas a reserva segregada de provisões já embarcadas, capaz de mitigar exclusivamente `MAJOR_PROVISION_LOSS`.

Seeds: `21001–21020`.

Resultado agregado:

- onda 15: `126/200` campanhas concluídas (`63,0%`);
- onda 16: `133/200` campanhas concluídas (`66,5%`).

O resultado relevante não é o ganho agregado, mas a separação por política sob as mesmas contingências:

| Arquétipo | Onda 15 | Onda 16 | Proteção por viagem |
|---|---:|---:|---:|
| GRAND_STRATEGIST | 18/20 | 20/20 | 10 dias |
| SURVIVALIST | 18/20 | 20/20 | 20 dias |
| COMPLETIONIST | 18/20 | 20/20 | 15 dias |
| ROLEPLAYER | 18/20 | 19/20 | 5 dias |
| MERCHANT | 18/20 | 18/20 | 0 |
| OPTIMIZER | 18/20 | 18/20 | 0 |
| CASUAL | 18/20 | 18/20 | 0 |
| EXPLORER | 0/20 | 0/20 | 0 |
| ROGUELIKE | 0/20 | 0/20 | 0 |
| SPEEDRUNNER | 0/20 | 0/20 | 0 |

As seeds `21010` e `21014` deixaram de ser derrotas universais e passaram a discriminar políticas de preparação. A conclusão de design é que a cauda rara pode ser preservada quando o jogador recebe uma decisão preparatória com custo e alcance limitados.

## Reserva segregada de provisões v0.5

A mitigação é explicitamente `SIMULATION`:

- não representa técnica ou serviço histórico documentado;
- não aumenta provisões embarcadas;
- não revela o evento futuro;
- afeta somente `MAJOR_PROVISION_LOSS`;
- custa `0,25` ponto de capital por dia-equivalente protegido em cada viagem.

Escolhas disponíveis: `0`, `5`, `10`, `15` ou `20` dias-equivalentes.

A medida introduz um trade-off entre robustez logística e capital comercial. Nas 20 seeds da onda 16, a mediana aproximada de capital final foi `48,10` para SURVIVALIST, `57,75` para COMPLETIONIST, `70,15` para GRAND_STRATEGIST, `85,08` para ROLEPLAYER e cerca de `97,58` para CASUAL/OPTIMIZER sem proteção.

Rastreabilidade:

- PR `#84`: implementação e validação da reserva segregada;
- issue `#85`: exposição da escolha na interface;
- PR `#86`: seletor `0/5/10/15/20`, custo pré-partida e feedback pós-viagem;
- merge do PR `#86`: `ab84649c23a8c7ecd8a95ed0274b9883f4bd9a3c`;
- resultado detalhado: `docs/player-archetypes-wave16-paired-results.md`.

## Integração na interface histórica

A escolha da proteção foi integrada à interface pré-partida. A seleção por si só não altera provisões, condição nem capital; o custo só é aplicado quando a viagem é efetivamente confirmada e executada.

Quando ocorre `MAJOR_PROVISION_LOSS`, o feedback informa perda bruta, parcela mitigada e perda líquida. Quando a proteção foi preparada e o evento severo não ocorreu, o custo permanece como custo de oportunidade, sem benefício artificial posterior.

Todos os testes e smokes existentes permaneceram verdes após a integração.

## Regra de design consolidada

Para riscos de cauda, a ordem de intervenção passa a ser:

1. preservar a distribuição estocástica enquanto não houver evidência de desbalanceamento estrutural;
2. verificar se existe decisão preparatória anterior ao evento;
3. exigir custo de oportunidade ou restrição material para essa decisão;
4. medir novamente com seeds pareadas;
5. recalibrar probabilidade ou severidade apenas se a agência continuar insuficiente.

## Diagnóstico preliminar de `STRUCTURAL_STRAIN`

Antes de acrescentar uma segunda mitigação, os resultados da própria onda 16 foram reexaminados como diagnóstico de condição estrutural.

Nos `200` playtests:

- a condição mínima global foi `36,79`;
- nenhuma sessão caiu abaixo do limiar de partida `20`;
- não houve blocker `VESSEL_CONDITION_TOO_LOW` no agregado;
- `8/200` sessões chegaram a condição mínima inferior a `40`;
- somente uma dessas oito sessões falhou, sem indicação de que a falha tenha sido causada por condição estrutural.

O resultado muda o próximo passo. Não há evidência suficiente para introduzir imediatamente manutenção preventiva, sobressalentes ou uma proteção específica contra `STRUCTURAL_STRAIN`. Fazer isso agora acrescentaria uma mecânica sem problema demonstrado.

Foi aberta a issue `#87` para um diagnóstico dirigido em um universo ampliado de seeds, mantendo `simulation/voyage_event_rules.csv` congelado. O gate deve registrar ocorrência de `STRUCTURAL_STRAIN`, condição antes/depois, condição mínima e blockers posteriores, separando falhas por condição das falhas por provisões, navegação ou política do arquétipo.

## Próximo gate — medir antes de mitigar

A próxima etapa é executar o diagnóstico da issue `#87`. Nova mecânica estrutural somente será considerada se o teste demonstrar concentração de becos sem saída ou derrotas inevitáveis associadas a `STRUCTURAL_STRAIN` entre políticas competentes. Caso contrário, a decisão correta será preservar o risco atual sem adicionar proteção redundante.
