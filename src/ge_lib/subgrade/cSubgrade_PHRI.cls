VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cSubgrade_PHRI"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
' ==============================================================
'  Reference :    SOILS AND FOUNDATIONS Vol. 45, No. 3, 51-70, June 2005
'            Japanese Geotechnical Society
' ==============================================================
' ESTIMATION OF SUBGRADE REACTION COEFFICIENT FOR HORIZONTALLY
' LOADED PILES BY STATISTICAL ANALYSES
' YUSUKE HONJO, YULVI ZAIKA and GYANESWOR POKHAREL
'
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


'Ah horizontal component of load of area Ah=D(1/beta)
Private mAh As Double

'alphak correction factor
Private malphak As Double

'beta chracteristic value of a pile beta=(kh*D/4EI)^0.25
Private mbeta As Double

'EI flexural stiffness of pile
Private mEI As Double

'E: Young 's modulus of soil from rigid circular plate
' loading test of plate diameter B
Private mEo As Double
Private mE30 As Double

'Ip: shape coefficient (for circular shape, 4 = 0.79)
Private mIp As Double

Private mD As Double

'v: Poisson 's ratio of soil
Private mPoisson As Double

Private mEf As Double

'kh: horizontal subgrade reaction coefficient for diameter B
Private mkh As Double

'k30 horizontal subgrade reaction for 30cm diameter plate
Private mk30 As Double

Public Property Let Eo(newValue As Double)
    mEo = newValue
End Property
Public Property Let D(newValue As Double)
    mD = newValue
End Property
Public Property Let EI(newValue As Double)
    mEI = newValue
End Property
Public Property Let k30(newValue As Double)
    mk30 = newValue
End Property
Public Property Let E30(newValue As Double)
    mE30 = newValue
End Property
Public Function calc_kh()
'mkh = mk30 / ((mB / 30) ^ (-3 / 4))
End Function
Public Function calc_kh30() As Double
mkh = mk30 / 30 * malphak * mEo
End Function

