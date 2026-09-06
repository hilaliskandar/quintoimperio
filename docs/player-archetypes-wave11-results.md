# Onda 11 — 10 arquétipos, 200 sessões

A primeira bateria completa executou 20 sessões independentes para cada um dos dez arquétipos definidos em `player-archetypes-playtest.md`, totalizando 200 sessões. O workflow e a agregação concluíram com sucesso.

## Resultado por arquétipo

| Arquétipo | Conclusões | Counterfactual | Mediana de ações | Mediana de bloqueios | Leitura principal |
|---|---:|---:|---:|---:|---|
| GRAND_STRATEGIST | 20/20 | 0 | 56 | 5 | planejamento de horizonte é robusto |
| SURVIVALIST | 20/20 | 0 | 57 | 7 | redundância adicional não aumenta conclusão, mas aumenta ações/bloqueios de serviço |
| MERCHANT | 20/20 | 0 | 56 | 5 | logística compatível com operação comercial mais agressiva |
| SPEEDRUNNER | 0/20 | 20 | 16 | 6 | tentativa de avançar sem orientação quebra cronologia e encontra falta de provisões |
| ROGUELIKE | 0/20 | 0 | 7 | 1 | política sem recuperação encerra cedo na primeira insuficiência logística |
| ROLEPLAYER | 20/20 | 0 | 56 | 5 | fluxo guiado e interpretação histórica são compatíveis com conclusão |
| EXPLORER | 3/20 | 20 | 29 | 5 | inspeção sem adesão à margem não basta; exploração deriva para atraso e falta de provisões |
| OPTIMIZER | 20/20 | 0 | 56 | 3 | horizonte + margem pública é suficiente com menor incidência mediana de bloqueios |
| COMPLETIONIST | 20/20 | 0 | 56 | 5 | segurança adicional e interações não prejudicam conclusão |
| CASUAL | 20/20 | 0 | 57 | 5 | orientação pública é suficiente mesmo com política menos especializada |

Total: **143/200 conclusões (71,5%)**. Houve **40/200 sessões counterfactual**, concentradas integralmente em SPEEDRUNNER e EXPLORER.

## Diagnóstico inicial

A bateria separa três famílias de comportamento. Arquétipos que aceitam a orientação logística e a cronologia guiada concluíram 100% das sessões. O OPTIMIZER obteve a mesma robustez com mediana de apenas três bloqueios, reforçando que o horizonte logístico + margem de 20 dias é suficiente sem necessidade de reserva adicional. O SURVIVALIST, apesar de mais prudente, não obteve ganho de conclusão e encontrou mais bloqueios de serviço, mostrando que excesso de reserva não é necessariamente vantajoso.

SPEEDRUNNER e ROGUELIKE falham por desenho: o primeiro testa insistência em avanço imediato e produz desvio cronológico; o segundo simula baixa tolerância a erro/recuperação e termina na primeira insuficiência. O caso mais informativo é EXPLORER: consultar avisos sem aderir à recomendação produz apenas 3/20 conclusões e 20/20 trajetórias counterfactual. Isso sugere que informação disponível e comportamento de planejamento devem ser avaliados separadamente.

Todos os arquétipos registraram pelo menos um bloqueio. Os bloqueios mais frequentes no conjunto foram `HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE`, `SERVICE_UNAVAILABLE`, `INSUFFICIENT_PROVISIONS` e `ONBOARD_PROVISION_CAP_REACHED`. Parte deles é esperada porque certos arquétipos tentam serviço ou avanço em condições deliberadamente inadequadas; não devem ser tratados automaticamente como defeitos do domínio.

## Próximo uso da bateria

A onda 11 deve funcionar como painel de regressão comportamental. Alterações futuras de interface, planejamento, serviços portuários, comércio ou campanha podem repetir as mesmas 200 sessões para verificar quais estilos ganham ou perdem robustez. A comparação deve preservar os arquétipos e seeds antes de qualquer recalibração.
