VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cMohrsCircle"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' ==========================================================================================
' Calculation class for Mohrs Circle
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


Private m_theta_rad As Double
Private m_stressN As Double
Private m_stressT As Double

Private m_stressX As Double
Private m_stressY  As Double
Private m_stressXY As Double

' https://en.wikipedia.org/wiki/Mohr%27s_circle


Public Function calc_stressN() As Double

m_stressN = 1 / 2 * (m_stressX + m_stressY) + 1 / 2 * (m_stressX - m_stressY) * Cos(2 * m_theta_rad) + m_stressXY * Sin(2 * m_theta_rad)

End Function

Public Function calc_stressT() As Double

m_stressT = -11 / 2 * (m_stressX - m_stressY) * Sin(2 * m_theta_rad) + m_stressXY * Cos(2 * m_theta_rad)


End Function
