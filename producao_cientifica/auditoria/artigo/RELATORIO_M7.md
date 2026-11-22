# Relatório M7 — Auditoria final e banca simulada

**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Marco:** M7 — auditoria final, após M0 a M6 entregues e aprovados
**Orquestrador:** marceloclaro
**Status:** rascunho para revisão humana; nenhuma aprovação editorial, nota ou Qualis é declarada
**Original preservado:** SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`
**Cópia auditada (estado pré-r1291):** SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`

**Extensão R1291:** em 2026-11-22 a cópia corrigida recebeu a aba documental `AUDITORIA_M7`, sem alterar modelos, fórmulas ou VBA. Hash atual: SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. O hash pré-r1291 citado nas auditorias abaixo identifica o estado nelas descrito. A cópia passou a ter 26 planilhas (25 originais mais a aba documental). A análise exploratória separada é diagnóstico do cache e não afirma desempenho do modelo corrigido.

## Resumo executivo

Sete auditorias finais foram executadas localmente: coerência interna, integridade da cadeia de evidências, força de alegação com contraprovas, bibliografia e ABNT, reprodutibilidade/proveniência/ética, apresentação ABNT e banca simulada. Cinco delegações a agentes especializados foram tentadas e falharam antes da execução — quatro por restrição regional do modelo OpenCode Go e uma por exigência de assinatura ativa. Nenhuma delas produziu artefato, e nenhuma é contabilizada como auditoria externa independente.

Não foram encontradas divergências internas entre pergunta, objetivos, métodos, resultados e conclusão. Permanecem pendências documentadas: causa da divergência do intervalo de confiança, anos de F11 e F12, exigência de abstract, parâmetros de diagramação do periódico, log do Solver, 30 imagens e seus dados de ética/proveniência, autoria, financiamento, conflitos e local de depósito. Três verbos de efeito não medido foram rebaixados para intenção de projeto; M5 e M6 foram regenerados e seus gates permanecem em 24/24 e 33/33.

A cadeia de gates foi reexecutada integralmente neste marco. O veredito é circunscrito à integridade documental e à reprodutibilidade da auditoria: não estabelece desempenho do modelo corrigido, validade diagnóstica, conformidade editorial ou aceite em periódico algum.

---

# Auditoria final 1 — Coerência interna

Nota metodológica: as cinco delegações de agentes especialistas tentadas neste marco falharam antes da execução (quatro por restrição regional do modelo OpenCode Go e uma por exigência de assinatura ativa). Nenhuma delas produziu artefato nem contou como revisão independente. Esta auditoria e as demais do marco M7 foram executadas localmente sob coordenação do orquestrador MarceloClaro, com o mesmo protocolo de evidência, sem alegar revisão externa.

| Item | Onde aparece | Expectativa fixada | Status | Evidência |
|---|---|---|---|---|
| Pergunta central | M5_01 §1.2; MANUSCRITO_ABNT §1.2 | Como falhas afetam a validade das métricas e quais controles detectam/reparam sem destruir o original | coerente | A pergunta é retomada literalmente na Conclusão, §5, primeiro parágrafo |
| Objetivo geral | M5_01 §1.2 | Propor e aplicar protocolo determinístico de auditoria e reparo | coerente | Os cinco objetivos específicos (i–v) são atendidos por M0–M4 e M6 |
| Proposições P1–P4 | SPEC, Escopo | Falhas detectáveis; reparo preserva estrutura; cache exige proveniência; recomendação de reporte | coerente | Tabela de métricas §3.3, §4.1 e Conclusão retomam cada proposição |
| Níveis N1–N5 | SPEC, Escopo | Inventário, reparo, recomputação, integridade, recomendação | coerente | Cada nível tem gate correspondente na cadeia 10/22/14/23/20/22/24/33 |
| Operações OP-01..OP-12 | M4_dados_analise; SPEC | Cálculos e verificações declarados | coerente | `recomputar_cache.py` e `M4_metricas_cache.json` registram comando, fórmulas e hash |
| Desenho do estudo | M5_02 §2 | Estudo de caso metodológico sobre artefato único, não validação diagnóstica | coerente | Nenhuma coorte, desfecho clínico ou amostra externa é reivindicada |
| Unidade de análise | M5_02; M4 | Cinco abas de RNA, 30 registros de teste por aba | coerente | `TP+TN+FP+FN=n`, 15 `TEA`/15 `NAO_TEA` por aba |
| Falhas detectadas | M5_03 §3.1–3.2; Resumo | Sinal em `K20`, rótulo `1 − EQM`, escala em `AG35/AH35`, p-code obsoleto | coerente | Quatro falhas aparecem no resumo, nos resultados e na conclusão de forma consistente |
| Reparo em cópia | M5_02 §2; M4 | Edição direta de OOXML/VBA; original preservado | coerente | Hashes distintos e inventário de 25/36/55/22/104 reaparecem em várias seções |
| Métricas do cache | M5_03 §3.3 | Valores 0,6333 a 0,9000, `n=30`, diagnóstico do estado original | coerente | Tabela 1 e Conclusão §5 usam a mesma faixa e a mesma proveniência |
| Divergência do IC | M5_03; M4_dados_analise | Cache reproduzido por Wilson; fórmula textual mais estreita; causa não resolvida | coerente | `[0,743786; 0,965401]` e `[0,758863; 0,950323]` aparecem com a mesma ressalva |
| Lacuna circunscrita | M5_01 §1.1; Resumo | "Não localizado nas buscas realizadas", nunca inexistência universal | coerente | §1.1 repete o mitigador em negrito; nenhuma seção o converte em negação absoluta |
| Conclusão | M5_05 §5 | Responde à pergunta sem introduzir dado novo | coerente | Conclusão cita apenas 10/22, faixa de métricas e a divergência do IC |
| Pendências | M5_07; Resumo | Solver, imagens, ética, autoria, financiamento, periódico | coerente | Mesmas pendências aparecem em Declarações e na Conclusão |
| Delimitações éticas | M5_07 §Ética | Sem alegação clínica; consentimento e anonimização pendentes | coerente | Nenhuma seção afirma validade diagnóstica ou desempenho pós-correção |
| Força de alegação | M5_00, M5_02, M6_03, M7_03 | Efeitos não medidos rebaixados para intenção de projeto | coerente | `impede`/`prevents` substituídos por `destina-se a evitar`/`is intended to prevent` |
| Scopo bibliográfico | M5_01 §1.1; M6_02 | 13 fontes incluídas, F14 fora do corpo, divergências F11/F12 registradas | coerente | Contagem e marcas `[A CONFIRMAR]` coincidem entre corpo, lista e apêndices |

