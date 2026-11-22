Attribute VB_Name = "modSolverRNA"
Option Explicit

' ============================================================================
' Proposta de substituicao de Módulo3.SOLVER1 (SPEC-AUD-TEA-001).
' NAO foi aplicada ao .xlsm original.
' Pre-requisito: referencia "Solver" habilitada (Ferramentas > Referencias).
' Uso: selecione uma aba "Rede Neural |..." e execute SolverRNA_Executar.
' ============================================================================

Private Const CELULA_OBJETIVO As String = "$R$16"
Private Const CELUNAS_VARIAVEIS As String = _
    "$W$19:$AA$19,$W$22:$AA$22,$W$25:$AA$25,$W$28:$AA$28," & _
    "$AE$19:$AI$19,$AE$22:$AI$22,$AE$25:$AI$25"
Private Const CELULA_LOG As String = "$AM$16"

Public Sub SolverRNA_Executar()
    Dim ws As Worksheet
    Dim statusSolver As Long
    Dim mensagem As String

    On Error GoTo Falha
    Set ws = ActiveSheet

    If Not SheetEhRedeNeural(ws) Then
        MsgBox "Selecione uma aba 'Rede Neural |...' antes de executar.", _
               vbExclamation, "Solver RNA"
        Exit Sub
    End If

    Application.ScreenUpdating = False

    ' Limpa estado residual do Solver: evita herdar opcoes de execucoes anteriores.
    SolverReset

    ' MaxMinVal:=2  -> minimizar R16 (erro quadratico medio).
    ' Engine:=1     -> GRG Nonlinear.
    SolverOk SetCell:=CELULA_OBJETIVO, _
             MaxMinVal:=2, _
             ValueOf:=0, _
             ByChange:=CELUNAS_VARIAVEIS, _
             Engine:=1, _
             EngineDesc:="GRG Nonlinear"

    ' StepThru:=False evita pausa/passo-a-passo.
    ' AssumeNonNeg:=False e necessario: pesos podem ser negativos.
    SolverOptions MaxTime:=0, _
                  Iterations:=0, _
                  Precision:=0.000000001, _
                  Convergence:=0.000000000001, _
                  StepThru:=False, _
                  Scaling:=True, _
                  AssumeNonNeg:=False, _
                  Derivatives:=1

    ' RandomSeed=1 preserva a reprodutibilidade declarada no estudo.
    SolverOptions PopulationSize:=900, _
                  RandomSeed:=1, _
                  MutationRate:=0.075, _
                  Multistart:=True, _
                  RequireBounds:=False, _
                  MaxTimeNoImp:=300

    ' UserFinish:=True suprime a caixa de dialogo "Resultados do Solver".
    statusSolver = SolverSolve(UserFinish:=True)

    Select Case statusSolver
        Case 1:  mensagem = "Solucao encontrada"
        Case 0:  mensagem = "Tempo esgotado antes da convergencia"
        Case 2:  mensagem = "Parou por limite de iteracoes/subproblemas"
        Case 3:  mensagem = "Execucao interrompida pelo usuario"
        Case 4:  mensagem = "Solucao inviavel"
        Case 5:  mensagem = "Modelo linear: usar motor Simplex LP"
        Case Else: mensagem = "Status nao documentado: " & statusSolver
    End Select

    With ws.Range(CELULA_LOG)
        .Value = "Solver: " & mensagem & _
                 " | status=" & statusSolver & _
                 " | seed=1 | " & Format(Now, "yyyy-mm-dd hh:nn:ss")
        .Columns.AutoFit
    End With

Sair:
    Application.ScreenUpdating = True
    Exit Sub

Falha:
    mensagem = "Erro " & Err.Number & ": " & Err.Description
    ws.Range(CELULA_LOG).Value = "Solver FALHOU: " & mensagem
    MsgBox mensagem, vbCritical, "Solver RNA"
    Resume Sair
End Sub

Private Function SheetEhRedeNeural(ByRef ws As Worksheet) As Boolean
    SheetEhRedeNeural = (Left$(ws.Name, 12) = "Rede Neural ")
End Function
