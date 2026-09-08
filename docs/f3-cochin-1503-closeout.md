# F3 — ciclo de 1503 em Cochim — closeout funcional

Data: 2026-09-08
Issue: #127
Baseline de entrada: `318f27c9a101f55626d2fc9e18cc8c85cffe9e89`

## Resultado

A F3 demonstrou que o ciclo de 1503 em Cochim pode ser representado com as camadas históricas já existentes — `node_state_events`, `expedition_events` e catálogo de `expeditions` — sem criar novo schema territorial, múltiplas frotas simultaneamente ativas ou combate geral.

O estado funcional relevante ao fim de 1503 é:

- soberania local do rajá de Cochim preservada;
- feitoria portuguesa restaurada;
- Forte Manuel estabelecido como fortificação portuguesa sob soberania local;
- guarnição portuguesa residente consolidada somente no fim do ano;
- três armadas de 1503 registradas historicamente como expedições distintas, sem pernas executáveis nesta tranche.

## 1. Sequência temporal de Cochim

A auditoria de `node_state_events.csv` confirmou e refinou a seguinte sequência:

- **29/04/1503** — prevalece o estado anterior à crise;
- **30/04/1503** — `COC1503_E01`: ofensiva de Calecute e deslocamento temporário, com `FACTORY_DISPLACED`, acesso `DISRUPTED` e `HOSTILE_PRESSURE`;
- **29/09/1503** — a crise ainda prevalece pela regra conservadora do intervalo de restauração;
- **30/09/1503** — `COC1503_E02` restaura autoridade local/feitoria e `COC1503_E03` estabelece a fortificação portuguesa;
- **30/12/1503** — forte existente, sem guarnição consolidada pelo intervalo documental;
- **31/12/1503** — `COC1503_E04` consolida a guarnição portuguesa residente.

A janela de `COC1503_E03` foi corrigida de `27/09–31/12` para `27/09–30/09/1503`. A referência de 27/09 continua `RANGE`, evidência B; a alteração evita o anacronismo inverso de fazer o Forte Manuel aparecer somente em 31/12 e mantém a fortificação ordenada depois da restauração conservadora do rajá.

Em todas as transições, soberania local permanece explicitamente separada de presença institucional, fortificação e guarnição portuguesas.

## 2. Persistência

O estado histórico do mundo continua sendo função determinística de `node_id + data` sobre dados versionados. Não foi criado estado paralelo no save.

Testes de roundtrip confirmam que:

- a sessão salva/restaurada preserva localização e data;
- uma consulta do mesmo `NodeStateEventModel` antes e depois da recarga produz exatamente o mesmo estado histórico;
- em 30/09 há feitoria restaurada + forte, sem guarnição;
- em 31/12 há forte + guarnição, ainda sob soberania local.

F3, portanto, não exige alteração do schema de persistência.

## 3. Vicente Sodré e Pêro de Ataíde

A continuidade histórica foi auditada sem criar uma subcampanha prematura:

1. a força de Vicente Sodré permanece no Índico após a partida de Vasco da Gama;
2. afasta-se da missão de proteção do Malabar;
3. sofre os naufrágios nas Cúria-Múria em 1503;
4. Pêro de Ataíde assume os remanescentes;
5. condições de navegação impedem retorno imediato ao Malabar;
6. os remanescentes permanecem em Anjediva;
7. ali são encontrados e incorporados às forças de Afonso e Francisco de Albuquerque;
8. participam depois da recuperação de Cochim.

Essa trajetória é causalmente importante, mas não demonstra um loop de decisões que exija `EXP_SODRE_1503` jogável. Cúria-Múria tampouco foi criada como nó apenas para localizar um naufrágio documental.

## 4. Armadas de 1503

A listagem `EVE_ARMADAS_MANUEL` sustenta partidas distintas:

- Afonso de Albuquerque — 06/04/1503;
- Francisco de Albuquerque — 14/04/1503;
- António de Saldanha — 15/04/1503.

Foram criados três registros independentes em `expeditions.csv`:

