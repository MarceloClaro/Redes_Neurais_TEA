# SPEC-935-R1282 — Artigo de auditoria metodológica de pipeline de RNA em planilha (TEA)

**ID:** SPEC-935-R1282
**Data:** 2026-11-21
**Orquestrador:** marceloclaro
**Status:** proposed — M0 a M7 entregues; aguardando aprovação da revisão humana e evidências pendentes do usuário
**Autorização do usuário:** caminho A (auditoria metodológica); Solver e imagens disponíveis para marco posterior; norma ABNT

## 1. Objetivo

Produzir um artigo científico em ABNT cuja contribuição seja **metodológica**: demonstrar, com evidência determinística, como falhas de implementação em um pipeline de rede neural artificial (RNA) hospedado em planilha `.xlsm` comprometem a validade de métricas reportadas, e propor controles de auditoria e reparo que preservem o artefato original.

## 2. Escopo

### Incluído
- Auditoria determinística de OOXML, VBA, fórmulas e nomes definidos (10 verificações do original).
- Reparo em cópia: Ondas 1 e 2, gate de 22 verificações.
- Análise do erro de sinal em `K20`, da métrica `1 − EQM` rotulada como "Acurácia" e da escala indevida em `AG35/AH35`.
- Métricas do cache pré-correção, **rotuladas como diagnóstico do estado original**.
- Divergência entre valor em cache e fórmula textual do intervalo de confiança, documentada sem escolha de versão correta.
- Proposta de taxonomia de falhas e de protocolo de verificação reproduzível.

### Fora de escopo nesta spec
- Desempenho clínico, validação externa, calibração e inferência causal.
- Reexecução do Solver e uso das 30 imagens — disponíveis com o usuário, registrados como pendência em M4 e reservados para integração futura com log e proveniência.
- Alegação de Qualis, nota, aceite ou aprovação editorial.
- Inventário de autores/DOI sem verificação por fonte primária.

## 3. Marcos e gates

| Marco | Entrega | Gate | Status |
|---|---|---|---|
| M0 | Contrato acadêmico | `artigo/verificar_m0_m1.py` | entregue |
| M1 | Problema, lacuna e arquitetura argumentativa | `artigo/verificar_m0_m1.py` | entregue |
| M2 | Busca e auditoria bibliográfica | `artigo/verificar_m2.py` (23/23) | entregue |
| M3 | Projeto metodológico e ética | `artigo/verificar_m3.py` (20/20) | entregue |
| M4 | Dados, análise e resultados | `artigo/verificar_m4.py` (22/22) | entregue — parte executável; log/imagens pendentes |
| M5 | Redação modular IMRAD | `artigo/verificar_m5.py` (24/24) | entregue |
| M6 | Formatação ABNT | `artigo/verificar_m6.py` (33/33) | entregue |
| M7 | Auditoria final e banca simulada | `artigo/verificar_m7.py` (H-01..H-24) | entregue — sete auditorias locais; delegações falharam antes da execução |

Avançar após aprovação explícita do usuário em cada marco, conforme o fluxo modular da skill `pesquisa-artigo-qualis-a1`.

## 4. Critérios de aceitação

| ID | Critério | Verificação |
|---|---|---|
| AC-1 | Spec formal precede qualquer entrega | este arquivo |
| AC-2 | M0 registra pergunta, tipo de estudo, norma, dados, entregáveis, ética e riscos | G-03, G-04 |
| AC-3 | M1 registra problema, lacuna pendente, perguntas, objetivos, construtos, unidade, delimitação e matriz de coerência | G-05, G-06, G-07 |
| AC-4 | Nenhuma promessa editorial ou de nota | G-08 |
| AC-5 | Nenhum DOI ou referência inventada | G-13 |
| AC-6 | Artefatos prévios íntegros e original preservado | G-10, G-11 |
| AC-7 | Risco de versionamento registrado | G-12 (M0/M1) |
| AC-8 | M2 registra bases, strings, datas, contagens e triagem com exclusões justificadas | `verificar_m2.py` G-03..G-09 |
| AC-9 | Lacuna afirmada apenas como ausência nas buscas realizadas | `verificar_m2.py` G-13, G-14 |
| AC-10 | Nenhum DOI inventado em M2 | `verificar_m2.py` G-12 |
| AC-11 | M3 com desenho, unidades, diretriz justificada, ética e matriz de riscos | `verificar_m3.py` G-02..G-13 |
| AC-12 | M4 recomputa cache com script auditável, separa diagnóstico de resultado validado e registra divergência do IC | `verificar_m4.py` G-02..G-22 |
| AC-13 | M5 consolida IMRAD de forma determinística, cita todas as fontes incluídas e preserva pendências e limites | `verificar_m5.py` G-02..G-24 |
| AC-14 | M6 formata ABNT, audita os 13 DOIs sem invenção, registra a triagem de alegações e mantém pendências | `verificar_m6.py` G-02..G-33 |
| AC-15 | M7 consolida sete auditorias locais e banca simulada, registra a falha das delegações sem contabilizá-las como revisão externa, rebaixa efeitos não medidos e preserva pendências | `verificar_m7.py` H-02..H-24 |

