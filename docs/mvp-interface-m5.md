# Gate M5 — Interface v0.2

## Objetivo

O M5 reorganiza a apresentação da vertical slice Lisboa–Calecute sem alterar o domínio histórico, econômico, náutico ou relacional. A interface continua sendo uma camada de leitura de estado e envio de comandos para os modelos existentes.

## Decisões de interface

- o objetivo atual é lido diretamente de `CampaignProgressModel`, introduzido no M4;
- o estado `GUIDED`/`COUNTERFACTUAL` permanece pertencendo à sessão e recebe apenas destaque visual;
- a viagem passa a exigir seleção e confirmação explícita antes da execução;
- bloqueios comuns são traduzidos para frases curtas na interface, preservando os códigos originais no domínio;
- as últimas mensagens relevantes são mantidas apenas como histórico transitório da interface, sem participar do save, do progresso ou das regras;
- controles de quantidade continuam sendo os do M3;
- o resumo e a conclusão da campanha continuam derivados do M4.

## Hierarquia visual mínima

A versão v0.2 mantém o mapa como área principal e acrescenta dois elementos de orientação sobre ele:

1. faixa superior com objetivo atual, progresso dos marcos e modo cronológico;
2. faixa inferior com acontecimentos recentes da sessão.

O painel lateral existente continua apresentando porto, data, navio, capital/carga, serviços, informação, relações, mercado e rotas. Esta escolha evita um redesign estrutural amplo antes do fechamento funcional do MVP.

Ao solicitar uma viagem viável, uma caixa modal apresenta rota, destino, duração prevista e base de navegação, exigindo confirmação ou cancelamento. Nenhuma regra de viabilidade é reimplementada nessa caixa: o plano exibido continua sendo produzido por `HistoricalCampaignModel.plan_voyage`.

## Histórico curto

`action_history` é estado efêmero da camada Pygame. Ele registra no máximo quatro mensagens e não é considerado fonte de verdade para cronologia, objetivos, comércio, conhecimento, acesso ou relações.

## Testes e smoke

O gate adiciona testes para:

- objetivo inicial derivado do M4;
- viagem sem alteração de estado antes da confirmação;
- execução somente após confirmação;
- cancelamento sem efeito de domínio;
- tradução de bloqueios;
- limite e deduplicação do histórico curto.

A CI também renderiza o quadro inicial da interface v0.2 e um quadro final após o smoke Lisboa–Calecute, além de preservar todos os testes e smokes anteriores.

## Fora do escopo

Não entram neste gate animação, áudio, sprites, identidade visual definitiva, novos sistemas de painel, persistência, novas mecânicas ou novos fatos históricos. O próximo gate funcional permanece M6 — Persistência.
