# Relatório de aplicação — Ondas 1 e 2 (RNA TEA)

**Data:** 2026-11-21
**Autorização:** "autorizo as duas ondas"
**Spec:** `SPEC-auditoria-rna-tea-aplicacao.md`
**Gate:** `verificar_correcao.py` — **22/22 PASS**

## 1. Integridade

| Artefato | SHA-256 | Bytes |
|---|---|---:|
| Original `producao_cientifica/Redes Neurais - TEA Dataset VBA.xlsm` | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` | 106.971.375 |
| Cópia corrigida `auditoria/Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` | 100.159.091 |

O original **não foi modificado**. A diferença de tamanho deve-se principalmente à
recompactação do ZIP e à remoção intencional de `xl/calcChain.xml` (170.736 bytes), cuja
cadeia ficaria obsoleta após a inserção das novas fórmulas. O conteúdo preservado inclui
25 planilhas, 36 gráficos, 55 desenhos, 22 arquivos de mídia e 104 tabelas.

## 2. O que mudou

### Onda 1 — correções estruturais

1. **`K20` nas 5 abas de RNA**: `MAX(0.1*z, z)` → `MAX(-0.1*z, z)`. `K21` já estava correto.
2. **Rótulos**: `Acurácia` → `1 - EQM (nao acuracia)`; `Erro Total` → `EQM medio do treino`.
3. **`AG35/AH35`**: removida a divisão por 100; agora espelham `R16` e `S16`.
4. **VBA `Módulo3.SOLVER1`**: `SolverReset`, um único `SolverOk`, `StepThru:=False`,
   `SolverSolve(UserFinish:=True)`, semente 1 preservada e log de status em `AM16`.
5. **VBA `Módulo4`**: aspas tipográficas U+201C/U+201D substituídas por aspas ASCII.
6. **Nomes definidos**: removidos resíduos de template (`Bananas`, `Laranjas`, `Maçãs`,
   `Limões`, `lst_Fruta`, `lst_TipoDeFruta`, `ImpostoSobreVendas`, `Remessa`) e a entrada
   `Pesos` com 7 referências `#REF!`.
7. **PerformanceCache** dos dois módulos alterados foi zerado para impedir execução de
   p-code desatualizado; `oletools` não aponta stomping.

### Onda 2 — documentação e métricas

8. **Texto corrigido** de 60 para 30 imagens de teste em `drawing15.xml` e na aba
   `EXPERIMENTOS | RESUMO`. As imagens faltantes **não** foram recuperadas.
9. **Bloco `S144:V149` em cada aba de RNA** com n, TP, TN, FP, FN, acurácia,
   sensibilidade, especificidade, VPP, VPN e IC 95% (Wilson), além de definições de
   perda (EQM médio), softmax/argmax e proveniência dos pesos.
10. **`T157`** traz o aviso explícito: `CACHE ORIGINAL - NAO VALIDADO apos K20; Solver nao reexecutado`.
11. **`fullCalcOnLoad="1"`**: o Excel recalculará o forward pass ao abrir.

## 3. Métricas calculadas do cache original

Valores derivados de `G145:G174` (esperado) e `R145:R174` (previsto em cache), antes da
correção do `K20`. Não são estimativas de desempenho clínico nem resultado de novo treino.

| Aba | Acurácia | Sens. | Esp. | VPP | VPN | IC 95% (Wilson) |
|---|---:|---:|---:|---:|---:|---:|
| Rede Neural \|n120\|n40\|n116\|n86 | 0,6333 | 0,5333 | 0,7333 | 0,6667 | 0,6111 | 0,4551–0,7813 |
| Rede Neural \|n120\|n40\|n116\|n50 | 0,7333 | 0,6000 | 0,8667 | 0,8182 | 0,6842 | 0,5555–0,8582 |
| Rede Neural \|n119\|n72\|n1\|n73 | 0,6333 | 0,5333 | 0,7333 | 0,6667 | 0,6111 | 0,4551–0,7813 |
| Rede Neural \|n120\|n40\|n119\|n72 | 0,8000 | 0,8000 | 0,8000 | 0,8000 | 0,8000 | 0,6269–0,9050 |
| Rede Neural \|n19\|n99\|n120\|n40\| | 0,9000 | 0,9333 | 0,8667 | 0,8750 | 0,9286 | 0,7438–0,9654 |

Matrizes de confusão (TP/TN/FP/FN), respectivamente: `8/11/4/7`, `9/13/2/6`,
`8/11/4/7`, `12/12/3/3` e `14/13/2/1`.

## 4. Limitações que permanecem

- **Solver não reexecutado.** Os pesos em cache pertencem ao modelo anterior. Como `K20`
  foi corrigido e o recálculo está habilitado, ao abrir no Excel as previsões e métricas
  mudarão; esse novo estado **ainda não é um modelo retreinado**.
- **VBA recompilação não verificada no Office.** O p-cache foi invalidado, mas não há
  host Excel neste ambiente para confirmar a recompilação na primeira abertura.
- **Entropia cruzada/estabilização não aplicadas.** A perda continua sendo EQM; alterá-la
  invalidaria os pesos em cache e exigiria novo treino com protocolo registrado.
- **30 imagens ausentes.** A documentação agora diz 30, mas as imagens de teste não estão
  no workbook.
- **Objetivo transcultural não testado.** Não há dados de Crateús-CE nem amostra externa.
- **Nenhuma alegação clínica.** Não há referência-padrão, calibração, sensibilidade
  externa nem análise de vazamento de feature selection.

## 5. Como reproduzir

```bash
.venv/bin/python -m marceloclaro.cli doctor
.venv/bin/python producao_cientifica/auditoria/verificar_auditoria.py   # 10/10 (original)
.venv/bin/python producao_cientifica/auditoria/aplicar_correcoes.py    # gera a cópia
.venv/bin/python producao_cientifica/auditoria/verificar_correcao.py   # 22/22 (cópia)
```

`doctor` com `.venv/bin/python`: 16 checks passed, 6 warned, 0 failed. Com `python3` do
sistema falha por `ModuleNotFoundError: whoosh`; usar o ambiente virtual do projeto.