## Divergências encontradas

Não foi encontrada divergência interna entre pergunta, objetivos, métodos, resultados e conclusão. Três pontos permanecem como **pendências documentadas**, não como incoerências:

1. **Intervalo de confiança.** Duas versões numéricas convivem no artefato. O texto não escolhe uma como correta; registra a origem de cada uma e a ausência de histórico de edição.
2. **Anos de F11 e F12.** O corpo mantém 2004 e 2002 respectivamente, com `[A CONFIRMAR]`, enquanto Crossref/DOI apontam 2003 e o DOI de F12 contém 1991. A decisão de preservar a marcação é consistente em todo o manuscrito.
3. **Abstract.** Permanece como exigência condicional do periódico; a forma provisória foi substituída por marcação explícita, sem afirmar que o abstract está dispensado.

Nenhuma dessas pendências foi resolvida por inferência para forçar harmonia superficial.

## Veredito circunscrito

A coerência interna é observada no estado atual do manuscrito e de seus módulos geradores. Isso não implica correção científica, conformidade com norma editorial externa ou aceite em periódico. A auditoria é heurística e humana, não substitui revisão por pares.

---

# Auditoria final 2 — Integridade da cadeia de evidências

Esta auditoria examina a cadeia entre artefato original, cópia corrigida, recomputação, gates e manuscrito. Ela avalia integridade documental, não validade diagnóstica nem mérito editorial.

| Item | Evidência | Situação | Limite |
|---|---|---|---|
| Original preservado | SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` | íntegro | hash registrado; conteúdo não reaberto para edição |
| Cópia corrigida (pré-r1291) | SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` | íntegro | distinta do original, como esperado |
| Cópia corrigida (atual, com `AUDITORIA_M7`) | SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb` | íntegro | extensão documental; modelos, fórmulas e VBA inalterados |
| Editoração do pacote | edição direta de OOXML e streams OLE/VBA; sem `openpyxl.save` | rastreável | não reproduzida fora do ambiente auditado |
| Inventário do ZIP (pré-r1291) | 25 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | preservado | contagens verificadas no gate da correção |
| Inventário do ZIP (atual) | 26 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | preservado | 25 originais mais `AUDITORIA_M7`; demais contagens inalteradas |
| Única remoção do ZIP | `xl/calcChain.xml` | rastreável | substituída por `fullCalcOnLoad="1"` |
| Força de recálculo | `fullCalcOnLoad="1"` nas cinco abas de RNA | observado | recálculo depende de abertura no Excel |
| Aviso de cache | `T157`: cache original não validado após `K20` | observado | não é resultado pós-correção |
| Sinal de ativação | `K20` corrigido nas cinco abas; `K21` já estava correto | verificado | ganho de desempenho não medido |
| Rótulo e escala | "Acurácia" explicada como `1 − EQM`; `AG35/AH35` sem divisão indevida por 100 | verificado | a correção do rótulo não altera número algum |
| Nomes e referências | resíduos de template e sete `#REF!` tratados | verificado | não implica ausência de outros erros latentes |
| VBA | `Módulo3` e `Módulo4` reescritos, `PerformanceCache` zerado | verificado | não executado neste ambiente |
| Recomputação do cache | `recomputar_cache.py`; JSON e tabela M4 com hash, comando e fórmulas | rastreável | valores anteriores à correção de `K20` |
| Matrizes e rótulos | `TP+TN+FP+FN=n`, 15/15 por aba, argmax 30/30 por aba | verificado | `n=30` por aba; intervalos largos |
| Divergência do IC | cache reproduzido por Wilson padrão; fórmula textual gera intervalo mais estreito | registrada | causa não resolvida; workbook não alterado |
| Cadeia de gates | 10/10, 22/22, 14/14, 23/23, 20/20, 22/22, 24/24, 33/33 | reexecutada | nenhuma contagem inferida de relatório anterior |
| Diagnóstico do ambiente | `doctor`: 16 passed, 6 warned, 0 failed com `.venv/bin/python` | observado | 6 avisos permanecem registrados |
| Critérios de aceitação | AC-1 a AC-14 na SPEC | completos | critérios são internos, não editoriais |
| Ciclos evolutivos | R1281 a R1289 registrados | rastreáveis | registro não equivale a revisão externa |
| Versionamento | `producao_cientifica/` segue no `.gitignore` do workspace de origem; publicação externa em `MarceloClaro/Redes_Neurais_TEA`, commit `374afb0`, sem o original por limite de 100 MiB | rastreável | configuração do workspace não alterada |
| Manuscritos | `MANUSCRITO_rascunho.md` (M5) e `MANUSCRITO_ABNT.md` (M6) gerados por scripts | distintos e rastreáveis | geradores não incluem data/hora |

