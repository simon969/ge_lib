import os
import numpy as np
import matplotlib.pyplot as plt

COMPONENT_VEL_X = 'VelocityX'
COMPONENT_VEL_Y = 'VelocityY'
COMPONENT_VEL_Z = 'VelocityZ'

COMPONENT_DISP_X = 'DisplacementX'
COMPONENT_DISP_Y = 'DisplacementY'
COMPONENT_DISP_Z = 'DisplacementZ'

COMPONENT_ACC_X = 'AccelerationX'
COMPONENT_ACC_Y = 'AccelerationY'
COMPONENT_ACC_Z = 'AccelerationZ'

class _AriasIntensity:
    def __init__(self,total:float=None,t5:float=None,duration5_75:float=None,duration5_95:float=None) -> None:
        self.Total = total
        self.T5 = t5
        self.Duration5_75 = duration5_75
        self.Duration5_95 = duration5_95


class _ResponseSpectrum:
    def __init__(self,omegas:np.array=None,ordinates:np.array=None,n:int=None) -> None:
        self.Omegas = omegas
        self.Ordinates = ordinates
        if n is None:
            self.PointsNo = np.size(omegas)
        else:
            self.PointsNo = n

    # Using integrals
    def ScalingFactorToMatch(self,targetResponseSpectrum) -> float:
        omegas = np.unique(np.append(self.Omegas,targetResponseSpectrum.Omegas))
        accThis = np.interp(omegas,self.Omegas,self.Ordinates)
        accTarget = np.interp(omegas,targetResponseSpectrum.Omegas,targetResponseSpectrum.Ordinates)
        x1 = omegas[0:-1]
        x2 = omegas[1:]
        g1 = accThis[0:-1]
        g2 = accThis[1:]
        toScaleIntegralSquared = np.sum((x2-x1)*(g1**2+g1*g2+g2**2))/3
        f1 = accTarget[0:-1]
        f2 = accTarget[1:]
        integralProduct = np.sum((x2-x1)*(f1*g1+f2*g2))/2
        scalingFactor = integralProduct/toScaleIntegralSquared
        return scalingFactor

    # Using just values
    def ScalingFactorToMatch2(self,targetResponseSpectrum) -> float:
        omegas = self.Omegas
        accThis = self.Ordinates
        accTarget = np.interp(omegas,targetResponseSpectrum.Omegas,targetResponseSpectrum.Ordinates)
        scalingFactor = np.sum(accThis*accTarget)/np.sum(accThis**2)
        return scalingFactor

class _PowerSpectralDensity:
    def __init__(self,omegas:np.array=None,psds:np.array=None,n:int=None) -> None:
        self.Omegas = omegas
        self.Psds = psds
        if n is None:
            self.PointsNo = np.size(omegas)
        else:
            self.PointsNo = n


class _XYZ:
    def __init__(self) -> None:
        self.X = None
        self.Y = None
        self.Z =  None


class _CorrelationCoefficient:
    def __init__(self) -> None:
        self.XY = None
        self.YZ = None
        self.ZX = None


class _XYZSelfCorrelation(_XYZ):
    def __init__(self) -> None:
        super().__init__()
        self.SelfCorrelation = _CorrelationCoefficient()


class MotionComponent:
    def __init__(self):
       self.Title = ""
       self.PointsNo = 0
       self.TimeStep = 0
       self.Values = []
             
    def Stats(self) -> tuple[int,float,float]:
        self.Mean = np.sum(self.Values)/self.PointsNo
        self.Stdv = np.sqrt(np.sum((self.Values-self.mean)**2)/self.PointsNo)
        self.MaxAbs = np.max(np.abs(self.Values))
        return (self.Mean,self.Stdv,self.MaxAbs)
        
    def LoadData(self, mr):
        (self.Title, self.PointsNo,self.TimeStep,self.Values) = mr.ReadFromFile()

