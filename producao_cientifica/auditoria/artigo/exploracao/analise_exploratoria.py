"""Analise exploratoria deterministica sobre o cache M4 (SPEC-935-R1291).

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/exploracao/analise_exploratoria.py

LIMITES DA ANALISE:
- Entrada UNICA: ../M4_metricas_cache.json. Nenhuma leitura do workbook.
- O cache nao contem scores/probabilidades individuais. Portanto, a secao
  sobre "limiares" compara CRITERIOS DE DECISAO aplicados a matriz de
  confusao observada. Nenhum limiar numerico e inventado.
- O bootstrap reamostra as CELLULAS da matriz dentro de cada classe
  verdadeira, nao os casos originais. E diagnostico de estabilidade do
  cache, nao inferencia populacional nem validacao clinica.
- Semente fixa. Mesma entrada produz bytes identicos; sem timestamp de
  execucao no conteudo gerado.
- Nunca afirma ganho de acuracia do modelo corrigido, validade diagnostica,
  calibracao, aceite editorial ou superioridade.
"""
import hashlib
import json
import math
import os
import random
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(BASE, os.pardir, "M4_metricas_cache.json")
SAIDA_JSON = os.path.join(BASE, "resultados_exploratorios.json")
SAIDA_MD = os.path.join(BASE, "RELATORIO_EXPLORACAO.md")

SEMENTE = 20261122
N_BOOTSTRAP = 2000
Z = 1.96
NIVEIS_PERTURBACAO = (0, 1, 2, 3)

TOL = 1e-12


def wilson(acertos, n, z=Z):
    """Intervalo de Wilson para uma proporcao; conjugado, determinstico."""
    if n <= 0:
        return 0.0, 0.0
    p = acertos / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    raio = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centro - raio), min(1.0, centro + raio)


def metricas(tp, tn, fp, fn):
    """Metricas derivadas apenas da matriz de confusao fornecida."""
    n = tp + tn + fp + fn
    sens = tp / (tp + fn) if (tp + fn) else 0.0
    esp = tn / (tn + fp) if (tn + fp) else 0.0
    vpp = tp / (tp + fp) if (tp + fp) else 0.0
    vpn = tn / (tn + fn) if (tn + fn) else 0.0
    den_f1 = 2 * tp + fp + fn
    return {
        "n": n,
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "acuracia": (tp + tn) / n if n else 0.0,
        "sensibilidade": sens,
        "especificidade": esp,
        "vpp": vpp,
        "vpn": vpn,
        "f1": (2 * tp / den_f1) if den_f1 else 0.0,
        "acuracia_balanceada": (sens + esp) / 2,
        "youden_j": sens + esp - 1,
    }


