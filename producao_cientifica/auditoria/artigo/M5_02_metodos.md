# 2 Materiais e métodos

## 2.1 Desenho

Trata-se de auditoria técnica com reparo de artefato, configurada como estudo de caso metodológico. O desenho é observacional, determinístico e baseado em evidências extraídas de bytes, fórmulas, streams e valores em cache do arquivo. Não é ensaio clínico, não é estudo de validação diagnóstica, não é revisão sistemática e não é investigação causal. Consequentemente, nenhuma afirmação sobre prevalência de transtorno do espectro autista, desempenho diagnóstico, calibração clínica ou superioridade de modelo será produzida.

A pergunta, as proposições P1–P4 e as subperguntas SP1–SP4 foram fixadas antes da execução. As proposições são verificáveis no artefato: inspeção direta detecta falhas ocultas; "Acurácia" é recuperável como `1 − EQM`; edição direta do ZIP preserva a estrutura; e recálculo obrigatório exige rotulagem dos valores antigos.

## 2.2 Artefato e proveniência

O original foi preservado com SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`. A cópia auditada no estado pré-r1291 tinha SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`. O pacote continha 25 planilhas originais, das quais cinco abas de RNA; 120 registros de treino por aba e 30 registros de teste por aba, nas linhas `145–174`. A integridade estrutural considerou 36 gráficos, 55 desenhos, 22 itens de mídia e 104 tabelas.

| Nível | Unidade | Evidência | Instrumento |
|---|---|---|---|
| N1 | Artefato | Hash e inventário do ZIP | `hashlib`, `zipfile` |
| N2 | Aba de RNA | Fórmulas, rótulos, avisos, bloco de teste | `xml.etree.ElementTree` |
| N3 | Célula | `K20`, `K21`, `R16`, `S16`, `AG35`, `AH35`, `T157` | Leitura de `<f>` e `<v>` |
| N4 | Stream OLE/VBA | `Módulo3`, `Módulo4`, `PerformanceCache`, nomes definidos | Descompactação MS-OVBA própria |
| N5 | Registro de teste | `G145:G174`, saídas `O:Q`, acertos em `S:V` | Leitura de cache, sem reexecução |

## 2.3 Procedimentos de auditoria

Os procedimentos foram executados sem Microsoft Excel e sem Solver. Não se usou `openpyxl.save`, que reescreveria desenhos e gráficos.

| ID | Procedimento | Saída verificável |
|---|---|---|
| OP-01 | Calcular hashes do original e da cópia | Dois SHA-256 distintos e registrados |
| OP-02 | Inventariar partes do ZIP | Contagens originais preservadas |
| OP-03 | Comparar a diferença entre pacotes | Única remoção: `xl/calcChain.xml` |
| OP-04 | Extrair `K20` e `K21` nas cinco abas | Assimetria no original; `-0.1` na cópia |
| OP-05 | Extrair `R16` e `S16` | EQM médio e `1 − EQM` |
| OP-06 | Verificar escala de `AG35/AH35` | Ausência de divisão indevida por 100 |
| OP-07 | Buscar `#REF!` e resíduos de template | Sem referência quebrada residual |
| OP-08 | Descompactar VBA e checar p-code, aspas e chamadas duplicadas | Código aplicado e `PerformanceCache=0` |
| OP-09 | Verificar `fullCalcOnLoad` e aviso em `T157` | Presentes nas cinco abas |
| OP-10 | Recomputar TP/TN/FP/FN e proporção de acertos | Valores rotulados como diagnóstico |
| OP-11 | Aplicar teste metamórfico de sinal e de rótulo | Mudança no cálculo; rótulo altera interpretação |
| OP-12 | Reexecutar gates prévios | 10/10 e 22/22 |

O gate do original registrou 10 verificações positivas. O gate da correção registrou 22 verificações positivas. Um número é considerado aprovado somente quando a verificação correspondente é executada; nenhuma contagem é inferida de relatório anterior sem reexecução.

## 2.4 Reparo da cópia

O reparo foi feito por edição direta dos componentes OOXML e dos streams VBA/OLE. Na Onda 1, corrigiu-se `K20` de `MAX(0.1*z,z)` para `MAX(-0.1*z,z)` nas cinco abas, ajustaram-se rótulos e escalas e substituiu-se o código VBA por versões aplicadas de `Módulo3` e `Módulo4`, com compressor MS-OVBA próprio e `PerformanceCache` zerado. Na Onda 2, documentaram-se a perda e a softmax de três logits, a proveniência da perda como EQM médio e o aviso de que o cache não é válido após a correção.

