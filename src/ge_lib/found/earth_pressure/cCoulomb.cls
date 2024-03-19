VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cCoulomb"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' ==========================================================================================
' Coulomb theory (1776) involves consideration of the stability, as a whole,
' of the wedge of soil between the retaining wall and a trial failure plane.
' Foundation Analysis and Design Fifth Edition
' Joseph E Bowles PE SE 1997
' 11-4 Coulomb Earth Pressure Theory Section Page 594
' ==========================================================================================
' Coded  | Simon Thomson
' ==========================================================================================
' Company | AECOM
' ==========================================================================================
' Date    | April 2010
' ==========================================================================================
' Version | 01.00.00
' ==========================================================================================



Option Explicit

' input parameters
' all angles in radians
Private m_phi_rad As Double
Private m_beta_rad As Double ' back slope angle
Private m_alpha_rad As Double ' wall angle to horizontal
Private m_delta_rad As Double ' wall angle to horizontal
Private Const const_PI = 3.14159

Private m_cw As Double
Private m_c As Double
Private m_G As Double

'output parameters
Private m_ka As Double
Private m_kac As Double
Private m_kpc As Double
Private m_Kp As Double
Private m_z0 As Double

' temp variables
Private s1 As Double
Private s2 As Double
Private s3 As Double

Property Let g(vData As Double)
m_G = vData
End Property
Property Let phi_deg(vData As Double)
m_phi_rad = vData * const_PI / 180
End Property
Property Let beta_deg(vData As Double)
m_beta_rad = vData * const_PI / 180
End Property
Property Let alpha_deg(vData As Double)
m_alpha_rad = vData * const_PI / 180
End Property
Property Let delta_deg(vData As Double)
m_delta_rad = vData * const_PI / 180
End Property
Property Let phi_rad(vData As Double)
m_phi_rad = vData
End Property
Property Let alpha_rad(vData As Double)
m_alpha_rad = vData
End Property
Property Let beta_rad(vData As Double)
m_beta_rad = vData
End Property
Property Let delta_rad(vData As Double)
m_delta_rad = vData
End Property
Property Let cw(vData As Double)
m_cw = vData
End Property
Property Let c(vData As Double)
m_c = vData
End Property
Property Get phi_rad() As Double
phi_rad = m_phi_rad
End Property
Property Get kac() As Double
kac = m_kac
End Property
Property Get Ka() As Double
Ka = m_ka
End Property
Property Get kpc() As Double
kpc = m_kpc
End Property
Property Get Kp() As Double
Kp = m_Kp
End Property
Property Get z0() As Double
z0 = m_z0
End Property

Public Function calc_Kp()
' Equation 11-6 Page 596
s1 = (Sin(m_alpha_rad - m_phi_rad)) ^ 2
s2 = Sin(m_alpha_rad) ^ 2 * Sin(m_alpha_rad + m_delta_rad)
s3 = Sin(m_phi_rad + m_delta_rad) * Sin(m_phi_rad + m_beta_rad) / (Sin(m_alpha_rad + m_delta_rad) * Sin(m_alpha_rad + m_beta_rad))

If (s2 * (1 - s3 ^ 0.5) ^ 2 = 0) Then
    m_Kp = 0
Else
    m_Kp = s1 / (s2 * (1 - s3 ^ 0.5) ^ 2)
End If

calc_Kp = m_Kp
End Function
Public Function calc_Ka() As Double
' Equation 11-3 Page 595
s1 = (Sin(m_alpha_rad + m_phi_rad)) ^ 2
s2 = Sin(m_alpha_rad) ^ 2 * Sin(m_alpha_rad - m_delta_rad)
s3 = Sin(m_phi_rad + m_delta_rad) * Sin(m_phi_rad - m_beta_rad) / (Sin(m_alpha_rad - m_delta_rad) * Sin(m_alpha_rad + m_beta_rad))

If (s2 * (1 + s3 ^ 0.5) ^ 2 = 0) Then
    m_ka = 0
Else
    m_ka = s1 / (s2 * (1 + s3 ^ 0.5) ^ 2)
End If

calc_Ka = m_ka
End Function

Public Function calc_Kac() As Double

If m_c > 0 Then
    m_kac = 2 * (m_ka * (1 + m_cw / m_c)) ^ 0.5
Else
    m_kac = 2 * m_kac ^ 0.5
End If

calc_Kac = m_kac

End Function
Public Function calc_Kpc() As Double

If m_c > 0 Then
    m_kpc = 2 * (m_Kp * (1 + m_cw / m_c)) ^ 0.5
Else
    m_kpc = 2 * m_Kp ^ 0.5
End If

calc_Kpc = m_kpc

End Function
Public Function calc_z0() As Double

If m_c > 0 & m_G * m_ka > 0 Then
    m_z0 = 2 * m_c * (1 + m_cw / m_c) ^ 0.5 / (m_G * m_ka ^ 0.5)
Else
    m_z0 = 0
End If

calc_z0 = m_z0

End Function
Public Function calc()
calc_Ka
calc_Kac
calc_Kp
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
