VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cSubgrade_BROMS"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

' Reference :   Subgrade Modulus of Laterally loaded Piles in Clays
'                   Danial O Wong
'               Transportation Research Record 1331
' ==============================================================
'               Single piles- static capacity and lateral loads,
'               16-15 Laterally loaded piles,
'               Equations 16-31,  16-32, 16-32a, 16-33
' ==============================================================
' Coded by : AECOM Simon Thomson
' ==============================================================
' Checked by :
' ==============================================================
' Version : 0.1
' ==============================================================
' Date 07 July 2018
' ==============================================================
' This code is the copyright of AECOM. No part of this
' code may be reproduced without the prior permission
' ==============================================================

' ==============================================================
'                     Input and Output Variables
' ==============================================================

' B: diameter of rigid circular plate
Private mB As Double

'E: Young 's modulus of soil from rigid circular plate
' loading test of plate diameter B
Private mEs As Double

'v: Poisson 's ratio of soil
Private mPoisson As Double

Private mLp As Double

'kh: horizontal subgrade reaction coefficient for diameter B
Private mkh As Double


Public Property Let Es(newValue As Double)
    mEs = newValue
End Property
Public Property Let B(newValue As Double)
    mB = newValue
End Property
Public Property Let Poisson(newValue As Double)
    mPoisson = newValue
End Property
Public Property Let Lp(newValue As Double)
    mLp = newValue
End Property
Public Property Get kh() As Double
    kh = mkh
End Property
Public Function calc_kh() As Double
Dim p1, p2 As Double
p1 = (1 + mPoisson) * (3 - 4 * mPoisson)
p2 = 2 * Log(2 * mLp / mB) - 0.433

mkh = 22.4 * mEs * (1 - mPoisson) / (p1 * p2)

End Function


