"""Gate SDD/TDD dos marcos M0 e M1 do artigo de auditoria metodologica.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m0_m1.py
Somente leitura. Nao altera artefatos e nao inventa evidencia.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
M0 = os.path.join(HERE, "M0_contrato_academico.md")
M1 = os.path.join(HERE, "M1_problema_lacuna_arquitetura.md")
ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"

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
    "SPEC": SPEC, "M0": M0, "M1": M1,
    "relatorio auditoria": os.path.join(AUD, "RELATORIO_AUDITORIA.md"),
    "relatorio aplicacao": os.path.join(AUD, "RELATORIO_APLICACAO.md"),
    "gate correcao": os.path.join(AUD, "verificar_correcao.py"),
    "copia corrigida": os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm"),
}
for nome, caminho in artefatos.items():
    if not os.path.exists(caminho) and nome not in ("SPEC",):
        check("G-00 artefato " + nome, False, "ausente")

missing = [n for n, p in artefatos.items() if not os.path.exists(p)]
check("G-00 artefatos prévios presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

spec, m0, m1 = read(SPEC), read(M0), read(M1)
conteudo = spec + m0 + m1

check("G-01 SPEC-935-R1282 presente",
      "SPEC-935-R1282" in spec and "Status:" in spec and "AC-1" in spec)
check("G-02 status proposicional",
      "proposed" in spec and "aguardando aprovação" in spec)
check("G-03 M0 com campos obrigatorios",
      all(k.lower() in m0.lower() for k in ("Pergunta provisória", "Tipo de estudo",
                                            "Corpus e dados", "Configuração editorial",
                                            "Mapa de entregáveis", "Limites éticos",
                                            "Riscos e pendências", "ABNT",
                                            "artigo científico")))
check("G-04 M0 com pendencias honestas",
      len(re.findall(r"\[A CONFIRMAR\]", m0)) >= 4)
check("G-05 M1 com secoes obrigatorias",
      all(k in m1 for k in ("Problema", "Lacuna", "Pergunta principal",
                            "Objetivos", "Construtos", "Unidade de análise",
                            "Delimitação", "Matriz de coerência")))
linha_matriz = next((l for l in m1.splitlines() if l.startswith("| Problema |")), "")
check("G-06 matriz com sete colunas",
      len([c for c in linha_matriz.split("|") if c.strip()]) == 7, linha_matriz[:80])
check("G-07 lacuna marcada como pendente", "[A DEMONSTRAR EM M2]" in m1)
proibidas = ["Qualis A1 garantido", "aceite garantido", "aprovação garantida",
             "nota 10 garantida", "publicação garantida"]
encontradas = [p for p in proibidas if p.lower() in conteudo.lower()]
check("G-08 sem promessa editorial", not encontradas, ", ".join(encontradas))
dois = re.findall(r"10\.\d{4,9}/\S+", conteudo)
check("G-09 nenhum DOI inventado", not dois, ", ".join(dois[:3]))
check("G-10 original preservado",
      sha256(ORIGINAL) == HASH_ORIGINAL, sha256(ORIGINAL)[:12])
check("G-11 risco de versionamento registrado",
      "gitignore" in m0.lower() and "version" in m0.lower())
check("G-12 cache rotulado como diagnostico",
      "diagnóstico" in spec and "diagnóstico" in m1)
m0_norm = m0.replace("**", "")
m1_norm = m1.replace("**", "")
check("G-13 nenhum resultado clinico afirmado",
      "não é estudo de validação diagnóstica" in m0_norm and
      "sem inferência" in m1_norm.lower())

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
