Attribute VB_Name = "mGroundResponseCurve"
Option Explicit
Private m_GRC As Variant
Private m_SCL As cSCL_Properties

Private Enum enumGroundResponseMethod
        None = 0
        BrownBrayLadeniHoek1993 = 1
        DuncanFama1993 = 2
        Salencon1969 = 3
        EberhardtGradClass2014 = 4
End Enum

Private Function get_enumGroundResponseMethod(Method As String) As enumGroundResponseMethod
If Len(Method) = 0 Then get_enumGroundResponseMethod = enumGroundResponseMethod.None
If InStr("hoek", LCase(Method)) Then get_enumGroundResponseMethod = enumGroundResponseMethod.BrownBrayLadeniHoek1993
If InStr("duncan", LCase(Method)) Then get_enumGroundResponseMethod = enumGroundResponseMethod.DuncanFama1993
If InStr("salencon", LCase(Method)) Then get_enumGroundResponseMethod = enumGroundResponseMethod.Salencon1969
If InStr("eberhardt", LCase(Method)) Then get_enumGroundResponseMethod = enumGroundResponseMethod.EberhardtGradClass2014
End Function

Private Function set_GRC(Optional Method As String = "hoek")
Dim enumCalcMethod
enumCalcMethod = get_enumGroundResponseMethod(Method)

Select Case enumCalcMethod
                Case Is = enumGroundResponseMethod.None, enumGroundResponseMethod.BrownBrayLadeniHoek1993
                Set m_GRC = New cGRC_BrownBrayLadanyiHoek1983
                
                Case Is = enumGroundResponseMethod.DuncanFama1993
                Set m_GRC = New cGRC_DuncanFama1993
                
                Case Is = enumGroundResponseMethod.EberhardtGradClass2014
                Set m_GRC = New cGRC_Eberhardt
                
                Case Is = enumGroundResponseMethod.Salencon1969
                Set m_GRC = New cGRC_Salencon1969
End Select

End Function
Public Function init_Functions(Optional catName As String = "Geotech Tunnels")

If Len(catName) = 0 Then catName = "Geotech Tunnels"

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="GRC_Pcr", Description:="calculate critical internal pressure, below which the plastic zone around the hole will collapse in an infinite Mohr Coulomb medium", Category:=catName
        .MacroOptions Macro:="GRC_Ure", Description:="calculate elastic displacemnt at limit of elastic ground movements on GRP curve ", Category:=catName
        .MacroOptions Macro:="GRC_Urp", Description:="calculate plastic displacemnt for given internal support pressure Pi", Category:=catName
        .MacroOptions Macro:="GRC_Ur", Description:="calculate total (Ure+Urp) displacemnt for given internal support pressure Pi", Category:=catName
        .MacroOptions Macro:="GRC_Ulin", Description:="calculate the lining displacement for given Pfict, Po", Category:=catName
        .MacroOptions Macro:="GRC_Plin", Description:="calculate the lining load required for given Pfict, Po", Category:=catName
  
     End With

With ThisWorkbook
        .IsAddin = True
End With


End Function

Public Function GRC_Pcr(Po As Double, cohesion As Double, friction_deg As Double, Optional Method As String = "Hoek") As Double
Attribute GRC_Pcr.VB_Description = "calculate critical internal pressure, below which the plastic zone around the hole will collapse in an infinite Mohr Coulomb medium"
Attribute GRC_Pcr.VB_ProcData.VB_Invoke_Func = " \n18"

set_GRC (Method)

With m_GRC
        .Po = Po
        .friction_deg = friction_deg
        .cohesion = cohesion
        .calc_Pcr
GRC_Pcr = .Pcr
End With

End Function

Public Function GRC_Ure(Radius As Double, _
                        Po As Double, Pint As Double, E As Double, Poisson As Double, _
                        Optional Method = "Hoek") As Double
Attribute GRC_Ure.VB_Description = "calculate elastic displacemnt at limit of elastic ground movements on GRP curve "
Attribute GRC_Ure.VB_ProcData.VB_Invoke_Func = " \n18"
set_GRC (Method)

With m_GRC
        .Radius_r = Radius
        .Po = Po
        .PI = Pint
        .Emod = E
        .Poisson = Poisson
        .calc_Ure
GRC_Ure = .Ure
End With

End Function
Public Function GRC_Urp(Radius As Double, _
                        Po As Double, Pint As Double, E As Double, Poisson As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        Optional Method = "Hoek") As Double
Attribute GRC_Urp.VB_Description = "calculate plastic displacemnt for given internal support pressure Pi"
Attribute GRC_Urp.VB_ProcData.VB_Invoke_Func = " \n18"
                        
set_GRC (Method)
With m_GRC
        .Radius_r = Radius
        .Po = Po
        .PI = Pint
        .Emod = E
        .Poisson = Poisson
        .cohesion = cohesion
        .friction_deg = friction_deg
        .dilation_deg = dilation_deg
        .cohesion_res = cohesion_res
        .friction_res_deg = friction_res_deg
        .calc_Urp
GRC_Urp = .Urp
End With

End Function

Public Function GRC_Ur(Radius As Double, _
                        Po As Double, Pint As Double, _
                        E As Double, Poisson As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        Optional Method As String = "Hoek") As Double
Attribute GRC_Ur.VB_Description = "calculate total (Ure+Urp) displacemnt for given internal support pressure Pi"
Attribute GRC_Ur.VB_ProcData.VB_Invoke_Func = " \n18"
                        
            get_GRC Radius, _
            Po, Pint, _
            E, Poisson, _
            cohesion, friction_deg, dilation_deg, _
            cohesion_res, friction_res_deg, _
            Method

