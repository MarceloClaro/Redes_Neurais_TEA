# M3 — Projeto metodológico, diretriz de relato e ética

**Artefato:** rascunho para aprovação
**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Data:** 22 de novembro de 2026
**Orquestrador:** marceloclaro

## 1. Desenho adotado

Auditoria técnica com reparo de artefato — estudo de caso metodológico de um workbook `.xlsm` específico. O desenho é **observacional, determinístico e baseado em artefato**: toda evidência deriva de bytes, fórmulas, streams e valores em cache presentes no arquivo.

| O que este estudo **é** | O que este estudo **não é** |
|---|---|
| Auditoria de implementação | Ensaio clínico |
| Estudo de caso metodológico | Estudo de validação diagnóstica |
| Reparo em cópia com preservação de estrutura | Revisão sistemática (M2 foi busca auditada, sem PRISMA) |
| Recomputação diagnóstica de cache | Inferência causal ou estimativa de eficácia clínica |
| Proposição de checklist computacional | Demonstração de conformidade com checklist clínico |

Consequência: nenhuma afirmação sobre prevalência de TEA, desempenho diagnóstico, calibração clínica ou superioridade de modelo será feita.

## 2. Pergunta e proposições operacionalizadas

Pergunta central (M0, inalterada): *Como falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas, e quais controles determinísticos permitem detectá-las e repará-las sem destruir o artefato original?*

| Proposição (M1) | Operacionalização em M3 | Critério de refutação |
|---|---|---|
| P1 — inspeção direta detecta falhas ocultas | Verificações sobre OOXML e streams VBA, sem abrir no Excel | Nenhuma falha encontrada nas verificações |
| P2 — "Acurácia" é recuperável como `1 − EQM` | Extrair `S16 = SUM(-R16,1)` e `R16 = SUM(R20:R139)/120` no XML | Fórmula diferente da esperada |
| P3 — edição direta do ZIP preserva a estrutura | Comparar contagens de partes e hashes; exceção documentada `calcChain.xml` | Perda de gráfico, desenho, mídia ou tabela |
| P4 — recálculo obrigatório exige rotulagem | Verificar `fullCalcOnLoad="1"`, ausência de `calcChain.xml` e aviso em `T157` | Aviso ausente em alguma aba |

## 3. Unidades de análise

| Nível | Unidade | O que é observado | Instrumento |
|---|---|---|---|
| N1 | Artefato | Hash SHA-256, inventário de partes do ZIP | `hashlib`, `zipfile` |
| N2 | Aba de RNA (5 abas) | Fórmulas, rótulos, avisos, bloco de teste | `xml.etree.ElementTree` |
| N3 | Célula / fórmula | `K20`, `K21`, `R16`, `S16`, `AG35`, `AH35`, `T157` | Leitura de `<f>` e `<v>` |
| N4 | Stream OLE / VBA | `Módulo3`, `Módulo4`, `PerformanceCache`, `dir`, nomes definidos | Descompactação MS-OVBA própria |
| N5 | Registro de teste (30 por aba) | `G145:G174`, saídas `O:Q`, acertos em `S:V` | Leitura de cache — **não** reexecução |

Não há unidade humana neste marco. A eventual inclusão das 30 imagens em M4 dependerá de decisão de proveniência e autorização (seção 8).

## 4. Procedimentos determinísticos

Todos executáveis sem Microsoft Excel e sem Solver. Nenhum procedimento usa `openpyxl.save`, que reescreveria desenhos e gráficos.

| ID | Procedimento | Saída esperada |
|---|---|---|
| OP-01 | Calcular SHA-256 do original e da cópia | `1c4c94ab…953dcd` e `3320701b…bb475` |
| OP-02 | Inventariar partes do ZIP por tipo | 25 planilhas, 36 gráficos, 55 desenhos, 22 mídias, 104 tabelas |
| OP-03 | Confirmar única parte removida | `xl/calcChain.xml` |
| OP-04 | Extrair fórmulas de `K20`/`K21` nas 5 abas | `MAX(-0.1*z,z)` na cópia; `0.1` no original |
| OP-05 | Extrair `R16` e `S16` | EQM médio e `1 − EQM` |
| OP-06 | Verificar escala de `AG35/AH35` | Ausência de divisão indevida por 100 |
| OP-07 | Procurar `#REF!` e resíduos de template em nomes definidos | Nenhuma referência quebrada residual |
| OP-08 | Descompactar VBA e checar `PerformanceCache=0`, `StepThru`, aspas tipográficas e chamadas duplicadas a `SolverOk` | Código aplicado conforme `modulo3_aplicado.bas` e `modulo4_aplicado.bas` |
| OP-09 | Verificar `fullCalcOnLoad` e aviso em `T157` nas 5 abas | Presentes |
| OP-10 | Recomputar TP/TN/FP/FN e proporção de acertos a partir do cache | Valores rotulados como **diagnóstico do estado original** |
| OP-11 | Teste metamórfico: alterar sinal de `K20` deve modificar o forward pass; renomear rótulo de métrica não altera o número, mas altera a interpretação | Mudança observada no primeiro caso; apenas interpretação no segundo |
| OP-12 | Reexecutar gates `verificar_auditoria.py` e `verificar_correcao.py` | 10/10 e 22/22 |

