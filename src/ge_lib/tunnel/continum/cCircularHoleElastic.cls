VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cCircularHoleElastic"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

' ==========================================================================================
' For a cylindrical hole in  an infinite, isotropic elastic medium under plain strain conditions,
' the radial and tangential stress distributions are given by the classical Kirsch solution
' (see Jaeger and Cook 1976)
' ==========================================================================================
' Coded   | Simon Thomson
' ==========================================================================================
' Company | AECOM
' ==========================================================================================
' Date    | April 2010
' ==========================================================================================
' Version | 01.00.00
' ==========================================================================================

Option Explicit

Private m_p1 As Double ' horizontal pressure
Private m_P2 As Double ' vertical pressure
Private m_G As Double ' shear modulus
Private m_poisson As Double ' Poisson ratio
Private m_a As Double ' radius of hole
Private m_R As Double ' polar coordinate radius
Private m_theta ' polar cordinate angle

Private m_a2r2 As Double
Private m_a4r4 As Double
Private m_a2r4g As Double

Private m_SR ' Radial Stress
Private m_ST ' Tangential Stress
Private m_SS ' Shear Stress

Private m_Ur ' Radial displacement
Private m_UT ' Tangential displacement

Private Const const_PI = 3.14159

Public Property Let theta_rad(var As Double)
m_theta = var
End Property
Public Property Let Theta_Deg(var As Double)
m_theta = var * const_PI / 180
End Property
Public Property Let Radius_a(var As Double)
m_a = var
End Property
Public Property Let Radius_r(var As Double)
m_R = var
End Property
Public Property Let p1(var As Double)
m_p1 = var
End Property
Public Property Let p2(var As Double)
m_P2 = var
End Property
Public Property Let Gmod(var As Double)
m_G = var
End Property
Public Property Let Poisson(var As Double)
m_poisson = var
End Property
Public Property Get Stress_Radial() As Double
Stress_Radial = m_SR
End Property
Public Property Get Stress_Tangential() As Double
Stress_Tangential = m_ST
End Property
Public Property Get Stress_Shear() As Double
Stress_Shear = m_SS
End Property
Public Property Get Disp_Radial() As Double
Disp_Radial = m_Ur
End Property
Public Property Get Disp_Tangential() As Double
Disp_Tangential = m_UT
End Property

Public Function calc()

m_a2r2 = m_a ^ 2 / m_R ^ 2
m_a4r4 = m_a ^ 4 / m_R ^ 4

m_SR = (m_p1 + m_P2) / 2 * (1 - m_a2r2) + (m_p1 - m_P2) / 2 * (1 - 4 * m_a2r2 + 3 * m_a4r4) * Cos(2 * m_theta)
m_ST = (m_p1 + m_P2) / 2 * (1 + m_a2r2) - (m_p1 - m_P2) / 2 * (1 + 3 * m_a4r4) * Cos(2 * m_theta)
m_SS = -(m_p1 - m_P2) / 2 * (1 + 2 * m_a2r2 - 3 * m_a4r4) * Sin(2 * m_theta)

If m_G > 0 Then
    m_a2r4g = m_a ^ 2 / (4 * m_G * m_R)
    m_Ur = (m_p1 + m_P2) * m_a2r4g + (m_p1 - m_P2) * m_a2r4g * (4 * (1 - m_poisson) - m_a2r2) * Cos(2 * m_theta)
    m_UT = -(m_p1 - m_P2) * m_a2r4g * (2 * (1 - 2 * m_poisson) + m_a2r2) * Sin(2 * m_theta)
Else
    m_Ur = 0
    m_UT = 0
End If

End Function
