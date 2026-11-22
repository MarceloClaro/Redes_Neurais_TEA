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
