VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cSubgrade_TERZAGHI"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' ==============================================================
'
'
' ==============================================================
' Reference : Estimation of subgrade reaction based on
'              TERZAGHI 1943 p 382
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

' Shape coefficient for Circular shape Ip=0.79
Private mIp As Double

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
Public Property Let Ip(newValue As Double)
    mIp = newValue
End Property

Public Function calcKs() As Double

    mks = mEs / (mIp * (1 - mPoisson ^ 2) / mB)
   
    calcKs = mks

End Function

