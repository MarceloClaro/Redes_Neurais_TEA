# 5 Conclusão

A pergunta central pode ser respondida nos limites do artefato analisado. Falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas porque alteram o cálculo, o rótulo ou a proveniência do número. Controles determinísticos baseados em inspeção de OOXML e de streams VBA detectam essas falhas, e o reparo por edição direta do pacote preserva gráficos, desenhos, mídia e tabelas. No caso estudado, o original passou por 10 verificações, a cópia por 22, e a única parte removida foi `xl/calcChain.xml`.

A auditoria também mostrou que um bloco de métricas pode ser internamente coerente e ainda assim não representar o modelo corrigido. Valores entre 0,6333 e 0,9000, com `n=30`, descrevem o cache original. A divergência entre o intervalo em cache e a fórmula textual reforça a necessidade de inspecionar a fórmula, não apenas o número. Isso não estabelece validade diagnóstica nem desempenho clínico.

As contribuições são uma taxonomia aplicada de falhas, um gate reproduzível, um protocolo de reparo não destrutivo e uma regra de comunicação que separa cache diagnóstico de resultado validado. Como trabalho futuro, a integração do log do Solver e das 30 imagens deverá seguir o protocolo de proveniência já registrado; qualquer edição adicional da fórmula de intervalo dependerá de autorização explícita e histórico de versões.
