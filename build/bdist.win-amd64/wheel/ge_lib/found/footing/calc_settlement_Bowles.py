
import math

# ' ==============================================================
# '  Reference :    Special Footings and Beams on Elastic Foundations
# '                   Bowles p501
# ' ==============================================================
# ' Estimation of subgrade reaction based on BOWLES p503
# ' Equations 9-7,  5-16 and 5-16a
# '
# ' ==============================================================
# ' Coded by : AECOM Simon Thomson
# ' ==============================================================
# ' Checked by :
# ' ==============================================================
# ' Version : 0.1
# ' ==============================================================
# ' Date 07 July 2018
# ' ==============================================================
# ' This code is the copyright of AECOM. No part of this
# ' code may be reproduced without the prior permission
# ' ==============================================================

# ' ==============================================================
# '                     Input and Output Variables
# ' ==============================================================


def calc_settlement(data):
     
    '''
    input parameters 
    ----------------
    Modulus of soil : data.Es
    Breadth : data.M
    Depth factor : data.Is
    Influence fcator : data.If
    Poisson Ratio : data.Poisson

    output parameters
    -----------------
    Settlement : data.dH
    
    '''

    data.dH = data.qo * data.B * (1 - data.Poisson ^ 2) / data.Es * data.M * data.Is * data.If
    return data.dH

def calc_ks (data):
    '''
    input parameters 
    ----------------
    Modulus of soil : data.Es
    Breadth : data.M
    Depth factor : data.Is
    Influence fcator : data.If
    Poisson Ratio : data.Poisson

    output parameters
    -----------------
    Subgrade reaction : data.ks
    
    '''

    data.ks = data.Es / (1 - math.pow(data.Poisson,2)) / (data.B * data.M * data.Is * data.If)
    return data.ks

