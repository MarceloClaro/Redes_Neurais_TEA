"""Gate SDD/TDD do marco M2 — busca e auditoria bibliografica.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m2.py
Somente leitura. Nao altera artefatos, nao consulta rede e nao inventa evidencia.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))

PROTOCOLO = os.path.join(HERE, "M2_protocolo_busca.md")
FICHAS = os.path.join(HERE, "M2_fichas_auditoria.md")
SINTESE = os.path.join(HERE, "M2_sintese_lacuna.md")
M0 = os.path.join(HERE, "M0_contrato_academico.md")
M1 = os.path.join(HERE, "M1_problema_lacuna_arquitetura.md")
GATE_ANTERIOR = os.path.join(HERE, "verificar_m0_m1.py")
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"

DOIS_APROVADOS = {
    "10.1136/bmj-2023-078378",
    "10.1136/bmj.q902",
    "10.1186/s12916-014-0241-z",
    "10.7326/M18-1376",
    "10.1016/j.jclinepi.2025.112118",
    "10.1038/s41598-020-69920-0",
    "10.1145/3510003.3510163",
    "10.1002/smr.1787",
    "10.1002/smr.*",
    "10.48550/arxiv.0809.3613",
    "10.48550/arxiv.1703.09785",
    "10.48550/arxiv.0802.3479",
    "10.1109/ase.2003.1240305",
    "10.1109/IJCNN.1991.155504",
    "10.48550/arxiv.2604.20070",
    "10.1145/3678890.3678909",
}

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


artefatos = {
    "protocolo": PROTOCOLO, "fichas": FICHAS, "sintese": SINTESE,
    "M0": M0, "M1": M1, "gate anterior": GATE_ANTERIOR,
    "SPEC": SPEC, "original": ORIGINAL,
}
missing = [n for n, p in artefatos.items() if not os.path.exists(p)]
check("G-01 artefatos M2 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

protocolo, fichas, sintese = read(PROTOCOLO), read(FICHAS), read(SINTESE)
m1 = read(M1)
conteudo = protocolo + "\n" + fichas + "\n" + sintese
norm = conteudo.replace("**", "").replace("`", "")

check("G-02 datas de busca e consolidacao",
      "21 de novembro de 2026" in conteudo and "22 de novembro de 2026" in conteudo)
check("G-03 quatro vias publicas registradas",
      all(v in protocolo for v in ("Crossref", "PubMed", "OpenAlex", "Europe PMC")))
check("G-04 falha da busca web registrada",
      "HTTP 402" in protocolo)
check("G-05 bloqueio do arXiv registrado",
      "robots.txt" in protocolo)
check("G-06 nove consultas com contagens",
      all(("Q%d" % i) in protocolo for i in range(1, 10)))
check("G-07 consulta mais especifica com unico resultado",
      "audit spreadsheet neural network VBA OOXML" in protocolo and
      "10.1145/3678890.3678909" in conteudo)
check("G-08 doze fichas incluidas e duas excluidas",
      all(("F%02d" % i) in fichas for i in range(1, 15)))
check("G-09 duas exclusoes justificadas",
      fichas.count("Motivo da exclusão") >= 2)
check("G-10 PMIDs conferidos",
      all(p in conteudo for p in ("38626948", "25563062", "30596875", "32792540", "41448505")))
check("G-11 campos obrigatorios das fichas",
      all(k in fichas for k in ("Identificadores", "URL de auditoria", "Limitação de uso",
                                "Papel argumentativo", "Achado")))

dois_encontrados = set()
for bruto in re.findall(r"10\.\d{4,9}/\S+", norm):
    dois_encontrados.add(bruto.rstrip(";,.\""))
dois_invalidos = sorted(dois_encontrados - DOIS_APROVADOS)
check("G-12 nenhum DOI inventado", not dois_invalidos, ", ".join(dois_invalidos))

low = norm.lower()
check("G-13 lacuna circunscrita ao escopo",
      "não foi localizado nenhum trabalho" in low and
      ("circunscrito ao escopo pesquisado" in low or
       "circunscrita ao escopo pesquisado" in low))
check("G-14 limite de redacao explicitado",
      "não constitui prova de inexistência universal" in low)
check("G-15 nao e revisao sistematica",
      "não é revisão sistemática" in low and "prisma" in protocolo.lower())
check("G-16 fonte limítrofe registrada",
      "limítrofe" in norm and "10.48550/arxiv.2604.20070" in conteudo)
check("G-17 divergencia de ano preservada",
      "[A CONFIRMAR]" in fichas and "10.1109/IJCNN.1991.155504" in conteudo)
check("G-18 cache como diagnostico",
      "diagnóstico do estado original" in norm)
check("G-19 M1 atualizavel sem quebrar marco",
      "[A DEMONSTRAR EM M2]" in m1)
check("G-20 sem promessa editorial",
      not any(p in norm.lower() for p in ("qualis a1 garantido", "aceite garantido",
                                          "nota 10 garantida", "publicação garantida")))
cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", conteudo)))
check("G-21 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
check("G-22 original preservado",
      sha256(ORIGINAL) == HASH_ORIGINAL, sha256(ORIGINAL)[:12])
check("G-23 origem das afirmacoes limitada a resumos",
      "extraída do resumo" in norm and "texto integral" in norm)

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
