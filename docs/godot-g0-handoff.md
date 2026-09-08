# Godot G0 — handoff de migração e paridade

Data: 2026-09-08
Issue: #138
Baseline congelado: `f4fd140677b7fda49a6f97456fa0b9e6ff83a735`
CI do baseline: `34200988759` — verde
Contrato de domínio: `docs/domain-freeze-1505.md`

## Objetivo

Abrir o runtime de produção em Godot sem reescrever o domínio histórico congelado em Python. A migração deve reproduzir estados observáveis, temporalidade, bloqueios, persistência e golden states do horizonte 1497–1505; não deve copiar a arquitetura interna do runtime Pygame nem aproveitar a mudança de engine para criar mecânicas novas.

## Versão alvo

Versão inicial de referência: **Godot 4.7.2-stable**, publicada em 18/08/2026.

Fontes oficiais consultadas em 08/09/2026:

- https://godotengine.org/download/archive/4.7.2-stable/
- https://godotengine.org/article/maintenance-release-godot-4-7-2/
- https://docs.godotengine.org/en/stable/about/release_policy.html

Motivo: 4.7.2 é a manutenção estável corrente da linha 4.x; 4.8 permanece em desenvolvimento. O projeto deve fixar a versão exata durante G0 para que CI e golden tests não variem implicitamente com o editor instalado.

## Princípio de portabilidade

A unidade de migração é o **contrato observável**, não a classe Python.

Para cada componente migrado, G0 deve registrar:

1. entrada canônica;
2. saída observável;
3. invariantes;
4. golden test Python correspondente;
5. representação Godot escolhida;
6. diferença deliberada de implementação, se houver;
7. teste de paridade.

## Fontes canônicas

`data/` continua contendo evidência histórica normalizada.

`simulation/` continua contendo parâmetros de simulação/experimento.

Godot deve consumir esses diretórios diretamente ou por um artefato gerado de forma reprodutível. Não é permitido manter uma segunda cópia manual dos mesmos fatos em `.tres`, cenas ou scripts.

Se recursos Godot derivados forem necessários por desempenho, eles devem ser artefatos geráveis e descartáveis, com origem rastreável ao CSV canônico.

## Arquitetura inicial proposta

```text
godot/
  project.godot
  README.md
  autoload/
    canonical_data.gd
    domain_clock.gd
    persistence.gd
  domain/
    node_state.gd
    expedition_event.gd
    session_state.gd
  parity/
    parity_cli.gd
    fixtures/
  scenes/
    bootstrap.tscn
```

A árvore é deliberadamente mínima. Nenhuma cena de produção deve ser criada antes do harness de paridade funcionar.

## Camadas

### 1. CanonicalData

Responsável exclusivamente por carregar/validar `data/` e `simulation/`.

Regras:

- preservar strings identificadoras sem coerção numérica;
- manter campos vazios distintos de valores explícitos;
- validar cabeçalhos mínimos usados pelo runtime;
- não interpretar evidência histórica como parâmetro de simulação;
- emitir erro determinístico para arquivo/coluna obrigatória ausente.

### 2. DomainClock

Contrato mínimo equivalente ao calendário usado pelo domínio Python: data explícita, avanço controlado e serialização estável. Não deve introduzir relógio de frame ou tempo real no domínio histórico.

### 3. NodeState

Primeiro candidato de paridade porque o freeze de 31/12/1505 já possui golden state explícito.

Semântica obrigatória:

- aplicar eventos em ordem temporal;
- `RANGE` torna-se disponível conservadoramente no limite superior quando consultado pelo contrato de freeze;
- campo vazio preserva a dimensão anterior;
- soberania, acesso, relação, presença, fortificação e guarnição permanecem independentes;
- nenhum estado posterior retroage.

### 4. ExpeditionEvent

Deve reproduzir leitura, ordenação por expedição/sequência e `available_by` pelo limite superior da evidência, sem transformar o evento em sistema jogável.

