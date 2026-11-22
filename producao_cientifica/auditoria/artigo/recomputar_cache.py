"""Recomputacao auditavel do cache de teste do workbook corrigido (M4).

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/recomputar_cache.py

Somente leitura do workbook. Nao abre Excel, nao reexecuta Solver, nao altera o .xlsm.
Saidas: M4_metricas_cache.json e M4_tabela_metricas.md neste diretorio.
Toda metrica emitida e rotulada como DIAGNOSTICO DO ESTADO ORIGINAL.
"""
import datetime
import hashlib
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
WORKBOOK = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
JSON_OUT = os.path.join(HERE, "M4_metricas_cache.json")
MD_OUT = os.path.join(HERE, "M4_tabela_metricas.md")

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"m": M}
TOL = 1e-12


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def carregar_planilhas(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    alvo = {c.attrib["Id"]: c.attrib["Target"] for c in rels}
    saida = {}
    for sh in wb.find("m:sheets", NS):
        rid = sh.attrib["{%s}id" % R]
        nome = sh.attrib["name"]
        if nome.startswith("Rede Neural"):
            caminho = alvo[rid]
            if not caminho.startswith("xl/"):
                caminho = "xl/" + caminho.lstrip("/")
            saida[nome] = caminho
    return saida


def carregar_celulas(z, caminho, shared):
    root = ET.fromstring(z.read(caminho))
    celulas = {}
    for c in root.iter("{%s}c" % M):
        ref = c.attrib["r"]
        tipo = c.attrib.get("t")
        f = c.find("m:f", NS)
        v = c.find("m:v", NS)
        inline = c.find("m:is", NS)
        valor = None
        if tipo == "s" and v is not None:
            valor = shared[int(v.text)]
        elif tipo == "inlineStr" and inline is not None:
            valor = "".join(t.text or "" for t in inline.iter("{%s}t" % M))
        elif v is not None:
            valor = v.text
        celulas[ref] = {"valor": valor, "formula": f.text if f is not None else None,
                        "tipo": tipo}
    return celulas


def texto(celulas, ref):
    return celulas.get(ref, {}).get("valor")


def numero(celulas, ref):
    bruto = texto(celulas, ref)
    if bruto is None:
        raise ValueError("celula ausente: " + ref)
    return float(bruto)


def wilson(p, n, z=1.96, variante="padrao"):
    """Duas formas nao equivalentes. A 'textual' reproduz a formula escrita em T155/T156."""
    z2 = z * z
    centro = (p + z2 / (2 * n)) / (1 + z2 / n)
    if variante == "padrao":
        half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    elif variante == "textual":
        half = z * math.sqrt((p * (1 - p) + z2 / (4 * n * n)) / n) / (1 + z2 / n)
    else:
        raise ValueError(variante)
    return centro - half, centro + half


def perto(a, b, tol=TOL):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


def analisar_aba(nome, celulas):
    n = int(numero(celulas, "T145"))
    tp = int(numero(celulas, "T147"))
    tn = int(numero(celulas, "T148"))
    fp = int(numero(celulas, "T149"))
    fn = int(numero(celulas, "T150"))
    p_cache = numero(celulas, "T146")
    rotulos = [texto(celulas, "G%d" % i) for i in range(145, 175)]
    previstos = [texto(celulas, "R%d" % i) for i in range(145, 175)]
    classes = [texto(celulas, "C%d" % i) for i in range(11, 14)]
    n_tea = sum(1 for r in rotulos if r == "TEA")
    n_nao = sum(1 for r in rotulos if r == "NAO_TEA")

    acuracia_calc = (tp + tn) / n
    sens_calc = tp / (tp + fn) if tp + fn else 0.0
    esp_calc = tn / (tn + fp) if tn + fp else 0.0
    vpp_calc = tp / (tp + fp) if tp + fp else 0.0
    vpn_calc = tn / (tn + fn) if tn + fn else 0.0
    wil_pad = wilson(p_cache, n, variante="padrao")
    wil_txt = wilson(p_cache, n, variante="textual")

    # Conferencia argmax das tres probabilidades em O:Q, quando disponiveis.
    argmax_ok = 0
    argmax_total = 0
    argmax_sem_classe = 0
    for row in range(145, 175):
        probs = []
        for col in "OPQ":
            v = texto(celulas, "%s%d" % (col, row))
            if v is None:
                break
            probs.append(float(v))
        if len(probs) == 3:
            argmax_total += 1
            idx = max(range(3), key=lambda i: probs[i])
            if idx >= len(classes) or not classes[idx]:
                argmax_sem_classe += 1
            elif classes[idx] == previstos[row - 145]:
                argmax_ok += 1

    return {
        "aba": nome,
        "n": n,
        "contagem_rotulos": {"TEA": n_tea, "NAO_TEA": n_nao},
        "matriz": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
        "soma_matriz_igual_n": tp + tn + fp + fn == n,
        "consistentes_totais": (tp + fn == n_tea) and (tn + fp == n_nao),
        "acuracia_cache": p_cache,
        "acuracia_recalculada": acuracia_calc,
        "acuracia_compativel": perto(p_cache, acuracia_calc),
        "sensibilidade": {"cache": numero(celulas, "T151"), "recalculada": sens_calc,
                          "compativel": perto(numero(celulas, "T151"), sens_calc)},
        "especificidade": {"cache": numero(celulas, "T152"), "recalculada": esp_calc,
                           "compativel": perto(numero(celulas, "T152"), esp_calc)},
        "vpp": {"cache": numero(celulas, "T153"), "recalculada": vpp_calc,
                "compativel": perto(numero(celulas, "T153"), vpp_calc)},
        "vpn": {"cache": numero(celulas, "T154"), "recalculada": vpn_calc,
                "compativel": perto(numero(celulas, "T154"), vpn_calc)},
        "ic_cache": {"inf": numero(celulas, "T155"), "sup": numero(celulas, "T156")},
        "ic_wilson_padrao": {"inf": wil_pad[0], "sup": wil_pad[1]},
        "ic_formula_textual": {"inf": wil_txt[0], "sup": wil_txt[1]},
        "cache_compativel_com_wilson_padrao":
            perto(numero(celulas, "T155"), wil_pad[0]) and perto(numero(celulas, "T156"), wil_pad[1]),
        "cache_compativel_com_formula_textual":
            perto(numero(celulas, "T155"), wil_txt[0]) and perto(numero(celulas, "T156"), wil_txt[1]),
        "formulas_ic_texto": {
            "inf": celulas.get("T155", {}).get("formula"),
            "sup": celulas.get("T156", {}).get("formula"),
        },
        "perda_eqm_treino": numero(celulas, "R16"),
        "um_menos_eqm": numero(celulas, "S16"),
        "aviso_cache": texto(celulas, "T157"),
        "argmax_confirmacoes": "%d/%d" % (argmax_ok, argmax_total),
        "argmax_sem_classe": argmax_sem_classe,
    }


def main():
    if not os.path.exists(WORKBOOK):
        print("workbook ausente: " + WORKBOOK, file=sys.stderr)
        return 1
    with zipfile.ZipFile(WORKBOOK) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sr = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sr.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % M)))
        planilhas = carregar_planilhas(z)
        abas = []
        for nome in sorted(planilhas):
            cel = carregar_celulas(z, planilhas[nome], shared)
            abas.append(analisar_aba(nome, cel))
    if len(abas) != 5:
        print("esperadas 5 abas de RNA; encontradas %d" % len(abas), file=sys.stderr)
        return 1

    relatorio = {
        "gerado_em": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "arquivo": os.path.relpath(WORKBOOK, os.path.dirname(AUD)),
        "sha256": sha256(WORKBOOK),
        "classificacao": "DIAGNOSTICO DO ESTADO ORIGINAL - cache gerado antes da correcao de K20; Solver NAO reexecutado",
        "metodo": {
            "acuracia": "(TP+TN)/n",
            "sensibilidade": "TP/(TP+FN)",
            "especificidade": "TN/(TN+FP)",
            "vpp": "TP/(TP+FP)",
            "vpn": "TN/(TN+FN)",
            "wilson_padrao": "(p+z^2/(2n))/(1+z^2/n) +/- z*sqrt(p(1-p)/n + z^2/(4n^2))/(1+z^2/n), z=1.96",
            "wilson_textual": "(p+z^2/(2n))/(1+z^2/n) +/- z*sqrt((p(1-p)+z^2/(4n^2))/n)/(1+z^2/n), z=1.96",
            "tolerancia": TOL,
        },
        "abas": abas,
    }
    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump(relatorio, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    linhas = [
        "# M4 — Métricas recomputadas do cache",
        "",
        "**Classificação:** " + relatorio["classificacao"],
        "",
        "**Arquivo:** `%s` · **SHA-256:** `%s`" % (relatorio["arquivo"], relatorio["sha256"]),
        "",
        "**Gerado em:** " + relatorio["gerado_em"] + " · **Script:** `recomputar_cache.py`",
        "",
        "| Aba | n | TP | TN | FP | FN | Acurácia cache | Recalculada | Sens. | Esp. | EQM (R16) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a in abas:
        m = a["matriz"]
        linhas.append("| %s | %d | %d | %d | %d | %d | %.4f | %.4f | %.4f | %.4f | %.6f |" % (
            a["aba"].replace("|", "\\|"), a["n"], m["TP"], m["TN"], m["FP"], m["FN"],
            a["acuracia_cache"], a["acuracia_recalculada"],
            a["sensibilidade"]["recalculada"], a["especificidade"]["recalculada"],
            a["perda_eqm_treino"]))
    linhas += [
        "",
        "## Divergência detectada na fórmula do intervalo de confiança",
        "",
        "Em todas as abas, o valor em cache de `T155/T156` é compatível com a forma padrão da "
        "fórmula de Wilson. A fórmula **textualmente presente** nas células, se avaliada, produz "
        "um intervalo mais estreito. O script calcula as duas variantes e registra a comparação "
        "no JSON. Não se afirma qual versão é a correta sem o histórico de edição do arquivo.",
        "",
        "| Aba | IC cache | Wilson padrão | Fórmula textual da célula | Compatível com cache |",
        "|---|---|---|---|---|",
    ]
    for a in abas:
        c = a["ic_cache"]
        w = a["ic_wilson_padrao"]
        t = a["ic_formula_textual"]
        rot = "padrão" if a["cache_compativel_com_wilson_padrao"] else (
            "textual" if a["cache_compativel_com_formula_textual"] else "nenhuma")
        linhas.append("| %s | [%.6f, %.6f] | [%.6f, %.6f] | [%.6f, %.6f] | %s |" % (
            a["aba"].replace("|", "\\|"), c["inf"], c["sup"], w["inf"], w["sup"],
            t["inf"], t["sup"], rot))
    linhas += [
        "",
        "## Limites",
        "",
        "- Estes números descrevem o **cache original**, não o modelo após a correção de `K20`.",
        "- O Solver não foi reexecutado neste ambiente.",
        "- `n=30` por aba; intervalos são largos e não autorizam generalização.",
        "- A abertura do workbook no Excel com `fullCalcOnLoad` atualizará os valores; o aviso em `T157` deve ser preservado.",
        "",
    ]
    with open(MD_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))

    print("JSON: " + JSON_OUT)
    print("MD:   " + MD_OUT)
    print("Abas processadas: %d" % len(abas))
    for a in abas:
        print("  %s | n=%d | ac=%.4f | matriz ok=%s | IC=padrão:%s textual:%s | argmax=%s" % (
            a["aba"], a["n"], a["acuracia_cache"], a["soma_matriz_igual_n"],
            a["cache_compativel_com_wilson_padrao"], a["cache_compativel_com_formula_textual"],
            a["argmax_confirmacoes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
