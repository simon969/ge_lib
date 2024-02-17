import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal as dc
from ..plotters.showplotasync import ShowPlotAsync
from ..fileloaders.dat import FileLoader_DAT
from ..fileloaders.deepsoil import FileLoader_DEEPSOIL
from ..filewriters.deepsoil import FileWriter_DEEPSOIL
from ..fourier import FourierTransformResample,FourierTransformDerivative,FourierTransformIntegral,FourierTransformFilterOut
from ..objects.responsespectrum import ResponseSpectrum
from ..objects.ariasintensity import AriasIntensity
from ..objects.powerspectraldensity import PowerSpectralDensity
from ..objects.fourierspectrum import FourierSpectrum
from ..methods import MotionComponentCorrelationFactor,CalculateMotionComponentStatistics,MotionComponentIntegrateSimpson,MotionComponentDifferentiateSimpson

class _Statistics:
    def __init__(self,parent):
        self.Peak = None
        self.Mean = None
        self.StandardDeviation = None
        self.Parent = parent # _MotionComponent()

    def Calculate(self):
        # Prepare inputs
        values = self.Parent.Values
        n = self.Parent.Parent.Parent.PointsNo
        # Calculate
        self.Peak,self.Mean,self.StandardDeviation = CalculateMotionComponentStatistics(values,n)

    def Clear(self):
        self.Peak = None
        self.Mean = None
        self.StandardDeviation = None

class _MotionComponent:
    def __init__(self,parent=None):
        self.Units = None
        self.Values = None
        self.Statistics = _Statistics(self)
        self.FourierSpectrum = FourierSpectrum(self)
        self.Parent = parent # _MotionComponents()

    def CorrelationCoefficientWith(self,target):
        # Check arguments
        if self.Parent.Parent.TimeStep != target.Parent.Parent.TimeStep or self.Parent.Parent.PointsNo != target.Parent.Parent.PointsNo:
            raise Exception('seismicmotions.objects._MotionComponent.CorrelationCoefficientWith: Timesteps and durations need to be the same for both motions, consider resampling and zero packing.')
        # Calculate
        self.Statistics.Calculate()
        target.Statistics.Calculate()
        corrCoeff = MotionComponentCorrelationFactor(self.Values,self.Statistics.Mean,self.Statistics.StandardDeviation,target.Values,target.Statistics.Mean,target.Statistics.StandardDeviation,self.Parent.Parent.PointsNo)
        return corrCoeff

    def IntegrateToMotionComponent(self,method='Simpson'):
        # Prepare input
        vals = self.Values
        duration = self.Parent.Parent.TimeStep*(self.Parent.Parent.PointsNo-1)
        timeStep = self.Parent.Parent.TimeStep
        # Calculate
        if method == 'Fourier':
            integral,_,_ = FourierTransformIntegral(vals,duration,timeStep) #Fourier ingration / differentiation does not give the correct result
        elif method == 'Simpson':
            integral = MotionComponentIntegrateSimpson(vals,timeStep)
        newMotionComponent = _MotionComponent()
        newMotionComponent.Units = self.Units + r'\cdot s'
        newMotionComponent.Values = integral
        return newMotionComponent

    def DeriveToMotionComponent(self,method='Simpson'):
        # Prepare input
        vals = self.Values
        duration = self.Parent.Parent.TimeStep*(self.Parent.Parent.PointsNo-1)
        timeStep = self.Parent.Parent.TimeStep
        # Calculate
        if method == 'Fourier':
            derivative,_,_ = FourierTransformDerivative(vals,duration,timeStep)
        elif method == 'Simpson':
            derivative = MotionComponentDifferentiateSimpson(vals,timeStep)
        newMotionComponent = _MotionComponent()
        newMotionComponent.Units = self.Units + r'/s'
        newMotionComponent.Values = derivative
        return newMotionComponent

    def LoadFromFile(self):
        pass

    def WriteToFile(self):
        pass

    def Clear(self):
        self.Units = None
        self.Values = None
        self.Statistics.Clear()
        self.FourierSpectrum.Clear()

    def Copy(self):
        newMotionComponent = _MotionComponent()
        newMotionComponent.Units = self.Units
        newMotionComponent.Values = None if self.Values is None else self.Values.copy()
        newMotionComponent.Statistics.Peak = self.Statistics.Peak
        newMotionComponent.Statistics.Mean = self.Statistics.Mean
        newMotionComponent.Statistics.StandardDeviation = self.Statistics.StandardDeviation
        newMotionComponent.Statistics.Parent = newMotionComponent
        newMotionComponent.FourierSpectrum = self.FourierSpectrum.Copy()
        newMotionComponent.FourierSpectrum.Parent = newMotionComponent
        newMotionComponent.Parent = self.Parent # _MotionComponents()
        return newMotionComponent

    def Plot(self,showAsync=False):
        fig,ax = plt.subplots(nrows=1,ncols=1,constrained_layout=True)
        t = np.linspace(0,self.Parent.Parent.TimeStep*(self.Parent.Parent.PointsNo-1),self.Parent.Parent.PointsNo)
        ax.plot(t,self.Values)
        ax.set_xlabel(r'$t\>[s]$')
        if self.Units == self.Parent.d.Units:
            fig.suptitle('Displacement time history')
            ax.set_ylabel(rf'$Displacement\>[{self.Units}]$')
        elif self.Units == self.Parent.v.Units:
            fig.suptitle('Velocity time history')
            ax.set_ylabel(rf'$Velocity\>[{self.Units}]$')
        elif self.Units == self.Parent.a.Units:
            fig.suptitle('Acceleration time history')
            ax.set_ylabel(rf'$Acceleration\>[{self.Units}]$')
        ax.grid(True,'both','both')
        if showAsync:
            ShowPlotAsync(fig)

