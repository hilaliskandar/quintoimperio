# Playtest sintético pós-MVP — onda 5

## Pergunta

Uma reserva logística explícita, constituída somente em portos com reabastecimento historicamente documentado e acionável, permite atravessar escalas cuja disponibilidade de provisões é historicamente indeterminada sem imputar serviço a essas escalas?

## Desenho

Mantêm-se os mesmos 20 perfis e seeds das ondas 2 e 4. A preparação torna a perna corrente viável e, quando o porto atual possui serviço de provisões documentado e acionável, solicita uma margem adicional experimental de 30 dias.

A margem de 30 dias é parâmetro do experimento. Não representa duração ou provisão historicamente observada. Nenhum valor de `nodes.csv` é alterado.

## Resultado

- 20/20 sessões executadas tecnicamente com sucesso;
- **16/20 concluíram a campanha (80%)**, contra 1/20 nas ondas 2 e 4;
- 4/20 entraram em `COUNTERFACTUAL`; são exatamente os quatro perfis `CAUTIOUS`;
- 16 sessões terminaram em Calecute;
- 2 terminaram no Rio do Cobre (`RCO`), 1 no Cabo da Boa Esperança (`CGH`) e 1 em Santa Helena (`SHB`);
- 61 ações de reserva foram executadas;
- 1.663 dias-unidade de provisões foram efetivamente adicionados como reserva ao longo das 20 sessões;
- 3 tentativas de reserva atingiram o limite de provisões a bordo;
- 64 oportunidades de reserva foram corretamente ignoradas por falta de serviço documentado/acionável;
- `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`: 13 ocorrências, contra 43 na onda 4;
- `INSUFFICIENT_PROVISIONS`: 3, contra 22 na onda 4;
- mediana de bloqueios: 2, contra 4 na onda 4.

Por perfil:

- `DISCIPLINED`: 4/4 concluíram;
- `FRUGAL`: 4/4 concluíram;
- `IMPATIENT`: 4/4 concluíram;
- `TRADER`: 4/4 concluíram;
- `CAUTIOUS`: 0/4 concluíram.

Todos os 16 casos concluídos chegaram a Calecute em 1498-05-22 e permaneceram em cronologia `GUIDED`.

## Assimetria do perfil CAUTIOUS

Os quatro casos `CAUTIOUS` registraram zero ações de reserva e zero `readiness_checks`. A causa é procedimental: a onda 5 aplicou a margem apenas no bloco de preparação anterior a uma espera histórica futura. O perfil cauteloso já parte de Lisboa na data histórica corrente e, portanto, não entra nesse bloco inicial; quando sua trajetória diverge, as partidas seguintes deixam de oferecer a mesma oportunidade de reserva guiada.

Consequentemente, a onda 5 demonstra a eficácia da **ideia de margem logística**, mas ainda não constitui um teste uniforme da política para os cinco perfis.

## Interpretação

O aumento de 5% para 80% de conclusão é evidência forte de que o principal gargalo material não requer preencher lacunas históricas de serviços. Ele pode ser contornado por planejamento de recursos antes de depender de uma escala incerta.

Isso também preserva a interpretação histórica: Santa Helena continua com provisões indeterminadas; o jogador que chega com margem suficiente simplesmente não precisa pressupor que ali havia reabastecimento.

## Próximo teste

Antes de incorporar qualquer ajuda de planejamento ao produto, deve ser executado um teste de sensibilidade em que a reserva seja considerada **antes de toda partida elegível**, inclusive quando a data de partida já foi alcançada. Recomenda-se comparar margens menores e a margem de 30 dias para verificar se o efeito é robusto e evitar transformar a política em um excesso automático de recursos.

Somente após essa sensibilidade deve ser definido o desenho de interface: indicador de autonomia, margem recomendada ou alerta de dependência de escalas com evidência indeterminada.