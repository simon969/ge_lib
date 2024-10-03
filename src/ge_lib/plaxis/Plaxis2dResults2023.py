from .PlaxisScripting import Status
from .Plaxis2dResults2019 import Plaxis2dResults2019
from .OutputWriter import GetWriter


class Plaxis2dResults2023(Plaxis2dResults2019):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResults2023, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2d2023"
    
    def getPlateResults(self,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None,
                    mode = 'new'
                    ):

        self.setPhaseOrder(sphaseOrder,
                            sphaseStart,
                            sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResults'
        
        columns ='Phase,PhaseIdent,X(m),Y(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Nx2D(kN/m),Nz2D(kN/m),Q2D(kN/m),M2D(kNm/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
                
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:
            print('Getting Plate results ' + phase.Identification.value)
            
            try: 
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')      
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uy, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUy, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U2, 'node')

                M2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M2D, 'node')
                Q2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q2D, 'node')
                Nx2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nx2D, 'node')
                Nz2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nz2D, 'node')
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, nx2d, nz2d, q2d, m2d)
                                    for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, nx2d, nz2d, q2d, m2d in zip(phaseName, phaseIdent, X, Y, Material, Element, Ux, Uy, Ut, PUx, PUy, PUt, U1, U2, Nx2D, Nz2D, Q2D, M2D)]                    
                w.writeOutput()

                    
            except Exception as e:
                print ('...exception reading Plate results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Plate results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST    
            
        print('getPlateResults Done')
        return Status.ELEMENT_PROCESSED

    def getPlateEnvelopeResults(self,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None,
                        mode = 'new'
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResults'
        
        columns ='Phase,PhaseIdent,X(m),Y(m),MaterialID,ElementID,Ux_max(m),Ux_min(m),Uy_max(m),Uy_min(m),Utot_max(m),PUx_max(m),PUx_min(m),PUy_max(m),PUy_min(m),PUt_max(m),Nx2D_max(kN/m),Nx2D_min(kN/m),Nz2D_max(kN/m),Nz2D_min(kN/m),Q2D_max(kN/m),Q2D_min(kN/m),M2D_max(kNm/m),M2D_min(kNm/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
       
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)
    
        for phase in self.phaseOrder:
            print('Getting Plate results ' + phase.Identification.value)
            
            try: 
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')      
                
                Ux_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UxMin, 'node')  
                Ux_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UxMax, 'node')
                
                Uy_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UyMin, 'node')
                Uy_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UyMax, 'node')
                
                Ut_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UtotMax, 'node')

                PUx_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUxMin, 'node')
                PUx_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUxMax, 'node')

                PUy_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUyMin, 'node')
                PUy_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUyMax, 'node')

                PUt_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtotMax, 'node')

                M2D_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M_EnvelopeMax2D, 'node')
                M2D_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M_EnvelopeMin2D, 'node')
                
                Q2D_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q_EnvelopeMax2D, 'node')
                Q2D_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q_EnvelopeMin2D, 'node')
                
                Nx2D_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nx_EnvelopeMax2D, 'node')
                Nx2D_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nx_EnvelopeMin2D, 'node')
                
                Nz2D_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nz_EnvelopeMax2D, 'node')
                Nz2D_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nz_EnvelopeMin2D, 'node')

                print('...read Plate Envelope results ' + phase.Identification.value)
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux_max, ux_min, uy_max, uy_min, ut_max, pux_max, pux_min, puy_max, puy_min, put_max, nx2d_max, nx2d_min, nz2d_max, nz2d_min, q2d_max, q2d_min, m2d_max, m2d_min)
                                 for pname, pident, x, y, mat, el, ux_max, ux_min, uy_max, uy_min, ut_max, pux_max, pux_min, puy_max, puy_min, put_max, nx2d_max, nx2d_min, nz2d_max, nz2d_min, q2d_max, q2d_min, m2d_max, m2d_min 
                                 in zip(phaseName, phaseIdent, X, Y, Material, Element, Ux_max, Ux_min, Uy_max, Uy_min, Ut_max, PUx_max, PUx_min, PUy_max, PUy_min, PUt_max, Nx2D_max, Nx2D_min, Nz2D_max, Nz2D_min, Q2D_max, Q2D_min, M2D_max, M2D_min)]                    
                w.writeOutput()

                    
            except Exception as e:
                print ('...exception reading Plate Envelope results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Plate Envelope results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST    
         
        print('getPlateEmvelopeResults Done')
        return Status.ELEMENT_PROCESSED
    
    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  mode = 'new'
                                  ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getEmbeddedBeamResults'

        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)
        
        for phase in self.phaseOrder:

            msg = 'Getting Embeddedbeam results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.MaterialIndex, 'node')
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
    
    def getInterfaceResults(self,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None,
                    mode = 'new'
                    ):
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResults'
        
        columns = "Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)"
        formats = "{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}"
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Y, 'node')
              
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.ElementID, 'node')
              
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uy, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUy, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U2, 'node')

                EffNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node')
                TotNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, 'node')
                ShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node')
                RelShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, 'node')

                PExcess = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PExcess, 'node')
                PActive = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PActive, 'node')
                PSteady = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PSteady, 'node')
                PWater = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PWater, 'node')
                
                Suction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Suction, 'node')
                EffSuction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.EffSuction, 'node')
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                                    phaseName, phaseIdent,
                                    X, Y, Material, Element, 
                                    Ux, Uy, Ut, 
                                    PUx, PUy, PUt, 
                                    U1, U2, 
                                    EffNormalStress, TotNormalStress, ShearStress, RelShearStress,
                                    PExcess, PActive, PSteady, PWater, 
                                    Suction,  EffSuction)]
                w.writeOutput()
            except Exception as e:
                print ('Exception reading Interface results in phase' + phase.Name.value)
                self.logger.error('...exception reading Interface results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST    
        
        print('getInterfaceResults Done')  
        return Status.ELEMENT_PROCESSED
    
    def getNodeToNodeAnchorResults(self,
                                   fileOut=None,
                                   tableOut=None,
                                   sphaseOrder=None,
                                   sphaseStart=None,
                                   sphaseEnd=None, 
                                   mode = 'new'
                                   ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getNodeToNodeAnchorResults'
       
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'    

        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)

            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.ElementID, 'node')
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Uy, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUy, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U2, 'node')

                Force2D = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node')

                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, force2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, force2d in zip(phaseName, phaseIdent, X, Y, Material, Element, Ux, Uy, Ut, PUx, PUy, PUt, U1, U2, Force2D)]                    
                w.writeOutput()

            except Exception as e:
                print ('Exception reading NodeToNodeAnchor results in phase' + phase.Name.value)
                self.logger.error('...exception reading NodeToNodeAnchor results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST           
        print('getNodeToNodeAnchorResults Done')
        return Status.ELEMENT_PROCESSED
    
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 tableOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None,
                                 mode = 'new'
                                 ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getFixedEndAnchorResults'
        
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)


        for phase in self.phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Y, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.ElementID, 'node')
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Uy, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUy, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U2, 'node')

                Force2D = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.AnchorForce2D, 'node')
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                w.rowsOut = [formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, force2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, force2d in zip(phaseName, phaseIdent, X, Y, Material, Element, Ux, Uy, Ut, PUx, PUy, PUt, U1, U2, Force2D)]                    
                w.writeOutput()

            except Exception as e:
                print ('Exception reading NodeToNodeAnchor results in phase' + phase.Name.value)
                self.logger.error('...exception reading NodeToNodeAnchor results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST 
                    
        print('getFixedEndAnchorResults Done')
        return Status.ELEMENT_PROCESSED