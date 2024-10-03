from .PlaxisScripting import Status
from .Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2
from .OutputWriter import GetWriter


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
    

    def getInterfaceDynamicSingleResultsByPointsBySteps (self,  
                                                  steps,
                                                  PhaseName,
                                                  fileOut,
                                                  tableOut=None,
                                                  mode = 'new'
                        ):
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceDynamicResults'  

        columns ='PhaseName,StepName,StepTime,LocName,X(m),Y(m),Ax(m/s2),Ay(m/s2),Eff NormalStress (kPa), ShearStress (kPa)'
        formats = '{},{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        for step in steps:
                # initialize data for lists
                iPhaseName = []
                iStepName = []
                iStepTime = []
                iLocName = []
                iY = []
                iX = []
                iAx = []
                iAy = []
                iEffNormalStress = []
                iShearStress = []
                
                reached = step.Reached
                self.logger.info("Request Interface dynamic single results for phase:{} step:{} time:{}".format(PhaseName, step.Name.value, reached.Time))                    
                for pt in self.NodeList:
                    
                    try:
                        ax =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ax, (pt.x, pt.y))
                        ay =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ay, (pt.x, pt.y))
                        ens = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, (pt.x, pt.y), self.result_smoothing)
                        ss = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceShearStress, (pt.x, pt.y), self.result_smoothing)
                        
                        self.logger.info("Received Interface dynamic results for phase:{} step:{} time:{} location:{} ({},{})".format(PhaseName, step.Name.value, reached.Time, pt.name, pt.x, pt.y))
                        iPhaseName.append(PhaseName)
                        iStepName.append(step.Name.value) 
                        iStepTime.append(reached.Time.value)
                        iLocName.append(pt.name)
                        iX.append(pt.x)
                        iY.append(pt.y)
                        iAx.append(ax)
                        iAy.append(ay)
                        iEffNormalStress.append(ens)
                        iShearStress.append(ss)
                            
                    except Exception as e:
                        msg = str(e)
                        self.logger.error('...exception reading Interface dynamic single results '+ msg)
                        if 'Invalid step or phase' in msg:                         
                            break
                        else:
                            continue
                
                if len(iPhaseName)>0:
                    w.rowsOut = [formats.format(pname, sname, stime, lname, x, y, ax, ay, ens, ss)
                                        for pname, sname, stime, lname, x, y, ax, ay, ens, ss 
                                        in zip(iPhaseName, iStepName, iStepTime, iLocName, iX, iY, iAx, iAy, iEffNormalStress, iShearStress)]                    
                    w.writeOutput()
        print('getInterfaceDynamicSingleResultsByPointsBySteps Done') 
        return Status.ELEMENT_PROCESSED
    
    def getInterfaceDynamicResultsByPointsBySteps(self,  
                                                  steps,
                                                  PhaseName,
                                                  fileOut,
                                                  tableOut=None,
                                                  mode = 'new'
                                                
                                                ):
        
        self.s_o.allow_caching = False
        
        self.s_o.enable_logging()
            
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceDynamicResults'
     
        columns ='PhaseName,StepName,StepTime,LocName,X(m),Y(m),Ax(m/s2),Ay(m/s2),Eff NormalStress (kPa), ShearStress (kPa)'
        formats = '{},{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
                    
        for step in steps:
                
                # initialize data for lists
                iPhaseName = []
                iStepName = []
                iStepTime = []
                iLocName = []
                iY = []
                iX = []
                iAx = []
                iAy = []
                iEffNormalStress = []
                iShearStress = []

                reached = step.Reached
               
                self.logger.info("Request Interface dynamic results for phase:{} step:{}".format(PhaseName, step.Name.value))             
                
                try:
                    interX = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.X, 'node')
                    interY = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.Y, 'node')
                    interEffNormalStress = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node', self.result_smoothing)
                    interShearStress = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node', self.result_smoothing)
                    interAx = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.Ax, 'node', self.result_smoothing)
                    interAy = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.Ay, 'node', self.result_smoothing)
                   
                    counter = 0
                   
                    for x, y, ens, ss, ax, ay in zip(
                            interX, 
                            interY, 
                            interEffNormalStress, 
                            interShearStress,
                            interAx, 
                            interAy): 
                        add_node = True
                        loc_name='none'
                        if self.NodeList:
                            add_node = False
                            p = self.getXYNodeListItem(x, y) 
                            if (p != None):
                                loc_name = p.name
                                add_node = True
                        if add_node:
                            iPhaseName.append(PhaseName)
                            iStepName.append(step.Name.value)
                            iStepTime.append(reached.Time.value)
                            iLocName.append(loc_name)
                            iX.append(x)
                            iY.append(y)
                            iEffNormalStress.append(ens)
                            iShearStress.append(ss)
                            iAx.append (ax)
                            iAy.append (ay)
                            counter += 1
                    
                    self.logger.info("Received Interface dynamic results for {} {} rows added".format(step.Name.value, counter))
                
                except Exception as e:
                    self.logger.error('...exception reading Interface dynamic results  '+ str(e))
                    continue
                                
                if len(iPhaseName)>0:
                    w.rowsOut = [formats.format(pname, sname, stime, lname, x, y, ax, ay, ens, ss)
                                        for pname, sname, stime, lname, x, y, ax, ay, ens, ss 
                                        in zip(iPhaseName, iStepName, iStepTime, iLocName, iX, iY, iAx, iAy, iEffNormalStress, iShearStress)]                    
                    w.writeOutput()

        print('getInterfaceDynamicResultsByPointsBySteps Done') 
        return Status.ELEMENT_PROCESSED


    def getSoilDynamicResultsByPointsBySteps(self,
                    steps,
                    PhaseName,
                    fileOut=None,
                    tableOut=None,
                    mode = 'new'
                    ):
        
        self.s_o.allow_caching = False
        
        self.s_o.enable_logging()
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilDynamicResults'

        columns ='PhaseName,StepName,StepTime,LocName,X(m),Y(m),Ax(m/s2),Ay(m/s2)'
        formats = '{},{},{},{},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
               
        for step in steps:
                self.logger.info("Request Soil dynamic results for {}".format(step.Name.value))
                # initialize data for lists
                sPhaseName = []
                sStepName = []
                sStepTime = []
                sLocName = []
                sY = []
                sX = []
                sAx = []
                sAy = []
                            
                try:
                    soilX = self.g_o.getresults(step, self.g_o.ResultTypes.Soil.X, 'node')
                    soilY = self.g_o.getresults(step, self.g_o.ResultTypes.Soil.Y, 'node')
                    soilAx = self.g_o.getresults(step, self.g_o.ResultTypes.Soil.Ax, 'node', self.result_smoothing)
                    soilAy = self.g_o.getresults(step, self.g_o.ResultTypes.Soil.Ay, 'node', self.result_smoothing)
                    reached = step.Reached
                    counter = 0
                
                    for x, y, ax, ay in zip(
                            soilX, 
                            soilY, 
                            soilAx, 
                            soilAy): 
                        add_node = True
                        loc_name='none'
                        if self.NodeList:
                            add_node = False
                            p = self.getXYNodeListItem(x, y) 
                            if (p != None):
                                loc_name = p.name
                                add_node = True
                        if add_node:
                            sPhaseName.append(PhaseName.value)
                            sStepName.append(step.Name.value)
                            sStepTime.append(reached.Time.value)
                            sLocName.append(loc_name)
                            sX.append(x)
                            sY.append(y)
                            sAx.append (ax)
                            sAy.append (ay)
                            counter += 1
                    
                    self.logger.info("Received Soil dynamic results for {} {} rows added".format(step.Name.value, counter))
                    
                    if len (sPhaseName) > 0: 
                        w.rowsOut = [formats.format(pname, sname, stime, lname, x, y, ax, ay)
                                            for pname, sname, stime, lname, x, y, ax, ay 
                                            in zip(sPhaseName, sStepName, sStepTime, sLocName, sX, sY, sAx, sAy)]                    
                        w.writeOutput()
                except Exception as e:
                    self.logger.error('...exception reading Soil dynamic results  '+ str(e))
                    continue
        print('getSoilDynamicResultsByPointsBySteps Done') 
        return Status.ELEMENT_PROCESSED
    
    def getSoilDynamicSingleResultsByPointsBySteps (self,
                        steps,
                        PhaseName,
                        fileOut=None,
                        tableOut=None,
                        mode='new'
                        ):
        
        
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSoilDynamicResults'  

        columns ='PhaseName,StepName,StepTime,LocName,X(m),Y(m),Ax(m/s2),Ay(m/s2)'
        formats = '{},{},{},{},{:2f},{:2f},{:2f},{:2f}'
        
        w = GetWriter (fileOut, tableOut, columns, formats, self.logger, mode)
        
        for step in steps:
                # initialize data for lists
                sPhaseName = []
                sStepName = []
                sStepTime = []
                sLocName = []
                sY = []
                sX = []
                sAx = []
                sAy = []
                             
                reached = step.Reached
                print("Getting Soil dynamic single results for Phase:{} Step:{} Time:{}".format(PhaseName, step.Name.value, reached.Time))
                                    
                for pt in self.NodeList:
                    
                    try:
                        
                        ax =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Soil.Ax, (pt.x, pt.y), self.result_smoothing)
                        ay =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Soil.Ay, (pt.x, pt.y), self.result_smoothing)
                        
                        print("results for {} {} ({} {}) retrieved".format(step.Name.value, pt.name, pt.x, pt.y))
                        # add filters in here if necessary
                        sPhaseName.append(PhaseName.value)
                        sStepName.append(step.Name.value) 
                        sStepTime.append(reached.Time.value)
                        sLocName.append(pt.name)
                        sX.append(pt.x)
                        sY.append(pt.y)
                        sAx.append(ax)
                        sAy.append(ay)
                            
                    except Exception as e:
                        msg = str(e)
                        self.logger.error('...exception reading Soil dynamic single results  '+ msg)
                        if 'Invalid step or phase' in msg:                         
                            break
                        else:
                            continue
            
                if len(sPhaseName)>0:            
                    w.rowsOut = [formats.format(pname, sname, stime, lname, x, y, ax, ay)
                                        for pname, sname, stime, lname, x, y, ax, ay 
                                        in zip(sPhaseName, sStepName, sStepTime, sLocName, sX, sY, sAx, sAy)]                    
                    w.writeOutput()
        
        print('getSoilDynamicSingleResultsByPointsByStep Done') 
        return Status.ELEMENT_PROCESSED