class MotionComponentAcceleration(MotionComponent):
    def __init__(self):
        self.AriasIntensity = _AriasIntensity(*self.CalculateAriasIntensity())
        self.AccelerationsResponseSpectrum = _ResponseSpectrum(*self.FiniteDifferencesResponseSpectrum())
        self.PowerSpectralDensity = _PowerSpectralDensity(*self.CalculatePowerSpectralDensity())

    def CalculateAriasIntensity(self) -> tuple[float,float,float,float]:
        g1 = self.Values[0:-1]
        g2 = self.Values[1:]
        ariasIntensity = np.pi/2/3*self.TimeStep*np.cumsum(g1**2+g1*g2+g2**2)
        ariasIntensity = np.append(np.zeros(0),ariasIntensity)
        diff = np.clip(ariasIntensity-0.05*ariasIntensity[-1],None,0)
        i = np.argmax(diff)-1
        t5 = i*self.TimeStep+self.TimeStep/2
        diff = np.clip(ariasIntensity-0.75*ariasIntensity[-1],None,0)
        i = np.argmax(diff)-1
        t75 = i*self.TimeStep+self.TimeStep/2
        diff = np.clip(ariasIntensity-0.95*ariasIntensity[-1],None,0)
        i = np.argmax(diff)-1
        t95 = i*self.TimeStep+self.TimeStep/2
        return(ariasIntensity[-1],t5,t75-t5,t95-t5)

    def FiniteDifferencesResponseSpectrum(self,omegas:np.array=None,ksi:float=0.05) -> tuple[np.array,np.array]:
        # Function to interpolate the acceleration function at the intermediate time moments
        def InterpolateAcc(t:float) -> float:
            i = int(t/self.TimeStep)
            if t>(self.PointsNo-1)*self.TimeStep:
                return 0
            elif t==(self.PointsNo-1)*self.TimeStep:
                return self.Values[self.PointsNo-1]
            else:
                return self.Values[i]+(self.Values[i+1]-self.Values[i])*(t-i*self.TimeStep)/self.TimeStep
        
        # Get omegas
        if omegas is None:
            # Tmin determined by omega_max, determined by the maximum omega of the Fourier transform
            Tmin = (self.TimeStep*(self.PointsNo+1))/(int(self.PointsNo/2+0.5)-1)
            # Tmax determined by ASCE requiring at least 20s
            Tmax = 20
            # Number of points distributed evenly, 100 per frequency decade as per ASCE
            fmin = 1/Tmax
            fmax = 1/Tmin
            nOmegas = int(np.log10(fmax/fmin)*100+0.5)+1
            omegas = 2*np.pi*np.geomspace(fmin,fmax,nOmegas)
        else:
            nOmegas = np.size(omegas)

        # Response timestep
        ts = self.TimeStep/10
        nI = self.PointsNo
        nO = int((nI-1)*self.TimeStep/ts+1 + 0.5)
        
        # Constants
        omegasTs = omegas*ts
        twoMinusOmegasTsSquared = 2-omegasTs**2
        ksiOmegasTs = ksi*omegasTs
        OnePlusKsiOmegasTs = 1+ksiOmegasTs
        OneMinusKsiOmegasTs = 1-ksiOmegasTs
        
        dispResponse = []
        i = 0
        dispResponse.append(np.zeros(nOmegas))
        i = 1
        dispResponse.append(-ts**2*InterpolateAcc((i-1)*ts)*np.ones(nOmegas))
        for i in range(2,nO):
            dispResponse.append(dispResponse[i-1]*twoMinusOmegasTsSquared/OnePlusKsiOmegasTs - dispResponse[i-2]*OneMinusKsiOmegasTs/OnePlusKsiOmegasTs - InterpolateAcc((i-1)*ts)*ts**2/OnePlusKsiOmegasTs)
    
        velResponse = []
        i = 0
        velResponse.append(np.zeros(nOmegas))
        for i in range(1,nO-1):
            velResponse.append((dispResponse[i+1]-dispResponse[i-1])/(2*ts))
        i = nO-1
        dispResponse_nO = dispResponse[i]*twoMinusOmegasTsSquared/OnePlusKsiOmegasTs - dispResponse[i-1]*OneMinusKsiOmegasTs/OnePlusKsiOmegasTs - InterpolateAcc(i*ts)*ts**2/OnePlusKsiOmegasTs
        velResponse.append((dispResponse_nO-dispResponse[i-1])/(2*ts))
    
        accResponse = []
        i = 0
        accResponse.append(2*(dispResponse[1]-dispResponse[0])/ts**2)
        for i in range(1,nO-1):
            accResponse.append((dispResponse[i+1]-2*dispResponse[i]+dispResponse[i-1])/ts**2)
        i = nO-1
        accResponse.append((dispResponse_nO-2*dispResponse[i]+dispResponse[i-1])/ts**2)
        tResponse = np.linspace(0,(nO-1)*ts,nO)
        dispResponse = np.array(dispResponse)
        velResponse = np.array(velResponse)
        accResponse = np.array(accResponse)

        # Get maximums for the response spectrum
        a_max = np.amax(np.abs(accResponse),axis=0)
        return (omegas,a_max,nO)

    def CalculatePowerSpectralDensity(self) -> tuple[np.array,np.array]:
        # Do a first Fourier transformation
        n = self.PointsNo
        amps = np.abs(np.fft.fft(self.Values))
        if n%2==0:
            omegas = 2*np.pi*np.linspace(0,n//2-1,n//2)/(self.TimeStep*n)
            amps = amps[0:int(n/2+0.5)]
        else:
            omegas = 2*np.pi*np.linspace(0,n//2,n//2+1)/(self.TimeStep*n)
            amps = amps[0:int((n-1)/2+1+0.5)]
        amps = amps*self.TimeStep
        # Then use the transformation to calculate Power Spectral Density (PSD)
        psds = amps**2/(np.pi*self.AriasIntensity.Duration5_75)
        return (omegas,psds)

    
    

class MotionComponentAcceleration2(MotionComponentAcceleration):
    def __init__(self,title:str,timeStep:float,values:np.array) -> None:
        self.Title = title
        self.TimeStep = timeStep
        self.Values = values
        self.PointsNo = np.size(values)
       

   
class Motion:
    def __init__(self) -> None:
       
        self.Displacements = _XYZ()
        self.Velocities = _XYZ()
        self.Accelerations = _XYZSelfCorrelation()
        self.V_A = _XYZ()
        self.AD_V2 = _XYZ()
      
    
    def LoadData(self, component, mr):
              
        if (component==COMPONENT_DISP_X):
           self.Displacements.X = MotionComponent()
           self.Dispalcements.X.LoadData(mr)
        if (component==COMPONENT_DISP_Y):
           self.Displacements.Y = MotionComponent()
           self.Displacements.Y.LoadData(mr)
        if (component==COMPONENT_DISP_Z):
           self.Displacements.Z = MotionComponent()
           self.Dispalcements.Z.LoadData(mr)
        
        if (component==COMPONENT_VEL_X):
           self.Velocities.X = MotionComponent()
           self.Velocities.X.LoadData(mr)
        if (component==COMPONENT_VEL_Y):
           self.Velocities.Y = MotionComponent()
           self.Velocities.Y.LoadData(mr)
        if (component==COMPONENT_VEL_Z):
           self.Velocities.Z = MotionComponent()
           self.Velocities.Z.LoadData(mr)
        
        if (component==COMPONENT_ACC_X):
           self.Accelerations.X = MotionComponentAcceleration()
           self.Accelerations.X.LoadData(mr)
        if (component==COMPONENT_ACC_Y):
           self.Accelerations.Y = MotionComponentAcceleration()
           self.Accelerations.Y.LoadData(mr)
        if (component==COMPONENT_ACC_Z):
           self.Accelerations.Z = MotionComponentAcceleration()
           self.Accelerations.Z.LoadData(mr)

    def InitialiseCorrelations(self):
        if self.Accelerations!=None:
            self.Accelerations.SelfCorrelation.XY = self.CorrelationCoefficient(self.Accelerations.X,self.Accelerations.Y)
            self.Accelerations.SelfCorrelation.YZ = self.CorrelationCoefficient(self.Accelerations.Y,self.Accelerations.Z)
            self.Accelerations.SelfCorrelation.ZX = self.CorrelationCoefficient(self.Accelerations.Z,self.Accelerations.X)

    def SetV_A(self):    
        if self.Velocities!=None and self.Accelerations!=None:
            self.V_A.X = self.Velocities.X.MaxAbs/self.Accelerations.X.MaxAbs
            self.V_A.Y = self.Velocities.Y.MaxAbs/self.Accelerations.Y.MaxAbs
            self.V_A.Z = self.Velocities.Z.MaxAbs/self.Accelerations.Z.MaxAbs 

    def SetAD_V2(self):
        if self.Displacements!=None and self.Velocities!=None and self.Accelerations!=None:
            self.AD_V2.X = self.Accelerations.X.MaxAbs*self.Displacements.X.MaxAbs/self.Velocities.X.MaxAbs**2
            self.AD_V2.Y = self.Accelerations.Y.MaxAbs*self.Displacements.Y.MaxAbs/self.Velocities.Y.MaxAbs**2
            self.AD_V2.Z = self.Accelerations.Z.MaxAbs*self.Displacements.Z.MaxAbs/self.Velocities.Z.MaxAbs**2

    def CorrelationCoefficient(self,motionComponent1:MotionComponent,motionComponent2:MotionComponent) -> float:

        if motionComponent1.TimeStep != motionComponent2.TimeStep:
            raise ValueError('Motion.CorrelationCoefficient: Unable to calculate correlation coefficient for motions with different time steps.')
        
        n1 = motionComponent1.PointsNo
        n2 = motionComponent2.PointsNo
        
        if n1 < n2:
            n = n2
            mot1 = np.append(motionComponent1.Values,np.zeros(n2-n1))
            m1 = motionComponent1.Mean*n1/n2
            stdv1 = np.sqrt(np.sum(motionComponent1.Values**2)*(n2-n1)/n1**2+motionComponent1.Stdv**2)
            mot2 = np.append(motionComponent2.Values,np.zeros(0))
            m2 = motionComponent2.Mean
            stdv2 = motionComponent2.Stdv
        else:
            n = n1
            mot1 = np.append(motionComponent1.Values,np.zeros(0))
            m1 = motionComponent1.Mean
            stdv1 = motionComponent1.Stdv
            mot2 = np.append(motionComponent2.Values,np.zeros(n1-n2))
            m2 = motionComponent2.Mean*n2/n1
            stdv2 = np.sqrt(np.sum(motionComponent2.Values**2)*(n1-n2)/n2**2+motionComponent2.Stdv**2)
        r12 = np.sum((mot1-m1)*(mot2-m2))/(n*stdv1*stdv2)
        return r12

    
def ReadTargetSpectrum(path:str) -> _ResponseSpectrum:
    omegas = []
    ordinates = []
    with open(path,'r') as fil:
        for i in range(0,1):
            lin = fil.readline()
        while True:
            lin = fil.readline()
            if not lin:
                break
            lin = lin.strip(' \n').split('\t')
            omegas.append(float(lin[0]))
            ordinates.append(float(lin[1]))
    targetSpectrum = _ResponseSpectrum()
    targetSpectrum.Omegas = np.array(omegas)
    targetSpectrum.Omegas = 2*np.pi/targetSpectrum.Omegas
    targetSpectrum.Ordinates = np.array(ordinates)
    targetSpectrum.Omegas = np.flip(targetSpectrum.Omegas)
    targetSpectrum.Ordinates = np.flip(targetSpectrum.Ordinates)
    return targetSpectrum

