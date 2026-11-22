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
