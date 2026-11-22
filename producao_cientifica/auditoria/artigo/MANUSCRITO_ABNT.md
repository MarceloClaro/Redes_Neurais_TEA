# Auditoria metodológica de um pipeline de rede neural artificial em planilha eletrônica

**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Marco:** M6 — versão formatada para revisão humana
**Norma:** ABNT NBR 14724 (apresentação), NBR 6023 (referências) e NBR 10520 (citações)
**Status:** rascunho formatado; nenhuma aprovação editorial, nota ou Qualis é declarada
**Original preservado:** SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`
**Cópia auditada (estado pré-r1291):** SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`

**Extensão R1291:** em 2026-11-22 a cópia corrigida recebeu a aba documental `AUDITORIA_M7`, sem alterar modelos, fórmulas ou VBA. Hash atual: SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. O hash pré-r1291 citado nas seções abaixo identifica o estado descrito neste manuscrito. A cópia passou a ter 26 planilhas (25 originais mais a aba documental). A análise exploratória separada é diagnóstico do cache e não afirma desempenho do modelo corrigido.

---

# Resumo

Planilhas eletrônicas são usadas há décadas para prototipar redes neurais artificiais porque reúnem dados, fórmulas, macros e gráficos em um único artefato. Essa concentração facilita o uso, mas dificulta a inspeção da lógica de ativação, da função-objetivo e do significado dos rótulos de métricas. Objetivou-se propor e aplicar um protocolo determinístico de auditoria e reparo a um pipeline de RNA hospedado em arquivo `.xlsm`, preservando o original e separando valores em cache de resultado validado. Foram executadas inspeção direta de OOXML e de streams VBA/OLE, reparo em cópia com edição do pacote ZIP, recomputação auditável das métricas de teste e busca bibliográfica documentada em quatro APIs públicas. O original passou por 10 verificações e a cópia por 22, com preservação de 25 planilhas, 36 gráficos, 55 desenhos, 22 mídias e 104 tabelas; apenas `xl/calcChain.xml` foi removido. Foram identificados erro de sinal na ativação, rótulo "Acurácia" aplicado a `1 − EQM`, escala indevida e p-code obsoleto. Nas cinco abas, as métricas em cache foram internamente coerentes (`n=30` por aba; valores de 0,6333 a 0,9000) e o argmax das saídas coincidiu com a classe reportada em 30/30 registros. Também se detectou divergência entre o valor de intervalo de confiança em cache e a fórmula textual da célula. O Solver não foi reexecutado e as 30 imagens não foram integradas; portanto, nenhum desempenho do modelo corrigido é afirmado. Conclui-se que a auditoria determinística detecta falhas de implementação e que a rotulagem de proveniência destina-se a evitar que cache seja lido como resultado validado, sem estabelecer validade diagnóstica.

**Palavras-chave:** auditoria de software; planilha eletrônica; rede neural artificial; reprodutibilidade computacional; OOXML.

# Abstract

`[A CONFIRMAR EXIGÊNCIA DE ABSTRACT PELO PERIÓDICO]`

Spreadsheets have long been used to prototype artificial neural networks because data, formulas, macros and charts coexist in a single artifact. This concentration supports immediate use but obscures activation logic, objective definition and metric labels. This study proposes and applies a deterministic audit and repair protocol to an ANN pipeline hosted in an `.xlsm` file, preserving the original and separating cached values from validated results. Direct inspection of OOXML and VBA/OLE streams was combined with repair of a copy through ZIP package editing, auditable recomputation of test metrics and a documented bibliographic search across four public APIs. The original passed 10 checks and the repaired copy passed 22, with 25 worksheets, 36 charts, 55 drawings, 22 media items and 104 tables preserved; only `xl/calcChain.xml` was removed. Detected failures included a sign error in activation, an "Accuracy" label applied to `1 − MSE`, an invalid scale and outdated VBA p-code. Across five sheets, cached metrics were internally consistent (`n=30` per sheet; 0.6333 to 0.9000), and output argmax matched the reported class in 30/30 records. A mismatch was also found between the cached confidence interval and the cell formula. Solver was not rerun and the 30 images were not integrated, so no performance of the repaired model is claimed. The protocol detects implementation failures and provenance labeling is intended to prevent cached values from being read as validated results; diagnostic validity is not established.

**Keywords:** software audit; spreadsheet; artificial neural network; computational reproducibility; OOXML.

