from ..methods import MotionSuiteOptimiseFactorsToMatchSpectrum
from ..objects.motion import Motion

class MotionSuite:
    def __init__(self):
        self.Motions:list[Motion] = []

    def CalculateResponseSpectra(self,frequencies=None,ksi=0.05,accType='absolute',velType='relative',dispType='relative',nCores=None):
        for mot in self.Motions:
            mot.ResponseSpectrum.Calculate(frequencies,ksi,accType,velType,dispType,nCores)

    def OptimiseFactorsToMatchSpectrum(self,targetSpectrumComponent,component='a'):
        motionsOrdinates = [getattr(itm.ResponseSpectrum.Values,component).Ordinates for itm in self.Motions]
        motionFrequencies = self.Motions[0].ResponseSpectrum.Frequencies.Values
        return MotionSuiteOptimiseFactorsToMatchSpectrum(motionFrequencies,motionsOrdinates,targetSpectrumComponent.Parent.Frequencies.Values,targetSpectrumComponent.Ordinates)
    
    def Copy(self):
        newMotionSuite = MotionSuite()
        for mot in self.Motions:
            newMotionSuite.Motions.append(mot.Copy())
        return newMotionSuite
    
    def Clear(self):
        self.Motions.clear()