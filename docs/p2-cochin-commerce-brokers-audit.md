# P2-doc — cesta comercial e mediação mercantil de Cochim, 1500–1503

Issue: #106.

Data: 2026-09-07.

## Critério

A auditoria separa quatro coisas que não podem ser colapsadas:

1. mercadoria produzida no hinterland;
2. mercadoria transportada para Cochim;
3. mercadoria efetivamente disponível/carregada no porto;
4. mercadoria regional do Malabar sem prova específica para Cochim no recorte.

Também separa presença de uma comunidade na cidade de evidência de atuação como intermediário do comércio português.

## Cesta mínima

### Pimenta — `HIGH`

A pimenta é a única mercadoria que já possui evidência suficientemente forte para futura normalização direta em Cochim no recorte inicial.

Evidência convergente:

- `PRAKASH_ECE` afirma que, depois da ruptura em Calecute, foi mais conveniente deslocar o centro de aquisição de pimenta para Cochim;
- Prakash identifica Mappila e mercadores cristãos sírios como brokers/intermediários usados pelos portugueses na aquisição de pimenta;
- EVE/FCSH caracteriza Cochim como importante elo de ligação ao Malabar e principal porto de carregamento de pimenta nas embarcações portuguesas na fase inicial;
- a cronologia da armada de João da Nova registra a existência de pimenta preparada/embarcada a partir da feitoria de Cochim.

**Semântica recomendada:** `MARKET/TRANSIT`, não produção local automática. Prakash salienta que o rajá de Cochim não controlava efetivamente as áreas onde a pimenta era cultivada nem todas as rotas usadas para transportá-la ao porto.

### Especiarias genéricas — `HIGH` como categoria narrativa, insuficiente como `good_id`

A reconstrução documental da armada de Cabral afirma que as naus foram carregadas de “especiarias” em Cochim em 12–15 dias. Isso prova função comercial do porto, mas não autoriza distribuir a carga por espécies individuais sem fonte específica.

Portanto, `SPICES_GENERIC` é evidência narrativa; não deve virar bem agregado se o domínio trabalha com mercadorias específicas.

### Gengibre — `MEDIUM`

João de Barros, ao narrar a armada de João da Nova de 1501, distingue as mercadorias que o rei de Cananor oferecia e registra que parte delas — entre as quais gengibre — também poderia ser tomada em Cochim. A crónica é posterior aos acontecimentos e deve ser hierarquizada abaixo da documentação contemporânea.

Cabral comprou gengibre em Cananor na saída de janeiro de 1501; esse fato não deve ser reatribuído a Cochim.

**Decisão:** gengibre é candidato secundário defensável para Cochim, mas não deve ser necessário ao primeiro loop P2 se pimenta bastar.

### Canela — `MEDIUM/LOW` para Cochim

A mesma passagem de Barros sobre João da Nova sugere disponibilidade de canela em Cochim, embora Cananor apareça como ponto preferencial para receber canela/gengibre e outras drogas.

Na cronologia de Cabral, a compra explicitamente identificada de canela ocorre em Cananor, não Cochim.

**Decisão:** não inserir canela na cesta mínima de Cochim apenas para ampliar variedade. Pode ser mantida como candidata histórica secundária.

### Cardamomo — `REGIONAL_ONLY`

Prakash inclui cardamomo entre as exportações da costa do Malabar por volta de 1500. Isso é evidência regional, não específica de Cochim.

**Decisão:** não normalizar em Cochim neste gate sem evidência portuária específica.

### Têxteis, coco e derivados — `REGIONAL_ONLY`

Prakash registra têxteis, coco e produtos derivados entre exportações da costa. Não há ainda evidência suficiente de que devam compor a cesta jogável de Cochim em 1500–1503.

**Decisão:** não inserir.

## Meios de pagamento e problema de liquidez

A literatura sobre a chegada de João da Nova em 1501 descreve um problema central: Gonçalo Gil Barbosa teria recebido mercadorias portuguesas para vender e converter em recursos de compra, mas esses bens tinham baixa aceitação, enquanto mercadores de especiarias preferiam pagamento em prata/dinheiro.

A evidência é plausível e coerente com o problema geral já observado na primeira viagem de Gama, porém a auditoria ainda não possui uma peça contemporânea individual diretamente transcrita para a operação de Cochim.

