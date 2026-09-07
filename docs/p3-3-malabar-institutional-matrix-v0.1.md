# P3.3-doc — matriz institucional do Malabar 1502–1503 v0.1

Data: 2026-09-07
Issue: #113

## Objetivo

Distinguir mudanças de agente, acesso, relação e presença naval produzidas pela segunda viagem de Vasco da Gama sem converter alianças comerciais em soberania portuguesa nem eventos violentos em sistema geral de combate.

## Cochim

Estado herdado: aliança e feitoria iniciadas sob Cabral.

Mudança em 1502:
- reafirmação dos acordos com o rajá;
- Gonçalo Gil Barbosa é substituído por Diogo Fernandes Correia;
- Diogo Fernandes Correia permanece como feitor de Cochim até 1505 e também recebe função de juiz do peso da pimenta.

Interpretação:
- `relationship`: favorável/aliado, persistente;
- `access`: negociado e comercial;
- `resident_actor`: Diogo Fernandes Correia a partir de 1502;
- `sovereignty`: continua local; nenhuma posse portuguesa.

## Cananor

Estado herdado: contacto favorável sob Cabral e feitoria estabelecida sob João da Nova no fim de 1501.

Mudança em 1502:
- feitoria reorganizada;
- Gonçalo Gil Barbosa é transferido para Cananor como feitor;
- porto funciona como alternativa de carregamento e articulação contra a hegemonia comercial de Calecute.

Interpretação:
- `relationship`: favorável/negociada;
- `access`: comercial;
- `resident_actor`: Gonçalo Gil Barbosa;
- `sovereignty`: local; não portuguesa.

## Calecute

Estado herdado: ruptura e hostilidade desde dezembro de 1500.

Mudança em 1502:
- hostilidade é confirmada e intensificada;
- ocorrem bombardeio e bloqueio específicos;
- a força de Vicente Sodré permanece inicialmente ligada ao bloqueio enquanto Vasco da Gama carrega em Cochim e Cananor.

Interpretação:
- `relationship`: hostil;
- `access`: fortemente restrito/hostil;
- bombardeio e bloqueio devem ser eventos específicos da expedição;
- não criar combate naval genérico apenas por este gate.

## Força de Vicente Sodré

### Missão institucional

Vicente Sodré recebeu comando autónomo de força que deveria permanecer no Índico. A formulação das fontes associa essa força à proteção da posição portuguesa e à interdição/bloqueio das redes marítimas ligadas ao Mar Vermelho.

### Ação efetiva

Após a partida de Vasco da Gama, Sodré decide procurar embarcações muçulmanas no Mar Vermelho, deixando Cochim sem a proteção naval esperada contra Calecute.

### Consequência de modelagem

A campanha deve distinguir:
- `MISSION_ASSIGNED`: proteção/interdição estratégica;
- `OPERATIONAL_DECISION`: deslocamento para caça/presa no Mar Vermelho;
- `WORLD_EFFECT`: redução/ausência da proteção portuguesa em Cochim.

Isso cria agência histórica útil sem exigir um sistema abstrato de IA naval. Em modo guiado, a divergência observada pode ser evento/decisão documentada; em eventual modo contrafactual futuro, outras opções só deverão ser abertas se forem historicamente plausíveis e testadas.

## Temporalidade

- finais de 1502: reorganização das feitorias e carregamento;
- início de 1503: Vasco da Gama inicia retorno;
- 1503: força de Vicente Sodré permanece no Índico;
- 10/10/1503: Vasco da Gama entra em Lisboa com o grosso da armada.

## Fontes

- EVE/FCSH — Vasco da Gama;
- EVE/FCSH — Gonçalo Gil Barbosa;
- EVE/FCSH — Diogo Fernandes Correia;
- EVE/FCSH — Cananor;
- EVE/FCSH — Cochim;
- EVE/FCSH — Pedro de Ataíde.

## Decisão

As mudanças institucionais de 1502–1503 cabem majoritariamente nas estruturas já existentes de atores, relações, acesso, expedições e eventos. A única extensão potencial ainda não demonstrada é a persistência temporal de efeitos produzidos por uma força não controlada pelo jogador.