VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cGRC_Eberhardt"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' The ground response curve (GRC) can be constructed from the ealsto plastic solution of a
' circular tunnel radius, r, subject to a uniform stress field Po and internal
' pressuer Pi. It may happen that that the stress induced in the rock following
' excavation will exceed the yield strength of the rock mass and a plastic zone of
' Radius Rp will develope around the tunnel. The rock outsixde the boundary defined by Rp
' is assumed to remain elastic. Several solutions of this type based on the Mohr Coulomb
' failure criterion for rock have been developed.
' This is the method detailed by Dr Erik Eberhardt Tunnel Grad Class 2014.
'
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
' =============\=============================================================================
'radius of hole and radius to point under considerartion
Private m_R As Double

'Mohr-Coloumb failure criterion
Private m_phi_rad As Double
Private m_c As Double
Private m_ucs As Double

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

Private m_Ure As Double
Private m_Urp As Double
Private m_Ur As Double

Private Const const_PI = 3.14159


'Input stub parameters not used by class
Public Property Let dilation_rad(var As Double)
End Property
Public Property Let dilation_deg(var As Double)
End Property
Public Property Let friction_res_rad(var As Double)
End Property
Public Property Let friction_res_deg(var As Double)
End Property
Public Property Let cohesion_res(var As Double)
End Property

'Input parameters used by class
Public Property Let friction_rad(var As Double)
m_phi_rad = var
End Property
Public Property Let friction_deg(var As Double)
m_phi_rad = var * const_PI / 180
End Property
Public Property Let cohesion(var As Double)
m_c = var
End Property
Public Property Let ucs(var As Double)
m_ucs = var
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
Private Function calc_ucs()

m_ucs = 2 * m_c * Cos(m_phi_rad) / (1 - Sin(m_phi_rad))

End Function
' The scaled critical internal pressure, defined by point E on the
' Ground Response Curve. for which the elastic limit is achieved is Pcr
Public Function calc_Pcr()

    m_Pcr = (2 * m_Po - m_ucs) / (1 + m_K)

 End Function
Public Function calc_Ure()

    m_Ure = (1 + m_poisson) / m_e * m_R * (m_Po - m_Pi)

End Function
Public Function calc_Urp()
Dim p1, p2 As Double

p1 = 2 * (1 - m_poisson) * (m_Po - m_Pcr) * (m_Rp / m_R) ^ 2
p2 = (1 - 2 * m_poisson) * (m_Po - m_Pi)

m_Urp = m_R * (1 + m_poisson) / m_e * (p1 - p2)


End Function
Private Function calc_K()
If 1 - Sin(m_phi_rad) = 0 Then
    m_K = 0
Else
    m_K = (1 + Sin(m_phi_rad)) / (1 - Sin(m_phi_rad))
End If
End Function

Public Function calc_Rp()
Dim p1, p2, p3, p4 As Double

p1 = 2 * (m_Po * (m_K - 1) + m_ucs)
p2 = (1 + m_K) * ((m_K - 1) * m_Pi + m_ucs)
p3 = 1 / (m_K - 1)

m_Rp = m_R * (p1 / p2) ^ p3


End Function

Public Function calc_Ur() As Double
calc_ucs
calc_K
calc_Pcr
calc_Ure
calc_Rp
calc_Urp

If (m_Pcr > 0 And m_Pi > m_Pcr) Then
    m_Ur = m_Ure
Else
    m_Ur = m_Urp + m_Ure
End If

calc_Ur = m_Ur

End Function


