import matplotlib.pyplot as plt
import numpy as np
from ..methods import MotionComponentAccelerationCalculateResponseSpectra,ResponseSpectrumScalingFactorToMatchTargetSpectrum_OrdinateValues,ResponseSpectrumScalingFactorToMatchTargetSpectrum_Integrals
from ..plotters.showplotasync import ShowPlotAsync

class _ResponseSpectumComponent:
    def __init__(self,parent=None):
        self.Type = None
        self.Ordinates = None
        self.AtTimes = None
        self.Parent = parent # ResponseSpectrum()

    def ScalingFactorToMatch(self,target,method='integrals'):
        # Check arguments
        if method not in ['ordinates','integrals']:
            raise Exception(f'seismicmotions.objects._ResponseSpectumComponent.ScalingFactorToMatch: method cannot be "{method}", it can either be "ordinates" or "integrals".')
        # Prepare inputs
        if self.Parent.Frequencies.Units == 'Hz':
            parentFrequencies = self.Parent.Frequencies.Values
        elif self.Parent.Frequencies.Units == 'rad/s':
            parentFrequencies = 2*np.pi*self.Parent.Frequencies.Values
        parentOrdinates = self.Ordinates
        if target.Parent.Frequencies.Units == 'Hz':
            targetFrequencies = target.Parent.Frequencies.Values
        elif target.Parent.Frequencies.Units == 'rad/s':
            targetFrequencies = 2*np.pi*target.Parent.Frequencies.Values
        targetOrdinates = target.Ordinates
        # Calculate
        if method == 'ordinates':
            scalingFactor = ResponseSpectrumScalingFactorToMatchTargetSpectrum_OrdinateValues(parentFrequencies,parentOrdinates,targetFrequencies,targetOrdinates)
        if method == 'integrals':
            scalingFactor = ResponseSpectrumScalingFactorToMatchTargetSpectrum_Integrals(parentFrequencies,parentOrdinates,targetFrequencies,targetOrdinates)
        return scalingFactor

    def LoadFromFile(self,fileReader):
        tol = 1e-5
        self.Type,self.Ordinates,self.AtTimes,ordinateUnits,frequencyUnits,frequencyValues = fileReader.Load()
        
        if frequencyUnits not in [None, 'rad/s','Hz']:
            raise Exception(f'seismicmotions.objects.responsespectrum._ResponseSpectumComponent.LoadFromFile: Frequency Units cannot be "{frequencyUnits}", it can either be "rad/s" or "Hz".')
        
        if self.Parent.Parent.MotionComponents.a.Units is None:
            self.Parent.Parent.MotionComponents.a.Units = ordinateUnits
        elif self.Parent.Parent.MotionComponents.a.Units != ordinateUnits:
            raise Exception(f'seismicmotions.objects.responsespectrum._ResponseSpectumComponent.LoadFromFile: Acceleration units have already been defined as "{self.Parent.Parent.MotionComponents.a.Units}", they cannot be defined again as "{ordinateUnits}".')

        if self.Parent.Frequencies.Units is None:
           self.Parent.Frequencies.Units = frequencyUnits
        elif self.Parent.Frequencies.Units != frequencyUnits:
            raise Exception(f'seismicmotions.objects.responsespectrum._ResponseSpectumComponent.LoadFromFile: Frequency units have already been defined as "{self.Parent.Frequencies.Units}", they cannot be defined again as "{frequencyUnits}".')
        
        if self.Parent.Frequencies.Values is None:
            self.Parent.Frequencies.Values = frequencyValues
            self.Parent.PointsNo = frequencyValues.size
        elif self.Parent.Frequencies.Values.size != frequencyValues.size:
            raise Exception(f'seismicmotions.objects.responsespectrum._ResponseSpectumComponent.LoadFromFile: Frequency values have already been defined and the new values do not match ({self.Parent.Frequencies.Values.size} existing frequency values vs {frequencyValues.size} given).')
        elif (maxDiff := np.max(np.abs(self.Parent.Frequencies.Values-frequencyValues))) > tol:
            raise Exception(f'seismicmotions.objects.responsespectrum._ResponseSpectumComponent.LoadFromFile: Frequency values have already been defined and the new values do not match (max diference {maxDiff}, with error tolerance {tol}).')

    def Plot(self,xScale='linear'):
        if id(self) == id(self.Parent.Values.a):
            n_u = ['accelerations',self.Parent.Parent.MotionComponents.a.Units]
        elif id(self) == id(self.Parent.Values.v):
            n_u = ['velocities',self.Parent.Parent.MotionComponents.v.Units]
        elif id(self) == id(self.Parent.Values.d):
            n_u = ['displacements',self.Parent.Parent.MotionComponents.d.Units]

        fig,ax = plt.subplots(nrows=1,ncols=1,constrained_layout=True)
        fig.suptitle(r'$Response\>spectra$')
        ax.plot(self.Parent.Frequencies.Values,self.Ordinates,color='blue')
        ax.set_title(rf'${self.Type.capitalize()}\>{n_u[0]}$')
        ax.set_ylabel(rf'$accelerations\>[{n_u[1]}]$')
        ax0 = ax.twinx()
        if self.AtTimes is not None:
            ax0.plot(self.Frequencies.Values,self.Values.a.AtTimes,color=(1,0,0,0.3))
        ax0.set_ylabel(r'$Response\>time\>at\>ordinate\>[s]$')
        ax0.set_ylim([0,2*ax0.get_ylim()[1]])

        ax.grid(True,'both','both')
        ax.set_xlabel(rf'$frequencies\>[{self.Parent.Frequencies.Units}]$')
        ax.set_xscale(xScale)

        ShowPlotAsync(fig)

