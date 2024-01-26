from plaxis.PlaxisRequests.PlaxisScripting import PlaxisScripting

## Plaxis 3d Results
from plaxis.PlaxisRequests.Plaxis3dResults import Plaxis3dResults
from plaxis.PlaxisRequests.Plaxis3dResultsConnect import Plaxis3dResultsConnect
from plaxis.PlaxisRequests.Plaxis3dResults2018 import Plaxis3dResults2018

## Plaxis 2d Results
from plaxis.PlaxisRequests.Plaxis2dResults import Plaxis2dResults
from plaxis.PlaxisRequests.Plaxis2dResults2016 import Plaxis2dResults2016
from plaxis.PlaxisRequests.Plaxis2dResults2019 import Plaxis2dResults2019
from plaxis.PlaxisRequests.Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2
from plaxis.PlaxisRequests.Plaxis2dResultsConnectV22 import Plaxis2dResultsConnectV22

versions = ['Plaxis2d','Plaxis2d2016','Plaxis2d2019','Plaxis2dConnect','Plaxis2dConnectV2','Plaxis2dConnectV20','Plaxis2dConnectV21','Plaxis2dConnectV22',
            'Plaxis3d','Plaxis3d2018','Plaxis3dConnect'
            ] 



def GetPlaxisResults (host=None, port=None, password=None, version=None, path=None) :
    ps = PlaxisScripting(None, host, port, password, path)
    
    if (ps.is_connected == False):
            return None

    if (version != None): 
        if version not in versions:
            version = None 
    
    if (version==None):
        if (ps.s_o.is_3d):
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

