import numpy as np
from multiprocessing import Pool as mp_Pool, cpu_count as mp_cpu_count
from itertools import repeat as iter_repeat
from .fourier import FourierTransformMotionEquationSolution,FourierTransform

# Calculate Arias Intensity
def CalculateAriasIntensity(accValues,timeStep,n):
    g1 = accValues[0:-1]
    g2 = accValues[1:]
    ariasIntensity = np.pi/2/3*timeStep*np.cumsum(g1**2+g1*g2+g2**2)
    ariasIntensity = np.append(0,ariasIntensity)
    diff = np.clip(ariasIntensity-0.05*ariasIntensity[-1],None,0) 
    i = np.argmax(diff)-1
    t5 = i*timeStep+timeStep/2
    diff = np.clip(ariasIntensity-0.75*ariasIntensity[-1],None,0)
    i = np.argmax(diff)-1
    t75 = i*timeStep+timeStep/2
    diff = np.clip(ariasIntensity-0.95*ariasIntensity[-1],None,0)
    i = np.argmax(diff)-1
    t95 = i*timeStep+timeStep/2
    return ariasIntensity[-1],t5,t75,t95,n,timeStep,ariasIntensity

# Calculate power spectral density
def CalculatePowerSpectralDensity(accValues,tSignificant,timeStep,n):
    fourierFrequencies,fourierTransform = FourierTransform(accValues,timeStep*(n-1),timeStep)
    psd = np.abs(fourierTransform)**2/(np.pi*tSignificant)
    return fourierFrequencies,psd

# Scale given response spectrum to match given target spectrum by minimising the square of the vertical distance
# between their given ordinates. The first response spectrum is scaled to match the second, swapping first with
# second changes the result.
def ResponseSpectrumScalingFactorToMatchTargetSpectrum_OrdinateValues(parentFrequencies,parentOrdinates,targetFrequencies,targetOrdinates):
    freqs = np.unique(np.append(parentFrequencies,targetFrequencies))
    parOrds = np.interp(freqs,parentFrequencies,parentOrdinates)
    tarOrds = np.interp(freqs,targetFrequencies,targetOrdinates)
    scalingFactor = np.sum(parOrds*tarOrds)/np.sum(parOrds**2)
    return scalingFactor

# Scale given response spectrum to match given target spectrum by minimising the square of the area between the
# two. The first response spectrum is scaled to match the second, swapping first with second changes the result.
def ResponseSpectrumScalingFactorToMatchTargetSpectrum_Integrals(parentFrequencies,parentOrdinates,targetFrequencies,targetOrdinates):
    freqs = np.unique(np.append(parentFrequencies,targetFrequencies))
    parOrds = np.interp(freqs,parentFrequencies,parentOrdinates)
    tarOrds = np.interp(freqs,targetFrequencies,targetOrdinates)
    x1 = freqs[0:-1]
    x2 = freqs[1:]
    g1 = parOrds[0:-1]
    g2 = parOrds[1:]
    f1 = tarOrds[0:-1]
    f2 = tarOrds[1:]
    toScaleIntegralSquared = np.sum((x2-x1)*(g1**2+g1*g2+g2**2))/3
    integralProduct = np.sum((x2-x1)*(f1*g1+f2*g2))/2
    scalingFactor = integralProduct/toScaleIntegralSquared
    return scalingFactor

# Calculate statistical figures for a given motion component
def CalculateMotionComponentStatistics(values,n):
    peak = np.max(np.abs(values))
    mean = np.sum(values)/n
    standardDeviation = np.sqrt(np.sum((values-mean)**2)/n)
    return peak,mean,standardDeviation

# Integrate motion component to get e.g. velocities from accelerations
def MotionComponentIntegrateSimpson(vals,timeStep):
    vals1 = vals[0:-1]
    vals2 = vals[1:]
    return np.append([0],timeStep/2*np.cumsum(vals1+vals2))

# Differentiate motion component to get e.g. accelerations from velocities
def MotionComponentDifferentiateSimpson(vals,timeStep):
    vals1 = vals[0:-1]
    vals2 = vals[1:]
    res = np.zeros(vals.size)
    for i in range(1,vals.size):
        res[i] = 2*(vals[i]-vals[i-1])/timeStep-res[i-1]
    return res

# Calculate correlation factor
def MotionComponentCorrelationFactor(thisValues,thisMean,thisStandardDeviation,thatValues,thatMean,thatStandardDeviation,n):
    corrCoeff = np.sum((thisValues-thisMean)*(thatValues-thatMean))/(n*thisStandardDeviation*thatStandardDeviation)
    return corrCoeff

# Use the Fourier method to calculate the relative response of the single degree of freedom oscilator for single frequency
def MotionComponentAccelerationCalculateResponseSpectraOrdinates(accValues,duration,timeStep,frequency,ksi,velValues,dispValues,accType,velType,dispType):
    accVals,velVals,dispVals,_,_ = FourierTransformMotionEquationSolution(accValues,duration,timeStep,frequency,ksi)
    if accType == 'absolute':
        accVals += accValues
    if velType == 'absolute':
        velVals += velValues
    if dispType == 'absolute':
        dispVals += dispValues
    accVals = np.abs(accVals)
    velVals = np.abs(velVals)
    dispVals = np.abs(dispVals)

    return np.array([accVals.max(),accVals.argmax()*timeStep,velVals.max(),accVals.argmax()*timeStep,dispVals.max(),dispVals.argmax()*timeStep])
    