## Divergências que permanecem em aberto

1. **Intervalo de confiança.** O valor em cache e a fórmula textual das células não coincidem. Não há histórico de edição no artefato que permita escolher a versão correta.
2. **Ano de F11.** O corpo e o rascunho M5 registram 2004; Crossref e DOI indicam 2003. A divergência foi mantida sem alteração silenciosa.
3. **Ano de F12.** O DOI contém 1991, OpenAlex registrou 2002 e Crossref não informou ano. A marcação `[A CONFIRMAR]` permanece.

Nenhuma dessas divergências foi convertida em escolha editorial dentro do artigo.

## Veredito circunscrito

A cadeia de evidências é íntegra no que pode ser verificado por hashes, contagens, comandos e gates reexecutados. Isso **não** estabelece que o modelo corrigido tenha desempenho validado, que as imagens sejam eticamente aptas ou que o manuscrito será aceito em qualquer periódico. A auditoria é documental e depende de revisão humana final.

---

# Auditoria final 3 — Força de alegação e contraprovas

A escada de força adotada é: **E0** delimitação; **E1** fato observado no artefato; **E2** valor recomputado com método declarado; **E3** inferência metodológica circunscrita; **E4** recomendação ou salvaguarda de projeto; **E5** alegação não sustentada e, portanto, mantida fora do texto. A classificação abaixo é revisão humana; não é resultado de modelo nem prova de ausência de excesso.

| Alegação examinada | Classe | Âncora | Contraprova que a derrubaria | Situação |
|---|---|---|---|---|
| `K20` usava `MAX(0.1*z,z)` e passou a `MAX(-0.1*z,z)` nas cinco abas | E1 | gate da correção, OP-04 | uma aba com sinal divergente ou hash idêntico ao original | mantida |
| Célula rotulada "Acurácia" continha `1 − EQM` | E1 | `R16` e `S16` | fórmula diferente no XML | mantida |
| 25 planilhas originais, 36 gráficos, 55 desenhos, 22 mídias e 104 tabelas foram preservados no estado pré-r1291 | E1 | inventário do ZIP | contagem divergente na cópia | mantida |
| 26 planilhas no estado atual, sem alterar gráficos, desenhos, mídias ou tabelas | E1 | aba documental R1291 | aba adicional poderia ser lida como alteração de modelo | mantida com rótulo explícito |
| Única parte removida foi `xl/calcChain.xml` | E1 | comparação de pacotes | qualquer outra remoção ou adição | mantida |
| Métricas em cache variam de 0,6333 a 0,9000 | E2 | `M4_metricas_cache.json` | divergência acima de `1e-12` na recomputação | mantida como diagnóstico do estado original |
| Argmax de `O:Q` coincidiu com `R145:R174` em 30/30 registros por aba | E2 | gate M4 G-07 | um único registro divergente | mantida |
| Valor de IC em cache foi reproduzido por Wilson padrão | E2 | `[0,743786; 0,965401]` | reprodução numérica diferente | mantida |
| Fórmula textual gera intervalo mais estreito | E2 | `[0,758863; 0,950323]` | avaliação literal diferente | mantida, sem escolha de versão correta |
| Falhas de implementação comprometem a validade das métricas reportadas | E3 | assimetria de sinal, rótulo e escala | evidência de que rótulo e sinal não afetam interpretação | mantida como inferência metodológica, não clínica |
| Reparo por edição direta preserva a estrutura do artefato | E1/E3 | 22/22 e inventário | perda de parte do pacote | mantida |
| Rotulagem de proveniência evita leitura de cache como resultado validado | E4 | `T157`, `fullCalcOnLoad`, JSON M4 | evidência de leitura humana equivocada | rebaixada de efeito comprovado para intenção de projeto |
| Lacuna não foi localizada nas buscas realizadas | E0/E3 | protocolo M2, quatro vias públicas | estudo anterior localizado no mesmo escopo | mantida como ausência circunscrita |
| Nenhum desempenho do modelo corrigido é afirmado | E0 | Solver não reexecutado; imagens não integradas | log de reexecução com pesos finais | mantida |
| Nenhuma validade diagnóstica é estabelecida | E0 | ausência de referência-padrão e amostra externa | referência-padrão confirmada e validação externa | mantida |
| Recomenda-se hash, comando, fórmula e log de otimização em todo artefato | E4 | seção 4.1 | não aplicável; recomendação normativa | mantida como recomendação |

## Ajuste executado nesta auditoria

