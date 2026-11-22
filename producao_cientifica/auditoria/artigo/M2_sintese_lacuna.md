# M2 — Síntese da lacuna e decisão argumentativa

**Artefato:** rascunho para aprovação
**Protocolo:** `M2_protocolo_busca.md` · **Fichas:** `M2_fichas_auditoria.md`
**Busca:** 21 de novembro de 2026 · consolidação: 22 de novembro de 2026

## 1. Formulação estrita da lacuna

Nas buscas realizadas em 21/11/2026 nas vias Crossref, PubMed, OpenAlex e Europe PMC, com as strings e contagens registradas no protocolo, **não foi localizado nenhum trabalho que proponha e execute, em um pipeline de RNA hospedado em planilha `.xlsm`, um protocolo determinístico que simultaneamente**:

1. inspecione diretamente o pacote OOXML e os streams VBA/OLE;
2. detecte falhas de implementação como sinal incorreto de ativação, rótulo de métrica inconsistente com a fórmula, escala indevida e resíduos de template/`#REF!`;
3. repare essas falhas em **cópia**, preservando contagens de planilhas, gráficos, desenhos, mídia e tabelas;
4. impeça que valores em cache gerados antes do reparo sejam reportados como desempenho do modelo corrigido.

**Limite obrigatório de redação:** essa ausência é **circunscrita ao escopo pesquisado**. Não constitui prova de inexistência universal e não deve ser escrita como "a literatura não possui" ou "não existe trabalho algum". A forma correta é "não foi localizado nas buscas realizadas".

## 2. Evidência que sustenta a afirmação limitada

| Evidência | Valor observado | Interpretação permitida |
|---|---|---|
| Consulta OpenAlex `audit spreadsheet neural network VBA OOXML` | 1 resultado: ADAPT it! (cibersegurança) | A consulta mais específica não retornou trabalho de auditoria de planilha de RNA |
| Consulta OpenAlex `OOXML VBA audit machine learning` | 3 resultados, nenhum sobre RNA | Reforça a ausência no recorte OOXML/VBA |
| Consulta OpenAlex `spreadsheet neural network audit` | 4.997 resultados; mais próximo: Pista (2026) | Pista audita ações de agente em tempo de execução, não o artefato |
| Consulta OpenAlex `spreadsheet Leaky ReLU` | 72 resultados, nenhum sobre auditoria de ativação em planilha | O erro específico do caso não aparece como tema de auditoria |
| F07 (EXACT, 2016) | Compreende planilhas VBA e dependências entre células | É o trabalho mais próximo em compreensão, mas não emite gate nem repara preservando o pacote |
| F11 (Ahmad et al., 2004) | Detecção estática de erros de unidade em planilhas | Precedente de verificação estática, com alvo diferente do erro de ativação |
| F12 (RNA em planilha) | Resumo que descreve planilhas como ferramenta simples para simular RNAs | Mostra que o ambiente é antigo; não há auditoria associada no resumo |
| F05, F06 | Reprodutibilidade e variabilidade em DL | Agenda consolidada em outros ecossistemas, não no Excel/Solver |

## 3. Por que as fontes próximas não preenchem a lacuna

| Fonte | O que faz | O que não faz |
|---|---|---|
| F01–F04 (TRIPOD, TRIPOD+AI, PROBAST, aderência) | Definem o que deve ser **relatado** e como julgar relato/risco de viés | Não inspecionam artefato computacional; não leem fórmulas, VBA ou cache |
| F05–F06 (reprodutibilidade em DL) | Tratam variabilidade, aleatoriedade de software e hardware | Não cobrem Solver do Excel, planilhas ou reparo não destrutivo |
| F07 (EXACT) | Compreende aplicações VBA e dependências entre células | Não propõe critérios de passagem, não detecta erro de sinal em ativação, não repara preservando OOXML |
| F11 (sistema de tipos) | Detecta erro de unidade estaticamente | Não trata ativação, rótulo de métrica ou integridade de pacote |
| F13 (Pista) | Torna ações de agente auditáveis e controláveis em planilhas durante a execução | Não inspeciona OOXML/VBA, não lida com RNA em planilha, não repara artefato |
| F12 (1991/2002) | Demonstra simulação de RNA em planilha | Resumo apenas; sem método de auditoria |

## 4. Contribuição decorrente — formulação defensável

A contribuição do manuscrito não é "o primeiro protocolo de auditoria de planilhas" nem "uma solução para ciência enganosa". É mais estreita e verificável:

> **A partir de um workbook real, este estudo deriva e aplica um protocolo determinístico de auditoria e reparo para um pipeline de RNA em planilha, demonstrando que (i) falhas de implementação são detectáveis por inspeção do pacote, (ii) o reparo pode preservar a estrutura do artefato e (iii) métricas em cache exigem rotulagem de proveniência para não serem confundidas com resultado validado. Nas buscas realizadas, não foi localizado trabalho que combine esses três elementos nesse ambiente.**

Essa redação é compatível com o desenho de auditoria técnica definido em M0 e com as proposições P1–P4 de M1. Não depende de reexecução do Solver nem das 30 imagens; estas pertencem a M4 e servirão para demonstrar o antes/depois, não para substituir a contribuição metodológica.

## 5. Ajustes ao marco M1

- O campo "Lacuna" de M1 permanecia como `[A DEMONSTRAR EM M2]`. Com esta síntese, ele passa a estar **demonstrado nos termos do escopo pesquisado**. A redação final deve manter o limite indicado na seção 1.
- A pergunta central fixada em M0 não precisa ser alterada; M2 apenas dá suporte à sua relevância.
- Nenhuma referência bibliográfica foi inserida em M0/M1; as fichas F01–F12 são o conjunto candidato a compor o referencial de M5, sujeito a conferência final de ABNT em M6.

## 6. O que M2 **não** estabeleceu

1. Não prova que a lacuna seja universal.
2. Não avaliou o texto integral das 12 fontes incluídas; usou resumos e metadados.
3. Não executou revisão sistemática, dupla triagem ou avaliação formal de qualidade.
4. Não consultou bases indexadoras adicionais (Scopus, Web of Science, IEEE Xplore, SciELO, CAPES/Periódicos).
5. Não validou a taxonomia do workbook contra a taxonomia Panko-Halverson completa — apenas identificou F08 como base teórica.
6. Não resolveu o ano exato de F12 (`[A CONFIRMAR]`).
7. Não alterou nenhuma conclusão sobre desempenho do modelo; o cache continua classificado como diagnóstico do estado original.

## 7. Recomendação de decisão

Avançar para **M3 — projeto metodológico e ética**, com as seguintes entradas já fixadas:

- lacuna formulada com o limite "nas buscas realizadas";
- F01–F04 para o arcabouço de relato e risco de viés;
- F05–F06 para reprodutibilidade e variabilidade;
- F07–F11 para taxonomia, compreensão e detecção estática em planilhas;
- F12 como contexto histórico;
- F13 na discussão como trabalho limítrofe; F14 fora do corpo;
- pendências `[A CONFIRMAR]` preservadas.
