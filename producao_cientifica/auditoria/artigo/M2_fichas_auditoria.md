# M2 — Fichas de auditoria bibliográfica

**Artefato:** rascunho para aprovação
**Protocolo:** `M2_protocolo_busca.md`
**Busca:** 21 de novembro de 2026 · consolidação: 22 de novembro de 2026

## Convenções

- **Achado** = afirmação extraída do resumo ou dos metadados efetivamente consultados. Não é avaliação do texto integral.
- **Limitação de uso** = fronteira que impede emprestar à fonte uma conclusão que ela não sustenta.
- **Papel argumentativo** = função pretendida no manuscrito, ainda a ser confirmada na redação (M5).
- Padrões de URL de auditoria: `https://api.openalex.org/works/doi:{DOI}?select=...`, `https://api.crossref.org/works/{DOI}` e `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"{DOI}"&format=json&resultType=lite|core`.

---

## F01 — TRIPOD+AI statement (incluída)

| Campo | Valor |
|---|---|
| Título | TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods |
| Ano / periódico | 2024 / BMJ |
| Identificadores | DOI `10.1136/bmj-2023-078378`; PMID `38626948`; OpenAlex `W4394857110` |
| Tipo / desenho | Diretriz de relato atualizada;artigo de desenvolvimento da diretriz |
| URL de auditoria | OpenAlex `works/doi:10.1136/bmj-2023-078378`; Europe PMC `DOI:"10.1136/bmj-2023-078378"` |

**Achado.** O TRIPOD (2015) fornecia recomendações mínimas de relato; com o uso disseminado de modelos de IA/ML, foi necessária uma atualização. O TRIPOD+AI harmoniza o relato de modelos preditivos independentemente do uso de regressão ou aprendizado de máquina, substitui a lista de 2015, apresenta lista ampliada de **27 itens**, explicação detalhada e lista para resumos. Seu objetivo é promover relato completo, exato e transparente para facilitar avaliação, comparação e implementação de modelos.

**Limitação de uso.** É diretriz de **relato**, não ferramenta de inspeção de artefato: não examina fórmulas, OOXML, VBA nem caches. O presente estudo não é um estudo de desenvolvimento/validação de modelo clínico e não preenche a lista de 27 itens.

**Papel argumentativo.** Fundamentar a exigência de declarar proveniência, definição de métrica e estado do modelo; fixar a distinção entre "relato transparente" e "resultado validado" na discussão.

---

## F02 — TRIPOD Statement (incluída)

| Campo | Valor |
|---|---|
| Título | Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD Statement |
| Ano / periódico | 2015 / BMC Medicine |
| Identificadores | DOI `10.1186/s12916-014-0241-z`; PMID `25563062`; OpenAlex `W2019694480` |
| Tipo / desenho | Diretriz de relato; desenvolvimento baseado em revisão da literatura, pesquisa pela web e reunião de metodologistas, profissionais de saúde e editores |
| URL de auditoria | OpenAlex `works/doi:10.1186/s12916-014-0241-z`; Europe PMC `DOI:"10.1186/s12916-014-0241-z"` |

**Achado.** A qualidade do relato de estudos de modelos preditivos é, em geral, baixa. Somente com relato completo e claro de todos os aspectos do modelo é possível avaliar adequadamente o risco de viés e a utilidade potencial. A diretriz cobre estudos de desenvolvimento, validação ou atualização de modelos diagnósticos e prognósticos.

**Limitação de uso.** Foi **superada** pelo TRIPOD+AI (F01) para estudos que envolvem aprendizado de máquina; deve ser citada como contexto histórico, não como lista normativa corrente.

**Papel argumentativo.** Mostrar que a preocupação com transparência em modelos preditivos é antiga e que a opacidade de rótulos e proveniência é problema reconhecido — sem transferir para o workbook uma condição de estudo clínico.

---

## F03 — PROBAST (incluída)

| Campo | Valor |
|---|---|
| Título | PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies |
| Ano / periódico | 2019 / Annals of Internal Medicine |
| Identificadores | DOI `10.7326/M18-1376`; PMID `30596875`; OpenAlex `W2907554860` |
| Tipo / desenho | Ferramenta de avaliação de risco de viés e aplicabilidade; Delphi com 38 especialistas e piloto |
| URL de auditoria | OpenAlex `works/doi:10.7326/M18-1376`; Europe PMC `DOI:"10.7326/M18-1376"` |