Os trechos "a rotulagem de proveniência impede que cache seja lido como resultado validado", "provenance labeling prevents cached values..." e "Esses mecanismos impedem que a abertura do arquivo preserve..." foram rebaixados para "destina-se a evitar" e "is intended to prevent". A mudança não altera dado, número, citação ou conclusão; apenas remove alegação de efeito não medido. Os geradores M5 e M6 foram reexecutados e seus gates permanecem em 24/24 e 33/33.

## Alegações deliberadamente mantidas fora do texto

- "acurácia validada do modelo corrigido";
- "desempenho diagnóstico comprovado";
- "primeiro protocolo de auditoria de planilhas";
- "Qualis A1", "nota 10" ou "aceite garantido";
- "inexistência universal de estudo semelhante";
- "conformidade com TRIPOD+AI, PROBAST, STARD, CONSORT-AI ou PRISMA".

## Limite da auditoria

A ausência de alegação acima da evidência foi verificada por contraprovas formuladas nesta seção, não por consenso de revisores. A banca simulada complementa o exercício, mas não substitui avaliação externa real.

---

# Auditoria final 4 — Bibliografia, citações e ABNT

Nota metodológica: a delegação a agente especializado falhou antes da execução por restrição regional do modelo OpenCode Go. Não houve auditoria bibliográfica externa; o trabalho abaixo foi executado localmente a partir da evidência já coletada nos marcos M2, M5 e M6. Nenhuma fonte foi relida na íntegra neste marco e nenhum DOI foi acrescentado.

| Fonte | Veredito | Evidência |
|---|---|---|
| F01 Collins et al., 2024 — TRIPOD+AI | citada e listada; DOI verificado no Crossref | `10.1136/bmj-2023-078378`; BMJ, v. 385, p. e078378; forma no corpo `(COLLINS et al., 2024)` |
| F02 Collins et al., 2015 — TRIPOD | citada e listada; DOI verificado no Crossref | `10.1186/s12916-014-0241-z`; BMC Medicine, v. 13, n. 1, p. 1; `(COLLINS et al., 2015)` |
| F03 Wolff et al., 2019 — PROBAST | citada e listada; DOI verificado no Crossref | `10.7326/M18-1376`; Annals of Internal Medicine, v. 170, n. 1, p. 51-58; `(WOLFF et al., 2019)` |
| F04 De Kanter et al., 2026 — aderência TRIPOD+AI | citada e listada; DOI verificado no Crossref | `10.1016/j.jclinepi.2025.112118`; Journal of Clinical Epidemiology, v. 191, p. 112118; `(DE KANTER et al., 2026)` |
| F05 Renard et al., 2020 — variabilidade em segmentação | citada e listada; DOI verificado no Crossref | `10.1038/s41598-020-69920-0`; Scientific Reports, v. 10, n. 1; página/número do artigo com `[A CONFIRMAR]`; `Renard et al. (2020)` |
| F06 Chen et al., 2022 — reprodutibilidade | citada e listada; DOI verificado no Crossref | `10.1145/3510003.3510163`; ICSE 2022, p. 2202-2214; local e editora com `[A CONFIRMAR]`; `Chen et al. (2022)` |
| F07 Amalfitano et al., 2016 — EXACT | citada e listada; DOI verificado no Crossref | `10.1002/smr.1787`; Journal of Software: Evolution and Process, v. 28, n. 6, p. 483-505; `(AMALFITANO et al., 2016)` |
| F08 Panko, 2008 — taxonomia | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.0809.3613`; arXiv, 2008; versão do preprint com `[A CONFIRMAR]`; `(PANKO, 2008)` |
| F09 AlTarawneh e Thorne, 2017 | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.1703.09785`; arXiv, 2017; versão com `[A CONFIRMAR]`; `AlTarawneh e Thorne (2017)` |
| F10 Bishop e McDaid, 2008 | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.0802.3479`; arXiv, 2008; versão com `[A CONFIRMAR]`; `(BISHOP; MCDAID, 2008)` |
| F11 Ahmad et al. — sistema de tipos | citada e listada; DOI verificado no Crossref | `10.1109/ASE.2003.1240305`; ASE 2003, p. 174-183; ano 2004 mantido no corpo com `[A CONFIRMAR]`, DOI/Crossref indicam 2003; `Ahmad et al. (2004)` |
| F12 Antonini — simulação de RNA em planilha | citada e listada; DOI verificado no Crossref | `10.1109/IJCNN.1991.155504`; IJCNN-91, v. II, p. 910; ano 2002 mantido com `[A CONFIRMAR]`, DOI contém 1991, Crossref sem ano; `(ANTONINI, 2002)` |
| F13 Sabouri et al., 2026 — auditoria de agentes | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.2604.20070`; arXiv, 2026; versão com `[A CONFIRMAR]`; `(SABOURI et al., 2026)` |

## Correspondência citação ↔ referência

Foram contadas **13 fontes citadas no corpo** e **13 entradas na lista de referências**. Não foi detectada fonte citada sem entrada, nem entrada sem citação no corpo. O DOI `10.1145/3678890.3678909` (F14), embora identificada na busca, permanece fora do corpo e fora da lista, conforme decisão registrada no marco M5. As duas formas de citação autor-ano previstas pela NBR 10520 — `(SOBRENOME, ano)` e `Sobrenome et al. (ano)` — ocorrem no manuscrito e foram ambas aceitas pelo gate M6.

## Divergências de ano

