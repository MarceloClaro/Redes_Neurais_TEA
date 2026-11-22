# Auditoria final 5 — Reprodutibilidade, proveniência e ética

Nota metodológica: a delegação a agente especializado falhou antes da execução por restrição regional do modelo OpenCode Go. Não houve auditoria externa; o trabalho abaixo foi executado localmente. Declara-se reprodutibilidade da **auditoria**, jamais do treino da RNA ou do desempenho do modelo corrigido.

| Item | Evidência | Status | Limite |
|---|---|---|---|
| Hash do original | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` | rastreável | confirma identidade, não integridade semântica de todo conteúdo |
| Hash da cópia (pré-r1291) | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` | rastreável | distinta do original, como esperado |
| Hash da cópia (atual) | `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb` | rastreável | aba `AUDITORIA_M7` inserida; modelos e fórmulas inalterados |
| Preservação do original | gate `verificar_auditoria.py` 10/10 | rastreável | original não reeditado neste marco |
| Edição do pacote | OOXML e streams OLE/VBA diretos; sem `openpyxl.save` | rastreável | executada neste ambiente, não documentada em outro sistema |
| Inventário estrutural (pré-r1291) | 25 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | rastreável | contagens do gate da correção |
| Inventário estrutural (atual) | 26 planilhas; 36 gráficos; 55 desenhos; 22 mídias; 104 tabelas | rastreável | 25 originais mais a aba documental |
| `xl/calcChain.xml` | única parte removida do ZIP | rastreável | remoção intencional, registrada |
| `fullCalcOnLoad="1"` | presente nas cinco abas de RNA | rastreável | depende de abertura no Excel para ter efeito |
| VBA e p-code | `Módulo3` e `Módulo4` reescritos; `PerformanceCache` zerado | rastreável | macros não executadas neste ambiente |
| Comandos de verificação | nove gates reexecutados, de 10/10 a 33/33 | rastreável | contagens sempre reexecutadas, nunca inferidas de relatório anterior |
| Ambiente Python | `.venv/bin/python`; `doctor` 16 passed, 6 warned, 0 failed | rastreável | seis avisos permanecem; `python3` do sistema falha por falta de `whoosh` |
| Saída JSON M4 | `M4_metricas_cache.json` com comando, fórmulas e hash | rastreável | descreve recomputação, não treino |
| Tabela de métricas | `M5_03_resultados.md` e Tabela 1 do MANUSCRITO_ABNT | rastreável | valores são diagnóstico do cache pré-correção |
| Cache versus resultado validado | aviso em `T157` e regra de comunicação no §4.1 | rastreável | nenhum número pós-correção é apresentado |
| Solver | não reexecutado; versão, data, status, seed e pesos finais ausentes | pendente | depende de log a enviar pelo usuário |
| 30 imagens | não integradas; ausentes proveniência, licença e referência-padrão | pendente | nenhuma análise de imagem realizada neste marco |
| Consentimento e anonimização | marcados `[A CONFIRMAR]` em `M5_07_declaracoes.md` | pendente | sem esses dados, não há deliberação ética possível |
| Financiamento | `[A CONFIRMAR]` | pendente | não declarar ausência sem confirmação |
| Conflitos de interesse | `[A CONFIRMAR]` | pendente | não declarar ausência sem confirmação |
| Autoria e contribuições | `[A CONFIRMAR]` | pendente | nomes e afiliações não fornecidos |
| Uso de IA | declarado em `M5_07_declaracoes.md` | rastreável | revisão humana final não registrada como concluída |
| Deposição de dados/código | `producao_cientifica/` no `.gitignore`; nada commitado | parcial | local público, licença e condições de acesso `[A CONFIRMAR]` |
| Periódico-alvo | `[A CONFIRMAR]` | pendente | determine exigência de abstract, normas de diagramação e prazo |
| Geradores determinísticos | `montar_m5.py` e `montar_m6.py` sem data/hora | rastreável | M7 seguirá o mesmo padrão |

## O que é reproduzível

São reproduzíveis neste ambiente: a inspeção do original e da cópia por hashes e contagens; os nove gates de verificação; a recomputação das métricas a partir do cache por `recomputar_cache.py`; a avaliação numérica das duas versões do intervalo de confiança; e a regeneração determinística do rascunho IMRAD e da versão ABNT a partir dos módulos-fonte. Comandos, saídas e marcos estão registrados na SPEC e nos apêndices.

## O que não é reproduzível neste ambiente

Não são reproduzíveis: o treino da RNA pelo Solver, porque não houve reexecução nem log com versão, data, status, seed e pesos finais; o desempenho do modelo corrigido, porque a correção de `K20` não foi seguida de otimização; a análise das 30 imagens, porque não foram fornecidas nem acompanhadas de proveniência e consentimento; e a conferência do texto integral das fontes, porque apenas metadados e resumos foram consultados. A edição da fórmula textual do IC depende de autorização explícita e não foi executada.

## Recomendações antes de submissão

1. Enviar e arquivar o log do Solver com versão do Excel/Solver, data, status de convergência, seed, arquivo salvo e hash dos pesos finais; separar esse artefato do cache original.
2. Fornecer proveniência das 30 imagens, natureza dos dados, consentimento, anonimização, licença de uso e referência-padrão antes de qualquer incorporação.
3. Decidir, com registro de versão, se a fórmula textual do IC será editada; essa é a Onda 3 e exige autorização explícita.
4. Confirmar periódico-alvo, autoria, financiamento, conflitos, instituição e local de depósito de dados/código.
5. Registrar revisão humana final e aplicar diagramação ABNT no editor, com paginação, margens e fonte confirmadas.
6. Publicar ou disponibilizar os scripts e as saídas com licença declarada, mantendo o original preservado.

Esta auditoria documenta rastreabilidade e limites; não substitui revisão humana nem estabelece reprodutibilidade completa do estudo.
