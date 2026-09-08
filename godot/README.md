# Runtime Godot — G0

Este diretório inicia a migração do runtime de produção após o `Python 1505 GREEN`.

## Versão fixada

Godot `4.7.2-stable`.

O gate G0 trata o Python como implementação de referência e `docs/domain-freeze-1505.md` como contrato do domínio 1497–1505. A migração não autoriza expansão histórica ou alteração de mecânicas congeladas.

## Dados canônicos

O runtime lê diretamente os diretórios irmãos `../data/` e `../simulation/`. Arquivos `.tres`, cenas e scripts Godot não devem conter cópias manuais de fatos históricos ou parâmetros que já pertençam a essas fontes.

`autoload/canonical_data.gd` resolve o diretório raiz do repositório a partir de `res://`, abre CSVs canônicos e preserva campos vazios como strings vazias.

## Smoke G0

Execução local, com Godot 4.7.2 disponível no PATH:

```bash
godot --headless --path godot --editor --quit
godot --headless --path godot --script res://parity/parity_cli.gd
```

O segundo comando deve terminar com código zero e imprimir uma linha `PARITY_SMOKE=...` confirmando a leitura de `data/node_state_events.csv`.

A CI Godot é separada da regressão Python. Nenhum workflow Godot substitui a suíte histórica existente.