---

# 1 Introdução

Planilhas eletrônicas ocupam posição ambígua em ciência de dados e informática em saúde. São acessíveis, ubíquas e permitem prototipar modelos sem infraestrutura de programação, mas concentram dados, lógica de cálculo, macros, gráficos e resultados em um único arquivo. Essa concentração é simultaneamente a vantagem e o risco do ambiente: o que facilita a circulação do artefato também torna opacas camadas críticas de um pipeline de aprendizado de máquina, como a função de ativação, a função-objetivo e a definição das métricas exibidas. O uso de planilhas para simular redes neurais não é recente; já foi descrito como estratégia simples de prototipagem e ensino (ANTONINI, 2002 `[A CONFIRMAR]`).

Erros em planilhas são fáceis de introduzir e difíceis de detectar. A taxonomia de Panko mostra que categorias como omissão e dimensão de ciclo de vida são frequentemente simplificadas quando a taxonomia é reutilizada (PANKO, 2008). Em contexto científico, AlTarawneh e Thorne (2017) relataram que a ausência de projeto adequado e de treinamento aparece como fator de risco em pesquisa que depende de planilhas, com consequências potenciais graves para a confiabilidade de resultados. Experimentos sobre comportamento de revisores indicam que a quantidade de células inspecionadas correlaciona-se com o número de erros corrigidos, o que expõe o limite da inspeção humana espontânea (BISHOP; MCDAID, 2008).

Já existem mecanismos de verificação estática e de compreensão de planilhas. Ahmad et al. (2004) propuseram um sistema de tipos para detectar erros por unidade em planilhas, e Amalfitano et al. (2016) desenvolveram uma ferramenta para compreender aplicações VBA, extraindo dependências entre células e elementos de interface. Esses trabalhos estabelecem precedentes importantes, mas não emitem um gate de auditoria para um pipeline de RNA nem tratam da preservação do pacote OOXML após reparo.

Em paralelo, a literatura sobre modelos preditivos em saúde consolidou a exigência de relato transparente. A TRIPOD original estabeleceu recomendações mínimas para estudos de desenvolvimento e validação de modelos diagnósticos e prognósticos (COLLINS et al., 2015), e a TRIPOD+AI ampliou e atualizou essas recomendações para modelos que empregam aprendizado de máquina (COLLINS et al., 2024). A PROBAST oferece vocabulário para risco de viés, com destaque para falhas no domínio da análise (WOLFF et al., 2019), e instrumentos de aderência mostram que a avaliação de relato depende de critérios uniformes (DE KANTER et al., 2026). Essas fontes tratam do que deve ser informado e de como julgar relato ou risco de viés; não inspecionam fórmulas, streams VBA nem caches.

A reprodutibilidade de modelos de aprendizado profundo também é tema estabelecido. Renard et al. (2020) identificaram variabilidade em segmentação de imagens médicas e recomendaram descrição adequada do arcabouço, análise de fontes de variabilidade e avaliação eficiente de resultados. Chen et al. (2022) propuseram critérios e mecanismos para lidar com aleatoriedade de software e não determinismo de hardware. Entretanto, esses trabalhos pertencem a ecossistemas de arquiteturas de aprendizado profundo, não ao Excel com Solver.

## 1.1 Lacuna circunscrita

A busca auditada executada em 21 de novembro de 2026 em Crossref, PubMed, OpenAlex e Europe PMC, com as strings e contagens registradas em protocolo próprio, **não localizou** trabalho que proponha e execute, em pipeline de RNA hospedado em planilha `.xlsm`, um protocolo determinístico que combine: inspeção direta de OOXML e de streams VBA/OLE; detecção de erro de sinal em ativação, rótulo de métrica inconsistente, escala indevida e resíduos de template; reparo em cópia com preservação de gráficos, desenhos, mídia e tabelas; e separação explícita entre valor em cache e resultado validado. Essa ausência é **circunscrita ao escopo pesquisado e não constitui prova de inexistência universal**.

A fonte mais próxima localizada foi EXACT (AMALFITANO et al., 2016), voltada à compreensão de aplicações VBA. Um trabalho limítrofe sobre auditoria e controle de ações de agentes de IA em planilhas (SABOURI et al., 2026) torna etapas de execução auditáveis, mas não inspeciona o pacote OOXML, não lida com RNA em planilha e não repara artefato. Registrá-lo evita transformar uma lacuna circunscrita em negação absoluta.

