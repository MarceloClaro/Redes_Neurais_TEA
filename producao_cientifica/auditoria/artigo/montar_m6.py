"""Monta a versao ABNT do manuscrito a partir dos modulos M5 e dos anexos M6.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/montar_m6.py

Deterministico: nao inclui data/hora nem informacao do ambiente. Os modulos M5
nao sao alterados em disco; apenas transformacoes explicitas sao aplicadas em
memoria. O arquivo gerado e verificado por verificar_m6.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MANUSCRITO_ABNT.md")

CORPO_M5 = [
    "M5_00_resumo.md",
    "M5_01_introducao.md",
    "M5_02_metodos.md",
    "M5_03_resultados.md",
    "M5_04_discussao.md",
    "M5_05_conclusao.md",
]
POS_TEXTUAIS = [
    "M6_01_referencias_abnt.md",
    "M5_07_declaracoes.md",
    "M6_02_auditoria_referencias.md",
    "M6_03_auditoria_alegacoes.md",
    "M6_04_notas_abnt.md",
]
TODOS = CORPO_M5 + POS_TEXTUAIS

CABECALHO = """# Auditoria metodológica de um pipeline de rede neural artificial em planilha eletrônica

**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Marco:** M6 — versão formatada para revisão humana
**Norma:** ABNT NBR 14724 (apresentação), NBR 6023 (referências) e NBR 10520 (citações)
**Status:** rascunho formatado; nenhuma aprovação editorial, nota ou Qualis é declarada
**Original preservado:** SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`
**Cópia auditada (estado pré-r1291):** SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`

**Extensão R1291:** em 2026-11-22 a cópia corrigida recebeu a aba documental `AUDITORIA_M7`, sem alterar modelos, fórmulas ou VBA. Hash atual: SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. O hash pré-r1291 citado nas seções abaixo identifica o estado descrito neste manuscrito. A cópia passou a ter 26 planilhas (25 originais mais a aba documental). A análise exploratória separada é diagnóstico do cache e não afirma desempenho do modelo corrigido.

---

"""

PLACEHOLDER_ABSTRACT = "[RASCUNHO — CONFIRMAR EXIGÊNCIA DE ABSTRACT PELO PERIÓDICO]"
PLACEHOLDER_FINAL = "[A CONFIRMAR EXIGÊNCIA DE ABSTRACT PELO PERIÓDICO]"


def transformar_corpo(texto):
    """Aplica apenas ajustes de formato e rotulagem, sem alterar conteudo."""
    texto = texto.replace(PLACEHOLDER_ABSTRACT, PLACEHOLDER_FINAL)
    linhas = texto.splitlines()
    saida = []
    for linha in linhas:
        if linha.startswith("| Aba | n | TP |"):
            saida.append("**Tabela 1 — Métricas recomputadas do cache pré-correção nas cinco abas de RNA.**")
            saida.append("")
        saida.append(linha)
        if linha.startswith("| " + chr(96) + "n19"):
            saida.append("")
            saida.append(
                "Fonte: elaborado pelos autores a partir de `M4_metricas_cache.json`; "
                "workbook corrigido com SHA-256 "
                "`3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`."
            )
    return "\n".join(saida).rstrip() + "\n"


def ler(nome):
    with open(os.path.join(HERE, nome), "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    faltando = [m for m in TODOS if not os.path.exists(os.path.join(HERE, m))]
    if faltando:
        print("modulos ausentes: " + ", ".join(faltando), file=sys.stderr)
        return 1

    partes = [CABECALHO]
    for indice, modulo in enumerate(TODOS):
        conteudo = ler(modulo)
        if indice < len(CORPO_M5):
            conteudo = transformar_corpo(conteudo)
        partes.append(conteudo.rstrip() + "\n")
        partes.append("\n---\n\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(partes).rstrip() + "\n")
    print("gerado: " + OUT)
    print("modulos: %d" % len(TODOS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