def percentil(valores, frac):
    """Percentil com interpolacao linear; determinstico, sem numpy."""
    if not valores:
        return 0.0
    ordenado = sorted(valores)
    if len(ordenado) == 1:
        return ordenado[0]
    pos = frac * (len(ordenado) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordenado[lo]
    return ordenado[lo] + (ordenado[hi] - ordenado[lo]) * (pos - lo)


def bootstrap_matriz(tp, tn, fp, fn, semente, n_boot):
    """Reamostragem binomial das celulas dentro de cada classe verdadeira.

    Classe TEA: tp acertos / fn erros. Classe NAO_TEA: tn acertos / fp erros.
    Os totais por classe (15 e 15) sao preservados. O resultado e a
    distribuicao amostral HIPOTETICA do cache, nao dos dados originais.
    """
    rng = random.Random(semente)
    n_tea = tp + fn
    n_nao = tn + fp
    p_tea = tp / n_tea if n_tea else 0.0
    p_nao = tn / n_nao if n_nao else 0.0
    acuracias, sensibilidades, especificidades = [], [], []
    for _ in range(n_boot):
        tp_b = sum(1 for _ in range(n_tea) if rng.random() < p_tea)
        tn_b = sum(1 for _ in range(n_nao) if rng.random() < p_nao)
        m = metricas(tp_b, tn_b, n_nao - tn_b, n_tea - tp_b)
        acuracias.append(m["acuracia"])
        sensibilidades.append(m["sensibilidade"])
        especificidades.append(m["especificidade"])
    return {
        "semente": semente,
        "replicas": n_boot,
        "acuracia": {
            "mediana": percentil(acuracias, 0.5),
            "ic_percentil_inf": percentil(acuracias, 0.025),
            "ic_percentil_sup": percentil(acuracias, 0.975),
        },
        "sensibilidade": {
            "mediana": percentil(sensibilidades, 0.5),
            "ic_percentil_inf": percentil(sensibilidades, 0.025),
            "ic_percentil_sup": percentil(sensibilidades, 0.975),
        },
        "especificidade": {
            "mediana": percentil(especificidades, 0.5),
            "ic_percentil_inf": percentil(especificidades, 0.025),
            "ic_percentil_sup": percentil(especificidades, 0.975),
        },
    }


def perturbacao_rotulo(tp, tn, fp, fn, k):
    """Cenario HIPOTETICO: k erros de rotulo incidindo sobre acertos.

    Assume-se explicitamente que os acertos TEA trocados viram FP e os
    acertos NAO_TEA trocados viram FN, com predicoes inalteradas. Nao e
    observacao; e analise de sensibilidade mecanica sobre a matriz.
    """
    if k > min(tp, tn):
        return None
    return metricas(tp - k, tn - k, fp + k, fn + k)


def fmt(x, casas=4):
    return ("%.*f" % (casas, x)).replace(".", ",")


def md_cell(texto):
    """Escapa pipes para que nomes de abas nao quebrem tabelas Markdown."""
    return str(texto).replace("\\", "\\\\").replace("|", "\\|")


def carregar():
    with open(ENTRADA, "r", encoding="utf-8") as fh:
        dados = json.load(fh)
    with open(ENTRADA, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    return dados, sha


def analisar(dados, sha_entrada):
    abas = []
    for item in dados["abas"]:
        m = item["matriz"]
        tp, tn, fp, fn = m["TP"], m["TN"], m["FP"], m["FN"]
        met = metricas(tp, tn, fp, fn)
        inf, sup = wilson(tp + tn, met["n"])
        ci = item["ic_wilson_padrao"]
        boot = bootstrap_matriz(tp, tn, fp, fn, SEMENTE, N_BOOTSTRAP)
        pert = {}
        for k in NIVEIS_PERTURBACAO:
            p = perturbacao_rotulo(tp, tn, fp, fn, k)
            if p is not None:
                pert[str(k)] = {
                    "acuracia": p["acuracia"],
                    "sensibilidade": p["sensibilidade"],
                    "especificidade": p["especificidade"],
                }
        abas.append({
            "aba": item["aba"],
            "n": met["n"],
            "contagem_rotulos": item["contagem_rotulos"],
            "matriz": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
            "metricas": met,
            "wilson_recomputado": {"inf": inf, "sup": sup},
            "wilson_no_cache": {"inf": ci["inf"], "sup": ci["sup"]},
            "wilson_recomputado_igual_cache":
                abs(inf - ci["inf"]) < TOL and abs(sup - ci["sup"]) < TOL,
            "bootstrap": boot,
            "sensibilidade_erro_rotulo": pert,
        })

    criterios = ("acuracia", "sensibilidade", "especificidade",
                 "f1", "acuracia_balanceada", "youden_j")
    ranqueamentos = {}
    for crit in criterios:
        ordem = sorted(abas, key=lambda a: (-a["metricas"][crit], a["aba"]))
        ranqueamentos[crit] = [{
            "posicao": i + 1,
            "aba": a["aba"],
            "valor": a["metricas"][crit],
        } for i, a in enumerate(ordem)]

    return {
        "spec": "SPEC-935-R1291",
        "classificacao": "DIAGNOSTICO DO CACHE - NAO e resultado validado do modelo corrigido",
        "fonte": "../M4_metricas_cache.json",
        "sha256_fonte": sha_entrada,
        "semente": SEMENTE,
        "replicas_bootstrap": N_BOOTSTRAP,
        "z_wilson": Z,
        "criterios_comparados": list(criterios),
        "abas": abas,
        "ranqueamentos": ranqueamentos,
        "declaracoes": [
            "Nao ha scores individuais no cache; nenhum limiar de probabilidade foi inventado.",
            "Criterios de decisao foram comparados sobre a matriz observada; a escolha do criterio muda o ranqueamento.",
            "Bootstrap reamostra celulas da matriz, nao casos originais; incerteza e diagnostica, nao populacional.",
            "Perturbacao de rotulo e cenario mecanico hipotetico incidindo sobre acertos.",
            "Nenhuma acuracia, sensibilidade ou especificidade aqui e validade diagnostica.",
            "Nenhum ganho de classificacao do modelo corrigido e afirmado; Solver nao foi reexecutado.",
        ],
    }


def gerar_markdown(res):
    L = []
    add = L.append
    add("# Analise exploratoria separada do cache M4 (SPEC-935-R1291)")
    add("")
    add("**Classificacao:** " + res["classificacao"] + ".")
    add("")
    add("**Fonte unica:** `%s` — SHA-256 `%s`." % (res["fonte"], res["sha256_fonte"]))
    add("")
    add("**Semente:** %d. **Replicas bootstrap:** %d. **z de Wilson:** %.2f."
        % (res["semente"], res["replicas_bootstrap"], res["z_wilson"]))
    add("")
    add("> Este documento e diagnostico do estado original em cache. Nao "
        "representa desempenho do arquivo corrigido, nao valida o modelo e "
        "nao autoriza conclusao clinica. Nenhum dado externo foi acrescentado.")
    add("")
    add("## 1. Metricas recompostas e intervalos")
    add("")
    add("| Aba | TP/TN/FP/FN | Acuracia | IC Wilson (recomp.) | IC Wilson (cache) | Coincide |")
    add("|---|---|---:|---|---|---|")
    for a in res["abas"]:
        m = a["matriz"]
        w = a["wilson_recomputado"]
        c = a["wilson_no_cache"]
        add("| %s | %d/%d/%d/%d | %s | [%s; %s] | [%s; %s] | %s |"
            % (md_cell(a["aba"]), m["TP"], m["TN"], m["FP"], m["FN"],
               fmt(a["metricas"]["acuracia"]), fmt(w["inf"]), fmt(w["sup"]),
               fmt(c["inf"]), fmt(c["sup"]),
               "sim" if a["wilson_recomputado_igual_cache"] else "nao"))
    add("")
    add("O intervalo de Wilson foi recomputado a partir de TP+TN e n. A "
        "coincidencia com o cache e esperada e nao constitui validacao "
        "externa; a divergencia com a formula textual do workbook permanece "
        "sem causa resolvida e nao foi alterada.")
    add("")
    add("## 2. Comparacao de criterios de decisao (nao de limiares)")
    add("")
    add("O cache nao contem probabilidades individuais. Em vez de inventar "
        "um limiar, comparou-se o ranqueamento das mesmas cinco matrizes sob "
        "criterios de decisao distintos. Isso mostra que a nocao de 'melhor' "
        "depende do objetivo, sem afirmar ganho de classificacao.")
    add("")
    nomes = {
        "acuracia": "Acuracia", "sensibilidade": "Sensibilidade",
        "especificidade": "Especificidade", "f1": "F1",
        "acuracia_balanceada": "Acuracia balanceada", "youden_j": "J de Youden",
    }
    add("| Criterio | 1o | 2o | 3o |")
    add("|---|---|---|---|")
    for crit in res["criterios_comparados"]:
        top = res["ranqueamentos"][crit][:3]
        add("| %s | %s (%s) | %s (%s) | %s (%s) |"
            % (nomes[crit],
               md_cell(top[0]["aba"]), fmt(top[0]["valor"]),
               md_cell(top[1]["aba"]), fmt(top[1]["valor"]),
               md_cell(top[2]["aba"]), fmt(top[2]["valor"])))
    add("")
    add("A mudanca de posicoes entre criterios e uma hipotese sobre prioridades "
        "de decisao. Para escolher um criterio seria necessario definir custos "
        "de falso positivo e falso negativo em contexto clinico, o que nao "
        "esta disponivel neste material.")
    add("")
    add("## 3. Bootstrap diagnostico das matrizes")
    add("")
    add("Reamostragem binomial dentro de cada classe verdadeira (15/15), com "
        "semente fixa. Intervalos percentis de 95% descrevem variabilidade do "
        "cache reamostrado, nao da populacao.")
    add("")
    add("| Aba | Acuracia mediana [IC p95] | Sens. mediana [IC p95] | Esp. mediana [IC p95] |")
    add("|---|---|---|---|")
    for a in res["abas"]:
        b = a["bootstrap"]
        add("| %s | %s [%s; %s] | %s [%s; %s] | %s [%s; %s] |"
            % (md_cell(a["aba"]),
               fmt(b["acuracia"]["mediana"]),
               fmt(b["acuracia"]["ic_percentil_inf"]),
               fmt(b["acuracia"]["ic_percentil_sup"]),
               fmt(b["sensibilidade"]["mediana"]),
               fmt(b["sensibilidade"]["ic_percentil_inf"]),
               fmt(b["sensibilidade"]["ic_percentil_sup"]),
               fmt(b["especificidade"]["mediana"]),
               fmt(b["especificidade"]["ic_percentil_inf"]),
               fmt(b["especificidade"]["ic_percentil_sup"])))
    add("")
    add("## 4. Sensibilidade a erro de rotulo (cenario hipotetico)")
    add("")
    add("Cenario mecanico: k erros de rotulo incidindo sobre acertos TEA e "
        "NAO_TEA, com predicoes inalterados. Acertos TEA trocados viram FP; "
        "acertos NAO_TEA trocados viram FN. Nao e observacao nem estimativa "
        "de erro real de anotacao.")
    add("")
    add("| Aba | k=0 | k=1 | k=2 | k=3 |")
    add("|---|---:|---:|---:|---:|")
    for a in res["abas"]:
        p = a["sensibilidade_erro_rotulo"]
        def celula_k(k):
            val = p.get(str(k), {}).get("acuracia")
            return fmt(val) if val is not None else "—"
        add("| %s | %s | %s | %s | %s |"
            % (md_cell(a["aba"]),
               fmt(p["0"]["acuracia"]),
               celula_k(1), celula_k(2), celula_k(3)))
    add("")
    add("## 5. Declaracoes")
    add("")
    for d in res["declaracoes"]:
        add("- " + d)
    add("")
    add("## 6. Proximo passo necessario para qualquer afirmativa de melhoria")
    add("")
    add("Somente uma reexecucao documentada do Solver no Excel — com versao, "
        "data, status de convergencia, semente, arquivo salvo e pesos finais "
        "com hash — permitiria comparar o estado corrigido com o cache. Ate "
        "la, toda discusao sobre 'melhor classificacao' permanece hipotetica.")
    add("")
    return "\n".join(L) + "\n"


def main():
    dados, sha = carregar()
    res = analisar(dados, sha)
    json_txt = json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    md_txt = gerar_markdown(res)
    with open(SAIDA_JSON, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json_txt)
    with open(SAIDA_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md_txt)
    print("SHA-256 fonte:", sha)
    print("Abas analisadas:", len(res["abas"]))
    print("JSON:", os.path.relpath(SAIDA_JSON))
    print("MD:", os.path.relpath(SAIDA_MD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
