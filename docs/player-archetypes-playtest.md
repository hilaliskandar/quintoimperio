# Bateria de arquétipos de jogadores sintéticos

Esta bateria amplia os playtests do MVP sem pretender classificar usuários reais. Cada arquétipo é uma política deliberadamente estilizada que aborda a campanha Lisboa–Calecute como se o jogador viesse de um gênero ou tradição de jogo diferente. Todos usam apenas informações e ações públicas do domínio.

## Arquétipos

| Arquétipo | Referência de estilo | Comportamento dominante | Pressão de teste |
|---|---|---|---|
| `GRAND_STRATEGIST` | grand strategy / 4X | planeja o horizonte logístico completo, segue margem e aceita mais ações preventivas | qualidade do planejamento de longo alcance |
| `SURVIVALIST` | survival / expedition management | mantém redundância elevada e margem adicional de 20 dias sobre a recomendação | robustez com excesso de prudência |
| `MERCHANT` | trading / tycoon | assegura a rota, evita reserva adicional deliberada e tenta comprar maior volume em Calecute | interação logística-comércio |
| `SPEEDRUNNER` | speedrun / action optimization | tenta partir imediatamente, não consulta recomendação e recupera apenas após bloqueio duro | clareza dos blockers e recuperação |
| `ROGUELIKE` | roguelike / permadeath | aceita risco, ignora margem preventiva e encerra quando um erro exige recuperação | severidade de falhas não recuperadas |
| `ROLEPLAYER` | historical RPG / roleplay | segue cronologia, recomendações e contatos documentados | coerência da experiência guiada |
| `EXPLORER` | exploration / adventure | consulta avisos e interage com atores, mas não transforma a recomendação em meta logística | legibilidade de incertezas e descoberta |
| `OPTIMIZER` | puzzle / systems optimization | usa exatamente horizonte + margem recomendada e evita reservas extras | suficiência mínima da heurística pública |
| `COMPLETIONIST` | completionist / achievement hunting | acumula segurança, realiza contatos e comércio, aceitando maior número de ações | compatibilidade entre sistemas e excesso de ações |
| `CASUAL` | casual / tutorial-led | segue orientação básica, faz pouca preparação adicional e reage a problemas visíveis | tolerância do fluxo a baixa especialização |

## Desenho da bateria

A onda 11 executa 20 sessões independentes para cada um dos dez arquétipos, totalizando 200 sessões. As seeds são determinísticas e separadas por arquétipo. O workflow usa dez jobs, cada qual executando sequencialmente suas vinte sessões, evitando transformar 200 sessões em 200 instalações independentes do projeto.

Cada sessão registra conclusão, objetivo corrente, cronologia, bloqueios, capacidade de recuperação, ações tentadas e executadas, consultas e adesão à recomendação logística, avisos de evidência indeterminada, reabastecimentos, autonomia e condição mínimas, viagens, esperas, negociação de acesso, comércio, data e local finais, capital e carga.

## Interpretação

As diferenças entre arquétipos são intencionais. Uma taxa de conclusão menor não significa necessariamente defeito: `ROGUELIKE` e `SPEEDRUNNER`, por exemplo, existem justamente para testar políticas que recusam prudência preventiva. O diagnóstico relevante é onde cada política falha, se o bloqueio é inteligível, se a recuperação prevista funciona e se a interface pública oferece informação suficiente para os perfis que decidem consultá-la.

A bateria não deve ser usada para recalibrar dados históricos. Não altera `nodes.csv`, datas observadas, disponibilidade `UNKNOWN`/`NONE`, eventos, preços ou regras históricas. Ajustes posteriores devem distinguir problema de UX, política sintética e regra substantiva antes de modificar parâmetros do jogo.
