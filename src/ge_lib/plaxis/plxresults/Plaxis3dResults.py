from ge_lib.plaxis.plxresults.PlaxisScripting import PlaxisScripting  
class Plaxis3dResults (PlaxisScripting):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults, self).__init__(server, host, port, password)
        
        if (self.s_o.is_3d == False):
            raise ValueError('This is a Plaxis3d output reader, but the output plaxis server is not Plaxis3d');
    def version (self):
        return "Plaxis3d"

    def getPhaseDetails(self):
        results = []
        allpassed = True
        
        print('getting output phase details')
        for phase in self.g_o.Phases[:]:
            results.append( "{},{},{}\n".format(phase.Name, phase.Identification, phase.Number))

        return allpassed, results
    
    def getSoilResultsByRange(self,
                              fileOut=None,
                              tableOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              xMin=0.0, xMax=0.0,
                              yMin=0.0, yMax=0.0,
                              zMin=0.0, zMax=0.0,
                              Output="stress, displacement,pwp"
                              ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByRange'  
        
        PhaseName = []
        PhaseIdent = []
        
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
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []
        
        pExcess = []
        pActive = []    
        pSteady = []
        pWater = []
        
        phasenames = []

        # look into all phases, all steps
        for phase in self.phaseOrder:
        
            print('Getting soil results for Phase ', phase.Name.value)
        
            soilX = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node')
            soilY = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node')
            soilZ = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Z, 'node')
             
            print('Coordinates retrieved for Phase ', phase.Name.value)
            if "displacement" in Output:
                
                soilUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Ux, 'node')
                soilUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Uy, 'node')
                soilUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Uz, 'node')
                soilUtot = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Utot, 'node')
                
                soilPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUx, 'node')
                soilPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUy, 'node')
                soilPUz = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUz, 'node')
                soilPUtot = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PUtot, 'node') 
                print('Displacments retrieved for Phase ', phase.Name.value)
            
            if "stress" in Output:
                soilEffSxx = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigxxE, 'node')
                soilEffSyy = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigyyE, 'node')
                soilEffSzz = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigzzE, 'node')
                
                soilEffP1= self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective1, 'node')
                soilEffP2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective2, 'node')
                soilEffP3 = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.SigmaEffective3, 'node')  
                print('Stresses retrieved for Phase ', phase.Name.value)
            
            if "pwp" in Output:
                soilPExcess = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PExcess, 'node')
                soilPActive = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PActive, 'node')
                soilPSteady = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PSteady, 'node')
                soilPWater = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.PWater, 'node')
                print('PWP retrieved for Phase ', phase.Name.value)
            
            print('Preparing to cycle through results for nodes within range...x(', xMin, xMax, ') y(', yMin, yMax,') z (', zMin, zMax ,')')
            
            if "displacement" in Output and "stress" in Output and "pwp" in Output: 
                for x, y, z, ux, uy, uz, utot, pux, puy, puz, putot, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(
                        soilX, soilY, soilZ, soilUx, soilUy, soilUz, soilUtot, soilPUx, soilPUy, soilPUz, soilPUtot, soilEffSxx, soilEffSyy, soilEffSzz, soilEffP1, soilEffP2, soilEffP3,soilPExcess, soilPActive, soilPSteady, soilPWater):
                
                    if xMin < x < xMax:
                        if yMin < y < yMax:
                            if zMin < z < zMax:
                                print('Adding Results for',x,y,z)
                  
                                PhaseName.append(phase.Name.value)
                                PhaseIdent.append(phase.Identification.value)
                                
                                locX.append(x)
                                locY.append(y)
                                locZ.append(z)
                                                                 
                                Uxx.append(ux)
                                Uyy.append(uy)
                                Uzz.append(uz)
                                Utot.append(utot)
                                 
                                PUxx.append(pux)
                                PUyy.append(puy)
                                PUzz.append(puz)
                                PUtot.append(putot)

                                EffSxx.append(esxx)
                                EffSyy.append(esyy)
                                EffSzz.append(eszz)
                             
                                EffP1.append(esxx)
                                EffP2.append(esyy)
                                EffP3.append(eszz)
                                

                                pExcess.append(pex)
                                pActive.append(pact) 
                                pSteady.append(pst)
                                pWater.append(pw)
                columns = 'Phase, PhaseIdent,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),SigxxE(kPa),SigyyE(kPa),SigzzE(kPa),SigEff1(kPa),SigEff2(kPa),SigEff3(kPa),pExcess(kPa),pActive(kPa),pSteady(kPa),pWater(kPa)'
                formats =  '{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
                
                if (fileOut == None and tableOut == None):
                    print('Outputting to string....')
                    columns += '\n'
                    formats += '\n'
                    rows = ''.join([formats.format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw)
                            for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, pExcess, pActive, pSteady, pWater)])
                    return columns + rows

                if (fileOut != None and tableOut == None):
                    print('Outputting to file ', fileOut, '....')  
                    columns += '\n'
                    formats += '\n'
                    with open(fileOut, "w") as file:
                        file.writelines([columns])
                        file.writelines([formats.format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw)
                            for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, pExcess, pActive, pSteady, pWater)])
                
                if (fileOut != None and tableOut != None):
                    print('Outputting to database ', fileOut, '....')

                    self.getConnected (fileOut)
                    self.createTable(tableOut, columns, formats)
                    for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, pExcess, pActive, pSteady, pWater):
                        row = []
                        row.append(pName)
                        row.append(pIdent)
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
                        row.append(put)
                        row.append(esxx)
                        row.append(esyy)
                        row.append(eszz)
                        row.append(ep1)
                        row.append(ep2)
                        row.append(ep3)
                        row.append(pex)
                        row.append(pact)
                        row.append(pst)
                        row.append(pw)
                        self.insertValues(row)
                    
            if "displacement" in Output and not "stress" in Output and not "pwp" in Output: 
                for x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(
                        soilX, soilY, soilZ, soilUx, soilUy, soilUz, soilUtot, soilPUx, soilPUy, soilPUz, soilPUtot):
                    print (x, y, z)
                    if xMin < x < xMax:
                        if yMin < y < yMax:
                            if zMin < z < zMax:
                                print('Adding Results for',x,y,z)
                  
                                PhaseName.append(phase.Name.value)
                                PhaseIdent.append(phase.Identification.value)
                                
                                locX.append(x)
                                locY.append(y)
                                locZ.append(z)
                                
                                Uxx.append(ux)
                                Uyy.append(uy)
                                Uzz.append(uz)
                                Utot.append(utot)
                                 
                                PUxx.append(pux)
                                PUyy.append(puy)
                                PUzz.append(puz)
                                PUtot.append(putot)  
                columns='Phase, PhaseIdent,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m)'
                formats='{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'                
                if (fileOut != None and tableOut == None):
                    print('Outputting to file ', fileOut, '....')
                    columns += '\n'
                    formats += '\n'
                    with open(fileOut, "w") as file:
                        file.writelines([columns])
                        file.writelines([formats.format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot)
                            for x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot)])
                if (fileOut != None and tableOut != None):
                    print('Outputting to database ', fileOut, '....')
                    self.getConnected (fileOut)
                    self.createTable(tableOut, columns, formats)
                    for x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot):
                        row=[]
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
                        row.append(dutot)
                        self.insertValues(row)
                        
    def getSoilResultsByPoints(self,
                              fileOut=None,
                              tableOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              Output="stress, displacement,pwp",
                              xMin=0.0, xMax=0.0,
                              yMin=0.0, yMax=0.0,
                              zMin=0.0, zMax=0.0,
                              ):
                              
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByRange2'  
        
        
        
        phaseName = []
        phaseIdent = []
        
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
        
        self.setNodeList (xMin, xMax,
                          yMin, yMax,
                          zMin, zMax)
       
        for phase in self.phaseOrder:
            
            print('retrieving results for ', phase.Name.value)  

            for pt in self.NodeList:
                ux = self.g_o.getsingleresult(phase, self.g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = self.g_o.getsingleresult(phase, self.g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = self.g_o.getsingleresult(phase, self.g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = self.g_o.getsingleresult(phase, self.g_o.Soil.Utot, (pt.x, pt.y, pt.z))
                pux = self.g_o.getsingleresult(phase, self.g_o.Soil.PUx, (pt.x, pt.y, pt.z))
                puy = self.g_o.getsingleresult(phase, self.g_o.Soil.PUy, (pt.x, pt.y, pt.z))
                puz = self.g_o.getsingleresult(phase, self.g_o.Soil.PUz, (pt.x, pt.y, pt.z))
                putot = self.g_o.getsingleresult(phase, self.g_o.Soil.PUtot, (pt.x, pt.y, pt.z)) 
                
                # sxx = self.g_o.getsingleresult(phase, self.g_o.Soil.SigxxE, (pt.x, pt.y, pt.z))
                # syy = self.g_o.getsingleresult(phase, self.g_o.Soil.SigyyE, (pt.x, pt.y, pt.z))
                # szz = self.g_o.getsingleresult(phase, self.g_o.Soil.SigzzE, (pt.x, pt.y, pt.z))
                # xpwp = self.g_o.getsingleresult(phase, self.g_o.Soil.PExcess, (pt.x, pt.y, pt.z))
                
                print('results for ', phase.Name.value, pt.x, pt.y, pt.z ,' retrieved')
                
                phaseName.append(phase.Name.value)
                phaseIdent.append(phase.Identification.value)
              
                locX.append (pt.x)
                locY.append (pt.y)
                locZ.append (pt.z)
                               
                Uxx.append (ux)
                Uyy.append (uy)
                Uzz.append (uz)
                Utot.append (utot)
                
                PUxx.append (pux)
                PUyy.append (puy)
                PUzz.append (puy)
                PUtot.append (putot)
         
        columns='Phase, PhaseIdent,X(m),Y(m),Z(m),MaterialId,ElementId,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m)'
        formats='{},{},{:2f},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'                
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot)
                for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(phaseName, phaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(phaseName, phaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot):
                row=[]
                row.append(pName)
                row.append(pIdent)
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
                row.append(dutot)
                self.insertValues(row)                
                  
    def getSoilResultsByPoints(self,
                               filePoints=None,
                               fileOut=None,
                               tableOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               ):
        self.getSoilResultsByPoints_Displacements(
                               filePoints=filePoints,
                               fileOut=fileOut,
                               tableOut=tableOut,
                               sphaseOrder=sphaseOrder,
                               sphaseStart=sphaseStart,
                               sphaseEnd=sphaseEnd,
                               )                           
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
            
                ux = self.g_o.getsingleresult(phase, self.g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = self.g_o.getsingleresult(phase, self.g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = self.g_o.getsingleresult(phase, self.g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = self.g_o.getsingleresult(phase, self.g_o.Soil.Utot, (pt.x, pt.y, pt.z))
                 
                pux = self.g_o.getsingleresult(phase, self.g_o.Soil.PUx, (pt.x, pt.y, pt.z))
                puy = self.g_o.getsingleresult(phase, self.g_o.Soil.PUy, (pt.x, pt.y, pt.z))
                puz = self.g_o.getsingleresult(phase, self.g_o.Soil.PUz, (pt.x, pt.y, pt.z))
                putot = self.g_o.getsingleresult(phase, self.g_o.Soil.PUtot, (pt.x, pt.y, pt.z)) 
                
                ex = self.g_o.getsingleresult(phase, self.g_o.Soil.Epsxx, (pt.x, pt.y, pt.z))
                ey = self.g_o.getsingleresult(phase, self.g_o.Soil.Epsyy, (pt.x, pt.y, pt.z))
                ez = self.g_o.getsingleresult(phase, self.g_o.Soil.Epszz, (pt.x, pt.y, pt.z))
                
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
                
    def getSoilResultsByPoints_Stresses(self,
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
            tableOut = 'getSoilResultsByPoints_Stresses'  
        
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
        
        SigxxT = []
        SigyyT = []
        SigzzT = []
        
        Sigxy = []
        Sigyz = []
        Sigzx = []

            
        for phase in self.phaseOrder:
            print(phase.Name.value)
    
            for pt in self.NodeList:
            
                ux = self.g_o.getsingleresult(phase, self.g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = self.g_o.getsingleresult(phase, self.g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = self.g_o.getsingleresult(phase, self.g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = self.g_o.getsingleresult(phase, self.g_o.Soil.Utot, (pt.x, pt.y, pt.z))
             
                sig_xxt = self.g_o.getsingleresult(phase, self.g_o.Soil.SigxxT, (pt.x, pt.y, pt.z))
                sig_yyt = self.g_o.getsingleresult(phase, self.g_o.Soil.SigyyT, (pt.x, pt.y, pt.z))
                sig_zzt = self.g_o.getsingleresult(phase, self.g_o.Soil.SigzzT, (pt.x, pt.y, pt.z))
                            
                sig_xy = self.g_o.getsingleresult(phase, self.g_o.Soil.Sigxy, (pt.x, pt.y, pt.z))
                sig_yz = self.g_o.getsingleresult(phase, self.g_o.Soil.Sigyz, (pt.x, pt.y, pt.z))
                sig_zx = self.g_o.getsingleresult(phase, self.g_o.Soil.Sigzx, (pt.x, pt.y, pt.z))
                
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
                
                    SigxxT.append (sig_xxt)
                    SigyyT.append (sig_yyt)
                    SigzzT.append (sig_zzt)
                
                    Sigxy.append (sig_xy)
                    Sigyz.append (sig_yz)
                    Sigzx.append (sig_zx)
              
                
        columns='Phase,PhaseIdent,locName,locX(m),locY(m),locZ(m),Ux(m),Uy(m),Uz(m),Utot(m),SxxT,SyyT,SzzT,Sxy,Syz,Szx'
        formats='{},{},{},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}'                
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            try: 
                with open(fileOut, "w") as file:
                    file.writelines([columns])
                    file.writelines([formats.format(pName, pIdent,locname, float(x), float(y), float(z), float(ux), float(uy), float(uz), float(utot), float(sig_xxt), float(sig_yyt), float(sig_zzt), float(sig_xy), float(sig_yz), float(sig_zx))
                    for pName, pIdent, locname, x, y, z, ux, uy, uz, utot, sig_xxt, sig_yyt, sig_zzt, sig_xy, sig_yz, sig_zx in zip(phaseName, phaseIdent, locName, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, SigxxT, SigyyT, SigzzT, Sigxy, Sigyz, Sigzx)])
            except:
                print ('Exception writing fileoutput')    
        print("end")
        file.close
        
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
                #~ plateEl =  self.g_o.getresults(phase, self.g_o.Plate.ElementID, 'node')
                
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
                
                #~ print (plateEl)
                
                for x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(
                        plateX, plateY, plateZ, plateMat, plateUx, plateUy, plateUz, plateUt, platePUx, platePUy, platePUz, platePUt, plateU1, plateU2, plateU3, plateN1, plateN2, plateQ12, plateQ23, plateQ13, plateM11, plateM22, plateM12):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    
                    pX.append(x)
                    pY.append(y)
                    pZ.append(z)
                    pMat.append(mat)
                   
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
            except:
                print ('Exception reading Plate in phase' + phase.Name.value)

        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N1(kN/m),N2(kN/m),Q12(kN/m),Q23(kN/m),Q13(kN/m),M11(kNm/m),M22(kNm/m),M12(kNm/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            print (self.columns)
            print (self.formats)
            print (self.types)
            for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12):
                row= []
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
        
    def getPlateResultsByPoints(self,
                        filePoints=None,
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
        
  
        if not filePoints is None:
            self.loadXYZNodeList(filePoints)
        
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResultsByPoints'  
        print('FileOut=', fileOut)

        # initialise data for lists
        pPhaseName = []
        pPhaseIdent = []
                
        pLocName = []
        
        pY = []
        pX = []
        pZ = []
        
        pMat = []
               
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
            
            for pt in self.NodeList:
                try: 
                    
                    mat = self.g_o.getsingleresult(phase, self.g_o.Plate.MaterialID, (pt.x, pt.y, pt.z))
                                    
                    ux = self.g_o.getsingleresult(phase, self.g_o.Plate.Ux, (pt.x, pt.y, pt.z))
                    uy = self.g_o.getsingleresult(phase, self.g_o.Plate.Uy, (pt.x, pt.y, pt.z))
                    uz = self.g_o.getsingleresult(phase, self.g_o.Plate.Uz, (pt.x, pt.y, pt.z))
                    ut = self.g_o.getsingleresult(phase, self.g_o.Plate.Utot, (pt.x, pt.y, pt.z))

                    pux = self.g_o.getsingleresult(phase, self.g_o.Plate.PUx, (pt.x, pt.y, pt.z))
                    puy = self.g_o.getsingleresult(phase, self.g_o.Plate.PUy, (pt.x, pt.y, pt.z))
                    puz = self.g_o.getsingleresult(phase, self.g_o.Plate.PUz, (pt.x, pt.y, pt.z))
                    put = self.g_o.getsingleresult(phase, self.g_o.Plate.PUtot, (pt.x, pt.y, pt.z))

                    u1 = self.g_o.getsingleresult(phase, self.g_o.Plate.U1, (pt.x, pt.y, pt.z))
                    u2 = self.g_o.getsingleresult(phase, self.g_o.Plate.U2, (pt.x, pt.y, pt.z))
                    u3 = self.g_o.getsingleresult(phase, self.g_o.Plate.U3, (pt.x, pt.y, pt.z))
                    
                    n1 = self.g_o.getsingleresult(phase, self.g_o.Plate.N11, (pt.x, pt.y, pt.z))
                    n2 = self.g_o.getsingleresult(phase, self.g_o.Plate.N22, (pt.x, pt.y, pt.z))                
                    q12 = self.g_o.getsingleresult(phase, self.g_o.Plate.Q12, (pt.x, pt.y, pt.z))
                    q23 = self.g_o.getsingleresult(phase, self.g_o.Plate.Q23, (pt.x, pt.y, pt.z))
                    q13 = self.g_o.getsingleresult(phase, self.g_o.Plate.Q13, (pt.x, pt.y, pt.z))
                    m11 = self.g_o.getsingleresult(phase, self.g_o.Plate.M11, (pt.x, pt.y, pt.z))
                    m22 = self.g_o.getsingleresult(phase, self.g_o.Plate.M22, (pt.x, pt.y, pt.z))
                    m12 = self.g_o.getsingleresult(phase, self.g_o.Plate.M12, (pt.x, pt.y, pt.z))
                    
                    if ux == 'not found':
                        print('results for ', phase.Name.value, pt.name, pt.x, pt.y, pt.z ,' not found')
                    if ux != 'not found':
                        print('results for ', phase.Name.value, pt.name, pt.x, pt.y, pt.z ,' retrieved')
                        # add filters in here if necessary
                        pPhaseName.append(phase.Name.value)
                        pPhaseIdent.append(phase.Identification.value)
                        
                        pX.append(pt.x)
                        pY.append(pt.y)
                        pZ.append(pt.z)
                        
                        pMat.append(int(float(mat) + .1))
                        pLocName.append (pt.name)
                        
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
                        
                except:
                    print ('Exception reading Plate in phase' + phase.Name.value)

        columns ='Phase,PhaseIdent,LocName, X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N1(kN/m),N2(kN/m),Q12(kN/m),Q23(kN/m),Q13(kN/m),M11(kNm/m),M22(kNm/m),M12(kNm/m)'
        formats = '{},{},{},{:2f},{:2f},{:2f},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, plocname, float(x), float(y), float(z), mat, float(ux), float(uy), float(uz), float(ut), float(pux), float(puy), float(puz), float(put), float(u1), float(u2), float(u3), float(n1), float(n2), float(q12), float(q23), float(q13), float(m11), float(m22), float(m12))
                                 for pname, pident, plocname, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pLocName, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, plocname, float(x), float(y), float(z), mat, float(ux), float(uy), float(uz), float(ut), float(pux), float(puy), float(puz), float(put), float(u1), float(u2), float(u3), float(n1), float(n2), float(q12), float(q23), float(q13), float(m11), float(m22), float(m12))
                                 for pname, pident, plocname, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pLocName, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            print (self.columns)
            print (self.formats)
            print (self.types)
            for pname, pident,locname, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pLocName, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12):
                row= []
                row.append(pname) 
                row.append(pident)
                row.append(locname)
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
                row.append(n1)
                row.append(n2)
                row.append(q12)
                row.append(q23)
                row.append(q13)
                row.append(m11)
                row.append(m22)
                row.append(m12)
                self.insertValues(row)
        
        print('getPlateResultsByPoints Done')       
   
    def getInterfaceResultsByPoints(self,
                        filePoints=None,
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
                    x = self.g_o.getsingleresult(phase, self.g_o.Interface.X, (pt.x, pt.y, pt.z))
                    y = self.g_o.getsingleresult(phase, self.g_o.Interface.Y, (pt.x, pt.y, pt.z))
                    z = self.g_o.getsingleresult(phase, self.g_o.Interface.Z, (pt.x, pt.y, pt.z))
                    mat = self.g_o.getsingleresult(phase, self.g_o.Interface.MaterialID,  (pt.x, pt.y, pt.z))
                                   
                    ux = self.g_o.getsingleresult(phase, self.g_o.Interface.Ux, (pt.x, pt.y, pt.z))
                    uy = self.g_o.getsingleresult(phase, self.g_o.Interface.Uy, (pt.x, pt.y, pt.z))
                    uz = self.g_o.getsingleresult(phase, self.g_o.Interface.Uz, (pt.x, pt.y, pt.z))
                    ut = self.g_o.getsingleresult(phase, self.g_o.Interface.Utot, (pt.x, pt.y, pt.z))

                    pux = self.g_o.getsingleresult(phase, self.g_o.Interface.PUx, (pt.x, pt.y, pt.z))
                    puy = self.g_o.getsingleresult(phase, self.g_o.Interface.PUy, (pt.x, pt.y, pt.z))
                    puz = self.g_o.getsingleresult(phase, self.g_o.Interface.PUz, (pt.x, pt.y, pt.z))
                    put = self.g_o.getsingleresult(phase, self.g_o.Interface.PUtot, (pt.x, pt.y, pt.z))

                    u1 = self.g_o.getsingleresult(phase, self.g_o.Interface.U1, (pt.x, pt.y, pt.z))
                    u2 = self.g_o.getsingleresult(phase, self.g_o.Interface.U2, (pt.x, pt.y, pt.z))
                    u3 = self.g_o.getsingleresult(phase, self.g_o.Interface.U3, (pt.x, pt.y, pt.z))
                    
                    ens = self.g_o.getsingleresult(phase, self.g_o.Interface.InterfaceEffectiveNormalStress, (pt.x, pt.y, pt.z))
                    tns = self.g_o.getsingleresult(phase, self.g_o.Interface.InterfaceTotalNormalStress, (pt.x, pt.y, pt.z))
                    ss = self.g_o.getsingleresult(phase, self.g_o.Interface.InterfaceShearStress, (pt.x, pt.y, pt.z))
                    rss = self.g_o.getsingleresult(phase, self.g_o.Interface.InterfaceRelativeShearStress, (pt.x, pt.y, pt.z))

                    pe = self.g_o.getsingleresult(phase, self.g_o.Interface.PExcess, (pt.x, pt.y, pt.z))
                    pa = self.g_o.getsingleresult(phase, self.g_o.Interface.PActive, (pt.x, pt.y, pt.z))
                    pst = self.g_o.getsingleresult(phase, self.g_o.Interface.PSteady, (pt.x, pt.y, pt.z))
                    pw = self.g_o.getsingleresult(phase, self.g_o.Interface.PWater, (pt.x, pt.y, pt.z))
                    
                    su = self.g_o.getsingleresult(phase, self.g_o.Interface.Suction, (pt.x, pt.y, pt.z))
                    esu = self.g_o.getsingleresult(phase, self.g_o.Interface.EffSuction, (pt.x, pt.y, pt.z))
                    
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
                     
                for mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(
                        beamMat, beamX, beamY, beamZ, beamUx, beamUy, beamUz, beamUt, beamPUx, beamPUy, beamPUz, beamPUt, beamU1, beamU2, beamU3, beamN, beamQ12, beamQ13, beamM2, beamM3):
                    # print ('YUt') 
                    
                    # add filters in here if necessary
                    bPhaseName.append(phase.Name.value)
                    bPhaseIdent.append(phase.Identification.value)
                    
                    bMat.append(mat)
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

        columns ='Phase,PhaseIdent,MaterialID,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN/m),Q12(kN/m),Q13(kN/m),M2(kNm/m),M3(kNm/m)'
        formats = '{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                                 for pname, pident, mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3)
                                 for pname, pident, mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, mat, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3 in zip(bPhaseName, bPhaseIdent, bMat, bX, bY, bZ, bUx, bUy, bUz, bUt, bPUx, bPUy, bPUz, bPUt, bU1, bU2, bU3, bN, bQ12, bQ13, bM2, bM3):
                row= []
                row.append(pname) 
                row.append(pident)
                row.append(mat)
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
                embeamX = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.X, 'node')
                embeamY = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Y, 'node')
                embeamZ = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeam.Z, 'node')
                print('Retrieved U')
                ebeamMat = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.MaterialID, 'node')
                                
                embeamUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Ux, 'node')
                embeamUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Uy, 'node')
                embeamUz = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Uz, 'node')
                embeamUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Utot, 'node')
                print('Retrieved U')
                embeamPUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUx, 'node')
                embeamPUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUy, 'node')
                embeamPUz = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUz, 'node')
                embeamPUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUtot, 'node')
                print('Retrieved dU')
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
                
                for x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(
                        embeamX, embeamY, embeamZ, ebeamMat, embeamUx, embeamUy, embeamUz, embeamUt, embeamPUx, embeamPUy,  embeamPUz, embeamPUt, embeamU1, embeamU2, embeamU3, embeamN, embeamQ12, embeamQ13, embeamM2, embeamM3, embeamTskin, embeamTlat, embeamTlat2):
                    # add filters in here if necessary
                    PhaseName.append(phase.Name.value)
                    PhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eZ.append(z)
                    eMat.append(mat)
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
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),MaterialID,Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),N(kN),Q12(kN),Q13(kN),M2(kNm),M3(kNm),Tskin(kN/m),Tlat(kN/m),Tlat2(kN/m)'
        formats = '{},{},{:2f},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, mat,ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, mat,ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eMat, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2):
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
        
    def getNodeToNodeAnchorResults(self,
                                   fileOut=None,
                                   tableOut=None,
                                   sphaseOrder=None,
                                   sphaseStart=None,
                                   sphaseEnd=None,
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
        
        print('FileOut=', fileOut)

        # initialize data for lists
        aPhaseName = []
        aPhaseIdent = []
        
        aY = []
        aX = []
        aZ = []
                
        aUx = []
        aUy = []
        aUz = []
        aUt = []
        
        aPUx = []
        aPUy = []
        aPUz = []
        aPUt = []
        
        aU1 = []
        aU2 = []
        aU3 = []
        
        aForce3D = []

        for phase in self.phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Y, 'node')
                anchorZ = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Z, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Uy, 'node')
                anchorUz = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Uz, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUy, 'node')
                anchorPUz = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUz, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.U2, 'node')
                anchorU3 = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.U3, 'node')
                
                anchorForce3D = self.g_o.getresults(phase, self.g_o.NodeToNodeAnchor.AnchorForce3D, 'node')

                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3D in zip(
                        anchorX, anchorY, anchorZ, anchorUx, anchorUy, anchorUz, anchorUt, anchorPUx, anchorPUy, anchorPUz, anchorPUt, anchorU1, anchorU2, anchorU3, anchorForce3D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    
                    aX.append(x)
                    aY.append(y)
                    aZ.append(z)
                                        
                    aUx.append(ux)
                    aUy.append(uy)
                    aUz.append(uz)
                    aUt.append(ut)
                    
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUz.append(puz)
                    aPUt.append(put)
                    
                    aU1.append(u1)
                    aU2.append(u2)
                    aU3.append(u3)   
                    
                    aForce3D.append(f3D)
            except:
                 print ('Exception reading  NodeToNodeAnchor in phase' + phase.Name.value, phase.Identification.value)
        
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),U1(m),U2(m),U3(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D):
                row = []
                row.append(pname)
                row.append(pident)
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
                row.append(f3d)
                self.insertValues(row)
        print('getNodeToNodeAnchorResults Done')
   
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 tableOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None
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
        
        print('FileOut=', fileOut)

        # initialize data for lists
        aPhaseName = []
        aPhaseIdent = []

        aY = []
        aX = []
        aZ = []
        
        aUx = []
        aUy = []
        aUz = []
        aUt = []
        
        aPUx = []
        aPUy = []
        aPUz = []
        aPUt = []
        
        aU1 = []
        aU2 = []
        aU3 = []
        
        aForce3D = []

        for phase in self.phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Y, 'node')
                anchorZ = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Z, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Uy, 'node')
                anchorUz = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Uz, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUy, 'node')
                anchorPUz = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUz, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.U2, 'node')
                anchorU3 = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.U3, 'node')
                
                anchorForce3D = self.g_o.getresults(phase, self.g_o.FixedEndAnchor.AnchorForce3D, 'node')
                
                print('Retrieved FixedEndAnchor results for ', phase.Name.value)
          
                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3D in zip(
                        anchorX, anchorY, anchorZ, anchorUx, anchorUy, anchorUz, anchorUt, anchorPUx, anchorPUy, anchorPUz, anchorPUt, anchorU1, anchorU2, anchorU3, anchorForce3D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    
                    aX.append(x)
                    aY.append(y)
                    aZ.append(z)
                                         
                    aUx.append(ux)
                    aUy.append(uy)
                    aUz.append(uz)
                    aUt.append(ut)
                    
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUz.append(puz)
                    aPUt.append(put)
                    
                    aU1.append(u1)
                    aU2.append(u2)
                    aU3.append(u3)
                    
                    aForce3D.append(f3D)
            except:
                print ('Exception reading  FixedEndAnchor in phase' + phase.Name.value)
                
        columns ='Phase,PhaseIdent,X(m),Y(m),Z(m),Ux(m),Uy(m),Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUtot(m),U1(m),U2(m),U3(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            print('Outputting to string....')
            columns += '\n'
            formats += '\n'
            rows = ''.join([formats.format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            print('Outputting to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D):
                row = []
                row.append(pname)
                row.append(pident)
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
                row.append(f3d)
                self.insertValues(row)
                
        print('getFixedEndAnchorResults Done')

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
                interX = self.g_o.getresults(phase, self.g_o.Interface.X, 'node')
                interY = self.g_o.getresults(phase, self.g_o.Interface.Y, 'node')
                interZ = self.g_o.getresults(phase, self.g_o.Interface.Z, 'node')
                
                interMat = self.g_o.getresults(phase, self.g_o.Interface.MaterialID, 'node')
                               
                interUx = self.g_o.getresults(phase, self.g_o.Interface.Ux, 'node')
                interUy = self.g_o.getresults(phase, self.g_o.Interface.Uy, 'node')
                interUz = self.g_o.getresults(phase, self.g_o.Interface.Uz, 'node')
                interUt = self.g_o.getresults(phase, self.g_o.Interface.Utot, 'node')

                interPUx = self.g_o.getresults(phase, self.g_o.Interface.PUx, 'node')
                interPUy = self.g_o.getresults(phase, self.g_o.Interface.PUy, 'node')
                interPUz = self.g_o.getresults(phase, self.g_o.Interface.PUz, 'node')
                interPUt = self.g_o.getresults(phase, self.g_o.Interface.PUtot, 'node')

                interU1 = self.g_o.getresults(phase, self.g_o.Interface.U1, 'node')
                interU2 = self.g_o.getresults(phase, self.g_o.Interface.U2, 'node')
                interU3 = self.g_o.getresults(phase, self.g_o.Interface.U3, 'node')
                
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
            except :
                print ('Exception reading Interface results in phase' + phase.Name.value)
                    
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
        
    def getAllStructuralResults(self,
                    folderOut=None,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):    
        
        if (self.IsDbFile(fileOut) == False):
            fileOut = folderOut + r'\getBeamResults.csv'
        else:
            tableOut = 'getBeamResults'                
        self.getBeamResults (fileOut=fileOut, tableOut=tableOut,
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
        
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
            fileOut = folderOut + r'\getEmbeddedBeamResults.csv'
        else:
            tableOut = 'getEmbeddedBeamResults'  
        self.getEmbeddedBeamResults (fileOut=fileOut,tableOut=tableOut,
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

