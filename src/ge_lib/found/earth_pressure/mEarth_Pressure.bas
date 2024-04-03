Attribute VB_Name = "mEarth_Pressure"
Option Explicit

Private Enum LateralAnalysisMethod
enumRankine = 0
enumCoulomb = 1
End Enum

Public Function init_Functions(Optional catName As String = "Geotech Earth Pressure")

If Len(catName) = 0 Then catName = "Geotech Earth Pressure"

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="calc_Rankine_Ka", Description:="calculate Rankine coefficient of active earth pressure, Ka after Rankine (1857)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_Kp", Description:="calculate Rankine coefficient of passive earth pressure, Kp after Rankine (1857)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_Kac", Description:="calculate Rankine cohesive coefficient kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_Kpc", Description:="calculate Rankine cohesive coefficient kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_z0", Description:="calculate Rankine coefficient of passive earth pressure, Kp after Rankine (1857)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_Active", Description:="calculate Rankine active earth pressure, using Ka after Rankine (1857) and kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_Passive", Description:="calculate Rankine passive earth pressure, using Kp after Rankine (1857) and kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_hc", Description:="calculate the critical height hc  below which the active (Rankine) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName
        .MacroOptions Macro:="calc_Rankine_zc", Description:="calculate the critical height zc  below which the active (Rankine) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName

        .MacroOptions Macro:="calc_Coulomb_Ka", Description:="calculate Coulomb coefficient of active earth pressure, Ka after Rankine (1857) NB alpha_deg measured from horizontal (=90 for vertical wall)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_Kp", Description:="calculate Coulomb coefficient of passive earth pressure, Kp after Rankine (1857)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_Kac", Description:="calculate Coulomb cohesive coefficient kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_Kpc", Description:="calculate Coulomb cohesive coefficient kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_z0", Description:="calculate Coulomb coefficient of passive earth pressure, Kp after Rankine (1857)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_Active", Description:="calculate Coulomb active earth pressure, using Ka after Coulomb (1776) and kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_Passive", Description:="calculate Coulomb passive earth pressure, using Kp after Rankine (1857) and kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_hc", Description:="calculate the critical height hc  below which the active (Coulomb) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName
        .MacroOptions Macro:="calc_Coulomb_zc", Description:="calculate the critical height zc  below which the active (Coulomb) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName

        .MacroOptions Macro:="calc_Ka", Description:="calculate coefficient of active earth pressure, Ka after Rankine (1857) or Coulomb (1776)", Category:=catName
        .MacroOptions Macro:="calc_Kp", Description:="calculate coefficient of passive earth pressure, Kp after Rankine (1857) or Coulomb (1776)"", Category:=catName"
        .MacroOptions Macro:="calc_Kac", Description:="calculate Rankine (1857) or Coloumb (1776) cohesive coefficient kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Kpc", Description:="calculate Rankine (1857) or Coloumb (1776) cohesive coefficient kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_z0", Description:="calculate Rankine (1857) or Coloumb (1776) z0", Category:=catName
        .MacroOptions Macro:="calc_Active", Description:="calculate Active earth pressure Rankine (1857) or Coloumb (1776) and kac after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_Passive", Description:="calculate Passive earth pressure Rankine (1857) or Coloumb (1776) and kpc after Bell (1915)", Category:=catName
        .MacroOptions Macro:="calc_hc", Description:="calculate the critical height hc  below which the active (Coulomb or Rankine) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName
        .MacroOptions Macro:="calc_zc", Description:="calculate the critical height zc  below which the active (Coulomb or Rankine) pressure is greater than the residual stress due to compaction Broms (1971)", Category:=catName

End With

With ThisWorkbook
        .IsAddin = True
End With

End Function

