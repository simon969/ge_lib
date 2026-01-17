import matplotlib.pyplot as plt
import numpy as np
from ..fourier import FourierTransform,FourierTransformInverse
from ..plotters.showplotasync import ShowPlotAsync

class FourierSpectrum:
    def __init__(self,parent=None):
        self.Frequencies = None
        self.PointsNo = None
        self.Values = None
        self.Parent = parent # _MotionComponent()

    def Calculate(self):
        vals = self.Parent.Values
        duration = (self.Parent.Parent.Parent.PointsNo-1)*self.Parent.Parent.Parent.TimeStep
        timeStep = self.Parent.Parent.Parent.TimeStep
        self.Frequencies,self.Values = FourierTransform(vals,duration,timeStep)
        self.PointsNo = self.Frequencies.size

    def BackCalculate(self,duration=None,timeStep=None,calculateAllMotionComponents=True):
        state = (duration is None) + 2*(timeStep is None)
        if state == 0:
            # Both are given
            self.Parent.Parent.Parent.TimeStep = timeStep
            self.Parent.Parent.Parent.PointsNo = (duration/timeStep).__round__()+1
        elif state == 1:
            # Only duration is None
            self.Parent.Parent.Parent.TimeStep = timeStep
            duration = timeStep*(self.Parent.Parent.Parent.PointsNo-1)
        elif state == 2:
            # Only timestep is None
            timeStep = self.Parent.Parent.Parent.TimeStep
            self.Parent.Parent.Parent.PointsNo = (duration/timeStep).__round__()+1
        elif state == 3:
            # Both are None
            duration = self.Parent.Parent.Parent.TimeStep*(self.Parent.Parent.Parent.PointsNo-1)
            timeStep = self.Parent.Parent.Parent.TimeStep
        # Clear motioncomponents but keep motion top level data and data of this fourier spectrum while it is not known which motioncomponent this is in.
        u,f,p,v = self.Parent.Units,self.Frequencies,self.PointsNo,self.Values
        self.Parent.Parent.a.Clear()
        self.Parent.Parent.v.Clear()
        self.Parent.Parent.d.Clear()
        self.Parent.Units,self.Frequencies,self.PointsNo,self.Values = u,f,p,v
        self.Parent.Values,_,_ = FourierTransformInverse(self.Values,duration,timeStep)
        if calculateAllMotionComponents:
            self.Parent.Parent.Parent.CalculateMotionComponents()

    def LoadFromFile(self):
        pass

    def WriteToFile(self):
        pass

    def Clear(self):
        self.Frequencies = None
        self.PointsNo = None
        self.Values = None
    
    def Copy(self):
        newFourierSpectrum = FourierSpectrum()
        newFourierSpectrum.Frequencies = None if self.Frequencies is None else self.Frequencies.copy()
        newFourierSpectrum.PointsNo = self.PointsNo
        newFourierSpectrum.Values = None if self.Values is None else self.Values
        newFourierSpectrum.Parent = self.Parent # _MotionComponent()
        return newFourierSpectrum

    def Plot(self,title=None,showAsync=False):
        fig,ax = plt.subplots(nrows=1,ncols=1,constrained_layout=True)
        if title is None:
            fig.suptitle(r'$Fourier spectrum\>$')
        else:
            fig.suptitle(f'{title}')
        ax.plot(self.Frequencies,np.abs(self.Values))
        ax.set_xlabel(r'$f\>[Hz]$')
        ax.set_ylabel(rf'$Fourier\>Amplitudes\>[{self.Parent.Units}]$')
        ax.grid(True,'both','both')
        if showAsync:
            ShowPlotAsync(fig)