- **F11 (Ahmad).** O corpo e o rascunho M5 registram 2004; o DOI contém `2003` e o Crossref não trouxe ano divergente que sustente 2004. A marcação `[A CONFIRMAR ANO; CROSSREF E DOI INDICAM 2003]` foi mantida na lista. Não houve alteração silenciosa do ano citado no corpo, porque a fonte primária não foi lida na íntegra.
- **F12 (Antonini).** O DOI contém `1991`, o Crossref não informou ano e o OpenAlex registrou `2002`. A marcação `[A CONFIRMAR ANO; DOI CONTÉM 1991; CROSSREF NÃO INFORMA ANO]` foi mantida. A escolha de 2002 no corpo é provisória e explícita.

Em ambos os casos, a decisão foi preservar a divergência e sinalizá-la, não resolver por semelhança de metadados.

## Conformidade ABNT observada

A conferência cobriu a NBR 6023 (referências alfabéticas pelo primeiro autor, com DOI quando disponível) e a NBR 10520 (citações no sistema autor-ano). A NBR 14724 depende de diagramação final e foi registrada nas notas do apêndice C. Foram observadas 13 entradas com DOI, ordem alfabética e ausência de DOI inventado. A pendência de versão dos quatro preprints e de páginas de F05 impede declarar conformidade completa de metadados. Papel, margens, fonte, espaçamento e paginação permanecem `[A CONFIRMAR PELO PERIÓDICO]`.

## Limites

O texto integral das fontes F01–F13 ainda não foi conferido; a auditoria apoiou-se em resumos, metadados de APIs públicas e auditoria por DOI. A triagem não foi cega e não houve revisão bibliográfica externa independente. Nenhuma promessa editorial, Qualis, nota ou aceite é feita.

---

# Auditoria final 5 — Reprodutibilidade, proveniência e ética

Nota metodológica: a delegação a agente especializado falhou antes da execução por restrição regional do modelo OpenCode Go. Não houve auditoria externa; o trabalho abaixo foi executado localmente. Declara-se reprodutibilidade da **auditoria**, jamais do treino da RNA ou do desempenho do modelo corrigido.

| Item | Evidência | Status | Limite |
|---|---|---|---|
| Hash do original | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` | rastreável | confirma identidade, não integridade semântica de todo conteúdo |
| Hash da cópia (pré-r1291) | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` | rastreável | distinta do original, como esperado |
| Hash da cópia (atual) | `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb` | rastreável | aba `AUDITORIA_M7` inserida; modelos e fórmulas inalterados |
| Preservação do original | gate `verificar_auditoria.py` 10/10 | rastreável | original não reeditado neste marco |
| Edição do pacote | OOXML e streams OLE/VBA diretos; sem `openpyxl.save` | rastreável | executada neste ambiente, não documentada em outro sistema |
| Inventário estrutural (pré-r1291) | 25 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | rastreável | contagens do gate da correção |
| Inventário estrutural (atual) | 26 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | rastreável | 25 originais mais a aba documental |
| `xl/calcChain.xml` | única parte removida do ZIP | rastreável | remoção intencional, registrada |
| `fullCalcOnLoad="1"` | presente nas cinco abas de RNA | rastreável | depende de abertura no Excel para ter efeito |
| VBA e p-code | `Módulo3` e `Módulo4` reescritos; `PerformanceCache` zerado | rastreável | macros não executadas neste ambiente |
| Comandos de verificação | nove gates reexecutados, de 10/10 a 33/33 | rastreável | contagens sempre reexecutadas, nunca inferidas de relatório anterior |
| Ambiente Python | `.venv/bin/python`; `doctor` 16 passed, 6 warned, 0 failed | rastreável | seis avisos permanecem; `python3` do sistema falha por falta de `whoosh` |
| Saída JSON M4 | `M4_metricas_cache.json` com comando, fórmulas e hash | rastreável | descreve recomputação, não treino |
| Tabela de métricas | `M5_03_resultados.md` e Tabela 1 do MANUSCRITO_ABNT | rastreável | valores são diagnóstico do cache pré-correção |
| Cache versus resultado validado | aviso em `T157` e regra de comunicação no §4.1 | rastreável | nenhum número pós-correção é apresentado |
| Solver | não reexecutado; versão, data, status, seed e pesos finais ausentes | pendente | depende de log a enviar pelo usuário |
| 30 imagens | não integradas; ausentes proveniência, licença e referência-padrão | pendente | nenhuma análise de imagem realizada neste marco |
| Consentimento e anonimização | marcados `[A CONFIRMAR]` em `M5_07_declaracoes.md` | pendente | sem esses dados, não há deliberação ética possível |
| Financiamento | `[A CONFIRMAR]` | pendente | não declarar ausência sem confirmação |
| Conflitos de interesse | `[A CONFIRMAR]` | pendente | não declarar ausência sem confirmação |
| Autoria e contribuições | `[A CONFIRMAR]` | pendente | nomes e afiliações não fornecidos |
| Uso de IA | declarado em `M5_07_declaracoes.md` | rastreável | revisão humana final não registrada como concluída |
| Deposição de dados/código | `producao_cientifica/` no `.gitignore`; nada commitado | parcial | local público, licença e condições de acesso `[A CONFIRMAR]` |
| Periódico-alvo | `[A CONFIRMAR]` | pendente | determine exigência de abstract, normas de diagramação e prazo |
| Geradores determinísticos | `montar_m5.py` e `montar_m6.py` sem data/hora | rastreável | M7 seguirá o mesmo padrão |

