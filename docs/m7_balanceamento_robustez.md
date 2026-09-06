# M7 — Balanceamento e robustez

## Objetivo

O gate M7 verifica se a vertical slice Lisboa–Calecute permanece concluível e determinística sem becos sem saída artificiais, sem geração gratuita de recursos e sem exploração trivial dos parâmetros de simulação.

Este gate não altera fatos históricos para melhorar a jogabilidade. Qualquer calibração eventualmente necessária deve ocorrer exclusivamente em `simulation/`.

## Estratégia de validação

A suíte `tests/test_mvp_robustness.py` adiciona cinco invariantes de regressão.

### 1. Campanha GUIDED em múltiplas seeds

A campanha completa é executada nas seeds `0`, `1`, `7`, `42` e `1498` usando somente as ações normais do domínio: viagem, reabastecimento explícito, espera histórica e contato com a autoridade de Melinde.

Como as dez pernas da campanha possuem observações históricas utilizadas pela cronologia `GUIDED`, eventos genéricos de simulação devem permanecer suprimidos. Por isso, todas as seeds devem produzir o mesmo estado terminal em Calecute, em 21 de maio de 1498.

Esse teste protege simultaneamente:

- continuidade das dez pernas;
- suficiência do teto abstrato de provisões quando o jogador usa serviços documentados;
- precedência das observações históricas sobre ruído de simulação;
- determinismo da vertical slice guiada.

### 2. Eventos marítimos em COUNTERFACTUAL

Uma viagem contrafactual a partir de Moçambique é planejada em 100 seeds.

Para cada seed são exigidos:

- plano determinístico quando repetido com o mesmo estado e seed;
- no máximo um evento por viagem;
- atraso máximo de 3 dias;
- perda adicional máxima de 5 pontos de condição;
- marcação explícita `simulation_only`;
- frequência observada abaixo de 60% no conjunto de 100 seeds.

O último limite é um sentinela de regressão, não uma estimativa histórica de incidência de tempestades, calmarias ou avarias.

### 3. Comércio e arbitragem local

Após a chegada normal a Calecute e negociação explícita de acesso, são realizadas cinco sequências consecutivas de compra e venda de uma unidade de pimenta no mesmo mercado e na mesma seed.

O capital deve cair a cada ciclo. A regra protege contra arbitragem circular trivial criada pelo próprio modelo. O spread já existente em `simulation/trade_rules.csv` continua sendo parâmetro de simulação e não margem histórica.

### 4. Não vazamento de informação

Um estado localizado em Hurmuz sem conhecimento operacional de mercado deve produzir `MarketView.entries == ()` e mercado não acionável. Relações ainda não estabelecidas também não podem aparecer em `contacted_relationships`.

O objetivo é garantir que dados estruturais disponíveis ao motor não sejam automaticamente convertidos em informação disponível ao jogador.

### 5. Espera sem recursos gratuitos

A espera necessária para uma partida histórica altera o relógio, mas preserva provisões, condição, capital/carga, conhecimento e relações. Serviços materiais continuam exigindo ações explícitas.

## Parâmetros observados antes da medição

Nenhum parâmetro foi alterado antes dos testes M7.

Os valores relevantes já existentes são:

- compra: multiplicador `1.05`;
- venda: multiplicador `0.95`;
- condição mínima para partida: `20`;
- consumo: `1` dia-equivalente de provisão por dia de viagem;
- provisões máximas a bordo: `120` dias-equivalentes;
- evento genérico: no máximo um por viagem, com atraso e perda de condição limitados pelas regras atuais.

Esses números permanecem parâmetros abstratos de simulação. A aprovação do gate apenas indica que eles não geram uma falha óbvia dentro da vertical slice do MVP; não os transforma em estimativas históricas.

## Critério de saída

M7 pode ser encerrado quando:

1. a nova suíte passa integralmente junto com todos os testes anteriores;
2. a CI completa permanece verde;
3. não existe achado concreto bloqueador na revisão do PR;
4. eventual ajuste de parâmetro, se necessário, estiver restrito a `simulation/` e documentado.

Se os testes passarem sem recalibração, a decisão correta é preservar os parâmetros atuais e avançar para M8, evitando ajuste sem evidência de problema.