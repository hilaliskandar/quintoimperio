# Roteiro de produção

## Estado consolidado

A vertical slice Lisboa–Calecute está concluída. Os gates **M0–M8 estão atendidos**. O **P1 — retorno da primeira viagem** também está concluído nos gates documental, funcional, playtest e interface/persistência.

A definição funcional e metodológica do MVP está em `docs/mvp-gate.md`. O histórico de balanceamento, agência e risco está em `docs/development-log.md`; o fechamento documental do retorno está em `docs/p1-closeout.md`; o procedimento de continuidade em `docs/p1-roadmap-handoff-2026-09-07.md`; e o fechamento funcional/interface em `docs/return-p1-wave19-results.md` e `docs/p1-ui-return-interface-results.md`.

Princípio permanente: **dados históricos e parâmetros de simulação permanecem separados; fatos históricos não são recalibrados para resolver jogabilidade**.

## Definição do MVP concluído

O MVP é a vertical slice da primeira viagem portuguesa de 1497–1498, com fase simulada de preparação a partir de 6 de julho, partida histórica preservada em 8 de julho de 1497 e encerramento após a primeira estadia jogável e operação comercial elegível em Calecute.

O fluxo canônico percorre:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`.

O jogador consegue, sem `TECHNICAL` ou override de teste:

1. participar da armada e percorrer as dez pernas normalizadas;
2. lidar com permanências históricas, espera, serviços, provisões e condição;
3. manter separadas cronologia `GUIDED` e trajetória `COUNTERFACTUAL`;
4. utilizar o piloto documentado de Melinde quando aplicável;
5. tratar conhecimento, acesso institucional e relações como estados distintos;
6. realizar operação comercial jogável em mercado documentado;
7. acompanhar objetivos e condição explícita de encerramento;
8. salvar e restaurar o estado;
9. enfrentar contingência estocástica reproduzível sem antecipação do evento;
10. passar pela CI, smoke tests, baterias sintéticas e diagnósticos de robustez.

## Gates M0–M8

| Gate | Escopo | Status |
|---|---|---|
| M0 | saneamento pós-merge e organização do backlog | CONCLUÍDO |
| M1 | campanha Lisboa–Calecute ponta a ponta | CONCLUÍDO |
| M2 | relações mínimas por atores documentados | CONCLUÍDO |
| M3 | comércio operacional | CONCLUÍDO |
| M4 | objetivos e encerramento da campanha | CONCLUÍDO |
| M5 | interface v0.2 | CONCLUÍDO |
| M6 | persistência JSON versionada | CONCLUÍDO |
| M7 | balanceamento e robustez | CONCLUÍDO |
| M8 | gate final do MVP | CONCLUÍDO |

## Robustez incorporada ao baseline

O fechamento inicial de M7 foi ampliado por playtests sintéticos e diagnósticos posteriores. Esses ensaios não reabrem M7; refinam seu baseline de regressão.

### Planejamento logístico

A campanha dispõe de fase pré-partida e painel que distingue duração da próxima perna, horizonte até o próximo abastecimento documentado, autonomia atual, margem heurística de 20 dias e evidência indeterminada de provisões no destino. A margem é `SIMULATION`, não exigência histórica.

### Contingência estocástica

A mesma seed aplicada ao mesmo estado é determinística; seeds diferentes podem produzir resultados distintos.

Em `GUIDED`, observações históricas exatas preservam o timing documentado. Eventos que alterariam duração são suprimidos quando incompatíveis com esse timing, mas eventos `observed_timing_safe` podem afetar provisões ou condição.

Os eventos atuais incluem efeitos positivos e negativos. `MAJOR_PROVISION_LOSS` representa uma cauda rara de perda extensa de provisões; `STRUCTURAL_STRAIN` introduz perda de condição. Ambos são parâmetros de `SIMULATION`, não frequências históricas.

### Agência sobre risco de provisões

Playtests pareados mostraram que perdas severas de provisões podiam gerar seeds praticamente inevitáveis sem uma escolha preparatória. A solução validada foi uma reserva segregada de provisões já embarcadas, com opções 0/5/10/15/20 dias-equivalentes e custo de oportunidade. A proteção atua exclusivamente sobre `MAJOR_PROVISION_LOSS`, não cria recursos e não antecipa eventos.

### Diagnóstico de risco estrutural

No diagnóstico de 7.000 campanhas com sete arquétipos competentes e 1.000 seeds pareadas houve 3.274 ocorrências de `STRUCTURAL_STRAIN`, 185 terminaram abaixo de condição 40, nenhuma abaixo de 20 e não houve blocker `VESSEL_CONDITION_TOO_LOW` na perna seguinte.

Conclusão: **não criar mitigação estrutural sem problema de agência demonstrado**.

## Marco de versão do MVP

O commit `f308fb0e97687e34365fd23ed257a0114fd81613` permanece a referência documental do fechamento do MVP Lisboa–Calecute. A vertical slice continua como baseline de comparação para toda expansão posterior.

## Pós-MVP — primeira expansão 1498–1505

A expansão ocorre em gates pequenos e reversíveis, sem inserir todos os sistemas de uma vez.

### P1 — Retorno e reconfiguração da primeira viagem

**Status: CONCLUÍDO em 07/09/2026.**

- gate documental: issue #92 — concluída;
- schema/epílogo divergente: issue #93 — concluída;
- integração funcional: issue #99 — concluída;
- agência logística Calecute–Anjediva/Santa Maria: issue #100 — concluída;
- carena documentada em Anjediva: issue #101 — concluída;
- interface e persistência do retorno: issue #102 — concluída.

A sequência operacional estabilizada até o limite do corpo primário do `Roteiro` é:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`.

