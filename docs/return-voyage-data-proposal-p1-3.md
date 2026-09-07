# P1.3 — Proposta documental de tradução para dados

Status: proposta de implementação, ainda sem alterar `data/`.

Issue: #92.

## Princípio

A expansão pós-MVP deve introduzir somente elementos cuja natureza esteja suficientemente auditada. O retorno não é a ida invertida e combina escalas logísticas, marcos náuticos, eventos de campanha e, após o Rio Grande, trajetórias divergentes.

## Novos candidatos

### ANJ — Anjediva

- natureza: escala logística/ancoradouro;
- confiança cartográfica: `HIGH`;
- serviços historicamente sustentados no retorno: água, madeira, gêneros alimentares, carena;
- mercado: **não inferir**;
- recomendação: candidato a novo `node` operacional.

### SMI — Ilhéus de Santa Maria

- natureza: marco insular/padrão;
- confiança cartográfica: `MEDIUM` regional;
- serviços: nenhum serviço logístico robusto identificado;
- mercado: não;
- recomendação: só criar como nó se a continuidade espacial da viagem exigir; caso contrário, manter como observação/evento.

### BSR — Baixos de São Rafael

- natureza: banco/baixio + evento histórico de redução da frota;
- confiança cartográfica: `LOW-MEDIUM`;
- mercado: não;
- recomendação: nó-evento ou referência náutica; não usar coordenada urbana.

### SJO — Ilhas de São Jorge

- natureza: ilhéus próximos a Moçambique; parada breve e ritual;
- confiança cartográfica: `MEDIUM`;
- mercado: não;
- recomendação: observação ou marco náutico; não precisa ser escala plena se o motor puder registrar parada/evento curto.

### RGR — Baixos do Rio Grande

- natureza: área de sondagem/banco marítimo, associada ao Rio Grande/Geba na atual Guiné-Bissau;
- confiança: `MEDIUM-HIGH` regional e `LOW` pontual;
- mercado: não;
- recomendação: marco náutico/área de navegação; evitar ponto terrestre artificialmente preciso.

## Segmentação proposta até o fim da narrativa primária

`CAL → SMI → ANJ → MAL → BSR → SJO → SBR → CGH → RGR`

A segmentação deve preservar:

- permanência em Anjediva separada da viagem;
- travessia Anjediva–Melinde como perna de risco extremo e elevada mortalidade documentada, sem ainda criar doença genérica;
- queima do S. Rafael em BSR como evento específico da expedição;
- passagem por Zanzibar e Moçambique sem transformar essas referências em escalas operacionais de retorno;
- São Brás como escala logística forte;
- Rio Grande como limite da narrativa primária.

## Depois do Rio Grande

Não usar `expedition_routes.csv` como se toda a armada permanecesse unida. O fechamento precisa representar, pelo menos conceitualmente:

1. Bérrio / Nicolau Coelho → Cascais/Lisboa, chegada editorial preferida em 10/07/1499, variante 11/07;
2. S. Gabriel → São Tiago → Lisboa sob João de Sá, chegada antes de 28/08/1499;
3. Vasco + Paulo da Gama → São Tiago → Terceira em caravela fretada;
4. Vasco da Gama → Lisboa, com tradições concorrentes 29/08, 08/09 e 18/09.

## Necessidades de schema identificadas

Antes da implementação, verificar se o schema atual suporta sem distorção:

- `source_layer` ou equivalente para distinguir narrativa primária e síntese editorial;
- datas incertas/intervalos ou variantes documentais;
- mudança de composição da frota durante a expedição;
- mudança de comando de uma embarcação;
- trajetória de personagem diferente da trajetória de sua embarcação original;
- nós do tipo marco/baixio sem mercado e sem serviço portuário.

Se o schema já suportar esses casos por notas e campos existentes, evitar criar abstrações novas. Caso contrário, abrir issue técnica pequena e separada antes de inserir dados.

## Regra de não regressão

A implementação do retorno não deve alterar os dados, balanceamento ou comportamento do MVP Lisboa–Calecute. O commit `f308fb0e97687e34365fd23ed257a0114fd81613` permanece o baseline funcional; novos testes devem verificar que o fluxo até Calecute continua idêntico quando a expansão não é acionada.