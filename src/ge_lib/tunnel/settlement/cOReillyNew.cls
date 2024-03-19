VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cOReillyNew"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Const const_PI As Double = 3.14159
Private m_K As Double
Private m_z0 As Double ' z ordinate
Private m_i As Double
Private m_y As Double ' y ordinate
Private m_Smax As Double ' Max vertical Movement
Private m_Sv As Double ' Vertical Movement
Private m_Sh As Double ' Horizontal movement
Private m_Vloss As Double ' Volume Loss

' input paramaters
Public Property Let I(vNewData As Double)
m_i = vNewData
End Property
Public Property Let z0(vNewData As Double)
m_z0 = vNewData
End Property
Public Property Let y(vNewData As Double)
m_y = vNewData
End Property
Public Property Let k(vNewData As Double)
m_K = vNewData
End Property
Public Property Let Vloss(vNewData As Double)
m_Vloss = vNewData
End Property

'output parameters
Public Property Get I() As Double
I = m_i
End Property
Public Property Get Smax() As Double
Smax = m_Smax
End Property
Public Property Get Sv() As Double
Sv = m_Sv
End Property
Public Property Get Sh() As Double
Sh = m_Sh
End Property

' calculations
Public Function calc_Sv()
m_Sv = m_Smax * Exp(-m_y ^ 2 / 2 * m_i ^ 2)
End Function
Public Function calc_Sh()
m_Sh = m_y / m_z0 * m_Sv
End Function
Public Function calc_i()
m_i = m_K * m_z0
End Function
Public Function calc_Smax()
m_Smax = m_Vloss / ((2 * const_PI) ^ 0.5 * m_i)
End Function
Public Function calc()
calc_i
    
    If m_i > 0 And m_Vloss > 0 Then
        calc_Smax
    Else
    m_Smax = 0
    End If
    
 calc_Sv
 calc_Sh

End Function

