
from .PlaxisScripting import Status
from .Plaxis3dResultsConnect import Plaxis3dResultsConnect
from .OutputWriter import GetWriter

class Plaxis3dResults2023 (Plaxis3dResultsConnect): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults2023, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3d2023"
    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  mode = 'new'
                                  ):
# file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_EmbeddedBeam.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getEmbeddedBeamResults'  
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,ElementID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN),Q12(kN),Q13(kN),M2(kNm),M3(kNm),Tskin(kN/m),Tlat(kN/m),Tlat2(kN/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
      
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        
        for phase in self.phaseOrder:

            msg = 'Getting EmbeddedBeam results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            
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
                print ('Exception reading EnbeddedBeam results in phase' + phase.Name.value)
                self.logger.error('...exception reading EmbeddedBeam results  '+ str(e))

            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST

        print('Exiting getEmbeddedBeamResults()')  
        return Status.ELEMENT_PROCESSED

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
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID, ElementID, Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N1(kN/m),N2(kN/m),Q12(kN/m),Q23(kN/m),Q13(kN/m),M11(kNm/m),M22(kNm/m),M12(kNm/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:
            msg = 'Getting Plate results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            try: 
                
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Z, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')
                                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uy, 'node')
                Uz = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uz, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUy, 'node')
                PUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUz, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U2, 'node')
                U3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U3, 'node')
                
                N11 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N11, 'node')
                N22 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N22, 'node')                
                Q12 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q12, 'node')
                Q23 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q23, 'node')
                Q13 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q13, 'node')
                M11 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M11, 'node')
                M22 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M22, 'node')
                M12 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M12, 'node')
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                w.rowsOut = [formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(phaseName, phaseIdent, X, Y, Z, Material, Element, Ux, Uy, Uz, Ut, PUx, PUy, PUz, PUt, U1, U2, U3, N11, N22, Q12, Q23, Q13, M11, M22, M12)]                    
                w.writeOutput()

            except Exception as e:
                print ('Exception reading Plate in phase' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Plate results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST
        
        print('Exiting getPlateResults()')
        return Status.ELEMENT_PROCESSED
    
    def getBeamResults(self,
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
            tableOut = 'getBeamResults'
           
        columns ='Phase,PhaseIdent,MaterialID,ElementID,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN/m),Q12(kN/m),Q13(kN/m),M2(kNm/m),M3(kNm/m)'
        formats = '{},{},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)
        
        for phase in self.phaseOrder:
        
            print('Getting Beam results for Phase ', phase.Name.value, phase.Identification.value)
            
            try: 
                beamMat = self.g_o.getresults(phase, self.g_o.Beam.Materialndex, 'node')
                beamEl = self.g_o.getresults(phase, self.g_o.Beam.ElementID, 'node') 
                beamX = self.g_o.getresults(phase, self.g_o.Beam.X, 'node')
                beamY = self.g_o.getresults(phase, self.g_o.Beam.Y, 'node')
                beamZ = self.g_o.getresults(phase, self.g_o.Beam.Z, 'node')
                
                beamUx = self.g_o.getresults(phase, self.g_o.Beam.Ux, 'node')
                beamUy = self.g_o.getresults(phase, self.g_o.Beam.Uy, 'node')
                beamUz = self.g_o.getresults(phase, self.g_o.Beam.Uz, 'node')
                beamUt = self.g_o.getresults(phase, self.g_o.Beam.Utot, 'node')

                beamPUx = self.g_o.getresults(phase, self.g_o.Beam.PUx, 'node')
                beamPUy = self.g_o.getresults(phase, self.g_o.Beam.PUy, 'node')
                beamPUz = self.g_o.getresults(phase, self.g_o.Beam.PUz, 'node')
                beamPUt = self.g_o.getresults(phase, self.g_o.Beam.PUtot, 'node')

                beamU1 = self.g_o.getresults(phase, self.g_o.Beam.U1, 'node')
                beamU2 = self.g_o.getresults(phase, self.g_o.Beam.U2, 'node')
                beamU3 = self.g_o.getresults(phase, self.g_o.Beam.U3, 'node')
                
                beamN = self.g_o.getresults(phase, self.g_o.Beam.N, 'node')
                beamQ12 = self.g_o.getresults(phase, self.g_o.Beam.Q12, 'node')
                beamQ13 = self.g_o.getresults(phase, self.g_o.Beam.Q13, 'node')
                beamM2 = self.g_o.getresults(phase, self.g_o.Beam.M2, 'node')
                beamM3 = self.g_o.getresults(phase, self.g_o.Beam.M3, 'node')
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                    
                w.rowsOut = [formats.format(pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                    for pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(phaseName, phaseIdent, beamMat, beamEl, beamX, beamY, beamZ, beamUx, beamUy, beamUz, beamUt, beamPUx, beamPUy, beamPUz, beamPUt, beamU1, beamU2, beamU3, beamN, beamQ12, beamQ13, beamM2, beamM3)]
                
                w.writeOutput()
                msg = 'Retreived Beam results for ' + phase.Name.value  + '(beam-' + phase.Identification.value +')' 
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
      
    def getSoilResultsByPoints_Displacements(self,
                               filePoints=None,
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
        
        if not filePoints is None:
            self.loadXYZNodeList(filePoints)
        
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByPoints_Displacements'  
        
        columns='Phase,PhaseIdent,locName,locX(m),locY(m),locZ(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),Epsxx,Epsyy,Epszz'
        formats='{},{},{},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}'                    
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)
                
        for phase in self.phaseOrder:
            phaseName = phase.Name.value
            phaseIdent = phase.Identification.value
            for pt in self.NodeList:
                try:
                    ux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Ux, (pt.x, pt.y, pt.z))
                    uy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Uy, (pt.x, pt.y, pt.z))
                    uz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Uz, (pt.x, pt.y, pt.z))
                    utot = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Utot, (pt.x, pt.y, pt.z))
                    
                    pux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUx, (pt.x, pt.y, pt.z))
                    puy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUy, (pt.x, pt.y, pt.z))
                    puz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUz, (pt.x, pt.y, pt.z))
                    putot = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUtot, (pt.x, pt.y, pt.z)) 
                    
                    ex = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Epsxx, (pt.x, pt.y, pt.z))
                    ey = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Epsyy, (pt.x, pt.y, pt.z))
                    ez = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Epszz, (pt.x, pt.y, pt.z))

                    w.rowsOut = [formats.format(phaseName, phaseIdent,pt.locname, float(pt.x), float(pt.y), float(pt.z), float(ux), float(uy), float(uz), float(utot), float(pux), float(puy), float(puz), float(putot), float(ex), float(ey), float(ez))]
                    w.writeOutput()
                except Exception as e:
                    msg = '...exception reading SoilResultsByPoints_Displacements results ' + phase.Identification.value
                    print (msg)
                    self.logger.error(msg + str(e))
        
        if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST

        print('Exiting SoilResultsByPoints_Displacements()')  
        return Status.ELEMENT_PROCESSED    

    def getInterfaceResults(self,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None, 
                        mode = 'new'
                        ):
            # file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_Interface.html
            
        self.setPhaseOrder(sphaseOrder,
            sphaseStart,
            sphaseEnd)
        
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResults' 
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)
        
        for phase in self.phaseOrder:
            msg = 'Getting Interface results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Z, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.MaterialIndex, 'node')
                            
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uy, 'node')
                Uz = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uz, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUy, 'node')
                PUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUz, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U2, 'node')
                U3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U3, 'node')
                
                InterfaceEffNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node')
                InterfaceTotNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, 'node')
                InterfaceShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node')
                InterfaceRelShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, 'node')

                PExcess = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PExcess, 'node')
                PActive = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PActive, 'node')
                PSteady = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PSteady, 'node')
                PWater = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PWater, 'node')
                
                Suction = self.g_o.getresults(phase,self.g_o.ResultTypes.Interface.Suction, 'node')
                EffSuction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.EffSuction, 'node')
                
                phaseName = []
                phaseIdent = []
            
                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                w.rowsOut = [formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                    for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                    in zip(phaseName, phaseIdent, X, Y, Z, Material, Ux, Uy, Uz, Ut, PUx, PUy, PUz, PUt, U1, U2, U3, InterfaceEffNormalStress, InterfaceTotNormalStress, InterfaceShearStress, InterfaceRelShearStress, PExcess, PActive, PSteady, PWater, Suction, EffSuction)]
                w.writeOutput()
                
                msg = 'Retreived Interface results for ' + phase.Name.value  + '(interface-' + phase.Identification.value +')' 
                print(msg)
                self.logger.info(msg)
                
            except Exception as e:
                print ('Exception reading interface results in phase' + phase.Name.value)
                self.logger.error('...exception reading Interface results  '+ str(e))

    
            if not self.is_connected():
                    print ('Connection lost ')
                    self.logger.error('Connection lost ')
                    return Status.CONNECTION_LOST

        print('Exiting getInterfaceResults()')  
        return Status.ELEMENT_PROCESSED
    
    def getNodeToNodeAnchorResults(self,
                                   fileOut=None,
                                   tableOut=None,
                                   sphaseOrder=None,
                                   sphaseStart=None,
                                   sphaseEnd=None,
                                   mode = 'new'
                                   ):
        #file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_NodeToNodeAnchor.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
            
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getNodeToNodeAnchorResults'  
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),U1(m),U2(m),U3(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'

        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Z, 'node')
                
                Mat = self.g_o.getresults(phase, self.g_o.ResultTypes.Node2NodeAnchor.MaterialIndex, 'node')
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Uy, 'node')
                Uz = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Uz, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUy, 'node')
                PUz = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUz, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U2, 'node')
                U3 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U3, 'node')
                
                Force3D = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForce3D, 'node')
                
                phaseName = []
                phaseIdent = []
            
                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                w.rowsOut = [formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(phaseName, phaseIdent, X, Y, Z, Mat, Ux, Uy, Uz, Ut, PUx, PUy, PUz, PUt, U1, U2, U3, Force3D)]
                w.writeOutput()
            
                msg = 'Retreived Node2NodeAnchor results for ' + phase.Name.value  + '(nodetonodeanchor-' + phase.Identification.value +')' 
                print(msg)
                self.logger.info(msg)
                
            except Exception as e:
                print ('Exception reading node2nodeanchor results in phase' + phase.Name.value)
                self.logger.error('...exception reading node2nodeanchor results  '+ str(e))

    
            if not self.is_connected():
                    print ('Connection lost ')
                    self.logger.error('Connection lost ')
                    return Status.CONNECTION_LOST

        print('Exiting getNode2NodeAnchoreResults()')  
        return Status.ELEMENT_PROCESSED
    
   
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 tableOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None, mode = 'new'
                                 ):
        # file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_FixedEndAnchor.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
                
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getFixedEndAnchorResults' 

        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),U1(m),U2(m),U3(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            
            try:
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Z, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.MaterialIndex, 'node')
                
                Ux = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Ux, 'node')
                Uy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Uy, 'node')
                Uz = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Uz, 'node')
                Ut = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Utot, 'node')

                PUx = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUx, 'node')
                PUy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUy, 'node')
                PUz = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUz, 'node')
                PUt = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUtot, 'node')

                U1 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U1, 'node')
                U2 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U2, 'node')
                U3 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U3, 'node')
                
                Force3D = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.AnchorForce3D, 'node')
                
                phaseName = []
                phaseIdent = []
            
                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)

                          
                w.rowsOut = [formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                        for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(phaseName, phaseIdent, X, Y, Z, Material, Ux, Uy, Uz, Ut, PUx, PUy, PUz, PUt, U1, U2, U3, Force3D)]
                
                w.writeOutput()
            
                msg = 'Retreived FixedEndAnchor results for ' + phase.Name.value  + '(nodetonodeanchor-' + phase.Identification.value +')' 
                print(msg)
                self.logger.info(msg)
                
            except Exception as e:
                print ('Exception reading fixedendanchor results in phase' + phase.Name.value)
                self.logger.error('...exception reading node2nodeanchor results  '+ str(e))

    
            if not self.is_connected():
                    print ('Connection lost ')
                    self.logger.error('Connection lost ')
                    return Status.CONNECTION_LOST

        print('Exiting getFixedEndAnchoreResults()')  
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
            tableOut = 'getPlateEnvelopeResults'  
        # with movements
        # columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID, ElementID, Ux_max(m),Ux_min(m),Uy_max(m),Uy_min(m),Uz_max(m),Uz_min(m),Utot_max(m),PUx_max(m),PUx_min(m),PUy_max(m),PUy_min(m),PUz_max(m),PUz_min(m),PUt_max(m),N11_max(kN/m),N11_min(kN/m),N22_max(kN/m),N22_max(kN/m),Q12_max(kN/m),Q12_min(kN/m),Q23_max(kN/m),Q23_min(kN/m),Q13_max(kN/m),Q13_min(kN/m),M11_max(kNm/m),M11_min(kNm/m),M12_max(kNm/m),M12_min(kNm/m),M22_max(kNm/m),M22_min(kN/m)'
        # formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        # without movements
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,ElementID,N11_max(kN/m),N11_min(kN/m),N22_max(kN/m),N22_max(kN/m),Q12_max(kN/m),Q12_min(kN/m),Q23_max(kN/m),Q23_min(kN/m),Q13_max(kN/m),Q13_min(kN/m),M11_max(kNm/m),M11_min(kNm/m),M12_max(kNm/m),M12_min(kNm/m),M22_max(kNm/m),M22_min(kN/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
       
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:
            msg = 'Getting Plate results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            try: 
                
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Z, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialIndex, 'node')
                Element = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')
                
                # movement envelopes not reported in PLaxis3d 2023                
                # Ux_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UxMin, 'node')  
                # Ux_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UxMax, 'node')
                
                # Uy_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UyMin, 'node')
                # Uy_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UyMax, 'node')
                
                # Uz_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UzMin, 'node')
                # Uz_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UzMax, 'node')

                # Ut_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.UtotMax, 'node')

                # PUx_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUxMin, 'node')
                # PUx_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUxMax, 'node')

                # PUy_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUyMin, 'node')
                # PUy_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUyMax, 'node')
                
                # PUz_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUzMin, 'node')
                # PUz_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUzMax, 'node')

                # PUt_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtotMax, 'node')

                N11_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N11_EnvelopeMax, 'node')
                N11_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N11_EnvelopeMin, 'node')
                
                N22_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N22_EnvelopeMax, 'node')
                N22_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N22_EnvelopeMin, 'node')
                     
                Q12_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q12_EnvelopeMax, 'node')
                Q12_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q12_EnvelopeMin, 'node')
                
                Q13_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q13_EnvelopeMax, 'node')
                Q13_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q13_EnvelopeMin, 'node')
                
                Q23_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q23_EnvelopeMax, 'node')
                Q23_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q23_EnvelopeMin, 'node')
                
                M11_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M11_EnvelopeMax, 'node')
                M11_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M11_EnvelopeMin, 'node')
                
                M22_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M22_EnvelopeMax, 'node')
                M22_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M22_EnvelopeMin, 'node')
                
                M12_max = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M12_EnvelopeMax, 'node')
                M12_min = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M12_EnvelopeMin, 'node')
               
                
                phaseName = []
                phaseIdent = []

                for x in range(len(X)): 
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                # with movements 
                # w.rowsOut = [formats.format(pname, pident, x, y, z, material, element, ux_max, ux_min, uy_max, uy_min, uz_max, uz_min, ut_max, pux_max, pux_min, puy_max, puy_min, puz_max, puz_min, put_max, n11_max, n11_min, n22_max, n22_min, q12_max, q12_min, q23_max, q23_min, q13_max, q13_min, m11_max, m11_min, m12_max, m12_min, m22_max, m22_min)
                #                         for pname, pident, x, y, z, material, element, ux_max, ux_min, uy_max, uy_min, uz_max, uz_min, ut_max, pux_max, pux_min, puy_max, puy_min, puz_max, puz_min, put_max, n11_max, n11_min, n22_max, n22_min, q12_max, q12_min, q23_max, q23_min, q13_max, q13_min, m11_max, m11_min, m12_max, m12_min, m22_max, m22_min in 
                #                 zip(phaseName, phaseIdent, X, Y, Z, Material, Element, Ux_max, Ux_min, Uy_max, Uy_min, Uz_max, Uz_min, Ut_max, PUx_max, PUx_min, PUy_max, PUy_min, PUz_max, PUz_min, PUt_max, N11_max, N11_min, N22_max, N22_min, Q12_max, Q12_min, Q23_min, Q23_min, Q13_max, Q13_min, M11_max, M11_min, M12_max, M12_min, M22_max, M22_min)]                    
                
                # without movements
                w.rowsOut = [formats.format(pname, pident, x, y, z, material, element, n11_max, n11_min, n22_max, n22_min, q12_max, q12_min, q23_max, q23_min, q13_max, q13_min, m11_max, m11_min, m12_max, m12_min, m22_max, m22_min)
                                        for pname, pident, x, y, z, material, element, n11_max, n11_min, n22_max, n22_min, q12_max, q12_min, q23_max, q23_min, q13_max, q13_min, m11_max, m11_min, m12_max, m12_min, m22_max, m22_min in 
                                zip(phaseName, phaseIdent, X, Y, Z, Material, Element, N11_max, N11_min, N22_max, N22_min, Q12_max, Q12_min, Q23_max, Q23_min, Q13_max, Q13_min, M11_max, M11_min, M12_max, M12_min, M22_max, M22_min)]                    

                w.writeOutput()

            except Exception as e:
                print ('Exception reading PlateEnvelopeResults in phase' + phase.Identification.value + str(e))
                self.logger.error('...exception reading PlateEnvelope results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST
        
        print('Exiting getPlateEnvelopeResults()')
        return Status.ELEMENT_PROCESSED