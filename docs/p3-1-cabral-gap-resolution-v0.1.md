# P3.1-doc — resolução de lacunas: Dias, Quiloa e Cananor v0.1

Data: 2026-09-07
Issue: #111

## A. Diogo Dias × Pêro Dias — RESOLVIDO para normalização

A listagem geral EVE de armadas registra `Pêro Dias` entre os capitães de 09/03/1500. Contudo, três linhas independentes de evidência favorecem `Diogo Dias`:

1. a Carta de Pêro Vaz de Caminha menciona explicitamente **Diogo Dias**, antigo almoxarife de Sacavém, presente na armada e nas interações em Vera Cruz;
2. a reconstrução crítica de João Paulo Oliveira e Costa/EVE inclui **Diogo Dias** entre os capitães régios em nau e lhe atribui a trajetória separada depois do Cabo;
3. estudo académico da NOVA sobre navegadores portugueses afirma que as duas embarcações régias destinadas a Sofala eram capitaneadas pelos irmãos **Bartolomeu e Diogo Dias**.

Decisão documental: para uma futura normalização da armada, usar **Diogo Dias**. A ocorrência `Pêro Dias` na listagem geral da EVE permanece registrada como inconsistência editorial/metadado da listagem, não como variante histórica equiprovável.

Essa decisão não resolve automaticamente o nome da embarcação de Diogo Dias, que deve permanecer indeterminado se não houver fonte suficiente.

## B. Quiloa — nó existente

`data/nodes.csv` já contém:

- `KIL` — Kilwa Kisiwani;
- âncora `-8.9570, 39.5220`;
- confiança `MEDIUM`;
- `FOREIGN_ENTREPOT`;
- Sultanato de Kilwa;
- `FOREIGN_NEGOTIATED`;
- proveniência `ALPERS_IOWH|SUBRAHMANYAM_PEA`.

Portanto, P3.1 **não deve criar novo nó para Quiloa**. A visita de Cabral em julho de 1500 deve futuramente ser representada como uso de `KIL`, com atividades específicas da expedição e sem alterar automaticamente a disponibilidade comercial genérica do nó.

## C. Cananor — âncora candidata

Cananor/Kannur ainda não consta em `nodes.csv`.

Fontes institucionais convergem:

- HPIP: Kannur [Cananor], aproximadamente `11.8537667, 75.3720889`;
- EVE/FCSH: Cananor/Kannanur/Kannur, porto do norte do Malabar no reino de Kolathunad/Kolathiri, aproximadamente `11°51'19"N, 75°21'41.82"E`.

### Confiança espacial

A identificação da cidade/porto moderno é segura. Contudo, o ponto preciso de acostagem de janeiro de 1501 não deve ser equiparado à feitoria de 1502 nem à fortificação de 1505. Assim:

- `coordinate_confidence`: **HIGH** para identidade cidade/porto;
- nota obrigatória: coordenada moderna de referência, não posição exata do ancoradouro de 1501;
- `active_from`: não usar 1502 para o porto — o porto preexiste; 1502 é apenas o estabelecimento permanente português;
- fortificação portuguesa deve permanecer ausente para 1501.

### Proposta documental, ainda não executável

| Campo | Valor candidato |
|---|---|
| node_id | `CAN` |
| historical_name | `Cananor` |
| modern_name | `Kannur` |
| latitude | `11.8538` |
| longitude | `75.3721` |
| coordinate_confidence | `HIGH` |
| node_type | `FOREIGN_PORT` |
| polity | `Kolathunad / Kolathiri` |
| access_regime | `FOREIGN_NEGOTIATED` |
| market_scale | `REGIONAL` ou manter indeterminado até auditoria comercial específica |

Não inserir ainda em `data/nodes.csv`.

## D. Consequência para o checklist #111

- Pendência A `Diogo Dias × Pêro Dias`: **resolvida**.
- Pendência B cartografia Quiloa: **resolvida por reuso de KIL**.
- Pendência B cartografia Cananor: **resolvida em nível de âncora**, faltando somente decisão de campos comerciais/políticos mínimos antes de normalização.

Permanecem bloqueantes: Gaspar de Lemos e chegada da notícia do Brasil; identificação do conjunto de seis embarcações em Quiloa; retorno Moçambique/Sofala; latência completa de informação; classificação final das transições de estado.