## 1.2 Pergunta e objetivos

**Pergunta central.** Como falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas, e quais controles determinísticos permitem detectá-las e repará-las sem destruir o artefato original?

**Objetivo geral.** Propor e aplicar um protocolo determinístico de auditoria e reparo para pipelines de RNA em planilha, avaliando sua capacidade de preservar o artefato e de prevenir a comunicação enganosa de métricas.

**Objetivos específicos.** (i) inventariar falhas no original por verificações reproduzíveis; (ii) reparar em cópia as falhas identificadas e documentar as demais; (iii) recomputar métricas do cache com rótulo de proveniência e incerteza; (iv) verificar a integridade estrutural da cópia; (v) derivar recomendações de reporte para estudos que usem planilhas como ambiente de modelagem.

## 1.3 Contribuição

A contribuição é metodológica e delimitada. A partir de um workbook real, deriva-se e aplica-se um protocolo que demonstra três pontos: falhas de implementação são detectáveis por inspeção do pacote; o reparo pode preservar a estrutura do artefato; e métricas em cache exigem rotulagem de proveniência para não serem confundidas com resultado validado. Não se afirma ser o primeiro protocolo de auditoria de planilhas, nem se resolve a validade clínica do modelo auditado.

---

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

---

# 3 Resultados

## 3.1 Falhas detectadas no original

A inspeção direta identificou falhas simultâneas nas cinco abas de RNA. A ativação em `K20` usava `MAX(0.1*z,z)`, enquanto `K21` usava `MAX(-0.1*z,z)`, produzindo assimetria de sinal em unidades que deveriam operar a mesma função. A célula rotulada como "Acurácia" na área de treino continha `S16 = SUM(-R16,1)`, isto é, `1 − EQM médio`, e não proporção de acertos. As células `AG35/AH35` aplicavam escala indevida por 100 a `R16/S16`. Nomes definidos conservavam resíduos de template e a entrada `Pesos` continha sete referências `#REF!`. O projeto VBA apresentava chamadas duplicadas a `SolverOk`, `StepThru:=True` e aspas tipográficas em comando.

Todas essas falhas foram detectadas sem abrir o arquivo no Excel. O gate do original registrou 10/10 verificações positivas, confirmando P1 e P2 nos termos definidos em M3.

## 3.2 Reparo e integridade estrutural

A cópia corrigida passou por 22/22 verificações no estado pré-r1291. Foram preservadas as contagens de 25 planilhas originais, 36 gráficos, 55 desenhos, 22 itens de mídia e 104 tabelas. A única parte removida do pacote foi `xl/calcChain.xml`, substituída pela exigência de recálculo mediante `fullCalcOnLoad="1"`. O hash da cópia nesse estado, `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`, diferia do original e permitia distinguir os dois estados. Após a extensão R1291, a aba documental `AUDITORIA_M7` elevou o total para 26 planilhas e o hash atual passou a ser `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`, sem alterar modelos, fórmulas ou VBA.

A ativação corrigida em `K20` passou a empregar `MAX(-0.1*z,z)`. O aviso em `T157` está presente nas cinco abas. A perda foi declarada como EQM médio e a classificação como softmax de três logits em `O:Q`, seguida de escolha da maior probabilidade. Não foi demonstrado ganho de desempenho decorrente do reparo, pois o Solver não foi reexecutado neste ambiente.

## 3.3 Métricas recomputadas do cache

A tabela seguinte apresenta os valores recomputados do cache. Todos são **diagnóstico do estado original**, gerados antes da correção de `K20`.

**Tabela 1 — Métricas recomputadas do cache pré-correção nas cinco abas de RNA.**

| Aba | n | TP | TN | FP | FN | Acurácia | Sens. | Esp. | EQM (R16) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `n120\|n40\|n116\|n86` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n116\|n50` | 30 | 9 | 13 | 2 | 6 | 0,7333 | 0,6000 | 0,8667 | 0,235776 |
| `n119\|n72\|n1\|n73` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n119\|n72` | 30 | 12 | 12 | 3 | 3 | 0,8000 | 0,8000 | 0,8000 | 0,180387 |
| `n19\|n99\|n120\|n40\|` | 30 | 14 | 13 | 2 | 1 | 0,9000 | 0,9333 | 0,8667 | 0,197131 |

