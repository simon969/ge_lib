import os
import platform
import json
import math
import unittest

from found.pyGround.GroundModel import GroundModel
from found.pyGround.GroundStresses import GroundStresses
from found.pyGround.GroundModelSupport import addStressesStrengthStiffness, addEffectiveStress, addEModulus
from found.pyGround.GroundProcess import process_request
from ge_py.settings import APP_LOGGER_PATH
from found.tests.test_support import json_to_file, csv_to_file

if (platform.system()=='Linux'):
    path ='/mnt/chromeos/GoogleDrive/MyDrive/Projects/tests/pyground_tests/'    
else:
    path = 'G:\\My Drive\\Projects\\ground_tests\\'

def main ():
    # RunExample101()
    # TestInitData()
    # test_process_request()
    print ("main complete ({0})")



class TestGroundMethods(unittest.TestCase):

    def test_InitData(self):
    

        # create a dictionary object
        dic_bad = {"name":"Ground Model from dict object",
                "strata": [
                    {"name": "Made Ground", "density":20, "phi_deg":30, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposits", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3, "phi_deg":25}
                    ]
                }
        dic_good = {"Description":"Ground Model from dict object",
                "strata": [
                    {"set_name": "_default",  "Description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "State":"undrained", "Description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "State":"drained", "Description":"River Terraced Deposits", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "State":"undrained", "Description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                    ]
                }
        
        self.failUnlessRaises(ValueError, GroundModel, dic_bad)
        gm_d = GroundModel (data=dic_good)
        self.failIfEqual (gm_d, None)

        
        # create a JSON string 
        s1_bad = "{\"name\": \"Made Ground\", \"density\":20, \"phi_deg\":30, \"phi_deg\":32},{\"set_name\": \"_default\",  \"State\":\"undrained\", \"Name\":\"Alluvium\", \"level_top\":100, \"level_base\":98, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"cu_top\":40, \"cu_grad\":0, \"phi_deg\":20, \"cohesion\":0},"
        s1 = "{\"set_name\": \"_default\",  \"state\":\"drained\", \"description\":\"Made Ground\", \"level_top\":98, \"level_base\":94, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"phi_deg\":32},"
        s2 = "{\"set_name\": \"_default\",  \"state\":\"drained\", \"description\":\"River Terraced Deposists\", \"level_top\":98, \"level_base\":94, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"phi_deg\":32},"
        s3 = "{\"set_name\": \"_default\",  \"state\":\"undrained\", \"description\":\"London Clay\", \"level_top\":94, \"level_base\":74, \"density_dry\":20, \"density_sat\":20, \"water_level\":98, \"ko\":1.0, \"poisson_ratio\":0.3, \"cu_top\":70, \"cu_grad\":8, \"phi_deg\":25, \"cohesion\":2}"
        s_good = "{\"name\":\"Ground Model from json string\",\"strata\":[" + s1 + s2 + s3+"]}"
        s_bad = "{\"name\":\"Ground Model from json string\",\"strata2\":[" + s1_bad + s2 + s3+"]}"
        
        self.failUnlessRaises(ValueError, GroundModel, s_bad)
        gm_s = GroundModel (data = s_good)
        self.failIfEqual (gm_s, None)


     



    def test_RunExample101(self):
        
        gm = getGroundModel('103')
        
        json_to_file ( path + "/gm.json", gm.to_json())

        f = open(path + "/gm.json")
        data = json.load(f)

        gm_test = GroundModel(data=data)
        
        gm.collectStrataSet(['_default'])
        
        gm21 = addStressesStrengthStiffness(gm, APP_LOGGER_PATH + "\ge_pile.log")
        
        gs = GroundStresses ("Groundmodel sampled from +102m to +42m in -0.5m steps", gm21, 102, 80, -0.5)
        json_stress = gs.getStressesJSON ();
        json_to_file (path + 'res_stress.json', json_stress)    
    
        header_stress, rows_stress = gs.getStressesCSV(include_header_in_rows=True);
        csv_to_file (path + 'res_stress.csv', rows_stress)   
    def test_process_request(self):
        request_dic = {"groundmodel":{
                    "description":"Ground Model from dict object",
                    "strata": [
                    {"set_name": "_default",  "description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposists", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                        ]
                    },
                    "piles":[
                        {"description":"CFA_450", "base":math.pi*math.pow(0.45,2)/4,"perimeter":math.pi*0.45,"alpha":0.6,"ks":0.8,"tan_delta":0.67, "nq":200},
                        {"description":"CFA_600", "base":math.pi*math.pow(0.6,2)/4,"perimeter":math.pi*0.60,"alpha":0.6,"ks":0.8,"tan_delta":0.67, "nq":200},
                        {"description":"CFA_750", "base":math.pi*math.pow(0.75,2)/4,"perimeter":math.pi*0.75,"alpha":0.6,"ks":0.8,"tan_delta":0.67, "nq":200}
                        ]
                    }
        json_str = json.dumps(request_dic)

        ret = process_request (json_str,"json")
        json_to_file (path + "ret_data.json",ret)

def _GroundModel101():
    # typical ground conditions central london
    gm = GroundModel (Description ='London Basin')
    gm.addCohesiveStrata('Aluvium',102,100,18,16,102,40,0)
    gm.addGranularStrata('Rivert Terrace Deposits',100,97,18,16,102,38,0.0)
    gm.addCohesiveStrata('London Clay',97,67,20,20,97,70,8.5)
    gm.addCohesiveStrata('Lambeth Group',67,57,20,18,60,100,0.0)
    gm.addGranularStrata('Chalk',57,42,19,18,60,34,0.0)
    gm.collectStrataSet(['_default'])
    return gm

def _GroundModel102():
    # single cohesive strata water level intermediate (not for whole of strata)
    gm = GroundModel (Description='London Clay')
    gm.addCohesiveStrata('London Clay',100,50,20,20,97,70,8.5)
    gm.collectStrataSet(['_default'])
    return gm
def _GroundModel103():
  # single granular strata water level intermediate (not for whole of strata)
    gm = GroundModel (Description='River Terrace Deposits')
    gm.addGranularStrata('Rivert Terrace Deposits',100,85,18,16,91,38,0)
    gm.collectStrataSet(['_default'])
    return gm

ground_models_dict = {'101':_GroundModel101,
                      '102':_GroundModel102,
                      '103':_GroundModel103
                        }

def getGroundModel(id, format="obj"):
    gm = ground_models_dict[id]() 
    if format == "json":
        return gm.to_json()
    if format == "dict":
        return gm.to_dict()
    return gm
    



if __name__ == '__main__':
    unittest.main()
