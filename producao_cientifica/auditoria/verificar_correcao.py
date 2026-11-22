"""Gate SDD/TDD das Ondas 1 e 2 aplicadas ao workbook de RNA TEA.

Uso: .venv/bin/python producao_cientifica/auditoria/verificar_correcao.py
O arquivo original NAO e modificado. Este script apenas verifica a copia corrigida.
"""
import hashlib
import math
import os
import re
import sys
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL = os.path.join(BASE, "Redes Neurais - TEA Dataset VBA.xlsm")
CORRIGIDO = os.path.join(os.path.dirname(__file__),
                         "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"

try:
    import openpyxl
    import olefile
    from oletools.olevba import VBA_Parser
except ImportError:
    sys.exit("Dependencias ausentes: use .venv/bin/python (openpyxl, olefile, oletools)")

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok, detalhe))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


check("G-01 original preservado", os.path.exists(ORIGINAL) and sha256(ORIGINAL) == HASH_ORIGINAL)
check("G-02 copia corrigida existe", os.path.exists(CORRIGIDO),
      os.path.basename(CORRIGIDO) if os.path.exists(CORRIGIDO) else "ausente")

if not os.path.exists(CORRIGIDO):
    print("\nResumo: 0/%d verificacoes positivas" % len(resultados))
    sys.exit(1)

check("G-03 copia difere do original", sha256(CORRIGIDO) != HASH_ORIGINAL)

with zipfile.ZipFile(ORIGINAL) as zo, zipfile.ZipFile(CORRIGIDO) as zc:
    check("G-04 ZIP integro", zc.testzip() is None)
    total_planilhas = len([n for n in zc.namelist()
                           if re.match(r"xl/worksheets/sheet\d+\.xml$", n)])
    check("G-05 planilhas preservadas (25 + AUDITORIA_M7)",
          total_planilhas == 26 and
          'name="AUDITORIA_M7"' in zc.read("xl/workbook.xml").decode("utf-8"))
    check("G-06 graficos/desenhos preservados",
          len([n for n in zo.namelist() if n.startswith("xl/charts/")]) ==
          len([n for n in zc.namelist() if n.startswith("xl/charts/")]) and
          len([n for n in zo.namelist() if n.startswith("xl/drawings/")]) ==
          len([n for n in zc.namelist() if n.startswith("xl/drawings/")]))
    check("G-06b midia/tabelas preservadas",
          len([n for n in zo.namelist() if n.startswith("xl/media/")]) ==
          len([n for n in zc.namelist() if n.startswith("xl/media/")]) and
          len([n for n in zo.namelist() if n.startswith("xl/tables/")]) ==
          len([n for n in zc.namelist() if n.startswith("xl/tables/")]) and
          set(zo.namelist()) - set(zc.namelist()) == {"xl/calcChain.xml"})

    wbxml = zc.read("xl/workbook.xml").decode("utf-8", "replace")
    residuos = [k for k in ("Bananas", "Laranjas", "Maçãs", "Limões", "lst_Fruta",
                            "lst_TipoDeFruta", "ImpostoSobreVendas", "Remessa")
                if k in wbxml]
    check("G-07 nomes residuais removidos", not residuos, ", ".join(residuos))
    check("G-08 #REF! removido dos nomes", "#REF!" not in wbxml,
          "ocorrencias=%d" % wbxml.count("#REF!"))
    check("G-09 recalculo forçado no Excel", 'fullCalcOnLoad="1"' in wbxml)

    desenho = zc.read("xl/drawings/drawing15.xml").decode("utf-8", "replace")
    texto_desenho = re.sub(r"<[^>]+>", "", desenho)
    check("G-10 documento corrigido para 30 imagens de teste",
          re.search(r"TESTES\s+COM\s+30\s+IMAGENS", texto_desenho) is not None and
          re.search(r"TESTES\s+COM\s+60\s+IMAGENS", texto_desenho) is None)

    shared = zc.read("xl/sharedStrings.xml").decode("utf-8", "replace")
    antigo = ('<si><r><t xml:space="preserve">Números de Imagens Embbeding teste =   </t></r>'
              '<r><rPr><b/><sz val="10"/><color rgb="FFFFFF00"/><rFont val="Calibri"/>'
              '<family val="2"/><scheme val="minor"/></rPr>'
              '<t xml:space="preserve"> 60</t></r></si>')
    novo = antigo.replace(" 60", " 30")
    check("G-11 resumo corrigido para 30 imagens de teste", antigo not in shared and novo in shared)

    vba_bytes = zc.read("xl/vbaProject.bin")

wb = openpyxl.load_workbook(CORRIGIDO, read_only=True, data_only=False)
wbv = openpyxl.load_workbook(CORRIGIDO, read_only=True, data_only=True)
redes = [s for s in wb.sheetnames if s.startswith("Rede Neural")]
check("G-12 5 abas de RNA presentes", len(redes) == 5, "%d abas" % len(redes))

