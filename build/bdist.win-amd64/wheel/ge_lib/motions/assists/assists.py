import os
from math import gcd,prod
from fractions import Fraction as fc
from ..objects.motion import Motion

# Factors a number to primes
def PrimeFactors(n):
    pF = []
    c = 2
    while n > 1:
        if n % c == 0:
            n /= c
            pF.append(c)
        else:
            c += 1
    return pF

# Gets a numerator and denominator in decimal format and deermines whether their true division
# return number with finite decimal digits.
# Source: https://www.onemathematicalcat.org/algebra_book/online_problems/finite_or_inf_rep.htm#:~:text=Start%20by%20putting%20the%20fraction,has%20a%20finite%20decimal%20name.
def HasFiniteDecimalDigits(numerator,denominator):
    exp = min(denominator.as_tuple().exponent,numerator.as_tuple().exponent)
    if exp < 0:
        n = denominator*10**(-exp).__int__()//gcd((numerator*10**(-exp)).__int__(),(denominator*10**(-exp)).__int__())
    else:
        n = denominator.__int__()//gcd(numerator.__int__(),denominator.__int__())
    pFu = set()
    c = 2
    while n > 1:
        if n % c == 0:
            n //= c
            pFu.add(c)
        else:
            c += 1
    return pFu.__contains__(2) + pFu.__contains__(5) == pFu.__len__()

# Gets a number of intervals and return how PLAXIS would accept them as substeps and steps. substeps * steps >= given intervals
def PLAXISSubstepsStepsSimple(n):
    PLAXIS_max_Steps_Substeps = 10000
    substepsNo = n//PLAXIS_max_Steps_Substeps+1
    stepsNo = n//substepsNo +(n%substepsNo != 0)
    return substepsNo,stepsNo

def ResampleHelp():
    fldIn = r'C:\Users\EmmanouilZ\AECOM\Project 6 Seismic Team - Documents\General\400 Technical\430 Geotech\02. PLAXIS model input motions\03. DEEPSOIL model\Deconvolved Time Histories\DEEPSOIL_text'
    fldOut = r'C:\Users\EmmanouilZ\AECOM\Project 6 Seismic Team - Documents\General\400 Technical\430 Geotech\02. PLAXIS model input motions\05. PLAXIS model\01. resampled input motions'
    filDetails = r'C:\Users\EmmanouilZ\AECOM\Project 6 Seismic Team - Documents\General\400 Technical\430 Geotech\02. PLAXIS model input motions\05. PLAXIS model\resampled motion details.txt'
    targetTimeStep = fc('0.00085')
    mot = Motion()
    with open(filDetails,'w') as detFil:
        for fil in os.listdir(fldIn):
            mot.LoadFromFile(fldIn + '\\' + fil,'DEEPSOIL')
            newPointsNo = ((mot.PointsNo-1)*mot.TimeStep/targetTimeStep).__ceil__()+1
            substepsNo,stepsNo = PLAXISSubstepsStepsSimple(newPointsNo-1)
            newPointsNo = substepsNo*stepsNo+1
            newTimeStep = (mot.PointsNo-1)*mot.TimeStep/(newPointsNo-1)
            divisor = mot.TimeStep/newTimeStep
            motR = mot.Copy()
            motR.Resample(divisor)
            motR.WriteToFile(fldOut + '\\' + fil,'DEEPSOIL')
            detFil.write(f'{fil}\n\tN = {mot.PointsNo}\n\tts = {mot.TimeStep.__float__()}\n\tNr = {motR.PointsNo}\n\ttsr = {motR.TimeStep.__float__()}\n\tPLAXIS substeps = {substepsNo}\n\tPLAXIS steps = {stepsNo}\n')
            print(f'{fil}\n\tN = {mot.PointsNo}\n\tts = {mot.TimeStep.__float__()}\n\tNr = {motR.PointsNo}\n\ttsr = {motR.TimeStep.__float__()}\n\tPLAXIS substeps = {substepsNo}\n\tPLAXIS steps = {stepsNo}')
            mot.Clear()