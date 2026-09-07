# P3.2-doc — aquisição de informação em São Brás v0.1

Data: 2026-09-07
Issue: #112

## Evento documental

A armada de João da Nova parte de Lisboa em março de 1501 sem notícia do resultado da missão de Cabral no Malabar. A fonte oficial portuguesa consultada afirma que João da Nova imaginava que o comércio de especiarias estava organizado em Calecute.

Na escala em Angra de São Brás, para aguada, a armada encontra uma mensagem deixada por um capitão da esquadra de Cabral, dentro de um sapato pendurado numa árvore. A mensagem informa o estado das negociações na Índia e orienta a nova armada a dirigir-se a **Cochim e Cananor** e **evitar Calecute**.

Fontes sul-africanas associam a mensagem a Pêro de Ataíde. Para o modelo, o fato essencial é a transmissão da informação; autoria e data diária podem permanecer com grau de confiança menor enquanto não forem conferidas em edição especializada.

## Proposta de evento documental

| Campo conceitual | Valor |
|---|---|
| information_id | `CABRAL_MALABAR_WARNING` |
| event_type | `INFORMATION_ACQUISITION` |
| expedition_id | futuro `EXP_JOAO_NOVA_1501` |
| location | `SBR` |
| holder_before | informação não disponível à expedição |
| holder_after | expedição de João da Nova |
| content | Calecute hostil/inadequado; Cochim e Cananor como alternativas comerciais |
| sender | capitão da armada de Cabral; Pêro de Ataíde como identificação provável/documentada por fontes locais |
| medium | mensagem escrita deixada em ponto de aguada |
| effect_scope | conhecimento/planejamento da expedição |
| world_state_effect | nenhum: os estados locais já existiam |
| crown_knowledge_effect | nenhum retroativo |

## Antes e depois do evento

### Antes de São Brás

A expedição conhece:
- rota precedente de Vasco da Gama;
- notícia de Vera Cruz já disponível à Coroa;
- objetivo comercial de carregar especiarias.

Não deve conhecer:
- destruição da feitoria de Calecute;
- ruptura política com o Samorim;
- feitoria/residentes em Cochim;
- acolhimento de Cananor.

### Depois de São Brás

A expedição pode conhecer operacionalmente:
- que Calecute deve ser evitada;
- que Cochim oferece alternativa efetiva;
- que Cananor é alternativa favorável.

Isso justifica a sequência histórica posterior por Quiloa, Melinde, Anjediva, Cananor e Cochim sem transformar esse conhecimento em propriedade global automática de todos os atores portugueses.

## Implicação para o domínio

O projeto já separa conhecimento da Coroa e do personagem/expedição e já persiste `information_history`. A hipótese mínima para P3-func deve tentar reutilizar essa arquitetura antes de criar um novo sistema.

O evento precisa ser:
- one-shot;
- datado/localizado;
- persistente após save/load;
- capaz de alterar planejamento/visibilidade de rota sem alterar retroativamente o mundo;
- reproduzível em `GUIDED`.

## Teste conceitual futuro

Um teste mínimo deverá comprovar:

1. antes de `SBR`, `CAL_HOSTILE_AFTER_CABRAL` não pertence ao conhecimento da expedição;
2. após a ação/evento de leitura da mensagem, esse conhecimento passa a pertencer à expedição;
3. `COC` e `CAN` tornam-se destinos historicamente informados;
4. o estado objetivo de Calecute não muda no momento da leitura — ele já havia mudado em dezembro de 1500;
5. save/load não permite repetir o evento nem perder a informação adquirida.

## Decisão

O aviso de São Brás é suficientemente importante para ser tratado como **evento funcional de informação** em um futuro P3-func. Ele não justifica sistema genérico de correio ou mensagens; primeiro deve ser implementado como caso documental específico usando mecanismos existentes sempre que possível.