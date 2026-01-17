from .PlaxisScripting import PlaxisScripting     
class Plaxis3dInput (PlaxisScripting):
    def __init__(self,
                 input_server
                 ):
        super(Plaxis3dInput, self).__init__(input_server)  
        
#   file:///C:/Program%20Files/Plaxis/PLAXIS%203D/Manuals/English/input_objects/contents.html
    def getPhaseName(self, phase):
        for p in self.g_o.Phases[:]:
            if (str(p)==str(phase)):
                return p.Name
    
    def getPhaseDetails(self):
        results = []
        allpassed = True
        
        print('getting input phase details')
        
        for phase in self.g_o.Phases[:]:
            msg ="not calculated"
            if not phase.ShouldCalculate:
                if phase.CalculationResult == phase.CalculationResult.ok:
                    msg ="OK" 
                    #may be extended for more details
                else:
                    msg ="Failed: error {0}".format(phase.LogInfo)
                    allpassed =False
            
            prevPhaseName = self.getPhaseName (phase.PreviousPhase)
            results.append( "{},{},{},{},{},{}".format(phase.Name, phase.Comments, phase.Number, phase.Identification, prevPhaseName, phase.DeformCalcType))
        return allpassed, results

