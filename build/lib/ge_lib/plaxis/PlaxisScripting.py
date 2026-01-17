# import imp
import os.path
import math
import logging
# import time
# from io import StringIO

import pypyodbc as pyodbc

from .plxscripting_py311.easy import new_server
from .plxscripting_py311.logger import Logger
from .plxscripting_py311.error_mode import ErrorMode

# Plaxis Server connection parameters
REQUEST_TIMEOUT = 3600 
TIMEOUT = 10.0
RESULT_SMOOTHING = False
XYZ_COORD_FORMAT = "{0:.3f},{1:.3f},{2:.3f}"
XY_COORD_FORMAT = "{0:.3f},{1:.3f}"

class CustomLoggingFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
class Status:
        CONNECTION_LOST = -2
        FAIL = -1
        READY = 0
        PROCESSING = 1
        SUCCESS = 2 
        ELEMENT_PROCESSED = 3
        
# path_pypyodbc = path_geo3523 + r'\pypyodbc-1.3.5'
# found_module = imp.find_module('pypyodbc', [path_pypyodbc])
# pypyodbc = imp.load_module('pypyodbc', *found_module)
def _is_file_like(obj):
    
    """Check if object is file like

    Returns
    -------
    bool
        Return True if obj is file like, otherwise return False
    """

    if not (hasattr(obj, 'read') or hasattr(obj, 'write')):
        return False

    if not hasattr(obj, "__iter__"):
        return False

    return True