## O que é reproduzível

São reproduzíveis neste ambiente: a inspeção do original e da cópia por hashes e contagens; os nove gates de verificação; a recomputação das métricas a partir do cache por `recomputar_cache.py`; a avaliação numérica das duas versões do intervalo de confiança; e a regeneração determinística do rascunho IMRAD e da versão ABNT a partir dos módulos-fonte. Comandos, saídas e marcos estão registrados na SPEC e nos apêndices.

## O que não é reproduzível neste ambiente

Não são reproduzíveis: o treino da RNA pelo Solver, porque não houve reexecução nem log com versão, data, status, seed e pesos finais; o desempenho do modelo corrigido, porque a correção de `K20` não foi seguida de otimização; a análise das 30 imagens, porque não foram fornecidas nem acompanhadas de proveniência e consentimento; e a conferência do texto integral das fontes, porque apenas metadados e resumos foram consultados. A edição da fórmula textual do IC depende de autorização explícita e não foi executada.

## Recomendações antes de submissão

1. Enviar e arquivar o log do Solver com versão do Excel/Solver, data, status de convergência, seed, arquivo salvo e hash dos pesos finais; separar esse artefato do cache original.
2. Fornecer proveniência das 30 imagens, natureza dos dados, consentimento, anonimização, licença de uso e referência-padrão antes de qualquer incorporação.
3. Decidir, com registro de versão, se a fórmula textual do IC será editada; essa é a Onda 3 e exige autorização explícita.
4. Confirmar periódico-alvo, autoria, financiamento, conflitos, instituição e local de depósito de dados/código.
5. Registrar revisão humana final e aplicar diagramação ABNT no editor, com paginação, margens e fonte confirmadas.
6. Publicar ou disponibilizar os scripts e as saídas com licença declarada, mantendo o original preservado.

Esta auditoria documenta rastreabilidade e limites; não substitui revisão humana nem estabelece reprodutibilidade completa do estudo.

---

# Auditoria final 6 — Apresentação ABNT

Nota metodológica: a delegação a agente especializado falhou antes da execução por restrição regional do modelo OpenCode Go. A conferência abaixo foi feita localmente sobre o arquivo Markdown gerado no M6 e sobre as notas do apêndice C. É auditoria de documento, não aceite editorial.

| Critério | Norma | Evidência no manuscrito | Status | Ação recomendada |
|---|---|---|---|---|
| Título | NBR 14724 | "Auditoria metodológica de um pipeline de rede neural artificial em planilha eletrônica" no cabeçalho | observado | Manter; conferir forma exigida pelo periódico |
| Resumo | NBR 14724 | `# Resumo` na abertura, com objetivo, métodos, resultados e limites | observado | Conferir extensão máxima exigida pelo periódico |
| Palavras-chave | NBR 14724 | Presentes no módulo do resumo, separadas por ponto e vírgula | observado | Confirmar quantidade e idioma exigidos |
| Abstract | NBR 14724 / periódico | Marcação `[A CONFIRMAR EXIGÊNCIA DE ABSTRACT PELO PERIÓDICO]` | pendente | Incluir, traduzir ou dispensar conforme norma do periódico |
| Sequência IMRAD | NBR 14724 | Introdução, Materiais e métodos, Resultados, Discussão, Conclusão, na ordem | observado | Manter a ordem na conversão final |
| Numeração de seções | NBR 14724 | Seções primárias `1` a `5` em algarismos arábicos | observado | Aplicar maiúsculas na diagramação final |
| Tabelas | NBR 14724 | Tabela 1 com título acima e fonte abaixo | observado | Reaplicar espaçamento simples e numeração sequencial na conversão |
| Figuras | NBR 14724 | Nenhuma figura inserida; 30 imagens permanecem pendentes | pendente | Se integradas, exigir legenda, fonte e proveniência |
| Citações no texto | NBR 10520 | Sistema autor-ano nas formas `(SOBRENOME, ano)` e `Sobrenome et al. (ano)` | observado | Padronizar a forma adotada pelo periódico se houver preferência |
| Referências | NBR 6023 | 13 entradas alfabéticas, com DOI; onze campos confirmados em fonte primária ou suplementar | parcial | Resolver pendências de versão de preprint, páginas de F05 e anos de F11/F12 |
| Apêndices | NBR 14724 | Apêndices A, B e C após as Declarações | observado | Confirmar se o periódico aceita apêndices de auditoria |
| Paginação | NBR 14724 | algarismos arábicos, canto superior direito; primeira página sem número | pendente | Parâmetro registrado como `[A CONFIRMAR PELO PERIÓDICO]` |
| Margens | NBR 14724 | superior e esquerda 3 cm; inferior e direita 2 cm | pendente | Confirmar antes da diagramação; periódicos costumam impor outro padrão |
| Fonte e corpo | NBR 14724 | Times New Roman ou Arial, 12 pt | pendente | Confirmar com o periódico |
| Espaçamento | NBR 14724 | 1,5 entre linhas; simples em referências, notas, citações longas e legendas | parcial | Mapeado nas notas; aplicar no editor |
| Alinhamento e recuo | NBR 14724 | justificado; citações longas com recuo de 4 cm | parcial | Mapeado nas notas; aplicar no editor |

