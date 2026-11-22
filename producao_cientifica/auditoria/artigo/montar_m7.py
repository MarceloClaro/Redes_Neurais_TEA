"""Monta o RELATORIO_M7.md a partir das sete auditorias finais.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/montar_m7.py

Deterministico: nao inclui data/hora nem informacao do ambiente. Os arquivos
de auditoria nao sao alterados em disco; apenas concatenados com um cabecalho
e um resumo executivo fixos. O arquivo gerado e verificado por verificar_m7.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "RELATORIO_M7.md")

MODULOS = [
    "M7_01_auditoria_coerencia.md",
    "M7_02_auditoria_integridade.md",
    "M7_03_auditoria_alegacoes.md",
    "M7_04_auditoria_bibliografica.md",
    "M7_05_auditoria_reprodutibilidade.md",
    "M7_06_auditoria_abnt.md",
    "M7_07_banca_simulada.md",
]

CABECALHO = """# Relatório M7 — Auditoria final e banca simulada

**Spec:** `specs/SPEC-935-R1282-auditoria-metodologica-rna-tea.md`
**Marco:** M7 — auditoria final, após M0 a M6 entregues e aprovados
**Orquestrador:** marceloclaro
**Status:** rascunho para revisão humana; nenhuma aprovação editorial, nota ou Qualis é declarada
**Original preservado:** SHA-256 `1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd`
**Cópia auditada (estado pré-r1291):** SHA-256 `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`

**Extensão R1291:** em 2026-11-22 a cópia corrigida recebeu a aba documental `AUDITORIA_M7`, sem alterar modelos, fórmulas ou VBA. Hash atual: SHA-256 `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`. O hash pré-r1291 citado nas auditorias abaixo identifica o estado nelas descrito. A cópia passou a ter 26 planilhas (25 originais mais a aba documental). A análise exploratória separada é diagnóstico do cache e não afirma desempenho do modelo corrigido.

## Resumo executivo

Sete auditorias finais foram executadas localmente: coerência interna, integridade da cadeia de evidências, força de alegação com contraprovas, bibliografia e ABNT, reprodutibilidade/proveniência/ética, apresentação ABNT e banca simulada. Cinco delegações a agentes especializados foram tentadas e falharam antes da execução — quatro por restrição regional do modelo OpenCode Go e uma por exigência de assinatura ativa. Nenhuma delas produziu artefato, e nenhuma é contabilizada como auditoria externa independente.

Não foram encontradas divergências internas entre pergunta, objetivos, métodos, resultados e conclusão. Permanecem pendências documentadas: causa da divergência do intervalo de confiança, anos de F11 e F12, exigência de abstract, parâmetros de diagramação do periódico, log do Solver, 30 imagens e seus dados de ética/proveniência, autoria, financiamento, conflitos e local de depósito. Três verbos de efeito não medido foram rebaixados para intenção de projeto; M5 e M6 foram regenerados e seus gates permanecem em 24/24 e 33/33.

A cadeia de gates foi reexecutada integralmente neste marco. O veredito é circunscrito à integridade documental e à reprodutibilidade da auditoria: não estabelece desempenho do modelo corrigido, validade diagnóstica, conformidade editorial ou aceite em periódico algum.

---

"""

RODAPE = """
---

## Veredito final circunscrito

O marco M7 consolida sete auditorias locais e uma banca simulada. As auditorias documentam integridade de hashes, comandos, gates, citações e formatação no estado atual do manuscrito, com pendências explicitamente marcadas. Não há revisão externa real, não houve reexecução do Solver, não houve integração das 30 imagens e não foi declarada qualquer aprovação editorial, Qualis, nota, aceite ou validade clínica. A entrega permanece sujeita a revisão humana e a confirmações dependentes do usuário e do periódico-alvo.
"""


def ler(nome):
    with open(os.path.join(HERE, nome), "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    faltando = [m for m in MODULOS if not os.path.exists(os.path.join(HERE, m))]
    if faltando:
        print("modulos ausentes: " + ", ".join(faltando), file=sys.stderr)
        return 1

    partes = [CABECALHO]
    for modulo in MODULOS:
        partes.append(ler(modulo).rstrip() + "\n")
        partes.append("\n---\n\n")
    partes.append(RODAPE.strip() + "\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(partes))
    print("gerado: " + OUT)
    print("modulos: %d" % len(MODULOS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
