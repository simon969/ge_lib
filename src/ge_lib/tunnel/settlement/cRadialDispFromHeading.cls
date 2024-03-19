VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cRadialDispFromHeading"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private m_LamdaD As Double
Private m_x As Double
Private m_R As Double
Private m_PfictFactor As Double
Private Enum enumCalc_Method
        None = 0
        Panet = 1
        Hoek = 2
End Enum

Property Let x(var As Double)
m_x = var
End Property
Property Let r(var As Double)
m_R = var
End Property
Property Get LamdaD() As Double
LamdaD = m_LamdaD
End Property
Property Get PfictFactor() As Double
PfictFactor = m_PfictFactor
End Property
Private Function get_enumMethod(Method As String) As enumCalc_Method
If Len(Method) = 0 Then get_enumMethod = enumCalc_Method.None
If InStr("hoek", LCase(Method)) Then get_enumMethod = enumCalc_Method.Hoek
If InStr("panet", LCase(Method)) Then get_enumMethod = enumCalc_Method.Panet
End Function
Public Function calc_LamdaD(Method As String)
Dim enum_method As enumCalc_Method

enum_method = get_enumMethod(Method)

Select Case enum_method
        Case Is = enumCalc_Method.Panet
                calc_LamdaD_Panet1995
        Case Is = enumCalc_Method.Hoek
                calc_LamdaD_Hoek1999
End Select

End Function

Public Function calc_LamdaD_Panet1995()
m_LamdaD = 0.25 + 0.75 * (1 - (0.75 / (0.75 + m_x / m_R)) ^ 2)
End Function
Public Function calc_LamdaD_Hoek1999()
m_LamdaD = (1 + Exp(-m_x / (1.1 * m_R))) ^ (-1.7)
End Function
Public Function calc_PfictFactor(Method As String)
Dim enum_method As enumCalc_Method

enum_method = get_enumMethod(Method)

Select Case enum_method
        Case Is = enumCalc_Method.Panet
                calc_PfictFactor_PanetGuenot1982
        Case Is = enumCalc_Method.Hoek
                calc_PfictFactor_Hoek
End Select

End Function

' Panet and Guenot A 1982 'Analysis of convergence behind the face of a tunnel'
' Proc Tunnelling 82  Brighton  J 197-204
Public Function calc_PfictFactor_PanetGuenot1982()
Dim a, B As Double

a = 0.72
B = 0.845 * m_R

m_PfictFactor = a * B / (m_x + B)

End Function

Public Function calc_PfictFactor_Hoek()

calc_LamdaD_Hoek1999

m_PfictFactor = 1 - m_LamdaD

End Function
