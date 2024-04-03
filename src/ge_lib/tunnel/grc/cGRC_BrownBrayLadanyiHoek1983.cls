VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cGRC_BrownBrayLadanyiHoek1983"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'
'Ground response curves for rock tunnels

'ET Brown, JW Bray, B Ladanyi… - Journal of Geotechnical …, 1983 - ascelibrary.org
' Calculations of support pressure-tunnel convergence relationships, or ground response
' curves are used to improve understanding or rocksupport interaction and to aid in the
' dimensioning of tunnel support elements. Methods of response curve calculation are...
' The ground response curve (GRC) can be constructed from the ealsto plastic solution of a
' circular tunnel radius, r, subject to a uniform stress field Po and internal
' pressuer Pi. It may happen that that the stress induced in the rock following
' excavation will exceed the yield strength of the rock mass and a plastic zone of
' Radius Rp will develope around the tunnel. The rock outsixde the boundary defined by Rp
' is assumed to remain elastic. Several solutions of this type based on the Mohr Coulomb
' failure criterion for rock have been developed. This is Jian-gong VChen etal (EJGE Vol 17 2012 Bund, T)
' representation of the original solution Brown etal 1983. Which is still widely used in practice.
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
Private m_R As Double

'Mohr-Coloumb failure criterion
Private m_phi_rad As Double
Private m_dilation_rad As Double
Private m_c As Double

'Residual failure criterion
Private m_phi_res_rad As Double
Private m_c_res As Double

'Elastic stiffness properties
Private m_poisson As Double
Private m_e As Double

'Internal and external radial pressures
Private m_Pi As Double
Private m_Po As Double


' ==========================================================================================
' Output parameters
' ==========================================================================================

'radius of plastic zone around hole
Private m_Rp As Double
Private m_Pcr As Double

Private m_K As Double
Private m_Nr As Double

Private m_Ure As Double
Private m_Urp As Double
Private m_Ur As Double

Private Const const_PI = 3.14159

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
Public Property Let friction_deg(var As Double)
m_phi_rad = var * const_PI / 180
End Property
Public Property Let cohesion(var As Double)
m_c = var
End Property
Public Property Let friction_res_rad(var As Double)
m_phi_res_rad = var
End Property
Public Property Let friction_res_deg(var As Double)
m_phi_res_rad = var * const_PI / 180
End Property
Public Property Let cohesion_res(var As Double)
m_c_res = var
End Property
Public Property Let Radius_r(var As Double)
m_R = var
End Property
Public Property Let Po(var As Double)
m_Po = var
End Property
Public Property Let PI(var As Double)
m_Pi = var
End Property
Public Property Let Emod(var As Double)
m_e = var
End Property
Public Property Let Poisson(var As Double)
m_poisson = var
End Property
Public Property Get Pcr() As Double
Pcr = m_Pcr
End Property
Public Property Get Urp() As Double
Urp = m_Urp
End Property
Public Property Get Ure() As Double
Ure = m_Ure
End Property
Public Property Get Ur() As Double
Ur = m_Ur
End Property
Public Property Get Rp() As Double
Rp = m_Rp
End Property
' The scaled critical internal pressure, defined by point E on the
' Ground Response Curve. for which the elastic limit is achieved is Pcr
Public Function calc_Pcr()

        m_Pcr = (1 - Sin(m_phi_rad)) * m_Po - m_c * Cos(m_phi_rad)

 End Function
Public Function calc_Ure()

    m_Ure = (1 + m_poisson) / m_e * m_R * (m_Po - m_Pi)

End Function
Public Function calc_Urp()
Dim p1, p2, p3, p4, p5 As Double

Dim cot, cot_res As Double
cot = m_c / Tan(m_phi_rad)
cot_res = m_c_res / Tan(m_phi_res_rad)

p1 = Sin(m_phi_rad) * cot * m_Rp ^ (m_K + 1) / m_R ^ m_K
p2 = (2 - 2 * m_poisson) * (m_Po + cot_res) / m_R ^ m_K
p3 = (1 + m_K * m_Nr - m_poisson * (m_K + 1) * (m_Nr + 1)) / ((m_Nr + m_K) * m_R ^ (m_Nr - 1))
p4 = (m_Pi + cot_res) * (m_Rp ^ (m_Nr + m_K)) / m_R ^ m_K * m_R ^ m_Nr

m_Urp = (1 + m_poisson) / m_e * (p1 + p2 - p3 * p4)


End Function
Private Function calc_K()
If 1 - Sin(m_dilation_rad) = 0 Then
    m_K = 0
Else
    m_K = (1 + Sin(m_dilation_rad)) / (1 - Sin(m_dilation_rad))
End If
End Function

Private Function calc_Nr()
If 1 - Sin(m_phi_rad) = 0 Then
    m_Nr = 0
Else
    m_Nr = (1 + Sin(m_phi_rad)) / (1 - Sin(m_phi_rad))
End If

End Function

Public Function calc_Rp()
Dim p1, p2, p3, p4 As Double

p1 = m_Po + m_c_res / Tan(m_phi_res_rad)
p2 = (m_Po + m_c / Tan(m_phi_rad)) * Cos(m_phi_rad)
p3 = m_Pi + m_c_res / Tan(m_phi_res_rad)
p4 = (1 - Sin(m_phi_res_rad)) / (2 * Sin(m_phi_res_rad))

m_Rp = m_R * ((p1 - p2) ^ p4) / p3

End Function

Public Function calc_Ur() As Double

calc_Pcr
calc_Ure
calc_K
calc_Nr
calc_Rp
calc_Urp

If (m_Pcr > 0 And m_Pi > m_Pcr) Then
    m_Ur = m_Ure
Else
    m_Ur = m_Urp + m_Ure
End If

calc_Ur = m_Ur

End Function
