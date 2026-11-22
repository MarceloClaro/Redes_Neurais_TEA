# M4 — Métricas recomputadas do cache

**Classificação:** DIAGNOSTICO DO ESTADO ORIGINAL - cache gerado antes da correcao de K20; Solver NAO reexecutado

**Arquivo:** `auditoria/Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` · **SHA-256:** `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`

**Gerado em:** 2026-11-22T00:35:18-03:00 · **Script:** `recomputar_cache.py`

| Aba | n | TP | TN | FP | FN | Acurácia cache | Recalculada | Sens. | Esp. | EQM (R16) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Rede Neural \|n119\|n72\|n1\|n73 | 30 | 8 | 11 | 4 | 7 | 0.6333 | 0.6333 | 0.5333 | 0.7333 | 0.198766 |
| Rede Neural \|n120\|n40\|n116\|n50 | 30 | 9 | 13 | 2 | 6 | 0.7333 | 0.7333 | 0.6000 | 0.8667 | 0.235776 |
| Rede Neural \|n120\|n40\|n116\|n86 | 30 | 8 | 11 | 4 | 7 | 0.6333 | 0.6333 | 0.5333 | 0.7333 | 0.275909 |
| Rede Neural \|n120\|n40\|n119\|n72 | 30 | 12 | 12 | 3 | 3 | 0.8000 | 0.8000 | 0.8000 | 0.8000 | 0.180387 |
| Rede Neural \|n19\|n99\|n120\|n40\| | 30 | 14 | 13 | 2 | 1 | 0.9000 | 0.9000 | 0.9333 | 0.8667 | 0.197131 |

## Divergência detectada na fórmula do intervalo de confiança

Em todas as abas, o valor em cache de `T155/T156` é compatível com a forma padrão da fórmula de Wilson. A fórmula **textualmente presente** nas células, se avaliada, produz um intervalo mais estreito. O script calcula as duas variantes e registra a comparação no JSON. Não se afirma qual versão é a correta sem o histórico de edição do arquivo.

| Aba | IC cache | Wilson padrão | Fórmula textual da célula | Compatível com cache |
|---|---|---|---|---|
| Rede Neural \|n119\|n72\|n1\|n73 | [0.455132, 0.781263] | [0.455132, 0.781263] | [0.464978, 0.771417] | padrão |
| Rede Neural \|n120\|n40\|n116\|n50 | [0.555517, 0.858175] | [0.555517, 0.858175] | [0.566182, 0.847510] | padrão |
| Rede Neural \|n120\|n40\|n116\|n86 | [0.455132, 0.781263] | [0.455132, 0.781263] | [0.464978, 0.771417] | padrão |
| Rede Neural \|n120\|n40\|n119\|n72 | [0.626940, 0.904950] | [0.626940, 0.904950] | [0.638633, 0.893257] | padrão |
| Rede Neural \|n19\|n99\|n120\|n40\| | [0.743786, 0.965401] | [0.743786, 0.965401] | [0.758863, 0.950323] | padrão |

## Limites

- Estes números descrevem o **cache original**, não o modelo após a correção de `K20`.
- O Solver não foi reexecutado neste ambiente.
- `n=30` por aba; intervalos são largos e não autorizam generalização.
- A abertura do workbook no Excel com `fullCalcOnLoad` atualizará os valores; o aviso em `T157` deve ser preservado.