**Achado.** A ferramenta organiza-se em quatro domínios — participantes, preditores, desfecho e análise — com 20 perguntas-sinal. Define risco de viés como distorção sistemática de estimativas de desempenho decorrente de falhas em desenho, condução ou análise. Embora desenvolvida para revisões sistemáticas, pode ser usada na apreciação crítica de estudos de modelos preditivos.

**Limitação de uso.** Não avalia código, fórmulas nem integridade de planilha. O domínio "análise" é aqui emprestado apenas como **conceito**: uma falha de implementação pode distorcer desempenho reportado. Não afirmaremos que o workbook foi avaliado pelos 20 itens do PROBAST.

**Papel argumentativo.** Apoiar a proposição de que falhas de análise/implementação comprometem a validade de métricas — uma das teses centrais do artigo — com vocabulário metodológico reconhecido.

---

## F04 — Adherence to TRIPOD+AI (incluída)

| Campo | Valor |
|---|---|
| Título | Adherence to TRIPOD+AI guideline: an updated reporting assessment tool |
| Ano / periódico | 2026 (publicação online registrada como 2025 no OpenAlex) / Journal of Clinical Epidemiology |
| Identificadores | DOI `10.1016/j.jclinepi.2025.112118`; PMID `41448505`; OpenAlex `W7116843807` |
| Tipo / desenho | Estudo de desenvolvimento de instrumento de avaliação de aderência; discussão de equipe e teste piloto |
| URL de auditoria | OpenAlex `works/doi:10.1016/j.jclinepi.2025.112118`; Europe PMC `DOI:"10.1016/j.jclinepi.2025.112118"` |

**Achado.** Relato incompleto limita a utilidade da pesquisa e contribui para desperdício de pesquisa. A avaliação de aderência a diretrizes frequentemente carece de uniformidade. Os autores atualizaram a ferramenta original do TRIPOD para o TRIPOD+AI, resultando em instrumento com **37 itens principais** e regras de pontuação refinadas.

**Limitação de uso.** Avalia a **completude do relato**, não a correção da execução. Não detecta erro de sinal nem mede integridade de artefato.

**Papel argumentativo.** Justificar a analogia entre instrumento de aderência (uniformidade de critérios para julgar relato) e gate determinístico (uniformidade de critérios para julgar artefato computacional).

---

## F05 — Variabilidade e reprodutibilidade em segmentação de imagens médicas (incluída)

| Campo | Valor |
|---|---|
| Título | Variability and reproducibility in deep learning for medical image segmentation |
| Ano / periódico | 2020 / Scientific Reports |
| Identificadores | DOI `10.1038/s41598-020-69920-0`; PMID `32792540`; OpenAlex `W3048802707` |
| Tipo / desenho | Revisão da literatura com proposta de recomendações |
| URL de auditoria | OpenAlex `works/doi:10.1038/s41598-020-69920-0`; Europe PMC `DOI:"10.1038/s41598-020-69920-0"` |

**Achado.** Modelos de aprendizado profundo superam métodos clássicos em segmentação de imagens médicas, mas são complexos e podem apresentar ampla variabilidade, colocando em questão a reprodutibilidade. Os autores propõem três recomendações: descrição adequada do framework de aprendizado profundo, análise das fontes de variabilidade e sistema eficiente de avaliação dos resultados.

**Limitação de uso.** O domínio é segmentação de imagens médicas, não classificação em planilha; a fonte não trata OOXML, VBA ou Solver do Excel.

**Papel argumentativo.** Fundamentar a necessidade de descrever framework, versões, semente e avaliação — exatamente o que faltava no workbook original — e sustentar a recomendação de log de reexecução do Solver em M3/M4.

---

## F06 — Towards training reproducible deep learning models (incluída)

| Campo | Valor |
|---|---|
| Título | Towards training reproducible deep learning models |
| Ano / periódico | 2022 / conferência indexada pela ACM |
| Identificadores | DOI `10.1145/3510003.3510163`; OpenAlex `W4220914596` |
| Tipo / desenho | Proposta metodológica com framework e diretriz; avaliação em seis projetos de código aberto e um comercial informada no resumo |
| URL de auditoria | OpenAlex `works/doi:10.1145/3510003.3510163` |