### 5. SessionState/Persistence

A persistência Godot deve representar o estado pertencente à sessão. O estado histórico objetivo continua derivado de data + dados canônicos.

G0 não precisa importar automaticamente saves Python antigos. Primeiro deve ser definido um contrato de equivalência semântica e fixtures comuns. Migração de arquivos reais de save pode ser gate posterior se houver necessidade de produto.

## Determinismo e seed

Não se deve exigir identidade bit a bit entre geradores pseudoaleatórios Python e Godot como pré-condição geral. O contrato deve distinguir dois níveis:

1. **determinismo intra-engine**: mesma versão, seed e estado produzem a mesma sequência no runtime;
2. **paridade inter-engine**: para golden cases selecionados, resultado observável deve coincidir. Quando a implementação depende de PRNG, a estratégia preferencial é portar um gerador pequeno e especificado pelo projeto ou usar fixtures de decisões aleatórias explícitas, em vez de depender de algoritmos internos distintos dos engines.

A escolha final do PRNG de paridade é uma decisão ADR de G0.

## Primeiro golden state

O primeiro teste de paridade deve ser o estado documental de `31/12/1505`, por não depender de interface nem de aleatoriedade.

Nós obrigatórios:

- `KIL`;
- `SOF`;
- `ANJ`;
- `CAN`;
- `COC`;
- `MOM`.

Referências Python:

- `tests/test_f5_1505_golden_state.py`;
- `tests/test_f5_1505_freeze_persistence.py`;
- `src/quintoimperio/domain/node_state_event.py`;
- `data/node_state_events.csv`.

Gate mínimo: uma execução headless Godot deve produzir uma saída JSON determinística para esses nós, comparável a uma fixture Python congelada.

## Segundo alvo de paridade

Após o golden state temporal, migrar um fluxo pequeno sem aleatoriedade sistêmica: leitura/ordenação de `EXP_ALMEIDA_1505` e consulta de eventos disponíveis em 31/12/1505.

Referência: `tests/test_f5_almeida_authority_events.py`.

## CI proposta

Criar workflow separado para Godot, sem alterar o workflow Python existente:

1. baixar/fixar Godot 4.7.2-stable headless/standard Linux;
2. validar abertura/importação do projeto em `--headless`;
3. executar harness `godot/parity/parity_cli.gd`;
4. comparar JSON produzido com fixture esperada;
5. manter a regressão Python existente em workflow próprio.

Nenhum gate Godot deve substituir a CI Python durante a migração.

## ADRs necessários antes de ampliar implementação

- ADR-G0-01 — versão fixa do Godot e política de atualização;
- ADR-G0-02 — estratégia de dados canônicos e recursos derivados;
- ADR-G0-03 — PRNG/determinismo inter-engine;
- ADR-G0-04 — persistência e compatibilidade de saves;
- ADR-G0-05 — contrato do harness de paridade.

## Fora de escopo

- expansão histórica após 1505;
- combate geral;
- governo/vice-reinado como sistema global;
- múltiplas frotas simultaneamente controláveis;
- arte final;
- animação e áudio;
- distribuição;
- substituição ou remoção da implementação Python de referência.

## Critério de verde G0

G0 somente pode ser encerrado quando:

1. versão do engine estiver fixada e documentada;
2. projeto Godot mínimo abrir em CI headless;
3. `data/`/`simulation/` forem consumidos sem cópia factual manual;
4. primeiro golden state `31/12/1505` passar em paridade;
5. ao menos um contrato de `ExpeditionEvent` passar em paridade;
6. decisões de determinismo e persistência estiverem registradas em ADR;
7. CI Python continuar verde;
8. nenhum desvio de domínio permanecer sem classificação explícita.

## Próximo incremento

Criar o shell mínimo em `godot/`, fixar Godot 4.7.2, implementar carregamento CSV read-only e produzir a primeira fixture JSON do golden state 1505. Somente depois implementar `NodeState` em GDScript e comparar a saída no CI.
