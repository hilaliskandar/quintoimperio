# P3.3-doc — Vasco da Gama 1502–1503 — matriz de evidências v0.1

Data: 2026-09-07
Issue: #113

## Escopo

Reconstrução documental da segunda viagem de Vasco da Gama, com atenção à composição da armada, cronologia, reorganização institucional no Malabar e distinção entre a frota que regressa e a força de Vicente Sodré que permanece no Índico.

## Achados principais

### Comando e composição

A EVE/FCSH registra a partida principal em 01/02/1502 sob Vasco da Gama, com Pedro Afonso de Aguiar, D. Luís Coutinho, Diogo Fernandes Correia, Gil Matoso, Francisco da Cunha, António do Campo, João Lopes Perestrelo, Gil Fernandes de Sousa, Rui de Castanheda, Brás Sodré, Vicente Sodré, Álvaro de Ataíde, Fernão Rodrigues Bardaças e António Fernandes. Uma segunda componente parte em 01/04/1502 sob Estêvão da Gama, com João de Bonagrácia, Lopo Mendes de Vasconcelos, Lopo Dias e Tomás de Carmona.

A biografia de Vasco da Gama explicita que Vicente Sodré recebeu comando autónomo sobre uma força destinada a permanecer no Índico. Essa autonomia esteve na origem do conflito que afastou Cabral do comando da armada de 1502.

### Cronologia mínima

- Fevereiro de 1502 — partida de Lisboa.
- Junho de 1502 — chegada a Sofala.
- Julho de 1502 — aproximação a Quiloa; negociação sob ameaça de bombardeamento e compromisso tributário do governante local.
- Setembro de 1502 — chegada à zona de Cananor.
- Fase seguinte — bloqueio/hostilidade dirigida a Calecute enquanto a frota portuguesa carrega em Cochim e Cananor.
- Retorno de Vasco da Gama — partida para Portugal deixando no Índico a força de Vicente Sodré.

### Reorganização institucional

Em Cochim, Vasco da Gama leva instruções para substituir Gonçalo Gil Barbosa por Diogo Fernandes Correia como feitor. Gonçalo Gil Barbosa deveria passar a Cananor.

Em Cananor, a presença iniciada sob João da Nova é reorganizada em 1502, com Gonçalo Gil Barbosa como feitor. O porto é tratado como alternativa comercial a Calecute e não como posse portuguesa.

### Calecute

A relação hostil persiste. Pedro de Ataíde participa no bombardeamento de Calecute e permanece com a força de Vicente Sodré no bloqueio do porto enquanto Vasco da Gama carrega em Cochim e Cananor.

### Força permanente

A principal inovação institucional de 1502 é a permanência de uma força naval portuguesa no Índico sob Vicente Sodré. A missão documental associada é proteger a posição portuguesa e bloquear/interditar tráfego ligado ao Mar Vermelho; posteriormente Sodré se afasta da proteção de Cochim para procurar presas no Mar Vermelho, deixando o aliado exposto.

## Consequências para modelagem

1. A armada de 1502 não deve ser tratada apenas como nova instância do padrão Lisboa–Malabar–retorno.
2. A separação entre `RETURNING_FLEET` e `RESIDENT_NAVAL_FORCE` é historicamente estrutural.
3. Cochim e Cananor requerem mudança de agentes residentes, não mudança de soberania.
4. Calecute permanece estado relacional hostil; bombardeio e bloqueio são eventos específicos, não justificativa automática para combate genérico.
5. Quiloa já existe no grafo como `KIL`; Sofala já existe como `SOF`; Cochim como `COC`; Calecute como `CAL`.
6. Cananor permanece o único nó novo indispensável herdado do gate P3.2.

## Grau de evidência

- composição nominal da armada: A/B, EVE/FCSH;
- comando autónomo de Vicente Sodré: A, EVE/FCSH;
- Sofala e Quiloa na cronologia: A/B, EVE/FCSH;
- reorganização Cochim/Cananor: A, EVE/FCSH;
- bloqueio/bombardeamento de Calecute: B/A conforme detalhe, EVE/FCSH;
- missão e desvio posterior de Vicente Sodré: A/B, EVE/FCSH.

## Fontes consultadas

- EVE/FCSH — Vasco da Gama (1469?–1524).
- EVE/FCSH — Armadas da Índia do Reinado de D. Manuel I.
- EVE/FCSH — Carreira da Índia: Capitães e Capitães-Mores.
- EVE/FCSH — Gonçalo Gil Barbosa.
- EVE/FCSH — Cananor.
- EVE/FCSH — Pedro de Ataíde.

## Pendências para fechamento

- reconstruir com maior precisão a torna-viagem de Vasco da Gama;
- determinar se Estêvão da Gama deve ser modelado como subexpedição ou reforço agregado;
- documentar o momento exato em que a força de Vicente Sodré se separa da frota principal;
- separar missão prescrita e ação efetivamente adotada por Sodré;
- verificar se a arquitetura atual suporta múltiplas forças contemporâneas sem novo schema.