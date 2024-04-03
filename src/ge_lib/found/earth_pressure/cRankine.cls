VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cRankine"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

' ==========================================================================================
' Rankine theory (Rankine 1857)  presents a solution for a mass of cohesionless soil
' in a state of limiting equilibrium.The magnitude of horz stress depends only on
' the vertical effective stress and the shear strength of the soil.
' No aaccount is taken of displacment as so this is a lower bound solution
' ref Basic Soil Mechanics Roy EWhitlow 4th Edition Eq 8.10(a0 and 8.10(b)
'
' The Bell (Bell 1915) extension of the Rankine theory is incorporeated in the paramters
' kac and kap
' ref Basic Soil Mechanics Roy EWhitlow 4th Edition Eq 8.11(a0 and 8.11(b)
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

' all angles in radians
' input parameters
Private Const const_PI = 3.14159
Private m_phi_rad As Double ' friction angle
Private m_beta_rad As Double ' back slope angle
Private m_c As Double ' cohesion
Private m_G As Double

' calculated output parameters
Private m_ka As Double
Private m_Kp As Double
Private m_kac As Double
Private m_kpc As Double
Private m_z0 As Double

' temp variables
Private s1 As Double
Private s2 As Double
Private s3 As Double
Property Let phi_rad(vData As Double)
m_phi_rad = vData
End Property
Property Let phi_deg(vData As Double)
m_phi_rad = vData * const_PI / 180
End Property
Property Let beta_rad(vData As Double)
m_beta_rad = vData
End Property
Property Let beta_deg(vData As Double)
m_beta_rad = vData * const_PI / 180
End Property
Property Let g(vData As Double)
m_G = vData
End Property
Property Let c(vData As Double)
m_c = vData
End Property
Property Get phi_rad() As Double
phi_rad = m_phi_rad
End Property
Property Get Ka() As Double
Ka = m_ka
End Property
Property Get Kp() As Double
Kp = m_Kp
End Property
Property Get kac() As Double
kac = m_kac
End Property
Property Get kpc() As Double
kpc = m_kpc
End Property
Public Function calc_Kp() As Double
s1 = (Cos(m_beta_rad) ^ 2 - Cos(m_phi_rad) ^ 2) ^ 0.5
m_Kp = (Cos(m_beta_rad) + s1) / (Cos(m_beta_rad) - s1)
calc_Kp = m_Kp
End Function
Public Function calc_Ka() As Double
s1 = (Cos(m_beta_rad) ^ 2 - Cos(m_phi_rad) ^ 2) ^ 0.5
m_ka = (Cos(m_beta_rad) - s1) / (Cos(m_beta_rad) + s1)
calc_Ka = m_ka
End Function
Public Function calc_Kac() As Double
calc_Ka
m_kac = 2 * (m_ka) ^ 0.5
calc_Kac = m_kac
End Function
Public Function calc_Kpc() As Double
calc_Kp
m_kpc = 2 * (m_Kp) ^ 0.5
calc_Kpc = m_kpc
End Function
Public Function calc_z0() As Double
calc_Ka

If m_G * m_ka > 0 Then
    m_z0 = 2 * m_c / (m_G * m_ka ^ 0.5)
Else
    m_z0 = 0
End If

calc_z0 = m_z0

End Function
Public Function calc()
calc_Kac
calc_Kpc
calc_z0
End Function

Public Function calc_Active(v As Double) As Double
calc_Active = v * m_ka - m_kac * m_c
End Function
Public Function calc_Passive(v As Double) As Double
calc_Passive = v * m_Kp + m_kpc * m_c
End Function
Public Function calc_zc(p As Double) As Double
' Equation 8.39a
If m_G > 0 Then
calc_zc = (m_ka ^ 2 / (1 - m_ka ^ 2)) ^ 0.5 * (2 * p / (const_PI * m_G)) ^ 0.5
Else
calc_zc = 0
End If
End Function
Public Function calc_hc(p As Double) As Double
' Equation 8.41
If m_G > 0 Then
calc_hc = 1 / m_ka * (2 * p / (const_PI * m_G)) ^ 0.5
Else
calc_hc = 0
End If
End Function
