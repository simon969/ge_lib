from plaxis.PlaxisRequests.PlaxisScripting import PlaxisScripting  
class Plaxis2dResults (PlaxisScripting):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResults, self).__init__(server, host, port, password=password)
       
        if (self.s_o.is_2d == False):
            raise ValueError('This is a Plaxis2d output reader, but the output plaxis server is not Plaxis2d');
    def version (self):
        return "Plaxis2d"    

    def getSoilResultsByRanges(self,
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
            tableOut = 'getSoilResultsByRanges'  

        locY = []
        locX = []
        
        Uyy = []
        Uxx = []
        Utot = []
        
        PUyy = []
        PUxx = []
        PUtot = []
        
        MaterialID = []
        ElementID =[]
        
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
            
            soilMat = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.MaterialID, 'node')
            soilEl = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.ElementID, 'node')
            
            soilX = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node')
            soilY = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node')
            
            soilUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Ux, 'node')
            soilUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Uy, 'node')
            soilUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Ut, 'node')
            
            soilPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUy, 'node')
            soilPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUx, 'node')
            soilPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUt, 'node')            
            
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
            
            for x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(
                soilX, soilY, soilMat, soilEl, soilUx, soilUy, soilUt, soilPUx, soilPUy, soilPUt, soilEffSxx, soilEffSyy, soilEffSzz, soilEffP1, soilEffP2, soilEffP3, soilPExcess, soilPActive, soilPSteady, soilPWater, soilSuction, soilEffSuction):
                
                if self.inRange (x_val = x, 
                                 y_val = y) == True:
                    
                    print(phase.Name.value, phase.Identification.value, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu)
          
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
           
                    locX.append(x)
                    locY.append(y)
                    
                    Uxx.append(ux)
                    Uyy.append(uy)
                    Utot.append(ut)
                    
                    PUxx.append(pux)
                    PUyy.append(puy)
                    PUtot.append(put)
                    
                    MaterialID.append(mat)
                    ElementID.append(el)
                    
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
        columns = 'Phase,PhaseIdent,locX(m),locY(m),MaterialID,ElementID,Ux(m),Uy(m),Ut(m),PUx(m),PUy(m),PUt(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa),EffSuct(kPa)'
        formats =  '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'       
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident,  x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu )
                for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident,  x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu )
                for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
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
                
        print('getSoilResultsByRanges Done')
         
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
        
        MaterialID = []
        ElementID =[]
        
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
               
        if filePoints:
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
                    mat = self.g_o.getsingleresult(phase, self.g_o.Soil.MaterialID, (pt.x, pt.y))
                    el = self.g_o.getsingleresult(phase, self.g_o.Soil.ElementID, (pt.x, pt.y))
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
                        
                        MaterialID.append(int(float(mat) + .1))
                        ElementID.append(int(float(el) + .1))
                        
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
                    print (pt.name, pt.x, pt.y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
        columns = 'Phase,PhaseIdent,locName,locX(m),locY(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa)'  
        formats = '{},{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut != None and tableOut == None):
            try :
                print('Outputting to file ', fileOut, '....')
                columns += '\n'
                formats += '\n'
                with open(fileOut, "w") as file:
                    file.writelines([columns])
                    file.writelines([formats.format(pname, pident, locname, float(x), float(y), mat, el, float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(esx), float(esy), float(esz), float(ep1), float(ep2), float(ep3), float(pe), float(pa), float(ps), float(pw), float(su))
                                     for pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)])
            except:
                print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
               #~ print (pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
                #~ print (pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(locname)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
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
        pEl = []
        
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
                plateX = self.g_o.getresults(phase, self.g_o.Plate.X, 'node')
                plateY = self.g_o.getresults(phase, self.g_o.Plate.Y, 'node')
                
                plateMat = self.g_o.getresults(phase, self.g_o.Plate.MaterialID, 'node')
                plateEl = self.g_o.getresults(phase, self.g_o.Plate.ElementID, 'node')
                
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
                
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(
                        plateX, plateY, plateMat, plateEl, plateUx, plateUy, plateUt, platePUx, platePUy, platePUt, plateU1, plateU2, plateM2D, plateQ2D, plateNx2D, plateNz2D):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    pX.append(x)
                    pY.append(y)
                    pMat.append(mat)
                    pEl.append(el)
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
                    
            except Exception as e:
                print ('...exception reading Plate results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Plate results  '+ str(e))
                
        columns ='Phase,PhaseIdent,X(m),Y(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(columns)
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pEl, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pEl, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
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
    
    def getEmbeddedBeamResults (self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  ):
        return self.getEmbeddedBeamRowResults(fileOut=fileOut,
                                  tableOut=tableOut,
                                  sphaseOrder=sphaseOrder,
                                  sphaseStart=sphaseStart,
                                  sphaseEnd=sphaseEnd)
     
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
        eEl = []
        
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
                embeamEl = self.g_o.getresults(phase, self.g_o.EmbeddedBeamRow.ElementID, 'node')
                
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
                
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(
                        embeamX, embeamY, embeamMat, embeamEl, embeamUx, embeamUy, embeamUt, embeamPUx, embeamPUy, embeamPUt, embeamU1, embeamU2, embeamM2D, embeamQ2D, embeamNx2D, embeamNz2D, embeamTskin, embeamTlat):
                    # add filters in here if necessary
                    
                    ePhaseName.append(phase.Name.value)
                    ePhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eMat.append(mat)
                    eEl.append(el)
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
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eEl, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eEl, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat):
                row = []
                row.append(ename)
                row.append(eident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
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
                
        print('getEmbeddedBeamRowResults Done')
    
    
    def getNodeToNodeAnchorResults(self,
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
            tableOut = 'getNodeToNodeAnchorResults'
            
        # init data for lists
        aPhaseName = []
        aPhaseIdent = []
        
        aY = []
        aX = []
        
        aMat = []
        aEl = []
        
        aUx = []
        aUy = []
        
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in self.phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Y, 'node')
                
                anchorMat = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.MaterialID, 'node')
                anchorEl = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.ElementID, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Uy, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUy, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.U2, 'node')

                anchorForce2D = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.AnchorForce2D, 'node')

                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorMat, anchorEl, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aMat.append(mat)
                    aEl.append(el)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except:
                 print ('Exception reading  NodeToNodeAnchor in phase' + phase.Name.value, phase.Identification.value)
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(u1)
                row.append(u2)
                row.append(f2d)
                
                self.insertValues(row)
                
        print('getNodeToNodeAnchorResults Done')
   
    def getFixedEndAnchorResults(self,
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
            tableOut = 'getFixedEndAnchorResults'
        
        # init data for lists
        aPhaseName = []
        aPhaseIdent = []

        aY = []
        aX = []
        
        aMat = []
        aEl = []
        
        aUx = []
        aUy = []
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in self.phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Y, 'node')
                
                anchorMat = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.MaterialID, 'node')
                anchorEl = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.ElementID, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Uy, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUy, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.U2, 'node')

                anchorForce2D = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.AnchorForce2D, 'node')
                
                print('Retrieved FixedEndAnchor results for ', phase.Name.value)
          
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorMat, anchorEl, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aMat.append(mat)
                    aEl.append(el)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except:
                print ('Exception reading  FixedEndAnchor in phase' + phase.Name.value)
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D):
                 row = []
                 row.append(pname)
                 row.append(pident)
                 row.append(x)
                 row.append(y)
                 row.append(mat)
                 row.append(el)
                 row.append(ux)
                 row.append(uy)
                 row.append(ut)
                 row.append(pux)
                 row.append(puy)
                 row.append(put)
                 row.append(u1)
                 row.append(u2)
                 row.append(f2d)
                 
                 self.insertValues(row)
                 
        print('getFixedEndAnchorResults Done')
    def getInterfaceResults2016(self,
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
            tableOut = 'getInterfaceResults'
            
        # init data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []
        iMat = []
          
        iUx = []
        iUy = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUt = []

        iU1 = []
        iU2 = []

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
                interX = self.g_o.getresults(phase, self.g_o.Interface.X, 'node')
                interY = self.g_o.getresults(phase, self.g_o.Interface.Y, 'node')
              
                interMat = self.g_o.getresults(phase, self.g_o.Interface.MaterialID, 'node')
              
                interUx = self.g_o.getresults(phase, self.g_o.Interface.Ux, 'node')
                interUy = self.g_o.getresults(phase, self.g_o.Interface.Uy, 'node')
                interUt = self.g_o.getresults(phase, self.g_o.Interface.Utot, 'node')

                interPUx = self.g_o.getresults(phase, self.g_o.Interface.PUx, 'node')
                interPUy = self.g_o.getresults(phase, self.g_o.Interface.PUy, 'node')
                interPUt = self.g_o.getresults(phase, self.g_o.Interface.PUtot, 'node')

                interU1 = self.g_o.getresults(phase, self.g_o.Interface.U1, 'node')
                interU2 = self.g_o.getresults(phase, self.g_o.Interface.U2, 'node')

                interEffNormalStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceShearStress, 'node')
                interRelShearStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = self.g_o.getresults(phase, self.g_o.Interface.PExcess, 'node')
                interPActive = self.g_o.getresults(phase, self.g_o.Interface.PActive, 'node')
                interPSteady = self.g_o.getresults(phase, self.g_o.Interface.PSteady, 'node')
                interPWater = self.g_o.getresults(phase, self.g_o.Interface.PWater, 'node')
                
                interSuction = self.g_o.getresults(phase, self.g_o.Interface.Suction, 'node')
                interEffSuction = self.g_o.getresults(phase, self.g_o.Interface.EffSuction, 'node')

                for x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, interMat,  
                        interUx, interUy, interUt, 
                        interPUx, interPUy, interPUt, 
                        interU1, interU2, 
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    iX.append(x)
                    iY.append(y)
                    iMat.append(mat)
                    iUx.append(ux)
                    iUy.append(uy)
                    iUt.append(ut)
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUt.append(put)
                    iU1.append(u1)
                    iU2.append(u2)
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
        
        columns = "Phase,PhaseIdent,X(m),Y(m),MaterialId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)"
        formats = "{},{},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}"
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
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
            
        print('getInterfaceResults2016 Done')   
        
    def getInterfaceResults(self,
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
            tableOut = 'getInterfaceResults'
        
        # init data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []
        iMat = []
        iEl = []
        
        iUx = []
        iUy = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUt = []

        iU1 = []
        iU2 = []

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
                interX = self.g_o.getresults(phase, self.g_o.Interface.X, 'node')
                interY = self.g_o.getresults(phase, self.g_o.Interface.Y, 'node')
              
                interMat = self.g_o.getresults(phase, self.g_o.Interface.MaterialID, 'node')
                interEl = self.g_o.getresults(phase, self.g_o.Interface.ElementID, 'node')
              
                interUx = self.g_o.getresults(phase, self.g_o.Interface.Ux, 'node')
                interUy = self.g_o.getresults(phase, self.g_o.Interface.Uy, 'node')
                interUt = self.g_o.getresults(phase, self.g_o.Interface.Utot, 'node')

                interPUx = self.g_o.getresults(phase, self.g_o.Interface.PUx, 'node')
                interPUy = self.g_o.getresults(phase, self.g_o.Interface.PUy, 'node')
                interPUt = self.g_o.getresults(phase, self.g_o.Interface.PUtot, 'node')

                interU1 = self.g_o.getresults(phase, self.g_o.Interface.U1, 'node')
                interU2 = self.g_o.getresults(phase, self.g_o.Interface.U2, 'node')

                interEffNormalStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceShearStress, 'node')
                interRelShearStress = self.g_o.getresults(phase, self.g_o.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = self.g_o.getresults(phase, self.g_o.Interface.PExcess, 'node')
                interPActive = self.g_o.getresults(phase, self.g_o.Interface.PActive, 'node')
                interPSteady = self.g_o.getresults(phase, self.g_o.Interface.PSteady, 'node')
                interPWater = self.g_o.getresults(phase, self.g_o.Interface.PWater, 'node')
                
                interSuction = self.g_o.getresults(phase, self.g_o.Interface.Suction, 'node')
                interEffSuction = self.g_o.getresults(phase, self.g_o.Interface.EffSuction, 'node')

                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, interMat, interEl, 
                        interUx, interUy, interUt, 
                        interPUx, interPUy, interPUt, 
                        interU1, interU2, 
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    iX.append(x)
                    iY.append(y)
                    iMat.append(mat)
                    iEl.append(el)
                    iUx.append(ux)
                    iUy.append(uy)
                    iUt.append(ut)
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUt.append(put)
                    iU1.append(u1)
                    iU2.append(u2)
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
        
        columns = "Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)"
        formats = "{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}"
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iEl, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iEl, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
                                     row = []
                                     row.append(pname)
                                     row.append(pident)
                                     row.append(x)
                                     row.append(y)
                                     row.append(mat)
                                     row.append(el)
                                     row.append(ux)
                                     row.append(uy)
                                     row.append(ut)
                                     row.append(pux)
                                     row.append(puy)
                                     row.append(put)
                                     row.append(u1)
                                     row.append(u2)
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
        
    def getAllStructuralResults(self,
                    folderOut=None,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
                        
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getPlateResults.csv'
        else:
            tableOut = 'getPlateResults'                
        self.getPlateResults (fileOut=fileOut, tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
        
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getEmbeddedBeamRowResults.csv'
        else:
            tableOut = 'getEmbeddedBeamRowResults'  
        self.getEmbeddedBeamRowResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getNodeToNodeAnchorResults.csv'
        else:
            tableOut = 'getNodeToNodeAnchorResults' 
        self.getNodeToNodeAnchorResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
                       
   
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getFixedEndAnchorResults.csv'
            tableOut = None
        else:
            tableOut = 'getFixedEndAnchorResults'
        
        self.getFixedEndAnchorResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )

        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getInterfaceResults.csv'
        else:
            tableOut = 'getInterfaceResults'
        self.getInterfaceResults  (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )
    
    def getAllStructuralResults2016(self,
                    folderOut=None,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
                        
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getPlateResults.csv'
        else:
            tableOut = 'getPlateResults'                
        self.getPlateResults2016 (fileOut=fileOut, tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
        
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getEmbeddedBeamRowResults.csv'
        else:
            tableOut = 'getEmbeddedBeamRowResults'  
        self.getEmbeddedBeamRowResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getNodeToNodeAnchorResults.csv'
        else:
            tableOut = 'getNodeToNodeAnchorResults' 
        self.getNodeToNodeAnchorResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
                       
   
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getFixedEndAnchorResults.csv'
            tableOut = None
        else:
            tableOut = 'getFixedEndAnchorResults'
        
        self.getFixedEndAnchorResults (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )

        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getInterfaceResults.csv'
        else:
            tableOut = 'getInterfaceResults'
        self.getInterfaceResults2016  (fileOut=fileOut,tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      ) 

