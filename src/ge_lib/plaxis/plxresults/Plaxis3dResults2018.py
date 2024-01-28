

from ge_lib.plaxis.plxresults.PlaxisResults import Plaxis3dResults

class Plaxis3dResults2018 (Plaxis3dResults):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults2018, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3d2018"
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
                plateX = self.g_o.getresults(phase, self.g_o.Plate.X, 'node')
                plateY = self.g_o.getresults(phase, self.g_o.Plate.Y, 'node')
                plateZ = self.g_o.getresults(phase, self.g_o.Plate.Z, 'node')
                
                plateMat = self.g_o.getresults(phase, self.g_o.Plate.MaterialID, 'node')
                plateEl = self.g_o.getresults(phase, self.g_o.Plate.ElementID, 'node')
                                
                plateUx = self.g_o.getresults(phase, self.g_o.Plate.Ux, 'node')
                plateUy = self.g_o.getresults(phase, self.g_o.Plate.Uy, 'node')
                plateUz = self.g_o.getresults(phase, self.g_o.Plate.Uz, 'node')
                plateUt = self.g_o.getresults(phase, self.g_o.Plate.Utot, 'node')

                platePUx = self.g_o.getresults(phase, self.g_o.Plate.PUx, 'node')
                platePUy = self.g_o.getresults(phase, self.g_o.Plate.PUy, 'node')
                platePUz = self.g_o.getresults(phase, self.g_o.Plate.PUz, 'node')
                platePUt = self.g_o.getresults(phase, self.g_o.Plate.PUtot, 'node')

                plateU1 = self.g_o.getresults(phase, self.g_o.Plate.U1, 'node')
                plateU2 = self.g_o.getresults(phase, self.g_o.Plate.U2, 'node')
                plateU3 = self.g_o.getresults(phase, self.g_o.Plate.U3, 'node')
                
                plateN1 = self.g_o.getresults(phase, self.g_o.Plate.N11, 'node')
                plateN2 = self.g_o.getresults(phase, self.g_o.Plate.N22, 'node')                
                plateQ12 = self.g_o.getresults(phase, self.g_o.Plate.Q12, 'node')
                plateQ23 = self.g_o.getresults(phase, self.g_o.Plate.Q23, 'node')
                plateQ13 = self.g_o.getresults(phase, self.g_o.Plate.Q13, 'node')
                plateM11 = self.g_o.getresults(phase, self.g_o.Plate.M11, 'node')
                plateM22 = self.g_o.getresults(phase, self.g_o.Plate.M22, 'node')
                plateM12 = self.g_o.getresults(phase, self.g_o.Plate.M12, 'node')
                
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
        
    def getBeamResults(self,
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
            tableOut = 'getBeamResults'
        print('FileOut=', fileOut)

        # initialise data for lists
        bPhaseName = []
        bPhaseIdent = []
           
        bMat = []
        bEl =[]
        bY = []
        bX = []
        bZ = []
        
        bUx = []
        bUy = []
        bUz = []
        bUt = []

        bPUx = []
        bPUy = []
        bPUz = []
        bPUt = []

        bU1 = []
        bU2 = []
        bU3 = []
        
        bM2 = []
        bM3 = []
        
        bQ12 = []
        bQ13 = [] 
        
        bN = []
      

        for phase in self.phaseOrder:
            print('Getting Beam results for Phase ', phase.Name.value, phase.Identification.value)
            
            try: 
                beamMat = self.g_o.getresults(phase, self.g_o.Beam.MaterialID, 'node')
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
                     
                for mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(
                        beamMat, beamEl, beamX, beamY, beamZ, beamUx, beamUy, beamUz, beamUt, beamPUx, beamPUy, beamPUz, beamPUt, beamU1, beamU2, beamU3, beamN, beamQ12, beamQ13, beamM2, beamM3):
                    # print ('YUt') 
                    
                    # add filters in here if necessary
                    bPhaseName.append(phase.Name.value)
                    bPhaseIdent.append(phase.Identification.value)
                    
                    bMat.append(mat)
                    bEl.append(el)
                    bX.append(x)
                    bY.append(y)
                    bZ.append(z)
                                     
                    bUx.append(ux)
                    bUy.append(uy)
                    bUz.append(uz)
                    bUt.append(ut)
              
                    bPUx.append(pux)
                    bPUy.append(puy)
                    bPUz.append(puz)
                    bPUt.append(put)
                   
                    bU1.append(u1)
                    bU2.append(u2)
                    bU3.append(u3)
                    
                    bN.append(n)
                    
                    bQ12.append(q12)
                    bQ13.append(q13)
                    
                    bM2.append(m2)                    
                    bM3.append(m3)                  
                     
            except:
                print ('Exception reading beam in phase' + phase.Name.value)

        columns ='Phase,PhaseIdent,MaterialID,ElementID,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN/m),Q12(kN/m),Q13(kN/m),M2(kNm/m),M3(kNm/m)'
        formats = '{},{},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                                 for pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bEl, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                                 for pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bEl, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, mat, el, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bEl, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3):
                row= []
                row.append(pname) 
                row.append(pident)
                row.append(mat)
                row.append(el)
                row.append(x)
                row.append(y)
                row.append(z)
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
                row.append(n)
                row.append(q12)
                row.append(q13)
                row.append(m2)
                row.append(m3)
                self.insertValues(row)
        
        print('getBeamResults Done')

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
        
        print('FileOut=', fileOut)

        # init data for lists
        PhaseName = []
        PhaseIdent = []
           
        eY = []
        eX = []
        eZ = []
        
        eMat = []
        eEl = []
        
        eUx = []
        eUy = []
        eUz = []
        eUt = []

        ePUx = []
        ePUy = []
        ePUz = []
        ePUt = []

        eU1 = []
        eU2 = []
        eU3 = []
        
        eN = []
        eQ12 = []
        eQ13 = []
        eM2 = []
        eM3 = []

        eTskin = []
        eTlat = []
        eTlat2 = []
        eFfoot = []
        
        for phase in self.phaseOrder:

            print('Getting EmbeddedBeam results for Phase ',  phase.Name.value)
            
            try:
                embeamX = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.X, 'node')
                embeamY = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Y, 'node')
                embeamZ = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Z, 'node')
                #print('Retrieved U')
                ebeamMat = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.MaterialID, 'node')
                ebeamEl = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.ElementID, 'node')
                                
                embeamUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Ux, 'node')
                embeamUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Uy, 'node')
                embeamUz = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Uz, 'node')
                embeamUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Utot, 'node')
                #print('Retrieved U')
                embeamPUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUx, 'node')
                embeamPUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUy, 'node')
                embeamPUz = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUz, 'node')
                embeamPUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUtot, 'node')
                #print('Retrieved dU')
                embeamU1 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.U1, 'node')
                embeamU2 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.U2, 'node')
                embeamU3 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.U3, 'node')
                #print('Retrieved U1-U3')
                embeamN = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.N, 'node')
                embeamQ12 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Q12, 'node')
                embeamQ13 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Q13, 'node')
                embeamM2 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.M2, 'node')
                embeamM3 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.M3, 'node')
                #print('Retrieved N')
                embeamTskin = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tskin, 'node')
                embeamTlat= self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tlat, 'node')
                embeamTlat2= self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tlat2, 'node')
                #embeamFfoot= self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tlat2, 'node')
                
                print('Retrieved EmbeddedBeam results for ', phase.Name.value)
                
                for x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(
                        embeamX, embeamY, embeamZ, ebeamMat, ebeamEl, embeamUx, embeamUy, embeamUz, embeamUt, embeamPUx, embeamPUy,  embeamPUz, embeamPUt, embeamU1, embeamU2, embeamU3, embeamN, embeamQ12, embeamQ13, embeamM2, embeamM3, embeamTskin, embeamTlat, embeamTlat2):
                    # add filters in here if necessary
                    PhaseName.append(phase.Name.value)
                    PhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eZ.append(z)
                    eMat.append(mat)
                    eEl.append(el)
                    eUx.append(ux)
                    eUy.append(uy)
                    eUz.append(uz)
                    eUt.append(ut)
                    ePUx.append(pux)
                    ePUy.append(puy)
                    ePUz.append(puz)
                    ePUt.append(put)
                    eU1.append(u1)
                    eU2.append(u2)
                    eU3.append(u3)
                    eN.append(n)  
                    eQ12.append(q12)
                    eQ13.append(q13)
                    eM2.append(m2)
                    eM3.append(m3)
                    eTskin.append(tskin)
                    eTlat.append(tlat)
                    eTlat2.append(tlat2)
            except:
                print ('Exception reading EmbeddedBeam in phase' + phase.Name.value)
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,ElementID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN),Q12(kN),Q13(kN),M2(kNm),M3(kNm),Tskin(kN/m),Tlat(kN/m),Tlat2(kN/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eEl, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2)
                                 for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eEl, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, z, mat, el, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eEl, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2):
                row = []        
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
                row.append(n)
                row.append(q12)
                row.append(q13)
                row.append(m2)
                row.append(m3)
                row.append(tskin)
                row.append(tlat)
                row.append(tlat2)
                self.insertValues(row)
                
        print('getEmbeddedBeamResults Done')
        
    def getInterfaceResults(self,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
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
        print('FileOut=', fileOut)
        
        # initialize data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []
        iZ = []
        
        iMat = []
               
        iUx = []
        iUy = []
        iUz = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUz = []
        iPUt = []

        iU1 = []
        iU2 = []
        iU3 = []
        
        iEffNormalStress = []
        iTotNormalStress = []
        iShearStress = []
        iRelShearStress = []

        iPExcess = []
        iPActive = []
        iPSteady = []
        iPWater = []
        
        iSuction = []
        iEffSuction = []

        for phase in self.phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            try:
                interX = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.X, 'node')
                interY = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Y, 'node')
                interZ = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Z, 'node')
                
                interMat = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.MaterialID, 'node')
                               
                interUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Ux, 'node')
                interUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uy, 'node')
                interUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uz, 'node')
                interUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Utot, 'node')

                interPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUx, 'node')
                interPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUy, 'node')
                interPUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUz, 'node')
                interPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUtot, 'node')

                interU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U1, 'node')
                interU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U2, 'node')
                interU3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U3, 'node')
                
                interEffNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node')
                interRelShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PExcess, 'node')
                interPActive = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PActive, 'node')
                interPSteady = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PSteady, 'node')
                interPWater = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PWater, 'node')
                
                interSuction = self.g_o.getresults(phase,self.g_o.ResultTypes.Interface.Suction, 'node')
                interEffSuction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.EffSuction, 'node')

                for x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, interZ, interMat, 
                        interUx, interUy, interUz, interUt, 
                        interPUx, interPUy, interPUz, interPUt, 
                        interU1, interU2, interU3,
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    
                    iX.append(x)
                    iY.append(y)
                    iZ.append(z)
                    
                    iMat.append(mat)
                                        
                    iUx.append(ux)
                    iUy.append(uy)
                    iUz.append(uz)
                    iUt.append(ut)
                    
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUz.append(puz)
                    iPUt.append(put)
                    
                    iU1.append(u1)
                    iU2.append(u2)
                    iU3.append(u3)
                     
                    iEffNormalStress.append(ens)
                    iTotNormalStress.append(tns)
                    iShearStress.append(ss)
                    iRelShearStress.append(rss)
                    iPExcess.append(pe)
                    iPActive.append(pa)
                    iPSteady.append(pst)
                    iPWater.append(pw)
                    iSuction.append(su)
                    iEffSuction.append(esu)
            
            except Exception as e:
                msg = '...exception reading interface results ' + phase.Identification.value
                print (msg)
                self.logger.error(msg + str(e))
                    
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                in zip(iPhaseName, iPhaseIdent, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                in zip(iPhaseName, iPhaseIdent, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(z)
                row.append(mat)
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
                row.append(ens)
                row.append(tns)
                row.append(ss)
                row.append(rss)
                row.append(pe)
                row.append(pa)
                row.append(pst)
                row.append(pw)
                row.append(su)
                row.append(esu)
                self.insertValues(row)
                
        print('getInterfaceResults Done') 
        
    def getInterfaceResultsByPoints(self,
                    filePoints=None,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
                        
        if self.phaseOrder is None:
            self.setPhaseOrder(sphaseOrder,
                               sphaseStart,
                               sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1


        if not filePoints is None:
            self.loadXYZNodeList(filePoints)


        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResultsByPoints'  

        print('FileOut=', fileOut)

        # initialize data for lists
        iPhaseName = []
        iPhaseIdent = []

        iLocName = []

        iY = []
        iX = []
        iZ = []

        iMat = []
               
        iUx = []
        iUy = []
        iUz = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUz = []
        iPUt = []

        iU1 = []
        iU2 = []
        iU3 = []

        iEffNormalStress = []
        iTotNormalStress = []
        iShearStress = []
        iRelShearStress = []

        iPExcess = []
        iPActive = []
        iPSteady = []
        iPWater = []

        iSuction = []
        iEffSuction = []

        for phase in self.phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            
            for pt in self.NodeList:
            
                try:
                    x = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.X, (pt.x, pt.y, pt.z))
                    y = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Y, (pt.x, pt.y, pt.z))
                    z = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Z, (pt.x, pt.y, pt.z))
                    mat = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.MaterialID,  (pt.x, pt.y, pt.z))
                                   
                    ux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Ux, (pt.x, pt.y, pt.z))
                    uy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Uy, (pt.x, pt.y, pt.z))
                    uz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Uz, (pt.x, pt.y, pt.z))
                    ut = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Utot, (pt.x, pt.y, pt.z))

                    pux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PUx, (pt.x, pt.y, pt.z))
                    puy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PUy, (pt.x, pt.y, pt.z))
                    puz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PUz, (pt.x, pt.y, pt.z))
                    put = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PUtot, (pt.x, pt.y, pt.z))

                    u1 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.U1, (pt.x, pt.y, pt.z))
                    u2 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.U2, (pt.x, pt.y, pt.z))
                    u3 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.U3, (pt.x, pt.y, pt.z))
                    
                    ens = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, (pt.x, pt.y, pt.z))
                    tns = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, (pt.x, pt.y, pt.z))
                    ss = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.InterfaceShearStress, (pt.x, pt.y, pt.z))
                    rss = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, (pt.x, pt.y, pt.z))

                    pe = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PExcess, (pt.x, pt.y, pt.z))
                    pa = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PActive, (pt.x, pt.y, pt.z))
                    pst = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PSteady, (pt.x, pt.y, pt.z))
                    pw = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.PWater, (pt.x, pt.y, pt.z))
                    
                    su = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.Suction, (pt.x, pt.y, pt.z))
                    esu = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Interface.EffSuction, (pt.x, pt.y, pt.z))
                    
                    if ux == 'not found':
                        print('results for ', phase.Name.value, pt.name, pt.x, pt.y, pt.z ,' not found')
                    if ux != 'not found':
                        print('results for ', phase.Name.value, pt.name, pt.x, pt.y, pt.z ,' retrieved')
                        # add filters in here if necessary
                        iPhaseName.append(phase.Name.value)
                        iPhaseIdent.append(phase.Identification.value)
                        
                        iX.append(x)
                        iY.append(y)
                        iZ.append(z)
                        
                        iMat.append(mat)
                        iLocName.append (pt.name)
                        
                        iUx.append(ux)
                        iUy.append(uy)
                        iUz.append(uz)
                        iUt.append(ut)
                        
                        iPUx.append(pux)
                        iPUy.append(puy)
                        iPUz.append(puz)
                        iPUt.append(put)
                        
                        iU1.append(u1)
                        iU2.append(u2)
                        iU3.append(u3)
                         
                        iEffNormalStress.append(ens)
                        iTotNormalStress.append(tns)
                        iShearStress.append(ss)
                        iRelShearStress.append(rss)
                        iPExcess.append(pe)
                        iPActive.append(pa)
                        iPSteady.append(pst)
                        iPWater.append(pw)
                        iSuction.append(su)
                        iEffSuction.append(esu)
                        
                except:
                    print ('Exception reading Interface results in phase' + phase.Name.value)

        columns ='Phase,PhaseIdent,LocName,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)'
        formats = '{},{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, loc, float(x), float(y), float(z), float(mat), float(ux), float(uy), float(uz), float(ut), float(pux), float(puy), float(puz), float(put), float(u1), float(u2),float(u3), float(ens), float(tns), float(ss), float(rss), float(pe), float(pa), float(pst), float(pw), float(su), float(esu))
                for pname, pident, loc, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            
            #~ print(iLocName)
            #~ print(iPhaseName)
            #~ print(iPhaseIdent)
            #~ print(iX)
            #~ print(iY)
            #~ print(iZ)
            #~ print(iMat)
            
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, loc, float(x), float(y), float(z), float(mat), float(ux), float(uy), float(uz), float(ut), float(pux), float(puy), float(puz), float(put), float(u1), float(u2),float(u3), float(ens), float(tns), float(ss), float(rss), float(pe), float(pa), float(pst), float(pw), float(su), float(esu))
                for pname, pident, loc, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
       
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, loc, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iZ, iMat, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(loc)
                row.append(x)
                row.append(y)
                row.append(z)
                row.append(mat)
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
                row.append(ens)
                row.append(tns)
                row.append(ss)
                row.append(rss)
                row.append(pe)
                row.append(pa)
                row.append(pst)
                row.append(pw)
                row.append(su)
                row.append(esu)
                self.insertValues(row)

        print('getInterfaceResultsByPoints Done')     

