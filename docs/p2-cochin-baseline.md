# P2 — baseline funcional mínimo de Cochim

Data: 2026-09-07

Issue funcional: #108
PR de integração: #109
Commit de merge: `7b8a19ca3313095790d0ce1760b98aa270fa9e5f`
CI da branch: run `34121642510` — success
CI pós-merge em `main`: run `34122650263` — success

## Escopo integrado

O primeiro incremento funcional de P2 incorpora Cochim sem introduzir nova mecânica específica:

- nó `COC` com âncora cartográfica moderna de trabalho e confiança `MEDIUM`;
- acesso `FOREIGN_NEGOTIATED`;
- `PEPPER` como única mercadoria indispensável no recorte inicial;
- autoridade institucional local `ACT_COC_RAJA_1500`, sem harmonização artificial do nome pessoal do governante;
- comunidades mercantis Mappila e cristã síria como atores agregados documentados;
- rota `R_CAL_COC` como `PREEXISTING_NETWORK`, explicitando que a conexão costeira antecede a presença portuguesa;
- testes específicos de mercado, negociação e compra de pimenta em Cochim reutilizando as regras gerais existentes.

## Não regressão

A CI pós-merge confirmou:

- validação integral dos dados;
- testes de domínio verdes;
- protótipos de economia, navegação, viagem, serviços e comércio verdes;
- sessão integrada verde;
- retorno Lisboa–Calecute–BRG preservado;
- diagnósticos de Santa Maria e carena de Anjediva preservados;
- interfaces e persistência verdes;
- cartografia verde.

## Restrições preservadas

Continuam fora do baseline P2 atual:

- `EXP_CABRAL_1500` como campanha jogável;
- fortificação, guarnição e guerra de 1503+;
- qualquer representação de Cochim como posse portuguesa;
- preços históricos inventados;
- câmbio, crédito ou contratos sistêmicos;
- cesta comercial ampliada por retroprojeção;
- novas regras econômicas específicas de Cochim.

## Regra de continuidade

O próximo gate deve partir deste baseline e não reabrir o P1 nem ampliar Cochim por conveniência de jogabilidade. Qualquer expansão adicional deve começar por questão documental estreita, seguida de implementação mínima e regressão contra este commit.
