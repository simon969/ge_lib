'''
 ==========================================================================================
Stress within a semi-infinite, homogeneous, isotropic mass, with a linear stress-strain relationship
due to a point load on the surface were determined by Boussinesq in 1985
Every code of practice published since then makes reference to the "Westergaard solutions." 
These solutions are only available for three particular loading conditions (interior, edge, and corner) 
and assume a slab of infinite or semi-infinite dimensions. Since their first appearance, beginning in the early 1920s,
Westergaard equations have often been misquoted or misapplied in subsequent
publications. To remedy this situation, a reexamination of these solutions
using the finite element method is described in this paper. 
A number of interesting results are presented: (a) Several equations ascribed to Westergaard in
the literature are erroneous, usually as a result of a series of typographical
errors or misapplications, or both. The correct form of these equations and
their limitations have now been conclusively established. (b) Westergaard' s
original equation for edge stress is incorrect. The long-ignored equation given
in his 1948 paper should be used instead. (c) Improved expressions for maximum
corner loading responses have been developed. (d) Slab size requirements for
the development of Westergaard responses have also been established. 
'
' ==========================================================================================
' Coded   | Simon Thomson
' ==========================================================================================
' Company | AECOM
' ==========================================================================================
' Date    | April 2010
' ==========================================================================================
' Version | 01.00.00
' ==========================================================================================

'''

import math
from ge_lib.found.stress_field.HalfSpace2D import StressField


class BoussinesqStressField(StressField):

    def __init__(self, data):
        super (self,data)
        self.line_sz = line_sz
        self.line_sx = line_sx
        self.line_sxz = line_sxz

def line_sz (data, attr='line_sz'):
    """
    Equations for Line Load Q/m
        ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
        Eq 5.16 line_sz
    
    arguments:
        dictionary object containing:
        q : line load
        x : distance from line load
        z : depth below line load
        attr: return attribute attr='line_sz'

    return:
        returns 
        data[attr]

    """
    p1 = math.pow(math.pow(data.x, 2) + math.pow(data.z, 2), 2)

    data[attr] = 2 * data.q / math.pi * p1 * math.pow(data.z,3)

    return data[attr]

def line_sx (data, attr='line_sx'):
    """
        Equations for Line Load Q/m
        ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
        Eq 5.16 line_sx
    arguments:
        dictionary object containing:
        q : line load
        x : distance from line load
        z : depth below line load
        attr: return attribute attr='line_sx'

    return:
        returns 
        data[attr]

    """

    p1 = math.pow(math.pow(data.x,2) + math.pow(data.z,2),2)
    data[attr] = 2 * data.q / math.pi * p1 * math.pow(data.x,2) * data.z
    return data[attr]

def line_sxz(data, attr='line_sxz'):
    """
        Equations for Line Load Q/m

        ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
        
        Eq 5.16 line_sxz
    arguments:
        data:

        dictionary object containing

        data.q, applied line load 

        data.x, horizontal distance x from line load 
        
        data.z, depth below line load z
        
        return attribute attr

    return:
        data[attr]

    """
    
    p1 = math.pow(math.pow(data.x,2) + math.pow(data.z,2),2)

    data[attr] = 2 * data.q / math.pi * p1 * data.x * math.pow(data.z, 2)
    
    return data[attr]


