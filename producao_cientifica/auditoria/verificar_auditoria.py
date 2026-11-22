"""Verificacao deterministica dos achados da auditoria (SPEC-AUD-TEA-001).

Uso: .venv/bin/python producao_cientifica/auditoria/verificar_auditoria.py
Nao modifica o arquivo auditado. Nao carrega a aba gigante de dados brutos.
"""
import os, re, sys, zipfile, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSM = os.path.join(BASE, "Redes Neurais - TEA Dataset VBA.xlsm")

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl ausente: use .venv/bin/python")

resultados = []

def check(nome, condicao, detalhe=""):
    resultados.append((nome, bool(condicao), detalhe))
    print(("PASS " if condicao else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))

sha = hashlib.sha256(open(XLSM, "rb").read()).hexdigest()
print("SHA-256:", sha)

z = zipfile.ZipFile(XLSM)
wb_xml = z.read("xl/workbook.xml").decode("utf-8", "replace")
vba = z.read("xl/vbaProject.bin")

# A-01: residuos de template e referencias quebradas em nomes definidos
residuos = [k for k in ("Bananas", "Laranjas", "Maçãs", "lst_Fruta",
                        "ImpostoSobreVendas", "Remessa") if k in wb_xml]
check("A-01 residuos de template em nomes definidos", len(residuos) >= 5,
      ", ".join(residuos))
check("A-02 #REF! em nomes definidos", wb_xml.count("#REF!") >= 7,
      "ocorrencias=%d" % wb_xml.count("#REF!"))

# A-03: aspas tipograficas no codigo VBA (Módulo4 / telaCheia / telaNormal)
check("A-03 aspas tipograficas U+201C/U+201D no VBA",
      "\u201cDASHBOARD\u201d".encode("cp1252") in vba,
      "Módulo4: Application.Caption")

# A-04/05/06: achados nas 5 abas de RNA
wb = openpyxl.load_workbook(XLSM, read_only=True, data_only=False)
wbv = openpyxl.load_workbook(XLSM, read_only=True, data_only=True)
redes = [s for s in wb.sheetnames if s.startswith("Rede Neural")]
check("A-04 existem 5 abas de RNA", len(redes) == 5, str(len(redes)))

erros_k20, erros_acuracia, contagens, sem_metrica = [], [], [], []
for nome in redes:
    ws, wsv = wb[nome], wbv[nome]
    k20 = str(ws["K20"].value or "")
    k21 = str(ws["K21"].value or "")
    if "MAX(0.1" in k20 and "MAX(-0.1" in k21:
        erros_k20.append(nome)
    if str(ws["S16"].value).replace(" ", "") == "=SUM(-R16,1)":
        erros_acuracia.append(nome)
    n_treino = sum(1 for r in range(20, 140) if ws.cell(r, 7).value in ("TEA", "NAO_TEA"))
    n_teste = sum(1 for r in range(145, 175) if ws.cell(r, 7).value in ("TEA", "NAO_TEA"))
    contagens.append((n_treino, n_teste))
    extra = [c.coordinate for row in ws.iter_rows(min_row=144, max_row=175,
                                                  min_col=19, max_col=37)
             for c in row if c.value is not None]
    if not extra:
        sem_metrica.append(nome)
    r16, s16 = wsv["R16"].value, wsv["S16"].value
    if isinstance(r16, (int, float)) and isinstance(s16, (int, float)):
        if abs(s16 - (1 - r16)) > 1e-12:
            erros_acuracia.append(nome + " (cache inconsistente)")

check("A-05 sinal do Leaky ReLU errado apenas em K20", len(erros_k20) == 5,
      "%d/5 abas" % len(erros_k20))
check("A-06 'Acuracia' = 1 - erro quadratico medio", len(erros_acuracia) == 5,
      "%d/5 abas" % len(set(erros_acuracia)))
check("A-07 treino=120 e teste=30 em todas as abas",
      contagens == [(120, 30)] * 5, str(contagens[:2]) + " ...")
check("A-08 nenhuma metrica agregada no bloco de teste", len(sem_metrica) == 5,
      "%d/5 abas" % len(sem_metrica))

# A-09: divergencia documental 60 vs 30
txt_resumo = z.read("xl/drawings/drawing15.xml").decode("utf-8", "replace")
check("A-09 texto afirma 60 imagens de teste", "60" in re.sub(r"<[^>]+>", "", txt_resumo),
      "drawing15 (EXPERIMENTOS | RESUMO)")

# A-10: p-code sem stomping (modulos 'vazios' nao tem procedimentos)
pc = open(os.path.join(os.path.dirname(__file__), "_pcode_evidencia.txt"),
          encoding="utf-8").read() if os.path.exists(
    os.path.join(os.path.dirname(__file__), "_pcode_evidencia.txt")) else ""
if pc:
    check("A-10 apenas SOLVER1/telaCheia/telaNormal tem p-code",
          pc.count("FuncDefn") == 3, "FuncDefn=%d" % pc.count("FuncDefn"))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(1 for _, ok, _ in resultados if ok), len(resultados)))
sys.exit(0 if all(ok for _, ok, _ in resultados) else 1)
