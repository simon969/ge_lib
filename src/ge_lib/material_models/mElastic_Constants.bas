Attribute VB_Name = "mElastic_Constants"

 
Public Function init_Functions(catName As String)

If Len(catName) = 0 Then catName = "Geotech Bearing Capacity"

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="calc_KG", Description:="calculate elastic constant using Bulk Modulus, K and Shear modulus G", Category:=catName
        .MacroOptions Macro:="calc_KLames", Description:="calculate elastic constant using Bulk Modulus, K and Lames first parameters, lamda", Category:=catName
        .MacroOptions Macro:="calc_EG", Description:="calculate elastic constant using Youngs Modulus, E and Shear modulus G", Category:=catName
        .MacroOptions Macro:="calc_Epoisson", Description:="calculate elastic constant using Youngs Modulus, E and Poissons ratio p", Category:=catName
   
End With

With ThisWorkbook
        .IsAddin = True
End With


End Function


Public Function calc_KLames(k As Double, Lames As Double, ret As String) As Double
Attribute calc_KLames.VB_Description = "calculate elastic constant using Bulk Modulus, K and Lames first parameters, lamda"
Attribute calc_KLames.VB_ProcData.VB_Invoke_Func = " \n23"
Dim EC1 As cElastic_Constants
Set EC1 = New cElastic_Constants
With EC1
        .k = k
        .lamda = Lames
calc_KLames = .calc_KLames(ret)
End With
End Function
Public Function calc_EG(E As Double, g As Double, ret As String) As Double
Attribute calc_EG.VB_Description = "calculate elastic constant using Youngs Modulus, E and Shear modulus G"
Attribute calc_EG.VB_ProcData.VB_Invoke_Func = " \n23"
Dim EC1 As cElastic_Constants
Set EC1 = New cElastic_Constants
With EC1
        .E = E
        .g = g
calc_EG = .calc_EG(ret)
End With
End Function

Public Function calc_KG(k As Double, g As Double, ret As String) As Double
Attribute calc_KG.VB_Description = "calculate elastic constant using Bulk Modulus, K and Shear modulus G"
Attribute calc_KG.VB_ProcData.VB_Invoke_Func = " \n23"
Dim EC1 As cElastic_Constants
Set EC1 = New cElastic_Constants
With EC1
        .k = k
        .g = g
calc_KG = .calc_KG(ret)
End With
End Function


Public Function calc_EPoisson(E As Double, p As Double, ret As String) As Double
Attribute calc_EPoisson.VB_Description = "calculate elastic constant using Youngs Modulus, E and Poissons ratio p"
Attribute calc_EPoisson.VB_ProcData.VB_Invoke_Func = " \n23"
Dim EC1 As cElastic_Constants
Set EC1 = New cElastic_Constants
With EC1
        .E = E
        .Poisson = p
calc_EPoisson = EC1.calc_EPoisson(ret)
End With

End Function

