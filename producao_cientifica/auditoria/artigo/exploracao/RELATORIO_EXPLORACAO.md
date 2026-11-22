# Analise exploratoria separada do cache M4 (SPEC-935-R1291)

**Classificacao:** DIAGNOSTICO DO CACHE - NAO e resultado validado do modelo corrigido.

**Fonte unica:** `../M4_metricas_cache.json` — SHA-256 `7c428cdb81756c426e24ee8664f994bb0ca78fb967624abf2e1210ed3de69e5f`.

**Semente:** 20261122. **Replicas bootstrap:** 2000. **z de Wilson:** 1.96.

> Este documento e diagnostico do estado original em cache. Nao representa desempenho do arquivo corrigido, nao valida o modelo e nao autoriza conclusao clinica. Nenhum dado externo foi acrescentado.

## 1. Metricas recompostas e intervalos

| Aba | TP/TN/FP/FN | Acuracia | IC Wilson (recomp.) | IC Wilson (cache) | Coincide |
|---|---|---:|---|---|---|
| Rede Neural \|n119\|n72\|n1\|n73 | 8/11/4/7 | 0,6333 | [0,4551; 0,7813] | [0,4551; 0,7813] | sim |
| Rede Neural \|n120\|n40\|n116\|n50 | 9/13/2/6 | 0,7333 | [0,5555; 0,8582] | [0,5555; 0,8582] | sim |
| Rede Neural \|n120\|n40\|n116\|n86 | 8/11/4/7 | 0,6333 | [0,4551; 0,7813] | [0,4551; 0,7813] | sim |
| Rede Neural \|n120\|n40\|n119\|n72 | 12/12/3/3 | 0,8000 | [0,6269; 0,9050] | [0,6269; 0,9050] | sim |
| Rede Neural \|n19\|n99\|n120\|n40\| | 14/13/2/1 | 0,9000 | [0,7438; 0,9654] | [0,7438; 0,9654] | sim |

O intervalo de Wilson foi recomputado a partir de TP+TN e n. A coincidencia com o cache e esperada e nao constitui validacao externa; a divergencia com a formula textual do workbook permanece sem causa resolvida e nao foi alterada.

## 2. Comparacao de criterios de decisao (nao de limiares)

O cache nao contem probabilidades individuais. Em vez de inventar um limiar, comparou-se o ranqueamento das mesmas cinco matrizes sob criterios de decisao distintos. Isso mostra que a nocao de 'melhor' depende do objetivo, sem afirmar ganho de classificacao.

| Criterio | 1o | 2o | 3o |
|---|---|---|---|
| Acuracia | Rede Neural \|n19\|n99\|n120\|n40\| (0,9000) | Rede Neural \|n120\|n40\|n119\|n72 (0,8000) | Rede Neural \|n120\|n40\|n116\|n50 (0,7333) |
| Sensibilidade | Rede Neural \|n19\|n99\|n120\|n40\| (0,9333) | Rede Neural \|n120\|n40\|n119\|n72 (0,8000) | Rede Neural \|n120\|n40\|n116\|n50 (0,6000) |
| Especificidade | Rede Neural \|n120\|n40\|n116\|n50 (0,8667) | Rede Neural \|n19\|n99\|n120\|n40\| (0,8667) | Rede Neural \|n120\|n40\|n119\|n72 (0,8000) |
| F1 | Rede Neural \|n19\|n99\|n120\|n40\| (0,9032) | Rede Neural \|n120\|n40\|n119\|n72 (0,8000) | Rede Neural \|n120\|n40\|n116\|n50 (0,6923) |
| Acuracia balanceada | Rede Neural \|n19\|n99\|n120\|n40\| (0,9000) | Rede Neural \|n120\|n40\|n119\|n72 (0,8000) | Rede Neural \|n120\|n40\|n116\|n50 (0,7333) |
| J de Youden | Rede Neural \|n19\|n99\|n120\|n40\| (0,8000) | Rede Neural \|n120\|n40\|n119\|n72 (0,6000) | Rede Neural \|n120\|n40\|n116\|n50 (0,4667) |

