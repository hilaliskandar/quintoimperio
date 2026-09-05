# Âncoras cartográficas provisórias

Este documento registra duas coordenadas usadas pelo protótipo apenas como **âncoras cartográficas defensáveis**. Elas não são tratadas como posição arqueológica exata do cais ou assentamento do século XV.

## Mpinda / Soyo

Coordenada adotada:

```text
latitude  = -6.1981
longitude = 12.3933
confidence = MEDIUM
```

Racional:

- a historiografia do projeto identifica Mpinda como o porto associado a Soyo e às primeiras relações luso-kongolesas;
- fontes geográficas modernas preservam o topônimo `Pinda` imediatamente ao sul da atual Soyo, na região da margem meridional da foz do Congo;
- a âncora adotada corresponde aproximadamente à `Missão do Pinda`, não ao porto histórico provado por escavação;
- por isso o jogo usa o ponto para localização regional e navegação de mapa, mantendo explícita a incerteza espacial.

Referências auxiliares de localização:

- Mapcarta / OpenStreetMap, `Missão do Pinda`: aproximadamente `-6.19805, 12.39328`.
- Soyo moderna: aproximadamente `-6.14, 12.37`; descrições históricas secundárias identificam Mpinda como porto de Soyo na foz do Congo.

## Sofala

Coordenada adotada:

```text
latitude  = -20.1562
longitude = 34.7383
confidence = MEDIUM
```

Racional:

- a base histórica identifica Sofala como porto do sistema aurífero do sul da costa suaíli;
- a Enciclopédia Virtual da Expansão Portuguesa descreve o antigo porto a sul da foz do Pungué e observa que o sítio hoje está submerso;
- bases geográficas modernas identificam Nova Sofala / Sofala, incluindo o sítio histórico, em aproximadamente `-20.15616, 34.7383`;
- mudanças de estuário, assoreamento e submersão impedem interpretar essa coordenada como posição exata do porto medieval.

Referências auxiliares de localização:

- Enciclopédia Virtual da Expansão Portuguesa, entrada `Sofala`.
- Mapcarta / OpenStreetMap, `Sofala` / `Nova Sofala`: aproximadamente `-20.15616, 34.7383`.

## Regra de uso

Essas coordenadas podem ser usadas para:

- desenhar o nó no mapa de referência;
- calcular distâncias geodésicas **aproximadas** entre âncoras;
- definir enquadramento regional da interface.

Não podem ser usadas para:

- afirmar a posição exata de cais, fortificação ou núcleo urbano em 1497;
- reconstruir a derrota histórica de uma embarcação;
- converter distância geodésica em duração histórica sem evidência adicional;
- elevar `coordinate_confidence` para `HIGH` sem nova fonte espacial específica.
