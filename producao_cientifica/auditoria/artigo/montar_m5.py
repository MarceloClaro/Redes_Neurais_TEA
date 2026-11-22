"""Monta o rascunho consolidado do M5 a partir dos modulos IMRAD.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/montar_m5.py

Deterministico: nao inclui data/hora nem informacao do ambiente. A ordem dos
modulos e fixa. O arquivo gerado e verificado por verificar_m5.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MANUSCRITO_rascunho.md")

MODULOS = [
    "M5_00_resumo.md",
    "M5_01_introducao.md",
    "M5_02_metodos.md",
    "M5_03_resultados.md",
    "M5_04_discussao.md",
    "M5_05_conclusao.md",
    "M5_06_referencias.md",
    "M5_07_declaracoes.md",
]

CABECALHO = """# Manuscrito — rascunho modular IMRAD

**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Marco:** M5
**Norma prevista:** ABNT NBR 14724, NBR 6023 e NBR 10520
**Status:** rascunho para aprovacao; formatacao final em M6

**Extensao R1291:** em 2026-11-22 a copia corrigida recebeu a aba documental `AUDITORIA_M7`, sem alterar modelos, formulas ou VBA. Hash atual: SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. O hash `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475` citado nas secoes abaixo identifica o estado pre-r1291. A copia passou a ter 26 planilhas (25 originais mais a aba documental). A analise exploratoria separada e diagnostico do cache e nao afirma desempenho do modelo corrigido.

---

"""


def main():
    faltando = [m for m in MODULOS if not os.path.exists(os.path.join(HERE, m))]
    if faltando:
        print("modulos ausentes: " + ", ".join(faltando), file=sys.stderr)
        return 1
    partes = [CABECALHO]
    for modulo in MODULOS:
        with open(os.path.join(HERE, modulo), "r", encoding="utf-8") as fh:
            partes.append(fh.read().rstrip() + "\n")
        partes.append("\n---\n\n")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(partes).rstrip() + "\n")
    print("gerado: " + OUT)
    print("modulos: %d" % len(MODULOS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
