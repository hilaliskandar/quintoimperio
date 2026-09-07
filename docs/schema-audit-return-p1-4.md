# P1.4 — Checklist de auditoria de schema para o retorno

Status: preparação do gate técnico. Nenhuma alteração de código ou dados neste arquivo.

Antes de inserir o retorno em `data/`, verificar os seguintes pontos no domínio e CSVs existentes:

1. Evidência: existe campo capaz de registrar camada da fonte e confiança sem sobrecarregar `notes`?
2. Datas: o schema aceita data ausente, intervalo ou variantes sem escolher arbitrariamente um dia?
3. Expedição: `expedition_routes` aceita redução da frota entre pernas?
4. Comando: é possível alterar responsável por uma embarcação em meio à expedição sem reescrever a identidade do navio?
5. Personagem: a trajetória de Vasco da Gama pode divergir da do S. Gabriel depois de São Tiago?
6. Nó náutico: `nodes.csv` aceita baixio/ilha/marco sem mercado e sem serviços?
7. Observação: uma parada ritual ou um ponto de sondagem pode permanecer em `voyage_observations`/evento sem virar node operacional?
8. Não regressão: a expansão pode ficar desativada/fora do fluxo do MVP até Calecute?

O resultado desta auditoria deve produzir uma decisão binária por item: `SUPPORTED`, `SUPPORTED_WITH_NOTES`, `SCHEMA_GAP`. Apenas itens `SCHEMA_GAP` justificam alteração estrutural.