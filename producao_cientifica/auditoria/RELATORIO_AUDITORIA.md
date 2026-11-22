# Relatório de auditoria técnica e metodológica

**Artefato:** `producao_cientifica/Redes Neurais - TEA Dataset VBA.xlsm`
**SHA-256:** `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`
**Data:** 2026-11-21 · **Orquestrador:** marceloclaro · **Spec:** `SPEC-auditoria-rna-tea.md`
**Original não modificado.** Nenhum resultado aqui foi obtido reexecutando o Solver.

---

## 0. Resumo executivo

O workbook é um artefato de projeto de pesquisa (Psicologia, FPO/COA) que implementa cinco
MLPs de 4 neurônios ocultos no Solver do Excel, alimentadas por embeddings faciais
(VGG-19/OpenFace via Orange) do Autism Image Database. A estrutura é funcional e os dados
de treino estão balanceados (60 TEA / 60 não-TEA), mas **quatro defeitos impedem que os
números apresentados sejam interpretados como desempenho preditivo**:

1. A célula rotulada **"Acurácia" contém `1 − erro quadrático médio`**, não acurácia.
2. **Não existe nenhuma métrica agregada no conjunto de teste**, que além disso tem
   **30 imagens, não 60** como afirmam o texto e o resumo.
3. **Erro de sinal no Leaky ReLU da primeira linha** (`K20`) das cinco abas.
4. O **objetivo central do estudo — testar variação étnica latina com dados de Crateús-CE —
   não é executado no arquivo**: não há esses dados nem comparação populacional.

Há ainda um erro de sintaxe VBA (aspas tipográficas em `Módulo4`), resíduos de template,
referências `#REF!` e riscos de privacidade não documentados.

---

## 1. Achados críticos (P0)

### C1 — "Acurácia" é uma métrica inventada
**Evidência (5/5 abas de RNA):**
- `R16 = SUM(R20:R139)/120`, com `R20 = SUMXMY2(H20:J20,O20:Q20)` → erro quadrático médio
  entre one-hot e softmax.
- `S16 = SUM(-R16,1)` → `1 − EQM`, rotulado `Acurácia` em `S15`.
- `AG35 = R16/100` e `AH35 = S16/100` → nova divisão por 100 sem justificativa.

Valores em cache: erro entre `0,1804` e `0,2759`; "acurácia" entre `0,7241` e `0,8196`.
Ou seja, **o melhor resultado reportado no próprio arquivo é ~82% de "acurácia"**, distante
dos 96% citados no resumo como expectativa.

**Impacto:** `1 − perda` não é taxa de acertos; pode ser negativa se o erro > 1 e não tem
interpretação clínica. Invalidar qualquer frase do tipo "o modelo teve X% de precisão"
baseada em `S16`.

**Correção:** substituir por contagem de acertos com `argmax(softmax)`:
`=SUMPRODUCT(--(INDEX($C$11:$C$13,MATCH(MAX(O20:Q20),O20:Q20,0))=$G20))/120`.
Manter `R16` renomeado como `Erro quadratico medio (perda)`. Reportar separadamente
acurácia, sensibilidade, especificidade, VPP/VPN e IC 95% (Wilson).

### C2 — Teste sem métrica e divergência 60 × 30
**Evidência:** bloco de teste nas linhas 145–174 (30 registros, 15/15) em todas as abas;
colunas `S:AK` desse bloco vazias; `R145 = INDEX($C$11:$C$13,MATCH(MAX($O145:$Q145),...))`
classifica caso a caso, mas nada agrega. O `drawing15.xml` e a aba `EXPERIMENTOS | RESUMO`
afirmam "TESTES COM 60 IMAGENS" e "Números de Imagens Embbeding teste = 60".

**Impacto:** não há estimativa de generalização; a afirmação de 60 imagens não corresponde
ao arquivo. Onde estão as outras 30?

**Correção:** recuperar as 60 imagens ou corrigir o texto para 30. Acrescentar, abaixo do
bloco de teste: acurácia, matriz de confusão 2×2, sensibilidade, especificidade e intervalo
de confiança. Sem isso, o estudo é apenas um ajuste de pesos em amostra de treino.

