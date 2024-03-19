VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cTerzaghi1d_Craig"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
' ==============================================================
'     1D Consolidation
' ==============================================================
' Reference :
'               Soil Mechanics Sixth Edition
'               Craig 1997 p2269 - p274
' ==============================================================
' Coded : AECOM Simon Thomson
' ==============================================================
' Checked by :
' ==============================================================
' Version : 2.1
' ==============================================================
' Date 11th September 2013
' ==============================================================
' This code is the copyright of AECOM. No part of this
' code may be reproduced without the prior permission
' ==============================================================

' ==============================================================
'                     Input and Output Variables
' ==============================================================

Private Type typedU
du As Double
z As Double
End Type

Private Type typeU
U As Double
t As Double
End Type

Private m_Cv As Double
Private m_Mv As Double
Private m_H As Double
Private m_p1 As Double
Private m_Uc As Double
Private m_dU() As typedU
Private m_U() As typeU
Private m_timesteps As Double
Private m_hsteps As Double
Private ResA() As Double
Const constPI = 3.14159

Public Property Let Mv(var As Double)
Let m_Mv = var
End Property
Public Property Let Cv(var As Double)
Let m_Cv = var
End Property

Public Property Let H(ByVal var As Double)
Let m_H = var
End Property

Public Property Let p1(ByVal var As Double)
Let m_p1 = var
End Property
Public Function calc_dUProfileAllTime(totaltime As Double, timesteps As Integer, hsteps As Integer)
Dim ttime As Double
Dim I As Integer

m_hsteps = hsteps
m_timesteps = timesteps

ReDim m_dU(m_timesteps, m_hsteps)
ReDim m_U(m_timesteps)

For I = 1 To m_timesteps
ttime = I / m_timesteps
calc_dUProfileTime ttime, hsteps, I
Next I

End Function
Public Function calc_dUProfileTime(time As Double, hsteps As Integer, Optional I As Integer = 0) As Variant
Dim j As Integer

ReDim ResA(1 To hsteps + 1, 1 To 1)

If I = 0 Then
m_hsteps = hsteps
ReDim m_U(1)
ReDim m_dU(1, m_hsteps)
I = 1
End If

m_U(I).t = time
m_U(I).U = sum_U(time)
calc_dUProfile time, I

ResA(1, 1) = m_U(I).U
For j = 1 To m_hsteps
ResA(1 + j, 1) = m_dU(I, j).du
Next j

calc_dUProfileTime = ResA

End Function
Public Function calc_dUProfileTimeRange(time As Double, rhsteps As Range, Optional I As Integer = 0) As Variant
Dim j As Integer

ReDim ResA(1 To rhsteps.Rows.count + 1, 1 To 1)

If I = 0 Then
ReDim m_U(1)
ReDim m_dU(1, rhsteps.Rows.count)
I = 1
End If

If time < 0 Then
calc_dUProfileTimeRange = ResA
Exit Function
End If

m_U(I).t = time
m_U(I).U = sum_U(time)
calc_dUProfileRange time, I, rhsteps

ResA(1, 1) = m_U(I).U
For j = 1 To rhsteps.Rows.count
ResA(1 + j, 1) = m_dU(I, j).du
Next j

calc_dUProfileTimeRange = ResA

End Function


Private Function calc_dUProfile(t As Double, I As Integer)
Dim z As Double
Dim j As Integer

For j = 1 To m_hsteps
z = j * m_H / m_hsteps
m_dU(I, j).z = z
m_dU(I, j).du = sum_dU(z, t)
Next j

End Function
Private Function calc_dUProfileRange(t As Double, I As Integer, rhsteps As Range)
Dim z As Double
Dim j As Integer

For j = 1 To rhsteps.Rows.count
z = m_H * rhsteps(j, 1)
m_dU(I, j).z = z
m_dU(I, j).du = sum_dU(z, t)
Next j

End Function
Public Function calc_Uc(dp1 As Double) As Double
m_Uc = m_Mv * m_H * dp1
calc_Uc = m_Uc
End Function
Public Function get_t50() As Double
get_t50 = get_timeTo(0.5)
End Function
Public Function get_t90() As Double
get_t90 = get_timeTo(0.9)
End Function
Public Function get_timeTo(percUt As Double) As Double
Dim I As Integer
For I = 1 To m_timesteps
    If m_U(I).U > percUt Then
    percUt = m_U(I).t
    Exit For
    End If
Next I

End Function
Private Function sum_dU(z As Double, t As Double, Optional mcount = 100) As Double
Dim M As Integer
Dim M1, p101, p102 As Double
Dim du As Double
Dim Tv As Double

Tv = m_Cv * t / m_H ^ 2

For M = 0 To mcount
M1 = constPI / 2 * (2 * M + 1)
p101 = Exp(-M1 ^ 2 * Tv)
p102 = Sin(M1 * z / m_H)
du = du + 2 * m_p1 / M1 * p101 * p102
Next M

sum_dU = du

End Function
Private Function sum_U(t As Double, Optional mcount = 100) As Double
Dim M As Integer
Dim M1 As Double
Dim p1, p2 As Double
Dim du As Double
Dim Tv As Double

Tv = m_Cv * t / m_H ^ 2

For M = 0 To mcount
M1 = constPI / 2 * (2 * M + 1)
p1 = Exp(-M1 ^ 2 * Tv)
p2 = 2 / M1 ^ 2
du = du + p1 * p2
Next M

sum_U = 1 - du

End Function
Public Function Print_dUProfile(Optional xlRange As Range = Nothing)
Dim I As Integer
Dim j As Integer

For I = 1 To m_timesteps
Debug.Print I, m_U(I).t, m_U(I).U
For j = 1 To m_hsteps
Debug.Print j, m_dU(I, j).z, m_dU(I, j).du
If Not xlRange Is Nothing Then
xlRange(I, j) = m_dU(I, j).du
End If

Next j
Next I

End Function

