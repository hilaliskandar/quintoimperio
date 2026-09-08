# ADR 0006 — Harness de paridade Python ↔ Godot

Status: **aceito**

Data: 2026-09-08

## Contexto

A migração deve provar equivalência de comportamento sem copiar classes Python. O projeto precisa de uma fronteira clara entre o que é contrato e o que é detalhe de implementação.

## Decisão

Adotar um harness headless baseado em fixtures JSON e saídas estruturadas.

Cada contrato migrado deverá declarar:

1. baseline Python de referência;
2. entrada canônica;
3. fixture ou checkpoint esperado;
4. saída Godot estruturada;
5. condição de falha não ambígua;
6. CI própria, separada da regressão Python.

O harness corrente é `godot/parity/parity_cli.gd`. Ele deverá encerrar com código diferente de zero para qualquer divergência.

Primeiros contratos G0:

- `NodeStateEventModel`: golden state de `31/12/1505` para `ANJ`, `CAN`, `COC`, `KIL`, `MOM`, `SOF`, incluindo limites superiores de eventos `RANGE`;
- `ExpeditionEventModel`: ordenação e disponibilidade temporal de `EXP_ALMEIDA_1505`.

O workflow `.github/workflows/godot-parity.yml` fixa a versão do Godot, valida abertura headless e executa o harness. A CI Python existente permanece obrigatória e independente.

## Regra de aceitação

Uma diferença entre Python e Godot somente pode ser aceita quando estiver:

- documentada;
- classificada como diferença de representação e não de comportamento; ou
- aprovada por ADR que altere explicitamente o contrato.

Diferenças não explicadas bloqueiam o gate de migração.

## Consequências

- os golden tests passam a ser especificação executável de portabilidade;
- implementações internas podem divergir sem perder controle sobre o comportamento;
- novos contratos podem ser adicionados incrementalmente ao harness;
- a futura retirada de Pygame como UI de produção não remove o Python como referência de regressão enquanto a migração estiver em curso.
