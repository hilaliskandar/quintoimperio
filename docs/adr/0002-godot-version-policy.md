# ADR 0002 — Versão do Godot e política de atualização

Status: **aceito**

Data: 2026-09-08

## Contexto

O `Python 1505 GREEN` congelou o domínio 1497–1505 no commit `f4fd140677b7fda49a6f97456fa0b9e6ff83a735`. A migração precisa de uma versão de engine reproduzível em desenvolvimento e CI; acompanhar automaticamente a versão mais recente introduziria variação não controlada no harness de paridade.

Na abertura de G0, Godot 4.7.2 era a manutenção estável corrente da linha 4.x, publicada em 18/08/2026. A linha 4.8 ainda estava em desenvolvimento.

## Decisão

Fixar **Godot 4.7.2-stable** como runtime de referência de G0.

No CI Linux x86_64, usar exatamente o artefato oficial:

`Godot_v4.7.2-stable_linux.x86_64.zip`

com SHA-256:

`cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.

A versão não será atualizada automaticamente. Uma mudança de versão exige gate explícito com:

1. atualização deste ADR ou ADR sucessor;
2. execução do harness de paridade;
3. regressão Python integralmente verde;
4. registro de qualquer mudança observável do engine;
5. decisão explícita sobre compatibilidade de saves e artefatos derivados.

## Consequências

- builds e CI de G0 tornam-se reproduzíveis quanto à versão do engine;
- correções futuras do Godot não entram silenciosamente no runtime;
- a migração para uma nova versão estável é permitida, mas passa por gate de compatibilidade;
- o número da versão do engine deve aparecer nos outputs de paridade e nos saves Godot quando a persistência for implementada.

## Relação com ADR 0001

O ADR 0001 permanece válido como registro da decisão que levou ao primeiro jogável em Python/Pygame. Este ADR não o invalida retroativamente: registra o novo runtime de produção após o fechamento do domínio Python.
