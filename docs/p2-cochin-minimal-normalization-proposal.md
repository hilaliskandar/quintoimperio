# P2-doc — proposta mínima de normalização de Cochim

Issue principal: #103.

Subgates concluídos: #104, #105, #106, #107.

Data: 2026-09-07.

Status: **proposta documental**. Este arquivo não altera `data/`, `simulation/` nem código. Sua finalidade é fixar o menor conjunto de linhas que um futuro P2-func poderá implementar e testar.

## Princípio de corte

O objetivo não é reproduzir toda a evolução de Cochim entre 1500 e 1505. É introduzir apenas o que já está documentalmente sustentado e é necessário para um primeiro loop local:

- um porto existente antes dos portugueses;
- uma autoridade local com a qual se negocia acesso;
- pimenta como mercadoria central de trânsito/exportação do hinterland;
- comunidades mercantis documentadas como intermediárias;
- uma conexão costeira com Calecute;
- presença portuguesa inicial registrada como contexto/evento, sem converter a cidade em posse portuguesa.

Fortificação, guarnição, guerra de 1503–1504, administração vice-real, novas armadas e sistema geral de feitorias ficam fora do primeiro P2-func, salvo quando estritamente necessários à consistência histórica.

# 1. Fonte/proveniência a acrescentar antes dos dados

A implementação deverá primeiro normalizar em `docs/sources.md` identificadores estáveis para as fontes novas efetivamente usadas. Proposta:

- `OLIVEIRA_COSTA_CABRAL_1500` — João Paulo Oliveira e Costa, cronologia da Armada da Índia de 1500 em *Descobridores do Brasil* / reprodução EVE/FCSH;
- `EVE_COCHIN` — José Luís Ferreira, “Cochim”, Enciclopédia Virtual da Expansão Portuguesa, 2009;
- `HPIP_COCHIN` — entrada Kochi/Cochim do Heritage of Portuguese Influence;
- `CANAVARRO_GGB_2000` — Ana Rita Canavarro, “Gonçalo Gil Barbosa”, em *Descobridores do Brasil*, 2000, somente se a implementação precisar projetar a feitoria/feitor como registro próprio.

`PRAKASH_ECE` e `SUBRAHMANYAM_PEA` já existem e continuam fontes de controle centrais.

# 2. Nó `COC`

Linha conceitual proposta para `nodes.csv`:

| campo | valor proposto | base |
|---|---|---|
| `node_id` | `COC` | identificador novo sem colisão conhecida |
| `historical_name` | `Cochim` | terminologia portuguesa do corpus |
| `modern_name` | `Kochi` | identificação moderna inequívoca |
| `latitude` | `9.9671` | HPIP |
| `longitude` | `76.2440` | HPIP |
| `coordinate_confidence` | `MEDIUM` | identidade segura, ponto histórico aproximado em sistema estuarino transformado |
| `node_type` | `FOREIGN_PORT` | porto relevante, mas menor que Calecute c. 1500 |
| `polity_1497` | `Perumpadappu Swarupam / Cochim` | polidade local anterior à presença portuguesa |
| `political_status` | nova categoria descritiva a validar: `SUBORDINATE_LOCAL_POLITY` | hegemonia/suzerania de Calecute sem incorporação territorial simples |
| `access_regime` | `FOREIGN_NEGOTIATED` | Cabral obtém acesso por negociação com o rajá |
| `active_from` | vazio | porto/polidade preexistente; não afirmar data fundacional |
| `known_to_portugal_1497` | `UNKNOWN` | não há evidência suficiente para conhecimento operacional português prévio |
| `player_default_knowledge` | `UNKNOWN` | não conceder conhecimento por retroprojeção |
| `market_scale` | `REGIONAL` | porto menor que Calecute c. 1500, embora entreposto real |
| `naval_services` | vazio/`UNKNOWN` conforme schema | não inventar capacidade portuária genérica |
| `provisions` | vazio/`UNKNOWN` | não inferir da cidade mercantil |
| `repair` | vazio/`UNKNOWN` | não retroprojetar infraestrutura posterior |
| `pilot_availability` | vazio/`UNKNOWN` | sem evidência específica |
| `broker_availability` | `HIGH` ou categoria equivalente existente | intermediários Mappila/cristãos sírios documentados; validar sem criar efeito automático |
| `royal_presence` | `NONE` | presença régia portuguesa, não autoridade local; a autoridade local entra em `actors.csv` |
| `fortification` | `NONE` para estado inicial | Forte Manuel é posterior, 1503 |

