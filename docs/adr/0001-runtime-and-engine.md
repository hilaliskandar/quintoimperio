# ADR 0001 — Runtime e motor do primeiro jogável

Status: **aceito**

Data: 2026-09-05

## Contexto

O projeto já possui uma base histórica em CSV, um protótipo econômico puro em Python e testes determinísticos executados no CI. O primeiro jogável será um jogo 2D de comércio, navegação e informação, com forte uso de menus, mapa, estados de porto e simulação econômica. Não há necessidade prevista de física complexa, 3D ou edição de cenas sofisticadas nesta fase.

Foram consideradas duas alternativas principais:

1. **Python + Pygame** — continuidade direta do protótipo, integração simples com CSV, testes e ferramentas de dados.
2. **Godot** — melhor editor visual, sistema de cenas e UI, exportação multiplataforma e maior estrutura para um produto mais amplo.

## Decisão

Adotar **Python 3.12 + pygame-ce** para o primeiro jogável, mantendo o núcleo de domínio independente da camada gráfica.

A simulação não deve depender de Pygame. A arquitetura será dividida em:

- `src/quintoimperio/domain/` — economia, tempo, navegação, conhecimento, reputação e estado do jogo;
- `src/quintoimperio/data/` — carregamento e validação das tabelas;
- `src/quintoimperio/ui/` — mapa, telas de porto, mercado, viagem e componentes visuais em Pygame;
- `data/` — evidência histórica estruturada;
- `simulation/` — parâmetros de balanceamento explicitamente não históricos;
- `tests/` — testes do domínio e invariantes históricas.

O protótipo atual em `prototype/economy.py` será migrado gradualmente para `src/quintoimperio/domain/` e permanecerá como referência apenas durante essa transição.

## Razões

### Continuidade técnica

O núcleo econômico já foi validado em Python com oito testes determinísticos. Manter a mesma linguagem reduz duplicação e risco de divergência entre um modelo de referência em Python e uma implementação de produção em outra linguagem.

### Compatibilidade com a natureza do jogo

O primeiro escopo é predominantemente 2D, baseado em mapa, menus e transições de estado. Pygame é suficiente para esse tipo de jogo sem introduzir a estrutura adicional de um motor de cenas completo.

### Pesquisa e dados

A pesquisa histórica, geração de tabelas, cálculos de distância, projeções cartográficas e futuras rotinas de QA já se beneficiam do ecossistema Python. A mesma linguagem facilita manter a cadeia pesquisa → dados → simulação → jogo.

### Testabilidade

O domínio continuará executável sem janela gráfica. Isso permite testes rápidos no GitHub Actions e evita que a interface se torne requisito para validar a economia e a navegação.

### Distribuição

A distribuição desktop poderá ser tratada posteriormente com empacotamento do executável. Essa etapa não é um requisito para validar o primeiro loop jogável.

## Consequências

- Pygame não poderá conter regras de negócio; deverá apenas apresentar e encaminhar comandos ao domínio.
- A UI exigirá mais construção manual que em Godot.
- O mapa deve partir de coordenadas e dados reais, e não de geografia gerada por IA.
- Os saves serão inicialmente arquivos JSON versionados; SQLite só será introduzido se o estado persistente justificar.
- O projeto evitará dependências adicionais de UI até existir uma necessidade concreta.

## Critérios para reconsiderar Godot

A decisão deve ser reavaliada se pelo menos um destes fatores se tornar dominante:

- necessidade de suporte amplo a controle/gamepad e múltiplas plataformas;
- crescimento importante da complexidade de animações e cenas;
- UI cuja manutenção manual em Pygame passe a consumir mais esforço que o domínio;
- necessidade de ferramentas visuais para autores não programadores;
- dificuldade prática de empacotamento/distribuição do runtime Python.

Uma eventual migração deverá preservar os CSVs históricos, os parâmetros em `simulation/` e testes de comportamento como especificação do domínio.
