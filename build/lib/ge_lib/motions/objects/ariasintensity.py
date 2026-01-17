import matplotlib.pyplot as plt
import numpy as np
from ..methods import CalculateAriasIntensity
from ..plotters.showplotasync import ShowPlotAsync

class AriasIntensity:
    def __init__(self,parent=None):
        self.Total = None
        self.t5 = None
        self.t75 = None
        self.t95 = None
        self.Values = None
        self.Parent = parent # Motion()
    
    def Calculate(self):
        # Prepare inputs
        accValues = self.Parent.MotionComponents.a.Values
        timeStep = self.Parent.TimeStep
        n = self.Parent.PointsNo
        # Calculate
        self.Total,self.t5,self.t75,self.t95,_,_,self.Values = CalculateAriasIntensity(accValues,timeStep,n)

    def LoadFromFile(self):
        pass

    def WriteToFile(self):
        pass

    def Clear(self):
        self.Total = None
        self.t5 = None
        self.t75 = None
        self.t95 = None
        self.Values = None
    
    def Copy(self):
        newAriasIntensity = AriasIntensity()
        newAriasIntensity.Total = self.Total
        newAriasIntensity.t5 = self.t5
        newAriasIntensity.t75 = self.t75
        newAriasIntensity.t95 = self.t95
        newAriasIntensity.Values = self.Values.copy() if self.Values is not None else None
        newAriasIntensity.Parent = self.Parent # Motion()
        return newAriasIntensity
    
    def Plot(self):
        fig,ax = plt.subplots(nrows=1,ncols=1,constrained_layout=True)
        fig.suptitle(r'$Arias\>Intensity$')
        t = np.linspace(0,self.Parent.TimeStep*(self.Parent.PointsNo-1),self.Parent.PointsNo)
        ax.plot(t,self.Values)
        ax.plot(self.t5,self.Total*0.05,marker='o',markeredgecolor='r',fillstyle='none',linestyle='None')
        ax.annotate(r'$t_{5}$',xy=(self.t5,self.Total*0.05),xycoords='data',xytext=(4,-8),textcoords='offset points')
        ax.plot(self.t75,self.Total*0.75,marker='o',markeredgecolor='r',fillstyle='none',linestyle='None')
        ax.annotate(r'$t_{75}$',xy=(self.t75,self.Total*0.75),xycoords='data',xytext=(4,-8),textcoords='offset points')
        ax.plot(self.t95,self.Total*0.95,marker='o',markeredgecolor='r',fillstyle='none',linestyle='None')
        ax.annotate(r'$t_{95}$',xy=(self.t95,self.Total*0.95),xycoords='data',xytext=(4,-8),textcoords='offset points')
        ax.set_xlabel(r'$t\>[s]$')
        ax.set_ylabel(rf'$Arias\>Intensity\>[{self.Parent.MotionComponents.a.Units}\cdot s]$')
        ax.set_xlim(t[0],t[-1])
        ax.grid(True,'both','both')
        ShowPlotAsync(fig)