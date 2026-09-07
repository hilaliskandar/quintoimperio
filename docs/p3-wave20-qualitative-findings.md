# P3 wave20 — análise qualitativa pareada

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`
Fonte reproduzível: `tools/analyze_p3_wave20_qualitative.py`
Resultado bruto: `docs/p3-wave20-qualitative-analysis.json`
Workflow: `.github/workflows/p3-wave20-qualitative-analysis.yml`
Run inicial persistente: `34144945973`

## Objetivo

Explicar por que a baseline corrigida da wave20 produz 144/220 conclusões, distinguindo efeito da política do jogador, intensidade da seed e defeitos remanescentes do runner.

## Resultado principal

A matriz pareada confirma que o modelo agora discrimina políticas em vez de impor um blocker estrutural comum. A taxa global permanece 144/220 (65,45%).

A hierarquia é estável:

- SURVIVALIST: 19/20;
- COMPLETIONIST: 18/20;
- GRAND_STRATEGIST, MERCHANT, OPTIMIZER, ROLEPLAYER e CASUAL: 16/20;
- EXPLORER: 15/20;
- RANDOM_PER_LEG: 12/20;
- ROGUELIKE: 0/20;
- SPEEDRUNNER: 0/20.

## Classes de seed

A análise classifica as seeds pela quantidade de arquétipos que concluem:

- alta tensão: `24001`, `24002`, `24010`;
- falha universal: `24019`;
- discriminantes: incluem `24003`, `24005`, `24006`, `24008`, `24009`;
- baixa tensão: `24004`, `24007`, `24011`, `24012`, `24013`, `24014`, `24015`, `24016`, `24017`, `24018`, `24020`.

Não há seed de sucesso universal porque ROGUELIKE e SPEEDRUNNER falham mesmo em cenários de baixa tensão.

## Seeds de alta tensão

### 24001

Somente COMPLETIONIST e SURVIVALIST concluem. Entre os demais, sete falham em COC e dois em ANJ. As perdas líquidas de provisões nos perfis convencionais ficam em torno de -22,77; GRAND_STRATEGIST reduz a perda efetiva observada para -12,77 e ROLEPLAYER para -17,77, mas ainda não concluem.

Interpretação: a seed exige margem/reserva superior à política padrão. A sobrevivência de COMPLETIONIST e SURVIVALIST é evidência de diferenciação estratégica, não de acesso desigual a escalas.

### 24002

Novamente apenas COMPLETIONIST e SURVIVALIST concluem. As falhas se distribuem mais cedo e por mais nós: ANJ 5, CAL 1, COC 1, KIL 1 e MOZ 1. A perda líquida típica é -24,64; GRAND_STRATEGIST registra -14,64 e ROLEPLAYER -19,64.

Interpretação: choque adverso mais distribuído ao longo da rota. A mesma seed consegue separar políticas de reserva ampliada das políticas de margem padrão.

### 24010

Apenas SURVIVALIST conclui. As dez falhas distribuem-se por ANJ 2, CAL 3, COC 3 e KIL 2. As perdas líquidas variam entre -9,93 e -33,61 conforme a trajetória/política; COMPLETIONIST, apesar da margem superior à maioria, falha nesta seed.

Interpretação: é o melhor caso de teste para a diferença entre `margem` e `reserva protegida`. Deve ser preservado como seed sentinela em futuras regressões.

## Seed 24019 — cauda adversa

Nenhum dos onze grupos conclui. Nove terminam em ANJ, um em COC e um em MOZ. As perdas líquidas são severas: -54,15 para vários perfis; -34,15 no GRAND_STRATEGIST; -24,15 no COMPLETIONIST; e ainda -19,77 no SURVIVALIST.

O fato de SURVIVALIST chegar mais longe e reduzir fortemente a perda efetiva, mas ainda assim falhar, é compatível com uma cauda estocástica extrema. Não há evidência, nesta análise, de escala documental perdida ou fallback incorreto. A seed deve permanecer como sentinela de estresse, não ser calibrada para produzir sucesso obrigatório.

## Falhas estruturais por política

### ROGUELIKE

Falha 20/20. Os pontos finais concentram-se em ANJ 12, MAL 5, MOZ 2 e KIL 1. `INSUFFICIENT_PROVISIONS` aparece nas 20 sessões. Isso é coerente com uma política que aceita risco e não protege margem suficiente para uma campanha longa.

### SPEEDRUNNER

Falha 20/20. Além de insuficiência de provisões, acumula grande quantidade de blockers cronológicos (`HISTORICAL_DEPARTURE_NOT_REACHED` e `HISTORICAL_STOP_NOT_RELEASED`). O resultado é coerente com a política de não esperar adequadamente janelas históricas. Não há razão para tornar a cronologia permissiva apenas para permitir que esse arquétipo conclua.

### EXPLORER

Falha em `24001`, `24002`, `24009`, `24010` e `24019`, totalizando 15/20 conclusões. Seu desempenho intermediário confirma o desenho: o piso preventivo permite aproveitar oportunidades documentadas, mas a recusa da margem recomendada reduz robustez em seeds adversas.

### COMPLETIONIST e SURVIVALIST

COMPLETIONIST falha apenas em `24010` e `24019`; SURVIVALIST apenas em `24019`. Essa diferença fornece uma fronteira útil de robustez sem tornar a campanha determinística.

## Diagnóstico de anomalias

Não foi encontrada anomalia funcional que justifique nova correção neste gate:

1. as mesmas seeds adversas afetam sistematicamente múltiplos perfis;
2. políticas mais conservadoras deslocam a falha para mais adiante ou convertem falha em sucesso;
3. a seed 24019 permanece extrema mesmo sob SURVIVALIST;
4. os blockers genéricos restantes estão restritos a nós sem ação documental específica;
5. não há repetição idêntica de tentativa genérica nem tentativa genérica residual em MOZ/MAL após consumo da ação documental.

## Decisão

Congelar a calibração logística da tranche Cabral neste ponto. Não alterar `VCR +5`, `MOZ +10`, `MAL +15`, teto Cabral 150, reservas ou disponibilidade histórica para elevar artificialmente a taxa de conclusão.

Preservar como sentinelas de regressão:

- `24019`: cauda extrema/falha universal;
- `24010`: apenas SURVIVALIST conclui;
- `24001` e `24002`: COMPLETIONIST + SURVIVALIST concluem;
- uma seed de baixa tensão, preferencialmente `24004` ou `24011`, em que todos os perfis planejadores concluem e apenas ROGUELIKE/SPEEDRUNNER falham.

## Próximo gate

O próximo passo funcional não é recalibrar Cabral. É consolidar testes sentinela para essa hierarquia e, uma vez verdes, avaliar a transição do P3-func-A para a próxima expedição/estado histórico previsto no roadmap, reutilizando a arquitetura de cronologia, informação e ações documentadas sem generalizar prematuramente sistemas de combate ou serviços.