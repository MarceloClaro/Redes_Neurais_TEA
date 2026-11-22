Attribute VB_Name = "Módulo3"
Sub SOLVER1()
    Dim s As Long
    On Error GoTo Falha
    SolverReset
    SolverOk SetCell:="$R$16", MaxMinVal:=2, ValueOf:=0, ByChange:= _
        "$W$19:$AA$19,$W$22:$AA$22,$W$25:$AA$25,$W$28:$AA$28,$AE$19:$AI$19,$AE$22:$AI$22,$AE$25:$AI$25", _
        Engine:=1, EngineDesc:="GRG Nonlinear"
    SolverOptions MaxTime:=0, Iterations:=0, Precision:=0.000000001, _
        Convergence:=0.000000000001, StepThru:=False, Scaling:=True, _
        AssumeNonNeg:=False, Derivatives:=1
    SolverOptions PopulationSize:=900, RandomSeed:=1, MutationRate:=0.075, _
        Multistart:=True, RequireBounds:=False, MaxTimeNoImp:=300
    s = SolverSolve(UserFinish:=True)
    ActiveSheet.Range("$AM$16").Value = "Solver status=" & s & " seed=1"
    Exit Sub
Falha:
    ActiveSheet.Range("$AM$16").Value = "Solver FALHOU: " & Err.Description
End Sub
'xxx