Fonte: elaborado pelos autores a partir de `M4_metricas_cache.json`; workbook corrigido com SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`.

Em todas as abas, `TP+TN+FP+FN=n`, `TP+FN=15` e `TN+FP=15`, compatíveis com 15 registros `TEA` e 15 `NAO_TEA`. Acurácia, sensibilidade, especificidade, valor preditivo positivo e valor preditivo negativo armazenados no cache coincidiram com a recomputação dentro da tolerância de `1e-12`. A classe prevista em `R145:R174` coincidiu com o argmax dos três logits em `O:Q` em 30/30 registros por aba; nenhum argmax recaiu na terceira posição, cuja célula `C13` está vazia. O maior valor observado foi 0,9000 na aba `n19|n99|n120|n40|`.

Essa coerência é limitada ao próprio cache. Ela não implica que os números descrevam o modelo após a correção de `K20`.

## 3.4 Divergência na fórmula do intervalo de confiança

Ao recomputar o intervalo de confiança, o valor armazenado em `T155/T156` foi reproduzido exatamente pela forma padrão de Wilson. Na aba de maior cache, obteve-se `[0,743786; 0,965401]`. A fórmula textualmente presente nas células, avaliada literalmente com o mesmo `p` e `n`, produziu `[0,758863; 0,950323]`, intervalo mais estreito. O mesmo padrão ocorreu nas cinco abas.

Duas hipóteses permanecem não distinguidas: a fórmula foi editada sem recálculo, ou o cache provém de versão anterior da planilha. O artefato não contém histórico de edição que permita escolher entre elas. Não se afirmou qual versão é correta e o workbook não foi alterado por causa desse achado.

## 3.5 Evidência pendente

O log do Solver e as 30 imagens não foram integrados. Em consequência, não há resultado pós-correção neste manuscrito. A comparação entre cache e uma eventual reexecução será apresentada, quando houver evidência, como mudança de estado computacional, não como ganho clínico. A seleção de atributos ocorreu antes da separação treino/teste no desenho original; essa configuração é registrada como risco de vazamento de dados, sem afirmar que houve vazamento efetivo.

---

# 4 Discussão

O resultado central não é um número de desempenho, e sim uma distinção metodológica: coerência interna e validade são propriedades diferentes. O bloco de teste era aritmeticamente consistente — matrizes fechadas, rótulos 15/15, argmax coincidente com a classe reportada — e ainda assim não podia ser usado como evidência do modelo corrigido. A divergência entre o intervalo em cache e a fórmula textual tornou essa distinção ainda mais concreta: um valor plausível e reproduzível por uma fórmula padrão convivia com uma fórmula escrita que geraria intervalo distinto. Esse padrão alinha-se à dimensão de ciclo de vida destacada por Panko (2008): o mesmo artefato muda de significado conforme a etapa de edição considerada.

A detecção estática de erros em planilhas já era defendida por Ahmad et al. (2004), e a compreensão de aplicações VBA por Amalfitano et al. (2016). O presente protocolo difere pelo alvo e pela saída: em vez de verificar unidades ou apenas compreender dependências, ele verifica um pipeline de RNA e produz um gate com critérios de passagem. Também se distingue do trabalho de Sabouri et al. (2026), pois audita o artefato em repouso, não ações de agente durante execução. Essa delimitação importa para não transformar uma lacuna circunscrita em afirmação de que nada semelhante existe.

A assimetria em `K20` ilustra como um detalhe de sinal pode comprometer a comparação entre estados computacionais. Um único caractere alterado em uma função de ativação muda a passagem direta; já a troca do rótulo "Acurácia" não altera o número, mas altera radicalmente a interpretação. O teste metamórfico aplicado distingue esses dois efeitos: o sinal afeta o cálculo, enquanto o rótulo afeta apenas o significado atribuído. A inspeção humana, cuja eficiência depende do tempo de exposição às células (BISHOP; MCDAID, 2008), beneficia-se de um gate que percorre o pacote de forma exaustiva e registrável.

Sob a ótica de relato, a TRIPOD+AI (COLLINS et al., 2024) ajuda a explicar por que declarar proveniência, definição de métrica e limitações é indispensável, mesmo quando o estudo não é clínico. A PROBAST (WOLFF et al., 2019) contribui com a noção de que falhas de análise podem distorcer o desempenho reportado; a ferramenta de 20 itens, porém, não foi aplicada. A analogia com instrumentos de aderência (DE KANTER et al., 2026) reforça que critérios uniformes são necessários também para auditoria computacional. Nenhuma conformidade com TRIPOD, PROBAST, STARD, CONSORT-AI ou PRISMA é afirmada.

A separação entre reprodutibilidade da auditoria e reprodutibilidade do treino é outra implicação. Os comandos, hashes e saídas dos gates permitem repetir a auditoria; já a reprodução do treino depende de log do Solver com versão, status, semente e pesos finais. Renard et al. (2020) e Chen et al. (2022) mostraram que variabilidade e aleatoriedade exigem descrição explícita em outros ecossistemas. No Excel, a ausência de `calcChain.xml` e o aviso em `T157` cumprem papel análogo ao impedir que um estado antigo seja lido como novo.

A relevância em pesquisa de saúde é indireta, mas não desprezível. AlTarawneh e Thorne (2017) relataram risco associado ao uso de planilhas em contexto científico; o caso aqui analisado mostra uma manifestação concreta desse risco em um pipeline de classificação. A prática de simular RNAs em planilha é antiga (ANTONINI, 2002 `[A CONFIRMAR]`), o que torna pertinente discutir controles específicos para esse ambiente. Ao mesmo tempo, a ausência de amostra externa, de referência-padrão confirmada e de log de reexecução impede qualquer inferência sobre utilidade diagnóstica.

## 4.1 Recomendações operacionais

Recomenda-se que todo artefato desse tipo registre: identificador e hash; versão do executor; comando exato; fórmula textual e valor em cache lado a lado; definição explícita de perda e de métrica; sinal de ativação verificado nas unidades equivalentes; mecanismo de recálculo obrigatório; e log de otimização com versão, data, status e pesos finais. A recomendação é compatível com o caráter computacional da auditoria e não depende de adaptação de listas clínicas.

## 4.2 Limitações

O estudo examina um único workbook, cinco abas e 30 registros de teste por aba. Intervalos são largos e não autorizam generalização. O Solver não foi reexecutado, as 30 imagens não foram integradas e a proveniência ética permanece pendente. A busca bibliográfica cobriu quatro vias públicas e resumos indexados; não houve triagem cega, texto integral das fontes ou consulta a bases adicionais. A divergência de ano da fonte F12 foi mantida como `[A CONFIRMAR]`. Por fim, uma eventual edição da fórmula de intervalo exigiria autorização explícita e histórico de versões; sem isso, a causa da divergência permanece indeterminada.

---

# 5 Conclusão

A pergunta central pode ser respondida nos limites do artefato analisado. Falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas porque alteram o cálculo, o rótulo ou a proveniência do número. Controles determinísticos baseados em inspeção de OOXML e de streams VBA detectam essas falhas, e o reparo por edição direta do pacote preserva gráficos, desenhos, mídia e tabelas. No caso estudado, o original passou por 10 verificações, a cópia por 22, e a única parte removida foi `xl/calcChain.xml`.

A auditoria também mostrou que um bloco de métricas pode ser internamente coerente e ainda assim não representar o modelo corrigido. Valores entre 0,6333 e 0,9000, com `n=30`, descrevem o cache original. A divergência entre o intervalo em cache e a fórmula textual reforça a necessidade de inspecionar a fórmula, não apenas o número. Isso não estabelece validade diagnóstica nem desempenho clínico.

As contribuições são uma taxonomia aplicada de falhas, um gate reproduzível, um protocolo de reparo não destrutivo e uma regra de comunicação que separa cache diagnóstico de resultado validado. Como trabalho futuro, a integração do log do Solver e das 30 imagens deverá seguir o protocolo de proveniência já registrado; qualquer edição adicional da fórmula de intervalo dependerá de autorização explícita e histórico de versões.

---

# Referências

A ordem é alfabética pelo sobrenome do primeiro autor, conforme a NBR 6023. Campos não confirmados em fonte primária permanecem marcados como `[A CONFIRMAR]`; nenhum foi preenchido por inferência.

AHMAD, Y. et al. A type system for statically detecting spreadsheet errors. In: 18th IEEE International Conference on Automated Software Engineering, 2003. Proceedings. `[A CONFIRMAR LOCAL E EDITORA]`, 2004 `[A CONFIRMAR ANO; CROSSREF E DOI INDICAM 2003]`. p. 174-183. DOI: 10.1109/ASE.2003.1240305.

ALTARAWNEH, G.; THORNE, S. A pilot study exploring spreadsheet risk in scientific research. arXiv, 2017. `[A CONFIRMAR VERSÃO DO PREPRINT]`. DOI: 10.48550/arXiv.1703.09785.

AMALFITANO, D. et al. EXACT: A tool for comprehending VBA-based Excel spreadsheet applications. Journal of Software: Evolution and Process, v. 28, n. 6, p. 483-505, 2016. DOI: 10.1002/smr.1787.

ANTONINI, R. Spreadsheet simulation of artificial neural network. In: IJCNN-91-Seattle International Joint Conference on Neural Networks. `[A CONFIRMAR LOCAL E EDITORA]`, 2002 `[A CONFIRMAR ANO; DOI CONTÉM 1991; CROSSREF NÃO INFORMA ANO]`. v. II, p. 910. DOI: 10.1109/IJCNN.1991.155504.

BISHOP, B.; MCDAID, K. An empirical study of end-user behaviour in spreadsheet error detection & correction. arXiv, 2008. `[A CONFIRMAR VERSÃO DO PREPRINT]`. DOI: 10.48550/arXiv.0802.3479.

CHEN, B. et al. Towards training reproducible deep learning models. In: Proceedings of the 44th International Conference on Software Engineering, 2022. p. 2202-2214. `[A CONFIRMAR LOCAL E EDITORA]`. DOI: 10.1145/3510003.3510163.

COLLINS, G. S. et al. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis: the TRIPOD statement. BMC Medicine, v. 13, n. 1, p. 1, 2015. DOI: 10.1186/s12916-014-0241-z.

COLLINS, G. S. et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ, v. 385, p. e078378, 2024. DOI: 10.1136/bmj-2023-078378.

DE KANTER, E. et al. Adherence to TRIPOD+AI guideline: an updated reporting assessment tool. Journal of Clinical Epidemiology, v. 191, p. 112118, 2026. DOI: 10.1016/j.jclinepi.2025.112118.

PANKO, R. R. Revisiting the Panko-Halverson taxonomy of spreadsheet errors. arXiv, 2008. `[A CONFIRMAR VERSÃO DO PREPRINT]`. DOI: 10.48550/arXiv.0809.3613.

RENARD, F. et al. Variability and reproducibility in deep learning for medical image segmentation. Scientific Reports, v. 10, n. 1, `[A CONFIRMAR PÁGINAS OU NÚMERO DO ARTIGO]`, 2020. DOI: 10.1038/s41598-020-69920-0.

SABOURI, S. et al. Auditing and controlling AI agent actions in spreadsheets. arXiv, 2026. `[A CONFIRMAR VERSÃO DO PREPRINT]`. DOI: 10.48550/arXiv.2604.20070.

WOLFF, R. F. et al. PROBAST: A tool to assess the risk of bias and applicability of prediction model studies. Annals of Internal Medicine, v. 170, n. 1, p. 51-58, 2019. DOI: 10.7326/M18-1376.

---

# Declarações

## Disponibilidade de dados e código

O original e a cópia corrigida no estado pré-r1291 são identificados pelos hashes `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` e `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`; após a extensão R1291, o hash da cópia é `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. Os scripts de auditoria e recomputação, bem como as saídas JSON e Markdown, encontram-se em `producao_cientifica/auditoria/artigo/`. Essa pasta está listada no `.gitignore` do repositório e não foi alterada sem autorização. Local de deposição público, licença e condições de acesso: `[A CONFIRMAR]`. Se não houver repositório público, a redação final deverá declarar explicitamente a disponibilidade sob demanda.