### Nota histórica recomendada

> Porto de Cochim/Kochi, centro do Perumpadappu Swarupam no sistema lagunar de Vembanad. Em 1500 era porto mercantil menor que Calecute, mas recebeu a armada de Cabral e tornou-se base de aquisição de especiarias, sobretudo pimenta. A coordenada usa a área histórica de Kochi/Fort Kochi–Mattancherry como âncora moderna aproximada e não representa o ponto exato do ancoradouro ou da feitoria. A aliança portuguesa não converte o porto em posse portuguesa; fortificação e guarnição pertencem ao ciclo de 1503.

# 3. Autoridade local

Proposta para `actors.csv`:

```text
ACT_COC_RAJA_1500,Rajá de Cochim / Trimumpara (Thirumalpad),LOCAL_AUTHORITY,1500,1503,...
```

Notas obrigatórias:

- ator institucional, não biografia individual;
- `Trimumpara` tratado como forma portuguesa de titulatura associada a `Thirumalpad/Tirumulpadu`;
- variantes de nome pessoal `Unni Goda Varma Koil Thirumalpad` e `Unni Rama/Raman Koil I` permanecem não resolvidas;
- não codificar `GODA` ou `RAMA` no `actor_id`.

Grau recomendado: `A` para existência/função da autoridade; a incerteza nominal fica na nota e não reduz a evidência do cargo.

Proposta para `node_actors.csv`:

```text
COC,ACT_COC_RAJA_1500,AUTHORITY,1500,1503,...
```

A função é gate de negociação local; não implica que toda transação de mercado exija audiência pessoal com o rajá.

# 4. Comunidades mercantis

## Mappila

Proposta de candidato:

```text
ACT_COC_MAPPILA_MERCHANTS,Mercadores Mappila de Cochim,MERCHANT_COMMUNITY,1500,1505,...
```

`node_actors.csv`:

```text
COC,ACT_COC_MAPPILA_MERCHANTS,MERCHANT_COMMUNITY,1500,1505,...
```

Grau recomendado: `B`, `NODE_DIRECT`, `PRAKASH_ECE`.

Nota: Prakash os identifica como brokers/intermediários cooperativos na aquisição portuguesa de pimenta em Cochim. Não representam todos os Mappila da costa nem bloco político homogêneo.

## Cristãos sírios / Nasrani

Proposta de candidato:

```text
ACT_COC_SYRIAN_CHRISTIAN_MERCHANTS,Mercadores cristãos sírios de Cochim,MERCHANT_COMMUNITY,1500,1505,...
```

`node_actors.csv`:

```text
COC,ACT_COC_SYRIAN_CHRISTIAN_MERCHANTS,MERCHANT_COMMUNITY,1500,1505,...
```

Grau recomendado: `B`, `NODE_DIRECT`, `PRAKASH_ECE|EVE_COCHIN`.

Nota: Prakash os identifica como intermediários da aquisição de pimenta; a EVE confirma presença nasrani antiga na cidade. O episódio de cristãos encontrados por Cabral em Cranganor não deve ser usado como substituto desta evidência específica de Cochim.

## Comunidade judaica

**Não normalizar no primeiro P2-func.** A presença na cidade é documentada, mas não foi demonstrada função necessária ao loop ou mediação específica da feitoria em 1500–1503.

# 5. Mercadoria mínima

Única linha indispensável em `node_goods.csv`:

```text
COC,PEPPER,1500,1505,EXPORT,HINTERLAND,FOREIGN_NEGOTIATED,FALSE,TRUE,A,NODE_DIRECT,PRAKASH_ECE|EVE_COCHIN,,...
```

Nota recomendada:

> Pimenta adquirida/carregada em Cochim a partir de redes de produção e transporte do hinterland do Malabar. A linha não afirma produção dentro da cidade nem controle do rajá sobre as áreas produtoras ou todas as rotas de abastecimento.

### Mercadorias explicitamente fora do mínimo

- `GINGER`: candidato secundário, evidência específica de força menor;
- `CINNAMON`: não necessário; Cabral a compra explicitamente em Cananor;
- `CARDAMOM`: evidência regional do Malabar, não suficiente para linha direta em Cochim;
- `TEXTILE_IND`, `COCONUT`, `GOLD`, `SILVER`, `HORSE`, `AROMATICS`: não copiar da cesta regional de Calecute.

A eventual preferência por prata/dinheiro como meio de pagamento deve permanecer em nota/pesquisa; não criar preço histórico nem taxa de câmbio.

