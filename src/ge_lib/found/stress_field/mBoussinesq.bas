Attribute VB_Name = "mBoussinesq"
Option Explicit
Private Const const_PI = 3.14159
Public Function init_Functions(Optional catName As String = "Geotech Boussinesq")

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="line_sz", Description:="vertical stress sz calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="line_sx", Description:="lateral stress sx calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="line_sxz", Description:="shear stress sxz calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="point_sz", Description:="vertical stress sz calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="point_sr", Description:="radial stress sr calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="point_stheta", Description:="tangential stress stheta calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="point_srz", Description:="shear stress srz calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)", Category:=catName
        .MacroOptions Macro:="strip_sz", Description:="vertical stress sz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2", Category:=catName
        .MacroOptions Macro:="strip_sz2", Description:="vertical stress sz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2, x measured from centre of strip, z depth below strip", Category:=catName
        .MacroOptions Macro:="strip_sx", Description:="lateral stress sx calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2", Category:=catName
        .MacroOptions Macro:="strip_sxz", Description:="shear stress sxz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2", Category:=catName
        .MacroOptions Macro:="linear_Strip_sz", Description:="vertical stress sz calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2", Category:=catName
        .MacroOptions Macro:="linear_Strip_sx", Description:="lateral stress sx calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2", Category:=catName
        .MacroOptions Macro:="linear_Strip_sxz", Description:="shear stress sxz calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2", Category:=catName
        .MacroOptions Macro:="circle_sz", Description:="vertical stress sz calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2", Category:=catName
        .MacroOptions Macro:="circle_sr", Description:="radial stress sr calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2", Category:=catName
        .MacroOptions Macro:="circle_stheta", Description:="tangential stress stheta calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2", Category:=catName
        .MacroOptions Macro:="rectangle_sz", Description:="vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2", Category:=catName
        .MacroOptions Macro:="rectangle_sz2", Description:="vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2", Category:=catName
        .MacroOptions Macro:="rectangle_sz3", Description:="vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2", Category:=catName
        .MacroOptions Macro:="calc_Ir", Description:="infuence factor for calculating the vertical stress sz at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2 m=B/z and n=L/z where L>B", Category:=catName
End With
With ThisWorkbook
        .IsAddin = True
End With


End Function

Public Function line_sz(q As Double, x As Double, z As Double)
Attribute line_sz.VB_Description = "vertical stress sz calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)"
Attribute line_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
line_sz = .line_sz(q, x, z)
End With
Set B1 = Nothing
End Function
Public Function line_sx(q As Double, x As Double, z As Double) As Double
Attribute line_sx.VB_Description = "lateral stress sx calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)"
Attribute line_sx.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
line_sx = .line_sx(q, x, z)
End With
Set B1 = Nothing
End Function
Public Function line_sxz(q As Double, x As Double, z As Double) As Double
Attribute line_sxz.VB_Description = "shear stress sxz calculated at depth z below and at x distance normal to the line load as the surface with a uniform load of Q/m Boussineque (1885)"
Attribute line_sxz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
line_sxz = .line_sxz(q, x, z)
End With
Set B1 = Nothing
End Function
Public Function point_sz(q As Double, r As Double, z As Double) As Double
Attribute point_sz.VB_Description = "vertical stress sz calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)"
Attribute point_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
point_sz = .point_sz(q, r, z)
End With
Set B1 = Nothing
End Function
Public Function point_sr(q As Double, r As Double, z As Double, Poisson As Double) As Double
Attribute point_sr.VB_Description = "radial stress sr calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)"
Attribute point_sr.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
point_sr = .point_sr(q, r, z, Poisson)
End With
Set B1 = Nothing
End Function
Public Function point_stheta(q As Double, r As Double, z As Double, Poisson As Double) As Double
Attribute point_stheta.VB_Description = "tangential stress stheta calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)"
Attribute point_stheta.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
point_stheta = .point_stheta(q, r, z, Poisson)
End With
Set B1 = Nothing
End Function
Public Function point_srz(q As Double, r As Double, z As Double) As Double
Attribute point_srz.VB_Description = "shear stress srz calculated at depth z below and at a radial distance r from a surface point load of Q Boussineque (1885)"
Attribute point_srz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
point_srz = .point_srz(q, r, z)
End With
Set B1 = Nothing
End Function
Public Function strip_sz(q As Double, alpha_rad As Double, beta_rad As Double) As Double
Attribute strip_sz.VB_Description = "vertical stress sz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2"
Attribute strip_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
strip_sz = .strip_sz(q, alpha_rad, beta_rad)
End With
Set B1 = Nothing
End Function
Public Function strip_sz2(q As Double, B As Double, x As Double, z As Double) As Double
Attribute strip_sz2.VB_Description = "vertical stress sz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2, x measured from centre of strip, z depth below strip"
Attribute strip_sz2.VB_ProcData.VB_Invoke_Func = " \n20"
strip_sz2 = strip_sz(q, get_alpha_rad(B, x, z), get_beta_rad(B, x, z))
End Function