**Achado.** A reprodutibilidade em aprendizado profundo é ameaçada por aleatoriedade de software e não determinismo de hardware. Os autores propõem critérios de avaliação, um framework com `record-and-replay` para aleatoriedade de software e `profile-and-patch` para não determinismo de hardware, além de diretriz de reprodutibilidade.

**Limitação de uso.** Trata frameworks de DL e GPUs; não avalia Solver do Excel nem corrige erro de sinal em fórmula de planilha. A contagem de projetos no resumo foi limitada pelo trecho recuperado — usar apenas como contexto, sem detalhar números.

**Papel argumentativo.** Demonstrar que reprodutibilidade já é agenda consolidada em DL, porém em ecossistema distinto; reforça que a lacuna é **específica** de planilhas, não generalizada.

---

## F07 — EXACT: compreensão de planilhas VBA (incluída)

| Campo | Valor |
|---|---|
| Título | EXACT: A tool for comprehending VBA-based Excel spreadsheet applications |
| Ano / periódico | 2016 / Software and Systems Modeling (periódico inferido do DOI `10.1002/smr.*`; conferir na M6) |
| Identificadores | DOI `10.1002/smr.1787`; OpenAlex `W2360792190` |
| Tipo / desenho | Ferramenta de engenharia reversa; extração de elementos, funcionalidades de interface e dependências entre células; validação descrita no resumo, detalhes além do trecho recuperado `[A CONFIRMAR]` |
| URL de auditoria | OpenAlex `works/doi:10.1002/smr.1787` |

**Achado.** Aplicações em planilhas são desenvolvidas por usuários finais sem formação específica em engenharia de software, crescem ao longo do tempo, são mal documentadas e não separam dados, lógica de negócio e interface. A ferramenta extrai informações dos elementos da aplicação, da funcionalidade exposta pela interface e das dependências entre células, apresentando-as em visualizações interativas.

**Limitação de uso.** Foco em **compreensão/reverse engineering**, não emissão de gate de auditoria com critérios de passagem, nem reparo preservando o pacote OOXML. É o trabalho mais próximo localizado; a distinção deve ser explicitada para não parecer apropriação indevida.

**Papel argumentativo.** Reconhecer o estado da arte em compreensão de planilhas VBA e demarcar a contribuição original: auditoria determinística com reparo não destrutivo aplicada a RNA.

---

## F08 — Revisão da taxonomia Panko-Halverson (incluída)

| Campo | Valor |
|---|---|
| Título | Revisiting the Panko-Halverson Taxonomy of Spreadsheet Errors |
| Ano /periódico | 2008 / arXiv (preprint) |
| Identificadores | DOI `10.48550/arxiv.0809.3613`; OpenAlex `W2952265384` |
| Tipo / desenho | Trabalho teórico de revisão de taxonomia |
| URL de auditoria | OpenAlex `works/doi:10.48550/arxiv.0809.3613` (acesso direto ao arXiv bloqueado por `robots.txt`) |

**Achado.** A taxonomia Panko-Halverson é amplamente usada, mas sua forma original é pouco disponível; usuários frequentemente a confundem com extratos simplificados. Muitos empregam apenas uma fração das categorias, em especial a **dimensão de ciclo de vida**. A taxonomia, originada de erros conhecidos em meados dos anos 1990, precisa ser estendida e a categoria de omissão é estreita demais.

**Limitação de uso.** Taxonomia geral de erros de planilha, não específica de RNA; é preprint. Não deve ser a única base da taxonomia do artigo sem contraste com F09 e F11.

**Papel argumentativo.** Base teórica para classificar as falhas encontradas (sinal de ativação, rótulo de métrica, escala, resíduos de template, `#REF!`, p-code) e para argumentar que a dimensão de ciclo de vida — antes da correção, depois do reparo — foi decisiva neste caso.

---

## F09 — Risco de planilhas em pesquisa científica (incluída)

| Campo | Valor |
|---|---|
| Título | A Pilot Study Exploring Spreadsheet Risk in Scientific Research |
| Ano / periódico | 2017 / arXiv (preprint) |
| Identificadores | DOI `10.48550/arxiv.1703.09785`; OpenAlex `W4299809739` |
| Tipo / desenho | Estudo de caso qualitativo em centro de neurociência no Reino Unido; 17 questionários e duas entrevistas semiestruturadas |
| URL de auditoria | OpenAlex `works/doi:10.48550/arxiv.1703.09785` |

