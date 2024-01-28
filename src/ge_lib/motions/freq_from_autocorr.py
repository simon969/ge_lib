import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate, fftconvolve
from scipy.interpolate import interp1d
# example of scipy.signal correlate
# https://stackoverflow.com/questions/61534687/how-to-calculate-pitch-fundamental-frequency-f-0-in-time-domain

# exmaple of numpy.fft
#https://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python


def main():

    fs = 44100
    frequency = 440
    length = 0.01 # in secondsd

    t = np.linspace(0, length, int(fs * length)) 
    y = np.sin(frequency * 2 * np.pi * t)

    res1 = freq_from_autocorr (y, fs)

    framerate = 100

    res2 = freq_from_fft  (y, fs)
    
    print (res1, res2)


def parabolic(f, x):
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    corr = correlate(sig, sig, mode='full')
    corr = corr[len(corr)//2:]
    d = np.diff(corr)
    start = np.nonzero(d > 0)[0][0]
    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px



if __name__ == '__main__':
    main()
