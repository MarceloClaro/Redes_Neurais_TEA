"""Gate SDD/TDD do marco M3 — projeto metodologico e etica.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m3.py
Somente leitura. Nao altera artefatos, nao consulta rede e nao inventa evidencia.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))

METODO = os.path.join(HERE, "M3_metodo_etica.md")
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"

DOIS_APROVADOS = {
    "10.1136/bmj-2023-078378", "10.1136/bmj.q902", "10.1186/s12916-014-0241-z",
    "10.7326/M18-1376", "10.1016/j.jclinepi.2025.112118", "10.1038/s41598-020-69920-0",
    "10.1145/3510003.3510163", "10.1002/smr.1787", "10.1002/smr.*",
    "10.48550/arxiv.0809.3613", "10.48550/arxiv.1703.09785",
    "10.48550/arxiv.0802.3479", "10.1109/ase.2003.1240305",
    "10.1109/IJCNN.1991.155504", "10.48550/arxiv.2604.20070",
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


artefatos = [METODO, SPEC, ORIGINAL,
             os.path.join(HERE, "M2_sintese_lacuna.md"),
             os.path.join(HERE, "verificar_m2.py")]
missing = [p for p in artefatos if not os.path.exists(p)]
check("G-01 artefatos M3 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

metodo = read(METODO)
norm = metodo.replace("**", "").replace("`", "")
low = norm.lower()

check("G-02 desenho com negacoes explicitas",
      all(k in metodo for k in ("Ensaio clínico", "Estudo de validação diagnóstica",
                                "Revisão sistemática", "Inferência causal")))
check("G-03 cinco niveis de unidade de analise",
      all(("N%d" % i) in metodo for i in range(1, 6)))
check("G-04 doze operacoes determinísticas",
      all(("OP-%02d" % i) in metodo for i in range(1, 13)))
check("G-05 diretrizes com decisao justificada",
      "não aplicada como checklist de conformidade" in low and
      "instrumento não aplicado" in low and
      "não aplicáveis" in low and
      "não aplicável" in low)
check("G-06 checklist proprio com proveniencia",
      "checklist próprio de auditoria computacional" in low and
      all(k in low for k in ("hash", "data", "executor", "versão do python", "comando exato")))
check("G-07 pendencias eticas marcadas",
      len(re.findall(r"\[A CONFIRMAR\]", metodo)) >= 8)
check("G-08 nenhuma affirmacao de aprovacao etica",
      "aprovada" not in low or "[A CONFIRMAR]" in metodo)
check("G-09 Solver nao reexecutado",
      "Solver não reexecutado neste ambiente" in metodo and "seed=1" in metodo)
check("G-10 cache como diagnostico",
      "diagnóstico do estado original" in metodo)
check("G-11 IC anterior nao reutilizado",
      "não foi reproduzido neste marco" in metodo)
check("G-12 matriz de riscos com status",
      "Matriz de riscos e mitigação" in metodo and
      all(k in metodo for k in ("Mitigado", "Pendente", "Parcialmente mitigado")))
check("G-13 criterios de aceitação AC-M3",
      all(("AC-M3-%d" % i) in metodo for i in range(1, 8)))
check("G-14 hashes e contagens do artefato",
      "1c4c94ab" in metodo and "3320701b" in metodo and
      all(k in metodo for k in ("25 planilhas", "36 gráficos", "55 desenhos",
                                "22 mídias", "104 tabelas")))
check("G-15 referencias cruzadas M2",
      all(("F%02d" % i) in metodo for i in range(1, 5)))
dois_encontrados = set()
for bruto in re.findall(r"10\.\d{4,9}/\S+", norm):
    dois_encontrados.add(bruto.rstrip(";,.\""))
dois_invalidos = sorted(dois_encontrados - DOIS_APROVADOS)
check("G-16 nenhum DOI inventado", not dois_invalidos, ", ".join(dois_invalidos))
check("G-17 sem promessa editorial",
      not any(p in low for p in ("qualis a1 garantido", "aceite garantido",
                                 "nota 10 garantida", "publicação garantida")))
cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", metodo)))
check("G-18 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
check("G-19 original preservado",
      sha256(ORIGINAL) == HASH_ORIGINAL, sha256(ORIGINAL)[:12])
check("G-20 pendencias de M4 declaradas",
      all(k in metodo for k in ("30 imagens", "log do Solver", "Recalcular estatísticas")))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
