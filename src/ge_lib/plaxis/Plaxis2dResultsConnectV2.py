

from .Plaxis2dResults2019 import Plaxis2dResults2019
from .OutputWriter import GetWriter

class Plaxis2dResultsConnectV2 (Plaxis2dResults2019):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResultsConnectV2, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2dConnectV2"

    def getInterfaceResultsByPointsByStep (self,
                        filePoints=None,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None,
                        stepList=None
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
  
        if not filePoints is None:
            self.loadXYNodeList(filePoints)
        
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResultsByPointsStep'  
        
        print('FileOut=', fileOut)

        # initialize data for lists
        iPhaseName = []
        iPhaseIdent = []
        
        iLocName = []
        
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

        iVx = []
        iVy = []
        iVt = []
        
        iAx = []
        iAy = []
        iAt = []           

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

            print("Getting Interface results for Phase:{}".format(phase.Name.value))
            
            for step in phase:
            
                if stepList is None or step.Name.value in stepList:
            
                    print("Getting Interface results for Step:{}".format(step.Name.value))
                    
                    for pt in self.NodeList:
                        
                        print("Getting Interface results for Node:{}".format(pt.name))
                        
                        try:
                           
                            x = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.X, (pt.x, pt.y))
                            y = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Y, (pt.x, pt.y))
                           
                            mat = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.MaterialID,  (pt.x, pt.y))
                                     
                            ux = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ux, (pt.x, pt.y))
                            uy = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Uy, (pt.x, pt.y))
                            ut = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Utot, (pt.x, pt.y))

                            pux = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PUx, (pt.x, pt.y))
                            puy = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PUy, (pt.x, pt.y))
                            put = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PUtot, (pt.x, pt.y))
                            
                            u1 = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.U1, (pt.x, pt.y))
                            u2 = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.U2, (pt.x, pt.y))
                            
                            vx =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Vx, (pt.x, pt.y))
                            vy = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Vy, (pt.x, pt.y))
                            vt = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Vtot, (pt.x, pt.y))
                           
                            ax =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ax, (pt.x, pt.y))
                            ay = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ay, (pt.x, pt.y))
                            at = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Atot, (pt.x, pt.y))
                            
                            ens = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, (pt.x, pt.y))
                            tns = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, (pt.x, pt.y))
                            ss = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceShearStress, (pt.x, pt.y))
                            rss = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, (pt.x, pt.y))

                            pe = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PExcess, (pt.x, pt.y))
                            pa = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PActive, (pt.x, pt.y))
                            pst = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PSteady, (pt.x, pt.y))
                            pw = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.PWater, (pt.x, pt.y))
                            
                            su = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Suction, (pt.x, pt.y))
                            esu = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.EffSuction, (pt.x, pt.y))
                            
                            if ux == 'not found':
                                print("results for {} {} ({} {}) not found".format(step.Name.value, pt.name, pt.x, pt.y))
                            if ux != 'not found':
                                print("results for {} {} ({} {}) retrieved".format(step.Name.value, pt.name, pt.x, pt.y))
                                # add filters in here if necessary
                                iPhaseName.append(phase.Name.value)
                                iPhaseIdent.append(phase.Identification.value)
                                
                                iX.append(x)
                                iY.append(y)
                                
                                iMat.append(mat)
                                iLocName.append (pt.name)
                                
                                iUx.append(ux)
                                iUy.append(uy)
                             
                                iUt.append(ut)
                                
                                iPUx.append(pux)
                                iPUy.append(puy)
                                iPUt.append(put)
                                
                                iU1.append(u1)
                                iU2.append(u2)
                              
                                iVx.append(vx)
                                iVy.append(vy)
                                iVt.append(vt)
                                
                                iAx.append(ax)
                                iAy.append(ay)
                                iAt.append(at)
                                
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
                            print ('Exception reading Interface results in phase:' + phase.Name.value + ' step:' + step.Name.value)
                            break
        columns ='Phase,PhaseIdent,LocName,X(m),Y(m),MaterialID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Vx(m/s),Vy(m/s),Vt(m/s),Ax(m/s2),Ay(m/s2),At(m/s2),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)'
        formats = '{},{},{},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, loc, float(x), float(y), float(mat), float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(u1), float(u2), float(vx), float(vy), float(vt), float(ax), float(ay), float(at), float(ens), float(tns), float(ss), float(rss), float(pe), float(pa), float(pst), float(pw), float(su), float(esu))
                for pname, pident, loc, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, vx, vy, vt, ax, ay, at, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iMat, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iVx, iVy, iVt, iAx, iAy, iAt, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
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
                file.writelines([formats.format(pname, pident, loc, float(x), float(y), float(mat), float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(u1), float(u2), float(vx), float(vy), float(vt), float(ax), float(ay), float(at), float(ens), float(tns), float(ss), float(rss), float(pe), float(pa), float(pst), float(pw), float(su), float(esu))
                for pname, pident, loc, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, vx, vy, vt, ax, ay, at, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iMat, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iVx, iVy, iVt, iAx, iAy, iAt, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, loc, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, vx, vy, vt, ax, ay, at, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iLocName, iX, iY, iMat, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iVx, iVy, iVt, iAx, iAy, iAt, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(loc)
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
                row.append(vx)
                row.append(vy)
                row.append(vt)
                row.append(ax)
                row.append(ay)
                row.append(at)
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
        
        print('getInterfaceResultsByPointsByStep Done') 
    def getSoilResultsByPoints(self,
                               filePoints=None,
                               fileOut=None,
                               tableOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               mode = 'new'
                               ):
        
        NotFound = ['not found','nan','Nan']

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
        
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilResultsByPoints'
                
        if filePoints:
            fpoint = open(filePoints, "r")

            while True:
                in_line = fpoint.readline()
                if in_line == "":
                    break
                print(in_line)
                try:
                    [name, nx, ny] = in_line.split(',')
                    self.NodeList.append(self.PointXY(name, nx, ny))
                except Exception as e:
                    print (str(e))
                    return


            fpoint.close()
        columns = 'Phase,PhaseIdent,locName,locX(m),locY(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa)'  
        formats = '{},{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        print('FileOut=', w.fileOut)

        for phase in self.phaseOrder:
            print('Getting soil results ' + phase.Identification.value)
                                 
            for pt in self.NodeList:

                try:
                    mat = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.MaterialID, (pt.x, pt.y))
                    el = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.ElementID, (pt.x, pt.y))
                    ux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Ux, (pt.x, pt.y))
                    uy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Uy, (pt.x, pt.y))
                    ut = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Utot, (pt.x, pt.y))
                    pux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUx, (pt.x, pt.y))
                    puy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUy, (pt.x, pt.y))
                    put = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUtot, (pt.x, pt.y))
                    esx = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigxxE, (pt.x, pt.y))
                    esy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigyyE, (pt.x, pt.y))
                    esz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigzzE, (pt.x, pt.y))
                    ep1 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective1, (pt.x, pt.y))
                    ep2 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective2, (pt.x, pt.y))
                    ep3 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective3, (pt.x, pt.y))  
                    pe = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PExcess, (pt.x, pt.y))
                    pa = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PActive, (pt.x, pt.y))
                    ps = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PSteady, (pt.x, pt.y))
                    pw = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PWater, (pt.x, pt.y))
                    su = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Suction, (pt.x, pt.y))
                    
                    w.rowsOut = [formats.format(phase.Name.value, phase.Identification.value, pt.name, pt.x, pt.y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa,ps,pw,su)]                    
                    w.writeOutput()
     
                except:
                    print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
                    print (phase.Name.value, phase.Identification.value, pt.name, pt.x, pt.y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa,ps,pw,su)
                
        print('getSoilResultsByPoint Done')