## Uso de ferramentas de IA

A auditoria, a recomputação e a redação foram orquestradas pelo agente MarceloClaro, com apoio de modelos de linguagem para análise de metadados, conferência de fórmulas e montagem do rascunho. Comandos, hashes e gates são reproduzíveis sem dependência de serviços externos. A revisão humana final ainda não foi registrada como concluída e deve ser declarada na entrega final.

## Ética

Não houve participantes humanos nesta etapa. A auditoria foi realizada sobre artefato computacional já existente. O workbook contém descritores extraídos de imagens; natureza dos dados, origem, consentimento, anonimização, licença de uso e referência-padrão permanecem `[A CONFIRMAR]`. A incorporação das 30 imagens e a eventual necessidade de aprovação ética dependem dessas informações. Nenhuma alegação clínica é feita.

## Financiamento

`[A CONFIRMAR]` — não declarar ausência de financiamento sem confirmação.

## Conflitos de interesse

`[A CONFIRMAR]` — não declarar ausência de conflitos sem confirmação.

## Autoria e contribuições

`[A CONFIRMAR]` — nomes, afiliações, contribuições e ordem de autoria não foram fornecidos e não devem ser inventados.

## Correspondência

`[A CONFIRMAR]` — periódico-alvo, instituição, prazo e dados de contato não foram fornecidos.

