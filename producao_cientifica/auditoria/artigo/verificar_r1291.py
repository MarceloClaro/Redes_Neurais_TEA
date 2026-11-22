"""Gate SDD/TDD da extensao R1291 (aba AUDITORIA_M7 + exploracao separada).

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_r1291.py

Somente leitura, exceto pela reexecucao deterministica do gerador de
exploracao, que e executado duas vezes e comparado byte a byte. Reexecuta
os nove gates anteriores como subprocessos e exige que nenhum falhe.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))
EXPL = os.path.join(HERE, "exploracao")

ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
CORRIGIDO = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
BACKUP = os.path.join(AUD, "backup", "Redes_Neurais_TEA_Dataset_VBA_corrigido.pre_r1291.xlsm")
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"
HASH_PRE = "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475"
HASH_ATUAL = "5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb"

SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1291-aba-auditoria-exploracao-rna-tea.md")
SPEC1282 = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
RELATORIO = os.path.join(HERE, "RELATORIO_R1291.md")
GERADOR_ABA = os.path.join(AUD, "inserir_aba_m7.py")
GERADOR_EXPL = os.path.join(EXPL, "analise_exploratoria.py")
JSON_EXPL = os.path.join(EXPL, "resultados_exploratorios.json")
MD_EXPL = os.path.join(EXPL, "RELATORIO_EXPLORACAO.md")
MANUSCRITO = os.path.join(HERE, "MANUSCRITO_ABNT.md")
RASCUNHO = os.path.join(HERE, "MANUSCRITO_rascunho.md")
REL_M7 = os.path.join(HERE, "RELATORIO_M7.md")

GATES_ANTERIORES = [
    os.path.join(AUD, "verificar_auditoria.py"),
    os.path.join(AUD, "verificar_correcao.py"),
    os.path.join(HERE, "verificar_m0_m1.py"),
    os.path.join(HERE, "verificar_m2.py"),
    os.path.join(HERE, "verificar_m3.py"),
    os.path.join(HERE, "verificar_m4.py"),
    os.path.join(HERE, "verificar_m5.py"),
    os.path.join(HERE, "verificar_m6.py"),
    os.path.join(HERE, "verificar_m7.py"),
]

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


artefatos = [SPEC, SPEC1282, RELATORIO, GERADOR_ABA, GERADOR_EXPL, JSON_EXPL,
             MD_EXPL, ORIGINAL, CORRIGIDO, BACKUP, MANUSCRITO, RASCUNHO, REL_M7]
artefatos += GATES_ANTERIORES
faltando = [p for p in artefatos if not os.path.exists(p)]
check("G-01 artefatos R1291 e cadeia anterior presentes", not faltando,
      ", ".join(os.path.basename(p) for p in faltando))
if faltando:
    print("\nResumo: %d/%d verificacoes positivas" %
          (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

# G-02 aba documental legivel, sem formulas nem macros
with zipfile.ZipFile(CORRIGIDO) as z:
    check("G-02 ZIP integro", z.testzip() is None)
    sheet = z.read("xl/worksheets/sheet26.xml")
    try:
        raiz = ET.fromstring(sheet)
        xml_ok = raiz.tag.endswith("worksheet")
    except ET.ParseError:
        xml_ok = False
    texto_aba = re.sub(r"<[^>]+>", "", sheet.decode("utf-8"))
    check("G-02 aba AUDITORIA_M7 legivel sem macros",
          xml_ok and "<f" not in sheet.decode("utf-8") and
          "AUDITORIA_M7" in z.read("xl/workbook.xml").decode("utf-8"))

    # G-03 inventario de planilhas
    with zipfile.ZipFile(ORIGINAL) as zo:
        nomes_orig = set(re.findall(r'<sheet name="([^"]+)"',
                                    zo.read("xl/workbook.xml").decode("utf-8")))
        nomes_corr = set(re.findall(r'<sheet name="([^"]+)"',
                                    z.read("xl/workbook.xml").decode("utf-8")))
    check("G-03 25 originais preservadas mais aba nova",
          len(nomes_orig) == 25 and nomes_corr == nomes_orig | {"AUDITORIA_M7"} and
          len(nomes_corr) == 26,
          "orig=%d corr=%d" % (len(nomes_orig), len(nomes_corr)))

    # G-04 contagens preservadas
    with zipfile.ZipFile(BACKUP) as zb:
        contagens = {}
        for prefixo in ("xl/charts/", "xl/drawings/", "xl/media/", "xl/tables/"):
            contagens[prefixo] = (
                len([n for n in zb.namelist() if n.startswith(prefixo)]),
                len([n for n in z.namelist() if n.startswith(prefixo)]),
            )
    check("G-04 graficos/desenhos/midia/tabelas preservados",
          all(a == b for a, b in contagens.values()),
          "; ".join("%s=%d/%d" % (k.rstrip("/"), a, b)
                    for k, (a, b) in contagens.items()))

    # G-05 VBA e recalculo
    vba_atual = z.read("xl/vbaProject.bin")
    with zipfile.ZipFile(BACKUP) as zb:
        vba_pre = zb.read("xl/vbaProject.bin")
    wbxml = z.read("xl/workbook.xml").decode("utf-8")
    check("G-05 VBA intacto e recalculo forçado",
          vba_atual == vba_pre and 'fullCalcOnLoad="1"' in wbxml and
          "PerformanceCache zerado" in texto_aba)

    # G-06 calcChain ausente
    check("G-06 calcChain permanece ausente", "xl/calcChain.xml" not in z.namelist())

    # G-07 avisos na aba
    check("G-07 aba declara limites e pendencias",
          all(s in texto_aba for s in (
              "NAO sao resultado validado", "Solver NAO reexecutado",
              "As 30 imagens NAO foram integradas", "Onda 3",
              "revisao humana pendente")))

    # G-08 aviso T157 preservado nas abas de RNA
    with zipfile.ZipFile(BACKUP) as zb:
        planilhas_rna = [n for n in zb.namelist()
                         if re.match(r"xl/worksheets/sheet\d+\.xml$", n)]
        avisos = sum("NAO VALIDADO" in zb.read(n).decode("utf-8", "replace")
                     for n in planilhas_rna)
    check("G-08 aviso NAO VALIDADO preservado nas cinco abas", avisos == 5,
          "%d/5" % avisos)

    # G-09 nenhuma planilha original alterada
    with zipfile.ZipFile(BACKUP) as zb:
        alteradas = [n for n in zb.namelist()
                     if re.match(r"xl/worksheets/sheet\d+\.xml$", n)
                     and zb.read(n) != z.read(n)]
    check("G-09 formulas e planilhas originais inalteradas", not alteradas,
          ", ".join(alteradas))

# G-10 hashes registrados e conferidos
tudo_hash = "\n".join(read(p) for p in (SPEC, SPEC1282, RELATORIO, MANUSCRITO,
                                        RASCUNHO, REL_M7))
check("G-10 cadeia de hashes registrada e conferida",
      all(h in tudo_hash for h in (HASH_ORIGINAL, HASH_PRE, HASH_ATUAL)) and
      sha256(ORIGINAL) == HASH_ORIGINAL and sha256(BACKUP) == HASH_PRE and
      sha256(CORRIGIDO) == HASH_ATUAL,
      "atual=%s" % sha256(CORRIGIDO)[:12])

# G-11 reexecucao dos gates anteriores
def executar_gate(camino):
    proc = subprocess.run([sys.executable, camino], cwd=ROOT,
                          capture_output=True, text=True)
    linhas = proc.stdout.splitlines()
    falhas = [linha for linha in linhas if linha.startswith("FAIL")]
    resumos = [linha for linha in linhas if linha.startswith("Resumo:")]
    ok_resumo = bool(resumos) and all(
        re.match(r"Resumo: (\d+)/(\d+)", linha) and
        re.match(r"Resumo: (\d+)/(\d+)", linha).group(1) ==
        re.match(r"Resumo: (\d+)/(\d+)", linha).group(2)
        for linha in resumos)
    return proc.returncode == 0 and not falhas and ok_resumo, falhas, resumos


estados = [(os.path.basename(p),) + executar_gate(p) for p in GATES_ANTERIORES]
ruins = [(nome, falhas) for nome, ok, falhas, _ in estados if not ok]
check("G-11 nove gates anteriores reexecutados sem FAIL",
      not ruins,
      "; ".join("%s:%s" % (n, f[:1]) for n, f in ruins))

# G-12/G-13 determinismo da exploracao e workbook intacto
json_antes, md_antes = sha256(JSON_EXPL), sha256(MD_EXPL)
wb_antes = sha256(CORRIGIDO)
proc = subprocess.run([sys.executable, GERADOR_EXPL], cwd=ROOT,
                      capture_output=True, text=True)
check("G-12 exploracao deterministica na reexecucao",
      proc.returncode == 0 and sha256(JSON_EXPL) == json_antes and
      sha256(MD_EXPL) == md_antes,
      "%s/%s" % (json_antes[:8], md_antes[:8]))
check("G-13 exploracao nao altera o workbook", sha256(CORRIGIDO) == wb_antes)

# G-14 sem afirmativa de ganho validado
corpus_expl = read(MD_EXPL) + read(JSON_EXPL)
proibidas = [
    "ganho de acuracia do modelo corrigido foi",
    "melhoria validada",
    "acuracia validada do modelo corrigido",
    "validade diagnostica comprovada",
    "superioridade comprovada",
    "desempenho comprovado do modelo corrigido",
]
check("G-14 exploracao sem afirmativa de ganho validado",
      not any(p in corpus_expl for p in proibidas) and
      "Nao representa desempenho do arquivo corrigido" in corpus_expl and
      "Nenhum ganho de classificacao do modelo corrigido" in corpus_expl)

# G-15 documentacao atualizada sem apagar pendencias
spec_txt, rel_txt = read(SPEC), read(RELATORIO)
check("G-15 SPEC e relatorio atualizados sem apagar pendencias",
      "AC-12" in spec_txt and "G-15" in spec_txt and
      all(s in rel_txt for s in (
          HASH_ATUAL, "Solver", "30 imagens", "Onda 3",
          "não estabelece desempenho", "sem revisão externa",
          "15/15")) and
      HASH_ATUAL in read(MANUSCRITO) and "Extensão R1291" in read(MANUSCRITO) and
      HASH_ATUAL in read(RASCUNHO) and HASH_ATUAL in read(REL_M7))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
