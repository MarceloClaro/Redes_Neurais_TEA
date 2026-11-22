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
