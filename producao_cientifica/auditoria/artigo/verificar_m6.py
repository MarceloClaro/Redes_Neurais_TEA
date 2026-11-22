"""Gate SDD/TDD do marco M6 — formatacao ABNT e auditoria de referencias.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m6.py

Somente leitura. Confere que a versao ABNT e geravel de forma deterministica,
que as NBRs foram conferidas, que os 13 DOIs foram auditados sem invencao e
que nenhuma alegação, pendencia ou limite foi suprimido na formatacao.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import montar_m6  # noqa: E402

AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))
MANUSCRITO = os.path.join(HERE, "MANUSCRITO_ABNT.md")
RASCUNHO = os.path.join(HERE, "MANUSCRITO_rascunho.md")
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
GATE_M5 = os.path.join(HERE, "verificar_m5.py")
GERADOR = os.path.join(HERE, "montar_m6.py")
CORRIGIDO = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
JSON_M4 = os.path.join(HERE, "M4_metricas_cache.json")

DOIS_APROVADOS = {
    "10.1136/bmj-2023-078378",
    "10.1186/s12916-014-0241-z",
    "10.7326/m18-1376",
    "10.1016/j.jclinepi.2025.112118",
    "10.1038/s41598-020-69920-0",
    "10.1145/3510003.3510163",
    "10.1002/smr.1787",
    "10.48550/arxiv.0809.3613",
    "10.48550/arxiv.1703.09785",
    "10.48550/arxiv.0802.3479",
    "10.1109/ase.2003.1240305",
    "10.1109/ijcnn.1991.155504",
    "10.48550/arxiv.2604.20070",
}

CITACOES = [
    (("collins et al., 2024",),),
    (("collins et al., 2015",),),
    (("wolff et al., 2019",),),
    (("de kanter et al., 2026",),),
    (("renard et al., 2020",), ("renard et al. (2020)",)),
    (("chen et al., 2022",), ("chen et al. (2022)",)),
    (("amalfitano et al., 2016",),),
    (("panko, 2008",), ("panko (2008)",)),
    (("altarawneh",),),
    (("mcdaid",),),
    (("ahmad et al., 2004",), ("ahmad et al. (2004)",)),
    (("antonini, 2002",), ("antonini (2002)",)),
    (("sabouri et al., 2026",),),
]
SOBRENOMES = [
    "collins, g. s. et al", "wolff, r. f. et al", "de kanter, e. et al",
    "renard, f. et al", "chen, b. et al", "amalfitano, d. et al",
    "panko, r. r", "altarawneh, g", "bishop, b", "ahmad, y. et al",
    "antonini, r", "sabouri, s. et al",
]

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


artefatos = [MANUSCRITO, RASCUNHO, SPEC, GATE_M5, GERADOR, CORRIGIDO, JSON_M4]
artefatos += [os.path.join(HERE, m) for m in montar_m6.TODOS]
missing = [p for p in artefatos if not os.path.exists(p)]
check("G-01 artefatos M6 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

manuscrito = read(MANUSCRITO)
modulos = {m: read(os.path.join(HERE, m)) for m in montar_m6.TODOS}
corpo = "\n".join(
    montar_m6.transformar_corpo(modulos[m]) for m in montar_m6.CORPO_M5
)
ref_abnt = modulos["M6_01_referencias_abnt.md"]
aud_ref = modulos["M6_02_auditoria_referencias.md"]
aud_aleg = modulos["M6_03_auditoria_alegacoes.md"]
notas = modulos["M6_04_notas_abnt.md"]

# G-02/G-03 determinismo
esperado = montar_m6.CABECALHO
for indice, modulo in enumerate(montar_m6.TODOS):
    conteudo = modulos[modulo]
    if indice < len(montar_m6.CORPO_M5):
        conteudo = montar_m6.transformar_corpo(conteudo)
    esperado += conteudo.rstrip() + "\n"
    esperado += "\n---\n\n"
esperado = esperado.rstrip() + "\n"
check("G-02 consolidado ABNT gerado de forma deterministica", manuscrito == esperado)
check("G-03 ordem dos modulos fixa",
      montar_m6.TODOS == montar_m6.CORPO_M5 + montar_m6.POS_TEXTUAIS)

# G-04 estrutura
secoes = [
    "# Auditoria metodológica de um pipeline", "# Resumo", "# Abstract",
    "# 1 Introdução", "# 2 Materiais e métodos", "# 3 Resultados",
    "# 4 Discussão", "# 5 Conclusão", "# Referências", "# Declarações",
    "# Apêndice A — Auditoria de referências e citações",
    "# Apêndice B — Triagem de força de alegação",
    "# Apêndice C — Notas de formatação ABNT",
]
check("G-04 estrutura ABNT completa", all(s in manuscrito for s in secoes))
posicoes = [manuscrito.index(s) for s in secoes]
check("G-05 elementos pos-textuais na ordem", posicoes == sorted(posicoes))

# G-06 notas de formato
check("G-06 NBRs 14724/6023/10520 conferidas",
      all(n in notas for n in ("NBR 14724", "NBR 6023", "NBR 10520")))
check("G-07 parametros de diagramacao explicitados",
      all(n in notas for n in ("A4", "12 pt", "1,5", "4 cm", "justificado",
                               "canto superior direito")))
check("G-08 parametros dependentes do periodico marcados",
      notas.count("[A CONFIRMAR PELO PERIÓDICO]") >= 4)

# G-09 tabela ABNT
check("G-09 tabela 1 titulada com fonte",
      "**Tabela 1 — Métricas recomputadas" in manuscrito and
      "Fonte: elaborado pelos autores a partir de `M4_metricas_cache.json`" in manuscrito)

# G-10..G-12 DOIs e referencias
norm = manuscrito.lower().replace("**", "").replace("`", "")
dois = set()
for bruto in re.findall(r"10\.\d{4,9}/\S+", norm):
    dois.add(bruto.rstrip(";,.)\""))
invalidos = sorted(dois - DOIS_APROVADOS)
check("G-10 nenhum DOI inventado na versao ABNT", not invalidos, ", ".join(invalidos))
check("G-11 treze DOIs mantidos", len(dois) == 13, str(len(dois)))
check("G-12 toda referencia ABNT com DOI",
      ref_abnt.count("DOI: 10.") == 13 and all(d in ref_abnt.lower() for d in DOIS_APROVADOS))
check("G-13 metadados primarios aparecem nas referencias",
      all(s in ref_abnt for s in ("v. 385", "p. e078378", "p. 51-58",
                                  "v. 28, n. 6", "v. 191")))

# G-14 auditoria de fontes
check("G-14 nove DOIs verificados no Crossref",
      aud_ref.count("VERIFICADA") >= 9, str(aud_ref.count("VERIFICADA")))
check("G-15 quatro preprints com via suplementar registrada",
      aud_ref.count("Crossref HTTPError") >= 4 and "OpenAlex" in aud_ref)
check("G-16 divergencias de F11 e F12 preservadas",
      "1991/2002" in aud_ref and "2003" in aud_ref and
      "CROSSREF E DOI INDICAM 2003" in ref_abnt and
      "DOI CONTÉM 1991" in ref_abnt)
check("G-17 conferencia citação ↔ referência registrada",
      "13 fontes incluídas aparecem no corpo e na lista" in aud_ref)

# G-18 cada citacao do corpo e cada sobrenome da lista
corpo_low = corpo.lower()
refs_low = ref_abnt.lower()
ausentes = []
for indice, alternativas in enumerate(CITACOES, start=1):
    if not any(all(s in corpo_low for s in opcao) for opcao in alternativas):
        ausentes.append("F%02d" % indice)
check("G-18 todas as fontes citadas no corpo ABNT", not ausentes, ", ".join(ausentes))
ausentes = [s for s in SOBRENOMES if s not in refs_low]
check("G-19 todas as referencias listadas com autor", not ausentes, ", ".join(ausentes))

# G-20 triagem de alegações
check("G-20 triagem heuristica com escopo e limite",
      "199 frases" in aud_aleg and "10 achados" in aud_aleg and
      "heurística" in aud_aleg and "decisão final abaixo é humana" in aud_aleg)
check("G-21 dez achados com decisao registrada",
      all("A%d |" % i in aud_aleg for i in range(1, 11)) and
      aud_aleg.count("manter") >= 10)
check("G-22 nenhum achado suprimido sem justificativa",
      "Nenhum achado foi removido por conveniência" in aud_aleg and
      "não se conclui" in aud_aleg.lower())

# G-23..G-26 integridade de conteudo
check("G-23 sem promessa editorial",
      not any(p in norm for p in (
          "qualis a1 garantido", "aceite garantido", "nota 10 garantida",
          "aprovado pelo periódico", "este é o primeiro protocolo")))
numeros = [
    "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd",
    "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475",
    "0,6333", "0,7333", "0,8000", "0,9000", "0,743786", "0,965401",
    "0,758863", "0,950323", "30/30", "22/22", "10/10", "1e-12",
]
ausentes = [n for n in numeros if n not in manuscrito]
check("G-24 hashes e numeros auditaveis preservados", not ausentes, ", ".join(ausentes))
check("G-25 Solver e imagens permanecem pendentes",
      "Solver não foi reexecutado" in manuscrito and
      "as 30 imagens não foram integradas" in manuscrito and
      "não há resultado pós-correção neste manuscrito" in norm)
check("G-26 pendencias marcadas",
      len(re.findall(r"\[A CONFIRMAR[^\]]*\]", manuscrito)) >= 14)
check("G-27 declaracoes de financiamento, conflitos e autoria",
      all(k in norm for k in ("financiamento", "conflitos de interesse",
                              "autoria e contribuições", "periódico-alvo")))
check("G-28 abstract segue pendente de exigencia do periodico",
      "[A CONFIRMAR EXIGÊNCIA DE ABSTRACT PELO PERIÓDICO]" in manuscrito and
      "[RASCUNHO —" not in manuscrito and
      "[FORMATO PROVISÓRIO" not in manuscrito)
check("G-29 lacuna circunscrita mantida",
      "não localizou trabalho" in norm and
      "não constitui prova de inexistência universal" in norm)
check("G-30 diretrizes sem conformidade afirmada",
      "não como lista de conformidade" in norm and
      "não foi aplicada" in norm and
      "não se aplicam" in norm)

# G-31 idioma e marcas residuais
cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", manuscrito)))
check("G-31 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
estranhos = re.findall(
    r"\b(?:after|during|however|therefore|summary|toutes|aplikado|herramienta|frameworks)\b",
    corpo_low,
)
check("G-32 sem palavras soltas em outro idioma", not estranhos, ", ".join(estranhos))
check("G-33 gate M5 e spec permanecem rastreaveis",
      "verificar_m5.py` (24/24)" in read(SPEC) and os.path.exists(RASCUNHO))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
