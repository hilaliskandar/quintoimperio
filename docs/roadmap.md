# Roteiro de produção

## Estado após o núcleo v0.1

O PR #1 foi integrado a `main`. O núcleo v0.1 reúne fundação histórica, economia relativa, navegação, calendário, conhecimento, viagem, serviços portuários, comércio, informação, acesso institucional, relações por atores, risco marítimo inicial, cartografia, sessão integrada e uma primeira interface Pygame.

O merge não encerra o projeto e não equivale ao MVP. O próximo objetivo é transformar sistemas já existentes em uma experiência histórica contínua, jogável e encerrável, evitando ampliar o escopo antes de fechar essa vertical slice.

Princípio de desenvolvimento até o MVP: **priorizar continuidade de campanha, consequências das decisões, legibilidade da interface e robustez da sessão; novos sistemas só entram quando forem necessários para fechar o loop.**

## Definição do MVP

O MVP é uma vertical slice da primeira viagem portuguesa de 1497–1498, iniciada em Lisboa em 8 de julho de 1497 e encerrada após a primeira estadia jogável em Calecute.

O jogador deve conseguir, sem usar o cenário técnico nem overrides de teste:

1. iniciar em Lisboa com a armada de Vasco da Gama;
2. percorrer as dez pernas normalizadas da campanha até Calecute;
3. lidar com permanências históricas, serviços, espera, informação e condição do navio;
4. manter separadas cronologia `GUIDED` e trajetória `COUNTERFACTUAL`;
5. chegar a Melinde e utilizar o piloto documentado quando aplicável;
6. chegar a Calecute com conhecimento e acesso institucional tratados como estados distintos;
7. estabelecer contatos apenas com atores historicamente normalizados;
8. consultar e realizar pelo menos uma operação comercial jogável em mercado documentado;
9. concluir objetivos explícitos da campanha e alcançar uma condição clara de encerramento;
10. salvar e restaurar o estado da campanha;
11. passar integralmente pela validação automática, testes, smoke tests e revisão externa do PR.

O MVP não precisa reproduzir ainda o retorno a Lisboa, Cochim, a armada de 1500, Goa, Ormuz, Malaca, cartaz, combate, naufrágio, tripulação individual ou economia monetária histórica completa.

## M0 — Saneamento pós-merge

Issue: #33.

Status: **em execução**.

Objetivos:

- confirmar `main` após o merge e CI verde;
- encerrar issues legadas cujo escopo v0.1 já foi entregue;
- eliminar backlog aberto que não represente trabalho futuro real;
- consolidar neste documento a definição do MVP e a sequência de gates;
- preparar uma branch limpa e um PR exclusivamente documental/organizacional.

Critério de saída: backlog legado encerrado, roadmap atualizado, CI preservado e próxima issue funcional pronta.

## M1 — Campanha Lisboa–Calecute ponta a ponta

Próxima frente funcional.

Objetivo: garantir que a campanha histórica percorra pela interface toda a sequência já presente no domínio:

`LIS → STG → SHB → CGH → SBR → RCO → RBS → MOZ → MOM → MAL → CAL`.

Entregas mínimas:

- cada perna executável pela interface;
- escala ativa correta após cada chegada;
- bloqueios de partida e espera coerentes com `GUIDED`;
- transição auditável para `COUNTERFACTUAL` quando o jogador divergir;
- reabastecimento e reparo apenas por ações explícitas e disponibilidade documentada;
- nenhuma rota `STRATEGIC_AGGREGATE` executável;
- piloto de Melinde restrito à competência documentada;
- testes de integração cobrindo a campanha completa até Calecute.

Não incluir neste gate retorno da Índia, Cochim ou nova expansão geográfica.

## M2 — Relações com consequências mínimas

Objetivo: dar consequência jogável a relações sem criar uma reputação global arbitrária.

Diretriz:

- manter relação por ator documentado;
- preferir estados categóricos a um score contínuo;
- introduzir apenas transições necessárias ao MVP, por exemplo `UNESTABLISHED → CONTACTED → COOPERATIVE` e, quando justificável, um estado adverso;
- efeitos devem ser locais e explícitos: acesso a informação, disponibilidade de intermediário, possibilidade de ação institucional ou outra consequência claramente parametrizada;
- contato relacional não deve alterar preço, crédito ou acesso por simples existência, salvo regra específica.

O MVP não exige uma diplomacia geral para todos os portos.

## M3 — Comércio operacional dentro da campanha

Objetivo: transformar o comércio atual de demonstração em decisão utilizável pelo jogador.

Entregas mínimas:

- quantidade selecionável na compra e venda;
- indicação clara de capital, carga e capacidade restante;
- visualização de bens conhecidos no mercado atual;
- bloqueios de acesso e de mercadoria explicados na interface;
- pelo menos uma decisão comercial útil dentro da vertical slice;
- preservação da regra de que índices econômicos de `simulation/` não são preços históricos.

