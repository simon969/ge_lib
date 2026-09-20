VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cPlaxis_HS"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Private m_E50 As Double
Private m_Ei As Double

Private m_Eoed As Double
Private m_Eur As Double

Private m_Ko As Double
Private m_eint As Double
Private m_pref As Double

Private m_poisson As Double

Private m_Cc As Double
Private m_Cs As Double

Private Const m_poisson_u = 0.495 ' Undrained Poisson ratio
Private m_G As Double ' Shear Modulus
Private m_K As Double ' Bulk Modulus
Private m_Ku As Double  ' Undrained Bulk Modulus

Private m_e As Double ' Drained Elastic Modulus
Private m_Eu As Double ' Undrained Elastic Modulus
Private m_Rf As Double

Private m_q As Double
Private m_qf As Double
Private m_qa As Double

Private m_alpha As Double

Private m_s1 As Double
Private m_s2 As Double
Private m_s3 As Double

Public Property Let Cc(var As Double)
m_Cc = var
End Property
Public Property Get Cc() As Double
Cc = m_Cc
End Property

Public Property Let Cs(var As Double)
m_Cs = var
End Property
Public Property Get Cs() As Double
Cs = m_Cs
End Property
Public Property Let pref(var As Double)
m_pref = var
End Property
Public Property Get pref() As Double
pref = m_pref
End Property
Public Property Let eint(var As Double)
m_eint = var
End Property
Public Property Get eint() As Double
eint = m_eint
End Property
Public Property Let Ko(var As Double)
m_Ko = var
End Property
Public Property Get Ko() As Double
Ko = m_Ko
End Property
Public Property Let Poisson(var As Double)
m_poisson = var
End Property
Public Property Get Poisson() As Double
Poisson = m_poisson
End Property
Public Property Let E(var As Double)
m_e = var
End Property
Public Property Get E() As Double
E = m_e
End Property
Public Property Let Eu(var As Double)
m_Eu = var
End Property
Public Property Get Eu() As Double
Eu = m_Eu
End Property
Public Function calc_Eoed() As Double
m_Eoed = 2.3 * (1 + m_eint) * m_pref / m_Cc
calc_Eoed = m_Eoed
End Function

Public Function calc_Eur() As Double
m_Eur = 2.3 * (1 + m_eint) * (1 + m_poisson) * (1 - 2 * m_poisson) * m_pref / ((1 - m_poisson) * m_Cs * m_Ko)
calc_Eur = m_Eur
End Function
Public Function calc_q(s1 As Double, s2 As Double, s3 As Double) As Double
m_q = s1 + (m_alpha - 1) * s2 - m_alpha * s3
calc_q = m_q
End Function
Public Function calc_qf(c As Double, phi_rad As Double, s3 As Double) As Double
m_qf = c / Tan(phi_rad) - s3 * (2 * Sin(phi_rad)) / (1 - Sin(phi_rad))
m_qa = m_qf / m_Rf
End Function

Public Function calc_Eu() As Double

m_G = m_e / (2 * (1 + m_poisson))
m_Ku = m_G * (1 + m_poisson_u) / (3 * (1 - 2 * m_poisson_u))

m_Eu = 2 * m_G * (1 + m_poisson_u)

calc_Eu = m_Eu

End Function
Public Function calc_alpha(phi_rad As Double)
m_alpha = (3 + Sin(phi_rad)) / (3 - Sin(phi_rad))
End Function
Public Function calc_e1(s1 As Double, s2 As Double, s3 As Double) As Double

calc_q s1, s2, s3

m_Ei = 2 * m_E50 / (2 - m_Rf)

End Function


Private Sub Class_Initialize()
m_Rf = 0.9
End Sub
