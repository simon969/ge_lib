VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cGRC_Salencon1969"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'
'
' The ground response curve (GRC) can be constructed from the ealsto plastic solution of a
' circular tunnel radius, r, subject to a uniform stress field Po and internal
' pressuer Pi. It may happen that that the stress induced in the rock following
' excavation will exceed the yield strength of the rock mass and a plastic zone of
' Radius Rp will develope around the tunnel. The rock outsixde the boundary defined by Rp
' is assumed to remain elastic. This is the formulation based on Salencon 1969
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
Private m_CHMC As cCircularHoleMC_Salencon1969
' ==========================================================================================
' Output parameters
' ==========================================================================================

'radius of plastic zone around hole
Private m_Pcr As Double
Private m_Rp As Double

Private m_Ur As Double
Private m_Ure As Double
Private m_Urp As Double
Private Const const_PI = 3.14159

'Input parameters
Private Function get_CHMC() As cCircularHoleMC_Salencon1969

If m_CHMC Is Nothing Then
m_CHMC = New cCircularHoleMC_Salencon1969
End If

Set get_CHMC = m_CHMC

End Function
Public Property Let dilation_rad(var As Double)
get_CHMC.dilation_rad = var
End Property
Public Property Let dilation_deg(var As Double)
get_CHMC.dilation_deg = var
End Property
Public Property Let friction_rad(var As Double)
get_CHMC.friction_rad = var
End Property
Public Property Let friction_deg(var As Double)
get_CHMC.friction_deg = var
End Property
Public Property Let cohesion(var As Double)
get_CHMC.cohesion = var
End Property
Public Property Let Radius_r(var As Double)
get_CHMC.Radius_r = var
End Property
Public Property Let Po(var As Double)
get_CHMC.Po = var
End Property
Public Property Let PI(var As Double)
get_CHMC.PI = var
End Property
Public Property Let Emod(var As Double)

If get_CHMC.Poisson > 0 Then
Dim ec As cElastic_Constants
Set ec = New cElastic_Constants
ec.E = var
ec.Poisson = get_CHMC.Poisson
get_CHMC.Gmod = ec.calc_EPoisson("g")
Else
get_CHMC.Gmod = 0
End If

End Property
Public Property Let Poisson(var As Double)
get_CHMC.Poisson = var
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
With m_CHMC
        m_Pcr = (1 - Sin(.friction_rad)) * .Po - .cohesion * Cos(.friction_rad)
End With
 End Function
Public Function calc_Ure()

 '   m_Ure = (1 + m_Poisson) / m_E * m_R * (m_Po - m_Pi)

End Function
Public Function calc_Urp()
'Dim p1, p2, p3, p4, p5 As Double
'
'Dim cot, cot_res As Double
'cot = m_c / Tan(m_phi_rad)
'cot_res = m_c_res / Tan(m_phi_res_rad)
'
'p1 = Sin(m_phi_rad) * cot * m_Rp ^ (m_k + 1) / m_R ^ m_k
'p2 = (2 - 2 * m_Poisson) * (m_Po + cot_res) / m_R ^ m_k
'p3 = (1 + m_k * m_Nr - m_Poisson * (m_k + 1) * (m_Nr + 1)) / ((m_Nr + m_k) * m_R ^ (m_Nr - 1))
'p4 = (m_Pi + cot_res) * (m_Rp ^ (m_Nr + m_k)) / m_R ^ m_k * m_R ^ m_Nr
'
'm_Urp = (1 + m_Poisson) / m_E * (p1 + p2 - p3 * p4)
'

End Function
Private Function calc_K()
'If 1 - Sin(m_dilation_rad) = 0 Then
'    m_k = 0
'Else
'    m_k = (1 + Sin(m_dilation_rad)) / (1 - Sin(m_dilation_rad))
'End If
End Function



Public Function calc_Rp()

m_CHMC.calc_Ro

m_Rp = m_CHMC.Ro

End Function

Public Function calc_Ur() As Double

calc_Pcr
calc_Ure
calc_K
calc_Rp
calc_Urp

If (m_Pcr > 0 And m_CHMC.PI > m_Pcr) Then
    m_Ur = m_Ure
Else
    m_Ur = m_Urp + m_Ure
End If

calc_Ur = m_Ur

End Function