class PlaxisScripting (object):
    def __init__(self, ps = None, host=None, port=None, password=None, task_log = None, plx_log = None):
        print ('getting Connected...')      
        
        self.result_smoothing = RESULT_SMOOTHING

        if ps is None:
            if password is None:
                password = ''
            self.s_o, self.g_o = new_server(address=host, port=port, timeout=TIMEOUT, request_timeout=REQUEST_TIMEOUT, password=password)
            
            if task_log is not None:
                if _is_file_like(task_log):
                    hdlr = logging.StreamHandler (task_log)
                else:
                    hdlr = logging.FileHandler (task_log)
            else:
                hdlr = logging.StreamHandler ()
            
            # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(CustomLoggingFormatter())
            self.logger = logging.getLogger(host + '_PlaxisResults')
            self.logger.addHandler(hdlr)
            self.logger.setLevel(logging.INFO)
            
            if plx_log is not None:
                if _is_file_like(plx_log):
                    self.s_o.enable_logging(buffer=plx_log)
                else:
                    self.s_o.enable_logging(path=plx_log)    
            
            if (self.s_o.is_2d is False and self.s_o.is_3d is False ):
                print ('..no connection')     
                raise ValueError("Not Connected")
           
            else:
                print ('Connected:', host, port, self.s_o.name, self.s_o.major_version, self.s_o.minor_version, 'Is2d=', self.s_o.is_2d, 'Is3d=', self.s_o.is_3d)        
            
            self.NodeList = {}
        else:
            self.s_o = ps.s_o
            self.g_o = ps.g_o
            self.logger = ps.logger
            self.NodeList = ps.NodeList
            self.result_smoothing = ps.result_smoothing

    def match(self, **kwargs):
        return all(getattr(self, key) == val for (key, val) in kwargs.items())     
    def connect (self, host, port, password):
        self.s_o, self.g_o = new_server(address=host, port=port, password=password)
        print ('Connected:', host, port, self.s_o.name, self.s_o.major_version, self.s_o.minor_version, 'Is2d=', self.s_o.is_2d, 'Is3d=', self.s_o.is_3d)
    def is_connected(self):
        if (self.s_o is not None):
            return self.s_o.active
        return False    
    def clearNodeList (self):    
        self.NodeList = []
    def printNodeListXYZ (self):
        formats =  '{},{:.3f},{:.3f},{:.3f}'
        for point in self.NodeList:
            print (formats.format(point.name, point.x, point.y, point.z))
            
           # print(point.name, point.x, point.y, point.z)
    def add_points_list(self, csv_lst:list[str]):
        count = 0
        if csv_lst is None:
            return count
        for line in csv_lst:
            items = line.split(',')
            if (len(items) == 4):
                self.addXYZNode (items[0],items[1],items[2],items[3])
                count += 1
            else:
                if (len(items) == 3):
                    self.addXYNode (items[0],items[1],items[2])
                    count += 1
                else:
                    return count   
    
    class PointXY(object):
        def __init__(self, name, x, y):
                self.name = name
                self.x = float(x)
                self.y = float(y)
                self.coord = XY_COORD_FORMAT.format(float(x),float(y))
    class PointXYZ(object):
        def __init__(self, name, x, y, z):
                self.name = name
                self.x = float(x)
                self.y = float(y)
                self.z = float(z)
                self.coord = XYZ_COORD_FORMAT.format(float(x),float(y),float(z))
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False  
    
    def isfloat(self, s, value_false):
        try:
            if s == 'NaN':
                return value_false
            if s == 'not found':
                return value_false
            else:
                f = float(s)
                print('float:', f)
                return f

        except ValueError:
            return value_false
    def getPhaseList(self):
        return list(map(lambda x: x.Name.value, self.g_o.Phases))
    def getStepList(self):
        return list(map(lambda x: x.Name.value, self.Steps))
    
    def getStepId (self, steps, stepName):
        count = 0
        print('looking for step:' + stepName)
        for step in steps:
            if step.Name.value == stepName:
                print('found...', count)
                return count
            count += 1
        return -1
    
    def getPhaseInt(self, 
                    phaseName):
        phases = self.getPhaseList()
        return phases.index(phaseName)
    
        # count = 0
        # print('looking for phase:' + phaseName)
        # for phase in self.g_o.Phases:
        #     if phase.Name.value == phaseName:
        #         print('found...', count)
        #         return count
        #     count += 1
        # return -1
    def setSteps(self, 
                 phase,  
                 sstepOrder:list=None, 
                 offsets:list=None):
        
        self.Steps = [] 
        steps = phase[:]
               
        if sstepOrder: 
            sstep_all =list(map(lambda x: x.Name.value, steps))
            offsets = [sstep_all.index(i) for i in sstepOrder]
        
        if not offsets:
            offsets = list (range (1,  len (steps), 1))
        
        accessed_mapping = map(steps.__getitem__, offsets)
        self.Steps = list(accessed_mapping)
 
            
         
    # def setSteps(self, 
    #              phase):
        
    #     self.Steps = []
        
    #     print("{0} finding selected steps {1}".format(phase.Name.value,self.g_o.count(phase.Steps)))
        
    #     steps = phase[:]
        
    #     print ("{}".format(len(steps)))
 
    #     for step in steps:
    #         print ("{}".format(step))
    #         if not self.StepList or step in self.StepList:
    #             self.Steps.append(step)
    #             print("Added {0} {1}".format(step.Name, step))
    def setOutput (self, fileOut, tableOut, columns, formats):
        
        self.fileOut = fileOut
        self.tableOut = tableOut
        self.rowsOut = []

        self.getConnected (fileOut)
        self.createTable(tableOut, columns, formats)
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
           
    
    def writeOutput (self, clear=True):
        print('Outputting rows to file ', self.fileOut, '....')
        with open(self.fileOut, "w") as fp:
            fp.write("\n".join(str(row) for row in self.rowsOut))    
        if (clear==True):
            self.rowsOut = []

    def setPhaseOrder(self,
                      sphaseOrder=None,
                      sphaseStart=None,
                      sphaseEnd=None):

        self.phaseOrder = []
        
        if sphaseOrder == 'All':
            sphaseOrder=None 
        
        if sphaseOrder is None:
            if sphaseStart is None and sphaseEnd is None:
                self.phaseOrder = self.g_o.Phases[:]
                if self.phaseOrder is not None:
                    print ('All phases added to phaseOrder')

            if sphaseStart is None and sphaseEnd is not None:
                id = self.getPhaseInt(sphaseEnd)
                self.phaseOrder = self.g_o.Phases[:id]
                if self.phaseOrder is not None:
                    print ('All phases up to', sphaseEnd, ' added')
    

            if sphaseStart is not None and sphaseEnd is None:
                id = self.getPhaseInt(phaseName=sphaseStart)
                self.phaseOrder = self.g_o.Phases[id:]
                if self.phaseOrder is not None:
                    print ('All phases from ', sphaseStart, ' added')

            if sphaseStart is not None and sphaseEnd is not None:
                id = self.getPhaseInt(sphaseStart)
                id2 = self.getPhaseInt(sphaseEnd)
                self.phaseOrder = self.g_o.Phases[id:id2 + 1]
                if self.phaseOrder is not None:
                    print ('All phases from ', sphaseStart, ' to ', sphaseEnd, ' added')
                    
        if sphaseOrder is not None:
            aphaseOrder = sphaseOrder.split(",")
            for sphase in aphaseOrder:
                id = self.getPhaseInt(sphase)
                self.phaseOrder.append(self.g_o.Phases[id])
                print('phase:', sphase ,' added')
        
        if self.phaseOrder is not None:
                    print ('phaseOrder initialised with', len(self.phaseOrder) , ' no. phases')   

                    
    def setRange (self,
                  xMin=None,
                  xMax=None,
                  yMin=None,
                  yMax=None,
                  zMin=None,
                  zMax=None
                  ):
        global g_xMin, g_xMax, g_yMin, g_yMax, g_zMin, g_zMax
        g_xMin = xMin
        g_xMax = xMax
        g_yMin = yMin
        g_yMax = yMax
        g_zMin = zMin
        g_zMax = zMax
        
    def printRange(self):
        print ('g_xMin',g_xMin, 
               'g_xMax',g_xMax,
               'g_yMin',g_yMin,
               'g_yMax',g_yMax,)
               
    def inRange (self,
                 x_val=None,
                 y_val=None,
                 z_val=None
                 ):
                 
        xMinRangeOk = True 
        xMaxRangeOk = True 
        yMinRangeOk = True
        yMaxRangeOk = True
        zMinRangeOk = True
        zMaxRangeOk = True
        
      #  self.printRange()
        
      #  print ('x_val', x_val,
      #        'y_val', y_val)
               
        if g_xMin is not None and x_val is not None:
            if x_val >= g_xMin:
                xMinRangeOk = True 
            else:
                xMinRangeOk = False  
        else:
            xMinRangeOk = True 
        
        if g_yMin is not None and y_val is not None:
            if y_val >= g_yMin:
                yMinRangeOk = True 
            else:
                yMinRangeOk = False
        else:
            yMinRangeOk = True 
        
        if g_xMax is not None and x_val is not None:
            if x_val <= g_xMax:
                xMaxRangeOk = True 
            else:
                xMaxRangeOk = False  
        else:
            xMaxRangeOk = True 
        
        if g_yMax is not None and y_val is not None:
            if y_val <= g_yMax:
                yMaxRangeOk = True 
            else:
                yMaxRangeOk = False
        else:
            yMaxRangeOk = True 
           
        if g_zMax is not None and z_val is not None:
            if z_val <= g_zMax:
                zMaxRangeOk = True 
            else:
                zMaxRangeOk = False
        else:
            zMaxRangeOk = True     
        
        if g_zMin is not None and z_val is not None:
            if z_val >= g_zMin:
                zMinRangeOk = True 
            else:
                zMinRangeOk = False
        else:
            zMinRangeOk = True 
            
        if xMinRangeOk and xMaxRangeOk and yMinRangeOk and yMaxRangeOk and zMinRangeOk and zMaxRangeOk:
           # print ('inRange x_val', x_val,
           #     'y_val', y_val)
            return True 
        else:
            return False  
            
  
    def setXYZNodeList (self,
                     xMin=0.0, xMax=0.0,
                     yMin=0.0, yMax=0.0,
                     zMin=0.0, zMax=0.0):
        
        phase = self.phaseOrder[0]
        
        self.setRange(xMin, xMax,
                      yMin, yMax, 
                      zMin, zMax)
        soilN = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.NodeID, 'node')
        soilX = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node')
        soilY = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node')
        soilZ = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Z, 'node')
        
        print('Coordinates retrieved for Phase ', phase.Name.value)
        
        for x, y, z, n in zip(soilX, soilY, soilZ, soilN):
            if self.inRange (x_val = x, y_val = y, z_val = z) == True:
                self.addXYZNode(n, x, y, z)
                print ('Added node ',n,' at (', x, y, z, ')')
        print (len(self.NodeList), ' nodes added to NodeList')   
        
    def setXYNodeList (self,
                     xMin=0.0, xMax=0.0,
                     yMin=0.0, yMax=0.0):
        phase = self.phaseOrder[0]
                
        self.setRange(xMin, xMax,
                      yMin, yMax, 
                      zMin = None, zMax = None)
        soilN = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.NodeID, 'node')
        soilX = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node')
        soilY = self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node')
               
        print('Coordinates retrieved for Phase ', phase.Name.value)
        
        for n, x, y in zip(soilN, soilX, soilY):
            if self.inRange (x_val = x, y_val = y, z_val = None) == True:
                self.addXYNode(n, x, y)
                print ('Added node at (', x, y, ')')
        print (len(self.NodeList), ' nodes added to NodeList')          
    def addXYNode(self, 
                    name,
                    x = 0.0, 
                    y = 0.0):
        pnt = self.PointXY(name, x, y)
        self.NodeList[pnt.coord] = pnt
        print ('Added node at (',name, x, y, ')')
    
    def addXYZNode(self,
                    name,
                    x=0.0,
                    y=0.0,
                    z=0.0):
                
        pnt = self.PointXYZ(name, x, y, z)
        self.NodeList[pnt.coord] = pnt
        print ('Added node at (',name, x, y, z, ')')
    def createXYArc(self,
                      name= None,
                      xCen= 0.00,
                      yCen= 0.00,
                      rad= 0.00,
                      degStart = 0.00,
                      degEnd = 0.00,
                      degStep = 0.00
                      ):
        ref = name
        counter = 0
        arc_array = []
        
        x = 0.0
        y = 0.0
        
        arc_array = self.getArcCoordsArray(xCen,
                                      yCen,
                                      rad,
                                      degStart,
                                      degEnd,
                                      degStep)
        
        for coord in arc_array:
            counter += 1
            if name is None:
                ref = counter 
            x, y = coord
            self.addXYNode(ref, x, y)
        print ('Added node at (',ref, x, y, ')')    
    
    def createXYZArc_XYPlane(self,
                      name= None,
                      xCen= 0.00,
                      yCen= 0.00,
                      zCen= 0.00,
                      rad= 0.00,
                      degStart = 0.00,
                      degEnd = 0.00,
                      degStep = 0.00
                      ):
        ref = name
        counter = 0
        arc_array = []
        
        x = 0.0
        z = 0.0
        
        arc_array = self.getArcCoordsArray(xCen,
                                      yCen,
                                      rad,
                                      degStart,
                                      degEnd,
                                      degStep)
        
        for coord in arc_array:
            counter += 1 
            if name is None:
                ref = counter
            x, y = coord
            self.addXYZNode(ref, x, y, zCen)
        print ('Added node at (',ref, x, y, zCen, ')')
    
    def createXYZArc_XZPlane(self,
                      name= None,
                      xCen= 0.00,
                      yCen= 0.00,
                      zCen = 0.00,
                      rad= 0.00,
                      degStart = 0.00,
                      degEnd = 0.00,
                      degStep = 0.00
                      ):
        ref = name
        counter = 0
        arc_array = []
        
        x = 0.0
        z = 0.0
        
        arc_array = self.getArcCoordsArray(xCen,
                                      zCen,
                                      rad,
                                      degStart,
                                      degEnd,
                                      degStep)
        
        for coord in arc_array: 
            counter += 1
            x, z = coord
            if name is None:
                ref = counter 
            self.addXYZNode(ref, x, yCen, z)
        print ('Added node at (',ref, x, yCen, z, ')')
    
    def createXYZArc_YZPlane(self,
                      name= None,
                      xCen= 0.00,
                      yCen= 0.00,
                      zCen = 0.00,
                      rad= 0.00,
                      degStart = 0.00,
                      degEnd = 0.00,
                      degStep = 0.00
                      ):
        ref = name
        counter = 0
        arc_array = []
        
        y = 0.0
        z = 0.0
        
        arc_array = self.getArcCoordsArray(yCen,
                                      zCen,
                                      rad,
                                      degStart,
                                      degEnd,
                                      degStep)
        
        for coord in arc_array:
            counter += 1
            y, z = coord
            if name is None:
                ref = counter 
            self.addXYZNode (ref, xCen, y, z)
        print ('Added node at (',name, xCen, y, z, ')')    
    
    def getArcCoordsArray(self,
                      iCen= 0.00,
                      jCen= 0.00,
                      rad= 0.00,
                      degStart = 0.00,
                      degEnd = 0.00,
                      degStep = 0.00
                      ):
        i_coord = 0.0
        j_coord = 0.0
        coords = []                  
        
        # direction vector for 0 degree (j=1; i=0)
        # diection vector for 90 degree (j=0, i=1)
        
        deg = degStart
        
        while (deg < degEnd):
            i_coord  = iCen + rad * math.sin(math.radians(deg))
            j_coord =  jCen + rad * math.cos(math.radians(deg))
            coord = (i_coord, j_coord)  
            coords.append(coord)
            deg = deg + degStep
        return coords;
                          
    def createXYZCylinder(self,
                     name = None,
                     rad= 0.00,
                     degStart = 0.00,
                     degEnd = 0.00,
                     degStep = 0.00,
                     xMin= 0.0, xMax= 0.0, xStep= 0.0,
                     yMin= 0.0, yMax= 0.0, yStep= 0.0,
                     zMin= 0.0, zMax= 0.0, zStep= 0.0,
                     ):
       
        arc_coords = [] 
        x = 0.0
        y = 0.0
        z = 0.0
        
        if xStep == 0:
            xcount = 1
        else:
            xcount = int(abs((xMax - xMin) / xStep) + 0.1) + 1
        
        if yStep == 0:
            ycount = 1
        else:
            ycount = int(abs((yMax - yMin) / yStep) + 0.1) + 1
        
        if zStep == 0:
            zcount = 1
        else:
            zcount = int(abs((zMax - zMin) / zStep) + 0.1) + 1
        
        if (ycount == 1 and zcount == 1):
            # cyclinder direction in x axis, arc in zy plane
            arc_coords = self.getArcCoordsArray(yMin,zMin,rad,degStart,degEnd,degStep)
        
        if (xcount == 1 and zcount == 1):
            # cyclinder direction in y axis, arc in zx plane
            arc_coords = self.getArcCoordsArray(xMin,zMin,rad,degStart,degEnd,degStep)

        if (xcount == 1 and ycount == 1):
            # cyclinder direction in z axis, arc in xy plane
            arc_coords = self.getArcCoordsArray(xMin,yMin,rad,degStart,degEnd,degStep)
         
        for ix in range(0, xcount, 1):
            x = xMin + xStep * ix
            for iy in range (0, ycount, 1):
                y = yMin + yStep * iy
                for iz in range (0, zcount, 1):
                    z = zMin + zStep * iz
                    if (ycount == 1 and zcount == 1):
                        # cyclinder direction in x axis, arc in zy plane
                        for coord in arc_coords:
                            y_arc, z_arc = coord
                            self.addXYZNode (name, x, y_arc, z_arc) 
                    
                    if (xcount == 1 and zcount == 1):
                        # cyclinder direction in y axis, arc in zx plane
                        for coord in arc_coords:
                            x_arc, z_arc = coord
                            self.addXYZNode (name, x_arc, y, z_arc)    
                    
                    if (xcount == 1 and ycount == 1):
                        # cyclinder direction in z axis, arc in xy plane
                        for coord in arc_coords:
                            x_arc, y_arc = coord
                            self.addXYZNode (name, x_arc, y_arc, z)
                    
    def getXYNodeListItem (self, x, y):
        find_coord = XY_COORD_FORMAT.format(float(x),float(y))
        if find_coord in self.NodeList:
            return self.NodeList[find_coord]
        return None
    def getXYZNodeListItem (self, x, y, z):
        find_coord = XYZ_COORD_FORMAT.format(float(x),float(y),float(z))
        if find_coord in self.NodeList:
            return self.NodeList[find_coord]
        return None
    def createXYZGrid(self,
                      name=None,
                      xMin= 0.0, xMax= 0.0, xStep= 0.0,
                      yMin= 0.0, yMax= 0.0, yStep= 0.0,
                      zMin= 0.0, zMax= 0.0, zStep= 0.0,
                      ):
        
        ref = name
        counter = 0
        
        x = 0.0
        y = 0.0
        z = 0.0
        
        if xStep==0:
            xcount = 1
        else:
            xcount = int(abs((xMax - xMin) / xStep) + 0.1) + 1
        
        if yStep==0:
            ycount = 1
        else:
            ycount = int(abs((yMax - yMin) / yStep) + 0.1) + 1
        
        if zStep==0:
            zcount = 1
        else:
            zcount = int(abs((zMax - zMin) / zStep) + 0.1) + 1
       
      #  print ('array size(', xcount, ycount, zcount, ')') 
        
        self.setRange(xMin, xMax,
                      yMin, yMax, 
                      zMin, zMax)
        
        for ix in range(0, xcount, 1):
            x = xMin + xStep * ix
            for iy in range (0, ycount, 1):
                y = yMin + yStep * iy
                for iz in range (0, zcount, 1):
                    z = zMin + zStep * iz
                    counter += 1
                    if name is None:
                        ref = counter
                    self.addXYZNode(ref, x, y, z)
                    print ('Added node at (', x, y, z, ')')            
                    
    def createXYGrid(self,
                      name=None,
                      xMin= 0.0, xMax= 0.0, xStep= 0.0,
                      yMin= 0.0, yMax= 0.0, yStep= 0.0):
                      
    
        count = 0
        ix = 0 
        iy = 0
        
        x = 0.0
        y = 0.0
        
        self.setRange(xMin, xMax,
                      yMin, yMax)
        if xStep==0:
            xcount = 1
        else:
            xcount = int(abs((xMax - xMin) / xStep) + 0.1) + 1
        
        if yStep==0:
            ycount = 1
        else:
            ycount = int(abs((yMax - yMin) / yStep) + 0.1) + 1
            
        for ix in range(1, xcount, 1):
            x = xMin + xStep * ix
            for iy in range (1, ycount, 1):
                y = yMin + yStep * iy
                count = count + 1
                if name is None:
                        ref = count
                self.addXYZNode(ref, x, y)
                print ('Added node at (', x, y, ')') 
                
    def loadXYZNodeList (self, 
                      fileIn,
                      append = False):
    
        fpoint = open(fileIn, "r")
        
        if (append==False):
            self.NodeList = []
            
        while True:
            in_line = fpoint.readline()
            if in_line == "":
                break
            if ',' in in_line:
                [name, nx, ny, nz] = in_line.split(',')
                if self.is_number(nx):
                    if self.is_number(ny):
                        if self.is_number(nz):
                            self.addXYZNode(name, nx, ny, nz)
                            print ('Node Added {},{:3f},{:3f},{:3f}'.format(name, float(nx), float(ny), float(nz)))

        fpoint.close()
    def loadXYNodeList (self, 
                      fileIn,
                      append = False):
    
        fpoint = open(fileIn, "r")
        
        if (append==False):
             self.NodeList = []
            
        while True:
            in_line = fpoint.readline()
            if in_line == "":
                break
            if ',' in in_line:
                [name, nx, ny] = in_line.split(',')
                if self.is_number(nx):
                    if self.is_number(ny):
                        self.addXYNode(name, nx, ny)
                        print ('Node Added {},{:3f},{:3f}'.format(name, float(nx), float(ny)))

        fpoint.close()
    
    def IsDbFile (self, db_file=None):   
        retvar = False
        
        if (db_file != None):
            if (db_file[-4:] == '.mdb'):
                retvar = True
            if (db_file[-6:] == '.accdb'):
                retvar = True
        
        return retvar
        
    def getConnected(self, db_file):
        
        self.conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file + ';'
        
        file = ''
        
        if (os.path.isfile(db_file)):
            self.conn = pyodbc.connect(self.conn_string)
            print('connecting to existing db:' + db_file)
        else:
            if db_file[-6:]=='.accdb':
                file = db_file[:-6]
            if db_file[-4:]=='.mdb':
                file = db_file[:-4]
            if not file:
                file = db_file
            self.conn = pyodbc.win_create_mdb(file) 
            print('connecting to new db:' + db_file)
            db_file = file + '.mdb'
        
        self.db_file = db_file
        
        
    def setFields(self, fields, formats):
        self.columns = fields.split(',')
        self.formats = formats.split(',') 
        self.types = formats.split(',')
        for i in range(len(self.types)):
            if (self.formats[i]=='{:2f}'):
                self.types[i] = 'float'
            if (self.formats[i]=='{:f}'):
                self.types[i] = 'float'    
            if (self.formats[i]=='{}'):
                self.types[i] = 'varchar(255)'
            if (self.formats[i]=='{:0}'):
                self.types[i] = 'int'  
            if (self.formats[i]=='{0}'):
                self.types[i] = 'int'              
                    
    def createTable(self, tname, fields, formats):
        self.tname = tname
        self.setFields(fields, formats)
        self.sql_insert = 'insert into ' + tname + ' ('
        self.sql_drop = 'drop table ' + tname
        self.sql_create = 'create table '+ tname + ' (id autoincrement primary key, '
        self.sql_select = 'select '
        separator = ''
        for i in range (len(self.columns)):
            if (i > 0):
                separator=', '
            self.sql_create += separator + '[' + self.columns[i] + '] ' + self.types[i]
            self.sql_insert += separator + '[' + self.columns[i] + ']'
            self.sql_select += separator + '[' + self.columns[i] + ']'
        self.sql_create += ')'
        self.sql_insert += ')'
        self.sql_select += ' from ' + tname
        print (self.sql_create)
        cursor = self.conn.cursor()
        if (self.tableExists(tname)):
            cursor.execute(self.sql_drop)
        cursor.execute(self.sql_create) 
        self.conn.commit()
    def tableExists(self, tname):
        try:
            cursor = self.conn.cursor()
            sql = 'select top 1 * from '  + tname 
            cursor.execute(sql)
            return True
        except:
            return False
        
    def insertValues(self, data):
        self.sql_data = self.sql_insert + ' values ('  
        separator = ''
        for i in range(len(data)):
            if (i > 0):
                separator=', '
            if (self.types[i].find('varchar') >= 0):
                self.sql_data += separator + '\'' + str(data[i]) + '\'' 
            else:
                self.sql_data += separator +  str(data[i])
        self.sql_data += ')'
        cursor = self.conn.cursor()
        cursor.execute(self.sql_data)
        self.conn.commit()
   



                