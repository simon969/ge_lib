VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cCoulomb_PIANC"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' all angles in radians
Private m_phi As Double
Private m_w1 As Double
Private m_delta As Double

Private m_kae As Double
Private m_ka As Double
Private m_kpe As Double
Private m_Kp As Double

Property Let phi_rad(vData As Double)
m_phi = vData
End Property
Property Let w1_rad(vData As Double)
m_w1 = vData
End Property
Property Let delta_rad(vData As Double)
m_delta = vData
End Property
Property Get kae() As Double
kae = m_kae
End Property
Property Get Ka() As Double
Ka = m_ka
End Property
Property Get kpe() As Double
kpe = m_kpce
End Property
Property Get Kp() As Double
Kp = m_Kp
End Property
Public Function calc_kae() As Double
Dim p1 As Double
p1 = (1 + (Sin(m_phi + m_delta) * Sin(m_phi - m_w1) / Cos(m_delta + m_w1)) ^ 0.5) ^ 2
m_kae = Cos(m_phi - m_w1) ^ 2 / (Cos(m_w1) * Cos(m_w1 + m_delta) * p1)
calc_kae = m_kae
End Function

Public Function calc_Ka() As Double
Dim p1 As Double
p1 = (1 + (Sin(m_phi + m_delta) * Sin(m_phi) / Cos(m_delta)) ^ 0.5) ^ 2
m_ka = Cos(m_phi) ^ 2 / (Cos(m_delta) * p1)
calc_Ka = m_ka
End Function
Public Function calc_kpe() As Double
Dim p1 As Double
p1 = (1 - (Sin(m_phi + m_delta) * Sin(m_phi - m_w1) / Cos(m_delta + m_w1)) ^ 0.5) ^ 2
m_kpe = Cos(m_phi - m_w1) ^ 2 / (Cos(m_w1) * Cos(m_w1 + m_delta) * p1)
calc_kpe = m_kpe
End Function

Public Function calc_Kp() As Double
Dim p1 As Double
p1 = (1 - (Sin(m_phi + m_delta) * Sin(m_phi) / Cos(m_delta)) ^ 0.5) ^ 2
m_Kp = Cos(m_phi) ^ 2 / (Cos(delta) * p1)
calc_Kp = m_Kp
End Function
