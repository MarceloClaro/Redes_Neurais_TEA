# Especificação da auditoria — Redes Neurais - TEA Dataset VBA.xlsm

**ID:** SPEC-AUD-TEA-001
**Data:** 2026-11-21
**Orquestrador:** marceloclaro
**Status:** executada (achaços confirmados por verificação determinística)

## 1. Objetivo

Avaliar, sem alterar o artefato original, a correção técnica, a validade metodológica e a
robustez computacional do workbook `producao_cientifica/Redes Neurais - TEA Dataset VBA.xlsm`,
produzindo recomendações priorizadas e um módulo VBA candidato a substituição.

## 2. Escopo

Incluído: estrutura OOXML, código VBA (fonte e p-code), fórmulas das 5 abas de RNA, bloco de
teste, resumo dos experimentos, texto científico em caixas de texto, nomes definidos, dados
brutos e metadados de integridade.

Fora de escopo: reexecução do Solver do Excel (não disponível neste ambiente), avaliação
clínica do método, verificação externa de DOI, e coleta de novos dados.

## 3. Critérios de aceitação

| ID | Critério | Método |
|---|---|---|
| AC-1 | Nenhuma modificação no `.xlsm` original | hash SHA-256 antes/depois |
| AC-2 | Todo achado crítico é reproduzível por script | `verificar_auditoria.py` imprime PASS por achado |
| AC-3 | Código VBA proposto compila conceitualmente | sintaxe VBA revisada; `SolverSolve` com `UserFinish` |
| AC-4 | Distinção explícita entre fato observado e inferência | relatório separa as duas seções |
| AC-5 | Nenhuma alegação de precisão/acurácia validada sem dado | relatório não endossa "96%" |

## 4. Decisões de não intervenção

- O arquivo original **não foi alterado**: correções de metodologia exigem decisão do autor
  (redefinição de métrica e reexecução do Solver).
- Subagentes de ML e de código falharam por indisponibilidade de assinatura/região do
  OpenCode Go; a verificação foi feita localmente com `oletools`, `pcodedmp`, `openpyxl`
  e parser OOXML direto. Registro em lição de ambiente.
