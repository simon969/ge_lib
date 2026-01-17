'''
' ==========================================================================================
' Stress within a semi-infinite, homogeneous, anisotropic mass, with a linear stress-strain relationship (1938)
' The pioneering analytical work of Harold Malcom Westergaard (1888-1950) 
' has been at the heart of slab-on-grade pavement design since the 1920s
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



class WestergaardStressField(StressField):

    def __init__(self, data):
        super (self,data)    