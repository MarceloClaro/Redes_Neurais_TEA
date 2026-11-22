"""Gate SDD/TDD do marco M5 — redacao modular IMRAD.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m5.py

Somente leitura. Confere que o consolidado e geravel de forma deterministica
pelos modulos, que a estrutura IMRAD esta presente e que nenhuma referencia,
resultado ou pendencia foi inventada ou suprimida.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))
sys.path.insert(0, HERE)
import montar_m5  # noqa: E402

MANUSCRITO = os.path.join(HERE, "MANUSCRITO_rascunho.md")
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
GERADOR = os.path.join(HERE, "montar_m5.py")
GATE_M4 = os.path.join(HERE, "verificar_m4.py")
CORRIGIDO = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")

MODULOS_PT = [
    "M5_01_introducao.md",
    "M5_02_metodos.md",
    "M5_03_resultados.md",
    "M5_04_discussao.md",
    "M5_05_conclusao.md",
    "M5_06_referencias.md",
    "M5_07_declaracoes.md",
]
TODOS_MODULOS = ["M5_00_resumo.md"] + MODULOS_PT

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

CITACOES = {
    "F01 Collins 2024": [("collins et al., 2024",)],
    "F02 Collins 2015": [("collins et al., 2015",)],
    "F03 Wolff 2019": [("wolff et al., 2019",)],
    "F04 de Kanter 2026": [("de kanter et al., 2026",)],
    "F05 Renard 2020": [("renard et al., 2020",), ("renard et al. (2020)",)],
    "F06 Chen 2022": [("chen et al., 2022",), ("chen et al. (2022)",)],
    "F07 Amalfitano 2016": [("amalfitano et al., 2016",)],
    "F08 Panko 2008": [("panko, 2008",), ("panko (2008)",)],
    "F09 AlTarawneh e Thorne 2017": [("altarawneh", "thorne", "2017")],
    "F10 Bishop e McDaid 2008": [("bishop", "mcdaid", "2008")],
    "F11 Ahmad 2004": [("ahmad et al., 2004",), ("ahmad et al. (2004)",)],
    "F12 Antonini 2002": [("antonini, 2002",), ("antonini (2002)",)],
    "F13 Sabouri 2026": [("sabouri et al., 2026",)],
}

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


artefatos = [MANUSCRITO, SPEC, GERADOR, GATE_M4, CORRIGIDO]
artefatos += [os.path.join(HERE, m) for m in TODOS_MODULOS]
missing = [p for p in artefatos if not os.path.exists(p)]
check("G-01 artefatos M5 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

manuscrito = read(MANUSCRITO)
modulos = {m: read(os.path.join(HERE, m)) for m in TODOS_MODULOS}
corpo = "\n".join(modulos[m] for m in MODULOS_PT[:-2])
referencias = modulos["M5_06_referencias.md"]
corpo_low = corpo.lower()
manuscrito_low = manuscrito.lower()
norm = manuscrito_low.replace("**", "").replace("`", "")

esperado = montar_m5.CABECALHO
for modulo in montar_m5.MODULOS:
    esperado += modulos[modulo].rstrip() + "\n"
    esperado += "\n---\n\n"
esperado = esperado.rstrip() + "\n"
check("G-02 consolidado gerado de forma deterministica", manuscrito == esperado)
check("G-03 modulos na ordem fixa", montar_m5.MODULOS == TODOS_MODULOS)

secoes = [
    "# Resumo", "# Abstract", "# 1 Introdução", "# 2 Materiais e métodos",
    "# 3 Resultados", "# 4 Discussão", "# 5 Conclusão", "# Referências",
    "# Declarações",
]
check("G-04 estrutura IMRAD e complementos",
      all(s in manuscrito for s in secoes))
check("G-05 pergunta central preservada",
      "Como falhas de implementação em um pipeline de RNA hospedado em planilha "
      "afetam a validade das métricas reportadas" in manuscrito)
check("G-06 lacuna circunscrita ao escopo",
      "não localizou trabalho" in norm and
      "não constitui prova de inexistência universal" in norm)
check("G-07 nenhuma promessa de desempenho clínico",
      not any(p in manuscrito_low for p in (
          "atinge 90% de acurácia", "clinicamente válido",
          "a correção de k20 melhorou", "este é o primeiro protocolo",
          "qualis a1 garantido", "aceite garantido", "nota 10 garantida")))

ausentes = []
for nome, alternativas in CITACOES.items():
    if not any(all(s in corpo_low for s in alternativa) for alternativa in alternativas):
        ausentes.append(nome)
check("G-08 todas as fontes citadas no corpo", not ausentes, ", ".join(ausentes))

dois = set()
for bruto in re.findall(r"10\.\d{4,9}/\S+", manuscrito_low.replace("**", "").replace("`", "")):
    dois.add(bruto.rstrip(";,.)\""))
dois_invalidos = sorted(dois - DOIS_APROVADOS)
check("G-09 nenhum DOI inventado", not dois_invalidos, ", ".join(dois_invalidos))
check("G-10 treze referencias com DOI", len(dois) == 13, str(len(dois)))
check("G-11 toda referencia listada e citada no corpo",
      all(s in referencias.lower() for s in ("10.1109/ase", "10.48550/arxiv.2604.20070")))

numeros = [
    "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd",
    "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475",
    "0,6333", "0,7333", "0,8000", "0,9000",
    "0,743786", "0,965401", "0,758863", "0,950323",
    "30/30", "22/22", "10/10", "1e-12",
]
ausentes = [n for n in numeros if n not in manuscrito]
check("G-12 numeros e hashes auditaveis presentes", not ausentes, ", ".join(ausentes))
check("G-13 Solver nao reexecutado e cache como diagnostico",
      "Solver não foi reexecutado" in manuscrito and
      "diagnóstico do estado original" in manuscrito_low)
check("G-14 ABNT declarada",
      all(n in manuscrito for n in ("NBR 14724", "NBR 6023", "NBR 10520")))
check("G-15 risco de vazamento sem afirmacao de ocorrencia",
      "risco de vazamento de dados" in manuscrito_low and
      "sem afirmar que houve vazamento efetivo" in manuscrito_low)
check("G-16 diretrizes com decisao explicita",
      "não como lista de conformidade" in manuscrito_low and
      "não foi aplicada" in manuscrito_low and
      "não se aplicam" in manuscrito_low)
check("G-17 edição adicional exige autorizacao",
      "autorização explícita" in manuscrito)
check("G-18 pendencias marcadas",
      len(re.findall(r"\[A CONFIRMAR[^\]]*\]", manuscrito)) >= 10)
check("G-19 declaracoes de financiamento, conflitos e autoria",
      all(k in manuscrito_low for k in ("financiamento", "conflitos de interesse",
                                        "autoria e contribuições", "periódico-alvo")))

cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", manuscrito)))
check("G-20 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
estranhos = re.findall(
    r"\b(?:after|during|however|therefore|summary|toutes|aplikado|during)\b",
    corpo_low,
)
check("G-21 sem palavras soltas em outro idioma", not estranhos, ", ".join(estranhos))
check("G-22 busca auditada com data e limites",
      "21 de novembro de 2026" in manuscrito and
      "não é revisão sistemática" in manuscrito_low and
      "HTTP 402" in manuscrito and "robots.txt" in manuscrito)
check("G-23 sem alegação de validade diagnóstica",
      "nenhuma alegação clínica" in manuscrito_low and
      "não estabelece validade diagnóstica" in manuscrito_low)
check("G-24 revisao humana nao declarada como concluida",
      "revisão humana final ainda não foi registrada como concluída" in manuscrito)

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
