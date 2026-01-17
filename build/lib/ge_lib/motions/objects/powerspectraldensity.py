import matplotlib.pyplot as plt
from ..methods import CalculatePowerSpectralDensity
from ..plotters.showplotasync import ShowPlotAsync

class _PowerSpectralDensityFrequencyComponent:
    def __init__(self):
        self.Units = None
        self.Values = None

class PowerSpectralDensity:
    def __init__(self,parent=None):
        self.Frequencies = _PowerSpectralDensityFrequencyComponent()
        self.PointsNo = None
        self.Values = None
        self.Parent = parent # Motion()

    def Calculate(self):
        # Prepare input
        accValues = self.Parent.MotionComponents.a.Values
        timeStep = self.Parent.TimeStep
        n = self.Parent.PointsNo
        # Calculate
        if self.Parent.AriasIntensity.Values is None: self.Parent.AriasIntensity.Calculate()
        tSignificant = self.Parent.AriasIntensity.t75-self.Parent.AriasIntensity.t5
        fourierFrequencies,psd = CalculatePowerSpectralDensity(accValues,tSignificant,timeStep,n)
        self.Frequencies.Units = 'Hz'
        self.Frequencies.Values = fourierFrequencies
        self.PointsNo = fourierFrequencies.size
        self.Values = psd

    def LoadFromFile(self):
        pass

    def WriteToFile(self):
        pass

    def Clear(self):
        self.Frequencies.Units = None
        self.Frequencies.Values = None
        self.PointsNo = None
        self.Values = None
    
    def Copy(self):
        newPowerSpectralDensity = PowerSpectralDensity()
        newPowerSpectralDensity.Frequencies.Units = self.Frequencies.Units
        newPowerSpectralDensity.Frequencies.Values = None if self.Frequencies.Values is None else self.Frequencies.Values.copy()
        newPowerSpectralDensity.PointsNo = self.PointsNo
        newPowerSpectralDensity.Values = None if self.Values is None else self.Values.copy()
        newPowerSpectralDensity.Parent = self.Parent
        return newPowerSpectralDensity
    
    def Plot(self,xScale='linear'):
        fig,ax = plt.subplots(nrows=1,ncols=1,constrained_layout=True)
        fig.suptitle(r'$Power\>Spectral\>Density$')
        ax.plot(self.Frequencies.Values,self.Values)
        ax.set_xlabel(rf'$frequencies\>[{self.Frequencies.Units}]$')
        ax.set_ylabel(r'$PSD$')
        ax.set_xscale(xScale)
        ax.grid(True,'both','both')
        ShowPlotAsync(fig)
