# P3.5-doc — Lopo Soares 1504 — proposta mínima de normalização

Data: 2026-09-08
Issue: #115
Baseline funcional herdado: `1a4f43822446a77d5bb79a76c14fab8a879a50d1`

## Objetivo

Definir o menor recorte funcional de 1504 necessário ao horizonte Python 1505 GREEN, preservando a defesa prolongada de Cochim, a chegada da armada de Lopo Soares e a transição institucional, sem converter documentação militar em um motor geral de combate.

## 1. Decisão de arquitetura sobre combate

### Decisão

**F4 deve permanecer baseada em eventos guiados estruturados + estados temporais. Combate funcional mínimo NÃO é necessário nesta tranche.**

### Fundamentação

A documentação demonstra agência militar histórica de Duarte Pacheco Pereira: seleção e defesa de passagens, distribuição de homens e embarcações, emprego de artilharia, resposta a tentativas de dividir a força e reparo/reposicionamento entre investidas. O ambiente lagunar e os acessos estreitos são causalmente relevantes ao resultado.

Porém, o domínio atual não coloca o jogador em identidade fixa como Duarte Pacheco nem exige, para representar o estado mundial de 1504, que o jogador distribua unidades ou resolva confrontos. Criar combate neste ponto introduziria uma árvore de decisões que o loop existente não consome.

O caso de 1504 deve preservar estrutura militar maior que um único evento “vitória”, mas isso pode ser feito como cadeia de eventos históricos específicos. F5 permanece o último gate do T4 para reabrir a decisão se 1505 demonstrar necessidade funcional real.

## 2. Estado inicial de F4

F4 deve iniciar a partir do estado já resolvido em `31/12/1503` por F3:

- Cochim sob soberania local;
- `FACTORY_RESTORED`;
- `PORTUGUESE_FORT`;
- `PORTUGUESE_GARRISON`;
- acesso `NEGOTIATED`;
- relação `FAVORABLE`.

Nenhuma dessas dimensões será duplicada ou recriada em novos arquivos.

## 3. Unidade histórica de Lopo Soares

Criar em `expeditions.csv`:

`EXP_LOPO_SOARES_1504`

Campos propostos:

- autoridade: Coroa portuguesa;
- líder: Lopo Soares de Albergaria;
- período: 1504–1505;
- tipo: expedição régia/comercial-militar;
- partida documental: 22/03/1504 preservada em evidência/documentação;
- composição nominal conforme `EVE_ARMADAS_MANUEL`.

### Jogabilidade

Inicialmente, **sem pernas executáveis**.

A documentação disponível neste gate não sustenta ainda uma sequência diária bastante fina Lisboa→Índia para `voyage_observations.csv`, e o ciclo defensivo de Cochim antecede a chegada da armada. Registrar a expedição não implica ativá-la como campanha.

A descrição Peutinger do percurso Lisboa→Calecute deve continuar como prioridade documental; se for recuperada com cronologia suficiente, a rota poderá ser aberta em subgate funcional posterior sem alterar esta decisão sobre combate.

## 4. Eventos defensivos mínimos em Cochim

Recomenda-se registrar uma cadeia curta, não uma linha por batalha narrada.

### F4_E01 — `DEFENSE_CAMPAIGN_BEGINS`

- nó: `COC→COC`;
- janela: março–abril de 1504, a refinar antes da escrita final;
- sujeito: sistema defensivo luso-cochinense sob Duarte Pacheco;
- função: marcar início da campanha defensiva prolongada;
- notas: posição lagunar, passagens estreitas, forte/guarnição herdados de 1503.

### F4_E02 — `DEFENSIVE_POSITION_MAINTAINED`

- nó: `COC→COC`;
- janela: fase intermediária das investidas, sem dia inventado;
- função: representar repetição/redistribuição e manutenção das passagens;
- não contém números de dano, força ou moral;
- fatores documentais ficam em notas: terreno, embarcações, artilharia, aliados locais.

### F4_E03 — `DEFENSE_CAMPAIGN_ENDS`

- nó: `COC→COC`;
- janela: fim de junho–início de julho, a refinar;
- resultado: ofensiva principal do Samorim fracassa e Cochim permanece preservada;
- não altera soberania local.

A finalidade destes três eventos é preservar a duração e repetição sem fabricar sete “batalhas” equivalentes nem criar combate sistêmico.

## 5. Coulão

A documentação sustenta ida de Duarte Pacheco a Coulão após a fase principal das defesas e sua permanência naquele contexto até a chegada de Lopo Soares em setembro.

### Decisão

**Não criar nó Coulão/Kollam em F4-doc nem na primeira implementação, salvo necessidade do loop.**

Razões:

1. o grafo atual não contém o nó;
2. a ida de Duarte Pacheco é importante para continuidade biográfica/institucional, mas não precisa ser navegada pelo jogador para resolver o estado de Cochim;
3. criar o nó exigiria também decidir mercado, acesso, serviços, mercadorias e relações, ampliando F4 para além do problema militar/institucional;
4. o deslocamento pode permanecer registrado em documentação até que uma campanha executável realmente precise de `COC→COL`.

Se F5 ou a futura rota de Lopo exigir Coulão para comércio/carga, abrir gate cartográfico/econômico próprio.

## 6. Chegada de Lopo Soares

A primeira implementação deve registrar como eventos, sem rota observada inventada:

### F4_E04 — `ROYAL_FLEET_ARRIVES_MALABAR`

- setembro de 1504, `INTERVAL` enquanto os limites inferior e superior não forem fechados documentalmente;
- sujeito: armada de Lopo Soares;
- efeito: reforço objetivo da presença portuguesa no Malabar.

### F4_E05 — `CALICUT_BOMBARDMENT`

- episódio específico ligado à chegada de Lopo Soares;
- permanece evento histórico, sem sistema de combate naval geral;
- não gera dano urbano quantificado no domínio.

### F4_E06 — `COCHIN_REINFORCEMENT`

- setembro de 1504;
- nó: `COC→COC`;
- reforça a continuidade do estado defensivo/institucional sem converter Cochim em soberania portuguesa.

### F4_E07 — `CRANGANORE_RAID`

- episódio posterior de 1504, somente se a evidência mínima for fechada;
- evento específico, não rota jogável nem combate genérico.

A batalha/ação de Pandarane e outras operações tardias da armada devem permanecer fora do primeiro F4 funcional salvo se forem necessárias ao estado de 31/12/1504.

## 7. Transição de comando

A documentação indica que Duarte Pacheco regressa com Lopo Soares e que Manuel Teles Barreto aparece como responsável subsequente pela guarda de Cochim; outras variantes onomásticas permanecem pendentes de auditoria. A cronologia segura alcança janeiro de 1505.

### Decisão

- não antecipar a troca para uma data de 1504 sem evidência suficiente;
- manter `PORTUGUESE_GARRISON` como estado institucional durante 1504;
- registrar a transição nominal de comando no handoff F4→F5 como janela `fim de 1504–janeiro de 1505` até fechamento documental;
- não criar um novo campo de comandante em `node_state_events` apenas para esse caso; se F5 demonstrar necessidade recorrente, reavaliar schema.

## 8. Dados que F4 NÃO deve alterar

- `simulation/` na primeira implementação;
- parâmetros de provisão/capital/navegação já congelados;
- soberania de Cochim;
- `fortification` estático de `nodes.csv`;
- classes de navio/tripulação;
- quantidades de forças, baixas ou peças de artilharia tomadas das crônicas;
- combate geral;
- `voyage_observations.csv` sem pares documentais diários.

## 9. Testes funcionais mínimos

F4 deve provar:

1. estado herdado de 31/12/1503 correto;
2. eventos de defesa não aparecem em campanhas anteriores;
3. cadeia de defesa de 1504 é temporalmente ordenada e conservadora;
4. soberania local permanece inalterada durante e depois da defesa;
5. chegada/reforço de Lopo em setembro não apaga fortificação/guarnição anteriores;
6. `EXP_LOPO_SOARES_1504`, se registrado sem pernas, não pode ser ativado acidentalmente;
7. save/load em data de 1504 resolve os mesmos estados/eventos;
8. regressão integral MVP/P1/P2/P3/F1/F2/F3 verde.

## 10. Playtests

**Não executar bateria de arquétipos nesta primeira F4**, porque a proposta não introduz nova decisão jogável. Smoke temporal + persistência + regressão são suficientes.

Se uma etapa posterior abrir uma escolha funcional de defesa, então criar bateria específica, seeds sentinela e telemetria antes de qualquer calibragem.

## 11. Gate T4 — decisão formal

Para o horizonte F4:

`COMBATE_FUNCIONAL_MINIMO = NAO_NECESSARIO`

`ARQUITETURA = EVENTOS_GUIADOS_ESTRUTURADOS + NODE_STATE_EVENTS`

`REABRIR_GATE = somente se F5 ou uma campanha executável demonstrar decisão militar do jogador que não possa ser representada sem resolução funcional`

## Critério de fechamento da #115

A #115 pode ser encerrada documentalmente quando:

- matriz de evidências v0.1 estiver aceita;
- matriz de decisão de combate estiver registrada;
- esta proposta mínima estiver registrada;
- Coulão permanecer explicitamente deferida salvo necessidade;
- a decisão T4 para F4 estiver formalizada;
- uma branch funcional F4 for aberta somente após integração deste gate documental.
