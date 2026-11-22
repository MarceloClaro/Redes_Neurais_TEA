"""Gate SDD/TDD do marco M4 — dados, analise e resultados (parte executavel).

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m4.py
Somente leitura. Valida o JSON produzido por recomputar_cache.py contra o workbook real.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))

DADOS = os.path.join(HERE, "M4_dados_analise.md")
JSON = os.path.join(HERE, "M4_metricas_cache.json")
TABELA = os.path.join(HERE, "M4_tabela_metricas.md")
SCRIPT = os.path.join(HERE, "recomputar_cache.py")
CORRIGIDO = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
HASH_PRE_R1291 = "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475"
HASH_ATUAL = "5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb"
HASH_ORIGINAL = "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd"
BACKUP_PRE = os.path.join(AUD, "backup", "Redes_Neurais_TEA_Dataset_VBA_corrigido.pre_r1291.xlsm")

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


artefatos = [DADOS, JSON, TABELA, SCRIPT, CORRIGIDO, ORIGINAL,
             os.path.join(HERE, "M3_metodo_etica.md"),
             os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")]
missing = [p for p in artefatos if not os.path.exists(p)]
check("G-01 artefatos M4 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

dados, tabela, fonte = read(DADOS), read(TABELA), read(SCRIPT)
rel = json.loads(read(JSON))
abas = rel.get("abas", [])
check("G-02 JSON com cinco abas", len(abas) == 5, str(len(abas)))

check("G-03 denominador e matriz fechada",
      all(a["n"] == 30 and
          sum(a["matriz"].values()) == 30 and a["soma_matriz_igual_n"] for a in abas))
check("G-04 rotulos 15/15 e totais consistentes",
      all(a["contagem_rotulos"] == {"TEA": 15, "NAO_TEA": 15} and
          a["consistentes_totais"] for a in abas))
check("G-05 acuracia recomputada compativel",
      all(a["acuracia_compativel"] for a in abas))
check("G-06 metricas derivadas compativeis",
      all(a[k]["compativel"] for a in abas
          for k in ("sensibilidade", "especificidade", "vpp", "vpn")))
check("G-07 argmax confirma 30/30 por aba",
      all(a["argmax_confirmacoes"] == "30/30" and a["argmax_sem_classe"] == 0 for a in abas))
check("G-08 IC em cache reproduzido pela forma padrao",
      all(a["cache_compativel_com_wilson_padrao"] for a in abas))
check("G-09 divergencia da formula textual registrada",
      all(not a["cache_compativel_com_formula_textual"] and
          a["formulas_ic_texto"]["inf"] and a["formulas_ic_texto"]["sup"] for a in abas))
melhor = max(abas, key=lambda a: a["acuracia_cache"])
check("G-10 maior cache 0,9000 na aba esperada",
      abs(melhor["acuracia_cache"] - 0.9) < 1e-12 and "n19" in melhor["aba"],
      melhor["aba"])
check("G-11 hash historico do cache e hash atual conferem",
      rel["sha256"] == HASH_PRE_R1291 and
      os.path.exists(BACKUP_PRE) and sha256(BACKUP_PRE) == HASH_PRE_R1291 and
      sha256(CORRIGIDO) == HASH_ATUAL,
      "cache=%s atual=%s" % (rel["sha256"][:12], sha256(CORRIGIDO)[:12]))
check("G-12 classificacao de diagnostico no JSON e na tabela",
      "DIAGNOSTICO DO ESTADO ORIGINAL" in rel["classificacao"] and
      "DIAGNOSTICO DO ESTADO ORIGINAL" in tabela)
check("G-13 workbook nao alterado neste marco",
      sha256(ORIGINAL) == HASH_ORIGINAL)
check("G-14 Solver nao reexecutado",
      "Solver NAO reexecutado" in rel["classificacao"] and
      "Solver não reexecutado neste ambiente" in dados)
numeros_ic = ("0.743786", "0.965401", "0.758863", "0.950323")


def tem_numero(texto, numero):
    """Aceita tanto ponto quanto virgula decimal, sem perder a exigencia numerica."""
    return numero in texto or numero.replace(".", ",") in texto


check("G-15 divergencia do IC documentada com numeros",
      all(tem_numero(dados, n) and tem_numero(tabela, n) for n in numeros_ic))
check("G-16 tabela escapa pipes dos nomes de aba",
      tabela.count("Rede Neural \\|n") >= 10)
low_dados = dados.lower()
check("G-17 protocolo de evidencia pendente",
      all(k in low_dados for k in ("versão do excel", "status de convergência", "seed=1",
                                   "hash sha-256", "consentimento", "anonimização",
                                   "referência-padrão")))
check("G-18 pendencias marcadas", len(re.findall(r"\[A CONFIRMAR\]", dados)) >= 3)
check("G-19 sem promessa editorial",
      not any(p in dados.lower() for p in ("qualis a1 garantido", "aceite garantido",
                                           "nota 10 garantida", "publicação garantida")))
corpus = dados + tabela + fonte
cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", corpus)))
check("G-20 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
solto = re.findall(r"\b(?:after|during|summary|however|therefore)\b", corpus, re.I)
check("G-21 sem palavras soltas em outro idioma", not solto, ", ".join(solto))
check("G-22 limites explicitados",
      all(k in dados for k in ("não autorizam generalização", "não é resultado validado",
                               "data leakage", "Nenhuma alteração ao workbook")))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
