# P3.5-doc — Lopo Soares 1504 — closeout documental

Data: 2026-09-08
Issue: #115
Baseline funcional herdado: `1a4f43822446a77d5bb79a76c14fab8a879a50d1`

## Resultado

O gate documental de 1504 produziu informação suficiente para iniciar F4 funcional sem antecipar um sistema geral de combate.

Foram consolidados:

- matriz de evidências de Lopo Soares/defesa de Cochim;
- matriz de decisão entre eventos guiados e combate funcional;
- proposta mínima de normalização;
- regra explícita sobre Coulão;
- separação entre agência histórica de Duarte Pacheco e agência efetivamente necessária ao jogador.

## 1. Estado inicial de 1504

F4 herda integralmente F3. Em 31/12/1503 Cochim resolve como:

- soberania local preservada;
- feitoria restaurada;
- Forte Manuel estabelecido;
- guarnição portuguesa residente;
- acesso negociado;
- relação favorável.

F4 não deve duplicar esses estados.

## 2. Armada de Lopo Soares

A listagem EVE/FCSH sustenta partida em 22/03/1504 e composição nominal de trabalho. A chegada ao Malabar é firmemente situada em setembro, mas a sequência diária Lisboa→Índia ainda não foi fechada neste gate.

A coleção de Conrad Peutinger contém uma descrição específica do percurso da armada de Lopo Soares de Lisboa a Calecute. Essa fonte passa a ser prioridade para eventual normalização futura da rota; a sua mera existência não autoriza preencher o itinerário por analogia.

Decisão: F4 pode criar `EXP_LOPO_SOARES_1504` como registro histórico inicialmente sem pernas executáveis. Uma rota só deve ser acrescentada se a documentação Peutinger ou outra fonte comparável fornecer resolução suficiente e se o loop funcional precisar dela.

## 3. Defesa de Cochim

A defesa de 1504 é qualitativamente mais complexa que os episódios militares anteriores. A documentação registra:

- campanha prolongada, com ataques repetidos;
- uso de passagens/canais estreitos;
- distribuição e redistribuição de homens e embarcações;
- emprego de artilharia em posições favoráveis;
- reação a tentativas de dividir a força defensiva;
- manutenção/reparo de meios entre investidas;
- participação combinada portuguesa e cochinense;
- preservação de Cochim como resultado histórico.

Estudo crítico moderno ressalta a importância da geografia lagunar e das passagens estreitas e recomenda cautela com os números extremamente elevados transmitidos pelas crônicas. F4 não deve normalizar força, baixas, moral ou dano a partir dessas cifras.

## 4. Gate T4 — combate

Decisão formal para F4:

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

`ARQUITETURA = EVENTOS_GUIADOS_ESTRUTURADOS + NODE_STATE_EVENTS`

Justificativa:

1. existe agência militar histórica real;
2. porém, o jogador não é identificado automaticamente com Duarte Pacheco;
3. o estado mundial de 1504 pode ser reproduzido sem resolução tática;
4. introduzir combate geral criaria decisões, parâmetros e balanceamento que o loop atual não consome;
5. a estrutura histórica não deve ser reduzida a um único evento de vitória, mas pode ser preservada por cadeia curta de episódios defensivos.

F5 permanece como último teste desse gate. Combate só deve ser reaberto se uma campanha executável demonstrar decisão militar do jogador que não possa ser representada de outra forma.

## 5. Cadeia funcional proposta

A primeira F4 deve preferir uma cadeia curta:

1. `DEFENSE_CAMPAIGN_BEGINS` — início da fase defensiva prolongada;
2. `DEFENSIVE_POSITION_MAINTAINED` — repetição/redistribuição sem microtática;
3. `DEFENSE_CAMPAIGN_ENDS` — retirada/fim da ofensiva principal até início de julho;
4. `ROYAL_FLEET_ARRIVES_MALABAR` — chegada de Lopo Soares em setembro;
5. `CALICUT_BOMBARDMENT` — episódio específico, se necessário ao encadeamento;
6. `COCHIN_REINFORCEMENT` — reforço da presença sem alteração de soberania;
7. `CRANGANORE_RAID` — somente se a evidência mínima e a função no estado de fim de 1504 forem confirmadas.

Nenhum desses tipos implica combate sistêmico.

## 6. Coulão

Duarte Pacheco desloca-se para Coulão depois da fase principal da defesa e permanece nesse contexto até a chegada de Lopo Soares.

Decisão: **Coulão/Kollam não será criado como nó na primeira F4 funcional.**

A ida é historicamente relevante, mas não precisa ser navegada pelo jogador para explicar o estado de Cochim. Criar o nó agora exigiria abrir simultaneamente cartografia, mercado, acesso, serviços e mercadorias.

Se a rota de Lopo ou F5 demonstrar necessidade comercial/logística real, Coulão deverá receber gate próprio.

## 7. Transição de comando

Duarte Pacheco regressa com a armada de Lopo Soares. A documentação aponta Manuel Teles Barreto como responsável subsequente pela guarda de Cochim; outras variantes onomásticas permanecem pendentes de auditoria. A cronologia segura alcança janeiro de 1505.

Decisão:

- não inventar uma data de troca dentro de 1504;
- manter `PORTUGUESE_GARRISON` durante o ano;
- carregar para F5 uma janela de transição `fim de 1504–janeiro de 1505`;
- não criar novo campo de comandante em `node_state_events` até que a recorrência desse requisito seja demonstrada.

## 8. O que permanece fora da F4 inicial

- combate geral;
- pontos de vida, dano, moral, baixas ou força quantitativa;
- microtática;
- classes militares detalhadas;
- Coulão como nó;
- rota Lisboa→Índia de Lopo preenchida por analogia;
- `voyage_observations` sem datas defensáveis;
- bateria de arquétipos sem nova decisão jogável;
- retroprojeção da mecânica militar para 1500–1503.

## 9. Critério funcional da futura F4

A F4 será considerada verde se:

- o estado herdado de 1503 permanecer íntegro;
- a campanha defensiva de 1504 estiver representada como sequência temporal estruturada;
- soberania local não for alterada;
- chegada/reforço de Lopo estiver representado no grau documental disponível;
- `EXP_LOPO_SOARES_1504` não ganhar pernas fictícias;
- save/load resolver o mesmo estado por data;
- nenhuma nova decisão jogável for criada sem necessidade;
- CI e regressão integral permanecerem verdes;
- handoff para F5 registrar explicitamente a transição de comando pendente.

## 10. Documentos do gate

- `docs/p3-5-lopo-soares-1504-evidence-v0.1.md`;
- `docs/p3-5-1504-defense-decision-matrix-v0.1.md`;
- `docs/p3-5-1504-minimal-normalization-proposal.md`;
- este closeout.

## Próximo passo

Após CI verde e integração desta branch documental:

1. encerrar #115;
2. abrir issue funcional F4 vinculada à #118;
3. criar branch funcional diretamente do `main` pós-merge documental;
4. implementar somente a cadeia de eventos/estado acima;
5. testar e integrar antes de abrir F5 documental.
