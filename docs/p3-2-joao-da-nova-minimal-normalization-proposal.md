# P3.2-doc — proposta mínima de normalização João da Nova 1501–1502

Data: 2026-09-07
Issue: #112

## Objetivo

Definir o menor conjunto documental que permitiria representar a terceira armada da Índia sem código novo neste gate e sem introduzir sistemas gerais desnecessários.

## 1. Expedição candidata

`EXP_JOAO_NOVA_1501`

- partida: 05/03/1501;
- comandante: João da Nova;
- quatro navios/capitães documentados pela EVE: João da Nova, Diogo Barbosa, Francisco Novais e Fernão Vinet;
- caráter primordialmente comercial;
- estado inicial de conhecimento não inclui o desfecho de Cabral no Malabar.

## 2. Evento obrigatório de informação

Em `SBR`, a campanha deve adquirir `CABRAL_MALABAR_WARNING`.

Antes do evento:
- Calecute não é conhecido pela expedição como hostil após Cabral;
- Cochim/Cananor não são conhecidos como alternativas resultantes da missão de 1500.

Depois do evento:
- Calecute passa a ser conhecido pela expedição como porto a evitar;
- Cochim e Cananor tornam-se alternativas historicamente informadas;
- o estado objetivo desses portos não é criado pelo evento; ele apenas se torna conhecido.

O evento deve ser one-shot e persistente.

## 3. Sequência operacional mínima

A sequência documentada mínima após a partida é:

`LIS → SBR → KIL → MAL → ANJ → CAN → COC → CAN → retorno`

A volta a Cananor antes da torna-viagem é justificada pela síntese naval portuguesa: após embarcar a pimenta disponível em Cochim, João da Nova regressa a Cananor, onde em 30/12/1501 está pronto para iniciar a viagem de regresso.

Não incluir Ceilão/Sri Lanka. Não materializar descobertas de Ascensão/Santa Helena no loop principal enquanto a cronologia e atribuição permanecerem controvertidas e sem necessidade jogável.

## 4. Cananor

`CAN` é o único novo nó indispensável já identificado para P3.2.

Estado ao longo do gate:

1. antes de João da Nova chegar: porto soberano local, relação favorável já criada objetivamente pelo contacto de Cabral;
2. após São Brás: a expedição conhece essa favorabilidade;
3. ao final de 1501: estabelecimento de feitoria/presença portuguesa;
4. em 1502: reorganização por Vasco da Gama — fora de P3.2.

A presença institucional deve persistir após a saída da armada e não deve ser confundida com soberania ou fortificação.

## 5. Cochim

`COC` reutiliza o baseline P2. A campanha de João da Nova deve:

- chegar informada pelo aviso de São Brás;
- carregar especiarias segundo disponibilidade/documentação já estabelecida;
- não transformar Cochim em posse portuguesa;
- preservar residentes/agentes deixados por Cabral como estado local já existente.

## 6. Calecute

`CAL` não precisa aparecer como escala operacional. Seu papel em P3.2 é principalmente relacional/informacional:

- estado objetivo hostil já existe;
- a expedição só adquire conhecimento desse estado em SBR;
- a rota guiada evita o porto;
- confronto posterior associado à saída de Cananor deve ser evento específico desta expedição, não justificativa automática para sistema geral de combate.

## 7. Feitoria de Cananor

Evento candidato:

`CANNANORE_FACTORY_ESTABLISHED`

- tipo: presença institucional;
- local: `CAN`;
- período: fim de 1501;
- efeito: instituição portuguesa residente no porto;
- não altera soberania;
- não cria fortificação;
- reorganização por Vasco da Gama pertence a 1502.

## 8. Confronto de fim de 1501

Fonte oficial portuguesa registra que, em 30/12, os navios estavam em Cananor prontos para regressar quando uma grande esquadra de Calecute bloqueou a saída. A documentação posterior descreve combate entre 31/12/1501 e início de janeiro de 1502.

Para a primeira normalização:

- registrar `CANNANORE_BLOCKADE_1501` / evento específico;
- consequência mínima: atraso/ameaça e liberação da rota de retorno após o confronto;
- não implementar ainda tática naval, artilharia detalhada, perdas humanas genéricas ou sistema de combate;
- se P3-func precisar de escolha jogável nesse ponto, abrir gate próprio antes de generalizar.

## 9. Retorno

A expedição regressa ao reino em 1502. A data diária exata de chegada e as atribuições tradicionais de descobertas de ilhas permanecem menos firmes que a cronologia Malabar e não são necessárias para o primeiro incremento funcional.

Para o primeiro P3-func, basta:

- iniciar torna-viagem após Cananor/confronto;
- reutilizar rota do Cabo de modo compatível com dados existentes;
- encerrar a campanha em Lisboa em 1502 com intervalo/data documental a refinar antes de `GUIDED` diário completo.

## 10. Schema necessário

A proposta exige somente capacidades já próximas da arquitetura atual:

- nova expedição/sequência de rotas;
- novo nó `CAN`;
- evento one-shot de aquisição de informação em `SBR`;
- presença institucional persistente em `CAN`;
- evento histórico específico de bloqueio/confronto;
- conhecimento separado entre Coroa e expedição.

Não exige:

- sistema geral de mensagens;
- frota individual detalhada;
- combate naval geral;
- Ceilão;
- doença/mortalidade sistêmica;
- crédito/câmbio complexo.

## 11. Divergências preservadas

- fontes diferem na data exata de partida em literatura secundária; o projeto adota 05/03/1501 pela listagem EVE/FCSH;
- autoria/data diária da mensagem de São Brás permanece abaixo do fato essencial da transmissão;
- hipóteses de Ceilão e atribuições de ilhas atlânticas permanecem fora do loop;
- data exata de chegada a Lisboa em 1502 deve ser refinada antes de uma cronologia diária fechada.

## Decisão de gate

P3.2-doc oferece base suficiente para futura normalização mínima sem novos sistemas gerais. O próximo subgate da issue #110 deve tratar a segunda viagem de Vasco da Gama em 1502–1503, porque ela reorganiza Cananor/Cochim e introduz uma força que permanece no Índico — mudança institucional mais importante que ampliar prematuramente a simulação de João da Nova.