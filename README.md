# Redes_Neurais_TEA

Auditoria metodológica determinística de um pipeline de rede neural artificial hospedado em planilha `.xlsm`, com foco em integridade estrutural, procedência de métricas em cache, reparo em cópia preservando o original e separação entre diagnóstico de cache e resultado validado.

**Status:** auditoria documental local concluída; sem revisão externa, sem reexecução do Solver, sem integração das 30 imagens e sem alegação de desempenho clínico, Qualis, nota ou aceite editorial.

## Conteúdo

- `producao_cientifica/Redes Neurais - TEA Dataset VBA.xlsm` — **não incluído neste repositório** (excede o limite de 100 MB do GitHub; ver abaixo).
- `producao_cientifica/auditoria/Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm` — cópia corrigida, com aba documental `AUDITORIA_M7`.
- `producao_cientifica/auditoria/backup/Redes_Neurais_TEA_Dataset_VBA_corrigido.pre_r1291.xlsm` — estado anterior à inserção da aba, preservado para auditoria.
- `producao_cientifica/auditoria/` — scripts de auditoria, reparo, gates e relatórios.
- `producao_cientifica/auditoria/artigo/` — manuscrito modular IMRAD/ABNT, auditorias M7 e exploração estatística separada.
- `producao_cientifica/auditoria/artigo/exploracao/` — análise exploratória determinística do cache (semente `20261122`).
- `documentacao/specs/` — especificações formais `SPEC-935-R1282` e `SPEC-935-R1291`.

## Cadeia de integridade (SHA-256)

| Artefato | SHA-256 |
|---|---|
| Original (fora do repositório) | `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd` |
| Cópia corrigida pré-R1291 | `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` |
| Cópia corrigida atual | `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb` |

O arquivo original tem 106.971.375 bytes, acima do limite de 100 MiB por arquivo do GitHub; a compressão não reduz abaixo do limite. Ele permanece disponível localmente e deve ser obtido sob demanda do autor, conferindo sempre o hash acima. Os dois workbooks incluídos têm menos de 100 MiB e foram preservados byte a byte.

## Resultados dos gates locais

| Gate | Resultado |
|---|---|
| Auditoria do original | 10/10 |
| Correção aplicada | 22/22 |
| M0/M1 | 14/14 |
| M2 | 23/23 |
| M3 | 20/20 |
| M4 | 22/22 |
| M5 | 24/24 |
| M6 | 33/33 |
| M7 | 24/24 |
| R1291 | 16/16 |

O gate `verificar_r1291.py` reexecuta os nove anteriores e exige que nenhum produza `FAIL`.

## Como reproduzir

A partir da raiz deste repositório, com Python 3.12 e as dependências `openpyxl`, `olefile` e `oletools`:

```bash
python3 producao_cientifica/auditoria/verificar_auditoria.py
python3 producao_cientifica/auditoria/verificar_correcao.py
python3 producao_cientifica/auditoria/artigo/verificar_m0_m1.py
python3 producao_cientifica/auditoria/artigo/verificar_m2.py
python3 producao_cientifica/auditoria/artigo/verificar_m3.py
python3 producao_cientifica/auditoria/artigo/verificar_m4.py
python3 producao_cientifica/auditoria/artigo/verificar_m5.py
python3 producao_cientifica/auditoria/artigo/verificar_m6.py
python3 producao_cientifica/auditoria/artigo/verificar_m7.py
python3 producao_cientifica/auditoria/artigo/verificar_r1291.py
```

Para regenerar a exploração estatística, determinística:

```bash
python3 producao_cientifica/auditoria/artigo/exploracao/analise_exploratoria.py
```

Os relatórios consolidados são `RELATORIO_M7.md` e `RELATORIO_R1291.md`, em `producao_cientifica/auditoria/artigo/`.

## Limites e pendências

- O Solver não foi reexecutado: faltam versão do Excel/Solver, data, status de convergência, seed, arquivo salvo e pesos finais com hash.
- As 30 imagens não foram integradas: faltam proveniência, natureza, consentimento, anonimização, licença e referência-padrão.
- A edição da fórmula textual do intervalo de confiança (Onda 3) não foi autorizada e não foi executada; a divergência entre o intervalo em cache e a fórmula textual permanece sem causa resolvida.
- As métricas em cache (acurácias de 0,6333 a 0,9000, n=30 por aba) são diagnóstico do estado original. Nenhuma acurácia validada do modelo corrigido é afirmada.
- A exploração separada usa apenas as matrizes de confusão do cache; como não há escores individuais, nenhum limiar de probabilidade foi inventado. Bootstrap e perturbação de rótulo são hipóteses diagnósticas, não inferência populacional.
- Periódico-alvo, instituição, autoria, financiamento, conflitos, prazo, local de depósito, abstract e parâmetros de diagramação permanecem `[A CONFIRMAR]`.
- O texto integral das fontes F01–F13 não foi conferido; M2/M5/M6 usaram resumos, metadados e auditoria por DOI.
- A banca simulada em M7 é heurística local, não revisão por pares.

## Licença

`[A CONFIRMAR]`
