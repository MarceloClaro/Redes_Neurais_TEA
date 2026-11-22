"""Gate SDD/TDD do marco M7 — auditoria final e banca simulada.

Uso: .venv/bin/python producao_cientifica/auditoria/artigo/verificar_m7.py

Somente leitura. Confere que as sete auditorias existem, que o relatorio e
geravel de forma deterministica, que a falha das delegacoes esta registrada sem
ter sido contabilizada como revisao externa, que os typos conhecidos foram
corrigidos e que nenhuma pendencia, limite ou promessa indevida foi alterado.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import montar_m7  # noqa: E402

AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(AUD))
RELATORIO = os.path.join(HERE, "RELATORIO_M7.md")
SPEC = os.path.join(ROOT, "specs", "SPEC-935-R1282-auditoria-metodologica-rna-tea.md")
MANUSCRITO = os.path.join(HERE, "MANUSCRITO_ABNT.md")
GATE_M6 = os.path.join(HERE, "verificar_m6.py")
CORRIGIDO = os.path.join(AUD, "Redes_Neurais_TEA_Dataset_VBA_corrigido.xlsm")
ORIGINAL = os.path.join(os.path.dirname(AUD), "Redes Neurais - TEA Dataset VBA.xlsm")
GERADOR = os.path.join(HERE, "montar_m7.py")

resultados = []


def check(nome, condicao, detalhe=""):
    ok = bool(condicao)
    resultados.append((nome, ok))
    print(("PASS " if ok else "FAIL ") + nome + (" | " + detalhe if detalhe else ""))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


artefatos = [RELATORIO, SPEC, MANUSCRITO, GATE_M6, CORRIGIDO, ORIGINAL, GERADOR]
artefatos += [os.path.join(HERE, m) for m in montar_m7.MODULOS]
missing = [p for p in artefatos if not os.path.exists(p)]
check("H-01 artefatos M7 e anteriores presentes", not missing, ", ".join(missing))
if missing:
    print("\nResumo: %d/%d" % (sum(ok for _, ok in resultados), len(resultados)))
    sys.exit(1)

relatorio = read(RELATORIO)
modulos = {m: read(os.path.join(HERE, m)) for m in montar_m7.MODULOS}
espec = read(SPEC)
manuscrito = read(MANUSCRITO)
tudo = relatorio.lower()

# H-02/H-03 determinismo
esperado = montar_m7.CABECALHO
for modulo in montar_m7.MODULOS:
    esperado += modulos[modulo].rstrip() + "\n"
    esperado += "\n---\n\n"
esperado += montar_m7.RODAPE.strip() + "\n"
check("H-02 relatorio gerado de forma deterministica", relatorio == esperado)
check("H-03 ordem das sete auditorias fixa",
      montar_m7.MODULOS == [
          "M7_01_auditoria_coerencia.md",
          "M7_02_auditoria_integridade.md",
          "M7_03_auditoria_alegacoes.md",
          "M7_04_auditoria_bibliografica.md",
          "M7_05_auditoria_reprodutibilidade.md",
          "M7_06_auditoria_abnt.md",
          "M7_07_banca_simulada.md",
      ])

# H-04 sete auditorias presentes e tituladas
titulos = [
    "# Auditoria final 1 — Coerência interna",
    "# Auditoria final 2 — Integridade da cadeia de evidências",
    "# Auditoria final 3 — Força de alegação e contraprovas",
    "# Auditoria final 4 — Bibliografia, citações e ABNT",
    "# Auditoria final 5 — Reprodutibilidade, proveniência e ética",
    "# Auditoria final 6 — Apresentação ABNT",
    "# Banca simulada — perguntas e respostas ancoradas",
]
check("H-04 sete auditorias tituladas e na ordem",
      all(t in relatorio for t in titulos) and
      [relatorio.index(t) for t in titulos] == sorted(relatorio.index(t) for t in titulos))

# H-05 falha das delegacoes registrada sem contar como revisao externa
check("H-05 falha das cinco delegações registrada",
      "cinco delegações" in tudo and "restrição regional" in tudo and
      "assinatura ativa" in tudo and "falharam antes da execução" in tudo)
check("H-06 nenhuma delegacao contada como auditoria externa",
      "nenhuma delas produziu artefato" in tudo and
      "nenhuma é contabilizada como auditoria externa" in tudo and
      "não houve revisores externos reais" in tudo and
      "não houve auditoria externa" in tudo)

# H-07 conteúdo das auditorias
coerencia = modulos["M7_01_auditoria_coerencia.md"]
integridade = modulos["M7_02_auditoria_integridade.md"]
alegacoes = modulos["M7_03_auditoria_alegacoes.md"]
biblio = modulos["M7_04_auditoria_bibliografica.md"]
reprod = modulos["M7_05_auditoria_reprodutibilidade.md"]
abnt = modulos["M7_06_auditoria_abnt.md"]
banca = modulos["M7_07_banca_simulada.md"]

check("H-07 coerencia com 12+ itens e veredito",
      coerencia.count("| coerente |") >= 12 and
      "## Divergências encontradas" in coerencia and
      "## Veredito circunscrito" in coerencia and
      "não substitui revisão por pares" in coerencia)
check("H-08 integridade com hashes e inventario",
      all(h in integridade for h in (
          "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd",
          "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475",
          "25 planilhas", "36 gráficos", "55 desenhos", "22 mídias",
          "104 tabelas", "xl/calcChain.xml")) and
      "## Divergências que permanecem em aberto" in integridade and
      "## Veredito circunscrito" in integridade)
check("H-09 alegoes com escada, contraprovas e ajuste",
      all(n in alegacoes for n in ("**E0**", "**E1**", "**E2**", "**E3**", "**E4**", "**E5**")) and
      "Contraprova que a derrubaria" in alegacoes and
      "destina-se a evitar" in alegacoes and "is intended to prevent" in alegacoes and
      "24/24" in alegacoes and "33/33" in alegacoes)
check("H-10 bibliografia F01-F13 e contagem",
      all("F%02d" % i in biblio for i in range(1, 14)) and
      "13 fontes citadas no corpo" in biblio and
      "13 entradas na lista de referências" in biblio and
      "1991" in biblio and "2003" in biblio and
      "10.1145/3678890.3678909" in biblio)
check("H-11 reprodutibilidade com 14+ itens e secoes",
      reprod.count("| rastreável |") + reprod.count("| pendente |") +
      reprod.count("| parcial |") >= 14 and
      all(s in reprod for s in (
          "## O que é reproduzível", "## O que não é reproduzível neste ambiente",
          "## Recomendações antes de submissão",
          "não substitui revisão humana")))
check("H-12 ABNT com NBRs, secoes e veredito",
      all(n in abnt for n in ("NBR 14724", "NBR 6023", "NBR 10520")) and
      "## Ajustes obrigatórios antes da conversão" in abnt and
      "## Ajustes condicionais ao periódico" in abnt and
      "## Veredito circunscrito" in abnt and
      "auditoria de documento, não aceite editorial" in abnt)

# H-13 banca
revisores = ["## Revisor 1 — Metodologia", "## Revisor 2 — Reprodutibilidade e estatística",
             "## Revisor 3 — Bibliografia e ABNT"]
check("H-13 banca com tres revisores e perguntas ancoradas",
      all(r in banca for r in revisores) and
      banca.count("Resposta ancorada:") >= 15 and
      "## Perguntas sem resposta satisfatória no estado atual" in banca and
      "simulação heurística" in banca)
check("H-14 nenhuma pergunta da banca ficou sem resposta no corpo",
      banca.count("**P") == banca.count("Resposta ancorada:"),
      "%d perguntas / %d respostas" %
      (banca.count("**P"), banca.count("Resposta ancorada:")))

# H-15 typos corrigidos
todo_texto = relatorio + manuscrito + espec
typos = ["manuscripto", "above a evidência", "often impõem", "dependents do usuario",
         "herramienta", "aplikado"]
presentes = [t for t in typos if t in todo_texto]
check("H-15 typos conhecidos corrigidos", not presentes, ", ".join(presentes))

# H-16 pendencias e limites
check("H-16 pendencias centrais preservadas",
      all(s in todo_texto for s in (
          "[A CONFIRMAR", "Solver não foi reexecutado", "30 imagens",
          "não há resultado pós-correção", "periódico-alvo")))
# As secoes que listam alegoes deliberately mantidas FORA do texto citam as
# proprias frases proibidas para documentar a decisao; devem ser excluidas da
# varredura para que o gate nao confunda enumeracao de exclusao com afirmacao.
trecho_exclusao = "## alegações deliberadamente mantidas fora do texto"
varredura = tudo.split(trecho_exclusao)[0] if trecho_exclusao in tudo else tudo
check("H-17 sem resultado pos-correcao ou validade clinica afirmada",
      not any(p in varredura for p in (
          "desempenho validado do modelo corrigido", "validade diagnóstica comprovada",
          "acurácia validada do modelo corrigido", "resultado pós-correção obtido")))
check("H-18 sem promessa editorial",
      not any(p in varredura for p in (
          "qualis a1 garantido", "aceite garantido", "nota 10 garantida",
          "aprovado pelo periódico", "primeiro protocolo de auditoria de planilhas")))
check("H-19 diretrizes sem conformidade afirmada",
      "conformidade com TRIPOD" not in tudo and
      "não como lista de conformidade" in manuscrito.lower())

# H-20 numeros e hashes
numeros = [
    "1c4c94ab6fc286feddd743b38eafb5b1220f616a7a8a5375e011f5d5bf953dcd",
    "3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475",
    "0,6333", "0,9000", "0,743786", "0,965401", "0,758863", "0,950323",
    "10/10", "22/22", "14/14", "23/23", "20/20", "24/24", "33/33",
    "24/24 e 33/33",
]
ausentes = [n for n in numeros if n not in relatorio]
check("H-20 hashes e numeros auditaveis preservados", not ausentes, ", ".join(ausentes))

# H-21 gate M6, SPEC e AC-15
check("H-21 gate M6 e spec rastreaveis",
      "verificar_m6.py" in espec and "33/33" in espec and os.path.exists(GATE_M6))
check("H-22 AC-15 e M7 registrados na SPEC",
      "AC-15" in espec and "M0 a M7 entregues" in espec and
      "verificar_m7.py" in espec)

# H-23 idioma
cjk = sorted(set(re.findall(r"[\u4e00-\u9fff]", relatorio)))
check("H-23 sem caracteres estranhos ao idioma", not cjk, "".join(cjk))
estranhos = re.findall(
    r"\b(?:after|during|however|therefore|summary|toutes|aplikado|herramienta|frameworks|often|dependents)\b",
    tudo,
)
check("H-24 sem palavras soltas em outro idioma", not estranhos, ", ".join(sorted(set(estranhos))))

print("\nResumo: %d/%d verificacoes positivas" %
      (sum(ok for _, ok in resultados), len(resultados)))
sys.exit(0 if all(ok for _, ok in resultados) else 1)
