# 1 Introdução

Planilhas eletrônicas ocupam posição ambígua em ciência de dados e informática em saúde. São acessíveis, ubíquas e permitem prototipar modelos sem infraestrutura de programação, mas concentram dados, lógica de cálculo, macros, gráficos e resultados em um único arquivo. Essa concentração é simultaneamente a vantagem e o risco do ambiente: o que facilita a circulação do artefato também torna opacas camadas críticas de um pipeline de aprendizado de máquina, como a função de ativação, a função-objetivo e a definição das métricas exibidas. O uso de planilhas para simular redes neurais não é recente; já foi descrito como estratégia simples de prototipagem e ensino (ANTONINI, 2002 `[A CONFIRMAR]`).

Erros em planilhas são fáceis de introduzir e difíceis de detectar. A taxonomia de Panko mostra que categorias como omissão e dimensão de ciclo de vida são frequentemente simplificadas quando a taxonomia é reutilizada (PANKO, 2008). Em contexto científico, AlTarawneh e Thorne (2017) relataram que a ausência de projeto adequado e de treinamento aparece como fator de risco em pesquisa que depende de planilhas, com consequências potenciais graves para a confiabilidade de resultados. Experimentos sobre comportamento de revisores indicam que a quantidade de células inspecionadas correlaciona-se com o número de erros corrigidos, o que expõe o limite da inspeção humana espontânea (BISHOP; MCDAID, 2008).

Já existem mecanismos de verificação estática e de compreensão de planilhas. Ahmad et al. (2004) propuseram um sistema de tipos para detectar erros por unidade em planilhas, e Amalfitano et al. (2016) desenvolveram uma ferramenta para compreender aplicações VBA, extraindo dependências entre células e elementos de interface. Esses trabalhos estabelecem precedentes importantes, mas não emitem um gate de auditoria para um pipeline de RNA nem tratam da preservação do pacote OOXML após reparo.

Em paralelo, a literatura sobre modelos preditivos em saúde consolidou a exigência de relato transparente. A TRIPOD original estabeleceu recomendações mínimas para estudos de desenvolvimento e validação de modelos diagnósticos e prognósticos (COLLINS et al., 2015), e a TRIPOD+AI ampliou e atualizou essas recomendações para modelos que empregam aprendizado de máquina (COLLINS et al., 2024). A PROBAST oferece vocabulário para risco de viés, com destaque para falhas no domínio da análise (WOLFF et al., 2019), e instrumentos de aderência mostram que a avaliação de relato depende de critérios uniformes (DE KANTER et al., 2026). Essas fontes tratam do que deve ser informado e de como julgar relato ou risco de viés; não inspecionam fórmulas, streams VBA nem caches.

A reprodutibilidade de modelos de aprendizado profundo também é tema estabelecido. Renard et al. (2020) identificaram variabilidade em segmentação de imagens médicas e recomendaram descrição adequada do arcabouço, análise de fontes de variabilidade e avaliação eficiente de resultados. Chen et al. (2022) propuseram critérios e mecanismos para lidar com aleatoriedade de software e não determinismo de hardware. Entretanto, esses trabalhos pertencem a ecossistemas de arquiteturas de aprendizado profundo, não ao Excel com Solver.

## 1.1 Lacuna circunscrita

A busca auditada executada em 21 de novembro de 2026 em Crossref, PubMed, OpenAlex e Europe PMC, com as strings e contagens registradas em protocolo próprio, **não localizou** trabalho que proponha e execute, em pipeline de RNA hospedado em planilha `.xlsm`, um protocolo determinístico que combine: inspeção direta de OOXML e de streams VBA/OLE; detecção de erro de sinal em ativação, rótulo de métrica inconsistente, escala indevida e resíduos de template; reparo em cópia com preservação de gráficos, desenhos, mídia e tabelas; e separação explícita entre valor em cache e resultado validado. Essa ausência é **circunscrita ao escopo pesquisado e não constitui prova de inexistência universal**.

A fonte mais próxima localizada foi EXACT (AMALFITANO et al., 2016), voltada à compreensão de aplicações VBA. Um trabalho limítrofe sobre auditoria e controle de ações de agentes de IA em planilhas (SABOURI et al., 2026) torna etapas de execução auditáveis, mas não inspeciona o pacote OOXML, não lida com RNA em planilha e não repara artefato. Registrá-lo evita transformar uma lacuna circunscrita em negação absoluta.

## 1.2 Pergunta e objetivos

**Pergunta central.** Como falhas de implementação em um pipeline de RNA hospedado em planilha afetam a validade das métricas reportadas, e quais controles determinísticos permitem detectá-las e repará-las sem destruir o artefato original?

**Objetivo geral.** Propor e aplicar um protocolo determinístico de auditoria e reparo para pipelines de RNA em planilha, avaliando sua capacidade de preservar o artefato e de prevenir a comunicação enganosa de métricas.

**Objetivos específicos.** (i) inventariar falhas no original por verificações reproduzíveis; (ii) reparar em cópia as falhas identificadas e documentar as demais; (iii) recomputar métricas do cache com rótulo de proveniência e incerteza; (iv) verificar a integridade estrutural da cópia; (v) derivar recomendações de reporte para estudos que usem planilhas como ambiente de modelagem.

## 1.3 Contribuição

A contribuição é metodológica e delimitada. A partir de um workbook real, deriva-se e aplica-se um protocolo que demonstra três pontos: falhas de implementação são detectáveis por inspeção do pacote; o reparo pode preservar a estrutura do artefato; e métricas em cache exigem rotulagem de proveniência para não serem confundidas com resultado validado. Não se afirma ser o primeiro protocolo de auditoria de planilhas, nem se resolve a validade clínica do modelo auditado.
