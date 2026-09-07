# Handoff P1 — retomada, memória e próximos gates

Data: 2026-09-07

## Finalidade

Este registro preserva o procedimento adotado para retomar o projeto após o fechamento do MVP Lisboa–Calecute e define a sequência imediata de trabalho conforme `docs/roadmap.md`. Ele não substitui as matrizes documentais específicas; funciona como memória operacional e gate de continuidade.

## Procedimento de retomada adotado

1. Conferir o arquivo de handoff/conversa fornecido pelo projeto e identificar o último estado explicitamente registrado.
2. Ler o `README.md` atual do repositório para não assumir que o handoff representa o estado mais recente.
3. Conferir `docs/roadmap.md`, issues abertas e commits posteriores ao commit de referência do MVP.
4. Comparar o estado documental com o estado executável antes de propor nova implementação.
5. Não reabrir gates já concluídos nem recalibrar dados históricos para resolver problemas de jogabilidade.
6. Registrar decisões relevantes no GitHub e manter espelho de acompanhamento no Google Drive.

## Estado encontrado

O commit de referência documental do MVP Lisboa–Calecute é `f308fb0e97687e34365fd23ed257a0114fd81613`. Depois dele, o P1 avançou além do ponto registrado no handoff:

- `76a90e761471f59346946a4a75bb74b0148a9671`: documentação do retorno e auditoria de gaps de schema;
- `dd38cc5cf76cc6edd3b6d4de2409170ec046658c`: dados documentais do retorno até os Baixos do Rio Grande;
- `3e12049620cc7c4946393ebf05c5b79173ab7de6`: epílogo divergente do retorno de 1499, preservando datas alternativas e trajetórias separadas sem refatoração ampla do domínio.

A issue #93 foi concluída. A issue-mãe #92 permanece aberta e deve funcionar como gate de fechamento de P1.

## Regra de continuidade

Não voltar às frentes de balanceamento do MVP, à frota física experimental, à reserva logística ou ao diagnóstico de `STRUCTURAL_STRAIN` salvo regressão demonstrada. Esses resultados pertencem ao baseline.

P1 deve ser fechado antes de iniciar P2. A expansão deve continuar em incrementos pequenos, reversíveis, testáveis e documentalmente rastreáveis.

## Próximos gates

### P1.5 — auditoria final e fechamento documental

Confrontar os critérios da issue #92 com os artefatos já incorporados. Confirmar explicitamente:

- matriz de evidências por perna;
- segmentação operacional do retorno;
- cronologia e distinção entre corpo do `Roteiro`, reconstruções editoriais e síntese pós-manuscrito;
- composição/redução da frota e mudança de comando onde documentadas;
- escalas, abastecimentos, reparos, perdas e mortalidade apenas nos limites suportados pelas fontes;
- âncoras cartográficas e respectivos graus de confiança;
- lacunas residuais de pesquisa;
- tratamento do epílogo divergente e das datas alternativas.

Se todos os critérios estiverem atendidos, registrar comentário conclusivo na #92 e encerrá-la como concluída. Se houver lacuna, abrir issue estreita para ela em vez de ampliar P1 indefinidamente.

### P1.6 — regressão e integração funcional mínima do retorno

Após o fechamento documental, verificar quais dados do retorno já podem ser consumidos pelo domínio atual sem refatoração. Preservar as dez pernas do MVP e saves existentes. Adicionar apenas o necessário para permitir continuidade pós-Calecute até o limite documental executável definido em P1.

Critérios de saída:

- CI integral verde;
- MVP Lisboa–Calecute sem regressão;
- retorno percorrível no recorte definido;
- datas e eventos documentais preservados;
- epílogo pós-manuscrito não apresentado como certeza operacional quando a evidência é divergente.

### P1.7 — playtest do retorno

Executar smoke test canônico e bateria sintética pequena com seeds reproduzíveis. O objetivo inicial não é balancear, mas detectar blockers, estados impossíveis, problemas de cronologia e escolhas sem agência.

Somente abrir ajuste de balanceamento quando um problema for demonstrado. Não alterar fatos históricos para corrigir jogabilidade.

### P1.8 — documentação e baseline pós-retorno

Atualizar README, roadmap, diário de desenvolvimento e documentação de método pertinente. Registrar commit de referência do retorno estabilizado e preservar o MVP anterior como baseline de regressão.

### P2 — Cochim e primeiros apoios portugueses no Malabar

Somente depois de P1 estabilizado:

1. gate documental de Cochim e atores relevantes;
2. mercados e regimes de acesso documentados;
3. consequências relacionais locais sustentadas por fonte;
4. expansão comercial sem séries de preços inventadas;
5. integração mínima ao loop;
6. regressão e playtests.

### P3 — expedições de 1500–1505

Somente depois de P2:

- normalizar expedições subsequentes;
- introduzir competição institucional e comercial de modo incremental;
- contratos, crédito e intermediários apenas quando necessários e documentáveis;
- mensagens, cartas persistentes e redes pessoais de informação em gate próprio.

## Sistemas mantidos fora do escopo imediato

Doença/mortalidade sistêmica, controle individual de tripulação, naufrágio/encalhe, classes detalhadas de navios, combate, crédito/câmbio complexos, reputação global e economia monetária histórica completa continuam condicionados a necessidade jogável demonstrada e evidência suficiente.

## Disciplina de memória do projeto

Ao final de cada gate relevante:

1. atualizar ou criar documento técnico no repositório;
2. vincular issue/PR/commit correspondente;
3. registrar resultado, decisão e próximo gate;
4. atualizar o espelho de acompanhamento no Drive;
5. somente então avançar para o gate seguinte.

Essa rotina passa a ser requisito de continuidade do projeto.