# M2 — Protocolo de busca e auditoria bibliográfica

**Artefato:** rascunho para aprovação
**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Data da busca:** 21 de novembro de 2026 · **consolidação:** 22 de novembro de 2026
**Orquestrador:** marceloclaro
**Natureza:** busca auditada circunscrita. **Não** é revisão sistemática, não aplica PRISMA e não produz metanálise.

## 1. Objetivo da busca

Verificar se já existe trabalho que proponha e execute um protocolo **determinístico** de auditoria de pipelines de rede neural artificial (RNA) hospedados em planilha `.xlsm`, compreendendo:

- inspeção direta de OOXML e de streams VBA/OLE;
- detecção de erro de sinal em função de ativação e de rótulo incorreto de métrica;
- reparo em cópia com preservação de gráficos, desenhos, mídia e tabelas;
- separação explícita entre valor em cache e resultado validado.

A busca também levantou fontes para fundamentar: relato de modelos preditivos/IA em saúde, risco de viés, reprodutibilidade em aprendizado profundo e erros em planilhas científicas.

## 2. Bases e vias de acesso

| Via | Endpoint / serviço | Finalidade | Observação |
|---|---|---|---|
| Crossref REST | `api.crossref.org/works` e `/works/{DOI}` | Resolução de DOI, título, autores, periódico | Consultas por título são muito amplas; usadas apenas para identificação, não como contagem de lacuna |
| PubMed E-utilities | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` e `esummary.fcgi` | Identificação de PMIDs | `TRIPOD+AI statement` → 41 registros |
| OpenAlex API | `api.openalex.org/works` e `/works/doi:{DOI}` | Busca por relevância, contagens, `abstract_inverted_index`, IDs persistentes | Sem chave de API; cota diária compartilhada informada na resposta |
| Europe PMC REST | `ebi.ac.uk/europepmc/webservices/rest/search` | Confirmação cruzada de DOI, PMID, ano e periódico | `resultType=lite` e `core` conforme necessidade |
| arXiv | `export.arxiv.org/api` | Tentativa de acesso direto a resumos | **Bloqueado por `robots.txt`**; resumos obtidos via OpenAlex |

### Limitação operacional registrada

A ferramenta de busca web geral do ambiente retornou **HTTP 402** em todas as tentativas. Por isso, nenhuma afirmação desta seção depende dela. A busca foi executada exclusivamente pelas APIs públicas listadas, com URLs e respostas auditáveis.

## 3. Strings, contagens e triagem

As contagens abaixo são as reportadas pelo OpenAlex em 21/11/2026. Elas são sensíveis à redação da consulta e **não** devem ser lidas como prevalência de literatura.

| # | String (OpenAlex `search=`) | Contagem | Primeiros resultados examinados | Decisão |
|---|---|---:|---|---|
| Q1 | `audit spreadsheet neural network VBA OOXML` | 1 | ADAPT it! (2024) | Excluído: cibersegurança, sem planilha de RNA |
| Q2 | `spreadsheet neural network audit` | 4.997 | "Auditing and Controlling AI Agent Actions in Spreadsheets" (2026) | Limítrofe: registrado como F13, não preenche a lacuna |
| Q3 | `spreadsheet Leaky ReLU` | 72 | Artigos de manutenção preditiva e MLP | Excluídos: uso de ReLU, não auditoria de ativação em planilha |
| Q4 | `OOXML VBA audit machine learning` | 3 | Armazenamento de documentos, ADAPT it!, tese em finlandês | Excluídos |
| Q5 | `spreadsheet formula error machine learning healthcare` | 2.343 | Tutoriais e revisões clínicas | Excluídos: nenhum audita fórmula de planilha de RNA |
| Q6 | `spreadsheet error detection neural network model` | 12.275 | TableSense (detecção de tabelas com CNN), modelagem cognitiva | Excluídos: RNA para detectar tabelas ≠ auditoria de planilha de RNA |
| Q7 | `spreadsheet errors scientific research` | 80.606 | Busca ampla de contexto | Usada apenas para calibrar escopo |
| Q8 | `implementation errors deep learning reproducibility` | 457.448 | Busca ampla de contexto | Usada apenas para calibrar escopo |
| Q9 | `"audit spreadsheet neural network VBA OOXML"` (repetição controlada) | 1 | Mesmo registro de Q1 | Confirma estabilidade da consulta mais específica |

Consultas complementares:

- Crossref `query.title=TRIPOD+AI updated guidance BMJ 2024` → localizou `10.1136/bmj-2023-078378` e `10.1136/bmj.q902`.
- Crossref `query.title=PROBAST risk of bias prediction model Wolff` → localizou `10.7326/M18-1376`.
- PubMed `TRIPOD+AI statement` → 41 registros; os primeiros examinados não eram o artigo-base, que foi confirmado por DOI/PMID.
- Europe PMC com cinco DOIs de diretrizes/estudos → cinco registros confirmados, com PMIDs `38626948`, `25563062`, `30596875`, `32792540` e `41448505`.

## 4. Critérios de triagem

### Inclusão

1. Identificador persistente verificado em pelo menos uma API (DOI, PMID ou OpenAlex ID).
2. Resumo recuperável ou, na ausência dele, título e metadados suficientes para classificar o trabalho.
3. Enquadramento em pelo menos um eixo:
   - **E1** — relato de modelos preditivos e IA em saúde (TRIPOD, TRIPOD+AI, PROBAST, aderência);
   - **E2** — reprodutibilidade e erros de implementação em aprendizado profundo;
   - **E3** — erros, compreensão ou auditoria de planilhas e planilhas VBA;
   - **E4** — RNA em planilhas.

### Exclusão

1. Foco em atribuição de campanhas de ameaças ou segurança ofensiva (F14).
2. Foco exclusivo em supervisão de agentes de IA em tempo de execução, sem inspeção de OOXML/VBA e sem reparo de artefato (F13) — registrado como limítrofe, não incluído como preenchimento da lacuna.
3. Ausência de identificador persistente conferível.
4. Uso do termo "auditoria" em sentido contábil/financeiro sem relação com planilhas de modelagem.

### Resultado da triagem

- **14 registros únicos** examinados.
- **12 incluídos** (F01–F12) com identificador persistente verificado.
- **2 excluídos com justificativa** (F13 limítrofe; F14 fora de escopo).
- Nenhum registro incluído sem DOI, PMID ou OpenAlex ID conferido.

## 5. Auditoria de cada fonte

Para cada fonte incluída foram registrados:

- título, ano e periódico conforme Crossref/OpenAlex, com ano conferido no Europe PMC quando disponível;
- DOI, PMID e/ou OpenAlex ID;
- URL de auditoria efetivamente consultada;
- tipo de fonte e desenho declarado no resumo;
- achado principal **somente** do resumo/metadados observados;
- limitação de uso no presente artigo;
- papel argumentativo.

As fichas encontram-se em `M2_fichas_auditoria.md`. Nenhuma referência foi aceita apenas por aparecer em lista de referências de outro trabalho.

## 6. Limites do protocolo

1. Busca circunscrita a quatro vias públicas; não houve consulta direta a Scopus, Web of Science, IEEE Xplore, SciELO ou CAPES/Periódicos.
2. Sem dupla triagem cega e sem cálculo de concordância entre triadores.
3. Sem instrumento formal de avaliação de qualidade (por exemplo, GRADE ou JBI); a "auditoria" aqui é de proveniência e função argumentativa.
4. Contagens do OpenAlex dependem da string e da cobertura do índice; uma contagem baixa é indício, não prova.
5. Resumos do arXiv foram obtidos por índice terceirizado (OpenAlex), porque o acesso direto foi bloqueado por `robots.txt`.
6. O ano de F12 diverge entre bases (DOI contém `1991`; OpenAlex registra `2002`); marcado como `[A CONFIRMAR]` na ficha.
7. Este protocolo não substitui uma revisão sistemática; a contribuição do artigo é metodológica e não depende de declarar exaustividade.

## 7. Decisão sobre a lacuna

A síntese em `M2_sintese_lacuna.md` afirma **ausência nas buscas realizadas**, não inexistência universal. Essa redação é exigência de integridade e deve ser preservada na redação final.
