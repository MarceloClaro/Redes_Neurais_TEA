# 3 Resultados

## 3.1 Falhas detectadas no original

A inspeção direta identificou falhas simultâneas nas cinco abas de RNA. A ativação em `K20` usava `MAX(0.1*z,z)`, enquanto `K21` usava `MAX(-0.1*z,z)`, produzindo assimetria de sinal em unidades que deveriam operar a mesma função. A célula rotulada como "Acurácia" na área de treino continha `S16 = SUM(-R16,1)`, isto é, `1 − EQM médio`, e não proporção de acertos. As células `AG35/AH35` aplicavam escala indevida por 100 a `R16/S16`. Nomes definidos conservavam resíduos de template e a entrada `Pesos` continha sete referências `#REF!`. O projeto VBA apresentava chamadas duplicadas a `SolverOk`, `StepThru:=True` e aspas tipográficas em comando.

Todas essas falhas foram detectadas sem abrir o arquivo no Excel. O gate do original registrou 10/10 verificações positivas, confirmando P1 e P2 nos termos definidos em M3.

## 3.2 Reparo e integridade estrutural

A cópia corrigida passou por 22/22 verificações no estado pré-r1291. Foram preservadas as contagens de 25 planilhas originais, 36 gráficos, 55 desenhos, 22 itens de mídia e 104 tabelas. A única parte removida do pacote foi `xl/calcChain.xml`, substituída pela exigência de recálculo mediante `fullCalcOnLoad="1"`. O hash da cópia nesse estado, `3320701be3003f2a797430984a4768f837b8622d1a6534452205c9ae027bb475`, diferia do original e permitia distinguir os dois estados. Após a extensão R1291, a aba documental `AUDITORIA_M7` elevou o total para 26 planilhas e o hash atual passou a ser `5dbc6e85cf0312007db88f21b1930403d95013f66844b333e1d35e1239b985cb`, sem alterar modelos, fórmulas ou VBA.

A ativação corrigida em `K20` passou a empregar `MAX(-0.1*z,z)`. O aviso em `T157` está presente nas cinco abas. A perda foi declarada como EQM médio e a classificação como softmax de três logits em `O:Q`, seguida de escolha da maior probabilidade. Não foi demonstrado ganho de desempenho decorrente do reparo, pois o Solver não foi reexecutado neste ambiente.

## 3.3 Métricas recomputadas do cache

A tabela seguinte apresenta os valores recomputados do cache. Todos são **diagnóstico do estado original**, gerados antes da correção de `K20`.

| Aba | n | TP | TN | FP | FN | Acurácia | Sens. | Esp. | EQM (R16) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `n120\|n40\|n116\|n86` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n116\|n50` | 30 | 9 | 13 | 2 | 6 | 0,7333 | 0,6000 | 0,8667 | 0,235776 |
| `n119\|n72\|n1\|n73` | 30 | 8 | 11 | 4 | 7 | 0,6333 | 0,5333 | 0,7333 | 0,198766 |
| `n120\|n40\|n119\|n72` | 30 | 12 | 12 | 3 | 3 | 0,8000 | 0,8000 | 0,8000 | 0,180387 |
| `n19\|n99\|n120\|n40\|` | 30 | 14 | 13 | 2 | 1 | 0,9000 | 0,9333 | 0,8667 | 0,197131 |

Em todas as abas, `TP+TN+FP+FN=n`, `TP+FN=15` e `TN+FP=15`, compatíveis com 15 registros `TEA` e 15 `NAO_TEA`. Acurácia, sensibilidade, especificidade, valor preditivo positivo e valor preditivo negativo armazenados no cache coincidiram com a recomputação dentro da tolerância de `1e-12`. A classe prevista em `R145:R174` coincidiu com o argmax dos três logits em `O:Q` em 30/30 registros por aba; nenhum argmax recaiu na terceira posição, cuja célula `C13` está vazia. O maior valor observado foi 0,9000 na aba `n19|n99|n120|n40|`.

Essa coerência é limitada ao próprio cache. Ela não implica que os números descrevam o modelo após a correção de `K20`.

## 3.4 Divergência na fórmula do intervalo de confiança

Ao recomputar o intervalo de confiança, o valor armazenado em `T155/T156` foi reproduzido exatamente pela forma padrão de Wilson. Na aba de maior cache, obteve-se `[0,743786; 0,965401]`. A fórmula textualmente presente nas células, avaliada literalmente com o mesmo `p` e `n`, produziu `[0,758863; 0,950323]`, intervalo mais estreito. O mesmo padrão ocorreu nas cinco abas.

Duas hipóteses permanecem não distinguidas: a fórmula foi editada sem recálculo, ou o cache provém de versão anterior da planilha. O artefato não contém histórico de edição que permita escolher entre elas. Não se afirmou qual versão é correta e o workbook não foi alterado por causa desse achado.

## 3.5 Evidência pendente

O log do Solver e as 30 imagens não foram integrados. Em consequência, não há resultado pós-correção neste manuscrito. A comparação entre cache e uma eventual reexecução será apresentada, quando houver evidência, como mudança de estado computacional, não como ganho clínico. A seleção de atributos ocorreu antes da separação treino/teste no desenho original; essa configuração é registrada como risco de vazamento de dados, sem afirmar que houve vazamento efetivo.