---

# Apêndice A — Auditoria de referências e citações

**Fonte primária:** Crossref por DOI, consultado em 22 de novembro de 2026 pela ferramenta `auditar_referencia`. **Via suplementar:** OpenAlex, consultada nos marcos M2 e M5 para autores e anos dos preprints que não resolvem no Crossref. A triagem abaixo registra vereditos, não aprovação editorial.

| ID | DOI | Veredito na fonte primária | Metadados confirmados | Pendência registrada |
|---|---|---|---|---|
| F01 | 10.1136/bmj-2023-078378 | VERIFICADA | BMJ; v. 385; p. e078378; 2024 | nenhuma |
| F02 | 10.1186/s12916-014-0241-z | VERIFICADA | BMC Medicine; v. 13, n. 1, p. 1; 2015 | nenhuma |
| F03 | 10.7326/M18-1376 | VERIFICADA | Annals of Internal Medicine; v. 170, n. 1, p. 51-58; 2019 | nenhuma |
| F04 | 10.1016/j.jclinepi.2025.112118 | VERIFICADA | Journal of Clinical Epidemiology; v. 191, p. 112118; 2026 | nenhuma |
| F05 | 10.1038/s41598-020-69920-0 | VERIFICADA | Scientific Reports; v. 10, n. 1; 2020 | páginas ou número do artigo não retornados |
| F06 | 10.1145/3510003.3510163 | VERIFICADA | ICSE 2022; p. 2202-2214 | local e editora não confirmados |
| F07 | 10.1002/smr.1787 | VERIFICADA | Journal of Software: Evolution and Process; v. 28, n. 6, p. 483-505; 2016 | nenhuma |
| F08 | 10.48550/arXiv.0809.3613 | Crossref HTTPError; metadados conferidos em OpenAlex | arXiv; 2008; Panko | versão do preprint |
| F09 | 10.48550/arXiv.1703.09785 | Crossref HTTPError; metadados conferidos em OpenAlex | arXiv; 2017; AlTarawneh e Thorne | versão do preprint |
| F10 | 10.48550/arXiv.0802.3479 | Crossref HTTPError; metadados conferidos em OpenAlex | arXiv; 2008; Bishop e McDaid | versão do preprint |
| F11 | 10.1109/ASE.2003.1240305 | VERIFICADA | ASE 2003; p. 174-183 | ano nulo no Crossref; M5 registra 2004 e DOI/Crossref indicam 2003 |
| F12 | 10.1109/IJCNN.1991.155504 | VERIFICADA | IJCNN-91; v. II, p. 910 | ano nulo no Crossref; divergência 1991/2002 mantida |
| F13 | 10.48550/arXiv.2604.20070 | Crossref HTTPError; metadados conferidos em OpenAlex | arXiv; 2026; Sabouri et al. | versão do preprint |

