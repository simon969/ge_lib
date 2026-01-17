from .Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2

class Plaxis2dResultsSSIA (Plaxis2dResultsConnectV2):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResultsSSIA, self).__init__(server, host, port, password)
    def getSelectedInterfaceResultsBySinglePointsByStep (self,
                        filePoints=None,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None,
                        stepList=None,
                        fileSteps=None
                        ):
        
        
        
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
  
        if not filePoints is None:
            self.loadXYNodeList(filePoints)
        
        if not stepList is None:
            step_list = stepList.split(",")
        
        if not fileSteps is None:
            self.loadStepList(fileSteps)
            
        if stepList is None and fileSteps is None:
            step_list = []
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getSelectedInterfaceResultsByPointsStep'  
        
        print('FileOut=', fileOut)

        # initialize data for lists
        iPhaseName = []
        iStepName = []
        iStepTime = []
        
        iLocName = []
        
        iY = []
        iX = []
        iAx = []
        iEffNormalStress = []
        iShearStress = []
        
        for phase in self.phaseOrder:

            print("Getting Interface results for Phase:{}".format(phase.Name.value))
            
            for step in phase:
            
                if self.StepList is None or step.Name.value in self.StepList:
                    reached = step.Reached
                    print("Getting Interface results for Step:{} {}s".format(step.Name.value, reached.Time))
                    
                    
                    for pt in self.NodeList:
                        
                        print("Getting Interface results for Node:{}".format(pt.name))
                        
                        try:
                           
                            ax =  self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.Ax, (pt.x, pt.y))
                            ens = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, (pt.x, pt.y))
                            ss = self.g_o.getsingleresult(step, self.g_o.ResultTypes.Interface.InterfaceShearStress, (pt.x, pt.y))
                            
                            if ax == 'not found':
                                print("results for {} {} ({} {}) not found".format(step.Name.value, pt.name, pt.x, pt.y))
                            
                            if ax != 'not found':
                                print("results for {} {} ({} {}) retrieved".format(step.Name.value, pt.name, pt.x, pt.y))
                                # add filters in here if necessary
                                iPhaseName.append(phase.Name.value)
                                iStepName.append(step.Name.value) 
                                iStepTime.append(reached.Time.value)

                                iLocName.append(pt.name)
                                iX.append(pt.x)
                                iY.append(pt.y)
                                
                                iLocName.append (pt.name)
                                
                                iAx.append(ax)
                                
                                iEffNormalStress.append(ens)
                                iShearStress.append(ss)
                                
                        except:
                            print ('Exception reading Interface results in phase:' + phase.Name.value + ' step:' + step.Name.value)
                            break
        columns ='Phase,Step,LocName,X(m),Y(m),Ax(m/s2),Eff NormalStress (kPa). ShearStress (kPa)'
        formats = '{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            print('Outputing to file ', fileOut, '....')
            columns += '\n'
            formats += '\n'
                        
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, sname, loc, float(x), float(y), float(ax), float(ens), float(ss))
                for pname, sname, stime, loc, x, y, ax, ens, ss in zip(iPhaseName, iStepName, iStepTime, iLocName, iX, iY, iAx, iEffNormalStress, iShearStress)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, sname, stime, loc, x, y, ax, ens, ss in zip(iPhaseName, iStepName, iStepTime, iLocName, iX, iY, iAx, iEffNormalStress, iShearStress):
                row = []
                row.append(pname)
                row.append(sname)
                row.append(stime)
                row.append(loc)
                row.append(x)
                row.append(y)
                row.append(ax)
                row.append(ens)
                row.append(ss)
                self.insertValues(row)
        
        print('getSelectedInterfaceResultsByPointsByStep Done') 
    
    def getSelectedInterfaceResultsByPointsBySteps(self,
                    fileOut=None,
                    filePoints=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None,
                    stepList=None,
                    fileSteps=None
                    ):
        
        self.s_o.allow_caching = False
        
        self.s_o.enable_logging()
        
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
           
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1
        
        if not filePoints is None:
            self.loadXYNodeList(filePoints)
        
        if not stepList is None:
            self.StepList = stepList.split(",")
        
        if not fileSteps is None:
            self.loadStepList(fileSteps)
            
        if stepList is None and fileSteps is None:
            self.StepList = []
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResults'

        print('FileOut=', fileOut)
        
        
        # init data for lists
        iPhaseName = []
        iStepName = []

        
        iLocName = []
        iY = []
        iX = []

       
        
        iEffNormalStress = []
        iShearStress = []
        
        print (self.StepList)
        
        
        for phase in self.phaseOrder:
            print("Getting Interface results for {}".format(phase.Name.value))
            
            self.setSteps (phase)
            
            for step in self.Steps:
                # print("        Interface results for {}".format(step.Name.value))
                    print("Request Interface results for {}".format(step.Name.value))
                   
                    try:
                        interX = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.X, 'node')
                        if interX == "not found":
                            break
                        interY = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.Y, 'node')
                        interEffNormalStress = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node')
                        interShearStress = self.g_o.getresults(step, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node')
                        counter = 0
                        reached = step.Reached
                        for x, y, ens, ss in zip(
                                interX, 
                                interY, 
                                interEffNormalStress, 
                                interShearStress):
                            p = self.getXYNodeListItem(x, y) 
                            if (p != None):
                                iPhaseName.append(phase.Name.value)
                                iStepName.append(step.Name.value)
                                iLocName.append(p.name)
                                iX.append(x)
                                iY.append(y)
                                iEffNormalStress.append(ens)
                                iShearStress.append(ss)
                                counter += 1
                        print("Receive Interface results for {} {} rows added".format(step.Name.value, counter))
                        self.logger.info("Received Interface results for {} {} rows added".format(step.Name.value, counter))
                    except Exception as e:
                        print ("...exception reading Interface results {0} {1} {2}".format(phase.Name.value, step.Name.value, str(e)))
                        self.logger.error('...exception reading Interface results  '+ str(e))
                    
        columns = "Phase,Step,LocName,X(m),Y(m),Eff NormalStress (kPa),Shear Stress (kPa)"
        formats = "{},{},{},{:2f},{:2f},{:2f},{:2f}"
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, sname, loc, x, y, ens, ss)
                                 for pname, sname, loc, x, y, ens, ss 
                                 in zip(iPhaseName, iStepName, iLocName, iX, iY, iEffNormalStress, iShearStress)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, sname, loc, x, y, ens, ss in zip(iPhaseName, iStepName, iLocName, iX, iY, iEffNormalStress, iShearStress):
                                     row = []
                                     row.append(pname)
                                     row.append(sname)
                                     row.append(loc)
                                     row.append(x)
                                     row.append(y)
                                     row.append(ens)
                                     row.append(ss)
                                     self.insertValues(row)
            
        print('getSelectedInterfaceResultsByPointsBySteps Done') 
  

