
from plaxis.PlaxisRequests.PlaxisScripting import Status
from plaxis.PlaxisRequests.Plaxis3dResults2018 import Plaxis3dResults2018
from plaxis.PlaxisRequests.OutputWriter import GetWriter

class Plaxis3dResultsConnect (Plaxis3dResults2018): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResultsConnect, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3dConnect"
    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
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
      
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger)
               
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
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.MaterialID, 'node')
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
                        sphaseEnd=None
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
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:
            msg = 'Getting Plate results for {0} ({1})'.format(phase.Name.value, phase.Identification.value)
            print(msg)
            self.logger.info(msg)
            try: 
                
                X = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                Y = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                Z = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Z, 'node')
                
                Material = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialID, 'node')
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
                print ('Exception reading Plate in phase' + phase.Name.value)
                self.logger.error('...exception reading Plate results  '+ str(e))
            
            if not self.is_connected():
                print ('Connection lost ')
                self.logger.error('Connection lost ')
                return Status.CONNECTION_LOST
        
        print('getPlateResults Done')

    def getPlateResults2(self,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResults'  
        print('FileOut=', fileOut)

        # initialise data for lists
        pPhaseName = []
        pPhaseIdent = []
           
        pY = []
        pX = []
        pZ = []
        
        pMat = []
        pEl = []
               
        pUx = []
        pUy = []
        pUz = []
        pUt = []

        pPUx = []
        pPUy = []
        pPUz = []
        pPUt = []

        pU1 = []
        pU2 = []
        pU3 = []
        
        pM11 = []
        pM22 = []
        pM12 = []
        
        pQ12 = []
        pQ23 = [] 
        pQ13 = []
        
        pN1 = []
        pN2 = []



        for phase in self.phaseOrder:
            print('Getting Plate results for Phase ', phase.Name.value, phase.Identification.value)
            
            try: 
                plateX = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                plateY = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                plateZ = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Z, 'node')
                
                plateMat = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialID, 'node')
                plateEl = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')
                                
                plateUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Ux, 'node')
                plateUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uy, 'node')
                plateUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uz, 'node')
                plateUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Utot, 'node')

                platePUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUx, 'node')
                platePUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUy, 'node')
                platePUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUz, 'node')
                platePUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtot, 'node')

                plateU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U1, 'node')
                plateU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U2, 'node')
                plateU3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U3, 'node')
                
                plateN1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N11, 'node')
                plateN2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.N22, 'node')                
                plateQ12 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q12, 'node')
                plateQ23 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q23, 'node')
                plateQ13 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q13, 'node')
                plateM11 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M11, 'node')
                plateM22 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M22, 'node')
                plateM12 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M12, 'node')
                
                for x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(
                        plateX, plateY, plateZ, plateMat, plateEl, plateUx, plateUy, plateUz, plateUt, platePUx, platePUy, platePUz, platePUt, plateU1, plateU2, plateU3, plateN1, plateN2, plateQ12, plateQ23, plateQ13, plateM11, plateM22, plateM12):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    
                    pX.append(x)
                    pY.append(y)
                    pZ.append(z)
                    pMat.append(mat)
                    pEl.append (el)
                   
                    pUx.append(ux)
                    pUy.append(uy)
                    pUz.append(uz)
                    pUt.append(ut)
                    
                    pPUx.append(pux)
                    pPUy.append(puy)
                    pPUz.append(puz)
                    pPUt.append(put)
                   
                    pU1.append(u1)
                    pU2.append(u2)
                    pU3.append(u3)
                    
                    pN1.append(n1)
                    pN2.append(n2)
                    pQ12.append(q12)
                    pQ23.append(q23)
                    pQ13.append(q13)
                    pM11.append(m11)                    
                    pM22.append(m22)                  
                    pM12.append(m12) 
            except Exception as e:
                print ('Exception reading Plate in phase' + phase.Name.value)
                self.logger.error('...exception reading Plate results  '+ str(e))
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID, ElementID, Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N1(kN/m),N2(kN/m),Q12(kN/m),Q23(kN/m),Q13(kN/m),M11(kNm/m),M22(kNm/m),M12(kNm/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pEl, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pEl, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            print (self.columns)
            print (self.formats)
            print (self.types)
            for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pEl, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12):
                row= []
                row.append(pname) 
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(z)
                row.append(mat)
                row.append(el)
                row.append(ux)
                row.append(uy)
                row.append(uz)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(puz)
                row.append(put)
                row.append(u1)
                row.append(u2)
                row.append(u3)
                row.append(n1)
                row.append(n2)
                row.append(q12)
                row.append(q23)
                row.append(q13)
                row.append(m11)
                row.append(m22)
                row.append(m12)
                self.insertValues(row)
        
        print('getPlateResults Done')
      
    def getSoilResultsByPoints_Displacements(self,
                               filePoints=None,
                               fileOut=None,
                               tableOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
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
            
        phaseName = []
        phaseIdent = []
        
        locName = []
        locY = []
        locX = []
        locZ = []
       
        Uyy = []
        Uxx = []
        Uzz = []
        Utot = []
        
        PUyy = []
        PUxx = []
        PUzz = []
        PUtot = []
        
        Epsyy = []
        Epsxx = []
        Epszz = []

            
        for phase in self.phaseOrder:
            print(phase.Name.value)
    
            for pt in self.NodeList:
            
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
                
                if ux != 'not found':
                    print('results for ', phase.Name.value, pt.x, pt.y, pt.z ,' retrieved')
                
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                    locName.append (pt.name)
                    locX.append (pt.x)
                    locY.append (pt.y)
                    locZ.append (pt.z)
                                     
                    Uxx.append (ux)
                    Uyy.append (uy)
                    Uzz.append (uz)
                    Utot.append (utot)
                
                    PUxx.append (pux)
                    PUyy.append (puy)
                    PUzz.append (puz)
                    PUtot.append (putot)
                
                    Epsxx.append (ex)
                    Epsyy.append (ey)
                    Epszz.append (ez)
              
                
        columns='Phase,PhaseIdent,locName,locX(m),locY(m),locZ(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),Epsxx,Epsyy,Epszz'
        formats='{},{},{},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}'                
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pName, pIdent,locname, float(x), float(y), float(z), float(ux), float(uy), float(uz), float(utot), float(pux), float(puy), float(puz), float(putot), float(ex), float(ey), float(ez))
                for pName, pIdent, locname, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot, ex, ey, ez in zip(phaseName, phaseIdent, locName, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, Epsxx, Epsyy, Epszz)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pName, pIdent, locname, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot, ex, ey, ez in zip(phaseName, phaseIdent, locName, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, Epsxx, Epsyy, Epszz):
                row = []
                row.append(pName)
                row.append(pIdent)
                row.append(locname)
                row.append(x)
                row.append(y)
                row.append(z)
                row.append(ux)
                row.append(uy)
                row.append(uz)
                row.append(utot)
                row.append(pux)
                row.append(puy)
                row.append(puz)
                row.append(putot)
                row.append(ex)
                row.append(ey)
                row.append(ez)
                self.insertValues(row)