**Decisão:** registrar `SILVER/CASH_PREFERENCE` e baixa liquidez de mercadoria europeia como mecanismo histórico a pesquisar, mas não criar taxa de câmbio, preço ou obrigação monetária no P2-doc.

Dados de preços ou instrumentos de pagamento de 1503/1510+ podem servir como controle temporal, nunca como valor de 1500.

## Comunidades mercantis

### Mappila — atuação como intermediários `HIGH/MEDIUM`

Prakash afirma explicitamente que, na transferência da aquisição de pimenta para Cochim, Mappila mais cooperativos foram usados como brokers/intermediários pelos portugueses.

Isso é evidência funcional, não apenas presença demográfica.

**Proposta futura:** comunidade mercantil candidata a ator local, com rótulo próprio e sem transformar `MAPPILA` em categoria homogênea para toda a costa. O período e o `actor_id` devem ser delimitados na proposta final P2-doc.

### Cristãos sírios / Nasrani — atuação como intermediários `HIGH/MEDIUM`

Prakash inclui mercadores cristãos sírios entre brokers/intermediários usados na aquisição de pimenta em Cochim. A EVE também registra presença antiga de cristãos nasranis na cidade.

A cronologia de Cabral encontra cristãos siro-malabares em Cranganor, o que não deve ser confundido com o evento comercial específico de Cochim; a evidência de mediação em Cochim vem de Prakash, não desse episódio de Cranganor.

**Proposta futura:** comunidade mercantil candidata a ator local separado de Mappila.

### Comunidade judaica — presença `HIGH`, mediação portuguesa no recorte `UNPROVEN`

A EVE registra comunidade judaica em Cochim no período anterior/da chegada portuguesa. Não foi localizada, nesta auditoria, evidência suficiente para atribuir a ela função específica de broker da feitoria em 1500–1503.

**Decisão:** não normalizar como ator jogável apenas porque a comunidade existia.

### Pardesi / mercadores do Mar Vermelho — contexto regional, não ator local automaticamente

Prakash distingue conflitos portugueses com mercadores `pardesi`, especialmente em Calecute, das relações mais cooperativas com Mappila em partes do Malabar.

**Decisão:** não copiar o ator mercantil de Calecute para Cochim sem evidência local específica.

## Matriz de decisão

| Elemento | Evidência Cochim 1500–1503 | Proposta mínima |
|---|---|---|
| `PEPPER` | forte e específica | incluir futuramente |
| `GINGER` | específica, crónica posterior | opcional; não necessária ao primeiro P2-func |
| `CINNAMON` | indício específico, preferência por Cananor | não incluir no mínimo |
| `CARDAMOM` | regional Malabar | não incluir |
| têxteis | regional Malabar | não incluir |
| coco/derivados | regional Malabar | não incluir |
| Mappila brokers | funcionalmente documentados | candidato a ator/comunidade |
| cristãos sírios brokers | funcionalmente documentados | candidato a ator/comunidade |
| judeus | presença documentada | não criar ator jogável sem função documentada |
| prata/dinheiro | forte plausibilidade histórica; evidência fina ainda incompleta | nota/mecânica futura, sem preço nem câmbio neste gate |

## Consequência para o loop

O primeiro P2-func não precisa de uma nova economia completa. Uma extensão mínima pode ser historicamente defensável com:

- Cochim como mercado/entreposto local preexistente;
- `PEPPER` como mercadoria comercial central;
- acesso negociado com o rajá;
- pelo menos uma comunidade intermediária documentada, se a camada relacional exigir ator mercantil;
- sem preço histórico inventado: o motor continua usando índice `SIMULATION` onde já previsto;
- sem converter o rajá em controlador do hinterland ou conceder estoque automaticamente.

## Fontes

- `PRAKASH_ECE`, caps. 1–2.
- EVE/FCSH, “Cochim” e “Armada da Índia de 1500”.
- João de Barros, *Décadas da Ásia*, livro referente à armada de João da Nova, usado como fonte cronística de força inferior à documentação contemporânea para a disponibilidade de gengibre/canela.
- literatura de controle sobre João da Nova e a feitoria, usada apenas para o problema de liquidez, sem normalização monetária nesta fase.

## Gate

A #106 pode ser encerrada para o escopo mínimo. Pimenta é a cesta necessária; Mappila e cristãos sírios são os únicos candidatos mercantis com função de mediação já sustentada. A próxima lacuna é cartográfica e, depois dela, a consolidação da proposta mínima de normalização P2-doc.
