from .PlaxisScripting import Status
from .Plaxis3dResults2023 import Plaxis3dResults2023
from .OutputWriter import GetWriter

class Plaxis3dResults2024 (Plaxis3dResults2023): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults2024, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3d2024"
def getBeamResultsBySteps(self,
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
        
        columns ='Phase,PhaseIdent,Step,Reached, MaterialID,ElementID,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN/m),Q12(kN/m),Q13(kN/m),M2(kNm/m),M3(kNm/m)'
        formats = '{},{},{},{},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
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
                    beamMat = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.MaterialIndex, 'node')
                    beamEl = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.ElementID, 'node') 
                    beamX = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.X, 'node')
                    beamY = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Y, 'node')
                    beamZ = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Z, 'node')
                    
                    beamUx = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Ux, 'node')
                    beamUy = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Uy, 'node')
                    beamUz = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Uz, 'node')
                    beamUt = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Utot, 'node')

                    beamPUx = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.PUx, 'node')
                    beamPUy = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.PUy, 'node')
                    beamPUz = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.PUz, 'node')
                    beamPUt = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.PUtot, 'node')

                    beamU1 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.U1, 'node')
                    beamU2 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.U2, 'node')
                    beamU3 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.U3, 'node')
                    
                    beamN = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.N, 'node')
                    beamQ12 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Q12, 'node')
                    beamQ13 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.Q13, 'node')
                    beamM2 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.M2, 'node')
                    beamM3 = self.g_o.getresults(step, self.g_o.ResultTypes.Beam.M3, 'node')
                    
                    phaseName = []
                    phaseIdent = []
                    stepName = [] 
                    stepReached = []
                    counter = 0
                    
                    for x in range(len(beamX)): 
                        phaseName.append(phase.Name.value)
                        phaseIdent.append(phase.Identification.value)
                        stepName.append(step.Name.value)
                        stepReached.append(step.Reached.SumMstage.value)
                        counter += 1 
                    w.rowsOut = [formats.format(pname, pident, sname, sreached, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                        for pname, pident, sname, sreached, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(phaseName, phaseIdent, stepName, stepReached, beamMat, beamEl, beamX, beamY, beamZ, beamUx, beamUy, beamUz, beamUt, beamPUx, beamPUy, beamPUz, beamPUt, beamU1, beamU2, beamU3, beamN, beamQ12, beamQ13, beamM2, beamM3)]
                    
                    w.writeOutput()
                    msg = "Retreived Beam results {} steps in phase {} ".format(phase.Name.value, counter) 
                    print(msg)
                    self.logger.info(msg)
                
                except Exception as e:
                    print ('Exception reading Beam results in phase' + phase.Name.value)
                    self.logger.error('...exception reading Beam results  '+ str(e))

                if not self.is_connected():
                    print ('Connection lost ')
                    self.logger.error('Connection lost ')
                    return Status.CONNECTION_LOST

        print('Exiting getBeamResults()')  
        return Status.ELEMENT_PROCESSED