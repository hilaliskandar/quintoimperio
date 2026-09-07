# P3.3-doc — proposta mínima de normalização — Vasco da Gama 1502–1503

Data: 2026-09-07
Issue: #113

## Objetivo

Definir o menor conjunto de dados e estados necessários para representar documentalmente a segunda viagem de Vasco da Gama e a permanência da força de Vicente Sodré, sem antecipar implementação ou criar sistemas gerais ainda não demonstrados.

## 1. Unidades de expedição

### `EXP_GAMA_1502`

Expedição principal de Vasco da Gama, de Lisboa ao Malabar, cobrindo Sofala, Quiloa, Cananor, Cochim e as ações específicas relacionadas a Calecute.

### `EXP_GAMA_RETURN_1503`

Subcampanha de retorno candidata, somente se a implementação funcional precisar separar o retorno para preservar o loop, seguindo o precedente de `EXP_GAMA_RETURN_1498`.

### `EXP_SODRE_1503`

Subcampanha/força residente candidata a partir do ponto documentado de separação. Deve representar a força sob comando autónomo de Vicente Sodré e sua permanência no Índico.

Não se propõe uma coleção de múltiplas expedições ativas simultaneamente no estado do jogador.

## 2. Nós e rotas

Nenhum novo nó além de Cananor (`CAN`) é indispensável neste gate.

Reutilizar:
- `LIS` — Lisboa;
- `SOF` — Sofala;
- `KIL` — Quiloa/Kilwa;
- `CAL` — Calecute;
- `COC` — Cochim;
- `CAN` — Cananor, já proposto em P3.2.

Melinde pode permanecer escala/rota apenas se a reconstrução final demonstrar passagem efetiva; a tentativa frustrada por mau tempo não deve automaticamente gerar stop observado.

## 3. Atores residentes

### Cochim

- remover Gonçalo Gil Barbosa como feitor ativo a partir da reorganização de 1502;
- adicionar Diogo Fernandes Correia como feitor;
- função adicional documentada: juiz do peso da pimenta.

### Cananor

- Gonçalo Gil Barbosa passa a feitor de Cananor em 1502.

Essas mudanças não alteram soberania dos portos.

## 4. Estados relacionais e de acesso

### Calecute

Persistir hostilidade iniciada em 1500. Bombardeio e bloqueio de 1502 são eventos específicos e não elevam a cidade a categoria territorial portuguesa.

### Cochim

Persistir relação aliada/negociada e acesso comercial.

### Cananor

Persistir relação favorável/negociada e feitoria comercial.

## 5. Eventos históricos específicos

Candidatos:

- `KILWA_TRIBUTE_1502` — negociação sob ameaça e compromisso tributário em ouro;
- `MIRI_1502` — captura/incêndio do navio Mîrî, evento histórico específico;
- `CALICUT_BOMBARDMENT_1502` — bombardeio de Calecute;
- `CALICUT_BLOCKADE_1502` — bloqueio associado à força de Vicente Sodré;
- `COCHIN_FACTOR_REPLACEMENT_1502` — Barbosa → Diogo Fernandes Correia;
- `CANNANORE_FACTOR_ASSIGNMENT_1502` — Gonçalo Gil Barbosa em Cananor;
- `SODRE_FORCE_REMAINS_1503` — força naval permanece no Índico;
- `SODRE_RED_SEA_DEVIATION_1503` — decisão efetiva de procurar presas no Mar Vermelho, deixando Cochim exposta.

Esses eventos não exigem sistema geral de combate.

## 6. Mercadorias

Nenhuma nova mercadoria é indispensável para este gate documental.

- Cochim: pimenta permanece bem central já normalizado;
- Cananor: gengibre e cardamomo são documentados regionalmente, enquanto pimenta é escassa mas reputada. Só devem entrar no primeiro P3-func se o loop comercial realmente exigir ampliação da cesta.

## 7. Comando e composição

A composição nominal da armada deve permanecer em documentação e, se necessário, em tabela de expedição/capitães. Não é necessário criar navios individualizados ou tripulação individual para fechar o gate.

A componente de Estêvão da Gama, partida em 01/04/1502, deve ser mantida como formação subordinada/reinforcement documentada até que a implementação demonstre necessidade de subexpedição própria.

## 8. Lacuna de schema identificada

A arquitetura atual suporta uma expedição ativa por sessão. Isso é suficiente para seguir uma trajetória escolhida.

A única lacuna potencial é o efeito cronológico de uma força não controlada pelo jogador sobre o estado do mundo. A solução mínima candidata é uma camada de eventos históricos datados, não múltiplas expedições ativas no save.

Esse mecanismo só deve ser implementado se P3-func demonstrar necessidade concreta.

## 9. Critérios para P3-func futuro

Antes de implementar:

1. normalizar `CAN`;
2. criar as unidades de expedição estritamente necessárias;
3. preservar regressão integral de MVP, P1 e P2;
4. representar trocas de feitor e relações sem mudar soberania;
5. representar separação de Sodré sem refatorar `GameSessionState` de forma preventiva;
6. manter todos os eventos violentos como eventos específicos até prova de que combate genérico é necessário;
7. executar smoke e bateria reprodutível antes de balanceamento.

## 10. Decisão de gate

P3.3 pode ser considerado documentalmente fechado com a seguinte conclusão: a segunda viagem de Gama introduz presença naval portuguesa permanente no Índico e reorganização institucional das feitorias, mas ainda não exige sistema geral de combate nem múltiplas frotas simultâneas no estado do jogador. O próximo subgate deve tratar as armadas de 1503 e a fortificação de Cochim, pois ali a dimensão territorial/militar muda novamente de escala.