# M4 — Dados, análise e resultados (parte executável)

**Artefato:** rascunho para aprovação
**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Data:** 22 de novembro de 2026
**Script:** `recomputar_cache.py` · **Saídas:** `M4_metricas_cache.json`, `M4_tabela_metricas.md`

## 1. Estado deste marco

Esta é a **parte executável agora**. O workbook foi lido sem abrir no Excel, sem reexecutar Solver e sem alterar o `.xlsm`. Os valores abaixo são, por definição, **diagnóstico do estado original** — cache gerado antes da correção de `K20`.

A parcela dependente do usuário (log do Solver e 30 imagens) está especificada na seção 6 e **ainda não foi integrada**. Nenhum resultado pós-correção é afirmado neste documento.

## 2. Proveniência

| Campo | Valor |
|---|---|
| Arquivo analisado | `auditoria/Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` |
| SHA-256 | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` |
| Original preservado | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` |
| Comando | `.venv/bin/python producao_cientifica/auditoria/artigo/recomputar_cache.py` |
| Ambiente | Python 3 da `.venv`; `zipfile` + `xml.etree`; sem `openpyxl.save` |
| Tolerância numérica | `1e-12` |
| Classificação | Diagnóstico do estado original; Solver não reexecutado neste ambiente |

## 3. Resultados recomputados

| Aba | n | TP | TN | FP | FN | Acurácia | Sens. | Esp. | EQM (R16) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `n120\|n40\|n116\|n86` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n116\|n50` | 30 | 9 | 13 | 2 | 6 | 0,7333 | 0,6000 | 0,8667 | 0,235776 |
| `n119\|n72\|n1\|n73` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n119\|n72` | 30 | 12 | 12 | 3 | 3 | 0,8000 | 0,8000 | 0,8000 | 0,180387 |
| `n19\|n99\|n120\|n40\|` | 30 | 14 | 13 | 2 | 1 | 0,9000 | 0,9333 | 0,8667 | 0,197131 |

Verificações executadas nas 5 abas:

- `TP + TN + FP + FN = n` em todas.
- `TP + FN = 15` e `TN + FP = 15`, correspondendo a 15 `TEA` e 15 `NAO_TEA`.
- Acurácia em cache `(TP+TN)/n` coincide com a recomputação nas 5 abas.
- Sensibilidade, especificidade, VPP e VPN em cache coincidem com as recomputações.
- A classe prevista em `R145:R174` coincide com o argmax dos três logits em `O:Q` em **30/30 registros por aba**. Nenhum argmax recaiu na terceira posição, cuja célula `C13` está vazia.
- Maior valor em cache: **0,9000** na aba `n19|n99|n120|n40|`.

Isso confirma que o bloco de métricas de teste é **internamente coerente com o próprio cache**. Isso não implica que o cache seja correto em relação ao modelo corrigido.

## 4. Achado novo: divergência entre valor em cache e fórmula textual do IC

Ao recomputar os intervalos de confiança, o valor armazenado em `T155/T156` foi reproduzido **exatamente** pela forma padrão da fórmula de Wilson:

`(p + z²/(2n))/(1 + z²/n) ± z·√(p(1−p)/n + z²/(4n²))/(1 + z²/n)`, com `z = 1,96`.

Contudo, a fórmula **efetivamente escrita** nas células é:

`(... + 1.96^2/(4*$T$145^2))/$T$145` dentro da raiz — isto é, `√((p(1−p) + z²/(4n²))/n)`.

Avaliada literalmente, essa fórmula produz intervalos mais estreitos. Exemplo na aba de maior cache:

| Versão | Intervalo |
|---|---|
| Valor em cache / Wilson padrão | [0,743786; 0,965401] |
| Fórmula textual da célula | [0,758863; 0,950323] |

O mesmo padrão ocorre nas 5 abas. **Hipóteses não distinguidas neste marco:** (i) a fórmula foi editada sem recálculo; (ii) o cache provém de versão anterior da planilha. Não há histórico de edição no artefato que permita escolher entre elas. Não afirmo qual versão é "a correta" e **não alterei o workbook** — uma eventual Onda 3 exigiria autorização explícita.

