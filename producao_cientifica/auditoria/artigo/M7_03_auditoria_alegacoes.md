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
