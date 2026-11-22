# M0 — Contrato acadêmico

**Artefato:** rascunho para aprovação
**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Data:** 2026-11-21
**Orquestrador:** marceloclaro

## 1. Identificação

| Campo | Valor |
|---|---|
| Nível | Artigo científico |
| Área | Informática em Saúde / Ciência de Dados |
| Subárea | Auditoria de pipelines de aprendizado de máquina; reprodutibilidade computacional |
| Modalidade | Auditoria técnica com reparo de artefato (estudo de caso metodológico) |
| Idioma | Português brasileiro; abstract em inglês a confirmar |
| Norma | ABNT — NBR 14724, NBR 6023 e NBR 10520 |
| Periódico-alvo | `[A CONFIRMAR]` |
| Instituição/programa | `[A CONFIRMAR]` |
| Prazo | `[A CONFIRMAR]` |
| Extensão sugerida | 8–12 páginas, incluindo tabelas e notas de reprodutibilidade |

## 2. Pergunta provisória

**Como falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas, e quais controles determinísticos permitem detectá-las e repará-las sem destruir o artefato original?**

Pergunta provisória porque M2 ainda não demonstrou a lacuna na literatura; a redação final será ajustada após a busca auditada.

## 3. Contribuição pretendida

1. **Taxonomia de falhas** em planilhas de RNA: erro de sinal em ativação, métrica nomeada incorretamente, escala indevida, nomes definidos com `#REF!`, resíduos de template e p-code obsoleto.
2. **Gate determinístico** de auditoria com verificações reproduzíveis sobre OOXML, VBA e fórmulas.
3. **Protocolo de reparo** que preserva gráficos, desenhos, mídia e tabelas mediante edição direta do pacote, sem `openpyxl.save`.
4. **Demonstração empírica local** de que `1 − EQM` estava rotulado como "Acurácia" e de que `K20` usava `MAX(0.1*z,z)` onde `K21` usava `MAX(-0.1*z,z)`.
5. **Regra de comunicação**: valores de cache pré-correção não podem ser reportados como desempenho do modelo corrigido.

## 4. Tipo de estudo

Auditoria técnica/estudo de caso metodológico. **Não** é ensaio clínico, **não** é estudo de validação diagnóstica, **não** é revisão sistemática (a menos que M2 redefine o desenho) e **não** contém inferência causal.

## 5. Corpus e dados disponíveis

- 1 workbook `.xlsm` original, preservado por SHA-256 `1c4c94ab…953dcd`.
- 1 cópia corrigida, SHA-256 `3320701b…bb475`, aprovada por 22 verificações.
- 5 abas de RNA; 120 registros de treino por aba; 30 registros de teste por aba (`G145:G174`).
- 25 planilhas, 36 gráficos, 55 desenhos, 22 mídias, 104 tabelas no pacote.
- Solver e 30 imagens de teste: **disponíveis com o usuário**, a incorporar em marco posterior com registro de versão, status e proveniência.

Unidade de análise: artefato, aba, célula ou stream VBA. Não há participantes humanos neste marco.

## 6. Configuração editorial

- **Norma:** ABNT (NBR 14724 para apresentação; NBR 6023 para referências; NBR 10520 para citações).
- **Estrutura:** IMRAD — introdução, objetivos, materiais e métodos, resultados, discussão, conclusão; complementos de disponibilidade de dados/código, declaração de IA, conflitos, financiamento e autoria.
- **Periódico:** `[A CONFIRMAR]` — a instrução oficial atual será consultada antes de M6.
- **Abstract:** a confirmar idioma e exigência do periódico.

## 7. Mapa de entregáveis

| Marco | Arquivo previsto | Status |
|---|---|---|
| M0 | `artigo/M0_contrato_academico.md` | entregue |
| M1 | `artigo/M1_problema_lacuna_arquitetura.md` | entregue |
| M2 | `artigo/M2_protocolo_busca.md` + fichas de auditoria | pendente |
| M3 | `artigo/M3_metodo_etica.md` | pendente |
| M4 | `artigo/M4_resultados_tabelas.md` | pendente |
| M5 | `artigo/MANUSCRITO_rascunho.md` | pendente |
| M6 | versão formatada ABNT | pendente |
| M7 | `artigo/M7_relatorio_banca.md` | pendente |

## 8. Limites éticos e de transparência

- O workbook contém descritores extraídos de imagens humanas; a natureza dos dados, o consentimento e a anonimização precisam ser confirmados pelo usuário antes de qualquer afirmação.
- Nenhuma alegação de desempenho clínico será feita sem referência-padrão, amostra externa e aprovação ética documentada.
- Dados, código e hashes serão declarados com localização e restrições; se não houver repositório público, dizer explicitamente "sob demande".
- Uso de ferramentas de IA na auditoria e na redação será declarado na seção correspondente.

## 9. Riscos e pendências

| Risco | Impacto | Ação |
|---|---|---|
| `producao_cientifica/` está no `.gitignore` | Artefatos fora do controle de versão | Solicitar ao usuário autorização para versionar ou mover para pasta rastreada; não alterar `.gitignore` por conta própria |
| Lacuna não demonstrada | Introdução fraca | M2 com busca documentada antes de redigir |
| Solver não reexecutado neste ambiente | Resultados pós-correção indisponíveis | Usar apenas cache como diagnóstico; integrar novo log quando o usuário executar |
| Imagens ausentes no pacote | Proveniência incompleta | Coletar hashes e origem com o usuário |
| `n=30` com IC largo | Risco de generalização indevida | Reportar incerteza e limitar conclusões ao artefato analisado |
| Referências não auditadas | Risco de citação inválida | Nenhuma referência entra sem fonte primária conferida |
