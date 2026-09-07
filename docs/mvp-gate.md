# Gate final do MVP Lisboa–Calecute

Status: **M8 concluído — candidato a marcação de versão**.

Base funcional auditada antes deste gate editorial: `main` após o PR #89, commit `970fd74c0f5a6f0a364fc93bd731f083fa1231a1`.

## Escopo do MVP

O MVP é a vertical slice da primeira viagem portuguesa de 1497–1498, iniciada em Lisboa com uma fase simulada de preparação em 6 de julho e partida histórica preservada em 8 de julho de 1497, encerrada após a primeira estadia jogável e operação comercial elegível em Calecute. Este gate consolida o comportamento integrado; não altera fatos históricos, regras de jogo ou parâmetros de `simulation/`.

## Matriz de verificação M8

| Critério do roadmap | Evidência atual | Resultado |
|---|---|---|
| Campanha inicia em Lisboa e chega a Calecute pela interface comum | `HistoricalCampaignModel`, interface histórica, smoke Lisboa–Calecute e baterias sintéticas | ATENDE |
| Nenhuma etapa exige `TECHNICAL` ou override de teste | fluxo canônico usa `EXP_GAMA_1497`; cenários técnicos permanecem separados | ATENDE |
| Divergências históricas mudam para `COUNTERFACTUAL` | testes cobrem partida fora da cronologia e permanência do modo contrafactual | ATENDE |
| Mercado, acesso e relações permanecem estados distintos | `GameSessionState` preserva conhecimento, acesso e relações como domínios separados | ATENDE |
| Existe ao menos uma decisão comercial real | quantidade selecionável, negociação de acesso e operação comercial em Calecute | ATENDE |
| Existem objetivos e condição explícita de encerramento | `CampaignProgressModel` deriva marcos e encerramento da vertical slice | ATENDE |
| Save/load preserva o estado | persistência JSON versionada e round-trip automatizado | ATENDE |
| CI integralmente verde | validação de dados, domínio, protótipos, interface, persistência e mapas permaneceram verdes nos gates posteriores | ATENDE |
| Smoke tests de interface e mapas aprovados | workflows continuam executando os smokes canônicos | ATENDE |
| Revisão automática sem achado concreto bloqueador | PRs funcionais e diagnósticos recentes foram integrados após revisão/CI | ATENDE |
| Documentação sincronizada com o comportamento real | `mvp-gate`, diário de desenvolvimento e diagnósticos pós-M7 registram a semântica estocástica atual | ATENDE |

## Robustez e contingência consolidadas

A robustez deixou de ser tratada como identidade de estado terminal entre seeds diferentes. O invariante correto é: **mesmo estado + mesma seed produzem o mesmo resultado; seeds diferentes podem produzir contingências distintas**.

Em cronologia `GUIDED`, uma observação histórica exata continua tendo precedência sobre o timing: eventos que alterariam a duração são suprimidos quando necessário para preservar a data documentada. Entretanto, eventos explicitamente marcados como `observed_timing_safe` podem afetar provisões ou condição sem deslocar a cronologia observada. Assim, a campanha guiada preserva datas documentadas sem se tornar deterministicamente idêntica entre todas as seeds.

A camada estocástica atualmente inclui eventos positivos e negativos de `SIMULATION`, entre eles deterioração moderada de provisões, racionamento eficiente, `MAJOR_PROVISION_LOSS` e `STRUCTURAL_STRAIN`. Esses eventos não são apresentados como incidentes ou frequências históricas.

### Evidência de balanceamento

As ondas pareadas 15 e 16 aplicaram as mesmas seeds `21001–21020` a dez arquétipos. A onda 16 introduziu apenas uma decisão de preparação contra `MAJOR_PROVISION_LOSS`, sem alterar sua probabilidade ou severidade. O resultado mostrou agência: políticas que pagaram por reserva segregada passaram a sobreviver a seeds antes praticamente fatais, ao custo de capital, enquanto perfis sem proteção mantiveram maior exposição ao risco.

A reserva segregada:

- protege somente provisões já embarcadas;
- não cria recursos nem serviço histórico;
- não revela antecipadamente o evento;
- oferece `0`, `5`, `10`, `15` ou `20` dias-equivalentes de proteção;
- custa `0,25` ponto de capital por dia protegido por viagem;
- afeta somente `MAJOR_PROVISION_LOSS`.

O diagnóstico estrutural posterior não encontrou justificativa equivalente para uma segunda proteção. Em 7.000 campanhas pareadas de sete arquétipos competentes foram observadas 3.274 ocorrências de `STRUCTURAL_STRAIN`; 185 terminaram abaixo de condição 40, nenhuma abaixo de 20 e não houve qualquer blocker `VESSEL_CONDITION_TOO_LOW` na perna seguinte. Portanto, a probabilidade e a severidade estruturais foram preservadas sem criar manutenção preventiva artificial.

## Estado funcional consolidado

O MVP inclui:

1. campanha contínua Lisboa → Calecute pelas dez pernas normalizadas;
2. fase pré-partida simulada sem antecipar a partida histórica;
3. cronologia `GUIDED` e `COUNTERFACTUAL`;
4. provisões, condição, espera, reabastecimento e reparo por ações explícitas;
5. planejamento por horizonte até o próximo abastecimento documentado e margem heurística explícita;
6. contingência estocástica reproduzível por seed, com resolução tardia;
7. decisão opcional e custosa de proteção de provisões contra uma cauda rara específica;
8. conhecimento por nó e por rota e aquisição de informação parametrizada;
9. acesso institucional separado de conhecimento e relações;
10. relações por atores historicamente normalizados;
11. piloto de Melinde limitado à rota documentada;
12. mercado documentado, quantidade selecionável e compra/venda;
13. objetivos derivados do estado e encerramento explícito em Calecute;
14. interface v0.2 com confirmação de viagem, histórico curto, indicação de cronologia e feedback de risco;
15. persistência JSON versionada em slot único;
16. validação automática, smoke tests, cartografia programática e baterias sintéticas reproduzíveis.

## Limites pós-MVP

Não fazem parte desta versão:

- retorno a Lisboa;
- Cochim e expansão cronológica além da primeira estadia em Calecute;
- crédito, câmbio, juros, contratos mercantis complexos ou moeda histórica completa;
- reputação global, diplomacia geral ou sistema amplo de facções;
- combate, doença, perdas de tripulação, naufrágio e controle individual da tripulação;
- múltiplos slots, nuvem ou migrações sofisticadas de save;
- refinamento estético amplo da interface;
- novos fatos, atores, portos, mercados ou rotas sem base documental.

## Decisão do gate

Os gates M0–M8 estão funcional e metodologicamente atendidos. O `main` resultante da sincronização editorial deste documento deve ser considerado o **commit de referência do MVP Lisboa–Calecute**.

A marcação de versão deve ocorrer somente após a CI e a revisão deste gate editorial. A expansão cronológica começa depois dessa marcação, preservando a vertical slice como baseline de regressão.
