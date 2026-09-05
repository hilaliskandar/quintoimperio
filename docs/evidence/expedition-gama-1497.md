# Evidência — armada de Vasco da Gama, 1497–1499

## Escopo

Esta ficha sustenta apenas uma camada institucional mínima para a primeira campanha: havia uma armada com comando nomeado e uma sequência documentada de deslocamentos até Calecute. Ela **não** define a identidade do protagonista, não afirma que Vasco da Gama pilotava pessoalmente cada trecho e não transforma a cadeia de comando em conhecimento náutico individual.

## Fontes

### Malyn Newitt — `NEWITT_PEW`

Em *Portugal in European and World History*, no capítulo sobre os descobrimentos, Newitt descreve a preparação de uma pequena frota de quatro navios em 1497. Segundo a síntese, D. Manuel investiu relativamente pouco na expedição, uma embarcação foi fornecida pelo banco Marchioni e Vasco da Gama, juntamente com seu irmão Paulo, foi nomeado para o comando. Newitt observa também que a frota estava mal preparada para a missão diplomática que encontraria no Índico.

Uso no projeto:

- existência de uma expedição organizada em 1497;
- chefia nomeada de Vasco da Gama;
- financiamento não reduzido a uma operação puramente estatal, pois ao menos uma embarcação tinha participação do banco Marchioni;
- cautela contra representar a armada como máquina estatal plenamente preparada.

### Sanjay Subrahmanyam — `SUBRAHMANYAM_PEA`

Em *The Portuguese Empire in Asia, 1500–1700*, Subrahmanyam trata Vasco da Gama como capitão-mor da expedição e reconstrói a sequência principal: saída do Tejo em 8 de julho de 1497, chegada ao Cabo da Boa Esperança em 19 de novembro, contato com Moçambique no início de março de 1498, passagem por Mombaça e Melinde e partida de Melinde em 24 de abril para Calecute. A mesma discussão registra especialistas embarcados e, no trecho final, a dependência de conhecimento local que o projeto já representa pelo piloto guzerate de Melinde.

Uso no projeto:

- sequência temporal e espacial das pernas agregadas de `EXP_GAMA_1497`;
- distinção entre comando da armada e especialistas/pilotos;
- confirmação de que a expedição portuguesa se apoiou em conhecimento que não era simplesmente conhecimento pessoal do capitão ou de cada participante.

## Tradução para o domínio

`data/expeditions.csv` registra a expedição e sua chefia. `data/expedition_routes.csv` registra cinco pernas agregadas que já existem em `routes.csv`:

1. `R_LIS_CGH` — Lisboa → Cabo da Boa Esperança;
2. `R_CGH_MOZ` — Cabo → Moçambique;
3. `R_MOZ_MOM` — Moçambique → Mombaça;
4. `R_MOM_MAL` — Mombaça → Melinde;
5. `R_MAL_CAL` — Melinde → Calecute.

Essas arestas são abstrações do grafo. Não afirmam navegação sem escalas, derrota exata ou controle institucional de todos os mares atravessados.

## Regra de modelagem

A base `FLEET_COMMAND` significa somente: um personagem que esteja participando da expedição ativa pode acompanhar a perna corrente sob o comando institucional da armada mesmo sem possuir conhecimento náutico individual `OPERATIONAL` daquela rota.

A regra não:

- aumenta o conhecimento pessoal antes da partida;
- concede bônus de velocidade, segurança, consumo ou desgaste;
- substitui um piloto documentado quando ele existe;
- autoriza rotas fora da sequência da expedição;
- fixa ocupação, estatuto social ou biografia do protagonista.

Depois de completar a viagem, o aprendizado individual segue `simulation/session_rules.csv`, como em qualquer outra rota efetivamente percorrida.

## Limitações

A camada v0.1 não modela ainda hierarquia completa de capitães, mestres, pilotos, escrivães, marinheiros e soldados, nem ordens régias específicas por navio. Também não modela disciplina, remuneração, propriedade das embarcações ou divisão de risco entre Coroa e financiadores. Esses elementos exigem documentação adicional antes de virar mecânica.