## 5. Critérios de decisão

### Falha detectada

- Divergência entre fórmula e definição metodológica declarada (ex.: rótulo "Acurácia" sobre `1 − EQM`).
- Assimetria de sinal entre unidades operando a mesma ativação (`K20` vs `K21`).
- Referência quebrada (`#REF!`), resíduo de template ou escala indevida.
- p-code/VBA desatualizado em relação ao código-fonte aplicado.
- Valor em cache sem mecanismo que impeça sua leitura como resultado validado.

### Reparo considerado bem-sucedido

- 22/22 verificações do gate de correção.
- Contagens de partes preservadas, com apenas `calcChain.xml` removido.
- Hash da cópia registrado e distinto do original.
- `fullCalcOnLoad="1"` nas 5 abas e aviso explícito no bloco de teste.
- Nenhuma alegação de desempenho do modelo corrigido enquanto o Solver não for reexecutado.

## 6. Decisão sobre diretrizes de relato

| Diretriz | Decisão | Justificativa |
|---|---|---|
| **TRIPOD+AI** (F01) | **Referência parcial de transparência; não aplicada como checklist de conformidade** | Orienta relato de modelos preditivos; este estudo não desenvolve nem valida modelo clínico. Usar seus princípios gerais (declarar dados, método, limitações) sem afirmar conformidade com os 27 itens |
| **TRIPOD 2015** (F02) | Contexto histórico | Substituída pelo TRIPOD+AI para estudos com ML |
| **PROBAST** (F03) | Conceito emprestado; instrumento **não aplicado** | "Falha de análise distorce desempenho" é útil; os 20 itens avaliam estudos de predição, não artefatos |
| **Adherence TRIPOD+AI** (F04) | Analogia metodológica | Uniformidade de critérios para julgar relato ↔ uniformidade de critérios para julgar artefato |
| **STARD / CONSORT-AI** | **Não aplicáveis** | Não há estudo de acurácia diagnóstica nem ensaio clínico |
| **PRISMA** | **Não aplicável** | M2 foi busca auditada circunscrita, não revisão sistemática |

**Instrumento adotado:** checklist próprio de auditoria computacional, derivado das 22 verificações já executadas e das 12 operações OP-01..OP-12, com campos obrigatórios de proveniência: identificador do artefato, hash, data, executor, versão do Python, comando exato e resultado. O artigo declarará explicitamente que **nenhuma diretriz clínica foi preenchida** e que o checklist proposto não substitui avaliação de risco de viés de estudos clínicos.

Essa decisão evita dois erros: (i) apresentar conformidade com diretriz inadequada; (ii) usar a ausência de diretriz clínica como desculpa para não adotar critérios rigorosos.

## 7. Plano de análise para M4

1. Recomputar TP/TN/FP/FN e proporção de acertos a partir do cache das 5 abas, com denominador explícito (`n=30` por aba).
2. Calcular intervalo de confiança Wilson de 95% com fórmula e parâmetros declarados no próprio script. **O valor de IC citado em resumos anteriores não foi reproduzido neste marco e não será reutilizado sem recálculo auditável.**
3. Maior valor observado em cache: `0,9000` na aba `Rede Neural |n19|n99|n120|n40|` — sempre rotulado como diagnóstico do estado original, nunca como desempenho do modelo reparado.
4. Se o Solver for reexecutado pelo usuário: registrar versão do Excel e do Solver, data, `seed=1` quando aplicável, status de convergência e pesos finais com hash. Novo resultado será comparado ao cache **como mudança de estado computacional**, não como validação clínica.
5. Teste pareado (McNemar) apenas se houver duas execuções pareadas com a mesma amostra; sem isso, não aplicar.
6. AUC, calibração e curvas ROC/PR dependem de saídas contínuas e referência-padrão; ficam fora de escopo até que esses dados existam.
7. Nenhuma generalização além do artefato analisado.

