import numpy as np
import math
import json

class SectionProperties():
    
    locArea = 0
    locAX = 1
    locAY = 2
    locIX = 3
    locIY = 4
    locIXY = 5
    locXc = 6
    locYc = 7
    locIXC = 8
    locIYC = 9
    locIXYC = 10
    locIU = 11
    locIV = 12
    locTheta = 13


    resSymbol = [None] * 14
    resText = [None] * 14
    resValues = [None] * 14
    resUnits = [None] * 14
    
    resSymbol[locArea] = "Area"
    resSymbol[locAX] = "AX"
    resSymbol[locAY] = "AY"
    resSymbol[locIX] = "IX"
    resSymbol[locIY] = "IY"
    resSymbol[locIXY] = "IXY"
    resSymbol[locXc] = "Xc"
    resSymbol[locYc] = "Yc"
    resSymbol[locIXC] = "IXC"
    resSymbol[locIYC] = "IYC"
    resSymbol[locIXYC] = "IXYC"
    resSymbol[locIU] = "IU"
    resSymbol[locIV] = "IV"
    resSymbol[locTheta] = "Theta"

    resText[locArea] = "Section area"
    resText[locAX] = "First moment of area about the X axis"
    resText[locAY] = "First moment of area about the Y axis"
    resText[locIX] = "Second Moment of Area about the X axis"
    resText[locIY] = "Second Moment of Area about the Y axis"
    resText[locIXY] = "Product of Inertia about origin"
    resText[locXc] = "Centroid X coordinate"
    resText[locYc] = "Centroid Y coordinate"
    resText[locIXC] = "2nd Moment of Area about axis through the centroid parallel to X"
    resText[locIYC] = "2nd Moment of Area about axis through the centroid parallel to Y"
    resText[locIXYC] = "Product of Inertia about centroid"
    resText[locIU] = "2nd moment of area about principal axis 1 through centroid"
    resText[locIV] = "2nd moment of area about principal axis 2 through centroid"
    resText[locTheta] = "Angle of principal axes to X,Y axes"
    

    def _set_unit_prefix (self, s):
        self.resUnits[self.locArea] = s +"2"
        self.resUnits[self.locAX] = s + "3"
        self.resUnits[self.locAY] = s + "3"
        self.resUnits[self.locIX] = s + "4"
        self.resUnits[self.locIY] = s + "4"
        self.resUnits[self.locIXY] = s + "4"
        self.resUnits[self.locXc] = s
        self.resUnits[self.locYc] = s
        self.resUnits[self.locIXC] = s + "4"
        self.resUnits[self.locIYC] = s + "4"
        self.resUnits[self.locIXYC] = s + "4"
        self.resUnits[self.locIU] = s + "4"
        self.resUnits[self.locIV] = s + "4"
        self.resUnits[self.locTheta] = "degrees"

    def calc_props (self, data):
        '''
        input params
        ------------
        data["coords"]

        data["units"]

        if data is "coords" with no "units" units None will be returned
        
        
        return lists
        ------------
        values, symbols, descriptions, units
        '''
        if isinstance(data, dict):
            dic = data
        else:
            if isinstance(data,list):
                dic = {"coords": data
                       }
            else:
                dic = json.loads(data)

        if "coords" in dic:
            coords = dic["coords"]
            if "units" in dic:
                self._set_unit_prefix (dic["units"])
        else:
            #  try assuming that it is a dict or coords
            coords = dic


        num_coords = len(coords)
        crosspA = array_2d (num_coords, 1)
        vect1 = array_2d (num_coords, 2)
        vect2 = array_2d (num_coords, 2)
        
        area = 0.0
        ax = 0.0
        ay = 0.0
        ix = 0.0
        iy = 0.0
        ixy = 0.0
        j = 0

        for i in range(0, num_coords-1):
            j = j + 1
            vect1[i][0] = coords[i][0]
            vect1[i][1] = coords[i][1]
            vect2[i][0] = coords[j][0]
            vect2[i][1] = coords[j][1]
            crosspA[i] = vect1[i][0] * vect2[i][1] - vect1[i][1] * vect2[i][0]

        for i in  range (0, num_coords-1):
            area = area + crosspA[i]
            ax = ax + crosspA[i] * (vect1[i][1] + vect2[i][1])
            ay = ay + crosspA[i] * (vect1[i][0] + vect2[i][0])
            ix = ix + (math.pow(vect1[i][1],2) + math.pow(vect2[i][1],2) + vect1[i][1] * vect2[i][1]) * crosspA[i]
            iy = iy + (math.pow(vect1[i][0], 2) + math.pow(vect2[i][0],2) + vect1[i][0] * vect2[i][0]) * crosspA[i]
            ixy = ixy + (vect1[i][0] * vect2[i][1] + 2 * vect1[i][0] * vect1[i][1] + 2 * vect2[i][0] * vect2[i][1] + vect2[i][0] * vect1[i][1]) * crosspA[i]
        
        area = -area / 2
        ax = -ax / 6
        ay = -ay / 6
        ix = -ix / 12
        iy = -iy / 12
        ixy= -ixy / 24
        xbar = ay / area
        ybar = ax / area
        ixc = ix - area * math.pow(ybar, 2)
        iyc = iy - area * math.pow(xbar, 2)
        ixyc = ixy - area * xbar * ybar
        a = math.pow((ixc - iyc) * (ixc - iyc) / 4 + math.pow(ixyc, 2), 0.5)
        iu = (ixc + iyc) / 2 + a
        iv = (ixc + iyc) / 2 - a
        
        if abs(ixyc) > 0.000001:
            theta = 0.5 * (atn2((ixc - iyc), 2 * ixyc))
        else:
            theta = 0

        theta = theta * 180 / math.pi
            
        self.resValues[self.locArea] = area
        self.resValues[self.locAX] = ax
        self.resValues[self.locAY] = ay
        self.resValues[self.locIX] = ix
        self.resValues[self.locIY] = iy
        self.resValues[self.locIXY] = ixy
        self.resValues[self.locXc] = xbar
        self.resValues[self.locYc] = ybar
        self.resValues[self.locIXC] = ixc
        self.resValues[self.locIYC] = iyc
        self.resValues[self.locIXYC] = ixyc
        self.resValues[self.locIU] = iu
        self.resValues[self.locIV] = iv
        self.resValues[self.locTheta] = theta

        return self.resValues, self.resSymbol, self.resText, self.resUnits
    
