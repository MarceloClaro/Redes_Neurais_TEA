# Relatório R1291 — aba de auditoria e exploração estatística separada

**Spec:** `specs/SPEC-935-R1291-aba-auditoria-exploracao-rna-tea.md`
**Data:** 2026-11-22
**Orquestrador:** marceloclaro
**Autorização do usuário:** inserir aba de relatório M7; revalidar cadeia; análise exploratória separada
**Status:** gates determinísticos locais; sem revisão externa, sem aceite editorial e sem validade clínica declarada

## 1. Cadeia de hashes

| Artefato | SHA-256 | Papel |
|---|---|---|
| `producao_cientifica/Redes Neurais - TEA Dataset VBA.xlsm` | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` | original preservado |
| `backup/Redes_Neurais_TEA_Dataset_VBA_corrigido.pre_r1291.xlsm` | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` | estado pré-r1291, descrito em M4–M7 |
| `Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` | `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb` | estado atual, com `AUDITORIA_M7` |

## 2. O que foi alterado

A aba documental `AUDITORIA_M7` foi inserida por edição mínima de OOXML (`xl/workbook.xml`, `xl/_rels/workbook.xml.rels`, `[Content_Types].xml` e `xl/worksheets/sheet26.xml`). Todas as demais partes do pacote foram copiadas byte a byte, inclusive `xl/vbaProject.bin`. A aba usa strings inline e não toca em `sharedStrings.xml`.

Foram preservadas as 25 planilhas originais, 36 gráficos, 55 desenhos, 22 mídias e 104 tabelas. `xl/calcChain.xml` permanece ausente; `fullCalcOnLoad="1"` e `PerformanceCache` zerado foram reconfirmados. Nenhuma fórmula das cinco abas de RNA foi alterada.

A aba registra hashes, gates reexecutados, falhas detectadas no original, reparo aplicado, pendências e o aviso de que valores em cache não são resultado validado. Ela não contém macros nem cálculo.

## 3. Exploração estatística separada

Os artefatos ficam em `producao_cientifica/auditoria/artigo/exploracao/`:

- `analise_exploratoria.py` — gerador determinístico, semente `20261122`;
- `resultados_exploratorios.json` — saída numérica;
- `RELATORIO_EXPLORACAO.md` — relatório legível.

A fonte única é `M4_metricas_cache.json` (SHA-256 `7c428cdb81756c426e24ee8664f994bb0ca78fb967624abf2e1210ed3de69e5f`). Foram executados: recomputação de Wilson, comparação de seis critérios de decisão sobre as matrizes observadas, bootstrap binomial estratificado por classe com 2.000 réplicas e sensibilidade mecânica a erro de rótulo (`k=0..3`).

O cache não contém escores ou probabilidades individuais. Portanto, nenhum limiar numérico foi inventado: a seção sobre decisão compara critérios, não limiares. O bootstrap reamostra células da matriz, não casos originais, e fornece incerteza diagnóstica do cache, não inferência populacional.

O melhor cache permanece `Rede Neural |n19|n99|n120|n40|` com TP14/TN13/FP2/FN1 e acurácia 0,9000. Sob especificidade, a aba `|n120|n40|n116|n50` empata em 0,8667. Essa mudança de ranqueamento é hipótese sobre prioridades de decisão, não ganho de classificação.

## 4. Bateria reexecutada

| Gate | Resultado |
|---|---|
| `verificar_auditoria.py` | 10/10 |
| `verificar_correcao.py` | 22/22 |
| `verificar_m0_m1.py` | 14/14 |
| `verificar_m2.py` | 23/23 |
| `verificar_m3.py` | 20/20 |
| `verificar_m4.py` | 22/22 |
| `verificar_m5.py` | 24/24 |
| `verificar_m6.py` | 33/33 |
| `verificar_m7.py` | 24/24 |
| `verificar_r1291.py` | 15/15 |
| `.venv/bin/python -m marceloclaro.cli doctor` | 16 passed, 6 warned, 0 failed |

`verificar_r1291.py` reexecuta os nove gates anteriores como subprocessos e exige que nenhum produza linha `FAIL`.

## 5. Pendências preservadas

- Nenhum log do Solver chegou: faltam versão do Excel/Solver, data, status de convergência, seed, arquivo salvo e pesos finais com hash.
- Nenhuma das 30 imagens chegou: faltam proveniência, natureza, consentimento, anonimização, licença e referência-padrão.
- A Onda 3 (edição da fórmula textual do IC) continua sem autorização explícita e não foi executada; a causa da divergência do IC permanece não resolvida.
- Periódico-alvo, instituição, prazo, financiamento, conflitos, autoria, local de depósito, abstract e parâmetros de diagramação permanecem `[A CONFIRMAR]`.
- O texto integral das fontes F01–F13 não foi conferido; M2/M5/M6 usaram resumos, metadados e auditoria por DOI.
- Não houve revisão externa real; a banca M7 foi simulação heurística local.
- `producao_cientifica/` permanece no `.gitignore` do workspace de origem; a produção científica foi publicada em `https://github.com/MarceloClaro/Redes_Neurais_TEA` no commit `374afb0`, sem o workbook original (106.971.375 bytes, acima do limite de 100 MiB), cujo hash está registrado no README.

## 6. Veredito circunscrito

A aba documental foi inserida e a cadeia de gates determinísticos foi revalidada. A exploração separada é diagnóstica e não estabelece desempenho do modelo corrigido, validade diagnóstica, calibração clínica, Qualis, nota ou aceite. Nenhuma melhoria de classificação é afirmada sem reexecução documentada do Solver e validação externa.