**Achado.** O uso de planilhas em neurociência e em outras disciplinas médicas é pouco relatado na pesquisa sobre planilhas. Erros em dados de pesquisa podem causar impactos severos, como ciência enganosa e danos à reputação pessoal e institucional. Falta de projeto adequado e de treinamento aparecem como fatores de risco.

**Limitação de uso.** Evidência qualitativa de um único centro; não quantifica erros em RNA nem avalia workbooks. Não autoriza generalização de prevalência.

**Papel argumentativo.** Sustentar a relevância do tema em contexto de saúde e pesquisa, mantendo o limite: o risco é plausível e relatado, mas não quantificado neste estudo.

---

## F10 — Comportamento de detecção e correção de erros (incluída)

| Campo | Valor |
|---|---|
| Título | An Empirical Study of End-User Behaviour in Spreadsheet Error Detection & Correction |
| Ano / periódico | 2008 / arXiv (preprint) |
| Identificadores | DOI `10.48550/arxiv.0802.3479`; OpenAlex `W4394644826` |
| Tipo / desenho | Experimento com 13 profissionais da indústria e 34 estudantes de contabilidade/finanças; plug-in VBA registrou seleção e alteração de células |
| URL de auditoria | OpenAlex `works/doi:10.48550/arxiv.0802.3479` |

**Achado.** Profissionais superaram estudantes na correção de certos tipos de erro. A análise do tempo por célula mostrou forte correlação entre a porcentagem de células inspecionadas e o número de erros corrigidos.

**Limitação de uso.** Estuda comportamento humano de depuração em planilhas financeiras/contábeis; não propõe gate automatizado nem trata RNAs.

**Papel argumentativo.** Posicionar a inspeção determinística como **complemento** da inspeção humana: reduzir aquilo que depende de sorte, tempo ou experiência do revisor.

---

## F11 — Detecção estática de erros por unidades (incluída)

| Campo | Valor |
|---|---|
| Título | A type system for statically detecting spreadsheet errors |
| Ano / periódico | 2004 / conferência IEEE (índice OpenAlex) |
| Identificadores | DOI `10.1109/ase.2003.1240305`; OpenAlex `W2097864578` |
| Tipo / desenho | Proposta de sistema de tipos; implementação para Microsoft Excel executada em exemplos práticos |
| URL de auditoria | OpenAlex `works/doi:10.1109/ase.2003.1240305` |

**Achado.** O método usa unidades como elementos básicos de verificação, define cabeçalhos e relações `is-a` e `has-a`, atribui unidades às células por regras e detecta erros verificando se cada célula possui unidade bem formada. Os autores relatam ter executado o sistema em exemplos práticos e encontrado erros em planilhas publicadas.

**Limitação de uso.** Detecta erros de **unidade**, não erro de sinal em ativação, rótulo de métrica ou p-code obsoleto. Não propõe reparo com preservação de gráficos, mídia e tabelas.

**Papel argumentativo.** Precedente de detecção estática em planilhas; permite afirmar que a ideia de verificar planilhas sem executá-las não é nova, enquanto o alvo (pipeline de RNA) e o reparo não destrutivo permanecem inexplorados nas buscas.

---

## F12 — Simulação de RNA em planilha (incluída)

| Campo | Valor |
|---|---|
| Título | Spreadsheet simulation of artificial neural network |
| Ano / periódico | DOI contém `1991`; OpenAlex registra `2002` — ano exato `[A CONFIRMAR]` |
| Identificadores | DOI `10.1109/IJCNN.1991.155504`; OpenAlex `W2169734716` |
| Tipo / desenho | Resumo apenas ("summary form only given") em conferência IJCNN |
| URL de auditoria | OpenAlex `works/doi:10.1109/IJCNN.1991.155504` |

**Achado.** Foi desenvolvido um método muito simples de simular redes neurais por meio de planilhas comuns. Planilhas são apresentadas como ferramenta útil e simples para prototipagem, estudo e simulação de redes neurais.

**Limitação de uso.** Resumo extremamente curto; sem detalhes de método, sem auditoria e sem reparo. A divergência de ano entre bases impede usar a data como marco cronológico preciso.

**Papel argumentativo.** Evidenciar que RNA em planilha é prática antiga e reconhecida, o que torna relevante a ausência de protocolos de auditoria específicos para esse ambiente.

