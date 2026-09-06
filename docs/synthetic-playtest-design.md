# Playtest sintético pós-MVP

Este experimento não representa telemetria de pessoas reais. Cada execução é um jogador sintético independente, com checkout/instalação próprios no GitHub Actions, seed reproduzível e uma política decisória pré-definida limitada às ações públicas do domínio do MVP.

## Amostra

20 sessões independentes, distribuídas em cinco perfis comportamentais, quatro sessões por perfil.

- `DISCIPLINED`: segue a cronologia guiada e toma somente as ações necessárias para manter a viagem executável.
- `CAUTIOUS`: reabastece com margem maior e evita partir com recursos baixos.
- `IMPATIENT`: tenta partir antes de algumas liberações históricas, registra bloqueios e então corrige a decisão.
- `FRUGAL`: posterga reabastecimentos, aceita planos bloqueados e tenta recuperar a sessão sem override.
- `TRADER`: segue a viagem com política estável e, em Calecute, realiza uma compra comercial maior dentro da capacidade e do capital disponíveis.

Os perfis não recebem conhecimento interno inacessível ao jogador. O runner usa somente estado e ações oferecidos pelo domínio da campanha.

## Métricas por sessão

- conclusão e objetivo final;
- seed e perfil;
- número de ações tentadas e executadas;
- tentativas bloqueadas;
- dias simulados e data final;
- localização final;
- modo `GUIDED`/`COUNTERFACTUAL`;
- reabastecimentos e quantidade total reabastecida;
- condição mínima e provisões mínimas observadas;
- eventos marítimos registrados;
- negociações de acesso;
- operações comerciais;
- capital final e carga final;
- distância em ações para uma trajetória de referência disciplinada;
- recuperação após primeiro bloqueio.

## Interpretação

Os resultados servem para avaliar robustez sistêmica, recuperabilidade, sensibilidade a políticas de decisão e custo operacional do loop. Não medem compreensão visual, diversão, frustração, interesse histórico ou experiência humana de uso; esses itens exigem playtest com participantes reais.
