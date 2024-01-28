import os
import platform
import json
import math
import unittest

from src.ge_lib.found.pyGround.GroundModel import GroundModel
from .test_ground import getGroundModel
from src.ge_lib.found.pyFooting.FootingGeoms import footing_array
from src.ge_lib.found.FootingProcess import process_request
from .test_support import json_to_file, list_to_json, str_to_file

if (platform.system()=='Linux'):
    path ='/mnt/chromeos/GoogleDrive/MyDrive/Projects/tests/pyfooting_tests/'    
else:
    path = 'G:\\My Drive\\Projects\\footing_tests\\'



# def main ():
#     unittest.main
#     import datetime 
#     # RunExample101()
#     TestInitData()
#     # test_process_request()
#     print ("main complete ({0})".format(datetime.Now))


 # max_depth = max_property (footings,"depth")
        # max_breadth = max_property (footings,"breadth")
        # max_level = gm.maxLevelTopStrataSet()
        # min_level = max_level - max(max_depth, 3.0 * max_breadth)

        # gm_increment = footing_data.get("increment",INCREMENT_DEFAULT)


def _geoms101 ():
   geom = [{
            "length":3.0,
            "breadth":1.0,
            "depth":0.5
            },{
            "length":4.0,
            "breadth":1.0,
            "depth":1.0
            },{
            "length":3.0,
            "breadth":2.0,
            "depth":0.75
            }]
   return geom
def _loadings101 ():
    loadings = [{
                "fx":100,
                "fy":100,
                "fz":300,
                "mx":25,
                "my":45,
                "mz":10,
                "state":"uls_c2"
            },{
                "fx":100,
                "fy":100,
                "fz":300,
                "mx":25,
                "my":45,
                "mz":10,
                "state":"uls_c1"
            },{
                "fx":100,
                "fy":100,
                "fz":300,
                "mx":25,
                "my":45,
                "mz":10,
                "state":"sls"
            },{
                "fx":100,
                "fy":100,
                "fz":300,
                "mx":25,
                "my":45,
                "mz":10,
                "state":"set_c"
            }]
      
    return loadings  
class TestFoootingMethods(unittest.TestCase):
               
    def test_init_data(self):
    
        gm = getGroundModel('101', "dict")

        # create a dictionary object
        data_good = {"ground_model": gm,
                    "footings": [{
                                "geoms": _geoms101(),
                                "loadings": _loadings101(),
                                "options":{"conc_density":25.0,
                                            "methods:": ['DrainedBearing_BS8004',
                                                         'UndrainedBearing_BS8004',
                                                         'DrainedBearing_EC7',
                                                         'UndrainedBearing_EC7']
                                            }
                                }]
                }
        
        data_bad = {"ground_model": gm,
                    "footings":[{},
                                {}]

        }

        try:  
            fa = footing_array(data=data_good["footings"], is_checked=False)
            data = list_to_json(fa)
            # print (data)
        except Exception as e:
            message = {"error":e,
                       "status": 404}
            print ("unable to initialise footing array", message)


    def test_RunExample101(self):
        
        gm = getGroundModel('103')
        
        json_to_file ( path + "gm.json", gm.to_json())

        f = open(path + "gm.json")
        data = json.load(f)
        f.close()
        gm_test = GroundModel(data=data)
        
        gm.collectStrataSet(['_default'])
    

    def test_process_request(self):
        request_dic = {"ground_model":{
                    "description":"Ground Model from dict object",
                   "strata": [
                    {"set_name": "_default",  "description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                        ]
                    },
                    "footings": [{
                                    "geoms": [{
                                                "length":3.0,
                                                "breadth":1.0,
                                                "depth":0.5
                                        },{
                                                "length":3.0,
                                                "breadth":2.0,
                                                "depth":0.75
                                            }],
                                "loadings":[{
                                            "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c2"
                                            },{
                                             "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c1"   
                                            }],
                                "options":{"conc_density":25.0,
                                            "methods:": ['DrainedBearing_BS8004',
                                                         'UndrainedBearing_BS8004',
                                                         'DrainedBearing_EC7',
                                                         'UndrainedBearing_EC7']
                                            }
                                }]
                    }
        json_str = json.dumps(request_dic)

        ret = process_request (json_str,"json")

        str_to_file (path + "ex101_ret_data.json",ret)
        
    
    def test_footing_from_file(self):

        f = open(path + "ex101_ret_data.json")
        data = json.load(f)
        f.close()
        uls_c1 = data["uls_c1"]
        uls_c2 = data["uls_c2"]
        sls = data["sls"]     

if __name__ == '__main__':
    unittest.main()
