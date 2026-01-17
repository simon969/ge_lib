from ..methods import MotionTripletSuiteOptimiseFactorsToMatchSpectrum
from .motiontriplet import MotionTriplet
import numpy as np

class MotionTripletSuite:
    def __init__(self):
        self.MotionTriplets:list[MotionTriplet] = []

    def CalculateResponseSpectra(self,frequencies=None,ksi=0.05,accType='absolute',velType='relative',dispType='relative',nCores=None):
        for motTrip in self.MotionTriplets:
            motTrip.CalculateResponseSpectra(frequencies,ksi,accType,velType,dispType,nCores)
    
    def OptimiseFactorsToMatchSpectrum(self,targetSpectrumComponentX,targetSpectrumComponentY,targetSpectrumComponentZ,component='a') -> np.ndarray:
        motionsOrdinatesX = [getattr(itm.x.ResponseSpectrum.Values,component).Ordinates for itm in self.MotionTriplets]
        motionsOrdinatesY = [getattr(itm.y.ResponseSpectrum.Values,component).Ordinates for itm in self.MotionTriplets]
        motionsOrdinatesZ = [getattr(itm.z.ResponseSpectrum.Values,component).Ordinates for itm in self.MotionTriplets]
        motionFrequencies = self.MotionTriplets[0].x.ResponseSpectrum.Frequencies.Values
        return MotionTripletSuiteOptimiseFactorsToMatchSpectrum(motionFrequencies,motionsOrdinatesX,motionsOrdinatesY,motionsOrdinatesZ,
                                                                targetSpectrumComponentX.Parent.Frequencies.Values,
                                                                targetSpectrumComponentX.Ordinates,
                                                                targetSpectrumComponentY.Parent.Frequencies.Values,
                                                                targetSpectrumComponentY.Ordinates,
                                                                targetSpectrumComponentZ.Parent.Frequencies.Values,
                                                                targetSpectrumComponentZ.Ordinates)

    def Copy(self):
        newMotionTripletSuite = MotionTripletSuite()
        for motTrip in self.MotionTriplets:
            newMotionTripletSuite.Motions.append(motTrip.Copy())
        return newMotionTripletSuite
    
    def Clear(self):
        self.MotionTriplets.clear()