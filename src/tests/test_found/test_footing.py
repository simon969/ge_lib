import os
import json
import datetime
import unittest

from ge_lib.found.ground.GroundModel import GroundModel
from ge_lib.found.footing.FootingGeoms import footing_array, Footing
from ge_lib.found.FootingProcess import process_request
from .test_ground import getGroundModel
from .test_support import json_to_file, list_to_json, str_to_file

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","footing")

def main ():
    # RunExample101()
    # TestInitData()
    # test_process_request()
    print ("test_pile : main complete(0)".format(datetime.now()))

def _model101():
    '''
    model description:  this model is two footings with two geometries and two loadings
    '''

    footings = []
    
    g1 = [{
            "description":"2.5m x 3.5m x 1.2m",
            "breadth": 2.5,
            "length": 3.5,
            "depth": 1.2
            },{
            "description":"2.5m x 3.5m x 1.2m",
            "breadth": 2.5,
            "length": 3.5,
            "depth": 1.2
            }
            ]
    l1 = [{  
            "description":"max vertical loading",
            "fx":100,
            "fy":100,
            "fz":300,
            "mx":25,
            "my":45,
            "mz":10,
            "state":"uls_c2" 
            },{
            "description":"max horizontal loading",
            "fx":200,
            "fy":200,
            "fz":2500,
            "mx":25,
            "my":45,
            "mz":10,
            "state":"uls_c2"         
            }
            ]
    o1 = {"conc_density":25.0,
            "methods:": ['DrainedBearing_BS8004',
                            'UndrainedBearing_BS8004',
                            'DrainedBearing_EC7',
                            'UndrainedBearing_EC7']
                            }
    d1 = {"geoms":g1,
          "loadings":l1,
          "options":o1
          }
    f1 = Footing (data=d1)
    footings.append(f1)

    g2 = [{"description":"1.5m x 3.5m x 1.2m",
            "breadth": 1.5,
            "length": 3.5,
            "depth": 1.2
            },{
            "description":"1.5m x 3.5m x 1.2m",
            "breadth": 1.5,
            "length": 3.5,
            "depth": 1.2
            }]
    l2 = [{ "description":"",
            "fx":100,
            "fy":100,
            "fz":300,
            "mx":25,
            "my":45,
            "mz":10,
            "state":"uls_c2" 
            },{  "description":"",
            "fx":100,
            "fy":100,
            "fz":300,
            "mx":25,
            "my":45,
            "mz":10,
            "state":"uls_c2" 
            }]
    o2 = {"conc_density":25.0,
            "methods:": ['DrainedBearing_BS8004',
                            'UndrainedBearing_BS8004',
                            'DrainedBearing_EC7',
                            'UndrainedBearing_EC7']
                                            }

    d2 = {"geoms":g2,
          "loadings":l2,
          "options":o2
          }
    f2 = Footing (data=d2)
    footings.append(f2)

    return footings

def _model102():
    '''
    model description:  this model is intentionally missing loadings and options and should fail
    '''
 
    footings = {
            "geoms" : [{"description": "2.5m x 3.5m x 1.2m",
            "breadth": 2.5,
            "length": 3.5,
            "depth": 1.2
            },
          {"description": "2.5m x 3.5m x 1.2m",
            "breadth": 2.5,
            "length": 3.5,
            "depth": 1.2
            }]
    }

    return footings

def _model103():
    '''
    model description:  this model is an empty array but should fail gracefully
    '''
    footings = []

    return footings

def _model104():
    '''
    model description:  this model is imported from the .footing_model104 files
    '''
    with open(os.path.join(data_folder,"footing_model104.json")) as my_file:
        s = my_file.read()
    return s


_models_dict = {'101':_model101(),
                      '102':_model102(),
                      '103':_model103(),
                      '104':_model104()
                    }