class _MotionComponents:
    def __init__(self,parent):
        self.d = _MotionComponent(self)
        self.v = _MotionComponent(self)
        self.a = _MotionComponent(self)
        self.Parent = parent # Motion()

class Motion:
    def __init__(self,parent=None):
        self.Name = None
        self.PointsNo = None
        self.TimeStep = None
        self.MotionComponents = _MotionComponents(self)
        self.ResponseSpectrum = ResponseSpectrum(self)
        self.AriasIntensity = AriasIntensity(self)
        self.PowerSpectralDensity = PowerSpectralDensity(self)
        self.Parent = parent

    # If not all motion components are given, calculate them through integration or derivation
    def CalculateMotionComponents(self):
        state = 1*(self.MotionComponents.a.Values is not None) + 2*(self.MotionComponents.v.Values is not None) + 4*(self.MotionComponents.d.Values is not None)
        if state == 0:
            # Nothing exists
            raise Exception('seismicmotions.objects.Motion.CalculateMotionComponents: No motion data has been provided.')
        elif state == 1:
            # Only a exists
            self.MotionComponents.v = self.MotionComponents.a.IntegrateToMotionComponent()
            self.MotionComponents.v.Parent = self.MotionComponents
            self.MotionComponents.d = self.MotionComponents.v.IntegrateToMotionComponent()
            self.MotionComponents.d.Parent = self.MotionComponents
        elif state == 2:
            # Only v exists
            self.MotionComponents.a = self.MotionComponents.v.DeriveToMotionComponent()
            self.MotionComponents.a.Parent = self.MotionComponents
            self.MotionComponents.d = self.MotionComponents.v.IntegrateToMotionComponent()
            self.MotionComponents.d.Parent = self.MotionComponents
        elif state == 3:
            # Only a and v exist
            oneWay = self.MotionComponents.a.IntegrateToMotionComponent()
            oneWay.Parent = self.MotionComponents
            oneWay = oneWay.IntegrateToMotionComponent()
            anotherWay = self.MotionComponents.v.IntegrateToMotionComponent()
            self.MotionComponents.d = oneWay
            self.MotionComponents.d.Values = (oneWay.Values+anotherWay.Values)/2
            self.MotionComponents.d.Parent = self.MotionComponents
        elif state == 4:
            # Only d exists
            self.MotionComponents.v = self.MotionComponents.d.DeriveToMotionComponent()
            self.MotionComponents.v.Parent = self.MotionComponents
            self.MotionComponents.a = self.MotionComponents.v.DeriveToMotionComponent()
            self.MotionComponents.a.Parent = self.MotionComponents
            pass
        elif state == 5:
            # Only a and d exist
            oneWay = self.MotionComponents.a.IntegrateToMotionComponent()
            anotherWay = self.MotionComponents.d.DeriveToMotionComponent()
            self.MotionComponents.v = oneWay
            self.MotionComponents.v.Values = (oneWay.Values+anotherWay.Values)/2
            self.MotionComponents.v.Parent = self.MotionComponents
        elif state == 6:
            # Only v and d exist
            oneWay = self.MotionComponents.d.DeriveToMotionComponent()
            oneWay.Parent = self.MotionComponents
            oneWay = oneWay.DeriveToMotionComponent()
            anotherWay = self.MotionComponents.v.DeriveToMotionComponent()
            self.MotionComponents.a = oneWay
            self.MotionComponents.a.Values = (oneWay.Values+anotherWay.Values)/2
            self.MotionComponents.a.Parent = self.MotionComponents
        elif state == 7:
            # All exist
            pass
            
    def Resample(self,timeStepDivisor):
        if timeStepDivisor == 1:
            return
        duration = self.TimeStep*(self.PointsNo-1)
        if self.MotionComponents.d.Values is not None:
            self.MotionComponents.d.Values,_,newTimeStep = FourierTransformResample(self.MotionComponents.d.Values,duration,self.TimeStep,timeStepDivisor)
        if self.MotionComponents.v.Values is not None:
            self.MotionComponents.v.Values,_,newTimeStep = FourierTransformResample(self.MotionComponents.v.Values,duration,self.TimeStep,timeStepDivisor)
        if self.MotionComponents.a.Values is not None:
            self.MotionComponents.a.Values,_,newTimeStep = FourierTransformResample(self.MotionComponents.a.Values,duration,self.TimeStep,timeStepDivisor)
        self.PointsNo = (duration/newTimeStep).__round__()+1
        self.TimeStep = newTimeStep

    def SpectralMatchingWith(self,target):
        pass

    def Curtail(self,minTime=0):
        self.ResponseSpectrum.Calculate()
        tmax = np.max([
            np.max(self.ResponseSpectrum.Values.a.AtTimes),
            np.max(self.ResponseSpectrum.Values.v.AtTimes),
            np.max(self.ResponseSpectrum.Values.d.AtTimes)
        ])
        n = (max(tmax,minTime)/self.TimeStep+0.5).__round__()
        self.PointsNo = n+1
        self.MotionComponents.a.Values = self.MotionComponents.a.Values[0:self.PointsNo]
        self.MotionComponents.a.Statistics.Clear()
        self.MotionComponents.v.Values = self.MotionComponents.v.Values[0:self.PointsNo]
        self.MotionComponents.v.Statistics.Clear()
        self.MotionComponents.d.Values = self.MotionComponents.d.Values[0:self.PointsNo]
        self.MotionComponents.d.Statistics.Clear()
        self.ResponseSpectrum.Clear()
        self.AriasIntensity.Clear()
        self.PowerSpectralDensity.Clear()

    def AlignAsPerAriasIntensityT5(self,target,reCalculateAriasIntensity=True):
        if self.TimeStep != target.TimeStep:
            raise Exception(f'seismicmotions.objects.Motion.AlignAsPerAriasIntensityT5: target needs to have the same time step as current motion i.e. {self.TimeStep}, not {target.TimeStep}.')
        if reCalculateAriasIntensity:
            self.AriasIntensity.Calculate()
            target.AriasIntensity.Calculate()
        if self.AriasIntensity.t5 >= target.AriasIntensity.t5:
            dt = self.AriasIntensity.t5-target.AriasIntensity.t5
            target.ZeroPad(dt)
        else:
            dt = target.AriasIntensity.t5-self.AriasIntensity.t5
            self.ZeroPad(dt)
    
    def ZeroPack(self,maxTime):
        # Check arguments
        if maxTime <= self.TimeStep*(self.PointsNo-1):
            return
        n = (maxTime/self.TimeStep).__ceil__()
        if maxTime-n*self.TimeStep > 1e-10:
            raise Exception(f'seismicmotions.objects.Motion.ZeroPack: maxTime needs to be an integer multiple of the timestep i.e. {self.TimeStep}, now it is {maxTime} = {n} * {self.TimeStep} + {maxTime-n*self.TimeStep}.')
        # Since there are already some points, adding n intervals means adding n points, not n+1 points.
        n = n-self.PointsNo+1
        zeros = np.zeros(n)
        self.PointsNo += n
        self.MotionComponents.d.Values = np.append(self.MotionComponents.d.Values,zeros)
        if self.MotionComponents.d.Statistics.Peak is not None: self.MotionComponents.d.Statistics.Calculate()
        self.MotionComponents.v.Values = np.append(self.MotionComponents.v.Values,zeros)
        if self.MotionComponents.v.Statistics.Peak is not None: self.MotionComponents.v.Statistics.Calculate()
        self.MotionComponents.a.Values = np.append(self.MotionComponents.a.Values,zeros)
        if self.MotionComponents.a.Statistics.Peak is not None: self.MotionComponents.a.Statistics.Calculate()
        self.AriasIntensity.Values = np.append(self.AriasIntensity.Values,np.repeat(self.AriasIntensity.Total,n))

    def ZeroPad(self,timeShift):
        n = int(timeShift/self.TimeStep.__float__()+0.5)
        if timeShift-n*self.TimeStep > 1e-10:
            raise Exception(f'seismicmotions.objects.Motion.ZeroPad: timeShift needs to be an integer multiple of the timestep i.e. {self.TimeStep}, now it is {timeShift} = {n} * {self.TimeStep} + {timeShift-n*self.TimeStep}.')
        # Since there are already some points, adding n intervals means adding n points, not n+1 points.
        zeros = np.zeros(n)
        self.PointsNo += n
        self.MotionComponents.d.Values = np.append(zeros,self.MotionComponents.d.Values)
        if self.MotionComponents.d.Statistics.Peak is not None: self.MotionComponents.d.Statistics.Calculate()
        self.MotionComponents.v.Values = np.append(zeros,self.MotionComponents.v.Values)
        if self.MotionComponents.v.Statistics.Peak is not None: self.MotionComponents.v.Statistics.Calculate()
        self.MotionComponents.a.Values = np.append(zeros,self.MotionComponents.a.Values)
        if self.MotionComponents.a.Statistics.Peak is not None: self.MotionComponents.a.Statistics.Calculate()
        if self.ResponseSpectrum.Values.d.Ordinates is not None: self.ResponseSpectrum.Values.d.AtTimes += n*self.TimeStep
        if self.ResponseSpectrum.Values.v.Ordinates is not None: self.ResponseSpectrum.Values.v.AtTimes += n*self.TimeStep
        if self.ResponseSpectrum.Values.a.Ordinates is not None: self.ResponseSpectrum.Values.a.AtTimes += n*self.TimeStep
        if self.AriasIntensity.t5 is not None: self.AriasIntensity.t5 += n*self.TimeStep
        if self.AriasIntensity.t75 is not None: self.AriasIntensity.t75 += n*self.TimeStep
        if self.AriasIntensity.t95 is not None: self.AriasIntensity.t95 += n*self.TimeStep
        if self.AriasIntensity.Values is not None: self.AriasIntensity.Values = np.append(zeros,self.AriasIntensity.Values)

    def FilterOutFrequenciesAfter(self,filterOutFrequencyIntervals):
        duration = self.TimeStep*(self.PointsNo-1)
        if self.MotionComponents.d.Values is not None:
            self.MotionComponents.d.Values,_,_ = FourierTransformFilterOut(self.MotionComponents.d.Values,duration,self.TimeStep,filterOutFrequencyIntervals)
        if self.MotionComponents.v.Values is not None:
            self.MotionComponents.v.Values,_,_ = FourierTransformFilterOut(self.MotionComponents.v.Values,duration,self.TimeStep,filterOutFrequencyIntervals)
        if self.MotionComponents.a.Values is not None:
            self.MotionComponents.a.Values,_,_ = FourierTransformFilterOut(self.MotionComponents.a.Values,duration,self.TimeStep,filterOutFrequencyIntervals)
        
    def LoadFromFile(self,fileReader):
        (self.TimeStep,self.PointsNo,
            self.MotionComponents.a.Values,self.MotionComponents.a.Units,
            self.MotionComponents.v.Values,self.MotionComponents.v.Units,
            self.MotionComponents.d.Values,self.MotionComponents.d.Units) = fileReader.Load()

    def WriteToFile(self,fileWriter):
        fileWriter.Write(self)

    def Clear(self):
        self.PointsNo = None
        self.TimeStep = None
        self.MotionComponents.a.Clear()
        self.MotionComponents.v.Clear()
        self.MotionComponents.d.Clear()
        self.ResponseSpectrum.Clear()
        self.AriasIntensity.Clear()
        self.PowerSpectralDensity.Clear()
    
    def Copy(self):
        newMotion = Motion()
        newMotion.PointsNo = self.PointsNo
        newMotion.TimeStep = self.TimeStep
        newMotion.MotionComponents.d = self.MotionComponents.d.Copy()
        newMotion.MotionComponents.d.Parent = newMotion.MotionComponents
        newMotion.MotionComponents.v = self.MotionComponents.v.Copy()
        newMotion.MotionComponents.v.Parent = newMotion.MotionComponents
        newMotion.MotionComponents.a = self.MotionComponents.a.Copy()
        newMotion.MotionComponents.a.Parent = newMotion.MotionComponents
        newMotion.MotionComponents.Parent = newMotion
        newMotion.ResponseSpectrum = self.ResponseSpectrum.Copy()
        newMotion.ResponseSpectrum.Parent = newMotion
        newMotion.AriasIntensity = self.AriasIntensity.Copy()
        newMotion.AriasIntensity.Parent = newMotion
        newMotion.PowerSpectralDensity = self.PowerSpectralDensity.Copy()
        newMotion.PowerSpectralDensity.Parent = newMotion
        newMotion.Parent = self.Parent
        return newMotion
    
    def Plot(self,title=None,showAsync=False):
        fig,axs = plt.subplots(nrows=3,ncols=1,constrained_layout=True,sharex=True)
        if title is None:
            fig.suptitle('Time history')
        else:
            fig.suptitle(title)
        t = np.linspace(0,self.TimeStep*(self.PointsNo-1),self.PointsNo)
        if self.MotionComponents.a.Values is None or self.MotionComponents.v.Values is None or self.MotionComponents.d.Values is None:
            self.CalculateMotionComponents()
        axs[0].plot(t,self.MotionComponents.a.Values)
        axs[0].set_ylabel(rf'$Acceleration\>[{self.MotionComponents.a.Units}]$')
        axs[1].plot(t,self.MotionComponents.v.Values)
        axs[1].set_ylabel(rf'$Velocity\>[{self.MotionComponents.v.Units}]$')
        axs[2].plot(t,self.MotionComponents.d.Values)
        axs[2].set_ylabel(rf'$Displacement\>[{self.MotionComponents.d.Units}]$')
        axs[2].set_xlabel(r'$t\>[s]$')
        axs[0].set_xlim([t[0],t[-1]])
        for ax in axs:
            ax.minorticks_on()
            ax.grid(True,'major','both')
            ax.grid(True,'minor','both',alpha=0.3)
        if showAsync:
            ShowPlotAsync(fig)