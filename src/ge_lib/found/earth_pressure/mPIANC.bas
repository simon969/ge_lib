Attribute VB_Name = "mPIANC"
Private Sub Main()
Dim phi As Double
Dim w1 As Double
Dim delta As Double

phi = radians(40)
delta = radians(20)
w1 = radians(20.6)

Debug.Print PIANC_calc_ka(phi, delta)
Debug.Print PIANC_calc_kae(phi, delta, w1)

End Sub

Private Function radians(deg As Double) As Double
radians = 3.14159 * deg / 180
End Function
Public Function init_Functions(Optional catName As String = "Geotech PIANC")

If Len(catName) = 0 Then catName = "Geotech PIANC"

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="PIANC_calc_ka", Description:="Calculates lateral active pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall", Category:=catName
        .MacroOptions Macro:="PIANC_calc_kae", Description:="Calculates the quasi static effective active pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall; w1=back slope angle due to ground movement", Category:=catName
        .MacroOptions Macro:="PIANC_calc_kpe", Description:="Calculates the quasi static effective passived pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall; w1=back slope angle due to ground movement", Category:=catName
End With
With ThisWorkbook
        .IsAddin = True
End With


End Function



Public Function PIANC_calc_ka(phi_deg As Double, delta_deg As Double) As Double
Attribute PIANC_calc_ka.VB_Description = "Calculates lateral active pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall"
Attribute PIANC_calc_ka.VB_ProcData.VB_Invoke_Func = " \n20"
Dim ceq As cCoulomb_PIANC
Set ceq = New cCoulomb_PIANC
With ceq
        .delta_rad = radians(delta_deg)
        .phi_rad = radians(phi_deg)
        PIANC_calc_ka = .calc_Ka
End With
Set ceq = Nothing
End Function

Public Function PIANC_calc_kae(phi_deg As Double, delta_deg As Double, w1_deg As Double) As Double
Attribute PIANC_calc_kae.VB_Description = "Calculates the quasi static effective active pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall; w1=back slope angle due to ground movement"
Attribute PIANC_calc_kae.VB_ProcData.VB_Invoke_Func = " \n20"
Dim ceq As cCoulomb_PIANC
Set ceq = New cCoulomb_PIANC
With ceq
        .delta_rad = radians(delta_deg)
        .phi_rad = radians(phi_deg)
        .w1_rad = radians(w1_deg)
        PIANC_calc_kae = .calc_kae
End With
Set ceq = Nothing
End Function
Public Function PIANC_calc_kpe(phi_deg As Double, delta_deg As Double, w1_deg As Double) As Double
Attribute PIANC_calc_kpe.VB_Description = "Calculates the quasi static effective passived pressure using Coulomb wedge principles, where phi_rad=friction angle of soil; delta_rad=friction on back of wall; w1=back slope angle due to ground movement"
Attribute PIANC_calc_kpe.VB_ProcData.VB_Invoke_Func = " \n20"
Dim ceq As cCoulomb_PIANC
Set ceq = New cCoulomb_PIANC
With ceq
        .delta_rad = radians(delta_deg)
        .phi_rad = radians(phi_deg)
        .w1_rad = radians(w1_deg)
        PIANC_calc_kpe = .calc_kpe
End With
Set ceq = Nothing
End Function