**Conferência citação ↔ referência.** As 13 fontes incluídas aparecem no corpo e na lista; nenhuma referência adicional foi acrescentada na formatação final. Nenhum DOI foi inferido, corrigido por semelhança ou tomado apenas da bibliografia de outra fonte. O ano de F12 continua marcado como `[A CONFIRMAR]`, e a divergência de F11 foi registrada sem alteração silenciosa do ano citado no corpo.

---

# Apêndice B — Triagem de força de alegação

**Instrumento:** `auditar_forca_alegacao`, triagem heurística por regex sobre 199 frases do manuscrito. **Resultado automático:** 10 achados, status `revisar`. A ferramenta não prova ausência de excesso; a decisão final abaixo é humana e cada item foi mantido apenas com âncora no texto, delimitação explícita ou verificação já executada.

| ID | Marcador heurístico | Trecho sinalizado | Decisão humana | Fundamento |
|---|---|---|---|---|
| A1 | quantificador absoluto | nenhum desempenho do modelo corrigido é afirmado | manter | Delimitação de escopo; Solver não reexecutado e imagens não integradas. |
| A2 | causalidade/demonstração | não constitui prova de inexistência universal | manter | O próprio trecho é o mitigador da lacuna circunscrita. |
| A3 | quantificador absoluto | nenhuma afirmação sobre prevalência... será produzida | manter | Declaração de não inferência clínica, não resultado. |
| A4 | quantificador absoluto | nenhuma contagem é inferida de relatório anterior sem reexecução | manter | Regra metodológica de gate; todas as contagens foram rerodadas. |
| A5 | quantificador absoluto | nenhuma variante foi escolhida como correta sem histórico de edição | manter | Ausência de histórico é fato observado no artefato. |
| A6 | quantificador absoluto | todos são diagnóstico do estado original | manter | Proveniência explicitada na seção 3.3 e no JSON M4. |
| A7 | quantificador absoluto | nenhum argmax recaiu na terceira posição | manter | Verificação determinística de 30/30 registros por aba. |
| A8 | efeito/eficácia | a fórmula textual... produziu intervalo mais estreito | manter | Resultado de avaliação literal da fórmula, com números e tolerância declarados. |
| A9 | causalidade/demonstração | workbook não foi alterado por causa desse achado | manter | Descrição de decisão de edição, não alegação de efeito clínico. |
| A10 | quantificador absoluto | nenhuma conformidade com TRIPOD, PROBAST, STARD, CONSORT-AI ou PRISMA é afirmada | manter | Delimitação de diretrizes; nenhuma lista de conformidade foi aplicada. |

