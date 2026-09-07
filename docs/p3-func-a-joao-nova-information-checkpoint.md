# P3-func-A — checkpoint João da Nova: latência de informação

Data: 2026-09-07
Issue: #116
Branch: `p3-func-a-116`

## Gate implementado

Foi iniciado o recorte funcional de `EXP_JOAO_NOVA_1501` pelo requisito histórico mais específico e mais bem documentado: a aquisição tardia, em Angra de São Brás (`SBR`), da informação sobre a ruptura de Calecute e sobre Cochim/Cananor.

A implementação não cria cronologia diária fictícia Lisboa→São Brás nem sistema geral de mensagens. O evento documental já existente `NOVA1501_E01` permanece com janela `1501-05-01` a `1501-08-31`; a ação funcional só pode ocorrer em `SBR`, dentro dessa janela, e é one-shot.

## Implementação

Criado `src/quintoimperio/domain/joao_nova_campaign.py` com `JoaoNovaCampaignModel`.

O estado inicial:

- inicia em Lisboa em `1501-03-05`;
- ativa `EXP_JOAO_NOVA_1501` em modo `GUIDED`;
- não contém `CABRAL_MALABAR_WARNING` em `information_history`.

A aquisição em São Brás registra `P3_INFO:CABRAL_MALABAR_WARNING` somente quando:

1. a expedição ativa é João da Nova;
2. a embarcação está em `SBR`;
3. o relógio está dentro da janela documental de `NOVA1501_E01`;
4. a informação ainda não foi adquirida.

O evento altera conhecimento da expedição, não o estado objetivo de Calecute, Cochim ou Cananor e não retroage informação para Lisboa.

## Testes

Criado `tests/test_p3_joao_nova_information.py`.

O teste demonstra:

- partida em Lisboa sem o aviso de Cabral;
- impossibilidade de aquisição fora de São Brás;
- correspondência com `NOVA1501_E01` (`INFORMATION_ACQUISITION`, `SBR→SBR`, janela maio–agosto de 1501);
- aquisição em São Brás;
- persistência do marcador no estado;
- semântica one-shot, sem duplicação em segunda tentativa.

O run `34146320704`, commit `6e3c6a5159c769e360312ffa8a9752f3eedb94a5`, passou integralmente: validação de dados, testes de domínio, protótipos, retorno, interfaces, persistência e cartografia.

`JoaoNovaCampaignModel` foi em seguida exposto pela API pública de `quintoimperio.domain` no commit `d5d901e54cfee91afa72aad407b8696fd952c76d`.

## Limite documental preservado

A matriz P3.2 registra como lacuna imediata a cronologia completa Lisboa→São Brás e as datas intermediárias. Portanto, este checkpoint não autoriza inventar duração de viagem, data diária de chegada a São Brás ou escala adicional apenas para tornar a campanha contínua.

O próximo gate funcional deve primeiro auditar `expedition_routes.csv`, `voyage_observations.csv` e as fontes P3.2 para identificar até onde é possível normalizar a sequência `LIS→SBR→KIL→MAL→ANJ→CAN→COC→CAN` com âncoras temporais defensáveis. Onde não houver data suficiente, a incerteza deve permanecer explícita em vez de ser convertida em precisão artificial.