"""
'====================================================================================================
'  Equations for Point Load Q
' ' ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
'====================================================================================================
Public Function point_sz(q As Double, r As Double, z As Double) As Double
'  Eq 5.10
m_q = q
p1 = (r / z) ^ 2
p2 = (1 / (1 + p1)) ^ (5 / 2)
point_sz = 3 * m_q / (2 * const_PI * z ^ 2) * p2
End Function
Public Function point_sr(q As Double, r As Double, z As Double, Poisson As Double) As Double
' Eq 5.11
m_q = q
m_poisson = Poisson
p1 = r ^ 2 + z ^ 2
p2 = 3 * r ^ 2 * z / (p1 ^ (5 / 2))
p3 = (1 - 2 * m_poisson) / (p1 + z * p1 ^ 0.5)
point_sr = m_q / (2 * const_PI) * (p2 - p3)
End Function
Public Function point_stheta(q As Double, r As Double, z As Double, Poisson As Double) As Double
' Eq 5.12
m_q = q
m_poisson = Poisson
p1 = r ^ 2 + z ^ 2
p2 = z / (p1 ^ (3 / 2))
p3 = 1 / (p1 + z * p1 ^ 0.5)
point_stheta = m_q / (2 * const_PI) * (1 - 2 * m_poisson) * (p2 - p3)
End Function
Public Function point_srz(q As Double, r As Double, z As Double) As Double
' Eq 5.13
m_q = q
p1 = r ^ 2 + z ^ 2
p2 = (r * z ^ 2) / (p1 ^ (5 / 2))
point_srz = 3 * m_q / (2 * const_PI) * p2
End Function

'====================================================================================================
'  Equations for uniform pressure q on a strip of width 2b and infinite length
' ' ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
' q applied pressure
' alpha_rad radians origin at point from vertical to edge of loaded strip
' beta_rad radians origin at point from near loaded edge to far loaded edge'
' Equations 6.69
'====================================================================================================
Public Function strip_sz(q As Double, alpha_rad As Double, beta_rad As Double) As Double
m_q = q
s1 = Sin(beta_rad)
c1 = Cos(2 * alpha_rad + beta_rad)
strip_sz = m_q / const_PI * (beta_rad + s1 * c1)
End Function
Public Function strip_sx(q As Double, alpha_rad As Double, beta_rad As Double) As Double
m_q = q
s1 = Sin(beta_rad)
c1 = Cos(2 * alpha_rad + beta_rad)
strip_sx = m_q / const_PI * (beta_rad - s1 * c1)
End Function
Public Function strip_sxz(q As Double, alpha_rad As Double, beta_rad As Double) As Double
m_q = q
s1 = Sin(beta_rad)
c1 = Cos(beta_rad * (2 * alpha_rad + beta_rad))
strip_sxz = m_q / const_PI * s1 * c1
End Function


'====================================================================================================
'  Equations for linear increaseing pressure from 0 to q/m2 on a strip of width c and infinite length
' ' ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
' Equations 6.70
'====================================================================================================
Public Function linear_strip_sz(q As Double, alpha_rad As Double, beta_rad As Double, x As Double, c As Double) As Double
m_q = q
s1 = Sin(2 * alpha_rad) / 2
linear_strip_sz = m_q / const_PI * (x / c * beta_rad - s1)
End Function
Public Function linear_strip_sx(q As Double, alpha_rad As Double, beta_rad As Double, x As Double, z As Double, c As Double) As Double
m_q = q
s1 = Sin(2 * beta_rad) / 2
p1 = (x ^ 2 - z ^ 2) / (x ^ 2 - c ^ 2 - z ^ 2)
p2 = z / c * Log(p1)
p3 = x / c * beta_rad
linear_strip_sx = m_q / const_PI * (p3 + s1 - p2)
End Function
Public Function linear_strip_sxz(q As Double, alpha_rad As Double, beta_rad As Double, z As Double, c As Double) As Double
m_q = q
c1 = Cos(2 * beta_rad)
p1 = 2 * z / c * alpha_rad
linear_strip_sxz = m_q / const_PI * (1 + c1 - p1)
End Function


'====================================================================================================
'  Equations for stressess below the centre of a circular area of radius R carrying a uniform pressure Q/m2
' ' ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
' Equations 6.71
' Circle_stheta=Circle_sr given by Egquation 5.26 of Craig's Soil Mechanics Seventh Edition Craig (2004)
'====================================================================================================
Public Function circle_sz(q As Double, z As Double, r As Double) As Double
m_q = q
p1 = 1 / (1 + (r / z) ^ 2)
circle_sz = m_q * (1 - p1 ^ 3 / 2)
End Function

Public Function circle_sr(q As Double, z As Double, r As Double, Poisson As Double) As Double
m_q = q
m_poisson = Poisson
p1 = 1 + (r / z) ^ 2
p2 = 2 * (1 + m_poisson) / (p1 ^ 0.5)
p3 = 1 / (p1) ^ (3 / 2)
circle_sr = m_q / 2 * ((1 + 2 * m_poisson) - p2 + p3)
End Function

Public Function circle_stheta(q As Double, z As Double, r As Double, Poisson As Double) As Double
circle_stheta = circle_sr(q, z, r, Poisson)
End Function

'====================================================================================================
'  Equations for stressess beneath the corner of recatngular area of B x L carrying a uniform pressure Q/m2
' ' ref Basic Soil Mechanics Roy Whitlow 4th Edition 2001 Whitlow (2004)
' Equations 6.73
Public Function rectangle_sz(q As Double, z As Double, B As Double, L As Double) As Double
Dim M As Double
Dim N As Double
Dim Ir As Double

m_q = q

If z = 0 Then
    Ir = 0.25
Else
    M = B / z
    N = L / z
    Ir = calc_Ir(M, N)
End If

rectangle_sz = q * Ir

End Function

Public Function calc_Ir(M As Double, N As Double) As Double
Dim M2 As Double
Dim N2 As Double
Dim mn2r As Double
Dim m2n2 As Double
Dim m2n21 As Double
Dim t1 As Double

M2 = M ^ 2
N2 = N ^ 2

mn2r = 2 * M * N * (M2 + N2 + 1) ^ 0.5
m2n2 = M2 + N2 + M2 * N2 + 1
m2n21 = M2 + N2 - M2 * N2 + 1

If m2n21 = 0 Then
t1 = const_PI
End If

If m2n21 < 0 Then
t1 = Atn(mn2r / m2n21) + const_PI
End If

If m2n21 > 0 Then
t1 = Atn(mn2r / m2n21)
End If

calc_Ir = 1 / (4 * const_PI) * ((mn2r / m2n2) * (M2 + N2 + 2) / (M2 + N2 + 1) + t1)

End Function
' https://www.rocscience.com/help/settle3d/webhelp/pdf_files/verification/Settle3D_Stress_Verification.pdf
'====================================================================================================
'  Equations for stressess beneath the corner of recatngular area of B x L carrying a uniform pressure Q/m2
' ' ref FOUNDATION aNALYSIS AND dESIGN jOSEPH bOWLES 1982 Equations 5.8
Public Function rectangle_sz3(q As Double, z As Double, B As Double, L As Double) As Double
Dim M As Double
Dim N As Double
Dim Ir As Double

m_q = q

If z = 0 Then
    Ir = 0.25
Else
    M = B / z
    N = L / z
    Ir = calc_Ir3(M, N)
End If

rectangle_sz3 = q * Ir

End Function
Public Function calc_Ir3(M As Double, N As Double) As Double
'
Dim v As Double
Dim v1 As Double
Dim t1 As Double

v = M ^ 2 + N ^ 2 + 1
v1 = (M * N) ^ 2

If v1 = v Then
t1 = const_PI
End If

If v1 > v Then
t1 = Atn((2 * M * N * v ^ 0.5) / (v - v1)) + const_PI
End If

If v1 < v Then
t1 = Atn((2 * M * N * v ^ 0.5) / (v - v1))
End If

calc_Ir3 = 1 / (4 * const_PI) * ((2 * M * N * v ^ 0.5) / (v + v1) * (v + 1) / v + t1)

End Function
'  Equations for stressess beneath the corner of recatngular area of B x L carrying a uniform pressure Q/m2
'  ref FOUNDATION aNALYSIS AND dESIGN jOSEPH bOWLES 1982 Equations 5.8
Public Function rectangle_sz2(q As Double, z As Double, a As Double, B As Double) As Double

Dim Ir As Double

m_q = q

If z = 0 Then
    Ir = 0.25
Else
    Ir = calc_Ir2(z, a, B)
End If

rectangle_sz2 = q * Ir

End Function

Public Function calc_Ir2(z As Double, a As Double, B As Double) As Double
Dim F As Double
Dim r As Double

r = (a ^ 2 + B ^ 2 + z ^ 2) ^ 0.5
F = 2 * a * B * z * r / (z ^ 2 * r ^ 2 + a ^ 2 * B ^ 2)

calc_Ir2 = 1 / (4 * const_PI) * (F * (1 + z ^ 2 / r ^ 2) + Asn(F))

End Function

Public Function Asn(x As Double) As Double
If (Sqr(1 - x * x) <= 0.000000000001) And _
   (Sqr(1 - x * x) >= -0.000000000001) Then
Asn = const_PI / 2
Else
Asn = Atn(x / Sqr(-x * x + 1))
End If
End Function

 """