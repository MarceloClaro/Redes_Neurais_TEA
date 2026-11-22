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
