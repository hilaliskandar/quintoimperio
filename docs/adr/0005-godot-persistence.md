# ADR 0005 — Persistência Godot e compatibilidade semântica

Status: **aceito**

Data: 2026-09-08

## Contexto

O runtime Python possui persistência JSON versionada. O freeze de 31/12/1505 demonstrou que o save deve conter o estado pertencente à sessão e sua data, enquanto o estado histórico objetivo dos nós é recomposto a partir dos dados canônicos. A migração não deve duplicar o mundo histórico dentro do arquivo de save.

## Decisão

A persistência Godot seguirá os mesmos invariantes sem exigir, em G0, identidade byte a byte com o JSON Python.

O contrato mínimo é:

- schema explicitamente versionado;
- versão do engine/runtime registrada;
- data e estado pertencente à sessão persistidos;
- seed/estado aleatório persistidos quando necessários à retomada determinística;
- identificadores canônicos preservados como strings;
- estado histórico objetivo recomposto de `data/` + data da sessão;
- nenhuma cena, nó visual ou estado efêmero de interface tratado como fonte do domínio.

Compatibilidade com arquivos de save Python existentes é uma capacidade opcional posterior. Se houver necessidade de produto, deverá ser implementada por adaptador/migração explícita e testada contra fixtures; não será obtida por acoplamento artificial da arquitetura Godot às classes Python.

## Consequências

- Godot pode adotar uma estrutura de save apropriada ao engine sem romper os invariantes do domínio;
- a referência Python continua utilizável para comparação sem obrigar o novo runtime a reproduzir sua representação interna;
- alterações futuras de schema exigem migração versionada;
- o golden state histórico continua independente do formato do save.