Public Function calc_Rankine_Ka(phi_deg As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Ka.VB_Description = "calculate Rankine coefficient of active earth pressure, Ka after Rankine (1857)"
Attribute calc_Rankine_Ka.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        calc_Rankine_Ka = .calc_Ka
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_Kp(phi_deg As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Kp.VB_Description = "calculate Rankine coefficient of passive earth pressure, Kp after Rankine (1857)"
Attribute calc_Rankine_Kp.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        calc_Rankine_Kp = .calc_Kp
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_Kpc(phi_deg As Double, c As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Kpc.VB_Description = "calculate Rankine cohesive coefficient kpc after Bell (1915)"
Attribute calc_Rankine_Kpc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .c = c
        calc_Rankine_Kpc = .calc_Kpc
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_Kac(phi_deg As Double, c As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Kac.VB_Description = "calculate Rankine cohesive coefficient kac after Bell (1915)"
Attribute calc_Rankine_Kac.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .c = c
        calc_Rankine_Kac = .calc_Kac
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_z0(phi_deg As Double, c As Double, g As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_z0.VB_Description = "calculate Rankine coefficient of passive earth pressure, Kp after Rankine (1857)"
Attribute calc_Rankine_z0.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .c = c
        .g = g
        calc_Rankine_z0 = .calc_z0
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_Active(phi_deg As Double, c As Double, v As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Active.VB_Description = "calculate Rankine active earth pressure, using Ka after Rankine (1857) and kac after Bell (1915)"
Attribute calc_Rankine_Active.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .c = c
        .calc_Kac
        calc_Rankine_Active = .calc_Active(v)
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_Passive(phi_deg As Double, c As Double, v As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_Passive.VB_Description = "calculate Rankine passive earth pressure, using Kp after Rankine (1857) and kpc after Bell (1915)"
Attribute calc_Rankine_Passive.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .c = c
        .calc_Kac
        calc_Rankine_Passive = .calc_Active(v)
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_zc(phi_deg As Double, p As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_zc.VB_Description = "calculate the critical height zc  below which the active (Rankine) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_Rankine_zc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .calc_Ka
        calc_Rankine_zc = .calc_zc(p)
End With
Set r1 = Nothing
End Function
Public Function calc_Rankine_hc(phi_deg As Double, p As Double, Optional beta_deg As Double = 0) As Double
Attribute calc_Rankine_hc.VB_Description = "calculate the critical height hc  below which the active (Rankine) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_Rankine_hc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim r1 As cRankine
Set r1 = New cRankine
With r1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .calc_Ka
        calc_Rankine_hc = .calc_hc(p)
End With
Set r1 = Nothing
End Function
Public Function calc_Coulomb_Ka(phi_deg As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Ka.VB_Description = "calculate Coulomb coefficient of active earth pressure, Ka after Rankine (1857) NB alpha_deg measured from horizontal (=90 for vertical wall)"
Attribute calc_Coulomb_Ka.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
         calc_Coulomb_Ka = .calc_Ka
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_Kp(phi_deg As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Kp.VB_Description = "calculate Coulomb coefficient of passive earth pressure, Kp after Rankine (1857)"
Attribute calc_Coulomb_Kp.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        calc_Coulomb_Kp = .calc_Kp
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_Kpc(phi_deg As Double, c As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Kpc.VB_Description = "calculate Coulomb cohesive coefficient kpc after Bell (1915)"
Attribute calc_Coulomb_Kpc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .c = c
        calc_Coulomb_Kpc = .calc_Kpc
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_Kac(phi_deg As Double, c As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Kac.VB_Description = "calculate Coulomb cohesive coefficient kac after Bell (1915)"
Attribute calc_Coulomb_Kac.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .c = c
        calc_Coulomb_Kac = .calc_Kac
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_z0(phi_deg As Double, c As Double, g As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_z0.VB_Description = "calculate Coulomb coefficient of passive earth pressure, Kp after Rankine (1857)"
Attribute calc_Coulomb_z0.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .c = c
        .g = g
        calc_Coulomb_z0 = .calc_z0
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_Active(phi_deg As Double, c As Double, v As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Active.VB_Description = "calculate Coulomb active earth pressure, using Ka after Coulomb (1776) and kac after Bell (1915)"
Attribute calc_Coulomb_Active.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .c = c
        .calc
        calc_Coulomb_Active = .calc_Active(v)
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_Passive(phi_deg As Double, c As Double, v As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_Passive.VB_Description = "calculate Coulomb passive earth pressure, using Kp after Rankine (1857) and kpc after Bell (1915)"
Attribute calc_Coulomb_Passive.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .calc_Kp
        calc_Coulomb_Passive = .calc_Passive(v)
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_zc(phi_deg As Double, p As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_zc.VB_Description = "calculate the critical height zc  below which the active (Coulomb) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_Coulomb_zc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .calc_Ka
        calc_Coulomb_zc = .calc_zc(p)
End With
Set c1 = Nothing
End Function
Public Function calc_Coulomb_hc(phi_deg As Double, p As Double, Optional alpha_deg = 90, Optional beta_deg As Double = 0, Optional delta_deg = 0) As Double
Attribute calc_Coulomb_hc.VB_Description = "calculate the critical height hc  below which the active (Coulomb) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_Coulomb_hc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim c1 As cCoulomb
Set c1 = New cCoulomb
With c1
        .phi_deg = phi_deg
        .beta_deg = beta_deg
        .alpha_deg = alpha_deg
        .delta_deg = delta_deg
        .calc_Ka
        calc_Coulomb_hc = .calc_hc(p)
End With
Set c1 = Nothing
End Function
Private Function getLateralAnalysisMethod(var As String) As LateralAnalysisMethod
If Len(var) = 0 Then
    getLateralAnalysisMethod = LateralAnalysisMethod.enumRankine
Else
If InStr(UCase(var), "RANK") > 0 Then getLateralAnalysisMethod = LateralAnalysisMethod.enumRankine
If InStr(UCase(var), "COUL") > 0 Then getLateralAnalysisMethod = LateralAnalysisMethod.enumCoulomb
If IsNumeric(var) Then
If CInt(var) = 0 Then getLateralAnalysisMethod = LateralAnalysisMethod.enumRankine
If CInt(var) = 1 Then getLateralAnalysisMethod = LateralAnalysisMethod.enumCoulomb
End If
End If
End Function
Public Function calc_Ka(phi_deg As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Ka.VB_Description = "calculate coefficient of active earth pressure, Ka after Rankine (1857) or Coulomb (1776)"
Attribute calc_Ka.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Ka = calc_Rankine_Ka(phi_deg, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Ka = calc_Coulomb_Ka(phi_deg, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_Kp(phi_deg As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Kp.VB_Description = "calculate coefficient of passive earth pressure, Kp after Rankine (1857) or Coulomb (1776)"", Category:=catName"
Attribute calc_Kp.VB_ProcData.VB_Invoke_Func = " \n14"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Kp = calc_Rankine_Kp(phi_deg, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Kp = calc_Coulomb_Kp(phi_deg, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_Kpc(phi_deg As Double, c As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Kpc.VB_Description = "calculate Rankine (1857) or Coloumb (1776) cohesive coefficient kpc after Bell (1915)"
Attribute calc_Kpc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Kpc = calc_Rankine_Kpc(phi_deg, c, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Kpc = calc_Coulomb_Kpc(phi_deg, c, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_Kac(phi_deg As Double, c As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Kac.VB_Description = "calculate Rankine (1857) or Coloumb (1776) cohesive coefficient kac after Bell (1915)"
Attribute calc_Kac.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Kac = calc_Rankine_Kac(phi_deg, c, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Kac = calc_Coulomb_Kac(phi_deg, c, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_z0(phi_deg As Double, c As Double, g As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_z0.VB_Description = "calculate Rankine (1857) or Coloumb (1776) z0"
Attribute calc_z0.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_z0 = calc_Rankine_z0(phi_deg, c, g, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_z0 = calc_Coulomb_z0(phi_deg, c, g, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_Active(phi_deg As Double, c As Double, v As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Active.VB_Description = "calculate Active earth pressure Rankine (1857) or Coloumb (1776) and kac after Bell (1915)"
Attribute calc_Active.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Active = calc_Rankine_Active(phi_deg, c, v, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Active = calc_Coulomb_Active(phi_deg, c, v, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_Passive(phi_deg As Double, c As Double, v As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_Passive.VB_Description = "calculate Passive earth pressure Rankine (1857) or Coloumb (1776) and kpc after Bell (1915)"
Attribute calc_Passive.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_Passive = calc_Rankine_Passive(phi_deg, c, v, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_Passive = calc_Coulomb_Passive(phi_deg, c, v, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_hc(phi_deg As Double, p As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_hc.VB_Description = "calculate the critical height hc  below which the active (Coulomb or Rankine) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_hc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_hc = calc_Rankine_hc(phi_deg, p, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_hc = calc_Coulomb_hc(phi_deg, p, alpha_deg, beta_deg, delta_deg)
End Function
Public Function calc_zc(phi_deg As Double, p As Double, Optional alpha_deg As Double = 90, Optional beta_deg As Double = 0, Optional delta_deg As Double = 0, Optional Method As String = "0") As Double
Attribute calc_zc.VB_Description = "calculate the critical height zc  below which the active (Coulomb or Rankine) pressure is greater than the residual stress due to compaction Broms (1971)"
Attribute calc_zc.VB_ProcData.VB_Invoke_Func = " \n20"
Dim M1 As LateralAnalysisMethod
M1 = getLateralAnalysisMethod(Method)
If M1 = LateralAnalysisMethod.enumRankine Then calc_zc = calc_Rankine_zc(phi_deg, p, beta_deg)
If M1 = LateralAnalysisMethod.enumCoulomb Then calc_zc = calc_Coulomb_zc(phi_deg, p, alpha_deg, beta_deg, delta_deg)
End Function
