# M1 — Problema, lacuna e arquitetura argumentativa

**Artefato:** rascunho para aprovação
**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Data:** 2026-11-21

## 1. Problema

Pipelines de RNA construídos diretamente em planilhas combinam fórmulas, macros, gráficos e dados em um único arquivo binário. Essa concentração facilita o uso imediato, mas torna opacas três camadas críticas: a lógica de ativação, a definição da função-objetivo e o significado dos rótulos de métricas. No workbook auditado, essas camadas apresentaram falhas simultâneas:

- `K20` usava `MAX(0.1*z,z)` enquanto `K21` usava `MAX(-0.1*z,z)` — assimetria de sinal na ativação Leaky ReLU.
- A célula rotulada "Acurácia" continha `1 − R16`, isto é, `1 − EQM médio`, e não proporção de acertos.
- `AG35/AH35` dividiam `R16/S16` por 100, produzindo escala incorreta.
- Nomes definidos continham resíduos de template e a entrada `Pesos` com sete referências `#REF!`.
- O projeto VBA continha chamadas duplicadas a `SolverOk`, `StepThru:=True` e aspas tipográficas em comando.

Como consequência, números aparentemente precisos podiam ser interpretados como desempenho validado quando, na verdade, descreviam um estado computacional não verificado.

## 2. Lacuna

`[A DEMONSTRAR EM M2]` — a afirmação de que a literatura ainda não oferece protocolos determinísticos acessíveis para auditoria de planilhas de RNA em contextos de saúde **não está demonstrada**. M2 deverá documentar string de busca, bases, datas, critérios de inclusão/exclusão e fichas de auditoria antes que esta lacuna se torne parte do argumento.

**Atualização M2 (22/11/2026):** a busca foi executada e documentada em quatro vias públicas. A lacuna passa a estar demonstrada **nos termos do escopo pesquisado** — isto é, "não foi localizado nas buscas realizadas", sem pretensão de exaustividade ou de inexistência universal. Ver `M2_protocolo_busca.md`, `M2_fichas_auditoria.md` e `M2_sintese_lacuna.md`. O marcador original é preservado para rastreabilidade da evolução do marco.

## 3. Pergunta principal e subperguntas

**Pergunta principal:** Como falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas, e quais controles determinísticos permitem detectá-las e repará-las sem destruir o artefato original?

**Subperguntas:**

- **SP1.** Quais falhas são detectáveis por inspeção determinística do pacote OOXML e dos streams VBA?
- **SP2.** Como a assimetria de sinal em `K20` altera o forward pass e invalida a comparação com o cache original?
- **SP3.** Que mecanismos impedem que métricas calculadas antes do reparo sejam reportadas como resultado do modelo reparado?
- **SP4.** Quais propriedades do pacote precisam ser preservadas para que o reparo não destrua gráficos, desenhos, mídia e tabelas?

## 4. Proposições testáveis

Não se trata de hipótese estatística sobre população; são proposições verificáveis no artefato:

- **P1.** A inspeção direta do OOXML detecta falhas que uma leitura superficial das células não revela.
- **P2.** A definição de "Acurácia" como `1 − EQM` é recuperável das fórmulas, embora o rótulo sugira outra métrica.
- **P3.** A edição direta do ZIP, com recompactação controlada, preserva as contagens de gráficos, desenhos, mídia e tabelas.
- **P4.** A ativação de `fullCalcOnLoad` e a remoção de `calcChain.xml` tornam obrigatório rotular os valores em cache como não validados.

## 5. Objetivos

**Objetivo geral:** propor e aplicar um protocolo determinístico de auditoria e reparo para pipelines de RNA em planilha, avaliando sua capacidade de preservar o artefato e de prevenir a comunicação enganosa de métricas.

**Objetivos específicos:**

1. Inventariar falhas no original por verificações reproduzíveis.
2. Reparar em cópia as falhas de Onda 1 e documentar as de Onda 2.
3. Recomputar métricas do cache com rótulo de proveniência e incerteza.
4. Verificar a integridade estrutural da cópia em comparação com o original.
5. Derivar recomendações de reporte para estudos que usem planilhas como ambiente de modelagem.