### C3 — Leaky ReLU com sinal invertido em `K20` (5/5 abas)
**Evidência:**
- `K20 = MAX(0.1*z, z)` → para `z < 0`, devolve `0,1z` (negativo).
- `K21:K139 = MAX(-0.1*z, z)` → correto (devolve `−0,1z`, positivo).

**Impacto:** uma única linha de treino é processada por um neurônio com comportamento
diferente dos demais. O efeito numérico é provavelmente pequeno, mas é uma falha de
reprodutibilidade: qualquer reexecução com pesos diferentes pode amplificá-lo. Observação
adicional: a aba `n119|n72|n1|n73` use `n1` como feature — o mesmo rótulo do neurônio
oculto — o que dificulta a leitura e merece renomeação.

**Correção:** `K20 = MAX(-0.1*(...),(...))`, idêntico a `K21`.

### C4 — A pergunta de pesquisa não é respondida pelo artefato
O resumo e os objetivos propõem confrontar um modelo treinado em imagens caucasianas/
norte-americanas/asiáticas/afro-americanas com imagens de alunos com TEA de uma escola
municipal de Crateús-CE, para testar variantes étnicas latinas. **Não há aba, tabela nem
metadado com dados locais de Crateús**; as abas 21–25 contêm apenas embeddings do AID.
O texto de "Resultados esperados" inclusive prevê o fracasso do modelo nesse cenário —
mas como expectativa, não como teste.

**Correção:** explicitar no texto que o estudo atual é pré-clínico/exploratório e que a
validação transcultural ainda não foi realizada; só então planejar coleta com consentimento.

### C5 — Privacidade e ética não documentadas
O estudo envolve imagens faciais de **crianças** com TEA. O arquivo não registra aprovação
de comitê de ética, consentimento dos responsáveis, assentimento, anonimização nem controle
de acesso; há um stream `:Zone.Identifier` (Mark-of-the-Web) indicando origem de download.

**Correção:** anexar ao projeto o protocolo submetido ao CEP (ou justificar dispensa), o
termo de consentimento e o plano de anonimização; tratar imagens como dado sensível de
saúde sob a LGPD; não distribuir o `.xlsm` com dados brutos identificáveis.

---

## 2. Achados altos (P1)

- **Softmax invertido e sem estabilização:** `exp(-z)/Σexp(-z)` em `O:Q`. Logits negados são
  uma escolha legítima apenas se declarada, mas a ausência de subtração do máximo cria risco
  de overflow/underflow: há bias `-37,93` e pesos da ordem de `-17,56` no arquivo.
- **Perda quadrática com softmax:** `SUMXMY2` é utilizável, mas entropia cruzada é o padrão
  para classificação e dá gradientes mais bem comportados. Documentar a escolha.
- **Solver frágil:** `SolverOk` repetido 3×; `StepThru:=True`; `SolverSolve` sem
  `UserFinish:=True` (abre diálogo e trava automação); nenhum `SolverReset`; nenhuma checagem
  de convergência nem log; `ActiveSheet` implícito. Correção completa em
  `modSolverRNA_corrigido.bas`.
- **Erro de sintaxe VBA:** `Application.Caption = “DASHBOARD”` e `= “”` usam U+201C/U+201D.
  O p-code contém `Ld “DASHBOARD”`, indicando divergência entre fonte e compilação — em VBE
  moderno isso tende a gerar erro de compilação. Substituir por aspas retas `"..."`.
- **Módulos vazios (25Planilhas + Módulo1/2):** não há p-code órfão, portanto **não houve
  VBA stomping**; são apenas resíduos de template. Podem ser removidos para reduzir ruído.
- **Nomes definidos e `#REF!`:** 7 ocorrências em `workbook.xml`, incluindo `Pesos =
  #REF!,#REF!,...`, e nomes de frutas/imposto (`Bananas`, `Laranjas`, `Maçãs`,
  `ImpostoSobreVendas`, `Remessa`, `grp_GuieMeChave`). Limpar.

---

## 3. Achados médios (P2)

