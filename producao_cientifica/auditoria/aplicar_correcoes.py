"""Aplica as Ondas 1 e 2 autorizadas numa COPIA do workbook.

Uso: .venv/bin/python producao_cientifica/auditoria/aplicar_correcoes.py
O original permanece intacto. A copia e gravada em auditoria/.
"""
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ORIGINAL = os.path.join(BASE, "Redes Neurais - TEA Dataset VBA.xlsm")
SAIDA = os.path.join(HERE, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")

sys.path.insert(0, HERE)
import olefile
import openpyxl
from oletools.olevba import decompress_stream
from vba_compress import compress_stream

RESIDUOS = [
    "Bananas", "Laranjas", "Maçãs", "Limões", "lst_Fruta",
    "lst_TipoDeFruta", "ImpostoSobreVendas", "Remessa",
]

REDES = [
    "Rede Neural |n120|n40|n116|n86",
    "Rede Neural |n120|n40|n116|n50",
    "Rede Neural |n119|n72|n1|n73",
    "Rede Neural |n120|n40|n119|n72",
    "Rede Neural |n19|n99|n120|n40|",
]

SHEET_BY_NAME = {}


def esc(texto):
    return escape(str(texto), {'"': "&quot;"})


def num(v):
    return format(float(v), ".17g")


def mapear_planilhas(z):
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    relmap = dict(re.findall(r'<Relationship Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    for nome, rid in re.findall(
            r'<sheet name="([^"]+)"[^>]*r:id="([^"]+)"', wb):
        alvo = relmap[rid]
        SHEET_BY_NAME[nome] = "xl/" + alvo.lstrip("/").replace("xl/", "", 1)


def metrics_from_cache(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {}
    for nome in REDES:
        ws = wb[nome]
        y = [ws[f"G{r}"].value for r in range(145, 175)]
        p = [ws[f"R{r}"].value for r in range(145, 175)]
        tp = sum(a == "TEA" and b == "TEA" for a, b in zip(y, p))
        tn = sum(a == "NAO_TEA" and b == "NAO_TEA" for a, b in zip(y, p))
        fp = sum(a == "NAO_TEA" and b == "TEA" for a, b in zip(y, p))
        fn = sum(a == "TEA" and b == "NAO_TEA" for a, b in zip(y, p))
        n, zval = len(y), 1.96
        acc = (tp + tn) / n
        den = 1 + zval * zval / n
        ctr = (acc + zval * zval / (2 * n)) / den
        half = zval * math.sqrt(acc * (1 - acc) / n + zval * zval / (4 * n * n)) / den
        out[nome] = {
            "n": n,
            "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "acc": acc, "ic_inf": ctr - half, "ic_sup": ctr + half,
            "sens": tp / (tp + fn) if tp + fn else 0.0,
            "esp": tn / (tn + fp) if tn + fp else 0.0,
            "vpp": tp / (tp + fp) if tp + fp else 0.0,
            "vpn": tn / (tn + fn) if tn + fn else 0.0,
            "r16": ws["R16"].value, "s16": ws["S16"].value,
        }
    wb.close()
    return out


def patch_workbook_xml(xml):
    for nome in RESIDUOS:
        xml = re.sub(
            r'<definedName\b[^>]*\bname="' + re.escape(nome) +
            r'"[^>]*>.*?</definedName>', "", xml, flags=re.S)
    xml = re.sub(r'<definedName\b[^>]*>[^<]*#REF![^<]*</definedName>', "", xml, flags=re.S)
    if 'fullCalcOnLoad="1"' not in xml:
        xml = xml.replace("<calcPr ", '<calcPr fullCalcOnLoad="1" ', 1)
    return xml


def patch_shared_strings(xml):
    xml = xml.replace("<si><t>Acurácia</t></si>",
                      "<si><t>1 - EQM (nao acuracia)</t></si>")
    xml = xml.replace("<si><t>Erro Total</t></si>",
                      "<si><t>EQM medio do treino</t></si>")
    antigo = ('<si><r><t xml:space="preserve">Números de Imagens Embbeding teste =   </t></r>'
              '<r><rPr><b/><sz val="10"/><color rgb="FFFFFF00"/><rFont val="Calibri"/>'
              '<family val="2"/><scheme val="minor"/></rPr>'
              '<t xml:space="preserve"> 60</t></r></si>')
    if antigo not in xml:
        raise RuntimeError("string de 60 imagens nao encontrada")
    xml = xml.replace(antigo, antigo.replace(" 60", " 30"))
    return xml


def patch_drawing(xml):
    antigo = "<a:t> COM 60 IMAGENS</a:t>"
    if xml.count(antigo) != 1:
        raise RuntimeError("texto de 60 imagens no drawing nao encontrado")
    return xml.replace(antigo, "<a:t> COM 30 IMAGENS</a:t>")


def set_cell(xml, ref, formula, value):
    padrao = r'<c r="' + re.escape(ref) + r'"[^>]*>.*?</c>'
    m = re.search(padrao, xml, re.S)
    if not m:
        raise RuntimeError("celula nao encontrada: " + ref)
    celula = m.group()
    celula, n1 = re.subn(r"<f>.*?</f>", "<f>" + esc(formula) + "</f>", celula, count=1, flags=re.S)
    celula, n2 = re.subn(r"<v>.*?</v>", "<v>" + num(value) + "</v>", celula, count=1, flags=re.S)
    if not (n1 and n2):
        raise RuntimeError("formula/valor nao encontrado em " + ref)
    return xml[:m.start()] + celula + xml[m.end():]


def style_from_row(row_xml, row):
    m = re.search(r'<c r="R%d"[^>]*\bs="(\d+)"' % row, row_xml)
    return m.group(1) if m else "3"


def build_metric_cells(row, style, values):
    # linha 144: cabecalho; 145-156: metricas; 157: status; 158+: proveniencia
    if row == 144:
        return (
            '<c r="S144" s="' + style + '" t="inlineStr"><is><t>'
            + esc("Metricas de teste (cache original)") + "</t></is></c>"
            '<c r="T144" s="' + style + '" t="inlineStr"><is><t>'
            + esc("Valor") + "</t></is></c>"
            '<c r="V144" s="' + style + '" t="inlineStr"><is><t>'
            + esc("DEFINICOES E PROVENIENCIA") + "</t></is></c>"
        )

    notas = {
        145: "Perda de treino: EQM medio = SUM(R20:R139)/120 (nao entropia cruzada)",
        146: "Classificacao: softmax de 3 logits (O:Q) seguido de argmax",
        147: "Pesos: cache gerado pelo Solver; Solver NAO reexecutado neste ambiente",
        148: "K20 corrigido: recalcular/retreinar no Excel antes de usar as metricas",
        149: "Status: CACHE ORIGINAL - NAO VALIDADO apos a correcao do K20",
    }
    saida = ""
    if row == 157:
        saida = ('<c r="T157" s="' + style + '" t="inlineStr"><is><t>'
                 + esc("CACHE ORIGINAL - NAO VALIDADO apos K20; Solver nao reexecutado")
                 + "</t></is></c>")
    elif row in values:
        label, formula, valor = values[row]
        saida = (
            '<c r="S%d" s="%s" t="inlineStr"><is><t>%s</t></is></c>' %
            (row, style, esc(label)) +
            '<c r="T%d" s="%s"><f>%s</f><v>%s</v></c>' %
            (row, style, esc(formula), num(valor))
        )
    if row in notas:
        saida += ('<c r="V%d" s="%s" t="inlineStr"><is><t>%s</t></is></c>' %
                  (row, style, esc(notas[row])))
    return saida


def patch_sheet(xml, nome, m):
    # Onda 1: sinal do Leaky ReLU apenas em K20.
    def corrige_k20(match):
        return match.group().replace("MAX(0.1*", "MAX(-0.1*")

    xml, n = re.subn(r'<c r="K20"[^>]*>.*?</c>', corrige_k20, xml,
                     count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("K20 nao encontrado em " + nome)

    # Onda 1: AG35/AH35 divisao por 100 indevida.
    xml = set_cell(xml, "AG35", "R16", m["r16"])
    xml = set_cell(xml, "AH35", "S16", m["s16"])

    # Onda 2: bloco de metricas de teste.
    zval = 1.96
    wilson_inf = (
        "($T$146+1.96^2/(2*$T$145))/(1+1.96^2/$T$145)"
        "-1.96*SQRT(($T$146*(1-$T$146)+1.96^2/(4*$T$145^2))/$T$145)"
        "/(1+1.96^2/$T$145)"
    )
    wilson_sup = wilson_inf.replace("-1.96*SQRT(", "+1.96*SQRT(")
    values = {
        145: ("n", "COUNTA($G$145:$G$174)", m["n"]),
        146: ("Acuracia", "SUMPRODUCT(--($G$145:$G$174=$R$145:$R$174))/COUNTA($G$145:$G$174)", m["acc"]),
        147: ("TP", 'COUNTIFS($G$145:$G$174,"TEA",$R$145:$R$174,"TEA")', m["tp"]),
        148: ("TN", 'COUNTIFS($G$145:$G$174,"NAO_TEA",$R$145:$R$174,"NAO_TEA")', m["tn"]),
        149: ("FP", 'COUNTIFS($G$145:$G$174,"NAO_TEA",$R$145:$R$174,"TEA")', m["fp"]),
        150: ("FN", 'COUNTIFS($G$145:$G$174,"TEA",$R$145:$R$174,"NAO_TEA")', m["fn"]),
        151: ("Sensibilidade", "IFERROR(T147/(T147+T150),0)", m["sens"]),
        152: ("Especificidade", "IFERROR(T148/(T148+T149),0)", m["esp"]),
        153: ("VPP", "IFERROR(T147/(T147+T149),0)", m["vpp"]),
        154: ("VPN", "IFERROR(T148/(T148+T150),0)", m["vpn"]),
        155: ("IC95% inf (Wilson)", wilson_inf, m["ic_inf"]),
        156: ("IC95% sup (Wilson)", wilson_sup, m["ic_sup"]),
    }

    for row in range(144, 158):
        padrao = r'(<row r="%d"[^>]*>)(.*?)(</row>)' % row
        mm = re.search(padrao, xml, re.S)
        if not mm:
            raise RuntimeError("linha %d ausente em %s" % (row, nome))
        abertura = re.sub(r'spans="\d+:\d+"', 'spans="2:22"', mm.group(1))
        estilo = style_from_row(mm.group(2), row)
        conteudo = mm.group(2) + build_metric_cells(row, estilo, values)
        xml = xml[:mm.start()] + abertura + conteudo + mm.group(3) + xml[mm.end():]

    return xml


def build_patched_vba():
    orig = zipfile.ZipFile(ORIGINAL).read("xl/vbaProject.bin")
    fd, tmp = tempfile.mkstemp(suffix=".bin", dir="/tmp/opencode")
    os.close(fd)
    with open(tmp, "wb") as fh:
        fh.write(orig)

    arquivos = {
        "VBA/Módulo3": os.path.join(HERE, "modulo3_aplicado.bas"),
        "VBA/Módulo4": os.path.join(HERE, "modulo4_aplicado.bas"),
    }
    ole = olefile.OleFileIO(tmp, write_mode=True)
    for stream_name, path in arquivos.items():
        antigo = ole.openstream(stream_name).read()
        m = re.search(br"\x00Attribut", antigo, re.I)
        if not m:
            raise RuntimeError("fonte comprimida nao encontrada: " + stream_name)
        offset = m.start() - 3
        fonte = open(path, "rb").read().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        comprimido = compress_stream(fonte)
        if decompress_stream(bytearray(comprimido)) != fonte:
            raise RuntimeError("roundtrip MS-OVBA falhou: " + stream_name)
        if len(comprimido) != len(antigo[offset:]):
            raise RuntimeError("tamanho comprimido divergente: " + stream_name)
        novo = b"\x00" * offset + comprimido  # invalida p-cache obsoleto
        if len(novo) != len(antigo):
            raise RuntimeError("tamanho de stream divergente: " + stream_name)
        ole.write_stream(stream_name, novo)
    ole.close()
    with open(tmp, "rb") as fh:
        resultado = fh.read()
    os.unlink(tmp)
    return resultado


def main():
    metricas = metrics_from_cache(ORIGINAL)
    vba = build_patched_vba()

    with zipfile.ZipFile(ORIGINAL) as zin:
        mapear_planilhas(zin)
        modificados = {}
        xml = patch_workbook_xml(zin.read("xl/workbook.xml").decode("utf-8"))
        modificados["xl/workbook.xml"] = xml.encode("utf-8")
        modificados["xl/sharedStrings.xml"] = patch_shared_strings(
            zin.read("xl/sharedStrings.xml").decode("utf-8")).encode("utf-8")
        modificados["xl/drawings/drawing15.xml"] = patch_drawing(
            zin.read("xl/drawings/drawing15.xml").decode("utf-8")).encode("utf-8")
        modificados["xl/_rels/workbook.xml.rels"] = re.sub(
            r'<Relationship\b[^>]*Target="calcChain\.xml"[^>]*/>', "",
            zin.read("xl/_rels/workbook.xml.rels").decode("utf-8")).encode("utf-8")
        modificados["[Content_Types].xml"] = re.sub(
            r'<Override\b[^>]*PartName="/xl/calcChain\.xml"[^>]*/>', "",
            zin.read("[Content_Types].xml").decode("utf-8")).encode("utf-8")

        for nome in REDES:
            planilha = SHEET_BY_NAME[nome]
            conteudo = patch_sheet(
                zin.read(planilha).decode("utf-8"), nome, metricas[nome])
            modificados[planilha] = conteudo.encode("utf-8")
        modificados["xl/vbaProject.bin"] = vba

        with zipfile.ZipFile(SAIDA, "w") as zout:
            for info in zin.infolist():
                if info.filename == "xl/calcChain.xml":
                    continue
                data = modificados.get(info.filename)
                if data is None:
                    data = zin.read(info.filename)
                zout.writestr(info, data)

    print("Copia corrigida gravada em:", SAIDA)
    print("SHA-256:", __import__("hashlib").sha256(open(SAIDA, "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