def _geoms101 ():
    '''
    model description:  this model is an array of geometries
    '''
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
    '''
    model description:  this model is an array of loadings
    '''
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
        """
        test description:
        1) Initialise ground model and footing arrays with known good data and known bad data
        2) Check that they are created for the good data and a None object is returned for the bad data 
        """

        gm = getGroundModel('101', "dict")

        # create a dictionary object
        data_good = {"ground_models": [gm],
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
        
        data_bad = {"ground_models": gm,
                    "footings":[{},
                                {}]

        }

        try:  
            fa = footing_array(data=data_good["footings"], is_checked=False)
            data = list_to_json(fa)
          
        except Exception as e:
            message = {"error":e,
                       "status": 404}
            print ("unable to initialise footing array", message)


    def test_process_request101(self):
        """
        test description:
        1) Create a footing request string with no "sets" ground models and no set name, so the strata array has only one set of strata properties 
        2) Check that "sets" arrays is created in each strata
        """
        request_dic = {"ground_models":
                       [{
                        "description":"Ground Model: With Made Ground",
                        "id":"001",
                        "strata": [
                        {"description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        {"state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                            ]
                        },{
                        "description":"Ground Model: No Made Ground)",
                        "id":"002",
                        "strata": [
                         {"state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        ]
                        }],
                    "footings": [{
                                 "description":"footing set1",
                                 "id":"001",
                                 "geoms": [{
                                                "length":3.0,
                                                "breadth":1.0,
                                                "depth":0.5,
                                                "id":"001"
                                        },{
                                                "length":3.0,
                                                "breadth":2.0,
                                                "depth":0.75,
                                                "id":"002"
                                            }],
                                "loadings":[{
                                            "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c2",
                                            "id":"001"
                                            },{
                                             "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c1",
                                            "id":"002"   
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

        str_to_file (os.path.join(data_folder, "ex101_ret_data.json"),str(ret))

    def test_process_request102(self):
        """
        test description:
        1) Create a footing request string with no "sets" ground models, so the strata array has only one set of strata properties 
        2) Check that "sets" arrays is created in each strata
        """

        request_dic = {"ground_models":
                       [{
                        "description":"Ground Model: With Made Ground",
                        "id":"001",
                        "strata": [
                        {"set_name": "_default",  "description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                            ]
                        },{
                        "description":"Ground Model: No Made Ground)",
                        "id":"002",
                        "strata": [
                         {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        ]
                        }],
                    "footings": [{
                                 "description":"footing set1",
                                 "id":"001",
                                 "geoms": [{
                                                "length":3.0,
                                                "breadth":1.0,
                                                "depth":0.5,
                                                "id":"001"
                                        },{
                                                "length":3.0,
                                                "breadth":2.0,
                                                "depth":0.75,
                                                "id":"002"
                                            }],
                                "loadings":[{
                                            "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c2",
                                            "id":"001"
                                            },{
                                             "fx":100,
                                            "fy":100,
                                            "fz":300,
                                            "mx":25,
                                            "my":45,
                                            "mz":10,
                                            "state":"uls_c1",
                                            "id":"002"   
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

        str_to_file (os.path.join(data_folder, "ex102_ret_data.json"),str(ret))   
    
    def test_process_request103 (self):
        """
        test description:
        1) Create request string with no ids keys in the ground_models, footings, geoms or loads arrays 
        2) Check that id keys based on the index of the respective arrays are added automatically
        """
        
        request_dic = {"ground_models":
                       [{
                        "description":"Ground Model: With Made Ground",
                        "strata": [
                        {"set_name": "_default",  "description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                            ]
                        },{
                        "description":"Ground Model: No Made Ground)",
                        "strata": [
                         {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                        {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                        ]
                        }],
                    "footings": [{
                                 "description":"footing set1",
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

        str_to_file (os.path.join(data_folder, "ex103_ret_data.json"),str(ret))
    
    def test_footing_from_file(self):
        """
        test description:
        None
        """
        f = open(os.path.join(data_folder, "ex101_ret_data.json"))
        data = json.load(f)
        f.close()
        for d in data:
            gm = d["ground_model"]
            uls_c1 = d["uls_c1"]
            uls_c2 = d["uls_c2"]
            sls = d["sls"]

    def test_process_request104(self):
        """
        test description:
        None
        
        """
         
        request_dic = _models_dict["104"]
        json_str = json.dumps(request_dic)

        ret = process_request (json_str,"json")

        str_to_file (os.path.join(data_folder, "ex104_ret_data.json"),str(ret))

if __name__ == '__main__':
    unittest.main()
