# F2 — Vasco da Gama 1502–1503 — closeout funcional

Data: 2026-09-08
Issue: #122
PR: #126
Baseline de entrada: `24b6de7799f3ebb40c9a3401a73ddb5913d1190f`

## Resultado

A F2 integrou `EXP_GAMA_1502` no máximo grau funcional atualmente defensável sem preencher lacunas cronológicas com datas diárias inventadas e sem ampliar o schema para múltiplas frotas simultâneas.

A campanha executável mínima é:

`LIS → SOF → KIL → CAN`

A continuação no Malabar é representada por eventos históricos temporalmente explícitos quando a documentação permite maior resolução, enquanto a torna-viagem transoceânica permanece documental e não jogável.

## 1. Cronologia e rotas

- partida principal de Lisboa: baseline de trabalho `01/02/1502`, preservando em documentação a divergência de `CALCOEN_1504`, que registra 10/02;
- Sofala: junho de 1502, `INTERVAL`;
- Quiloa: julho de 1502, `INTERVAL`;
- zona de Cananor: setembro de 1502, `INTERVAL`;
- `R_SOF_KIL` é reutilizada como rede suaíli preexistente; seu período foi estendido até 1505, sem reclassificação como criação portuguesa;
- somente as arestas indispensáveis `R_LIS_SOF_GAMA1502` e `R_KIL_CAN_GAMA1502` foram criadas;
- nenhuma linha de Gama 1502 foi adicionada a `voyage_observations.csv`, pois não há pares partida/chegada diários suficientes para durações históricas defensáveis.

## 2. Malabar 1502–1503

A incorporação de `CALCOEN_1504` permitiu registrar como eventos específicos:

- `27/10/1502` — saída de Cananor rumo a Calecute;
- `02/11/1502` — movimento de Calecute para Cochim;
- `28/11/1502` — negociação com o rajá de Cochim;
- `03/01/1503` — saída de Cochim em direção a Quilon;
- `12/02/1503` — combate naval ligado a Calecute;
- `13/02/1503` — partida rumo a Cananor para preparar o retorno.

Esses marcos não foram convertidos automaticamente em pernas jogáveis, `observed_days`, preços sistêmicos ou combate geral. Quilon permanece fora do grafo até existir necessidade funcional e cartográfica documentada.

## 3. Cochim e Cananor

A camada `node_state_events` existente foi suficiente para representar a reorganização institucional das feitorias em 1502:

- Diogo Fernandes Correia substitui Gonçalo Gil Barbosa em Cochim;
- Gonçalo Gil Barbosa passa a Cananor;
- os efeitos são aplicados conservadoramente no limite superior das janelas documentais;
- soberania de Perumpadappu em Cochim e de Kolathunad em Cananor permanece explícita;
- não há fortificação, guarnição ou soberania portuguesa retroativa.

Logo, F2 não demonstrou necessidade de novo schema de estado territorial.

## 4. Bifurcação Gama / Vicente Sodré

A pesquisa final acrescentou `ANTT_GAMA_CAN_1503`: documentos assinados por Vasco da Gama em Cananor em `22/02/1503`, que funcionam como `terminus post quem` para a partida final.

A partida é mantida como `INTERVAL` entre `23/02/1503` e `28/02/1503`. O dia 28 é limite superior de reconstrução e não foi elevado a testemunho `EXACT`.

- `GAMA1503_E10/RETURN_FLEET_DEPARTS` registra `CAN → LIS` nessa janela apenas como evento documental;
- `GAMA1502_E03/FORCE_REMAINS` usa a mesma janela e só consolida conservadoramente a autonomia da força residente no limite superior;
- nenhuma rota executável `CAN → LIS` foi criada;
- `EXP_GAMA_RETURN_1503` não é necessária para F2;
- `EXP_SODRE_1503` jogável também não é necessária apenas para expressar permanência no Índico.

A arquitetura com um único `active_expedition_id` permanece suficiente para este gate.

## 5. Persistência e regressão

A F2 possui testes específicos para:

- smoke `LIS → SOF → KIL → CAN`;
- ausência de observações diárias inventadas;
- estados institucionais temporais de Cochim e Cananor;
- eventos testemunhais do Malabar;
- janela de separação Gama/Sodré;
- inexistência de rota executável fictícia `CAN → LIS`;
- save/load durante `EXP_GAMA_1502`, preservando seed, relógio, posição, sequência de perna e `ChronologyMode.GUIDED`.

O run `34186212207`, no HEAD anterior à limpeza final de escopo, passou integralmente: validação dos CSVs, testes de domínio, protótipos, retorno P1, interfaces, persistência e cartografia. A limpeza final de `data/routes.csv` restaura ao texto exato de `main` alterações acidentais de Cabral e João da Nova; após essa correção, uma nova CI é o gate final para integração.

## 6. Auditoria de escopo do PR

A revisão completa do PR #126 detectou que uma atualização anterior de `data/routes.csv` havia carregado reformulações não necessárias de linhas de Cabral e João da Nova. Embora a suíte permanecesse verde, essas mudanças não pertenciam à F2.

A limpeza final restaura as linhas antigas ao estado de `main` e deixa em `routes.csv` somente:

1. extensão temporal de `R_SOF_KIL` até 1505;
2. `R_LIS_SOF_GAMA1502`;
3. `R_KIL_CAN_GAMA1502`.

Esse procedimento reduz o diff e evita reabrir implicitamente gates já congelados.

## 7. Itens deliberadamente fora de F2

- combate genérico ou microtático;
- Quilon como nó jogável;
- `EXP_GAMA_RETURN_1503`;
- `EXP_SODRE_1503` como campanha ativa apenas para representar presença;
- múltiplas frotas simultâneas no mesmo save;
- fortificação/guarnição de Cochim em 1503;
- ação posterior de Sodré no Mar Vermelho;
- doença/mortalidade sistêmica, tripulação individual e crédito/câmbio complexo.

## Handoff para F3 — ciclo de 1503 em Cochim

F3 deve partir do estado mundial deixado por F2 e responder a uma questão arquitetural mais exigente: se as ações autônomas de forças portuguesas em 1503, a ofensiva de Calecute contra Cochim, o refúgio em Vaipim, a recuperação de Cochim, a construção do Forte Manuel e a guarnição de Duarte Pacheco podem continuar sendo representadas por `expedition_events` + `node_state_events`, ou se alguma delas demonstra necessidade real de uma subcampanha jogável ou de mecânica funcional mínima de conflito.

A criação de `EXP_SODRE_1503` deve ser decidida em F3 pelo comportamento que precisa ser modelado, não pela mera coexistência histórica de forças.

## Critério final de integração

F2 está pronta para merge quando:

- a CI do HEAD pós-limpeza de escopo estiver integralmente verde;
- o diff final permanecer restrito à tranche F2, documentação e testes;
- o PR #126 estiver mergeável;
- o merge for seguido por CI verde em `main`.

Somente após esse gate a issue #122 deve ser encerrada e o baseline F2 registrado para abertura formal de F3.