Crédito, câmbio, juros, contratos complexos e unidade monetária histórica ficam fora do MVP.

## M4 — Objetivos e encerramento da campanha

Objetivo: transformar o loop em uma experiência com progresso reconhecível e fim definido.

Criar uma camada mínima de campanha, separada do domínio econômico e náutico, capaz de registrar marcos como:

- participação na armada;
- chegada às escalas-chave;
- aquisição de conhecimento;
- contato com atores documentados;
- chegada a Calecute;
- negociação de acesso;
- primeira operação comercial elegível.

O encerramento do MVP ocorre em Calecute, com resumo da campanha: cronologia, conhecimento adquirido, relações estabelecidas, capital/carga e indicação de eventual divergência contrafactual.

Não transformar esses marcos em uma sequência rígida de quests quando a liberdade do jogador permitir outra ordem.

## M5 — Interface v0.2

Objetivo: deixar de apresentar apenas um painel técnico e oferecer uma interface suficientemente clara para jogar a vertical slice.

Prioridades:

- hierarquia visual entre mapa, porto, navio, mercado, informação, relações e viagem;
- objetivo atual e estado da campanha visíveis;
- motivo dos bloqueios apresentado em linguagem curta;
- confirmação antes de viagens relevantes;
- controles simples de quantidade no comércio;
- histórico curto de acontecimentos da sessão;
- indicação discreta, porém clara, de `GUIDED` versus `COUNTERFACTUAL`;
- preservação da regra arquitetural: Pygame apresenta estado e envia comandos; regras de negócio permanecem no domínio.

Refino estético amplo fica depois do fechamento funcional do loop.

## M6 — Persistência

Objetivo: permitir interromper e retomar a campanha.

Escopo mínimo:

- um formato versionado de save, inicialmente JSON;
- serialização de `GameSessionState`, campanha, seed e versão do schema;
- um slot de save é suficiente;
- carregamento deve reproduzir o mesmo estado e determinismo;
- teste de round-trip save/load.

Perfis, múltiplos slots, nuvem e migrações sofisticadas não são requisitos do MVP.

## M7 — Balanceamento e robustez

Objetivo: verificar que a campanha completa não cria becos sem saída artificiais nem exploração trivial dos parâmetros de simulação.

Testar, em múltiplas seeds quando aplicável:

- provisões suficientes para tornar as pernas executáveis sem concessões automáticas;
- desgaste recuperável dentro das regras existentes;
- eventos marítimos sem dominar a campanha;
- comércio sem crescimento explosivo ou arbitragem infinita evidente;
- ações de espera com custo temporal perceptível;
- informação útil sem revelar conhecimento oculto;
- ausência de vazamento de nós, rotas, atores ou mercados desconhecidos;
- comportamento determinístico para mesma seed e mesmo estado.

Ajustes de balanceamento devem ocorrer em `simulation/`; fatos históricos não devem ser alterados para melhorar o jogo.

## M8 — Gate de MVP

O MVP só pode ser marcado quando todos os itens abaixo forem verdadeiros:

- a campanha histórica inicia em Lisboa e chega a Calecute pela interface comum;
- nenhuma etapa exige `TECHNICAL` ou override de teste;
- divergências históricas mudam corretamente para `COUNTERFACTUAL`;
- mercado, acesso e relações permanecem estados distintos;
- existe ao menos uma decisão comercial real dentro da campanha;
- existem objetivos e condição explícita de encerramento;
- save/load preserva o estado;
- CI integralmente verde;
- smoke tests de interface e mapas aprovados;
- revisão Copilot sem achado concreto bloqueador após as correções;
- documentação sincronizada com o comportamento real.

Após esse gate, criar a tag de versão do MVP e somente então ampliar o horizonte cronológico.

## Pós-MVP — Primeira expansão

A expansão imediata deve continuar 1498–1505, em incrementos pequenos:

1. retorno e reconfiguração após a primeira viagem;
2. Cochim e primeiras estruturas portuguesas na costa do Malabar;
3. novas expedições e competição institucional/comercial;
4. contratos, crédito e intermediários mais ricos quando necessários;
5. cartas persistentes, mensagens e redes pessoais de informação;
6. doença, perdas materiais e tripulação apenas com modelos próprios e evidência adequada.

## Pós-MVP — Expansão 1505–1540

Somente após estabilizar a vertical slice e a primeira expansão:

- Goa;
- Ormuz;
- Malaca;
- carreiras intra-asiáticas;
- cartaz;
- comércio privado e casados;
- Coromandel, Bengala e Sudeste Asiático;
- combate e violência marítima somente quando houver modelo histórico e mecânico defensável.

## Pesquisa histórica contínua