def array_2d(rows, columns):
    twod_list = []                                                             
    for i in range (0, rows):                               
        new = []                         
        for j in range (0, columns):              
            new.append(0)               
        twod_list.append(new)
    return twod_list

def atn2(x, y):

    # Inverse tangent based on X and Y coordinates
    # X and Y both zero produces an error.

    if (x == 0):
        if (y == 0):
            return 1 / 0
        else:
            if (y > 0):
                return math.pi / 2
            else:
                return -math.pi / 2
    else:
        if (x > 0):
            if (y == 0):
                return 0
            else:
                return math.atan(y / x)
        else:
            if (y == 0):
                return math.pi
            else:
                return (math.pi - math.atan(math.abs(y) / abs(x))) * math.sgn(y)



# Original VBA code

# Private ResA() As Double
# Private ResText() As String
# Private Vect1() As Double
# Private Vect2() As Double
# Private CrosspA() As Double

# Private Num1 As Long
# Private Area As Double
# Private AX As Double
# Private AY As Double
# Private IX As Double
# Private IY As Double
# Private IXY As Double
# Private IXC As Double
# Private IYC As Double
# Private IXYC As Double
# Private Xbar As Double
# Private Ybar As Double
# Private IU As Double
# Private IV As Double
# Private Theta As Double

# Private Const constPI As Double = 3.14159265358979
# Const pos_Area = 1
# Const pos_AX = 2
# Const pos_AY = 3
# Const pos_IX = 4
# Const pos_IY = 5
# Const pos_IXY = 6
# Const pos_Xc = 7
# Const pos_Yc = 8
# Const pos_IXC = 9
# Const pos_IYC = 10
# Const pos_IXYC = 11
# Const pos_IU = 12
# Const pos_IV = 13
# Const pos_Theta = 14


# Public Function SecProp(Coords As Variant, Optional NumOut As Long) As Variant
#    Dim I As Long, j As Long, a As Double
   
#     If NumOut = 0 Then NumOut = 14
    
#     If NumOut < 0 Then
#         ReDim ResText(1 To 14, 1 To 1)
#     Else
#         ReDim ResA(1 To NumOut, 1 To 1)
#     End If

#     If NumOut = -1 Then
#         ResText(pos_Area, 1) = "Area"
#         ResText(pos_AX, 1) = "AX"
#         ResText(pos_AY, 1) = "AY"
#         ResText(pos_IX, 1) = "IX"
#         ResText(pos_IY, 1) = "IY"
#         ResText(pos_IXY, 1) = "IXY"
#         ResText(pos_Xc, 1) = "Xc"
#         ResText(pos_Yc, 1) = "Yc"
#         ResText(pos_IXC, 1) = "IXC"
#         ResText(pos_IYC, 1) = "IYC"
#         ResText(pos_IXYC, 1) = "IXYC"
#         ResText(pos_IU, 1) = "IU"
#         ResText(pos_IV, 1) = "IV"
#         ResText(pos_Theta, 1) = "Theta"
#         SecProp = ResText
#         Exit Function
#     End If
    