## Ajustes obrigatórios antes da conversão

1. Substituir a marcação de abstract pela decisão do periódico.
2. Resolver, com confirmação de fonte, as pendências de metadados de F05, F08, F09, F10, F11, F12 e F13, sem preencher por inferência.
3. Aplicar paginação, margens, fonte, espaçamento e alinhamento no editor final; o Markdown não carrega esses atributos por si.
4. Registrar revisão humana final e declará-la nas Declarações, que hoje informam que ela ainda não foi concluída.

## Ajustes condicionais ao periódico

- Incluir ou suprimir abstract e keywords em inglês.
- Aceitar ou recusar apêndices de auditoria.
- Adotar normas de citação e referências próprias, se divergentes da ABNT.
- Definir local de depósito, licença e forma de disponibilidade de dados e código.
- Confirmar autoria, instituição, financiamento, conflitos e correspondência.

## Veredito circunscrito

O documento apresenta coerência estrutural com as NBRs 14724, 6023 e 10520 no que pode ser avaliado em Markdown, restando pendências editoriais e de metadados explicitamente marcadas. Trata-se de auditoria de documento, não de aceite editorial, nota, Qualis ou aprovação por periódico.

---

# Banca simulada — perguntas e respostas ancoradas

Esta é uma **simulação heurística** de arguição, conduzida localmente pelo orquestrador após a falha das delegações de agentes revisores. As delegações falharam antes da execução (restrição regional do modelo OpenCode Go e exigência de assinatura ativa), de modo que não houve revisores externos reais. As perguntas são difíceis e respondíveis com o manuscrito; as respostas citam seções e declaram limites. Nenhuma avaliação aqui equivale a revisão por pares, nota, Qualis ou aceite.

## Revisor 1 — Metodologia

**P1. Por que o estudo é um caso metodológico e não uma validação da RNA?**
Resposta ancorada: §1.3 e §2 declaram contribuição metodológica e desenho de caso único sobre artefato computacional. O §5 reforça que não há validade diagnóstica. Limite: não há coorte, desfecho clínico, referência-padrão nem amostra externa.

**P2. Como você sustenta que as falhas detectadas afetam a validade das métricas sem medir desempenho depois do reparo?**
Resposta ancorada: §3.1–3.2 mostram que o cálculo (`K20`), o rótulo (`1 − EQM` sob "Acurácia") e a escala (`AG35/AH35`) foram alterados no artefato; a inferência do §4.1 é metodológica, não clínica. Limite: o efeito no desempenho do modelo corrigido não foi medido porque o Solver não foi reexecutado.

**P3. Cinco abas com `n=30` cada são amostra suficiente para generalizar?**
Resposta ancorada: o §2 define cinco abas como unidades de análise de um único workbook; o §3.3 reporta `n=30` por aba. Limite: não se generaliza a outras planilhas, modelos ou populações; a contribuição é a taxonomia de falhas e o gate, não uma estimativa de desempenho.

**P4. A correção de `K20` não invalida os valores de métricas que você reporta?**
Resposta ancorada: o §3.3 e a Tabela 1 rotulam explicitamente os valores como diagnóstico do cache pré-correção; a declaração em `T157` e a regra do §4.1 separam cache de resultado validado. Limite: são números do estado original, não do modelo corrigido.

**P5. Por que a divergência do intervalo de confiança não foi resolvida?**
Resposta ancorada: o §3.3 registra que a forma padrão de Wilson reproduz o valor em cache `[0,743786; 0,965401]`, enquanto a avaliação literal da fórmula textual produz `[0,758863; 0,950323]`; o §4.1 e a Conclusão mantêm a causa como não resolvida. Limite: não há histórico de edição que permita escolher a versão correta; a Onda 3 exige autorização explícita.

**P6. Os controles determinísticos são uma contribuição ou apenas uma lista de checagens?**
Resposta ancorada: o §2 e o Apêndice A documentam nove gates encadeados de 10/10 a 33/33, com hashes e comandos; a Conclusão os apresenta como gate reproduzível e protocolo de reparo não destrutivo. Limite: são critérios internos de auditoria, não diretriz externa validada.

**P7. A lacuna foi demonstrada?**
Resposta ancorada: o §1.1 registra quatro vias públicas em 21/11/2026 e afirma que não localizou trabalho com a combinação descrita, com o mitigador em negrito. Limite: é ausência circunscrita às buscas realizadas, não prova de inexistência universal; o texto integral das fontes não foi conferido.

## Revisor 2 — Reprodutibilidade e estatística

**P1. O que exatamente é reproduzível no seu trabalho?**
Resposta ancorada: o Apêndice de reprodutibilidade (M7_05) e o §2 registram hashes, nove gates reexecutados, `recomputar_cache.py`, JSON M4 e geradores determinísticos. Limite: reproduz-se a auditoria, não o treino da RNA nem o desempenho pós-correção.

**P2. Por que o `doctor` do sistema falha e isso não invalida os gates?**
Resposta ancorada: M7_05 registra que `python3 -m marceloclaro.cli doctor` falha por falta de `whoosh`, enquanto `.venv/bin/python -m marceloclaro.cli doctor` resulta em 16 passed, 6 warned, 0 failed. Limite: os seis avisos permanecem documentados e não foram convertidos em silêncio.

