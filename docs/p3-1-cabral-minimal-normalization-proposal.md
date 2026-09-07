# P3.1-doc — proposta mínima de normalização Cabral 1500–1501

Data: 2026-09-07
Issue: #111

## Objetivo

Definir o menor conjunto de dados que permitiria, em gate funcional posterior, representar a armada de Pedro Álvares Cabral sem introduzir sistemas gerais de combate, frota, tripulação ou comunicação.

Este documento é **somente proposta documental**. Nenhuma linha abaixo deve ser gravada em `data/` antes de abertura explícita de P3-func.

## 1. Expedição principal candidata

`EXP_CABRAL_1500`

- líder: Pedro Álvares Cabral;
- partida: 09/03/1500;
- campanha principal: Lisboa → Vera Cruz → África Oriental → Malabar → retorno;
- frota inicial: 13 embarcações como atributo documental da expedição, não como 13 entidades plenamente simuladas;
- término: retornos assíncronos em junho–julho de 1501, com trajetórias separadas preservadas por eventos.

A campanha operacional jogável futura pode seguir o **núcleo principal** comandado por Cabral. Embarcações que desaparecem, naufragam, regressam antes ou seguem missões separadas devem ser registradas como trajetórias/eventos documentais.

## 2. Nós

### Reutilizar

- `LIS` — Lisboa;
- `CGH` — Cabo da Boa Esperança como marco náutico;
- `MOZ` — Ilha de Moçambique;
- `KIL` — Kilwa Kisiwani/Quiloa; já existe e não deve ser duplicada;
- `MAL` — Melinde;
- `ANJ` — Anjediva;
- `CAL` — Calecute;
- `COC` — Cochim.

### Novo candidato `VCR` — Terra de Vera Cruz / Costa do Descobrimento

Proposta:

- `historical_name`: Terra de Vera Cruz / Porto Seguro;
- `modern_name`: região Porto Seguro–Santa Cruz Cabrália / Coroa Vermelha;
- âncora moderna de trabalho: aproximadamente `-16.2830, -39.0299`, usando Coroa Vermelha apenas como referência regional moderna;
- `coordinate_confidence`: `MEDIUM` ou `LOW` — preferir `MEDIUM` para identificação regional e explicitar que o ancoradouro exato não está sendo afirmado;
- `node_type`: `ANCHORAGE` ou equivalente costeiro já aceito pelo schema;
- `access_regime`: `ANCHORAGE_CONTACT`;
- `market_scale`: `NONE`;
- nenhuma disponibilidade comercial/portuária genérica inferida;
- povos locais devem permanecer agregados apenas se houver necessidade relacional documentada e gate próprio.

O nó representa a permanência documental de abril–maio de 1500 e não uma cidade portuguesa posterior.

### Novo candidato `CAN` — Cananor

Proposta:

- `historical_name`: Cananor;
- `modern_name`: Kannur;
- `latitude`: `11.8538`;
- `longitude`: `75.3721`;
- `coordinate_confidence`: `HIGH` para identidade da cidade/porto, sem afirmar ponto exato de acostagem;
- `node_type`: `FOREIGN_PORT`;
- polity: `Kolathunad / Kolathiri`;
- `access_regime`: `FOREIGN_NEGOTIATED`;
- fortificação portuguesa: ausente em 1501;
- feitoria permanente: não retroprojetar 1502 para janeiro de 1501;
- cesta comercial mínima: somente o que o gate específico sustentar. Para Cabral, a narrativa documenta compra limitada de canela e gengibre, mas isso não obriga ainda a criar toda uma cesta genérica do porto.

## 3. Sequência principal mínima

A rota operacional não precisa materializar toda passagem astronômica ou todo avistamento. A sequência candidata é:

`LIS → VCR → CGH → MOZ → KIL → MAL → ANJ → CAL → COC → CAN → MOZ → CGH → LIS`

Observações:

- Canárias e Cabo Verde podem permanecer observações da viagem se não houver ação jogável necessária;
- `CGH` funciona como marco náutico e local do grande evento de fragmentação, não como porto;
- a ida e o retorno podem reutilizar nós existentes com datas/observações específicas da expedição;
- Sofala deve permanecer trajetória/missão específica de Sancho de Tovar, não desvio automático da campanha principal.

## 4. Frota e trajetórias

### Núcleo principal inferido em Quiloa

Partindo dos 13 iniciais e subtraindo:

- Vasco de Ataíde — desaparecido em 23/03;
- Gaspar de Lemos — regressa a Portugal desde Vera Cruz;
- Luís Pires, Aires Gomes da Silva, Bartolomeu Dias e Simão de Pina — perdidos no episódio do Cabo;
- Diogo Dias — separado do núcleo principal;

restam seis embarcações, coerentes com a cronologia que registra seis navios reunidos em Quiloa:

1. Pedro Álvares Cabral;
2. Sancho de Tovar;
3. Nicolau Coelho;
4. Simão de Miranda de Azevedo;
5. Pêro de Ataíde;
6. Nuno Leitão da Cunha (`Anunciada`).

Esta lista é uma **inferência documental reproduzível**, não uma enumeração literalmente fornecida por uma única fonte.

### Eventos/trajectórias mínimas

- `VESSEL_LOST_CONTACT` — Vasco de Ataíde, 23/03/1500;
- `DISPATCH_TO_CROWN` — Gaspar de Lemos, Vera Cruz → Lisboa, informação disponível à Coroa em junho de 1500;
- quatro `VESSEL_LOSS` no Cabo em maio de 1500;
- `TRAJECTORY_SPLIT` — Diogo Dias;
- `LOCAL_INSTITUTION_LOST` — feitoria de Calecute em dezembro de 1500;
- `RELATION_ACCESS_SHIFT` — Calecute torna-se hostil/inacessível no contexto da expedição;
- `LOCAL_INSTITUTION_ESTABLISHED` — residentes/feitoria inicial em Cochim;
- `PORT_CONTACT` — Cananor, janeiro de 1501;
- `VESSEL_LOSS` — nau de Sancho de Tovar no retorno;
- `MISSION_SPLIT` — Tovar/Sofala;
- `RETURN_ADVANCE` — `Anunciada` destacada para chegar primeiro;
- `RETURN_STRAGGLER` — Nicolau Coelho ou Simão de Miranda, identidade mantida como variante.

## 5. Schema de eventos

`expedition_epilogue_events.csv` já demonstra que o domínio documental aceita:

- `trajectory_id`;
- sujeito pessoa/embarcação;
- origem/destino;
- datas ou intervalos;
- variantes;
- `preferred_for_simulation`;
- grau de evidência.

A necessidade de Cabral é semelhante, mas ocorre durante toda a campanha. Recomenda-se, no futuro gate de implementação, **generalizar semanticamente esse mecanismo para eventos de trajetória de expedição** ou criar tabela irmã compatível. Não criar um sistema geral de frota antes desse teste mínimo.

## 6. Estados institucionais e relacionais

### Calecute

Após a crise de dezembro de 1500:

- feitoria portuguesa: não operacional/destruída;
- acesso/relação portuguesa: hostil no contexto subsequente;
- sobreviventes evacuados, com dois portugueses ocultos localmente;
- não é necessário sistema geral de combate para representar a transição.

### Cochim

- carregamento efetivo de especiarias;
- residentes portugueses sob Gonçalo Gil Barbosa;
- relação comercial/política favorável;
- soberania continua local;
- fortificação/guarnição posterior não entra.

### Cananor

- primeiro contacto operacional de Cabral em janeiro de 1501;
- acolhimento favorável;
- compra limitada documentada;
- estado local torna-se relevante para campanhas posteriores;
- João da Nova não parte de Lisboa conhecendo automaticamente esse resultado.

## 7. Latência de informação

A futura normalização deve preservar pelo menos:

- `VERA_CRUZ_NEWS`: disponível à Coroa em junho de 1500 via Gaspar de Lemos;
- `CALICUT_RUPTURE`, `COCHIN_FACTORY`, `CANNANORE_RECEPTION`: estados locais desde dezembro de 1500/janeiro de 1501, mas **não** conhecimento inicial de João da Nova em 05/03/1501;
- notícias do retorno de Cabral chegam a Lisboa a partir da `Anunciada` em 24/06/1501 e demais navios no fim de julho.

O mecanismo pode ser implementado futuramente com eventos de informação ou aproveitando os estados de conhecimento já existentes, após auditoria de compatibilidade.

## 8. Incertezas preservadas sem bloquear normalização

- a listagem EVE com `Pêro Dias` é tratada como inconsistência; a normalização deve usar `Diogo Dias` pela Carta de Caminha, cronologia crítica e estudo académico especializado;
- nome de algumas embarcações permanece desconhecido;
- a identidade da nau desgarrada no retorno permanece `Nicolau Coelho | Simão de Miranda` até nova evidência;
- o ponto cartográfico `VCR` é âncora regional, não ancoradouro exato;
- detalhes comerciais completos de Cananor exigem gate próprio se forem necessários além da compra específica de Cabral.

## 9. Sistemas que continuam desnecessários

A evidência da #111 **não exige**, para o primeiro incremento funcional:

- controle individual de 13 navios;
- tripulação individual;
- combate naval/tático geral;
- doença/mortalidade sistêmica;
- naufrágio genérico;
- correio genérico;
- preços históricos completos.

## Decisão de gate

A documentação de Cabral está suficiente para encerrar P3.1-doc quando esta proposta e as lacunas preservadas forem aceitas como baseline. O próximo subgate documental deve ser **João da Nova 1501–1502**, começando pela cronologia da expedição e, sobretudo, pelo momento em que sua armada adquire no próprio Índico o conhecimento dos estados deixados por Cabral.