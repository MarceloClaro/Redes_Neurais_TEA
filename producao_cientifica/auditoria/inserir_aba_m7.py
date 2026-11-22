"""Insere a aba AUDITORIA_M7 no workbook corrigido (SPEC-935-R1291).

Uso: .venv/bin/python producao_cientifica/auditoria/inserir_aba_m7.py

Edicao minima de OOXML: apenas workbook.xml, workbook.xml.rels,
[Content_Types].xml e a nova worksheet sao alterados. Todas as outras partes
do ZIP, incluindo VBA, graficos, midia e sharedStrings, sao copiadas byte a byte.
Nao usa openpyxl.save. Deterministico.
"""
import hashlib
import os
import re
import shutil
import sys
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(BASE, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
BACKUP = os.path.join(BASE, "backup", "Redes_Neurais_TEA_Dataset_VBA_corrigido.pre_r1291.xlsm")
TEMP = ALVO + ".r1291.tmp"

ABA = "AUDITORIA_M7"
SHEET_XML = "xl/worksheets/sheet26.xml"
SHEET_ID = "36"
R_ID = "rId32"

HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"
HASH_PRE = "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475"

LINHAS = [
    ("AUDITORIA METODOLOGICA M7 - REGISTRO DOCUMENTAL", True),
    ("", False),
    ("Finalidade: registrar a cadeia de evidencias da auditoria. Nao e resultado de modelo.", True),
    ("", False),
    ("Arquivo original preservado - SHA-256", True),
    (HASH_ORIGINAL, False),
    ("Copia corrigida antes desta aba - SHA-256", True),
    (HASH_PRE, False),
    ("", False),
    ("Gates reexecutados em M7", True),
    ("original 10/10; correcao 22/22; M0/M1 14/14; M2 23/23; M3 20/20", False),
    ("M4 22/22; M5 24/24; M6 33/33; M7 24/24; doctor 16 passed / 6 warned / 0 failed", False),
    ("", False),
    ("Falhas detectadas no original", True),
    ("K20 com MAX(0.1*z,z); rotulo Acuracia aplicado a 1-EQM; escala indevida em AG35/AH35", False),
    ("residuos de template e #REF!; p-code VBA obsoleto", False),
    ("", False),
    ("Reparo aplicado na copia", True),
    ("K20 -> MAX(-0.1*z,z) nas cinco abas; K21 ja estava correto", False),
    ("rotulo de proveniencia; edicao direta de OOXML/VBA; xl/calcChain.xml removido", False),
    ("fullCalcOnLoad=1; PerformanceCache zerado; 25 planilhas, 36 graficos, 55 desenhos, 22 midias, 104 tabelas preservados", False),
    ("", False),
    (" metricas em cache - diagnostico do estado original", True),
    ("n=30 por aba; acuracias 0,6333 / 0,7333 / 0,6333 / 0,8000 / 0,9000", False),
    ("IC em cache [0,743786; 0,965401] vs formula textual [0,758863; 0,950323]", False),
    ("Causa da divergencia do IC NAO resolvida; nenhuma versao foi escolhida como correta", False),
    ("", False),
    ("PENDENCIAS - NAO INTEGRADAS", True),
    ("Solver NAO reexecutado neste ambiente; sem versao, data, status, seed ou pesos finais", False),
    ("As 30 imagens NAO foram integradas; faltam proveniencia, consentimento, anonimizacao e referencia-padrão", False),
    ("Onda 3 (edicao da formula textual do IC) NAO autorizada e NAO executada", False),
    ("", False),
    ("LIMITES", True),
    ("Valores em cache NAO sao resultado validado. Nao ha desempenho do modelo corrigido.", False),
    ("Nao ha validade diagnostica, calibracao clinica ou aprovacao editorial declarada.", False),
    ("Aba documental criada em 2026-11-22 sob SPEC-935-R1291; revisao humana pendente.", False),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def xml_aba():
    linhas_xml = []
    for i, (texto, negrito) in enumerate(LINHAS, start=1):
        if not texto:
            continue
        estilo = ' s="1"' if negrito else ""
        celula = ('<c r="A%d"%s t="inlineStr"><is><t xml:space="preserve">%s</t>'
                  '</is></c>' % (i, estilo, esc(texto)))
        linhas_xml.append('<row r="%d">%s</row>' % (i, celula))
    corpo = "".join(linhas_xml)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<dimension ref="A1:A%d"/>'
            '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
            '<sheetFormatPr defaultRowHeight="15"/>'
            '<cols><col min="1" max="1" width="120" customWidth="1"/></cols>'
            '<sheetData>%s</sheetData>'
            '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" '
            'header="0.3" footer="0.3"/>'
            '</worksheet>' % (len(LINHAS), corpo))


def ler(z, nome):
    return z.read(nome).decode("utf-8")


def main():
    if not os.path.exists(BACKUP):
        print("backup ausente: execute a copia antes da edicao", file=sys.stderr)
        return 1
    with open(BACKUP, "rb") as fh:
        if hashlib.sha256(fh.read()).hexdigest() != HASH_PRE:
            print("backup nao confere com o hash pre-r1291", file=sys.stderr)
            return 1

    with zipfile.ZipFile(ALVO, "r") as zin:
        nomes = zin.namelist()
        if ABA in "".join(re.findall(r'<sheet name="([^"]+)"', ler(zin, "xl/workbook.xml"))):
            print("aba AUDITORIA_M7 ja existe", file=sys.stderr)
            return 1
        if SHEET_XML in nomes:
            print("parte sheet26.xml ja existe", file=sys.stderr)
            return 1
        if "xl/calcChain.xml" in nomes:
            print("calcChain presente; estado inesperado", file=sys.stderr)
            return 1

        wb = ler(zin, "xl/workbook.xml")
        rels = ler(zin, "xl/_rels/workbook.xml.rels")
        ct = ler(zin, "[Content_Types].xml")

        nova_sheet = ('<sheet name="%s" sheetId="%s" r:id="%s"/>'
                      % (ABA, SHEET_ID, R_ID))
        if "</sheets>" not in wb:
            print("marcador </sheets> ausente", file=sys.stderr)
            return 1
        wb = wb.replace("</sheets>", nova_sheet + "</sheets>", 1)

        nova_rel = ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/'
                    'officeDocument/2006/relationships/worksheet" '
                    'Target="worksheets/sheet26.xml"/>' % R_ID)
        if "</Relationships>" not in rels:
            print("marcador </Relationships> ausente", file=sys.stderr)
            return 1
        rels = rels.replace("</Relationships>", nova_rel + "</Relationships>", 1)

        novo_ct = ('<Override PartName="/xl/worksheets/sheet26.xml" '
                   'ContentType="application/vnd.openxmlformats-officedocument.'
                   'spreadsheetml.worksheet+xml"/>')
        if "</Types>" not in ct:
            print("marcador </Types> ausente", file=sys.stderr)
            return 1
        ct = ct.replace("</Types>", novo_ct + "</Types>", 1)

        substituidos = {
            "xl/workbook.xml": wb.encode("utf-8"),
            "xl/_rels/workbook.xml.rels": rels.encode("utf-8"),
            "[Content_Types].xml": ct.encode("utf-8"),
        }

        with zipfile.ZipFile(TEMP, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                dados = substituidos.get(info.filename, None)
                if dados is None:
                    dados = zin.read(info.filename)
                zout.writestr(info, dados)
            zout.writestr(SHEET_XML, xml_aba().encode("utf-8"))

    os.replace(TEMP, ALVO)
    with open(ALVO, "rb") as fh:
        print("novo hash:", hashlib.sha256(fh.read()).hexdigest())
    print("aba inserida:", ABA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