A mudanca de posicoes entre criterios e uma hipotese sobre prioridades de decisao. Para escolher um criterio seria necessario definir custos de falso positivo e falso negativo em contexto clinico, o que nao esta disponivel neste material.

## 3. Bootstrap diagnostico das matrizes

Reamostragem binomial dentro de cada classe verdadeira (15/15), com semente fixa. Intervalos percentis de 95% descrevem variabilidade do cache reamostrado, nao da populacao.

| Aba | Acuracia mediana [IC p95] | Sens. mediana [IC p95] | Esp. mediana [IC p95] |
|---|---|---|---|
| Rede Neural \|n119\|n72\|n1\|n73 | 0,6333 [0,4667; 0,8000] | 0,5333 [0,2667; 0,8000] | 0,7333 [0,5333; 0,9333] |
| Rede Neural \|n120\|n40\|n116\|n50 | 0,7333 [0,6000; 0,8667] | 0,6000 [0,3333; 0,8000] | 0,8667 [0,6667; 1,0000] |
| Rede Neural \|n120\|n40\|n116\|n86 | 0,6333 [0,4667; 0,8000] | 0,5333 [0,2667; 0,8000] | 0,7333 [0,5333; 0,9333] |
| Rede Neural \|n120\|n40\|n119\|n72 | 0,8000 [0,6333; 0,9333] | 0,8000 [0,6000; 1,0000] | 0,8000 [0,6000; 1,0000] |
| Rede Neural \|n19\|n99\|n120\|n40\| | 0,9000 [0,7667; 1,0000] | 0,9333 [0,8000; 1,0000] | 0,8667 [0,6667; 1,0000] |

## 4. Sensibilidade a erro de rotulo (cenario hipotetico)

Cenario mecanico: k erros de rotulo incidindo sobre acertos TEA e NAO_TEA, com predicoes inalterados. Acertos TEA trocados viram FP; acertos NAO_TEA trocados viram FN. Nao e observacao nem estimativa de erro real de anotacao.

| Aba | k=0 | k=1 | k=2 | k=3 |
|---|---:|---:|---:|---:|
| Rede Neural \|n119\|n72\|n1\|n73 | 0,6333 | 0,5667 | 0,5000 | 0,4333 |
| Rede Neural \|n120\|n40\|n116\|n50 | 0,7333 | 0,6667 | 0,6000 | 0,5333 |
| Rede Neural \|n120\|n40\|n116\|n86 | 0,6333 | 0,5667 | 0,5000 | 0,4333 |
| Rede Neural \|n120\|n40\|n119\|n72 | 0,8000 | 0,7333 | 0,6667 | 0,6000 |
| Rede Neural \|n19\|n99\|n120\|n40\| | 0,9000 | 0,8333 | 0,7667 | 0,7000 |

## 5. Declaracoes

- Nao ha scores individuais no cache; nenhum limiar de probabilidade foi inventado.
- Criterios de decisao foram comparados sobre a matriz observada; a escolha do criterio muda o ranqueamento.
- Bootstrap reamostra celulas da matriz, nao casos originais; incerteza e diagnostica, nao populacional.
- Perturbacao de rotulo e cenario mecanico hipotetico incidindo sobre acertos.
- Nenhuma acuracia, sensibilidade ou especificidade aqui e validade diagnostica.
- Nenhum ganho de classificacao do modelo corrigido e afirmado; Solver nao foi reexecutado.

## 6. Proximo passo necessario para qualquer afirmativa de melhoria

Somente uma reexecucao documentada do Solver no Excel — com versao, data, status de convergencia, semente, arquivo salvo e pesos finais com hash — permitiria comparar o estado corrigido com o cache. Ate la, toda discusao sobre 'melhor classificacao' permanece hipotetica.