- `EXP_AFONSO_ALBUQUERQUE_1503`;
- `EXP_FRANCISCO_ALBUQUERQUE_1503`;
- `EXP_SALDANHA_1503`.

Nenhum recebeu linhas em `expedition_routes.csv`. O domínio reconhece as expedições no catálogo histórico, mas `first_sequence()` recusa ativação porque não existem pernas. Isso formaliza a distinção entre **expedição documentada** e **campanha executável**.

A primeira CI desse teste falhou exclusivamente porque o arquivo novo importava `pytest`, dependência inexistente no projeto. O teste foi convertido para o framework `unittest` já adotado; nenhuma dependência foi adicionada e nenhuma regra de domínio foi alterada. O run corrigido `34186929676` terminou integralmente verde.

## 5. Convergência no Índico

A documentação sustenta:

- encontro dos remanescentes de Ataíde com as armadas de Afonso/Francisco em Anjediva;
- incorporação dos navios remanescentes;
- chegada ao contexto de Cochim em setembro;
- expulsão das forças de Calecute;
- restituição da cidade ao aliado local;
- início da fortificação;
- permanência posterior de Duarte Pacheco com duas caravelas.

O grau temporal permanece de intervalo para a convergência e a chegada. Portanto, F3 não cria:

- rota `LIS→ANJ` ou `ANJ→COC` com data arbitrária;
- `EXP_1503_COMBINED`;
- `voyage_observations` sem pares diários defensáveis;
- fusão das três armadas desde Lisboa.

António de Saldanha permanece registrado separadamente e não é comprimido no ciclo mínimo de Cochim.

## 6. Combate

A ofensiva de Calecute e a recuperação de Cochim são resultados históricos necessários ao estado mundial, mas F3 não demonstrou necessidade de resolução funcional de combate.

Não foram introduzidos:

- parâmetros abstratos de força, dano, moral ou baixas;
- unidades táticas;
- resolução probabilística de batalha;
- escolha militar que altere o resultado histórico no modo guiado.

A necessidade de combate deve ser reavaliada em F4, porque 1504 contém defesa prolongada e repetida de Cochim e oferece um teste muito mais forte para decidir se eventos guiados continuam suficientes.

## 7. Validação

Gates verdes relevantes:

- `34186632252` — estados temporais de Cochim + persistência por data;
- `34186929676` — registros das armadas de 1503 + suíte integral após correção para `unittest`.

Ambos passaram validação de dados, testes de domínio, protótipos, retorno P1, interfaces, persistência e cartografia.

## 8. Fora de escopo preservado

- `EXP_SODRE_1503` jogável;
- rotas completas das armadas de 1503;
- Cúria-Múria como nó operacional;
- Vaipim como mercado/nó jogável;
- combate geral;
- soberania portuguesa sobre Cochim;
- parâmetros militares inventados;
- defesa de 1504, pertencente a F4;
- doença/mortalidade sistêmica, tripulação individual, crédito/câmbio complexo.

## Handoff para F4 — Lopo Soares 1504

F4 deve partir do estado de **31/12/1503**:

- soberania local de Cochim;
- feitoria restaurada;
- `PORTUGUESE_FORT` ativo;
- `PORTUGUESE_GARRISON` ativo;
- força residente sob Duarte Pacheco como contexto histórico.

A questão central de F4 não é recriar o estado de 1503, mas testar se a defesa repetida de Cochim em 1504 ainda pode ser expressa como eventos/estados temporais ou se, pela primeira vez, existe necessidade funcional demonstrável de uma mecânica mínima de conflito.

A issue documental #115 deve ser lida como base da tranche. Qualquer implementação funcional de 1504 deve partir de branch própria e preservar o baseline F3.

## Critério final de integração

F3 está pronta para integração quando:

1. o diff completo contra `main` não contiver mudanças fora do escopo acima;
2. a CI do PR estiver integralmente verde;
3. não houver threads de revisão bloqueantes;
4. o merge for seguido por CI verde no `main`;
5. somente então a #127 for encerrada e o baseline F3 for registrado.