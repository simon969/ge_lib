from multiprocessing import Pool as mp_Pool, cpu_count as mp_cpu_count
import numpy as np
from fractions import Fraction as fc
from ..objects.motion import Motion

class MotionTriplet:
    def __init__(self):
        self.x = Motion(self)
        self.y = Motion(self)
        self.z = Motion(self)

    def CalculateResponseSpectra(self,frequencies=None,ksi=0.05,accType='absolute',velType='relative',dispType='relative',nCores=None):
        self.x.ResponseSpectrum.Calculate(frequencies,ksi,accType,velType,dispType,nCores)
        self.y.ResponseSpectrum.Calculate(frequencies,ksi,accType,velType,dispType,nCores)
        self.z.ResponseSpectrum.Calculate(frequencies,ksi,accType,velType,dispType,nCores)

    def ResampleToCommonTimeStep(self):
        self.x.TimeStep = fc(self.x.TimeStep)
        self.y.TimeStep = fc(self.y.TimeStep)
        self.z.TimeStep = fc(self.z.TimeStep)
        dt = np.gcd(np.gcd(self.x.TimeStep,self.y.TimeStep),self.z.TimeStep)
        self.x.Resample((self.x.TimeStep/dt).__round__())
        self.y.Resample((self.y.TimeStep/dt).__round__())
        self.z.Resample((self.z.TimeStep/dt).__round__())

    def ZeroPackToCommonDuration(self):
        dur = max([self.x.TimeStep*(self.x.PointsNo-1),self.y.TimeStep*(self.y.PointsNo-1),self.z.TimeStep*(self.z.PointsNo-1)])
        self.x.ZeroPack(dur)
        self.y.ZeroPack(dur)
        self.z.ZeroPack(dur)

    def ZeroPadAsPerLatestAriasIntensityT5(self):
        self.x.AriasIntensity.Calculate()
        self.y.AriasIntensity.Calculate()
        self.z.AriasIntensity.Calculate()
        i = np.argmax([self.x.AriasIntensity.t5,self.y.AriasIntensity.t5,self.z.AriasIntensity.t5])
        mot = [self.x,self.y,self.z][i]
        self.x.AlignAsPerAriasIntensityT5(mot,False)
        self.y.AlignAsPerAriasIntensityT5(mot,False)
        self.z.AlignAsPerAriasIntensityT5(mot,False)

    def _CalculateCorrelationCoefficient(self,left,right,motionComponent):
        return getattr(getattr(self,left).MotionComponents,motionComponent).CorrelationCoefficientWith(getattr(getattr(self,right).MotionComponents,motionComponent))
    def CalculateCorrelationCoefficients(self,motionComponent='a',nCores=0):
        # Correlation coefficients are calculated as corCoeff_xy, corCoeff_xz and corCoeff_yz 
        if nCores == 0:
            corCoeffs = []
            corCoeffs.append(getattr(getattr(self,'x').MotionComponents,motionComponent).CorrelationCoefficientWith(getattr(getattr(self,'y').MotionComponents,motionComponent)))
            corCoeffs.append(getattr(getattr(self,'x').MotionComponents,motionComponent).CorrelationCoefficientWith(getattr(getattr(self,'z').MotionComponents,motionComponent)))
            corCoeffs.append(getattr(getattr(self,'y').MotionComponents,motionComponent).CorrelationCoefficientWith(getattr(getattr(self,'z').MotionComponents,motionComponent)))
        else:
            with mp_Pool(min([mp_cpu_count(),3])) as pool:
                corCoeffs = pool.starmap(
                    self._CalculateCorrelationCoefficient,
                    zip(
                        ['x','x','y'],
                        ['y','z','z'],
                        [motionComponent]*3
                    )
                )
        return np.array(corCoeffs)
        
    def LoadFromFile(self):
        pass

    def WriteToFile(self):
        pass

    def Copy(self):
        newMotionTriplet = MotionTriplet()
        newMotionTriplet.x = self.x.Copy()
        newMotionTriplet.x.Parent = newMotionTriplet
        newMotionTriplet.y = self.y.Copy()
        newMotionTriplet.y.Parent = newMotionTriplet
        newMotionTriplet.z = self.z.Copy()
        newMotionTriplet.z.Parent = newMotionTriplet
        return newMotionTriplet
    
    def Clear(self):
        self.x = None
        self.y = None
        self.z = None

    def Plot(self):
        self.x.Plot()
        self.y.Plot()
        self.z.Plot()