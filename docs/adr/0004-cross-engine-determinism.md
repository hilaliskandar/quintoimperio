# ADR 0004 — Determinismo e aleatoriedade entre Python e Godot

Status: **aceito**

Data: 2026-09-08

## Contexto

O domínio Python usa seeds e seeds sentinela em partes da simulação. Python e Godot não devem ser presumidos como possuindo o mesmo algoritmo interno de geração pseudoaleatória, nem a mesma semântica de seleção a partir de uma seed. Exigir igualdade de PRNG nativo criaria dependência frágil de implementação; ignorar a questão tornaria impossível distinguir divergência de regra de divergência de sorteio.

## Decisão

Adotar um contrato em dois níveis.

### Determinismo intra-engine

Dentro de uma versão fixada do runtime, mesma seed + mesmo estado + mesmos dados canônicos devem produzir a mesma sequência observável. O save Godot deverá registrar informação suficiente para retomar essa sequência quando o estado aleatório fizer parte da sessão.

### Paridade inter-engine

A equivalência Python ↔ Godot será testada pelo comportamento do domínio sob uma **fita explícita de decisões aleatórias** (`decision tape`) nos casos em que a regra dependa de sorteio.

A referência Python poderá exportar, para seeds sentinela selecionadas, a sequência de decisões/draws que efetivamente alimenta o domínio. O Godot reproduzirá a mesma fita no harness de paridade. Assim, divergência de regra fica separada de divergência entre PRNGs nativos.

G0 não exige identidade bit a bit entre `random.Random` do Python e o gerador interno do Godot.

Se o produto futuro exigir que uma mesma seed textual produza exatamente a mesma campanha em engines diferentes, deverá ser introduzido por ADR posterior um PRNG especificado pelo projeto, com vetores de teste próprios. Essa necessidade não foi demonstrada no freeze 1505.

## Consequências

- golden states determinísticos sem aleatoriedade podem ser comparados diretamente;
- testes estocásticos podem comparar regras usando a mesma fita de decisões;
- o runtime Godot pode usar seu gerador determinístico interno em produção enquanto sua versão estiver fixada;
- seeds sentinela Python permanecem referência diagnóstica, mas não são automaticamente promessas de identidade numérica cross-engine.