## 8. Ética, proveniência e transparência

| Item | Posição neste marco |
|---|---|
| Participantes humanos | Nenhum neste marco |
| Imagens humanas | O workbook contém descritores extraídos de imagens; natureza, consentimento e anonimização: `[A CONFIRMAR]` |
| Uso das 30 imagens em M4 | Condicionado a proveniência, autorização e, se exigido, aprovação ética: `[A CONFIRMAR]` |
| Afirmação clínica | Vedada neste marco e no seguinte sem referência-padrão e amostra externa |
| Aprovação ética | Não requerida para auditoria de artefato; eventual necessidade em M4: `[A CONFIRMAR]` |
| Financiamento | `[A CONFIRMAR]` — não declarar ausência sem confirmação |
| Conflitos de interesse | `[A CONFIRMAR]` — não declarar ausência sem confirmação |
| Autoria e contribuições | `[A CONFIRMAR]` |
| Uso de IA | Declarar orquestração por agente e uso de modelos na análise e redação, com revisão humana final |
| Local de deposição de dados/código | `[A CONFIRMAR]`; `producao_cientifica/` está no `.gitignore` e não foi alterado sem autorização |

## 9. Reprodutibilidade computacional

- **Ambiente:** Python 3 da pasta `.venv`; biblioteca padrão para ZIP/XML/hash; compressor MS-OVBA próprio em `vba_compress.py`.
- **Dependências externas:** nenhuma necessária para os gates; `openpyxl` não é usado para salvar.
- **Semente:** `seed=1` registrada como parâmetro pretendido do Solver, mas **Solver não reexecutado neste ambiente**.
- **Logs:** comandos e saídas dos gates de 10/10, 22/22, 14/14 e 23/23; hashes do original e da cópia.
- **Limite:** reprodutibilidade da **auditoria** está demonstrada; reprodutibilidade do **treino** permanece pendente até M4 com o log do usuário.

## 10. Matriz de riscos e mitigação

| Risco | Mitigação adotada | Status |
|---|---|---|
| Cache lido como resultado validado | `fullCalcOnLoad`, remoção de `calcChain`, aviso em `T157`, rótulo "diagnóstico" | Mitigado no artefato |
| Destruição de gráficos/mídia na edição | Edição direta do ZIP + gate de integridade 22/22 | Mitigado e verificado |
| Diretriz clínica inadequada forçada | Decisão explícita da seção 6 | Mitigado neste marco |
| Generalização indevida de `n=30` | Delimitação e IC com denominador; sem inferência clínica | Mitigado na redação |
| Número de IC herdado sem recálculo | Recálculo obrigatório em M4 com fórmula declarada | Mitigado neste marco |
| Artefatos fora do controle de versão | Risco registrado; `[A CONFIRMAR]` local de deposição | Pendente |
| Proveniência/ética das imagens | `[A CONFIRMAR]`; imagens não integradas | Pendente |
| Solver não reexecutado | Log futuro com versão, status, seed e pesos; antes disso, apenas cache diagnóstico | Pendente |
| Qualidade das fichas de M2 baseada só em resumos | Limite registrado; conferência de texto integral antes de citações longas em M5/M6 | Parcialmente mitigado |

## 11. Critérios de aceitação do marco

| ID | Critério |
|---|---|
| AC-M3-1 | Desenho declarado com negações explícitas (não clínico, não causal, não revisão sistemática) |
| AC-M3-2 | Cinco níveis de unidade de análise e 12 operações definidas |
| AC-M3-3 | Decisão justificada sobre TRIPOD+AI, PROBAST, STARD, CONSORT-AI e PRISMA |
| AC-M3-4 | Checklist próprio com campos de proveniência |
| AC-M3-5 | Ética e pendências marcadas, sem afirmação inventada |
| AC-M3-6 | Solver não reexecutado e cache rotulado como diagnóstico |
| AC-M3-7 | Matriz de riscos com mitigação e status |

## 12. Pendências para M4

1. `[A CONFIRMAR]` natureza, origem, autorização e anonimização das 30 imagens.
2. `[A CONFIRMAR]` log do Solver: versão do Excel/Solver, data, `seed`, status, pesos finais.
3. `[A CONFIRMAR]` financiamento, conflitos, autoria, instituição, periódico e prazo.
4. Recalcular estatísticas do cache com fórmula auditável; não reutilizar IC anterior.
5. Conferir texto integral das fontes F01–F12 antes de citações diretas em M5.
