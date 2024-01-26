from plaxis.PlaxisRequests.PlaxisScripting import Status
from plaxis.PlaxisRequests.Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2
from plaxis.PlaxisRequests.OutputWriter import GetWriter


class Plaxis2dResultsConnectV22(Plaxis2dResultsConnectV2):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResultsConnectV22, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2dConnectV22"

    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getEmbeddedBeamResults'

        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger)
               
        print('FileOut=', w.fileOut)
        
        for phase in self.phaseOrder:

            msg = 'Getting Embeddedbeam results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.MaterialID, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.ElementID, 'node')
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Uy, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Utot, 'node')
                
                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUy, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.PUtot, 'node')
                 
                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.U2, 'node')

                M2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.M2D, 'node')
                Q2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Q2D, 'node')
                Nx2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Nx2D, 'node')
                Nz2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Nz2D, 'node')

                Tskin = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Tskin, 'node')
                Tlat= self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Tlat, 'node')
                     
                print ('Retrieved EmbeddedBeam results ' + phase.Identification.value)
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(phaseName, phaseIdent, X, Y, Material, Element, Ux, Uy, Ut, PUx, PUy, PUt, U1, U2, M2D, Q2D, Nx2D, Nz2D, Tskin, Tlat)]                    
                w.writeOutput()

            except Exception as e:
                print ('Exception reading EnbeddedBeam results in phase' + phase.Name.value)
                self.logger.error('...exception reading EmbeddedBeam results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST   
                
        print('getEmbeddedBeamResults Done')   
        return Status.ELEMENT_PROCESSED