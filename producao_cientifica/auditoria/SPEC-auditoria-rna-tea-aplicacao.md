# Especificação de aplicação — Ondas 1 e 2 (RNA TEA)

**ID:** SPEC-AUD-TEA-002
**Data:** 2026-11-21
**Orquestrador:** marceloclaro
**Status:** aplicada; gate determinístico 22/22 PASS
**Autorização do usuário:** "autorizo as duas ondas"

## 1. Objetivo

Aplicar, em cópia, as correções das Ondas 1 e 2 previstas em `RELATORIO_AUDITORIA.md`,
preservando integralmente o `.xlsm` original e separando claramente correção estrutural,
documentação e limitações inferenciais.

## 2. Produtos

| Artefato | Função |
|---|---|
| `aplicar_correcoes.py` | gera a cópia corrigida a partir do original |
| `Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` | entrega corrigida |
| `verificar_correcao.py` | gate SDD/TDD com 21 verificações deterministicas |
| `RELATORIO_APLICACAO.md` | descrição do que mudou e do que permanece limitação |
| `modulo3_aplicado.bas`, `modulo4_aplicado.bas`, `vba_compress.py` | fontes OVBA aplicadas |

## 3. Critérios de aceitação

| ID | Critério | Verificação |
|---|---|---|
| AC-1 | Original intacto (SHA-256 conhecido) | G-01 |
| AC-2 | Cópia gerada, ZIP íntegro, 25 planilhas, gráficos/desenhos/mídia/tabelas preservados | G-02..G-06b |
| AC-3 | Nomes residuais e `#REF!` removidos | G-07, G-08 |
| AC-4 | `K20` corrigido nas 5 abas; `K21` preservado | G-13, G-14 |
| AC-5 | Rótulos e escala de `AG35/AH35` corrigidos | G-15, G-16 |
| AC-6 | Bloco de teste com n, TP/TN/FP/FN, acurácia, sensibilidade, especificidade, VPP/VPN e IC Wilson | G-17 |
| AC-7 | Documentação 60→30 imagens | G-10, G-11 |
| AC-8 | VBA corrigido, p-cache obsoleto invalidado e sem stomping | G-18..G-21 |
| AC-9 | Recálculo habilitado e aviso explícito de não validação | G-09, G-17 |

## 4. Decisões de implementação

1. **Edição OOXML direta**, sem `openpyxl.save`, para não perder gráficos, desenhos,
   imagens, tabelas e metadados não suportados.
2. `fullCalcOnLoad="1"` e remoção de `calcChain.xml`: qualquer abertura no Excel recalcula
   o forward pass com o `K20` corrigido. Portanto os valores em cache gravados no bloco de
   métricas são explicitamente rotulados como **CACHE ORIGINAL — NAO VALIDADO**.
3. Métricas calculadas a partir de `G145:G174` (esperado) e `R145:R174` (previsto em cache),
   com IC 95% Wilson. Não há alegação de desempenho clínico.
4. Perda declarada como EQM médio (`SUM(R20:R139)/120`); classificação declarada como
   softmax de 3 logits seguido de argmax. Não foi introduzida entropia cruzada, pois isso
   exigiria redesenho do objetivo e novo treino.
5. VBA: `Módulo3` reescrito com `SolverReset`, `SolverOk` único, `StepThru:=False`,
   `UserFinish:=True`, semente 1 e log em `AM16`; `Módulo4` com aspas ASCII. O
   PerformanceCache dos dois módulos foi zerado para evitar execução de p-code obsoleto.
6. As 30 imagens ausentes não foram recuperadas; apenas a documentação foi corrigida.

## 5. Fora de escopo / não executado

- Reexecução do Solver do Excel (não disponível neste ambiente).
- Recompilação real do VBA pelo host Office; o cache foi invalidado, mas a recompilação
  depende da primeira abertura/edicião no Excel.
- Novas imagens, novo feature selection, amostra externa, calibração ou validação clínica.