A cópia recebeu `fullCalcOnLoad="1"` e teve `xl/calcChain.xml` removido, de modo que o Excel atualize as fórmulas ao abrir o arquivo. O bloco de teste contém aviso explícito em `T157`: "CACHE ORIGINAL - NAO VALIDADO apos K20; Solver nao reexecutado". Esses mecanismos destinam-se a evitar que a abertura do arquivo preserve silenciosamente números antigos como se fossem novos.

## 2.5 Recomputação e incerteza

As métricas de teste foram recomputadas do cache com fórmulas declaradas: acurácia `(TP+TN)/n`; sensibilidade `TP/(TP+FN)`; especificidade `TN/(TN+FP)`; valor preditivo positivo `TP/(TP+FP)`; valor preditivo negativo `TN/(TN+FN)`. A tolerância numérica foi `1e-12`. O intervalo de confiança de Wilson de 95% foi calculado em duas variantes: a forma padrão, `(p+z²/(2n))/(1+z²/n) ± z·√(p(1−p)/n + z²/(4n²))/(1+z²/n)`, e a forma que reproduz literalmente a fórmula textual presente nas células, na qual o termo `z²/(4n²)` é somado antes da divisão por `n`. Adotou-se `z=1,96`. Nenhuma variante foi escolhida como correta sem histórico de edição.

## 2.6 Busca bibliográfica

A etapa bibliográfica foi uma busca auditada circunscrita, não uma revisão sistemática. Foram consultadas quatro vias públicas — Crossref, PubMed, OpenAlex e Europe PMC — em 21 de novembro de 2026, com nove consultas registradas, contagens reportadas pelas APIs e critérios explícitos de inclusão e exclusão. Triagem de 14 registros resultou em 12 fontes incluídas e duas excluídas com justificativa. A ferramenta de busca web geral retornou HTTP 402, e o acesso direto ao arXiv foi bloqueado por `robots.txt`; por isso, resumos de preprints foram obtidos por índice terceirizado. Nenhuma fonte foi aceita apenas por aparecer na bibliografia de outra. O texto integral das 12 fontes ainda não foi conferido, limitação que será tratada na etapa final de formatação.

## 2.7 Critérios de decisão

Uma falha foi considerada detectada quando houve divergência entre fórmula e definição metodológica declarada, assimetria de sinal entre unidades equivalentes, referência quebrada, resíduo de template, escala indevida, p-code desatualizado ou ausência de mecanismo que impeça leitura de cache como resultado validado. O reparo foi considerado bem-sucedido quando o gate de correção atingiu 22/22, as contagens de partes foram preservadas, o hash da cópia foi registrado e o aviso de não validação esteve presente nas cinco abas.

## 2.8 Ética e transparência

Nesta etapa não houve participantes humanos. O workbook contém descritores extraídos de imagens; natureza dos dados, consentimento, anonimização, origem e referência-padrão permanecem `[A CONFIRMAR]`. Aprovação ética não foi requerida para auditoria de artefato, mas a eventual incorporação das 30 imagens dependerá de verificação `[A CONFIRMAR]`. Uso de agentes de IA na análise e na redação será declarado em seção própria, com revisão humana final pendente.

## 2.9 Diretrizes de relato

A TRIPOD+AI (COLLINS et al., 2024) é empregada como referência parcial de transparência, não como lista de conformidade, pois o estudo não desenvolve nem valida modelo clínico. A TRIPOD original (COLLINS et al., 2015) aparece apenas como contexto histórico. A PROBAST (WOLFF et al., 2019) contribui com o conceito de que falhas de análise distorcem desempenho, sem aplicação de seus 20 itens. Instrumentos de aderência (DE KANTER et al., 2026) inspiram a analogia entre uniformidade de critérios de relato e uniformidade de critérios de auditoria. STARD, CONSORT-AI e PRISMA não se aplicam: não há estudo de acurácia diagnóstica, ensaio clínico ou revisão sistemática. Adota-se, portanto, checklist próprio de auditoria computacional com identificador do artefato, hash, data, executor, versão do Python, comando exato e resultado.