k20_ok = k21_ok = rotulos_ok = ag_ok = metricas_ok = 0
for nome in redes:
    ws, wsv = wb[nome], wbv[nome]
    k20 = str(ws["K20"].value or "")
    k21 = str(ws["K21"].value or "")
    k20_ok += "MAX(-0.1*" in k20
    k21_ok += "MAX(-0.1*" in k21
    rotulos_ok += ("1 - EQM" in str(ws["S15"].value) and
                   "1 - EQM" in str(ws["AH34"].value) and
                   "EQM" in str(ws["AG34"].value))
    ag_ok += (str(ws["AG35"].value).replace(" ", "") == "=R16" and
              str(ws["AH35"].value).replace(" ", "") == "=S16")

    # Recalcula o esperado diretamente do bloco de teste em cache (G x R),
    # independentemente das formulas/cached values escritos em T.
    y = [wsv[f"G{r}"].value for r in range(145, 175)]
    p = [wsv[f"R{r}"].value for r in range(145, 175)]
    tp = sum(a == "TEA" and b == "TEA" for a, b in zip(y, p))
    tn = sum(a == "NAO_TEA" and b == "NAO_TEA" for a, b in zip(y, p))
    fp = sum(a == "NAO_TEA" and b == "TEA" for a, b in zip(y, p))
    fn = sum(a == "TEA" and b == "NAO_TEA" for a, b in zip(y, p))
    n, zv = len(y), 1.96
    acc = (tp + tn) / n
    den = 1 + zv * zv / n
    ctr = (acc + zv * zv / (2 * n)) / den
    half = zv * math.sqrt(acc * (1 - acc) / n + zv * zv / (4 * n * n)) / den
    exp = (n, acc, tp, tn, fp, fn,
           tp / (tp + fn) if tp + fn else 0.0,
           tn / (tn + fp) if tn + fp else 0.0,
           tp / (tp + fp) if tp + fp else 0.0,
           tn / (tn + fn) if tn + fn else 0.0,
           ctr - half, ctr + half)

    obtidos = tuple(wsv[f"T{r}"].value for r in range(145, 157))
    numericos = all(isinstance(v, (int, float)) for v in obtidos)
    compativel = numericos and all(abs(a - b) <= 1e-12 for a, b in zip(obtidos, exp))
    metricas_ok += (compativel and
                    "Metricas de teste" in str(ws["S144"].value) and
                    "NAO VALIDADO" in str(ws["T157"].value))

check("G-13 K20 corrigido nas 5 abas", k20_ok == 5, "%d/5" % k20_ok)
check("G-14 K21 ja estava correto e preservado", k21_ok == 5, "%d/5" % k21_ok)
check("G-15 rotulos de metricas renomeados", rotulos_ok == 5, "%d/5" % rotulos_ok)
check("G-16 AG35/AH35 sem divisao por 100", ag_ok == 5, "%d/5" % ag_ok)
check("G-17 metricas reais de teste presentes e corretas", metricas_ok == 5,
      "%d/5" % metricas_ok)

# Verificacao VBA direta no OLE, sem depender de conversao openpyxl.
import tempfile

with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tmp:
    tmp.write(vba_bytes)
    tmp_path = tmp.name
try:
    ole = olefile.OleFileIO(tmp_path)
    off3, off4 = 3263, 2862
    s3 = ole.openstream("VBA/Módulo3").read()
    s4 = ole.openstream("VBA/Módulo4").read()
    ole.close()

    with zipfile.ZipFile(CORRIGIDO) as zc:
        pass
    vp = VBA_Parser(CORRIGIDO)
    codigo = {stream: text for _, stream, _, text in vp.extract_macros()}
    m3 = codigo.get("VBA/Módulo3", "")
    m4 = codigo.get("VBA/Módulo4", "")
    check("G-18 VBA Módulo3 corrigido",
          "SolverReset" in m3 and "StepThru:=False" in m3 and
          m3.count("SolverOk ") == 1 and "SolverSolve(UserFinish:=True)" in m3 and
          "$AM$16" in m3)
    check("G-19 VBA Módulo4 com aspas ASCII",
          "\u201cDASHBOARD\u201d" not in m4 and 'Application.Caption = "DASHBOARD"' in m4 and
          'Application.Caption = ""' in m4)
    check("G-20 cache P-code obsoleto invalidado",
          s3[:off3] == b"\x00" * off3 and s4[:off4] == b"\x00" * off4)
    check("G-21 sem evidencia de VBA stomping", vp.detect_vba_stomping() is False)
finally:
    os.unlink(tmp_path)

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(1 for _, ok, _ in resultados if ok), len(resultados)))
sys.exit(0 if all(ok for _, ok, _ in resultados) else 1)
