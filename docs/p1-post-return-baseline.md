# P1.8 — baseline pós-retorno estabilizado

Data: 2026-09-07

## Estado

P1 está encerrado nos gates documental, funcional, playtest, interface e persistência.

Issues concluídas:

- #92 — reconstrução e auditoria documental do retorno;
- #93 — schema mínimo e epílogo divergente;
- #99 — integração funcional do retorno até BRG;
- #100 — agência logística Calecute–Anjediva/Santa Maria;
- #101 — carena documentada em Anjediva;
- #102 — interface e persistência do retorno.

## Baselines

Baseline histórico do MVP Lisboa–Calecute:

`f308fb0e97687e34365fd23ed257a0114fd81613`

Baseline funcional pós-retorno:

`47fb82baad1289077c048576f3bc52815d6b192f`

Validação pós-integração desse baseline no `main`:

GitHub Actions run `34118123204` — integralmente verde.

Commits posteriores que alteram somente documentação do fechamento não redefinem o baseline funcional.

## Fluxos preservados

MVP:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`

Retorno opt-in:

`CAL → SMI → ANJ → MAL → BSR → SBR → CGH → BRG`

O retorno não substitui o encerramento canônico do MVP. O jogador pode concluir o MVP em Calecute sem ativar `EXP_GAMA_RETURN_1498`.

## Invariantes de regressão

1. `EXP_GAMA_1497` continua com dez pernas.
2. A conclusão do MVP exige operação comercial elegível em Calecute; chegada ou negociação isolada não bastam.
3. `TECHNICAL` continua separado do cenário histórico.
4. Save/load v2 continua compatível e não ganhou schema específico para o retorno.
5. `GUIDED` preserva observações históricas exatas; divergência explícita muda para `COUNTERFACTUAL`.
6. Espera não gera recursos.
7. Serviços desconhecidos não são convertidos em disponíveis ou ausentes.
8. SMI é marco náutico, não mercado nem porto genérico.
9. Provisões de SMI e carena/provisões de ANJ são ações específicas da expedição; quantidades abstratas permanecem `SIMULATION`.
10. A queima/abandono do S. Rafael em BSR permanece evento específico; não existe sistema geral de frota/tripulação.
11. Doença/mortalidade sistêmica permanece fora do domínio jogável atual.
12. O pós-25/04/1499 permanece epílogo documental divergente, fora do loop.

## Robustez de referência

A wave19, com seeds e arquétipos reproduzíveis, produziu:

- 18 estados elegíveis após conclusão do MVP;
- 18 retornos concluídos;
- 0 blockers finais;
- cronologia `GUIDED` em todos os casos concluídos;
- chegada a BRG em 25/04/1499.

A solução foi obtida sem recalibrar fatos históricos para jogabilidade:

- a lacuna logística inicial foi resolvida pela segmentação documental de Santa Maria e por uma oportunidade alimentar específica;
- blockers de condição foram resolvidos por ação explícita de carena documentada em Anjediva;
- sensibilidade mostrou 2 pontos abstratos como menor restauração testada suficiente para a seed crítica.

## Persistência

Ações one-shot do retorno são registradas como identificadores `RETURN_ACTION:<stop_id>:<action>` em `information_history`, já persistido no schema v2. O teste dedicado verifica seed, `active_expedition_id`, `expedition_leg_sequence`, `active_stop_id`, `chronology_mode`, localização e não repetição após load.

## Documentos de referência

- `docs/p1-closeout.md`
- `docs/p1-roadmap-handoff-2026-09-07.md`
- `docs/return-p1-wave19-results.md`
- `docs/santa-maria-logistics-p1-func.md`
- `docs/p1-ui-return-interface-results.md`
- `docs/roadmap.md`

## Próximo gate autorizado

**P2-doc — Cochim e primeiros apoios portugueses no Malabar.**

O gate deve começar exclusivamente por pesquisa e normalização documental. Nenhum mercado, ator, regime de acesso, relação ou rota jogável de Cochim deve ser acrescentado antes de existir matriz de evidências e proposta mínima de integração.