#     If NumOut = -2 Then
#         ResText(pos_Area, 1) = "  Section area"
#         ResText(pos_AX, 1) = "  First moment of area about the X axis"
#         ResText(pos_AY, 1) = "  First moment of area about the Y axis"
#         ResText(pos_IX, 1) = "  Second Moment of Area about the X axis"
#         ResText(pos_IY, 1) = "  Second Moment of Area about the Y axis"
#         ResText(pos_IXY, 1) = "  Product of Inertia about origin"
#         ResText(pos_Xc, 1) = "  Centroid X coordinate"
#         ResText(pos_Yc, 1) = "  Centroid Y coordinate"
#         ResText(pos_IXC, 1) = "  2nd Moment of Area about axis through the centroid parallel to X"
#         ResText(pos_IYC, 1) = "  2nd Moment of Area about axis through the centroid parallel to Y"
#         ResText(pos_IXYC, 1) = "  Product of Inertia about centroid"
#         ResText(pos_IU, 1) = "  2nd moment of area about principal axis 1 through centroid"
#         ResText(pos_IV, 1) = "  2nd moment of area about principal axis 2 through centroid"
#         ResText(pos_Theta, 1) = "  Angle of principal axes to X,Y axes (degrees)"
#         SecProp = ResText
#         Exit Function
#     End If


#     If TypeName(Coords) = "Range" Then Coords = Coords.Value2

#     Num1 = UBound(Coords)
#     ReDim CrosspA(1 To Num1 - 1)
#     ReDim Vect1(1 To Num1 - 1, 1 To 2)
#     ReDim Vect2(1 To Num1 - 1, 1 To 2)
    
#     For I = 1 To Num1 - 1
#         j = I + 1
#         Vect1(I, 1) = Coords(I, 1)
#         Vect1(I, 2) = Coords(I, 2)
#         Vect2(I, 1) = Coords(j, 1)
#         Vect2(I, 2) = Coords(j, 2)
#         CrosspA(I) = Vect1(I, 1) * Vect2(I, 2) - Vect1(I, 2) * Vect2(I, 1)
#     Next I

#     For I = 1 To Num1 - 1
#         Area = Area + CrosspA(I)
#         AX = AX + CrosspA(I) * (Vect1(I, 2) + Vect2(I, 2))
#         AY = AY + CrosspA(I) * (Vect1(I, 1) + Vect2(I, 1))
#         IX = IX + (Vect1(I, 2) ^ 2 + Vect2(I, 2) ^ 2 + Vect1(I, 2) * Vect2(I, 2)) * CrosspA(I)
#         IY = IY + (Vect1(I, 1) ^ 2 + Vect2(I, 1) ^ 2 + Vect1(I, 1) * Vect2(I, 1)) * CrosspA(I)
#         IXY = IXY + (Vect1(I, 1) * Vect2(I, 2) + 2 * Vect1(I, 1) * Vect1(I, 2) + 2 * Vect2(I, 1) * Vect2(I, 2) + Vect2(I, 1) * Vect1(I, 2)) * CrosspA(I)
#     Next I
    
#     Area = -Area / 2
#     AX = -AX / 6
#     AY = -AY / 6
#     IX = -IX / 12
#     IY = -IY / 12
#     IXY = -IXY / 24
#     Xbar = AY / Area
#     Ybar = AX / Area
#     IXC = IX - Area * Ybar ^ 2
#     IYC = IY - Area * Xbar ^ 2
#     IXYC = IXY - Area * Xbar * Ybar
#     a = ((IXC - IYC) * (IXC - IYC) / 4 + IXYC ^ 2) ^ 0.5
#     IU = (IXC + IYC) / 2 + a
#     IV = (IXC + IYC) / 2 - a
    
#     If Abs(IXYC) > 0.000001 Then
#         Theta = 0.5 * (ATn2((IXC - IYC), 2 * IXYC))
#     Else
#         Theta = 0
#     End If
#     Theta = Theta * 180 / constPI
        
#     ResA(pos_Area, 1) = Area
#     ResA(pos_AX, 1) = AX
#     ResA(pos_AY, 1) = AY
#     ResA(pos_IX, 1) = IX
#     ResA(pos_IY, 1) = IY
#     ResA(pos_IXY, 1) = IXY
#     ResA(pos_Xc, 1) = Xbar
#     ResA(pos_Yc, 1) = Ybar
#     ResA(pos_IXC, 1) = IXC
#     ResA(pos_IYC, 1) = IYC
#     ResA(pos_IXYC, 1) = IXYC
#     ResA(pos_IU, 1) = IU
#     ResA(pos_IV, 1) = IV
#     ResA(pos_Theta, 1) = Theta
        
#     SecProp = ResA
    
# End Function


# def ATn2(x As Variant, y As Variant):

#     ' Inverse tangent based on X and Y coordinates

#     ' X and Y both zero produces an error.

#         If x = 0 Then
#             If y = 0 Then
#                 ATn2 = 1 / 0
#             ElseIf y > 0 Then
#                 ATn2 = constPI / 2
#             Else
#                 ATn2 = -constPI / 2
#             End If
#         ElseIf x > 0 Then
#             If y = 0 Then
#                 ATn2 = 0
#             Else
#                 ATn2 = Atn(y / x)
#             End If
#         Else
#             If y = 0 Then
#                 ATn2 = constPI
#             Else
#                 ATn2 = (constPI - Atn(Abs(y) / Abs(x))) * Sgn(y)
#             End If
#         End If

