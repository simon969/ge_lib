import numpy as np
from decimal import Decimal as dc

# Calculate Fourier transform of a signal and return complete values
def FourierTransform(vals,duration,timeStep):
    signalIntervalsNo = (duration/timeStep).__round__()
    fourierFrequenciesIntervalsNo = (signalIntervalsNo+1)//2
    fourierFrequencies = np.linspace(0,fourierFrequenciesIntervalsNo,fourierFrequenciesIntervalsNo+1)/duration.__float__()
    fourierTransform = np.fft.rfft(vals)*timeStep.__float__()
    return fourierFrequencies,fourierTransform

# Inverse Fourier transform and return complete values
def FourierTransformInverse(fourierTransform,duration,timeStep):
    signalIntervalsNo = (duration/timeStep).__round__()
    signal = np.fft.irfft(fourierTransform,signalIntervalsNo+1)/timeStep.__float__()
    return signal,duration,timeStep

# Use Fourier transform to do resampling
def FourierTransformResample(vals,duration,timeStep,timeStepDivisor):
    signalIntervalsNo = (duration/timeStep).__round__()
    # This has to be an integer, timeStepDivisor should have been selected in such a way, so the rounding just cuts off round off errors
    newSize = (signalIntervalsNo*timeStepDivisor).__round__()+1

    resampledSignal = np.fft.irfft(np.fft.rfft(vals),newSize)*timeStepDivisor.__float__()
    return resampledSignal,duration,timeStep/timeStepDivisor

# Filter out frequencies within given integrals
def FourierTransformFilterOut(vals,duration,timeStep,filterOutFrequencyIntervals):
    signalIntervalsNo = (duration/timeStep).__round__()
    fourierFrequenciesIntervalsNo = (signalIntervalsNo+1)//2
    fourierFrequencies = np.linspace(0,fourierFrequenciesIntervalsNo,fourierFrequenciesIntervalsNo+1)/duration.__float__()
    tmp = np.array(filterOutFrequencyIntervals)
    tmp = np.logical_or(
        (np.tile(fourierFrequencies,(tmp.shape[0],1))<np.tile(tmp[:,0],(fourierFrequencies.size,1)).T)
        ,
        (np.tile(fourierFrequencies,(tmp.shape[0],1))>np.tile(tmp[:,1],(fourierFrequencies.size,1)).T)
        )
    tmp = np.logical_or.reduce(tmp,0)
    newSignal = np.fft.irfft(np.fft.rfft(vals)*tmp,signalIntervalsNo+1)
    return newSignal,duration,timeStep

# Calculate integral of motion assuming the sampling points follow a shape function as determined by the FFT frequency - coefficient pairs
# with zero value as the initial boundary condition at t = 0
# ---------------------
# !!! Does not work !!!
# ---------------------
def FourierTransformIntegral(vals,duration,timeStep):
    fourierFrequencies,fourierTransform = FourierTransform(vals,duration,timeStep)
    # First Fourier frequency is zero, so substitute it with a relatively small number to facilitate division
    fourierFrequencies[0] = fourierFrequencies[1]*1e-50

    fourierTransformIntegral = fourierTransform/(fourierFrequencies*2*np.pi*1j)
    integral,duration,timeStep = FourierTransformInverse(fourierTransformIntegral,duration,timeStep)
    integral -= integral[0]
    return integral,duration,timeStep

# Calculate derivative of motion assuming the sampling points follow a shape function as determined by the FFT frequency - coefficient pairs
def FourierTransformDerivative(vals,duration,timeStep):
    fourierFrequencies,fourierTransform = FourierTransform(vals,duration,timeStep)
    fourierTransformDerivative = 2*np.pi*1j*fourierFrequencies*fourierTransform
    derivative,duration,timeStep = FourierTransformInverse(fourierTransformDerivative,duration,timeStep)
    return derivative,duration,timeStep

def FourierTransformMotionEquationSolution(accValues,duration,timeStep,f,ksi):
    # Fourier transform shall give a partial solution
    fourierFrequencies,fourierTransform = FourierTransform(accValues,duration,timeStep)
    dispValsP,_,_ = FourierTransformInverse(fourierTransform/(f**2+2*ksi*f*1j*fourierFrequencies-fourierFrequencies**2),duration,timeStep)
    dispValsP /= -4*np.pi**2
    velValsP,_,_ = FourierTransformDerivative(dispValsP,duration,timeStep)
    accValsP,_,_ = FourierTransformDerivative(velValsP,duration,timeStep)
    # Set up constants for homogeneous solution
    ksi0 = np.sqrt(1-ksi**2)
    c2 = -dispValsP[0]
    c1 = -dispValsP[0]*ksi/ksi0-velValsP[0]/(2*np.pi*f*ksi0)
    t = np.linspace(0,duration.__float__(),(duration/timeStep).__round__()+1)
    exp_minus_ksi_omega_t = np.exp(-2*np.pi*f*ksi*t)
    sin_ksi0_omega_t = np.sin(2*np.pi*f*ksi0*t)
    cos_ksi0_omega_t = np.cos(2*np.pi*f*ksi0*t)
    c1_sin_plus_c2_cos = c1*sin_ksi0_omega_t+c2*cos_ksi0_omega_t
    c1_cos_minus_c2_sin = c1*cos_ksi0_omega_t-c2*sin_ksi0_omega_t
    # Homogeneous solution
    dispVals0 = exp_minus_ksi_omega_t*c1_sin_plus_c2_cos
    velVals0 = 2*np.pi*f*exp_minus_ksi_omega_t * (ksi0*c1_cos_minus_c2_sin - ksi*c1_sin_plus_c2_cos)
    accVals0 = (2*np.pi*f)**2*exp_minus_ksi_omega_t * ((ksi**2 - ksi0**2)*c1_sin_plus_c2_cos - 2*ksi*ksi0*c1_cos_minus_c2_sin)
    # Final solution
    accVals = accValsP + accVals0
    velVals = velValsP + velVals0
    dispVals = dispValsP + dispVals0

    return accVals,velVals,dispVals,duration,timeStep