A pesquisa permanece ativa sem bloquear o MVP quando a lacuna não impede o loop. Continuam válidas as seguintes prioridades:

- refinar cronologias editoriais do `Roteiro` quando novas edições/fontes permitirem;
- melhorar âncoras cartográficas provisórias sem inventar precisão;
- introduzir perfis de vento direcionais somente quando documentados por trecho;
- normalizar novos atores somente quando houver base documental suficiente;
- ampliar cestas portuárias e rotas apenas quando necessárias à campanha ou à expansão planejada;
- preservar divergências entre fontes em vez de harmonizá-las silenciosamente.

## Decisões resolvidas

- Python 3.12 + pygame-ce no primeiro jogável;
- domínio independente da interface;
- dados históricos separados dos parâmetros de simulação;
- preços históricos não são inventados;
- linhas do mapa são arestas do grafo, não derrotas navegadas;
- coordenadas dos nós não são deslocadas para resolver colisões de rótulos;
- conhecimento de nó, conhecimento de rota, acesso institucional, relação com ator e comando de expedição são estados distintos;
- personagem e Coroa possuem estados de conhecimento separados;
- aquisição de informação não copia silenciosamente o estado da Coroa;
- rumor não produz conhecimento operacional;
- contato mercantil melhora conhecimento comercial/geográfico sem conferir navegação operacional;
- consulta a piloto fica limitada a `PARTIAL` e não substitui pilotagem/experiência;
- alvos informativos provêm apenas de rotas/nós documentados e excluem `STRATEGIC_AGGREGATE`;
- `FOREIGN_NEGOTIATED` exige negociação explícita na v0.1;
- negociação genérica não cobra dinheiro, não quantifica presentes e não sorteia êxito diplomático;
- `ROYAL_MONOPOLY` e `ROYAL_MONOPOLY_LEASED` não são abertos por negociação portuária genérica;
- `ANCHORAGE_CONTACT` e `NAVIGATION_ONLY` não geram mercado;
- restrição de mercadoria é independente do acesso ao porto;
- relações v0.1 usam `UNESTABLISHED` e `CONTACTED`, não reputação global numérica;
- ator não documentado não é criado apenas para completar uma ação ou tela;
- autoridade e comunidade mercantil de Calecute não são comprimidas em uma única facção;
- contato relacional não concede por si só acesso, preço, crédito ou bônus;
- atores não contatados não são revelados pela interface;
- piloto documentado não recebe bônus quantitativo não sustentado;
- `FLEET_COMMAND` não aumenta conhecimento pessoal antes da viagem;
- observação exata de viagem tem precedência sobre ruído/extrapolação e sobre evento aleatório em cronologia `GUIDED`;
- eventos marítimos v0.1 são `SIMULATION`, no máximo um por viagem e limitados a tempo/provisões/condição;
- evento genérico não representa calmaria, tempestade ou avaria histórica específica;
- em `COUNTERFACTUAL`, uma rota/data historicamente observada pode receber evento de simulação;
- itinerário Lisboa–Calecute é segmentado em pernas executáveis, mantendo conexões agregadas apenas como camada estratégica;
- ancoradouro logístico não é convertido automaticamente em mercado;
- datas editoriais do `Roteiro` são marcadas como reconstruções;
- `observed_stay_days` permanece distinto da diferença aritmética entre datas editoriais;
- espera histórica avança apenas o relógio e não concede recursos automaticamente;
- atraso além da partida documentada converte a sessão em cronologia contrafactual em vez de forçar datas históricas;
- limite de provisões continua parâmetro abstrato mesmo quando calibrado para acomodar uma perna histórica longa;
- serviço desconhecido não é tratado como ausente nem disponível;
- cenários técnicos permanecem explicitamente separados do estado histórico.

## Decisões abertas até o MVP

Somente decisões que podem bloquear a vertical slice devem ser resolvidas antes do MVP:

- protagonista e enquadramento mínimo da campanha, apenas no grau necessário para apresentar objetivos e encerramento;
- representação definitiva de quantidade/capacidade suficiente para controles de compra e venda;
- conjunto mínimo de estados relacionais além de `CONTACTED`, se os efeitos do MVP realmente exigirem;
- formato de persistência e versão inicial do schema de save.

## Decisões pós-MVP

Não devem expandir o escopo atual:

- classes detalhadas de navio e velocidades relativas;
- controle detalhado de tripulação;
- doenças, perdas de tripulação/carga, encalhe e naufrágio;
- combate marítimo;
- unidade monetária histórica definitiva;
- cartas, espionagem e desinformação;
- desenho visual definitivo da interface;
- hierarquias completas de capitães, mestres, pilotos, escrivães, marinheiros e soldados.

Essas decisões devem continuar sendo tomadas por pequenos protótipos, pesquisa e testes, não por documentação especulativa.