---

## F13 — Auditing and Controlling AI Agent Actions in Spreadsheets (excluída — limítrofe)

| Campo | Valor |
|---|---|
| Título | Auditing and Controlling AI Agent Actions in Spreadsheets |
| Ano / periódico | 2026 / arXiv (preprint) |
| Identificadores | DOI `10.48550/arxiv.2604.20070`; OpenAlex `W7155369730` |
| Tipo / desenho | Sistema (Pista); estudo formativo com N=8 e estudo posterior informado no resumo |
| URL de auditoria | OpenAlex `works/doi:10.48550/arxiv.2604.20070` |

**Achado.** Agentes de IA realizam trabalho complexo em múltiplas etapas, mas o processo permanece inacessível durante a execução; em planilhas, processo e artefato são inseparáveis, pois cada decisão fica registrada em células. O sistema Pista decompõe a execução em ações auditáveis e controláveis, permitindo visibilidade e intervenção em cada etapa.

**Motivo da exclusão.** Auditoria de **ações de agente em tempo de execução**, não inspeção determinística de OOXML/VBA, não detecção de erro de ativação em RNA e não reparo de artefato com preservação de pacote. É o trabalho mais próximo encontrado na busca por "spreadsheet neural network audit"; registrá-lo evita afirmar que nada relacionado existe.

**Uso permitido.** Citação na discussão como trabalho relacionado e delimitação explícita da diferença de escopo. Não pode ser usado para negar a lacuna nem para preenchê-la.

---

## F14 — ADAPT it! (excluída — fora de escopo)

| Campo | Valor |
|---|---|
| Título | ADAPT it! Automating APT Campaign and Group Attribution by Leveraging and Linking Heterogeneous Files |
| Ano / periódico | 2024 / conferência ACM |
| Identificadores | DOI `10.1145/3678890.3678909`; OpenAlex `W4402957761` |
| Tipo / desenho | Ferramenta de atribuição de campanhas de ameaças persistentes avançadas |
| URL de auditoria | OpenAlex `works/doi:10.1145/3678890.3678909` |

**Achado.** Trata do aumento de ameaças APT e da dificuldade de correlacionar inteligência de ameaças fragmentada para atribuição de campanhas e grupos.

**Motivo da exclusão.** Nenhuma relação com planilhas de RNA, auditoria de fórmulas ou reparo de artefato. Apareceu como **único** resultado da consulta `audit spreadsheet neural network VBA OOXML` — o que é indício limitado da lacuna, não prova dela.

**Uso permitido.** Registro no protocolo como resultado excluído; não deve ser citado no corpo do artigo.

---

## Quadro-síntese das fontes incluídas

| ID | Eixo | Identificador | Ano | Função no argumento |
|---|---|---|---|---|
| F01 | E1 | `10.1136/bmj-2023-078378` | 2024 | Transparência e relato de modelos com ML |
| F02 | E1 | `10.1186/s12916-014-0241-z` | 2015 | Contexto histórico da transparência |
| F03 | E1 | `10.7326/M18-1376` | 2019 | Falha de análise distorce desempenho |
| F04 | E1 | `10.1016/j.jclinepi.2025.112118` | 2026 | Uniformidade de critérios de avaliação |
| F05 | E2 | `10.1038/s41598-020-69920-0` | 2020 | Variabilidade e descrição do framework |
| F06 | E2 | `10.1145/3510003.3510163` | 2022 | Reprodutibilidade em DL, outro ecossistema |
| F07 | E3 | `10.1002/smr.1787` | 2016 | Compreensão de planilhas VBA — mais próxima |
| F08 | E3 | `10.48550/arxiv.0809.3613` | 2008 | Taxonomia de erros de planilha |
| F09 | E3 | `10.48550/arxiv.1703.09785` | 2017 | Risco em pesquisa científica |
| F10 | E3 | `10.48550/arxiv.0802.3479` | 2008 | Inspeção humana e limites da detecção |
| F11 | E3 | `10.1109/ase.2003.1240305` | 2004 | Detecção estática de erros |
| F12 | E4 | `10.1109/IJCNN.1991.155504` | `[A CONFIRMAR]` | RNA em planilha é prática antiga |

**Total incluído:** 12 fontes, todas com identificador persistente verificado em API pública.
