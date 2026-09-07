# P3.2-doc — João da Nova 1501–1502 — matriz documental v0.1

Data: 2026-09-07
Issue-mãe: #110
Subgate: #112

## Método

A matriz parte das fontes institucionais já localizadas para a armada de 1501 e privilegia os fatos necessários ao loop: composição, partida, aquisição de informação, sequência de escalas e consequências institucionais no Malabar. Afirmações sobre Ceilão/Sri Lanka permanecem fora da rota porque a própria EVE considera uma viagem de João da Nova em 1501 apenas plausível e não documentada.

Nenhuma linha abaixo autoriza ainda alteração em `data/` ou código.

## 1. Composição e natureza da armada

A listagem EVE/FCSH registra partida em **05/03/1501** e quatro capitães:

1. João da Nova — capitão-mor;
2. Diogo Barbosa;
3. Francisco Novais;
4. Fernão Vinet.

Fonte oficial portuguesa descreve a força como uma esquadra de **quatro naus**, destinada a carregar especiarias e de caráter primordialmente comercial.

### Consequência de modelagem

O primeiro P3-func não precisa de uma frota complexa. A expedição pode ser tratada como uma campanha principal de quatro navios, mantendo diferenças de armamento/propriedade apenas como documentação até que gerem decisão jogável comprovada.

## 2. Estado de conhecimento na partida

João da Nova parte em 05/03/1501 **antes do retorno de Cabral a Lisboa**. Portanto:

- conhece a rota e o precedente de Vasco da Gama;
- pode conhecer a notícia de Vera Cruz, já chegada ao reino em junho de 1500 via Gaspar de Lemos;
- **não deve receber automaticamente** como conhecimento inicial da Coroa a ruptura de Calecute, a feitoria de Cochim ou o acolhimento de Cananor, que ainda não haviam chegado a Lisboa.

Fonte oficial portuguesa afirma explicitamente que João da Nova largou imaginando que o trato das especiarias continuava organizado em Calecute.

## 3. Evento crítico de aquisição de informação em São Brás

Na escala em **Angra de São Brás**, para aguada, a armada encontra uma mensagem deixada por um capitão da esquadra de Cabral, dentro de um sapato pendurado numa árvore. A mensagem comunicava o estado em que Cabral deixara as negociações da Índia e instruía a nova armada a:

- dirigir-se a **Cochim** e **Cananor**;
- evitar **Calecute**.

Fontes locais sul-africanas associam a mensagem a **Pêro de Ataíde** e situam a escala em julho de 1501; a identificação do mensageiro é compatível com a tradição documental, mas o projeto deve manter grau de evidência separado para o detalhe nominal/data exata enquanto não houver edição especializada primária.

### Classificação recomendada

`INFORMATION_ACQUISITION` / `CABRAL_MALABAR_WARNING`

Efeito mínimo futuro:

- atualiza conhecimento da **expedição** sobre Calecute/Cochim/Cananor;
- **não** altera nesse momento o estado objetivo dos portos, que já havia mudado em dezembro de 1500/janeiro de 1501;
- não atualiza retroativamente conhecimento da Coroa em Lisboa;
- pode alterar o planejamento de rota a partir de São Brás.

Este é o melhor exemplo até agora de que P3 necessita de latência e titularidade da informação, mas não necessariamente de um sistema genérico de correio.

## 4. Sequência operacional inicial

Fonte oficial portuguesa registra, após São Brás:

`SBR → KIL → MAL → ANJ → CAN → COC`

João da Nova evita Calecute e chega a Cochim para carregar seus navios.

### Nós

Todos já existem ou já foram propostos documentalmente:

- `SBR` — Angra de São Brás;
- `KIL` — Quiloa/Kilwa Kisiwani;
- `MAL` — Melinde;
- `ANJ` — Anjediva;
- `CAN` — Cananor/Kannur, candidato definido em P3.1;
- `COC` — Cochim.

Nenhuma evidência atual exige novo nó no trecho Índico além de `CAN`.

## 5. Cananor e Cochim

A EVE registra que:

- Cananor fora visitada por Cabral em janeiro de 1501;
- ao final de 1501 a armada de João da Nova estabelece **presença portuguesa com uma feitoria**;
- Vasco da Gama reorganiza essa feitoria em 1502;
- Cananor era porto comercial relevante de Kolathunad, com gengibre e cardamomo abundantes e pouca pimenta local comparativamente ao restante do Malabar.

### Regra temporal

Para P3.2, distinguir:

1. **janeiro de 1501** — primeiro contacto operacional de Cabral;
2. **fim de 1501** — estabelecimento de presença/feitoria pela armada de João da Nova;
3. **1502** — reorganização por Vasco da Gama.

Não retroprojetar a feitoria de fim de 1501 para o estado inicial da viagem.

Cochim já possui baseline P2. Em P3.2, funciona como destino comercial indicado pela mensagem de São Brás e porto efetivo de carregamento.

## 6. Calecute

A armada não deve ser obrigada a visitar Calecute apenas porque o nó existe. O aviso recebido em São Brás transforma Calecute em um porto conhecido como hostil/inadequado no contexto desta expedição.

Para o futuro P3-func:

- `CAL` permanece estado objetivo já alterado por Cabral;
- João da Nova adquire conhecimento desse estado em SBR;
- o planejamento histórico guiado deve favorecer `CAN/COC` sem conceder informação antes de SBR.

## 7. Ceilão/Sri Lanka

A EVE afirma que os primeiros contactos portugueses documentados com Ceilão ocorreram em 1506 e que uma viagem de João da Nova em 1501, embora plausível segundo Bouchon, **não está documentada**.

Decisão: **não materializar Ceilão como escala de P3.2**. Qualquer futura inclusão exige nova evidência específica e gate próprio.

## 8. Lacunas imediatas

1. confirmar a cronologia completa Lisboa → São Brás e datas intermediárias;
2. identificar, se possível em fonte especializada, autoria e data exata da mensagem de São Brás;
3. reconstruir datas de Quiloa, Melinde, Anjediva, Cananor e Cochim;
4. documentar o carregamento em Cochim/Cananor e a instalação da feitoria de Cananor com fonte contemporânea ou estudo especializado;
5. reconstruir a torna-viagem e perdas/separações, se houver;
6. decidir quais efeitos são conhecimento, quais são relação/acesso e quais são presença institucional;
7. verificar se `information_history` e os estados de conhecimento atuais suportam o evento de São Brás sem novo schema.

## Decisão provisória

P3.2 já demonstra uma diferença importante em relação a Cabral: a campanha de João da Nova deve ser guiada por **aquisição tardia de informação**. O evento de São Brás é materialmente necessário para impedir vazamento de informação e explicar a mudança de rota para Cananor/Cochim. Nenhuma nova mecânica de combate ou frota é necessária para esse núcleo documental.