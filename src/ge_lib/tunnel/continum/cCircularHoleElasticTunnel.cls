VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cCircularHoleElasticTunnel"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False


' ==========================================================================================
' Calculation class for calculating Lined Circular Tunnel in Elastic Medium with Anisotropic Stressess
' Analyticla solution (Einstein and Schwartz 1979)
'
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

Private mR As Double
Private mK As Double
Private mP As Double
Private mTheta As Double

Private mEs As Double
Private mPS As Double

Private mET As Double
Private mPT As Double
Private mA As Double
Private mI As Double
Private mSlipStatus As Integer

Private c As Double
Private F As Double
Private a0 As Double
Private a2 As Double
Private b2 As Double
Private beta As Double
Private d1 As Double
Private f1 As Double
Private M1 As Double

Private mUs As Double ' Us radial displacement
Private mVs As Double ' Vs tangential displacement
Private mT As Double ' T Axial Thrusts
Private mM As Double ' M Bending Moment
Private mSR As Double ' Stress Radial
Private mST As Double ' Stress Tangential
Private Const const_PI = 3.14159
Private Const intNoSlip = 0
Private Const intFullSlip = 1
Public Property Let SlipStatus(var As Integer)
mSlipStatus = var
End Property
Public Property Let Radius(var As Double)
mR = var
End Property
Public Property Let Ko(var As Double)
mK = var
End Property
Public Property Let Pvert(var As Double)
mP = var
End Property
Public Property Let theta_rad(var As Double)
mTheta = var
End Property
Public Property Let Theta_Deg(var As Double)
mTheta = var * const_PI / 180
End Property
Public Property Let E_soil(var As Double)
mEs = var
End Property
Public Property Let Poisson_soil(var As Double)
mPS = var
End Property
Public Property Let E_tunnel(var As Double)
mET = var
End Property
Public Property Let Poisson_tunnel(var As Double)
mPT = var
End Property
Public Property Let Area(var As Double)
mA = var
End Property
Public Property Let Ival(var As Double)
mI = var
End Property
Public Function init(Radius As Double, Ko As Double, Pvert As Double, theta_rad As Double, E_soil As Double, Poiss_soil As Double, E_tun As Double, Poiss_tun As Double, A_tun As Double, I_tun)
mR = Radius
mK = Ko
mP = Pvert
mTheta = theta_rad
mEs = E_soil
mPS = Poiss_soil
mET = E_tun
mPT = Poiss_tun
mA = A_tun
mI = I_tun
End Function

Public Function calc_NoSlip()
mSlipStatus = intNoSlip
c = mEs * mR * (1 - mPT ^ 2) / (mET * mA * (1 - mPS ^ 2))
F = mEs * mR ^ 3 * (1 - mPT ^ 2) / (mET * mI * (1 - mPS ^ 2))

d1 = mP * mR * (1 + mPS) / mEs
M1 = mP * mR ^ 2 / 2
f1 = mP * mR / 2

beta = ((6 + F) * c * (1 - mPS) + 2 * F * mPS) / (3 * F + 3 * c + 2 * c * F * (1 - mPS))
b2 = c * (1 - mPS) / (2 * (c * (1 - mPS) + 4 * mPS - 6 * beta - 3 * beta * c * (1 - mPS)))
a2 = beta * b2
a0 = c * F * (1 - mPS) / (c + F + c * F * (1 - mPS))


mUs = d1 * ((1 + mK) * a0 / 2 + (1 - mK) / 2 * (4 * (1 - mPS) * b2 - 2 * a2) * Cos(2 * mTheta))
mVs = d1 * (-(1 - mK) * (a2 + (1 - 2 * mPS) * b2) * Sin(2 * mTheta))

mSR = mP / 2 * ((1 + mK) * (1 - a0) - (1 - mK) * (1 - 6 * a2 + 4 * b2) * Cos(2 * mTheta))
mST = mP / 2 * ((1 - mK) * (1 + 6 * a2 - 2 * b2) * Sin(2 * mTheta))

mT = f1 * ((1 + mK) * (1 - a0) + (1 - mK) * (1 + 2 * a2) * Cos(2 * mTheta))
mM = M1 * (1 / 2 * (1 - mK) * (1 - 2 * a2 + 2 * b2) * Cos(2 * mTheta))

End Function

Public Function calc_FullSlip()
mSlipStatus = intFullSlip
c = mEs * mR * (1 - mPT ^ 2) / (mET * mA * (1 - mPS ^ 2))
F = mEs * mR ^ 3 * (1 - mPT ^ 2) / (mET * mI * (1 - mPS ^ 2))

d1 = mP * mR * (1 + mPS) / mEs
M1 = mP * mR ^ 2 / 2
f1 = mP * mR / 2

a0 = c * F * (1 - mPS) / (c + F + c * F * (1 - mPS))
a2 = (F + 6) * (1 - mPS) / (2 * F * (1 - mPS) + 6 * (5 - 6 * mPS))

mUs = d1 * ((1 + mK) * a0 / 2 - (1 - mK) * ((5 - 6 * mPS) * a2 - (1 - mPS)) * Cos(2 * mTheta))
mVs = d1 * ((1 - mK) * 1 / 2 * ((5 - 6 * mPS) * a2 - (1 - mPS)) * Sin(2 * mTheta))

mSR = mP / 2 * ((1 + mK) * (1 - a0) - (1 - mK) * (3 - 6 * a2) * Cos(2 * mTheta))
mST = 0

mT = f1 * ((1 + mK) * (1 - a0) + (1 + mK) * (1 - 2 * a2) * Cos(2 * mTheta))
mM = M1 * ((1 - mK) * (1 - 2 * a2) * Cos(2 * mTheta))

End Function

Public Property Get disp_Us() As Double
disp_Us = mUs
End Property
Public Property Get disp_Vs() As Double
disp_Vs = mVs
End Property
Public Property Get Thrust() As Double
Thrust = mT
End Property
Public Property Get Moment() As Double
Moment = mM
End Property
Public Property Get Stress_Radial() As Double
Stress_Radial = mSR
End Property
Public Property Get Stress_Tangential() As Double
Stress_Tangential = mST
End Property

Public Function calc()
Select Case mSlipStatus
            Case Is = intNoSlip
            calc_NoSlip
            Case Is = intFullSlip
            calc_FullSlip
End Select
End Function