# 6. Ligação costeira Calecute–Cochim

Proposta mínima para `routes.csv`:

```text
R_CAL_COC,CAL,COC,COASTAL_OCEANIC,PREEXISTING_NETWORK,1450,1505,MALABAR_COASTAL,MEDIUM,,...
```

Princípios:

- a conexão é parte da rede costeira anterior à presença portuguesa;
- Cabral utiliza o eixo em dezembro de 1500, mas não “cria” a rota;
- `route_origin=PREEXISTING_NETWORK` evita converter a viagem portuguesa em origem da conectividade;
- não inserir duração observada precisa até existir data de partida suficientemente segura; a chegada a Cochim em 24/12/1500 é mais segura que o dia exato de saída de Calecute;
- não criar `EXP_CABRAL_1500` em P2. A modelagem das novas armadas pertence ao P3;
- conhecimento inicial do jogador deve permanecer baixo/indeterminado até o desenho do cenário P2.

Fonte mínima proposta: `PRAKASH_ECE|OLIVEIRA_COSTA_CABRAL_1500`.

# 7. Feitoria de 1500/1501

A feitoria é fato documental importante, mas **não precisa de uma nova entidade de domínio no primeiro P2-func**.

O mínimo pode registrá-la:

- na nota histórica do nó;
- na documentação da campanha/cenário;
- eventualmente como evento datado, se o futuro loop exigir passagem temporal de dezembro de 1500 para 1501.

Não criar neste momento:

- `ROYAL_FACTORY` como `political_status` do porto;
- `PORTUGUESE_POSSESSION`;
- fortificação antes de 1503;
- ator português específico para o feitor, salvo se houver mecânica relacional que efetivamente o utilize.

A auditoria #104 estabelece:

- Gonçalo Gil Barbosa como primeiro feitor de trabalho a partir da passagem de Cabral;
- Diogo Fernandes Correia como substituto em 1502;
- formulação divergente de Subrahmanyam preservada em nota.

# 8. Relação Cochim–Calecute

Não criar, no primeiro P2-func, uma relação binária de “posse”.

A semântica documental é:

- Cochim = polidade local;
- Samudri = poder hegemônico/suserano regional;
- obrigações tributárias/interferência política são documentadas na literatura;
- a aliança portuguesa busca ampliar a autonomia de Cochim;
- essa relação pode ser projetada futuramente como evento/conflito ou relação entre atores/polidades, se o domínio ganhar essa camada.

Por ora, a nota do nó e o `political_status` descritivo bastam.

# 9. O que o primeiro P2-func NÃO deve fazer

- não recriar a armada de Cabral inteira;
- não alterar o baseline Lisboa–Calecute/P1;
- não retroprojetar a fortaleza de 1503 para 1500;
- não tratar Cochim como posse ou colônia portuguesa;
- não copiar a cesta de Calecute;
- não inventar preços, estoques ou câmbio;
- não conceder produção local de pimenta;
- não resolver artificialmente o nome pessoal do rajá;
- não transformar todas as comunidades presentes em atores jogáveis;
- não criar guerra, combate, crédito sistêmico ou administração vice-real.

# 10. Critérios sugeridos para abrir P2-func

O P2-func pode ser aberto se a #103 aceitar esta proposta e se comprometer a implementar apenas:

1. fontes novas necessárias;
2. nó `COC`;
3. `PEPPER` em Cochim;
4. autoridade local;
5. Mappila e cristãos sírios apenas se a camada relacional precisar deles no loop mínimo;
6. rota `R_CAL_COC` como rede costeira preexistente;
7. smoke/testes que provem ausência de retroprojeção e regressão do MVP/P1.

Qualquer ampliação além disso deve ser justificada por um novo subgate documental.

# 11. Estado das lacunas

- cronologia Cabral–feitoria: resolvida metodologicamente em #104;
- autoridade/titulatura/relação com Calecute: resolvida metodologicamente em #105, preservando variante nominal;
- cesta comercial e intermediários: resolvida para o mínimo em #106;
- cartografia: resolvida em #107;
- preços/câmbio: deliberadamente não resolvidos e não necessários;
- novas armadas: P3;
- guerra/fortificação de 1503+: gate posterior.

## Decisão proposta

A #103 possui evidência suficiente para ser encerrada como gate documental. O próximo passo não deve ser nova pesquisa ampla, mas abrir **P2-func — integração mínima de Cochim**, com escopo fechado por este documento e implementação isolada em branch própria.
