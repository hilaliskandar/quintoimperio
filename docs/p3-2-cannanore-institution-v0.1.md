# P3.2-doc — Cananor: contacto, feitoria e reorganização 1501–1502 v0.1

Data: 2026-09-07
Issue: #112

## Problema

Cananor muda de estado em três momentos próximos, que não devem ser fundidos:

1. janeiro de 1501 — primeiro contacto operacional da armada de Cabral;
2. fim de 1501 — armada de João da Nova efetiva presença portuguesa por meio de feitoria;
3. 1502 — Vasco da Gama reorganiza a feitoria e deixa Gonçalo Gil Barbosa como feitor.

A EVE/FCSH registra explicitamente essa sequência. O projeto deve preservá-la para não retroprojetar instituição permanente para a visita de Cabral nem atribuir a João da Nova a reorganização posterior de Gama.

## Estado local por fase

### Fase CAN-1501A — Cabral

- porto soberano de Kolathunad/Kolathiri;
- recepção favorável;
- compra limitada de canela e gengibre;
- sem presença portuguesa permanente já consolidada;
- relação favorável documentada.

### Fase CAN-1501B — João da Nova

- destino conhecido pela expedição somente após o aviso de São Brás;
- porto efetivamente visitado;
- presença portuguesa passa a ser materializada por uma **feitoria** ao final do ano;
- o estabelecimento procura aproveitar o desvio do comércio de especiarias de Calecute.

### Fase CAN-1502 — Vasco da Gama

- feitoria reorganizada;
- Gonçalo Gil Barbosa passa a feitor de Cananor;
- esse estado pertence ao gate posterior de 1502 e não deve ser antecipado no P3.2.

## Cesta comercial

A EVE caracteriza a região de Cananor como abundante sobretudo em:

- gengibre;
- cardamomo;
- pimenta de alta qualidade, mas relativamente escassa.

Para P3.2, isso não obriga a normalizar imediatamente toda a cesta. O mínimo funcional pode limitar-se às mercadorias necessárias à narrativa comercial da expedição, preservando as demais como documentação até gate comercial específico.

## Consequências de estado candidatas

| Evento | Tipo de efeito futuro | Observação |
|---|---|---|
| contacto Cabral jan/1501 | relação/acesso local | já ocorreu antes da partida de João da Nova, mas não é conhecido por ele até adquirir informação |
| aviso SBR | conhecimento da expedição | revela Cananor como alternativa favorável |
| chegada João da Nova | acesso/mercado operacional | reutiliza relação local já favorável |
| criação da feitoria | presença institucional persistente | deve sobreviver à saída da armada |
| reorganização Gama 1502 | mudança institucional posterior | fora de P3.2 |

## Implicação arquitetural

O projeto precisa distinguir:

- conhecimento sobre a existência/favorabilidade de Cananor;
- acesso negociado ao porto;
- relação com a autoridade local;
- presença institucional portuguesa no nó.

Esses quatro estados não devem ser colapsados em um único `access_status`.

## Decisão

A feitoria de Cananor em **fim de 1501** é suficientemente sustentada para integrar a futura proposta mínima de João da Nova. Sua reorganização em 1502 pertence ao próximo gate de Vasco da Gama. Não criar fortificação ou posse portuguesa: a fortaleza de 1505 é cronologicamente posterior.