Nenhum achado foi removido por conveniência. A heurística tende a sinalizar absolutos mesmo quando eles são usados para negar inferências indevidas; por isso, a revisão humana preservou as frases e registrou a razão. Não se conclui que o manuscrito esteja livre de toda forma de excesso.

---

# Apêndice C — Notas de formatação ABNT

Este apêndice registra a conferência das normas ABNT NBR 14724 (apresentação de trabalhos acadêmicos), NBR 6023 (referências) e NBR 10520 (citações). O arquivo entregue é Markdown; quando a regra depende de editor, a parametrização fica explícita para conversão futura.

| Elemento | Regra adotada | Situação |
|---|---|---|
| Papel e orientação | A4, 210 mm × 297 mm, impressão frente e verso | `[A CONFIRMAR PELO PERIÓDICO]` |
| Margens | superior e esquerda de 3 cm; inferior e direita de 2 cm | `[A CONFIRMAR PELO PERIÓDICO]` |
| Fonte e corpo | Times New Roman ou Arial, 12 pt | `[A CONFIRMAR PELO PERIÓDICO]` |
| Espaçamento | 1,5 entre linhas; simples em citações longas, notas de rodapé, referências e legendas | adotado no mapeamento para conversão |
| Citações longas | mais de três linhas, recuo de 4 cm da margem esquerda, sem aspas, espaço simples | adotado no mapeamento para conversão |
| Alinhamento | justificado | adotado no mapeamento para conversão |
| Paginação | algarismos arábicos, canto superior direito; primeira página sem número | `[A CONFIRMAR PELO PERIÓDICO]` |
| Títulos | seções primárias numeradas em algarismos arábicos e em maiúsculas; secundárias com inicial maiúscula | mapeado dos cabeçalhos `#` e `##` |
| Tabelas e figuras | título acima, fonte abaixo, numeração sequencial e legenda com unidade quando aplicável | Tabela 1 implementada na seção 3.3 |
| Citações no texto | NBR 10520, sistema autor-ano | adotado; formas `(SOBRENOME, ano)` e `Sobrenome et al. (ano)` |
| Referências | NBR 6023, ordem alfabética pelo primeiro autor, DOI quando disponível | 13 entradas conferidas |
| Resumo e palavras-chave | resumo na língua do texto, após título; palavras-chave separadas por ponto e vírgula | adotado |
| Abstract e keywords | exigência e idioma dependem do periódico | `[A CONFIRMAR EXIGÊNCIA DO PERIÓDICO]` |
| Elementos pós-textuais | referências, declarações e apêndices de auditoria | adotado |

A parametrização acima não substitui a diagramação final em editor. Fonte, espaçamento exato, margens e paginação devem ser reaplicados após a confirmação das normas do periódico-alvo.

---
