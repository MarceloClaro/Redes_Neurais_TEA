Attribute VB_Name = "Módulo4"
Sub telaCheia()
    Application.DisplayFullScreen = True
    Application.DisplayFormulaBar = False
    ActiveWindow.DisplayHeadings = False
    ActiveWindow.DisplayHorizontalScrollBar = False
    ActiveWindow.DisplayVerticalScrollBar = False
    ActiveWindow.DisplayWorkbookTabs = False
    Application.DisplayStatusBar = False
    Application.DisplayFunctionToolTips = False
    Application.Caption = "DASHBOARD"
    With ActiveWindow

    End With
    
End Sub

Sub telaNormal()
    Application.DisplayFullScreen = False
    Application.DisplayFormulaBar = True
    ActiveWindow.DisplayHeadings = True
    ActiveWindow.DisplayHorizontalScrollBar = True
    ActiveWindow.DisplayVerticalScrollBar = True
    ActiveWindow.DisplayWorkbookTabs = True
    Application.DisplayStatusBar = True
    Application.DisplayFunctionToolTips = True
    Application.Caption = ""
    With ActiveWindow

    End With
    
End Sub
'0YT7QAc0w