## 6. Construtos e variáveis

| Construto | Operacionalização |
|---|---|
| Falha de implementação | Divergência entre fórmula/rótulo e a definição metodológica declarada |
| Validade de métrica | Correspondência entre o número reportado e o procedimento de cálculo efetivo |
| Rastreabilidade | Presença de hash, versão, log e proveniência para cada artefato |
| Integridade estrutural | Contagens e nomes de partes do ZIP preservados, exceto `calcChain.xml` |
| Incerteza | Intervalo de confiança Wilson 95% para proporções com `n=30` |

Variáveis observadas: sinal da ativação em `K20/K21`, conteúdo de `R16/S16`, escala de `AG35/AH35`, contagens de partes do ZIP, presença de `#REF!` e de p-code, TP/TN/FP/FN do bloco de teste.

## 7. Unidade de análise

Artefato (workbook), com desdobramento em aba de RNA, célula individual e stream OLE. Não há unidade humana neste marco; qualquer referência a participantes ou imagens depende de confirmação de proveniência.

## 8. Delimitação

- Um workbook específico, cinco abas de RNA, trinta registros de teste por aba.
- Sem reexecução do Solver neste marco; sem uso das imagens; sem amostra externa.
- Sem inferência sobre prevalência de TEA, desempenho diagnóstico ou eficácia clínica.
- Sem generalização para outros workbooks além daqueles que apresentarem as mesmas condições estruturais.

## 9. Justificativa

Erros em planilhas são baratos de introduzir e caros de detectar, especialmente quando a saída é uma probabilidade ou um rótulo de acerto. Em contextos de saúde, um rótulo incorreto pode transformar uma perda em "acurácia" e alterar a interpretação de um resultado. Um protocolo determinístico, executável sem abrir o arquivo em um host específico, oferece uma camada de defesa de baixo custo e alta rastreabilidade.

## 10. Contribuições esperadas

- **Metodológica:** sequência de verificações e reparo com preservação de artefato.
- **Técnica:** implementação reprodutível em Python e compressor MS-OVBA próprio para manter tamanho de streams.
- **Comunicacional:** regra explícita de separação entre cache diagnóstico e resultado validado.
- **Educacional:** taxonomia de falhas ilustrada com células reais do workbook.

## 11. Matriz de coerência

| Problema | Pergunta | Objetivos | Método | Análise | Resultado | Conclusão |
|---|---|---|---|---|---|---|
| Ativação assimétrica e métrica mal rotulada em planilha de RNA | Como detectar e reparar sem destruir o artefato? | Inventariar, reparar, recomputar, verificar | Inspeção OOXML/VBA + edição direta do ZIP + compressor OVBA | Comparação de hashes, contagens e fórmulas; Wilson 95% | 10/10 no original; 22/22 na cópia; 60→30 imagens documentadas | Protocolo detecta e repara falhas estruturais; não valida desempenho clínico |
| Cache pré-correção pode ser confundido com resultado do modelo reparado | Como impedir essa confusão? | Rotular proveniência e forçar recálculo | `fullCalcOnLoad`, remoção de `calcChain`, aviso em `T157` | Leitura de fórmulas e avisos; recomputação do cache | Aviso explícito nas 5 abas | Números antigos devem ser lidos como diagnóstico, não como desempenho |
| Lacuna não demonstrada | A auditoria é realmente uma contribuição? | Demonstrar lacuna na literatura | Busca documentada com fichas auditadas | Triagem e síntese crítica | `[A DEMONSTRAR EM M2]` | Contribuição só será afirmada se a lacuna for confirmada |

## 12. Pendências

- `[A DEMONSTRAR EM M2]` lacuna na literatura.
- `[A CONFIRMAR]` periódico, instituição, prazo, natureza dos dados de imagem, consentimento e anonimização.
- `[A CONFIRMAR]` se o abstract em inglês será exigido pelo periódico.
- Nenhuma referência bibliográfica foi inserida neste marco; nenhum DOI foi inventado.
