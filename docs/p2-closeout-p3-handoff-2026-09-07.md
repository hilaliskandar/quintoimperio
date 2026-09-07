# Fechamento P2 e handoff para P3 — 2026-09-07

## Estado consolidado

P2 — Cochim e primeiros apoios portugueses no Malabar está concluído nos gates documental e funcional mínimo.

Referências:
- P2-doc: issue #103 — concluída;
- subgates documentais: #104–#107 — concluídos;
- P2-func: issue #108 — concluída;
- PR de integração: #109;
- merge em `main`: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`;
- CI pós-merge: run `34122650263` — success;
- baseline: `docs/p2-cochin-baseline.md`.

## Conteúdo estabilizado de P2

O baseline incorpora Cochim sem nova mecânica específica:

- nó `COC`, `FOREIGN_PORT`, acesso `FOREIGN_NEGOTIATED`;
- âncora moderna de trabalho 9.9671, 76.2440, confiança espacial `MEDIUM`;
- autoridade institucional local, sem harmonização artificial do nome pessoal do governante;
- comunidades mercantis Mappila e cristã síria como atores agregados documentados;
- `PEPPER` como única mercadoria indispensável no primeiro incremento;
- conexão `R_CAL_COC` como `PREEXISTING_NETWORK`, não como criação portuguesa;
- negociação e comércio reutilizando regras gerais já existentes.

Continuam explicitamente fora de P2: `EXP_CABRAL_1500` jogável, fortificação/guarnição de 1503+, guerra, preços históricos inventados, crédito/câmbio sistêmico e cesta comercial ampliada por retroprojeção.

## Decisão de gate

Não há pendência explícita no escopo de P2 que impeça a abertura de P3. Qualquer ampliação adicional de Cochim será tratada apenas se uma necessidade concreta de P3 a exigir e deverá voltar a um subgate documental estreito.

P3 deve começar por documentação das expedições de 1500–1505, antes de qualquer nova campanha executável.

## P3 — objetivos do gate documental

1. construir inventário cronológico das expedições portuguesas de 1500–1505 relevantes ao loop;
2. identificar composição e comando das armadas somente no nível sustentado pelas fontes;
3. normalizar itinerários, escalas, perdas e eventos que alterem materialmente o estado de campanha;
4. distinguir conexões preexistentes do Índico de rotas efetivamente percorridas pelas armadas portuguesas;
5. identificar mudanças institucionais e comerciais produzidas ou reveladas por cada expedição;
6. separar fatos de 1500–1502, 1503 e 1504–1505 para evitar retroprojeção;
7. mapear quais sistemas já existentes suportam as novas expedições e quais lacunas realmente exigem nova mecânica;
8. produzir proposta mínima de integração funcional somente ao final do gate.

## Hipóteses que não devem ser assumidas

P3 não autoriza automaticamente:
- sistema geral de combate;
- tripulação individual;
- doença/mortalidade sistêmica;
- naufrágio/encalhe genéricos;
- crédito, câmbio ou contratos complexos;
- reputação/diplomacia global;
- economia monetária histórica completa;
- modelagem integral de toda armada portuguesa entre 1500 e 1505.

Esses sistemas somente entram se o corpus documental e o loop demonstrarem necessidade concreta.

## Sequência de trabalho

P3-doc deve ser executado em ordem:

1. inventário das expedições e corpus disponível;
2. matriz cronológica e por expedição;
3. cartografia e itinerários;
4. atores/comando e consequências institucionais;
5. comércio e acesso apenas quando materialmente necessários;
6. lacunas e divergências;
7. proposta mínima de normalização;
8. somente então abertura de P3-func.

## Disciplina de memória

Cada subgate deve registrar no repositório a evidência, decisão, issue/commit e próximo passo, com espelho correspondente no Drive. P1 e P2 permanecem baselines de regressão e não devem ser reabertos por conveniência de implementação.