## 5. Regras de integridade

1. Distinguir fato observado, inferência, proposição e recomendação.
2. Marcar `[A CONFIRMAR]` e `[A DEMONSTRAR EM M2]` toda informação ainda não verificada.
3. Não converter associação em causalidade nem métrica de cache em resultado validado.
4. Toda referência central deve ter identificador persistente ou URL oficial conferida antes de entrar no argumento.
5. Toda citação no corpo deve aparecer nas referências, e toda referência listada deve ser citada.

## 6. Riscos conhecidos

- `producao_cientifica/` está listado no `.gitignore`; os artefatos não estão versionados (registrado em M0).
- Lacuna formulada em M2 apenas como ausência nas buscas realizadas; não é prova de inexistência universal.
- Reexecução do Solver e uso das 30 imagens dependem de sessão com Excel, log e arquivos do usuário; o usuário informou que executará e enviará.
- Amostra de teste pequena (`n=30`) produz intervalos largos; generalização é inadmissível.
- Busca web geral indisponível (HTTP 402) e arXiv bloqueado por `robots.txt`; M2 usou apenas quatro vias públicas e resumos indexados.
- Ano de publicação da fonte F12 diverge entre bases; marcado como `[A CONFIRMAR]`.
- Valor de IC em cache foi reproduzido em M4 pela forma padrão de Wilson; a fórmula textual das células produz intervalo mais estreito. Causa da divergência não resolvida sem histórico de edição; workbook não foi alterado.
- F11 (Ahmad) mantém ano 2004 no corpo e no texto de M5, enquanto Crossref e DOI indicam 2003; a divergência foi registrada em M6 sem alteração silenciosa.
- Parâmetros de diagramação (papel, margens, fonte, paginação e abstract) dependem do periódico-alvo e permanecem `[A CONFIRMAR PELO PERIÓDICO]`; a versão ABNT é Markdown mapeado para conversão futura.
- Cinco delegações de agentes em M7 falharam antes da execução (restrição regional do OpenCode Go e assinatura ativa); as auditorias finais foram executadas localmente e não equivalem a revisão externa.
- Três verbos de efeito não medido (`impede`/`prevents`) foram rebaixados para intenção de projeto; M5 e M6 foram regenerados e permanecem em 24/24 e 33/33.

## 7. Extensão R1291 (2026-11-22)

A cópia corrigida recebeu a aba documental `AUDITORIA_M7`, autorizada pelo usuário, e passou a ter 26 planilhas (25 originais mais a aba). Nenhuma fórmula, modelo, VBA, gráfico, desenho, mídia ou tabela foi alterado. O hash pré-r1291 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` permanece como registro histórico do estado descrito em M4–M7 e está preservado em `producao_cientifica/auditoria/backup/`. O hash atual da cópia é `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`.

A exploração estatística separada, em `producao_cientifica/auditoria/artigo/exploracao/`, usa somente o cache M4, com semente fixa 20261122. Ela compara critérios de decisão sobre as matrizes observadas, recomputa Wilson, reamostra as células por classe e testa perturbação hipotética de rótulo. Como o cache não contém escores individuais, nenhum limiar de probabilidade foi inventado. Nenhum ganho de acurácia do modelo corrigido é afirmado; o Solver não foi reexecutado e as 30 imagens não foram integradas. A especificação detalhada é `SPEC-935-R1291-aba-auditoria-exploracao-rna-tea.md` e o gate é `verificar_r1291.py` (AC-1..AC-12).