# Use the Fourier method to calculate the relative response of the single degree of freedom oscilator for multiple frequencies
def MotionComponentAccelerationCalculateResponseSpectra(accValues,duration,timeStep,frequencies,ksi,velValues,dispValues,accType,velType,dispType,nCores):
    if nCores == 0:
        accVals,accTimes,velVals,velTimes,dispVals,dispTimes = [],[],[],[],[],[]
        for frequency in frequencies:
            accVal,accTime,velVal,velTime,dispVal,dispTime = MotionComponentAccelerationCalculateResponseSpectraOrdinates(accValues,duration,timeStep,frequency,ksi,velValues,dispValues,accType,velType,dispType)
            accVals.append(accVal)
            accTimes.append(accTime)
            velVals.append(velVal)
            velTimes.append(velTime)
            dispVals.append(dispVal)
            dispTimes.append(dispTime)
        accVals,accTimes,velVals,velTimes,dispVals,dispTimes = np.array(accVals),np.array(accTimes),np.array(velVals),np.array(velTimes),np.array(dispVals),np.array(dispTimes)
    else:
        if nCores is None:
            nCores = mp_cpu_count()
        n = len(frequencies)
        with mp_Pool(nCores) as pool:
            res = pool.starmap(
                MotionComponentAccelerationCalculateResponseSpectraOrdinates,
                zip(iter_repeat(accValues,n),
                iter_repeat(duration,n),
                iter_repeat(timeStep,n),
                frequencies,
                iter_repeat(ksi,n),
                iter_repeat(velValues,n),
                iter_repeat(dispValues,n),
                iter_repeat(accType,n),
                iter_repeat(velType,n),
                iter_repeat(dispType,n))
            )
        res = np.array(res).T
        accVals,accTimes,velVals,velTimes,dispVals,dispTimes = np.array(res[0],dtype=np.float64),res[1],np.array(res[2],dtype=np.float64),res[3],np.array(res[4],dtype=np.float64),res[5]
    return accVals,accTimes,velVals,velTimes,dispVals,dispTimes

def MotionSuiteOptimiseFactorsToMatchSpectrum(motFreqs:np.ndarray,motOrds:'list[np.ndarray]',freqs:np.ndarray,ords:np.ndarray) -> np.ndarray:
    n = len(motOrds)
    # Interpolate frequencies, so that everything uses the same frequency vector
    newFreqs = np.unique(np.append(motFreqs,freqs))
    newOrds = np.interp(newFreqs,freqs,ords)
    for i in range(0,n):
        motOrds[i] = np.interp(newFreqs,motFreqs,motOrds[i])
    freqs = newFreqs
    ords = newOrds
    newFreqs = None
    newOrds = None
    # Prepare square matrix A and vector B
    A = np.zeros((n,n))
    for i in range(0,n):
        for j in range(i,n):
            A[i,j] = np.sum(motOrds[i]*motOrds[j])
        for j in range(0,i):
            A[i,j] = A[j,i]
    B = np.zeros(n)
    for i in range(0,n):
        B[i] = np.sum(motOrds[i]*ords)
    # Solve for vector X
    if np.linalg.det(A) == 0:
        raise Exception('seismicmotions.methods.MotionSuiteOptimiseFactorsToMatchSpectrum: Matrix "A" is singular.')
    return np.linalg.solve(A,B)

def MotionTripletSuiteOptimiseFactorsToMatchSpectrum(motFreqs:np.ndarray,motOrdsX:'list[np.ndarray]',motOrdsY:'list[np.ndarray]',motOrdsZ:'list[np.ndarray]',
                                                     freqsX:np.ndarray,ordsX:np.ndarray,
                                                     freqsY:np.ndarray,ordsY:np.ndarray,
                                                     freqsZ:np.ndarray,ordsZ:np.ndarray) -> np.ndarray:
    n = len(motOrdsX)
    if n != len(motOrdsY) or n!= len(motOrdsZ):
        raise Exception('seismicmotions.methods.MotionTripletSuiteOptimiseFactorsToMatchSpectrum: "motOrdsX", "motOrdsY" and "motOrdsZ" do not have the same size.')
    # Interpolate frequencies, so that everything uses the same frequency vector
    newFreqs = np.unique(np.concatenate([motFreqs,freqsX,freqsY,freqsZ]))
    newOrdsX = np.interp(newFreqs,freqsX,ordsX)
    newOrdsY = np.interp(newFreqs,freqsY,ordsY)
    newOrdsZ = np.interp(newFreqs,freqsZ,ordsZ)
    for i in range(0,n):
        motOrdsX[i] = np.interp(newFreqs,motFreqs,motOrdsX[i])
        motOrdsY[i] = np.interp(newFreqs,motFreqs,motOrdsY[i])
        motOrdsZ[i] = np.interp(newFreqs,motFreqs,motOrdsZ[i])
    freqs = newFreqs
    ordsX,ordsY,ordsZ = newOrdsX,newOrdsY,newOrdsZ
    newFreqs = None
    newOrds = None
    # Prepare square matrix A and vector B
    A = np.zeros((n,n))
    for i in range(0,n):
        for j in range(i,n):
            A[i,j] = np.sum(motOrdsX[i]*motOrdsX[j])+np.sum(motOrdsY[i]*motOrdsY[j])+np.sum(motOrdsZ[i]*motOrdsZ[j])
        for j in range(0,i):
            A[i,j] = A[j,i]
    B = np.zeros(n)
    for i in range(0,n):
        B[i] = np.sum(motOrdsX[i]*ordsX)+np.sum(motOrdsY[i]*ordsY)+np.sum(motOrdsZ[i]*ordsZ)
    # Solve for vector X
    if np.linalg.det(A) == 0:
        raise Exception('seismicmotions.methods.MotionSuiteOptimiseFactorsToMatchSpectrum: Matrix "A" is singular.')
    return np.linalg.solve(A,B)