Este achado reforça a tese central do artigo: a coerência interna de um número não garante sua validade, e a inspeção da fórmula textual é necessária mesmo quando o valor em cache parece plausível.

## 5. O que os números autorizam dizer

**Autorizado:**

- "No cache original, a aba X apresentou `(TP+TN)/n = 0,9000` com `n=30`."
- "A definição interna de 'Acurácia' na planilha de treino é `1 − EQM médio` (`S16 = SUM(-R16,1)`)."
- "A fórmula textual do IC difere daquela que reproduz o valor em cache."
- "As métricas de teste são internamente consistentes com o cache."

**Não autorizado:**

- "O modelo corrigido atinge 90% de acurácia."
- "O modelo é clinicamente válido para TEA."
- "A correção de `K20` melhorou o desempenho."
- "O intervalo [0,7438; 0,9654] é a incerteza do modelo reparado."

## 6. Protocolo para a evidência pendente do usuário

Você informou que vai executar o Solver e enviar as 30 imagens. Para que M4 possa integrá-las sem inventar metadados, envie:

### 6.1 Log do Solver

| Campo | Por que é necessário |
|---|---|
| Versão do Excel | Define motor de cálculo e funções disponíveis |
| Versão/identificação do Solver (ex.: frente-par, GRG nonlinear, evolutivo) | Define o algoritmo de otimização |
| Data e hora da execução | Proveniência temporal |
| Status de convergência / mensagem do Solver | Indica se houve solução, parada ou falha |
| Configuração de `seed` (use `seed=1` se o Solver permitir fixar) | Reprodutibilidade |
| Planilha executada e intervalo de células-alvo | Delimita o que foi otimizado |
| Valores finais dos pesos (`W19:Z19`, `AA19`, `AE19:AH25`, `AI19:AI25`) ou o workbook salvo após a execução | Permite conferir o novo forward pass |
| Arquivo salvo após a execução, com hash SHA-256 | Liga o resultado ao artefato |

### 6.2 Imagens de teste

| Campo | Por que é necessário |
|---|---|
| Identificador de cada imagem (30 arquivos) | Liga imagem à linha `145–174` |
| Arquivo ou caminho com hash SHA-256 | Proveniência e integridade |
| Origem da coleta (base, estudo, instituição) e licença/condição de uso | `[A CONFIRMAR]`; direito de uso e rastreabilidade |
| Natureza dos dados (humano/não humano; adulto/criança) | `[A CONFIRMAR]`; delimitação ética |
| Natureza do consentimento e do processo de anonimização | `[A CONFIRMAR]` desde M0 |
| referência-padrão / rótulo clínico e quem o atribuiu | `[A CONFIRMAR]`; necessário para qualquer afirmação diagnóstica |
| Confirmação de aprovação ética, se aplicável | `[A CONFIRMAR]`; condição para uso em M4 |
| Descritores extraídos (OpenFace/VGG19) e versão do extrator | Liga imagem às colunas `C:F`/`K:N` |

**Importante:** a seleção de atributos ocorreu antes da separação treino/teste no desenho original. Isso será registrado como risco de vazamento de dados (`data leakage`) na discussão, sem afirmar que houve vazamento efetivo sem evidência.

## 7. Critérios para integrar a evidência futura

1. O log e/ou workbook pós-Solver devem ter hash registrado.
2. Novas métricas só entram após a recomputação pelo mesmo script, com saída separada e rótulo "pós-correção".
3. Comparação cache ↔ pós-correção é apresentada como mudança de estado computacional, não como ganho clínico.
4. Imagens só entram com os campos da seção 6.2 preenchidos ou com pendência explícita mantida no texto.
5. Nenhum resultado de imagem será produzido neste ambiente sem os arquivos e a autorização.

## 8. Limites deste marco

- `n=30` por aba; intervalos largos que não autorizam generalização.
- Cache pré-correção não é resultado validado.
- Divergência da fórmula do IC detectada, mas sem resolução de causa.
- Texto integral das fontes F01–F12 ainda não conferido.
- Log do Solver, imagens, financiamento, conflitos, autoria, instituição e periódico: `[A CONFIRMAR]`.
- Nenhuma alteração ao workbook corrigido foi feita neste marco.
