VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cSubgrade_VESIC"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' ==============================================================
'  Reference :    Special Footings and Beams on Elastic Foundations
'                   Bowles p501
' ==============================================================
' Estimation of subgrade reaction based on VESIC (1961a, 1961b)
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
' modulus of soil
Private mEs As Double

'possion ratio of soil
Private mPoisson As Double

'breadth of footing
Private mB As Double

' modulus of footing
Private mEf As Double

' moment of inertia of footing based on crossection
Private mIf As Double

'subgrade reaction pressure/m
Private mks As Double

Public Property Let Esoil(newValue As Double)
    mEs = newValue
End Property
Public Property Let B(newValue As Double)
    mB = newValue
End Property
Public Property Let Poisson(newValue As Double)
    mPoisson = newValue
End Property
Public Property Let Ifooting(newValue As Double)
    mIf = newValue
End Property
Public Property Let Efooting(newValue As Double)
    mEf = newValue
End Property

Public Function calcKs() As Double

    mks = 0.65 * ((mEs * mB ^ 4) / (mEf * mIf)) ^ (1 / 12) * mEs / (1 - mPoisson ^ 2) / mB
   
    calcKs = mks

End Function