Private Function get_alpha_rad(B As Double, x As Double, z As Double) As Double
If z = 0 Then
    If x <= B Then
        get_alpha_rad = const_PI
    Else
    get_alpha_rad = 0
    End If
Else
get_alpha_rad = Atn((x - B) / z)
End If
End Function

Private Function get_beta_rad(B As Double, x As Double, z As Double) As Double
If z = 0 Then
    If x <= B Then
        get_beta_rad = const_PI
    Else
        get_beta_rad = 0
    End If
Else
get_beta_rad = Atn((x + B) / z) - get_alpha_rad(B, x, z)
End If

End Function

Public Function strip_sx(q As Double, alpha_rad As Double, beta_rad As Double) As Double
Attribute strip_sx.VB_Description = "lateral stress sx calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2"
Attribute strip_sx.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
strip_sx = .strip_sx(q, alpha_rad, beta_rad)
End With
Set B1 = Nothing
End Function
Public Function strip_sxz(q As Double, alpha_rad As Double, beta_rad As Double) As Double
Attribute strip_sxz.VB_Description = "shear stress sxz calculated at depth z below a uniformly loaded strip 2b wide loaded Q/m2"
Attribute strip_sxz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
strip_sxz = .strip_sxz(q, alpha_rad, beta_rad)
End With
Set B1 = Nothing
End Function
Public Function linear_strip_sz(q As Double, alpha_rad As Double, beta_rad As Double, x As Double, c As Double) As Double
Attribute linear_strip_sz.VB_Description = "vertical stress sz calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2"
Attribute linear_strip_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
linear_strip_sz = .linear_strip_sz(q, alpha_rad, beta_rad, x, c)
End With
Set B1 = Nothing
End Function

Public Function linear_strip_sx(q As Double, alpha_rad As Double, beta_rad As Double, x As Double, z As Double, c As Double) As Double
Attribute linear_strip_sx.VB_Description = "lateral stress sx calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2"
Attribute linear_strip_sx.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
linear_strip_sx = .linear_strip_sx(q, alpha_rad, beta_rad, x, z, c)
End With
Set B1 = Nothing
End Function

Public Function linear_strip_sxz(q As Double, alpha_rad As Double, beta_rad As Double, z As Double, c As Double) As Double
Attribute linear_strip_sxz.VB_Description = "shear stress sxz calculated at depth z below a linearly increasing loaded strip 2b wide loaded from 0 to Q/m2"
Attribute linear_strip_sxz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
linear_strip_sxz = .linear_strip_sxz(q, alpha_rad, beta_rad, z, c)
End With
Set B1 = Nothing
End Function
Public Function circle_sz(q As Double, z As Double, r As Double) As Double
Attribute circle_sz.VB_Description = "vertical stress sz calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2"
Attribute circle_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
circle_sz = .circle_sz(q, z, r)
End With
Set B1 = Nothing
End Function
Public Function circle_sr(q As Double, z As Double, r As Double, Poisson As Double) As Double
Attribute circle_sr.VB_Description = "radial stress sr calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2"
Attribute circle_sr.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
circle_sr = .circle_sr(q, z, r, Poisson)
End With
Set B1 = Nothing
End Function
Public Function circle_stheta(q As Double, z As Double, r As Double, Poisson As Double) As Double
Attribute circle_stheta.VB_Description = "tangential stress stheta calculated at depth z below the center of a uniformly loaded circle of radius a with a pressure of Q/m2"
Attribute circle_stheta.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
circle_stheta = .circle_stheta(q, z, r, Poisson)
End With
Set B1 = Nothing
End Function
Public Function rectangle_sz(q As Double, z As Double, B As Double, L As Double) As Double
Attribute rectangle_sz.VB_Description = "vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2"
Attribute rectangle_sz.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
rectangle_sz = .rectangle_sz(q, z, B, L)
End With
Set B1 = Nothing
End Function
Public Function calc_Ir(M As Double, N As Double) As Double
Attribute calc_Ir.VB_Description = "infuence factor for calculating the vertical stress sz at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2 m=B/z and n=L/z where L>B"
Attribute calc_Ir.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
calc_Ir = .calc_Ir(M, N)
End With
Set B1 = Nothing
End Function

Public Function rectangle_sz2(q As Double, z As Double, a As Double, B As Double) As Double
Attribute rectangle_sz2.VB_Description = "vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2"
Attribute rectangle_sz2.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
rectangle_sz2 = .rectangle_sz2(q, z, a, B)
End With
Set B1 = Nothing
End Function
Public Function rectangle_sz3(q As Double, z As Double, a As Double, B As Double) As Double
Attribute rectangle_sz3.VB_Description = "vertical stress sz calculated at depth z below the corner of a rectangular area of length L and breadth B with a uniformly load of Q/m2"
Attribute rectangle_sz3.VB_ProcData.VB_Invoke_Func = " \n20"
Dim B1 As cBoussinesq
Set B1 = New cBoussinesq
With B1
rectangle_sz3 = .rectangle_sz3(q, z, a, B)
End With
Set B1 = Nothing
End Function
