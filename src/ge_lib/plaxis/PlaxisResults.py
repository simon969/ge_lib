from .plxresults.PlaxisScripting import PlaxisScripting

## Plaxis 3d Results
from .plxresults.Plaxis3dResults import Plaxis3dResults
from .plxresults.Plaxis3dResultsConnect import Plaxis3dResultsConnect
from .plxresults.Plaxis3dResults2018 import Plaxis3dResults2018
from .plxresults.Plaxis3dResults2023 import Plaxis3dResults2023

## Plaxis 2d Results
from .plxresults.Plaxis2dResults import Plaxis2dResults
from .plxresults.Plaxis2dResults2016 import Plaxis2dResults2016
from .plxresults.Plaxis2dResults2019 import Plaxis2dResults2019
from .plxresults.Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2
from .plxresults.Plaxis2dResultsConnectV22 import Plaxis2dResultsConnectV22
from .plxresults.Plaxis2dResults2023 import Plaxis2dResults2023

versions = ['Plaxis2d','Plaxis2d2016','Plaxis2d2019','Plaxis2dConnect','Plaxis2dConnectV2','Plaxis2dConnectV20','Plaxis2dConnectV21','Plaxis2dConnectV22','Plaxis2d2023'
            'Plaxis3d','Plaxis3d2018','Plaxis3dConnect','Plaxis3d2023'
            ] 



def GetPlaxisResults (host=None, port=None, password=None, version=None, task_log=None, plx_log=None):
    
    ps = PlaxisScripting(ps = None, 
                         host = host, 
                         port = port, 
                         password = password, 
                         task_log = task_log,
                         plx_log = plx_log)
    
    if (ps.is_connected == False):
            return None

    if (version != None): 
        if version not in versions:
            version = None 
    
    if (version==None):
        if (ps.s_o.is_3d):
            if (ps.s_o.major_version == 2023):
                return Plaxis3dResults2023 (ps)
            if (ps.s_o.major_version == 22.0):
                return Plaxis3dResultsConnect (ps)
            if (ps.s_o.major_version == 21.0):
                return Plaxis3dResultsConnect (ps)    
            if (ps.s_o.major_version == 20.0):
                return Plaxis3dResultsConnect (ps)    
            if (ps.s_o.major_version == 9.0):
                return Plaxis3dResults2018 (ps)
            if (ps.s_o.major_version < 9.0):
                return Plaxis3dResults (ps)
            ##    if (ps.s_o.minor_version==1422)

        if (ps.s_o.is_2d):
            if (ps.s_o.major_version == 2023):
                return Plaxis2dResults2023 (ps)
            if (ps.s_o.major_version == 22.0):
                return Plaxis2dResultsConnectV22 (ps)
            if (ps.s_o.major_version == 21.0):
                return Plaxis2dResultsConnectV2 (ps)    
            if (ps.s_o.major_version == 20.0):
                return Plaxis2dResultsConnectV2 (ps)    
            if (ps.s_o.major_version == 9.0):
                return Plaxis2dResults2019 (ps)
            if (ps.s_o.major_version == 8.0):
                return Plaxis2dResults2016 (ps)
        return ps
    else :
            if (version == 'Plaxis2d'):
                return Plaxis2dResults (ps)
            if (version == 'Plaxis2d2016'):
                return Plaxis2dResults2016 (ps)
            if (version == 'Plaxis2d2019'):
                return Plaxis2dResults2019 (ps)    
            if (version == 'Plaxis2dConnectV2' or 
                version == 'Plaxis2dConnectV21' or 
                version == 'Plaxis2dConnectV20' or
                version == 'Plaxis2dConnect'):
                return Plaxis2dResultsConnectV2 (ps)
            if (version == 'Plaxis2dConnectV22'):
                return Plaxis2dResultsConnectV22 (ps)
            if (version == 'Plaxis3d'):
                return Plaxis3dResults (ps) 
            if (version == 'Plaxis3d2018'):
                return Plaxis3dResults2018 (ps)      
            if (version == 'Plaxis3dConnect'):
                return Plaxis3dResultsConnect (ps)

