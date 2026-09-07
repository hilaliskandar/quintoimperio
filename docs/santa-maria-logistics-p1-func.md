# P1-func — Santa Maria como ponte logística documentada

Issues: #99, #100.

Data: 2026-09-07.

## Problema observado

Na wave17, um estado real de conclusão do MVP chegou a Calecute com `19,366` dias-equivalentes de provisões. A antiga perna agregada `CAL→ANJ` exigia 21 dias, tornando impossível iniciar o retorno apesar da longa permanência histórica em Calecute.

A solução não pode ser conceder provisões em Calecute por conveniência. A pesquisa dirigida no `Roteiro` não identificou uma tomada específica de mantimentos imediatamente antes da partida de 30/08/1498.

## Evidência encontrada durante a navegação costeira

A narrativa registra, contudo, eventos materiais antes de Anjediva:

- em 11/09, barcos aproximam-se da armada e oferecem peixe para venda;
- em 15/09, nos Ilhéus de Santa Maria, novos barcos trazem peixe;
- o padrão de Santa Maria é colocado nesse ponto;
- a armada prossegue na mesma noite e chega a Anjediva em 20/09.

Isso muda o problema de desenho. O trecho `CAL→ANJ` estava agregando uma oportunidade material historicamente documentada no interior da perna.

## Decisão de segmentação

A subcampanha do retorno passa de seis para sete pernas:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`

As duas primeiras observações usam:

- `CAL→SMI`: 30/08/1498 a 15/09/1498 = 16 dias;
- `SMI→ANJ`: 15/09/1498 a 20/09/1498 = 5 dias.

`SMI` é materializado somente como `NAVIGATION_POINT`, com `NAVIGATION_ONLY`, `market_scale=NONE` e todos os serviços portuários genéricos indisponíveis. A existência de peixe na passagem não é convertida em mercado.

## Identificação cartográfica

A auditoria preliminar havia associado Santa Maria genericamente às Laquedivas/Lakshadweep. A revisão dirigida encontrou base mais específica em Ravenstein e na edição anotada de Jeremy Lawrance para usar **Netrani/Pigeon Island** como âncora moderna de trabalho.

A tradição alternativa junto a Mulpy/Malpe permanece registrada. Portanto:

- posição moderna de Netrani: âncora cartográfica de trabalho;
- `coordinate_confidence=MEDIUM` para a equivalência histórica;
- nenhuma precisão histórica adicional é inferida da precisão da coordenada moderna.

## Projeção jogável do contato alimentar

O stop de Santa Maria registra `FISH_EXCHANGE|PADRAO`, com permanência de `0` dias porque a narrativa informa continuação na mesma noite.

A ação alimentar é específica da permanência e parametrizada em `simulation/return_rules.csv`:

- capacidade máxima por ação: **5 dias-equivalentes**;
- tempo consumido: **0 dias inteiros**;
- classificação: `SIMULATION`;
- disponibilidade portuária genérica: inalterada.

O limite de 5 não é quantidade histórica. Ele impede que um contato breve seja usado como abastecimento amplo e é suficiente apenas para a curta perna seguinte até Anjediva.

## Regra de uso

Nos diagnósticos automatizados, Santa Maria admite **uma única ação**. Essa disciplina evita explorar repetidamente o mesmo contato narrativo sem introduzir neste gate um novo campo de histórico de ações no save schema.

Se a interface futura expuser a ação diretamente ao jogador, deverá impor o mesmo caráter one-shot sem refatorar retroativamente a evidência histórica.

## Não regressão

A segmentação não altera:

- as dez pernas do MVP Lisboa–Calecute;
- a data histórica de saída de Calecute;
- a chegada a Anjediva em 20/09;
- a permanência e carena documentadas em Anjediva;
- mercados ou serviços genéricos dos nós;
- probabilidades e severidades de eventos;
- desgaste de viagem.

## Gate de validação

A alteração só deve ser considerada estabilizada depois de:

1. validação integral dos CSVs;
2. testes de continuidade com sete pernas;
3. smoke `CAL→SMI→ANJ→...→BRG` em `GUIDED`;
4. repetição do painel de 20 estados do MVP;
5. confirmação de que, combinada com a carena mínima de Anjediva, a solução elimina os blockers observados sem criar novos desvios cronológicos;
6. atualização do Drive e das issues correspondentes.