- **Texto científico em caixas de texto:** as abas 4–14 têm nome de seções científicas, mas
  as células contêm tutorial padrão do Excel; o conteúdo real está em `xl/drawings/*.xml`.
  Isso quebra busca, cópia, exportação PDF, leitores de tela e indexação. Recomenda-se
  transcrever o texto para células (coluna A, largura ajustada) preservando o original.
- **Peso e precisão espúria:** 102 MB; `sheet25.xml` com 442 MB descomprimido; 104 tabelas,
  36 gráficos e 55 desenhos; números com 15–16 dígitos. Recomenda-se mover os embeddings
  brutos para CSV/Parquet versionado com hash, manter no Excel só a amostra usada (180
  registros) e trocar `.xlsm` por `.xlsx` na distribuição de dados.
- **Exatidão histórica a revisar (verificar com fontes primárias):** o texto afirma que o
  DSM-IV foi publicado em 1987 (foi o DSM-III-R; o DSM-IV é de 1994), atribui a Bleuler
  1911 e a Kanner/Asperger 1943 (Asperger 1944) e diz que ADOS-G "ainda não foi validado no
  Brasil" — afirmação provavelmente desatualizada. Referência [1] sem autores; várias sem DOI.
- **Expectativa circular:** "espera-se 96% de precisão" importa um número externo como meta.
  Isso deve ser trocado por hipótese testável com intervalo de confiança.
- **Ambiente:** `python3 -m marceloclaro.cli doctor` falha por `ModuleNotFoundError: whoosh`
  (dependência ausente, alheia a esta auditoria); subagentes de ML/código falharam por
  assinatura/região do OpenCode Go. Verificação feita localmente com `oletools`, `pcodedmp`,
  `openpyxl` e parser OOXML.

---

## 4. Plano de correção recomendado (não aplicado)

**Onda 1 — integridade (baixo risco, alta prioridade)**
1. `K20` → sinal negativo nas 5 abas.
2. Renomear `S15` para "1 − EQM (não é acurácia)" ou remover; corrigir `AG35/AH35`.
3. Corrigir aspas do `Módulo4`; substituir `Módulo3` pelo módulo proposto.
4. Limpar nomes definidos e `#REF!`.

**Onda 2 — validade (exige decisão do autor)**
5. Recuperar/confirmar as 60 imagens de teste; compute acurácia, sensibilidade,
   especificidade, matriz de confusão e IC 95% no teste.
6. Declarar a métrica de perda e justificar softmax com sinal negado; considerar
   estabilização numérica e entropia cruzada.
7. Registrar semente, versão do Solver, versão do Excel, feature selection feita **antes**
   da separação treino/teste (para evitar vazamento) e número de execuções.

**Onda 3 — comunicação científica**
8. Transcrever texto das caixas para células; corrigir datas/DSM; converter referências
   para ABNT com DOI conferido; separar claramente resultado obtido de expectativa.
9. Documentar ética, consentimento, anonimização e limitação transcultural.

---

## 5. O que NÃO é possível concluir com este arquivo

- Se o Solver convergiu de fato: os pesos em cache são finitos, mas não há log de status.
- Se a seleção de pares de atributos usou o conjunto de teste (risco de vazamento):
  as abas 21–23 mostram ranks, não o protocolo de seleção.
- Se os 96% citados procedem: são atribuídos a Mujeeb Rahman & Subashini (2022), não
  reproduzidos aqui, e o melhor número interno é ~82% de uma métrica inválida.
- Se há dados de Crateús-CE: não estão no workbook.
- Desempenho clínico: nada aqui valida uso diagnóstico; seria necessário desenho com
  referência-padrão (CARS/ADOS), amostra externa e análise de calibração.

---

## 6. Evidências e reprodutibilidade

`verificar_auditoria.py` reproduz 10 checagens determinísticas (10/10 PASS), sem alterar o
artefato: resíduos de template, `#REF!`, aspas tipográficas, 5 abas, erro do ReLU, fórmula
de "acurácia", contagens 120/30, ausência de métrica no teste, divergência documental e
ausência de p-code órfão (`_pcode_evidencia.txt`). Relatório `olevba`: `/tmp/opencode/olevba_report.txt`.