**P3. A recomputação das métricas depende de serviço externo?**
Resposta ancorada: §2 e M7_05 afirmam que comandos, hashes e gates são reproduzíveis sem dependência de serviços externos; os dados vêm do cache do workbook e de scripts locais. Limite: a auditoria de referências usou APIs públicas, registradas nos apêndices.

**P4. Por que `1 − EQM` não pode ser tratado como acurácia?**
Resposta ancorada: o §3.2 mostra `R16` como EQM médio e `S16=SUM(-R16,1)`; o resumo e a Conclusão registram o rótulo indevido. Limite: o texto não reclassifica os números nem propõe nova métrica validada.

**P5. Há controle de erro nas contagens de TP, TN, FP e FN?**
Resposta ancorada: o §3.3 registra `TP+TN+FP+FN=n`, `TP+FN=15`, `TN+FP=15` e argmax 30/30 por aba. Limite: `n=30` por aba; intervalos largos são discutidos como limitação no §4.1.

**P6. Por que você não reexecutou o Solver para obter o número corrigido?**
Resposta ancorada: M7_05 e a Conclusão registram que o log com versão, data, status, seed e pesos finais não foi enviado e que nenhum resultado pós-correção é afirmado. Limite: a reexecução depende do usuário e de ambiente com Solver.

**P7. O que impede o leitor de confundir o cache com resultado validado?**
Resposta ancorada: a redação foi rebaixada no M7_03 de "impede" para "destina-se a evitar"; o aviso em `T157`, a Tabela 1 rotulada e a regra do §4.1 são os mecanismos documentados. Limite: trata-se de intenção de projeto e rotulagem, não de efeito medido sobre leitores.

## Revisor 3 — Bibliografia e ABNT

**P1. Quantas fontes foram efetivamente verificadas na fonte primária?**
Resposta ancorada: o Apêndice A (M6_02) registra nove DOIs verificados no Crossref e quatro preprints com metadados conferidos em OpenAlex. Limite: o texto integral das 13 fontes não foi lido.

**P2. Como você justifica citar F11 com ano divergente do DOI?**
Resposta ancorada: o Apêndice A e o M7_04 registram 2004 no corpo e `[A CONFIRMAR ANO; CROSSREF E DOI INDICAM 2003]` na lista, sem alteração silenciosa. Limite: a resolução depende de conferência da fonte primária.

**P3. E F12?**
Resposta ancorada: o DOI contém `1991`, o Crossref não informou ano e o OpenAlex registrou `2002`; o corpo mantém 2002 com `[A CONFIRMAR]`. Limite: não houve escolha definitiva.

**P4. Há referência citada sem entrada ou entrada sem citação?**
Resposta ancorada: o M7_04 contou 13 fontes citadas e 13 entradas, sem Correspondência quebrada; F14 permanece fora do corpo e da lista. Limite: a contagem foi feita por varredura determinística e revisão local, não por revisor externo.

**P5. A conformidade ABNT está fechada?**
Resposta ancorada: o Apêndice C e o M7_06 cobrem NBR 14724, 6023 e 10520 no que o Markdown permite, com tabela titulada e fonte. Limite: papel, margens, fonte, espaçamento, paginação e exigência de abstract dependem do periódico e estão marcados como pendentes.

**P6. Por que não converter para DOCX ou PDF agora?**
Resposta ancorada: as notas ABNT registram que a parametrização depende de editor e do periódico-alvo. Limite: converter antes da confirmação geraria artefato com metadados presumidos; a conversão não foi executada neste marco.

**P7. O manuscrito promete Qualis, nota ou aceite?**
Resposta ancorada: o cabeçalho e o M7_06 afirmam explicitamente que nenhuma aprovação editorial, nota ou Qualis é declarada. Limite: a ausência de promessa não é garantia de avaliação favorável.

## Perguntas sem resposta satisfatória no estado atual

1. Qual é o desempenho do modelo após a correção de `K20`? Depende do log do Solver com versão, data, status, seed, arquivo salvo e hash dos pesos finais.
2. As 30 imagens podem ser integradas? Dependem de proveniência, natureza dos dados, consentimento, anonimização, licença e referência-padrão.
3. Qual versão do intervalo de confiança está correta? Depende de histórico de edição e de autorização explícita para a Onda 3.
4. Qual é o ano correto de F11 e de F12? Depende de conferência do texto integral das fontes primárias.
5. Quais são periódico-alvo, autoria, financiamento, conflitos, instituição, prazo e local de depósito? Todos permanecem `[A CONFIRMAR]`.
6. Exige-se abstract, e quais são as normas exatas de diagramação do periódico? Depende da confirmação editorial.
7. Houve revisão humana final? As Declarações informam que ainda não foi registrada como concluída.

Nenhuma dessas lacunas foi preenchida por suposição nesta simulação.

---

---

## Veredito final circunscrito

O marco M7 consolida sete auditorias locais e uma banca simulada. As auditorias documentam integridade de hashes, comandos, gates, citações e formatação no estado atual do manuscrito, com pendências explicitamente marcadas. Não há revisão externa real, não houve reexecução do Solver, não houve integração das 30 imagens e não foi declarada qualquer aprovação editorial, Qualis, nota, aceite ou validade clínica. A entrega permanece sujeita a revisão humana e a confirmações dependentes do usuário e do periódico-alvo.
