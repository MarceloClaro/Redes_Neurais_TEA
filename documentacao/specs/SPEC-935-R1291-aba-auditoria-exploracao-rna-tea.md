# SPEC-935-R1291 — Aba de auditoria no workbook corrigido e exploração estatística separada (TEA)

**ID:** SPEC-935-R1291
**Data:** 2026-11-22
**Orquestrador:** marceloclaro
**Status:** proposed — aguardando execução
**Autorização do usuário:** inserir aba de relatório M7 no `.xlsm` corrigido; revalidar cadeia; análise exploratória separada; não integrar log do Solver nem imagens (não enviados)
**Relacionada:** SPEC-935-R1282 (M0–M7 entregues)

## 1. Objetivo

Acrescentar ao workbook corrigido uma aba documental que registre a cadeia de auditoria M7, e produzir, em arquivos separados, uma análise exploratória de técnicas de classificação **sem alterar o modelo treinado, sem reexecutar o Solver e sem reivindicar desempenho do modelo corrigido**.

## 2. Escopo

### Incluído
- Nova aba `AUDITORIA_M7` no `.xlsm` corrigido, com: hashes, marcos e gates reexecutados, falhas detectadas, reparo aplicado, pendências, delimitações éticas e aviso de que valores em cache não são resultado validado.
- Preservação integral de todas as partes existentes do pacote OOXML (planilhas, gráficos, desenhos, mídia, tabelas, VBA, nomes definidos).
- Novo hash da cópia corrigida e reexecução integral da bateria de gates.
- Análise exploratória em `producao_cientifica/auditoria/artigo/exploracao/`:Accuracy por aba com IC de Wilson, comparação de limiares de decisão, bootstrap estratificado determinístico e sensibilidade a erros de rótulo — sempre rotulada como diagnóstico do cache.

### Fora de escopo
- Reexecução do Solver, novos pesos, nova arquitetura ou alteração de `K20`/`S16`/`AG35`.
- Integração das 30 imagens ou de log do Solver.
- Edição da fórmula textual do IC (Onda 3), que continua exigindo autorização explícita separada.
- Alegação de acurácia validada, desempenho diagnóstico, validade clínica, Qualis, nota, aceite ou superioridade.

## 3. Critérios de aceitação

| ID | Critério | Verificação |
|---|---|---|
| AC-1 | Aba `AUDITORIA_M7` presente e legível sem macros | `verificar_r1291.py` G-02 |
| AC-2 | Todas as 25 planilhas originais preservadas; aba nova é a 26ª | G-03 |
| AC-3 | 36 gráficos, 55 desenhos, 22 mídias, 104 tabelas preservados | G-04 |
| AC-4 | VBA íntegro; `PerformanceCache` zerado; `fullCalcOnLoad=1` mantido | G-05 |
| AC-5 | `xl/calcChain.xml` permanece ausente | G-06 |
| AC-6 | Texto da aba declara explicitamente que cache não é resultado validado e que Solver/imagens estão pendentes | G-07 |
| AC-7 | Aviso em `T157` permanece | G-08 |
| AC-8 | Nenhuma fórmula das abas de RNA alterada | G-09 |
| AC-9 | Hash antigo e novo registrados; bateria completa reexecutada com gates verdes | G-10, G-11 |
| AC-10 | Análise exploratória separada, determinística, com semente fixa e sem tocar no workbook | G-12, G-13 |
| AC-11 | Exploração nunca afirma ganho de acurácia do modelo corrigido | G-14 |
| AC-12 | SPEC, relatório e declarações atualizados sem apagar pendências | G-15 |

## 4. Riscos conhecidos

- Alterar o `.xlsm` muda o hash `3320701b...`; todos os artefatos que o citam precisam ser regenerados.
- Inserir uma aba via edição direta de OOXML pode corromper relacionamentos se feito sem cuidado; a estratégia é mínima e validada por abertura ZIP econtagem de partes.
- Análise exploratória sobre `n=30` produz intervalos largos; qualquer diferença entre limiares é hipótese, não conclusão.
- A acurácia em cache (0,6333–0,9000) é diagnóstico do estado original; otimizar limiar sobre o mesmo conjunto é overfitting e será declarado como tal.