class _ResponseSpectumFrequencyComponent:
    def __init__(self):
        self.Units = None
        self.Values = None

class _ResponseSpectumComponents:
    def __init__(self,parent=None):
        self.d = _ResponseSpectumComponent(parent)
        self.v = _ResponseSpectumComponent(parent)
        self.a = _ResponseSpectumComponent(parent)

class ResponseSpectrum:
    def __init__(self,parent=None):
        self.Frequencies = _ResponseSpectumFrequencyComponent()
        self.PointsNo = None
        self.Values = _ResponseSpectumComponents(self)
        self.Parent = parent # Motion()
    
    def Calculate(self,frequencies=None,ksi=0.05,accType='absolute',velType='relative',dispType='relative',nCores=0):
        # Check arguments
        if frequencies is not None and frequencies.Units is not None and frequencies.Units not in ['rad/s','Hz']:
            raise Exception(f'seismicmotions.objects.responsespectrum.ResponseSpectrum.Calculate: frequencies.Units cannot be "{frequencies.Units}", it can either be "rad/s" or "Hz".')
        if accType not in ['absolute','relative']:
            raise Exception(f'seismicmotions.objects.responsespectrum.ResponseSpectrum.Calculate: accType cannot be "{accType}", it can either be "absolute" or "relative".')
        if velType not in ['absolute','relative']:
            raise Exception(f'seismicmotions.objects.responsespectrum.ResponseSpectrum.Calculate: accType cannot be "{accType}", it can either be "absolute" or "relative".')
        if dispType not in ['absolute','relative']:
            raise Exception(f'seismicmotions.objects.responsespectrum.ResponseSpectrum.Calculate: accType cannot be "{accType}", it can either be "absolute" or "relative".')
        # Prepare inputs
        accValues = self.Parent.MotionComponents.a.Values
        duration = self.Parent.TimeStep*(self.Parent.PointsNo-1)
        timeStep = self.Parent.TimeStep
        if frequencies is None:
            if self.Frequencies.Units is None:
                self.Frequencies.Units = 'Hz'
            if self.Frequencies.Values is None:
                self.Frequencies.Values = np.geomspace(0.0001,100,600)
            freqs = self.Frequencies.Values
        else:
            self.Frequencies.Values = frequencies.Values
            self.Frequencies.Units = frequencies.Units
            if frequencies.Units == 'rad/s':
                freqs = 2*np.pi*self.Frequencies.Values
            elif frequencies.Units == 'Hz':
                freqs = self.Frequencies.Values
        velValues = self.Parent.MotionComponents.v.Values
        dispValues = self.Parent.MotionComponents.d.Values
        # Calculate
        accVals,accTimes,velVals,velTimes,dispVals,dispTimes = MotionComponentAccelerationCalculateResponseSpectra(accValues,duration,timeStep,freqs,ksi,velValues,dispValues,accType,velType,dispType,nCores)
        self.PointsNo = self.Frequencies.Values.size
        self.Values.d.Type = dispType
        self.Values.d.Ordinates = dispVals
        self.Values.d.AtTimes = dispTimes
        self.Values.v.Type = velType
        self.Values.v.Ordinates = velVals
        self.Values.v.AtTimes = velTimes
        self.Values.a.Type = accType
        self.Values.a.Ordinates = accVals
        self.Values.a.AtTimes = accTimes

    def LoadFromFile(self):
        pass

    def WriteToFile(self,fileWriter):
        fileWriter.Write(self)
        pass

    def Clear(self):
        self.Frequencies.Units = None
        self.Frequencies.Values = None
        self.PointsNo = None
        self.Values.d.Type = None
        self.Values.d.Ordinates = None
        self.Values.d.AtTimes = None
        self.Values.v.Type = None
        self.Values.v.Ordinates = None
        self.Values.v.AtTimes = None
        self.Values.a.Type = None
        self.Values.a.Ordinates = None
        self.Values.a.AtTimes = None
    
    def Copy(self):
        newResponseSpectrum = ResponseSpectrum()
        newResponseSpectrum.Frequencies.Units = self.Frequencies.Units
        newResponseSpectrum.Frequencies.Values = self.Frequencies.Values.copy() if self.Frequencies.Values is not None else None
        newResponseSpectrum.PointsNo = self.PointsNo
        newResponseSpectrum.Values.d.Type = self.Values.d.Type
        newResponseSpectrum.Values.d.Ordinates = self.Values.d.Ordinates.copy() if self.Values.d.Ordinates is not None else None
        newResponseSpectrum.Values.d.AtTimes = self.Values.d.AtTimes.copy() if self.Values.d.AtTimes is not None else None
        newResponseSpectrum.Values.d.Parent = self.Values.d.Parent
        newResponseSpectrum.Values.v.Type = self.Values.v.Type
        newResponseSpectrum.Values.v.Ordinates = self.Values.v.Ordinates.copy() if self.Values.v.Ordinates is not None else None
        newResponseSpectrum.Values.v.AtTimes = self.Values.v.AtTimes.copy() if self.Values.v.AtTimes is not None else None
        newResponseSpectrum.Values.v.Parent = self.Values.v.Parent
        newResponseSpectrum.Values.a.Type = self.Values.a.Type
        newResponseSpectrum.Values.a.Ordinates = self.Values.a.Ordinates.copy() if self.Values.a.Ordinates is not None else None
        newResponseSpectrum.Values.a.AtTimes = self.Values.a.AtTimes.copy() if self.Values.a.AtTimes is not None else None
        newResponseSpectrum.Values.a.Parent = self.Values.a.Parent
        newResponseSpectrum.Parent = self.Parent # Motion()
        return newResponseSpectrum
    
    def Plot(self,xScale='linear'):
        fig,axs = plt.subplots(nrows=1,ncols=3,constrained_layout=True)
        fig.suptitle(r'$Response\>spectra$')
        axs[0].plot(self.Frequencies.Values,self.Values.a.Ordinates,color='blue')
        axs[0].set_title(rf'${self.Values.a.Type.capitalize()}\>accelerations$')
        axs[0].set_ylabel(rf'$accelerations\>[{self.Parent.MotionComponents.a.Units}]$')
        axs0 = axs[0].twinx()
        if self.Values.a.AtTimes is not None:
            axs0.plot(self.Frequencies.Values,self.Values.a.AtTimes,color=(1,0,0,0.3))
        axs0.set_ylabel(r'$Response\>time\>at\>ordinate\>[s]$')
        axs0.set_ylim([0,2*axs0.get_ylim()[1]])
        
        axs[1].plot(self.Frequencies.Values,self.Values.v.Ordinates,color='blue')
        axs[1].set_title(rf'${self.Values.v.Type.capitalize()}\>velocities$')
        axs[1].set_ylabel(rf'$velocities\>[{self.Parent.MotionComponents.v.Units}]$')
        axs1 = axs[1].twinx()
        if self.Values.v.AtTimes is not None:
            axs1.plot(self.Frequencies.Values,self.Values.v.AtTimes,color=(1,0,0,0.3))
        axs1.set_ylabel(r'$Response\>time\>at\>ordinate\>[s]$')
        axs1.set_ylim([0,2*axs1.get_ylim()[1]])

        axs[2].plot(self.Frequencies.Values,self.Values.d.Ordinates,color='blue')
        axs[2].set_title(rf'${self.Values.d.Type.capitalize()}\>displacements$')
        axs[2].set_ylabel(rf'$displacements\>[{self.Parent.MotionComponents.d.Units}]$')
        axs2 = axs[2].twinx()
        if self.Values.d.AtTimes is not None:
            axs2.plot(self.Frequencies.Values,self.Values.d.AtTimes,color=(1,0,0,0.3))
        axs2.set_ylabel(r'$Response\>time\>at\>ordinate\>[s]$')
        axs2.set_ylim([0,2*axs2.get_ylim()[1]])

        for ax in axs:
            ax.grid(True,'both','both')
            ax.set_xlabel(rf'$frequencies\>[{self.Frequencies.Units}]$')
        for ax in np.append(axs,[axs0,axs1,axs2]):
            ax.set_xscale(xScale)
        ShowPlotAsync(fig)