A segmentação `CAL→SMI→ANJ` substitui a antiga perna agregada `CAL→ANJ` porque a pesquisa posterior materializou o contato documentado nos Ilhéus de Santa Maria. `SMI` permanece marco náutico, sem mercado nem serviço portuário genérico.

O retorno é **opt-in**: a conclusão canônica do MVP em Calecute permanece inalterada quando a expansão não é ativada. Na interface histórica v0.2, a subcampanha pode ser continuada explicitamente até BRG.

As decisões materiais novas do retorno permanecem separadas da disponibilidade genérica dos nós:

- em SMI, uma oportunidade alimentar específica, one-shot, limitada por parâmetro `SIMULATION` e sem consumir um dia inteiro;
- em ANJ, provisões específicas da permanência documentada e carena explícita; a referência mínima validada é +2 pontos abstratos de condição;
- em BSR, abandono/queima do S. Rafael e transferência de carga permanecem eventos específicos da expedição, sem sistema geral de frota/tripulação.

A wave19 fechou o gate de robustez com **18/18 estados elegíveis concluindo o retorno, zero blockers e cronologia `GUIDED` até BRG em 25/04/1499**. Save/load durante o retorno preserva seed, expedição, sequência, escala ativa, cronologia e histórico das ações one-shot.

O epílogo posterior a 25/04/1499 continua documental e divergente, fora do loop jogável. Doença/mortalidade sistêmica, controle individual de tripulação e sistema geral de frota permanecem fora do escopo.

**Baseline funcional pós-retorno:** commit `47fb82baad1289077c048576f3bc52815d6b192f`; validação pós-integração no `main`: GitHub Actions run `34118123204`, integralmente verde.

### P2 — Cochim e primeiros apoios portugueses no Malabar

**Próximo gate: documental. Nenhuma alteração executável deve precedê-lo.**

Objetivos do gate documental P2:

1. identificar e normalizar Cochim/Kochi no recorte cronológico pertinente;
2. identificar autoridades, comunidades mercantis e outros atores relevantes apenas quando sustentados por fonte;
3. documentar regime político e de acesso, distinguindo autoridade local, soberania e relações com Calecute;
4. documentar mercados, mercadorias e conexões comerciais necessárias ao loop sem inventar séries de preços;
5. registrar rotas e escalas pertinentes com proveniência e confiança cartográfica;
6. distinguir fatos do período de 1498, 1500–1503 e desenvolvimentos posteriores, evitando retroprojeção;
7. produzir matriz de evidências, lacunas e proposta mínima de integração antes de qualquer código jogável.

Somente após o fechamento desse gate serão avaliadas consequências relacionais locais, ampliação comercial e integração mínima ao loop.

### P3 — Novas expedições 1500–1505

Depois de P2:

- expedições portuguesas subsequentes;
- competição institucional e comercial;
- contratos, crédito e intermediários apenas quando necessários ao loop e documentáveis;
- mensagens, cartas persistentes e redes pessoais de informação em gate próprio.

## Sistemas de maior risco metodológico

Não devem ser introduzidos apenas para aumentar variedade. Exigem modelo e evidência próprios:

- doença e mortalidade;
- perda de tripulação ou carga;
- controle individual de tripulação;
- encalhe e naufrágio;
- classes detalhadas de navio e desempenho relativo;
- combate e violência marítima;
- crédito, câmbio e contratos complexos;
- reputação global ou diplomacia geral;
- economia monetária histórica completa.

## Expansão 1505–1540

Somente após estabilizar 1498–1505:

- Goa;
- Ormuz;
- Malaca;
- carreiras intra-asiáticas;
- cartaz;
- comércio privado e casados;
- Coromandel, Bengala e Sudeste Asiático.

## Pesquisa histórica contínua

Continuam válidas as seguintes prioridades:

- refinar cronologias editoriais do `Roteiro` quando novas edições ou fontes permitirem;
- melhorar âncoras cartográficas provisórias sem inventar precisão;
- introduzir perfis de vento direcionais apenas quando documentados por trecho;
- normalizar novos atores somente quando houver base documental suficiente;
- ampliar cestas portuárias e rotas somente quando necessárias à campanha ou expansão;
- preservar divergências entre fontes em vez de harmonizá-las silenciosamente;
- manter parâmetros experimentais rastreáveis e testáveis por seeds reproduzíveis.

## Decisões de arquitetura preservadas

- Python 3.12 + pygame-ce no primeiro jogável;
- domínio independente da interface;
- dados históricos separados de `simulation/`;
- preços históricos não são inventados;
- linhas do mapa são arestas do grafo, não necessariamente rotas navegadas;
- conhecimento de nó, conhecimento de rota, acesso, relação e comando são estados distintos;
- personagem e Coroa mantêm estados de conhecimento separados;
- informação não copia silenciosamente conhecimento institucional;
- serviço desconhecido não é tratado como ausente nem disponível;
- ator não documentado não é criado para completar interface;
- observação histórica tem precedência sobre extrapolação;
- evento genérico não é apresentado como incidente histórico específico;
- `GUIDED` preserva timing observado, mas pode admitir efeitos `observed_timing_safe`;
- `COUNTERFACTUAL` pode receber contingência completa;
- espera não concede recursos automaticamente;
- reabastecimento e reparo exigem ação explícita;
- risco de cauda é medido antes de ser mitigado;
- nova proteção só entra quando houver evidência de problema de agência e custo de oportunidade defensável.

## Disciplina de memória

Ao final de cada gate relevante: registrar decisão, evidência, testes, issue/PR/commit e próximo passo no repositório; atualizar o espelho de acompanhamento no Drive; somente então iniciar o gate seguinte.

## Próximo gate

Abrir **P2-doc — Cochim e primeiros apoios portugueses no Malabar**. O trabalho inicial é exclusivamente documental e deve produzir uma matriz de evidências e uma proposta mínima de normalização antes de qualquer alteração executável.
