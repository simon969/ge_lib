Attribute VB_Name = "mConsolidation"
Option Explicit
Private Type typefun
strName As String
strDescription As String
strCategory As Variant
End Type
Public Function init_Functions(Optional catName As String = "Geotech Consolidation")

Dim I As Integer
Dim strFunction As String
Dim strDescript As String
Dim strName As String
Dim vCat As String
Dim fun(10) As typefun

If Len(catName) = 0 Then catName = "Geotech Tunnels"

fun(1).strCategory = catName
fun(1).strName = "Terzaghi1D_SimonsMenzies"
fun(1).strDescription = "1D Consolifation in accordance with Terzaghi fro a Short Course in Foundation Engineering by NE Simons and BK Menzies 1982 "

fun(2).strCategory = catName
fun(2).strName = "Terzaghi1D_Craig"
fun(2).strDescription = "1D Consolifation in accordance with Terzaghi from Soil Mechanics 6th Edition by RF Craig 1997"

fun(3).strCategory = catName
fun(3).strName = "Terzaghi1D"
fun(3).strDescription = "1D Consolifation in accordance with Terzaghi select either RF Craig 1997 or Simons and Menzies 1982"

For I = 1 To 10
strFunction = fun(I).strName
strDescript = fun(I).strDescription
vCat = fun(I).strCategory

If Len(strFunction) > 0 Then
Application.MacroOptions Macro:=strFunction, Description:=strDescript, Category:=vCat
End If

Next I

End Function

Public Sub Main()

Test101


End Sub


Private Sub Test101()
Dim t1d As cTerzaghi1d_Craig

Set t1d = New cTerzaghi1d_Craig
With t1d

.Cv = 1
.Mv = 0.0001
.p1 = 100
.H = 5
.calc_dUProfileAllTime 100000, 10, 10
.Print_dUProfile
End With

Set t1d = Nothing

End Sub
Public Function Terzaghi1D(p1 As Double, H As Double, Cv As Double, time As Double, rhsteps As Range, Optional strMethod = "Simons") As Variant
Attribute Terzaghi1D.VB_Description = "1D Consolifation in accordance with Terzaghi select either RF Craig 1997 or Simons and Menzies 1982"
Attribute Terzaghi1D.VB_ProcData.VB_Invoke_Func = " \n24"

If InStr(UCase(strMethod), "SIMON") > 0 Then
Terzaghi1D = Terzaghi1D_SimonsMenzies(p1, H, Cv, time, rhsteps)
End If

If InStr(UCase(strMethod), "CRAIG") > 0 Then
Terzaghi1D = Terzaghi1D_Craig(p1, H, Cv, time, rhsteps)
End If

End Function
Public Function Terzaghi1D_SimonsMenzies(p1 As Double, H As Double, Cv As Double, time As Double, rhsteps As Range) As Variant
Attribute Terzaghi1D_SimonsMenzies.VB_Description = "1D Consolifation in accordance with Terzaghi fro a Short Course in Foundation Engineering by NE Simons and BK Menzies 1982 "
Attribute Terzaghi1D_SimonsMenzies.VB_ProcData.VB_Invoke_Func = " \n24"

'If p1 <= 0 Then Exit Function
If H <= 0 Then Exit Function
If Cv <= 0 Then Exit Function
If rhsteps Is Nothing Then Exit Function
If time < 0 Then Exit Function

Dim t1d As cTerzaghi1D_SimonsMenzies
Set t1d = New cTerzaghi1D_SimonsMenzies

With t1d
.Cv = Cv
.H = H
.p1 = p1
End With

Terzaghi1D_SimonsMenzies = t1d.calc_dUProfileTimeRange(time, rhsteps, 0)

End Function
Public Function Terzaghi1D_Craig(p1 As Double, H As Double, Cv As Double, time As Double, rhsteps As Range) As Variant
Attribute Terzaghi1D_Craig.VB_Description = "1D Consolifation in accordance with Terzaghi from Soil Mechanics 6th Edition by RF Craig 1997"
Attribute Terzaghi1D_Craig.VB_ProcData.VB_Invoke_Func = " \n24"

'If p1 <= 0 Then Exit Function
If H <= 0 Then Exit Function
If Cv <= 0 Then Exit Function
If rhsteps Is Nothing Then Exit Function
If time < 0 Then Exit Function
Dim t1d As cTerzaghi1d_Craig
Set t1d = New cTerzaghi1d_Craig
With t1d
.Cv = Cv
.H = H
.p1 = p1
End With

Terzaghi1D_Craig = t1d.calc_dUProfileTimeRange(time, rhsteps, 0)

End Function

