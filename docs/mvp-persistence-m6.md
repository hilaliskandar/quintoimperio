# Gate M6 — Persistência

## Objetivo

O M6 permite interromper e retomar a vertical slice do MVP sem alterar a semântica do estado de campanha. O formato inicial é JSON, possui versão explícita de schema e usa um único slot local.

## Schema v1

O documento raiz contém:

- `schema_version`: versão inteira do formato, atualmente `1`;
- `seed`: seed da sessão usada para decisões determinísticas;
- `state`: representação integral de `GameSessionState`.

O bloco `state` preserva:

- navio: nó atual, data, provisões e condição;
- comércio: capital, capacidade e carga;
- conhecimento pessoal por nó e por rota;
- estados de acesso portuário;
- relações com atores documentados;
- expedição e sequência de perna ativas;
- modo cronológico `GUIDED` ou `COUNTERFACTUAL`;
- escala histórica ativa;
- histórico de oportunidades de informação já consumidas;
- histórico de eventos marítimos de simulação.

Datas são gravadas em ISO 8601. Enums são gravados por valor semântico, exceto `KnowledgeLevel` e `RelationshipStatus`, que são enums ordinais e usam seus inteiros estáveis no schema v1.

## Round-trip

`CampaignPersistence.dumps` e `loads` recompõem explicitamente cada dataclass do domínio. O critério de integridade é igualdade estrutural do `GameSessionState` carregado com o estado salvo, não apenas equivalência visual.

O teste de round-trip inclui deliberadamente carga, relação contatada, histórico de informação, evento de viagem, escala ativa e cronologia contrafactual, além dos demais registros já existentes no estado.

## Determinismo

A seed é parte do save. O teste de determinismo compara o próximo `VoyagePlan` calculado antes do save com o plano calculado após carregar o mesmo estado e reutilizar a seed persistida.

## Slot único na interface

`prototype/game_m6.py` estende a interface M5 com dois comandos visíveis:

- `Salvar [S]`;
- `Carregar [L]`.

O caminho padrão é `quintoimperio-save.json` e pode ser substituído por `--save-path` em execução técnica. Após o load, seleção de mercadoria, seleção de rota, confirmação modal e histórico curto da interface são limpos porque não pertencem ao domínio persistente.

## Validação de versão

Um arquivo com `schema_version` diferente de `1` é recusado explicitamente. O M6 não implementa migração automática porque ainda não existem versões históricas do schema a migrar.

## Smoke

A CI executa um smoke que:

1. cria o estado histórico inicial;
2. salva em JSON;
3. altera o estado em memória executando uma viagem;
4. carrega o slot;
5. exige que o estado restaurado seja exatamente igual ao original;
6. renderiza a interface M6 restaurada.

## Fora do escopo

Múltiplos slots, perfis, sincronização em nuvem e migrações sofisticadas permanecem fora do MVP. O arquivo também não guarda estado transitório de apresentação.
