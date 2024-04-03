VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cCircularHoleMC_Salencon1969"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

' ==========================================================================================
' Calculation class for determinination of stresses and displacements for the case of a
' cylindrical hole in an infinite elasto-plastic medium subject to insitu stresse.
' The medium is considered to be linearly elastic, perfectly plastic, witha failure surface
' defined by the Mohr-Coulomb criterion with both the assocaited (dilatancy=friction angle)
' and non-associated (dilatancy=0) flow rules.
'
' FLAC Verification Problems:  Problem 3 Cylindrical hole in an Infinite Mohr-Coulomb Medium
' This problem test the Mohr-Coulomb plasticity model, the plan-strain condition and the
' axisymetric geometry in 2d FLAC
'
' The yield zone radius, Ro is geiven analysitcally by the theoretical model based on the
' solution of Salencon (1969)
' The displacements Ure in the ealstic and Urp in the palstic regions are given by the
' solutions Salencon (1969)
' ==========================================================================================
' Coded  | Simon Thomson
' ==========================================================================================
' Company | AECOM
' ==========================================================================================
' Date    | Jan 2016
' ==========================================================================================
' Version | 01.00.00
' ==========================================================================================

Option Explicit
' ==========================================================================================
' Input parameters
' ==========================================================================================
'radius of hole and radius to point under considerartion
Private m_a As Double
Private m_R As Double

'Internal and external radial pressures
Private m_Pi As Double
Private m_Po As Double
Private m_Pcr As Double

'Mohr-Coloumb failure criterion
Private m_phi_rad As Double
Private m_dilation_rad As Double
Private m_c As Double

'Elastic stiffness properties
Private m_poisson As Double
Private m_G As Double

' ==========================================================================================
' Calculated intermediate parameters
' ==========================================================================================
Private m_q As Double
Private m_Kp As Double
Private m_Kps As Double
Private m_Si As Double


' Results in the plastic region

' Radial stress in the elastic zone
Private m_stressRp
' Tangential stress in the elastic zone
Private m_stressTp
' Displacement in the plastic regions
Private m_dispRp

' Results in the elastic region
' Radial stress in the elastic zone
Private m_stressRe
' Tangential stress in the elastic zone
Private m_stressTe
' Displacement in the elastic regions
Private m_dispRe

' The yield zone radius, radius to elastic/plastic Interface
Private m_Ro As Double
' Radial stress at the elastic/plastic interface
Private m_stressRo
' Radial displacement at the elastic/plastic interface
Private m_dispRo


' ==========================================================================================
' Calculated output parameters
' ==========================================================================================
' State at radius under consideration, "Elastic", "Interface" or "Plastic"
Private m_State As String
' Radial stress
Private m_stressR
' Tangential stress
Private m_stressT
' Radial displacement
Private m_dispR

Private Const const_PI = 3.14159
Private Const const_PI4 = 0.785398163


'Input parameters
Public Property Let dilation_rad(var As Double)
m_dilation_rad = var
End Property
Public Property Let dilation_deg(var As Double)
m_dilation_rad = var * const_PI / 180
End Property
Public Property Let friction_rad(var As Double)
m_phi_rad = var
End Property
Public Property Get friction_rad() As Double
friction_rad = m_phi_rad
End Property
Public Property Let friction_deg(var As Double)
m_phi_rad = var * const_PI / 180
End Property
Public Property Let cohesion(var As Double)
m_c = var
End Property
Public Property Get cohesion() As Double
cohesion = m_c
End Property
Public Property Let Radius_a(var As Double)
m_a = var
End Property
Public Property Let Radius_r(var As Double)
m_R = var
End Property
Public Property Let Po(var As Double)
m_Po = var
End Property
Public Property Get Po() As Double
Po = m_Po
End Property
Public Property Let PI(var As Double)
m_Pi = var
End Property
Public Property Get PI() As Double
PI = m_Pi
End Property
Public Property Let Gmod(var As Double)
m_G = var
End Property
Public Property Let Poisson(var As Double)
m_poisson = var
End Property
Public Property Get Poisson() As Double
Poisson = m_poisson
End Property

Public Property Get State_AsString() As String
Dim ret As String
Select Case m_State
            Case Is >= 1
            ret = "Elastic"
            Case Is = 0
            ret = "Interface"
            Case Is <= 0
            ret = "Plastic"
