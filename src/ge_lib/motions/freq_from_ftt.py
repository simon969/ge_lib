import numpy as np
from Motions import Motion
from .PEERNGARecords import PEERFormatFile

# https://dev.to/rstrange/visualising-volcanoseismic-events-an-exercise-in-signal-processing-5gal

def main():

    fs = 44100
    frequency = 440
    length = 0.01 # in seconds

    t = np.linspace(0, length, int(fs * length)) 
    y = np.sin(frequency * 2 * np.pi * t)

    res1 = freq_from_fft (y, fs)

    framerate = 100

    res2 = freq_from_fft  (y, fs)
    
    print (res1, res2)



def freq_from_fft(sig, fs):
    """
    Estimate frequency using furier transform
    """
    # sample_spacing
    d = 1
    # length of signal
    n = len(sig)

    w = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(n)

    print(freqs.min(), freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    return freq
    
def visualising_volcanoseismic_events():

    #read in the raw data
    input_df = pd.read_csv("../Data/Specimen_Event.csv", index_col="Seconds")

    #The output from the raw data isn't too useful, so let's look at the constituent frequencies

    fft_df = input_df.copy()

    y_values = np.fft.fft(input_df.Amplitude.values)

    no_of_datapoints = len(y_values)
    time_interval = 0.01 

    yf_values = 2.0/no_of_datapoints * np.abs(y_values[:no_of_datapoints//2])

    x_values = fftfreq(no_of_datapoints, d=time_interval)
    xf_values = fftfreq(no_of_datapoints, d=time_interval)[:no_of_datapoints//2]

    #The frequency data is useful, but we've lost all temporal information - let's just take time slices and transform those, and glue it back together like a histogram - aka a seismogram

    window_size = 256

    recording_rate = 100

    frequencies, times, amplitudes = signal.spectrogram(input_df.Amplitude.values, fs = recording_rate, window='hanning', nperseg = window_size, noverlap= window_size - 100, detrend= False, scaling="spectrum")

    decibels = 20 * np.log10(amplitudes)

    f, ax = plt.subplots()
    ax.pcolormesh(times, frequencies, decibels, cmap="viridis")

def earthquake_events():

     mr = PEERFormatFile()
     
     sg = mr.ReadFromFile ()

if __name__ == '__main__':
    main()
