from .PlaxisScripting import Status
from .Plaxis3dResults2024 import Plaxis3dResults2024
from .OutputWriter import GetWriter

class Plaxis3dResults2025 (Plaxis3dResults2024): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults2025, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3d2025"
    def getEmbeddedBeamResultsBySteps(self,
                    fileOut=None,
                    filePoints=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None,
                    stepList=None,
                    fileSteps=None,
                    mode = 'new'
                    ):
        
        self.s_o.allow_caching = False
        
        self.s_o.enable_logging()
        
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
           
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if not filePoints is None:
            self.loadXYNodeList(filePoints)
        
        if not stepList is None:
            self.StepList = stepList.split(",")
        
        if not fileSteps is None:
            self.loadStepList(fileSteps)
            
        if stepList is None and fileSteps is None:
            self.StepList = []
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,ElementID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN),Q12(kN),Q13(kN),M2(kNm),M3(kNm),Tskin(kN/m),Tlat(kN/m),Tlat2(kN/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
      
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)
        
        print (self.StepList)
        
        for phase in self.phaseOrder:
            print("Request beam results for {}".format(phase.Name.value))
            
            self.setSteps (phase)
            
            for step in self.Steps:
                # print("        Interface results for {}".format(step.Name.value))
                print("Request beam results for {}".format(step.Name.value))
                try:
                    X = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.X, 'node')
                    Y = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Y, 'node')
                    Z = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Z, 'node')
                    #print('Retrieved U')
                    Material = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.MaterialIndex, 'node')
                    Element = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.ElementID, 'node')
                                    
                    Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Ux, 'node')
                    Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Uy, 'node')
                    Uz = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Uz, 'node')
                    Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Utot, 'node')
                    #print('Retrieved U')
                    PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUx, 'node')
                    PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUy, 'node')
                    PUz = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUz, 'node')
                    PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUtot, 'node')
                    #print('Retrieved dU')
                    U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.U1, 'node')
                    U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.U2, 'node')
                    U3 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.U3, 'node')
                    #print('Retrieved U1-U3')
                    N = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.N, 'node')
                    Q12 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Q12, 'node')
                    Q13 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Q13, 'node')
                    M2 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.M2, 'node')
                    M3 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.M3, 'node')
                    #print('Retrieved N')
                    Tskin = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Tskin, 'node')
                    Tlat= self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Tlat, 'node')
                    Tlat2= self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Tlat2, 'node')
                    
                    phaseName = []
                    phaseIdent = []
                    stepName = [] 
                    stepReached = []
                    counter = 0
                    
                    for x in range(len(X)): 
                        phaseName.append(phase.Name.value)
                        phaseIdent.append(phase.Identification.value)

                    w.rowsOut = [formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin,tlat,tlat2)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(phaseName, phaseIdent, X, Y, Z, Material, Element, Ux, Uy, Uz, Ut, PUx, PUy, PUz, PUt, U1, U2, U3, N, Q12, Q13, M2, M3, Tskin, Tlat, Tlat2)]                    
                    w.writeOutput()
                    msg = 'Retreived EmbeddedBeam results for ' + phase.Name.value  + '(embeddedbeam-' + phase.Identification.value +')' 
                    print(msg)
                    self.logger.info(msg)
                
                except Exception as e:
                    print ('Exception reading EmbeddedBeam results in phase' + phase.Name.value)
                    self.logger.error('...exception reading EmbeddedBeam results  '+ str(e))

                if not self.is_connected():
                    print ('Connection lost ')
                    self.logger.error('Connection lost ')
                    return Status.CONNECTION_LOST

        print('Exiting getBeamResults()')  
        return Status.ELEMENT_PROCESSED