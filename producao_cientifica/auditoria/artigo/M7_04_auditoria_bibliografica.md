# Auditoria final 4 — Bibliografia, citações e ABNT

Nota metodológica: a delegação a agente especializado falhou antes da execução por restrição regional do modelo OpenCode Go. Não houve auditoria bibliográfica externa; o trabalho abaixo foi executado localmente a partir da evidência já coletada nos marcos M2, M5 e M6. Nenhuma fonte foi relida na íntegra neste marco e nenhum DOI foi acrescentado.

| Fonte | Veredito | Evidência |
|---|---|---|
| F01 Collins et al., 2024 — TRIPOD+AI | citada e listada; DOI verificado no Crossref | `10.1136/bmj-2023-078378`; BMJ, v. 385, p. e078378; forma no corpo `(COLLINS et al., 2024)` |
| F02 Collins et al., 2015 — TRIPOD | citada e listada; DOI verificado no Crossref | `10.1186/s12916-014-0241-z`; BMC Medicine, v. 13, n. 1, p. 1; `(COLLINS et al., 2015)` |
| F03 Wolff et al., 2019 — PROBAST | citada e listada; DOI verificado no Crossref | `10.7326/M18-1376`; Annals of Internal Medicine, v. 170, n. 1, p. 51-58; `(WOLFF et al., 2019)` |
| F04 De Kanter et al., 2026 — aderência TRIPOD+AI | citada e listada; DOI verificado no Crossref | `10.1016/j.jclinepi.2025.112118`; Journal of Clinical Epidemiology, v. 191, p. 112118; `(DE KANTER et al., 2026)` |
| F05 Renard et al., 2020 — variabilidade em segmentação | citada e listada; DOI verificado no Crossref | `10.1038/s41598-020-69920-0`; Scientific Reports, v. 10, n. 1; página/número do artigo com `[A CONFIRMAR]`; `Renard et al. (2020)` |
| F06 Chen et al., 2022 — reprodutibilidade | citada e listada; DOI verificado no Crossref | `10.1145/3510003.3510163`; ICSE 2022, p. 2202-2214; local e editora com `[A CONFIRMAR]`; `Chen et al. (2022)` |
| F07 Amalfitano et al., 2016 — EXACT | citada e listada; DOI verificado no Crossref | `10.1002/smr.1787`; Journal of Software: Evolution and Process, v. 28, n. 6, p. 483-505; `(AMALFITANO et al., 2016)` |
| F08 Panko, 2008 — taxonomia | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.0809.3613`; arXiv, 2008; versão do preprint com `[A CONFIRMAR]`; `(PANKO, 2008)` |
| F09 AlTarawneh e Thorne, 2017 | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.1703.09785`; arXiv, 2017; versão com `[A CONFIRMAR]`; `AlTarawneh e Thorne (2017)` |
| F10 Bishop e McDaid, 2008 | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.0802.3479`; arXiv, 2008; versão com `[A CONFIRMAR]`; `(BISHOP; MCDAID, 2008)` |
| F11 Ahmad et al. — sistema de tipos | citada e listada; DOI verificado no Crossref | `10.1109/ASE.2003.1240305`; ASE 2003, p. 174-183; ano 2004 mantido no corpo com `[A CONFIRMAR]`, DOI/Crossref indicam 2003; `Ahmad et al. (2004)` |
| F12 Antonini — simulação de RNA em planilha | citada e listada; DOI verificado no Crossref | `10.1109/IJCNN.1991.155504`; IJCNN-91, v. II, p. 910; ano 2002 mantido com `[A CONFIRMAR]`, DOI contém 1991, Crossref sem ano; `(ANTONINI, 2002)` |
| F13 Sabouri et al., 2026 — auditoria de agentes | citada e listada; via suplementar OpenAlex | `10.48550/arXiv.2604.20070`; arXiv, 2026; versão com `[A CONFIRMAR]`; `(SABOURI et al., 2026)` |

## Correspondência citação ↔ referência

Foram contadas **13 fontes citadas no corpo** e **13 entradas na lista de referências**. Não foi detectada fonte citada sem entrada, nem entrada sem citação no corpo. O DOI `10.1145/3678890.3678909` (F14), embora identificada na busca, permanece fora do corpo e fora da lista, conforme decisão registrada no marco M5. As duas formas de citação autor-ano previstas pela NBR 10520 — `(SOBRENOME, ano)` e `Sobrenome et al. (ano)` — ocorrem no manuscrito e foram ambas aceitas pelo gate M6.

## Divergências de ano

- **F11 (Ahmad).** O corpo e o rascunho M5 registram 2004; o DOI contém `2003` e o Crossref não trouxe ano divergente que sustente 2004. A marcação `[A CONFIRMAR ANO; CROSSREF E DOI INDICAM 2003]` foi mantida na lista. Não houve alteração silenciosa do ano citado no corpo, porque a fonte primária não foi lida na íntegra.
- **F12 (Antonini).** O DOI contém `1991`, o Crossref não informou ano e o OpenAlex registrou `2002`. A marcação `[A CONFIRMAR ANO; DOI CONTÉM 1991; CROSSREF NÃO INFORMA ANO]` foi mantida. A escolha de 2002 no corpo é provisória e explícita.

Em ambos os casos, a decisão foi preservar a divergência e sinalizá-la, não resolver por semelhança de metadados.

## Conformidade ABNT observada

A conferência cobriu a NBR 6023 (referências alfabéticas pelo primeiro autor, com DOI quando disponível) e a NBR 10520 (citações no sistema autor-ano). A NBR 14724 depende de diagramação final e foi registrada nas notas do apêndice C. Foram observadas 13 entradas com DOI, ordem alfabética e ausência de DOI inventado. A pendência de versão dos quatro preprints e de páginas de F05 impede declarar conformidade completa de metadados. Papel, margens, fonte, espaçamento e paginação permanecem `[A CONFIRMAR PELO PERIÓDICO]`.

## Limites

O texto integral das fontes F01–F13 ainda não foi conferido; a auditoria apoiou-se em resumos, metadados de APIs públicas e auditoria por DOI. A triagem não foi cega e não houve revisão bibliográfica externa independente. Nenhuma promessa editorial, Qualis, nota ou aceite é feita.
