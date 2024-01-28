from .Plaxis2dResults import Plaxis2dResults

class Plaxis2dResults2016 (Plaxis2dResults):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResults2016, self).__init__(server, host, port, password=password)
    def version (self):
        return "Plaxis2d2016"

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

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResults'
        
        # init data for lists
        pPhaseName = []
        pPhaseIdent = []
           
        pY = []
        pX = []
        
        pMat = []
          
        pUx = []
        pUy = []
        pUt = []

        pPUx = []
        pPUy = []
        pPUt = []

        pU1 = []
        pU2 = []

        pM2D = []
        pQ2D = []
        pNx2D = []
        pNz2D = []



        for phase in self.phaseOrder:
            print('Getting Plate results ' + phase.Identification.value)
            
            try: 
                plateX = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                plateY = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                
                plateMat = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialID, 'node')
                      
                plateUx = self.g_o.getresults(phase, self.g_o.Plate.Ux, 'node')
                plateUy = self.g_o.getresults(phase, self.g_o.Plate.Uy, 'node')
                plateUt = self.g_o.getresults(phase, self.g_o.Plate.Utot, 'node')

                platePUx = self.g_o.getresults(phase, self.g_o.Plate.PUx, 'node')
                platePUy = self.g_o.getresults(phase, self.g_o.Plate.PUy, 'node')
                platePUt = self.g_o.getresults(phase, self.g_o.Plate.PUtot, 'node')

                plateU1 = self.g_o.getresults(phase, self.g_o.Plate.U1, 'node')
                plateU2 = self.g_o.getresults(phase, self.g_o.Plate.U2, 'node')

                plateM2D = self.g_o.getresults(phase, self.g_o.Plate.M2D, 'node')
                plateQ2D = self.g_o.getresults(phase, self.g_o.Plate.Q2D, 'node')
                plateNx2D = self.g_o.getresults(phase, self.g_o.Plate.Nx2D, 'node')
                plateNz2D = self.g_o.getresults(phase, self.g_o.Plate.Nz2D, 'node')
                
                print('...read Plate results ' + phase.Identification.value)
                
                for x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(
                        plateX, plateY, plateMat, plateUx, plateUy, plateUt, platePUx, platePUy, platePUt, plateU1, plateU2, plateM2D, plateQ2D, plateNx2D, plateNz2D):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    pX.append(x)
                    pY.append(y)
                    pMat.append(mat)
                    pUx.append(ux)
                    pUy.append(uy)
                    pUt.append(ut)
                    pPUx.append(pux)
                    pPUy.append(puy)
                    pPUt.append(put)
                    pU1.append(u1)
                    pU2.append(u2)
                    pM2D.append(m2d)
                    pQ2D.append(q2d)
                    pNx2D.append(nx2d)
                    pNz2D.append(nz2d)
                    
            except:
                print ('...exception reading Plate results ' + phase.Identification.value)
        columns ='Phase,PhaseIdent,X(m),Y(m),MaterialID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(columns)
                file.writelines([formats.format(pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d)
                                 for pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(u1)
                row.append(u2)
                row.append(m2d)
                row.append(q2d)
                row.append(nx2d)
                row.append(nz2d)
                
                self.insertValues(row)
                
        print('getPlateResults Done')
        
    def getEmbeddedBeamRowResults(self,
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
            tableOut = 'getEmbeddedBeamRowResults'
        
        # init data for lists
        ePhaseName = []
        ePhaseIdent = []
           
        eY = []
        eX = []
        
        eMat = []
            
        eUx = []
        eUy = []
        eUt = []

        ePUx = []
        ePUy = []
        ePUt = []

        eU1 = []
        eU2 = []

        eM2D = []
        eQ2D = []
        eNx2D = []
        eNz2D = []

        eTskin = []
        eTlat= []

        for phase in self.phaseOrder:
            #echo ResultTypes.EmbeddedBeamRow
            print ('Getting EmbeddedBeamRow results ' + phase.Identification.value)
            try:
                embeamX = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.X, 'node')
                embeamY = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Y, 'node')
                
                embeamMat = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.MaterialID, 'node')
                
                embeamUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Ux, 'node')
                embeamUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Uy, 'node')
                embeamUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Utot, 'node')
                
                embeamPUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.PUx, 'node')
                embeamPUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.PUy, 'node')
                embeamPUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.PUtot, 'node')
                 
                embeamU1 = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.U1, 'node')
                embeamU2 = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.U2, 'node')

                embeamM2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.M2D, 'node')
                embeamQ2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Q2D, 'node')
                embeamNx2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Nx2D, 'node')
                embeamNz2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Nz2D, 'node')

                embeamTskin = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Tskin, 'node')
                embeamTlat= self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.Tlat, 'node')
                     
                print ('...read EmbeddedBeamRow results ' + phase.Identification.value)
                
                for x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(
                        embeamX, embeamY, embeamMat, embeamUx, embeamUy, embeamUt, embeamPUx, embeamPUy, embeamPUt, embeamU1, embeamU2, embeamM2D, embeamQ2D, embeamNx2D, embeamNz2D, embeamTskin, embeamTlat):
                    # add filters in here if necessary
                    
                    ePhaseName.append(phase.Name.value)
                    ePhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eMat.append(mat)
                    eUx.append(ux)
                    eUy.append(uy)
                    eUt.append(ut)
                    ePUx.append(pux)
                    ePUy.append(puy)
                    ePUt.append(put)
                    eU1.append(u1)
                    eU2.append(u2)
                    eM2D.append(m2d)
                    eQ2D.append(q2d)
                    eNx2D.append(nx2d)
                    eNz2D.append(nz2d)
                    eTskin.append(tskin)
                    eTlat.append(tlat)
            except:
                print ('...exception reading EmbeddedBeamRow '  + phase.Identification.value)
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat):
                row = []
                row.append(ename)
                row.append(eident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(u1)
                row.append(u2)
                row.append(m2d)
                row.append(q2d)
                row.append(nx2d)
                row.append(nz2d)
                row.append(tskin)
                row.append(tlat)
                
                self.insertValues(row)
    def getSoilResultsByRange(self,
                              fileOut=None,
                              tableOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              xMin=None, xMax=None,
                              yMin=None, yMax=None,
                              ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
                           
        self.setRange(xMin, xMax,
                      yMin, yMax)
        
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByRange'  
 
        locY = []
        locX = []
        
        Uyy = []
        Uxx = []
        Utot = []
            
        PUyy = []
        PUxx = []
        PUtot = []
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []        
        
        PExcess = []
        PActive = []
        PSteady = []
        PWater = []
        
        Suct = []
        EffSuct = []
        
        pPhaseName = []
        pPhaseIdent = []
        
        # look into all phases, all steps
        for phase in self.phaseOrder:
            print('Getting Soil results for Phase ', phase.Name.value, phase.Identification.value)
            
            soilX = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node')
            soilY = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node')
            
            soilUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Ux, 'node')
            soilUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Uy, 'node')
            soilUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Utot, 'node')
            
            soilPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUx, 'node')
            soilPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUy, 'node')
            soilPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUtot, 'node')
            
            soilEffSxx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigxxE, 'node')
            soilEffSyy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigyyE, 'node')
            soilEffSzz = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigzzE, 'node')
            
            soilEffP1= self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective1, 'node')
            soilEffP2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective2, 'node')
            soilEffP3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective3, 'node')  
            
            soilPExcess = self.g_o.getresults(phase, self.g_o.Soil.PExcess, 'node')
            soilPActive = self.g_o.getresults(phase, self.g_o.Soil.PActive, 'node')
            soilPSteady = self.g_o.getresults(phase, self.g_o.Soil.PSteady, 'node')
            soilPWater = self.g_o.getresults(phase, self.g_o.Soil.PWater, 'node')
            
            soilSuction = self.g_o.getresults(phase, self.g_o.Soil.Suction, 'node')
            soilEffSuction = self.g_o.getresults(phase, self.g_o.Soil.EffSuction, 'node')
            
            for x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(
                soilX, soilY, soilUx, soilUy, soilUt, soilPUx, soilPUy, soilPUt, soilEffSxx, soilEffSyy, soilEffSzz, soilEffP1, soilEffP2, soilEffP3, soilPExcess, soilPActive, soilPSteady, soilPWater, soilSuction, soilEffSuction):
                
                if self.inRange (x_val = x, 
                                 y_val = y) == True:
                    
                    print(phase.Name.value, phase.Identification.value, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu)
          
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
           
                    locX.append(x)
                    locY.append(y)
                    
                    Uyy.append (uy)
                    Uxx.append (ux)
                    Utot.append (ut)
            
                    PUyy.append (puy)
                    PUxx.append (pux)
                    PUtot.append (put)
                 
                    EffSxx.append(esx)
                    EffSyy.append(esy)
                    EffSzz.append(esz)
                    
                    EffP1.append (ep1)
                    EffP2.append (ep2)
                    EffP3.append (ep3)
                    
                    PExcess.append (pe)
                    PActive.append (pa)
                    PSteady.append (ps)
                    PWater.append (pw)
        
                    Suct.append (su)
                    EffSuct.append (esu)
                    
        columns = 'Phase,PhaseIdent,locX(m),locY(m),Ux(m),Uy(m),Utot(m), PUx(m), PUy(m), PUt(m), SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa),EffSuct(kPa)'
        formats =  '{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'       
        
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident,  x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu )
                for pname, pident, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(esx)
                row.append(esy)
                row.append(esz)
                row.append(ep1)
                row.append(ep2)
                row.append(ep3)
                row.append(pe)
                row.append(pa)
                row.append(ps)
                row.append(pw)
                row.append(su)
                row.append(esu)
                
                self.insertValues(row)
                
        print('getSoilResultsByRange Done')                
           
        
    def getSoilResultsByPoints(self,
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
        
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByPoints'
        
        locName = []
        locY = []
        locX = []
        
        Uyy = []
        Uxx = []
        Utot = []
            
        PUyy = []
        PUxx = []
        PUtot = []
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []        
        
        PExcess = []
        PActive = []
        PSteady = []
        PWater = []
        
        Suct = []
        EffSuct = []
        
        pPhaseName = []
        pPhaseIdent = []
               

        fpoint = open(filePoints, "r")

        while True:
            in_line = fpoint.readline()
            if in_line == "":
                break
            print(in_line)
            [name, nx, ny] = in_line.split(',')
            self.NodeList.append(self.PointXY(name, nx, ny))

        fpoint.close()

       

        for phase in self.phaseOrder:
            print('Getting soil results ' + phase.Identification.value)
            

                       
            for pt in self.NodeList:

                try:
                    ux = self.g_o.getsingleresult(phase, self.g_o.Soil.Ux, (pt.x, pt.y))
                    uy = self.g_o.getsingleresult(phase, self.g_o.Soil.Uy, (pt.x, pt.y))
                    ut = self.g_o.getsingleresult(phase, self.g_o.Soil.Utot, (pt.x, pt.y))
                    pux = self.g_o.getsingleresult(phase, self.g_o.Soil.PUx, (pt.x, pt.y))
                    puy = self.g_o.getsingleresult(phase, self.g_o.Soil.PUy, (pt.x, pt.y))
                    put = self.g_o.getsingleresult(phase, self.g_o.Soil.PUtot, (pt.x, pt.y))
                    esx = self.g_o.getsingleresult(phase, self.g_o.Soil.SigxxE, (pt.x, pt.y))
                    esy = self.g_o.getsingleresult(phase, self.g_o.Soil.SigyyE, (pt.x, pt.y))
                    esz = self.g_o.getsingleresult(phase, self.g_o.Soil.SigzzE, (pt.x, pt.y))
                    ep1 = self.g_o.getsingleresult(phase, self.g_o.Soil.SigmaEffective1, (pt.x, pt.y))
                    ep2 = self.g_o.getsingleresult(phase, self.g_o.Soil.SigmaEffective2, (pt.x, pt.y))
                    ep3 = self.g_o.getsingleresult(phase, self.g_o.Soil.SigmaEffective3, (pt.x, pt.y))  
                    pe = self.g_o.getsingleresult(phase, self.g_o.Soil.PExcess, (pt.x, pt.y))
                    pa = self.g_o.getsingleresult(phase, self.g_o.Soil.PActive, (pt.x, pt.y))
                    ps = self.g_o.getsingleresult(phase, self.g_o.Soil.PSteady, (pt.x, pt.y))
                    pw = self.g_o.getsingleresult(phase, self.g_o.Soil.PWater, (pt.x, pt.y))
                    su = self.g_o.getsingleresult(phase, self.g_o.Soil.Suction, (pt.x, pt.y))
                    
                    # print (pt.name, pt.x, pt.y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su) 
                    
                    if ux != 'not found':
                    
                        pPhaseName.append(phase.Name.value)
                        pPhaseIdent.append(phase.Identification.value)
                    
                        locName.append(pt.name)
                        locY.append(pt.y)
                        locX.append(pt.x)
                        
                        Uyy.append(uy)
                        Uxx.append(ux)
                        Utot.append(ut)
                        
                        PUyy.append(puy)
                        PUxx.append(pux)
                        PUtot.append(put)
                        
                        EffSxx.append (esx)
                        EffSyy.append (esy)
                        EffSzz.append (esz)
                           
                        EffP1.append (ep1)
                        EffP2.append (ep2)
                        EffP3.append (ep3)
                            
                        PExcess.append (pe)
                        PActive.append (pa)
                        PSteady.append (ps)
                        PWater.append (pw)
                        Suct.append (su)
                     
                except:
                    print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
                    print (pt.name, pt.x, pt.y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
        columns = 'Phase,PhaseIdent,locName,locX(m),locY(m),Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa)'  
        formats = '{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut != None and tableOut == None):
            try :
                print('Outputting to file ', fileOut, '....')
                columns += '\n'
                formats += '\n'
                with open(fileOut, "w") as file:
                    file.writelines([columns])
                    file.writelines([formats.format(pname, pident, locname, float(x), float(y), float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(esx), float(esy), float(esz), float(ep1), float(ep2), float(ep3), float(pe), float(pa), float(ps), float(pw), float(su))
                                     for pname, pident, locname, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)])
            except:
                print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
               #~ print (pname, pident, locname, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
                #~ print (pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, locname, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(locname)
                row.append(x)
                row.append(y)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(esx)
                row.append(esy)
                row.append(esz)
                row.append(ep1)
                row.append(ep2)
                row.append(ep3)
                row.append(pe)
                row.append(pa)
                row.append(ps)
                row.append(pw)
                row.append(su)
                
                self.insertValues(row)
                
        print('getSoilResultsByPoint Done')

