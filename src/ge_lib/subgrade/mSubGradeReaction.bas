Attribute VB_Name = "mSubGradeReaction"
Option Explicit

Public Function init_Functions(Optional catName As String = "Geotech General")

If Len(catName) = 0 Then catName = "Geotech General"

With ThisWorkbook
        .IsAddin = False
End With

With Application
        .MacroOptions Macro:="calc_Ks_TERZAGHI", Description:="calculate subgrade reaction; B=breadth, Esoil=Youngs modulus of soil, possion ratio", Category:=catName
        .MacroOptions Macro:="calc_Ks_VESIC", Description:="calculate subgrade reaction; B=breadth, Esoil=Youngs modulus of soil, possion ratio", Category:=catName
        .MacroOptions Macro:="calc_Ks_YOSHINAKA", Description:="calculate subgrade reaction; B=breadth, Esoil=Youngs modulus of soil, possion ratio", Category:=catName
        .MacroOptions Macro:="calc_Ks_BOWLES", Description:="calculate subgrade reaction; B=breadth, Esoil=Youngs modulus of soil, possion ratio", Category:=catName
        .MacroOptions Macro:="calc_If", Description:="calculate DepthFactor If from D/B ratio for L/B ratio and POissons ratio, Bowles Figure 5-7 Page 303", Category:=catName
        .MacroOptions Macro:="calc_Settlement_BOWLES", Description:="calculate settlement Bowles Eq 5-16 Page 303", Category:=catName
        .MacroOptions Macro:="calc_Is", Description:="calculate ShapeFactor Is from Poisson Ratio, Breadth B, Breadth Is_B, Length Is_L, Soil thickness H,  Bowles Eq 5-16(c) page 306", Category:=catName
        .MacroOptions Macro:="calc_I1", Description:="calculate ShapeFactor I1 from Breadth B, Breadth Is_B, Length Is_L, Soil thickness H,  Bowles Eq 5-16(a) page 303", Category:=catName
        .MacroOptions Macro:="calc_I2", Description:="calculate ShapeFactor I2 from Breadth B, Breadth Is_B, Length Is_L, Soil thickness H,  Bowles Eq 5-16(b) page 303", Category:=catName
      
     End With

With ThisWorkbook
        .IsAddin = True
End With


End Function

Public Function calc_Ks_VESIC(Esoil As Double, Poisson As Double, B As Double, Efooting As Double, Ifooting) As Double

Dim m_sg As cSubgrade_VESIC

Set m_sg = New cSubgrade_VESIC

With m_sg
       .B = B
       .Esoil = Esoil
       .Poisson = Poisson
       .Efooting = Efooting
       .Ifooting = Ifooting
calc_Ks_VESIC = .calcKs()

End With

End Function
Public Function calc_Ks_TERZAGHI(Esoil As Double, Poisson As Double, B As Double, Ip As Double) As Double

Dim m_sg As cSubgrade_TERZAGHI

Set m_sg = New cSubgrade_TERZAGHI

With m_sg
       .B = B
       .Esoil = Esoil
       .Poisson = Poisson
       .Ip = Ip
calc_Ks_TERZAGHI = .calcKs()

End With

End Function
Public Function calc_Ks_YOSHINAKA(E30 As Double, Poisson As Double, B As Double, Ip As Double) As Double

Dim m_sg As cSubgrade_YOSHINAKA

Set m_sg = New cSubgrade_YOSHINAKA

With m_sg
       .B = B
       .E30 = E30
       .Poisson = Poisson
       .Ip = Ip
calc_Ks_YOSHINAKA = .calc_kh()

End With

End Function

Public Function calc_Ks_BOWLES(Esoil As Double, Poisson As Double, B As Double, L As Double, Is_B As Double, Is_L As Double, D As Double, H As Double, Mfactor As Double) As Double

Dim m_sg As cSettlement_BOWLES

Set m_sg = New cSettlement_BOWLES

With m_sg
       .B = B
       .Is_B = Is_B
       .Is_L = Is_L
       .H = H
       .D = D
       .L = L
       .Mfactor = Mfactor
       .Esoil = Esoil
       .Poisson = Poisson
calc_Ks_BOWLES = .calcKs()

End With

End Function
Public Function calc_Settlement_BOWLES(Esoil As Double, Poisson As Double, B As Double, L As Double, Is_B As Double, Is_L As Double, D As Double, H As Double, Mfactor As Double, qO As Double) As Double

Dim m_sg As cSettlement_BOWLES

Set m_sg = New cSettlement_BOWLES

With m_sg
       .B = B
       .Is_B = Is_B
       .Is_L = Is_L
       .H = H
       .D = D
       .L = L
       .Mfactor = Mfactor
       .Esoil = Esoil
       .Poisson = Poisson
       .qO = qO
       
calc_Settlement_BOWLES = .calcSettlement()

End With

End Function
Public Function calc_I2(B As Double, Is_B As Double, Is_L As Double, H As Double) As Double
Dim ifactors As cInfluenceFactors
     
    Set ifactors = New cInfluenceFactors
    
    With ifactors
                .letM = Is_L / Is_B
                .letN = H / B
         calc_I2 = .calc_I2
    End With

End Function
Public Function calc_I1(B As Double, Is_B As Double, Is_L As Double, H As Double) As Double
Dim ifactors As cInfluenceFactors
     
    Set ifactors = New cInfluenceFactors
    
    With ifactors
                .letM = Is_L / Is_B
                .letN = H / B
         calc_I1 = .calc_I1
    End With

End Function
Public Function calc_Is(Poisson As Double, B As Double, Is_B As Double, Is_L As Double, H As Double) As Double
Dim m_sg As cSettlement_BOWLES

Set m_sg = New cSettlement_BOWLES

With m_sg
       .B = B
       .Is_B = Is_B
       .Is_L = Is_L
       .H = H
       .Poisson = Poisson
       
       calc_Is = .factorIs()

End With

End Function

Public Function calc_If(LoverB As Double, Poisson As Double, DoverB As Double) As Double

    Dim df As cDepthFactor
    Set df = New cDepthFactor
    
    calc_If = df.get_DepthFactor(LoverB, 0.3, DoverB)
    
End Function
