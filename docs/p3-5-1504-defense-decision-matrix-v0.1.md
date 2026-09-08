# P3.5-doc — defesa de Cochim 1504 — matriz de decisão de arquitetura v0.1

Data: 2026-09-08
Issue: #115
Baseline funcional herdado: `1a4f43822446a77d5bb79a76c14fab8a879a50d1`

## Pergunta

A defesa prolongada de Cochim em 1504 demonstra necessidade de um sistema funcional de combate, ou os fatos necessários ao horizonte Python 1505 GREEN podem continuar representados por eventos guiados e estados temporais?

## Princípio de decisão

Esta matriz separa três níveis que não devem ser confundidos:

1. **agência histórica do comandante** — decisões efetivamente atribuídas a Duarte Pacheco Pereira;
2. **causalidade histórica** — fatores que a documentação associa ao resultado das defesas;
3. **agência do jogador** — decisões que o loop atual precisa oferecer ao jogador para representar 1504.

Uma decisão historicamente importante não gera automaticamente uma mecânica jogável. Para justificar combate funcional, ela deve ser simultaneamente documentável, recorrente, traduzível em escolha abstrata e necessária ao loop controlável.

## Evidência dirigida

A EVE/FCSH sintetiza que, ao longo de 1504, Duarte Pacheco comandou forças portuguesas e cochinenses, explorando o terreno e a superioridade de artilharia para repelir forças numericamente superiores do Samorim.

A narrativa de Castanheda preservada na tradução de Kerr descreve decisões repetidas e observáveis: defesa de passagens estreitas, distribuição de homens entre forte, embarcações e posição avançada, retorno rápido a uma passagem ameaçada após uma manobra inimiga para dividir a força e reparo/refit das embarcações entre ataques.

Estudo recente de história militar destaca que os acessos estreitos do ambiente lagunar comprimiam a frente de combate e permitiam explorar armas de fogo contra forças que precisavam atravessar áreas restritas. Essa interpretação reduz a necessidade de aceitar literalmente números muito elevados fornecidos pelas crônicas e desloca o foco para posição, geografia e meios disponíveis.

Há também tradição historiográfica de que o regimento deixado pelos Albuquerque recomendava postura defensiva e evitar combate sempre que possível. Como a formulação exata ainda depende de fonte secundária/edição a ser auditada, ela é tratada nesta matriz como hipótese de trabalho, não como regra de domínio fechada.

## Matriz

| Decisão/fator | Recorrência | Causalidade sustentada | Traduzível em escolha abstrata | Pertence ao loop do jogador hoje? | Exige combate geral? | Decisão v0.1 |
|---|---:|---|---|---|---|---|
| selecionar passagem/canal defensável | alta | forte | sim | não demonstrado | não | estado/evento guiado; preservar como fator de posição |
| concentrar homens e embarcações na passagem ameaçada | alta | forte | sim | não demonstrado | não | evento de redistribuição; sem unidades táticas |
| distribuir meios entre forte, cidade e posição avançada | recorrente | forte | sim | não demonstrado | não | documentar como postura defensiva, não como roster de unidades |
| empregar artilharia a partir de embarcações/posição estreita | alta | forte | sim | não demonstrado | não | efeito causal narrativo; não criar dano/HP |
| reagir a tentativa inimiga de dividir a defesa | documentada | forte | sim | não demonstrado | não | evento de resposta/retorno à posição |
| reparar/refazer embarcações entre investidas | documentada | média/forte | sim | parcialmente análogo a manutenção existente, mas não no loop F4 | não | manter como atividade específica, sem serviço genérico novo |
| escolher entre defesa e iniciativa ofensiva | documentada em tradição historiográfica | média enquanto fonte primária não fechada | sim | potencialmente | não necessariamente | manter como hipótese; não implementar antes de fechar evidência |
| resolver baixas, moral e dano tático | crônicas narram resultados | fraca para parâmetros quantitativos confiáveis | tecnicamente sim | não | sim | explicitamente fora de escopo |
| resultado final da campanha defensiva | repetido e firme | forte | não é escolha | mundo histórico | não | evento/estado histórico guiado |

## Achado principal

**1504 demonstra agência militar histórica, mas ainda não demonstra necessidade de um motor geral de combate.**

O caso mostra decisões reais de comando, porém o domínio atual não coloca o jogador no papel fixo de Duarte Pacheco nem possui uma campanha executável de defesa em que seja necessário escolher distribuição tática. Introduzir combate agora produziria uma camada de decisão que o loop existente não consome.

Ao mesmo tempo, reduzir 1504 a um único evento “vitória defensiva” perderia estrutura histórica relevante. A alternativa mínima recomendada é uma **sequência estruturada de defesa**, ainda guiada, capaz de registrar:

- fase/episódio defensivo;
- local funcional abstrato da defesa, sem mapa microtático;
- postura/decisão histórica adotada;
- fatores relevantes: terreno, embarcações, artilharia, força aliada;
- resultado histórico;
- efeitos sobre `node_state_events` quando existirem.

Essa estrutura pode inicialmente permanecer em `expedition_events`/documentação se os tipos existentes forem suficientes. Novo schema só deve ser criado se a normalização mínima mostrar que múltiplos episódios não podem ser representados sem perda semântica relevante.

## Decisão provisória do gate T4

Para F4, a opção preferencial é:

**eventos guiados estruturados + estados temporais; sem combate funcional mínimo nesta primeira implementação.**

A decisão é provisória até três verificações finais:

1. fechar a cronologia e o número mínimo de episódios defensivos que precisam ser distinguidos;
2. verificar se os tipos atuais de `expedition_events` conseguem registrar postura/redistribuição/resultados sem criar campos artificiais;
3. confirmar que nenhuma etapa da futura campanha de Lopo Soares exige que o jogador participe diretamente da defesa anterior à chegada da armada.

Se essas verificações forem satisfeitas, a #115 deverá fechar formalmente `combate funcional = NÃO NECESSÁRIO EM F4`, deixando F5 como último teste do gate T4. Se alguma delas falhar por ausência real de agência representável, abrir issue estreita para a menor abstração possível de defesa, e não um motor geral de batalha.

## Não autorizado por esta matriz

- pontos de vida, moral ou dano por unidade;
- quantidades militares tomadas literalmente das crônicas;
- microtática ou posicionamento em grade;
- classes detalhadas de infantaria/artilharia;
- batalha probabilística genérica;
- retroprojeção de uma mecânica militar para 1500–1503;
- transformar o jogador automaticamente em Duarte Pacheco.

## Próximo subgate

1. construir uma cronologia mínima dos episódios defensivos que precisam ser distinguidos, usando fontes narrativas e estudos críticos;
2. testar semanticamente `expedition_events.csv` contra essa sequência sem editar dados ainda;
3. fechar Coulão e a chegada de Lopo Soares;
4. produzir a proposta mínima de normalização de 1504 e a decisão final do gate de combate.