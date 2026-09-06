# Playtest sintético pós-MVP — onda 3

## Pergunta

Os canais de informação já existentes conseguem resolver `SERVICE_AVAILABILITY_UNKNOWN` sem introduzir fatos históricos não documentados?

## Desenho

Mesmos 20 perfis e mesmas seeds das ondas anteriores. Mantém-se a preparação pré-partida da onda 2. Quando um reabastecimento falha com `SERVICE_AVAILABILITY_UNKNOWN`, o agente tenta, quando disponíveis, os canais públicos já implementados: `RUMOR`, `MERCHANT_CONTACT` e `PILOT_CONSULTATION`, e então repete a tentativa de serviço.

Nenhum canal recebe permissão para alterar diretamente os campos históricos `provisions` ou `repair`.

## Resultado

- 20 sessões executadas tecnicamente com sucesso;
- 1/20 concluiu a campanha, igual à onda 2;
- 4/20 entraram em `COUNTERFACTUAL`, igual à onda 2;
- 18 aquisições de informação foram executadas;
- 31 encontros com `SERVICE_AVAILABILITY_UNKNOWN`;
- 16 novas tentativas de serviço após aquisição de informação;
- **0 bloqueios de serviço desconhecido resolvidos**;
- 31 encontros permaneceram não resolvidos;
- `SERVICE_AVAILABILITY_UNKNOWN` apareceu 59 vezes por causa das tentativas e retentativas controladas;
- 14/20 sessões terminaram novamente em São Brás (`SHB`).

## Interpretação

O teste negativo confirma uma distinção estrutural no domínio. `SERVICE_AVAILABILITY_UNKNOWN` é produzido diretamente pelo valor vazio do campo histórico do nó, portanto significa ausência de evidência histórica na base. Já `RUMOR`, `MERCHANT_CONTACT` e `PILOT_CONSULTATION` modificam conhecimento pessoal geográfico, comercial, político e de navegação. Eles não possuem estado nem regra para transformar evidência histórica ausente em disponibilidade portuária conhecida.

Assim, o gargalo revelado pelas ondas 2 e 3 não pode ser resolvido apenas ensinando o jogador a procurar informação. Hoje existem dois conceitos colapsados sob a experiência de jogo:

1. **desconhecimento do jogador sobre um serviço que historicamente poderia estar documentado**;
2. **indeterminação da própria base histórica sobre a existência/capacidade do serviço**.

O primeiro poderia ser resolvido por informação adquirida; o segundo não deve ser convertido automaticamente em `LOW`, `MEDIUM`, `HIGH` ou `NONE`, pois isso inventaria evidência.

## Encaminhamento recomendado

Antes de recalibrar provisões ou eventos, separar semanticamente disponibilidade histórica de conhecimento do jogador. Uma solução defensável deve preservar `UNKNOWN` como estado da evidência e permitir, se desejado, uma camada de crença/informação do jogador com resultado incerto ou decisão sob risco, sem sobrescrever o dado histórico.

Este experimento não altera o MVP nem os parâmetros de simulação.