With m_GRC
            .calc_Ur
            GRC_Ur = .Ur
End With
                        


End Function


Private Function get_GRC(Radius As Double, _
                        Po As Double, Pint As Double, _
                        E As Double, Poisson As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        Optional Method As String = "Hoek") As Variant
                        
                      
set_GRC (Method)

With m_GRC
        .Radius_r = Radius
        .Po = Po
        .PI = Pint
        .Emod = E
        .Poisson = Poisson
        .dilation_deg = dilation_deg
        .cohesion = cohesion
        .friction_deg = friction_deg
        .cohesion_res = cohesion_res
        .friction_res_deg = friction_res_deg
End With

Set get_GRC = m_GRC

End Function
Public Function GRC_Ulin(Radius As Double, _
                         E_ground As Double, Poiss_ground As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        E_conc As Double, Poiss_conc As Double, thk_conc As Double, _
                        conc_time_hr As Double, ConcGainMethod As String, _
                        Ulin_orig As Double, Plin_orig As Double, _
                        Po As Double, Pfict As Double, _
                        Optional Method As String, _
                        Optional allowError As Double = 0.01 _
                        ) As Double
Attribute GRC_Ulin.VB_Description = "calculate the lining displacement for given Pfict, Po"
Attribute GRC_Ulin.VB_ProcData.VB_Invoke_Func = " \n18"
Set m_SCL = get_SCLtoGRC(Radius, _
                    E_ground, Poiss_ground, _
                    cohesion, friction_deg, dilation_deg, _
                    cohesion_res, friction_res_deg, _
                    E_conc, Poiss_conc, thk_conc, _
                    conc_time_hr, ConcGainMethod, _
                    Ulin_orig, Plin_orig, _
                    Po, Pfict, _
                    Method, _
                    allowError _
                    )
GRC_Ulin = m_SCL.Ur + Ulin_orig
End Function

Public Function GRC_Plin(Radius As Double, _
                         E_ground As Double, Poiss_ground As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        E_conc As Double, Poiss_conc As Double, thk_conc As Double, _
                        conc_time_hr As Double, ConcGainMethod As String, _
                        Ulin_orig As Double, Plin_orig As Double, _
                        Po As Double, Pfict As Double, _
                        Optional Method As String = "Hoek", _
                        Optional allowError As Double = 0.01 _
                        ) As Double
Attribute GRC_Plin.VB_Description = "calculate the lining load required for given Pfict, Po"
Attribute GRC_Plin.VB_ProcData.VB_Invoke_Func = " \n18"

 Set m_SCL = get_SCLtoGRC(Radius, _
                    E_ground, Poiss_ground, _
                    cohesion, friction_deg, dilation_deg, _
                    cohesion_res, friction_res_deg, _
                    E_conc, Poiss_conc, thk_conc, _
                    conc_time_hr, ConcGainMethod, _
                    Ulin_orig, Plin_orig, _
                    Po, Pfict, _
                    Method, _
                    allowError _
                    )
GRC_Plin = m_SCL.Po + Plin_orig
End Function

Private Function get_SCLtoGRC(Radius As Double, _
                         E_ground As Double, Poiss_ground As Double, _
                        cohesion As Double, friction_deg As Double, dilation_deg As Double, _
                        cohesion_res As Double, friction_res_deg As Double, _
                        E_conc As Double, Poiss_conc As Double, thk_conc As Double, _
                        conc_time_hr As Double, ConcGainMethod As String, _
                        Ulin_orig As Double, Plin_orig As Double, _
                        Po As Double, Pfict As Double, _
                        Optional Method As String = "Hoek", _
                        Optional allowError As Double = 0.01 _
                        ) As cSCL_Properties


   Set m_GRC = get_GRC(Radius, _
            Po, 0, _
            E_ground, Poiss_ground, _
            cohesion, friction_deg, dilation_deg, _
            cohesion_res, friction_res_deg, _
            Method)

   Set m_SCL = get_SCL(Radius, _
            E_conc, _
            conc_time_hr, ConcGainMethod, _
            Poiss_conc, thk_conc, _
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            
            


Dim Pstart As Double
Dim Pinc As Double
Dim Plast As Double

Pstart = Po / 100
Pinc = Po / 100

Do Until Pinc < allowError

Plast = step_Plin(Pstart, Pinc, _
                  Ulin_orig, Plin_orig, Po, Pfict _
                  )

Pstart = Plast - Pinc
Pinc = Pinc / 2


Loop

Set get_SCLtoGRC = m_SCL

End Function

Private Function step_Plin(Pstart As Double, Pinc As Double, _
                                Ulin_orig As Double, Plin_orig As Double, _
                                Po As Double, Pfict As Double _
                                ) As Double

Dim Plin As Double
Dim Ulin_tot As Double
Dim UGround As Double
Dim Plin_tot As Double

Plin = Pstart

Do

m_SCL.Po = Plin
m_SCL.calc_Ur

Ulin_tot = Ulin_orig + m_SCL.Ur
Plin_tot = Plin_orig + Plin

m_GRC.PI = Plin_tot + Pfict
m_GRC.calc_Ur
UGround = m_GRC.Ur

Plin = Plin + Pinc
Loop Until Ulin_tot > UGround

step_Plin = Plin - Pinc

End Function