End Select
State_AsString = ret

End Property
Public Property Get State() As Integer
State = m_State
End Property
Public Property Get Ro() As Double
Ro = m_Ro
End Property
Public Property Get StressR() As Double
StressR = m_stressR
End Property
Public Property Get StressT() As Double
StressT = m_stressT
End Property
Public Property Get dispR() As Double
dispR = m_dispR
End Property

Private Function calc_Kp()

If 1 - Sin(m_phi_rad) = 0 Then
    m_Kp = 0
Else
    m_Kp = (1 + Sin(m_phi_rad)) / (1 - Sin(m_phi_rad))
End If

End Function
Private Function calc_Kps()
If 1 - Sin(m_dilation_rad) = 0 Then
    m_Kps = 0
Else
    m_Kps = (1 + Sin(m_dilation_rad)) / (1 - Sin(m_dilation_rad))
End If

End Function
Private Function calc_q()
m_q = m_c * Tan(const_PI4 + m_phi_rad / 2)
End Function


Private Function calc_ElasticRegion()

m_stressRe = -m_Po + (m_Po - m_stressRo) * (m_Ro / m_R) ^ 2

m_stressTe = -m_Po - (m_Po - m_stressRo) * (m_Ro / m_R) ^ 2

m_dispRe = -(m_Po - (2 * m_Po - m_q) / (m_Kp + 1)) * m_Ro / (2 * m_G) * m_Ro / m_R

End Function

Private Function calc_PlasticRegion()

calc_Kps

' m_q/(m_kp-1)
Dim p1 As Double
p1 = m_q / (m_Kp - 1)

' 1/(m_kp-1)
Dim p2 As Double
If m_Kp <= 1 Then
    p2 = 0
Else
    p2 = (m_Kp - 1)
End If

' m_Kp+1
Dim p3 As Double
p3 = m_Kp + 1

Dim p4 As Double
p4 = (1 - m_poisson) * m_Kp ^ 2 - 1 / (m_Kp + m_Kps)

Dim p5 As Double
p5 = (m_Pi + p1) * (m_Ro / m_a) ^ p2 * (m_Ro / m_R) ^ p3

Dim p6 As Double
p6 = (2 - m_poisson) * (m_Po + p1)

Dim p7 As Double
p7 = (1 - m_poisson) * (m_Kp * m_Kps + 1) / (m_Kp + m_Kps) + m_poisson

Dim p8 As Double
p8 = (m_Pi + p1) * (m_R / m_a) ^ p2

m_Si = p6 + p4 * p5 + p7 * p8

m_stressRp = p1 - (m_Pi + p1) * (m_R / m_a) ^ p2

m_stressTp = p1 - m_Kp * (m_Pi + p1) * (m_R / m_a) ^ p2

m_dispRp = -m_R / (2 * m_G) * m_Si

End Function

Public Function calc_Ro()

calc_q
calc_Kp

' m_q/(m_kp-1)
Dim p1 As Double
p1 = m_q / (m_Kp - 1)

' 1/(m_kp-1)
Dim p2 As Double

If m_Kp = 1 Then
    p2 = 0
Else
    p2 = 1 / (m_Kp - 1)
End If

m_Ro = m_a * (2 / (m_Kp + 1) * (m_Po + p1) / (m_Pi + p1)) ^ p2

m_stressRo = 1 / (m_Kp + 1) * (2 * m_Po - m_q)

If m_G > 0 And m_R > 0 Then
m_dispRo = -(m_Po - (2 * m_Po - m_q) / (m_Kp + 1)) * m_Ro / (2 * m_G) * m_Ro / m_R
Else
m_dispRo = 0
End If

End Function
Public Function calc()

calc_Ro

Select Case m_R

                Case Is = m_Ro
                m_State = 0
                m_stressR = m_stressRo
                m_stressT = 0
                m_dispR = m_dispRo
                
                Case Is < m_Ro
                m_State = -1
                calc_PlasticRegion
                m_stressR = m_stressRp
                m_stressT = m_stressTp
                m_dispR = m_dispRp
                Case Is > m_Ro
                m_State = 1
                calc_ElasticRegion
                m_stressR = m_stressRe
                m_stressT = m_stressTe
                m_dispR = m_dispRe
                
End Select



End Function

