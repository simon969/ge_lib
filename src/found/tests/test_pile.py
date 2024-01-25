import os
import platform
import json
import math
import unittest

from found.pyGround.GroundModel import GroundModel
from found.pyGround.GroundStresses import GroundStresses
from found.pyGround.GroundModelSupport import addStressesStrengthStiffness
from found.tests.test_ground import getGroundModel
from found.pyPile.PileResistances import PileResistance, PILE_RESISTANCE_INCREMENT_DEFAULT
from found.pyPile.PileGeoms import CircularPile, GetPileArray
from found.pyPile.EC7PartialFactors import r4_factors_cfa, add_model_factor
from found.pyPile.PileProcess import process_request
from found.tests.test_support import json_to_file, csv_to_file

from ge_py.settings import APP_LOGGER_PATH

if (platform.system()=='Linux'):
    path ='/mnt/chromeos/GoogleDrive/MyDrive/Projects/tests/pypile_tests/'    
else:
    path = 'G:\\My Drive\\Projects\\pile_tests\\'
    
def main ():
    # RunExample101()
    # TestInitData()
    # test_process_request()
    print ("test_pile : main complete(0)".format(datetime.now))

def _PileModel101():
    piles = []
    
    cp450 = CircularPile ( "CFA_450", dia=0.45,Alpha= 0.6,Ks=0.8,TanDelta=0.67, Nq=200)
    piles.append(cp450)
    
    cp750 = CircularPile ( "CFA_750", dia=0.75,Alpha= 0.6,Ks=0.8,TanDelta=0.67, Nq=200)
    piles.append(cp750)

    return piles

def _PileModel102():
    piles = [
            {
            "name" : "CFA_450",
            "base" : math.pow(0.45,2) * math.pi / 4.0,
            "perimeter" : math.pi * 0.45,
            "alpha" : 0.6,
            "ks" :  0.8,
            "tan_delta": 0.67
            },{
            "name" : "CFA_750",
            "base" : math.pow(0.75,2) * math.pi / 4.0,
            "perimeter" : math.pi * 0.75,
            "alpha" : 0.6,
            "ks" :  0.8,
            "tan_delta": 0.67
            }
             ]

    return piles

def _PileModel103():
    piles = []

    return piles

pile_models_dict = {'101':_PileModel101,
                      '102':_PileModel102,
                      '103':_PileModel103
                        }

class TestPileMethods(unittest.TestCase):

    def test_InitData(self):
    
    
        # create a dictionary object
        # create a dictionary object
        d0bad = {"name":"Ground Model from dict object",
                "strata": [
                    {"name": "Made Ground", "density":20, "phi_deg":30, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "state":"drained", "description":"River Terraced Deposits", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "state":"undrained", "description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3, "phi_deg":25}
                    ]
                }
        d0good = {"Description":"Ground Model from dict object",
                "strata": [
                    {"set_name": "_default",  "Description":"Made Ground", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "State":"undrained", "Description":"Alluvium", "level_top":100, "level_base":98, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "cu_top":40, "cu_grad":0, "phi_deg":20, "cohesion":0},
                    {"set_name": "_default",  "State":"drained", "Description":"River Terraced Deposits", "level_top":98, "level_base":94, "density_dry":18, "density_sat":16, "water_level":101, "ko":0.5, "poisson_ratio":0.3, "phi_deg":32},
                    {"set_name": "_default",  "State":"undrained", "Description":"London Clay", "level_top":94, "level_base":74, "density_dry":20, "density_sat":20, "water_level":98, "ko":1.0, "poisson_ratio":0.3,"cu_top":70, "cu_grad":8, "phi_deg":25,"cohesion":2}
                    ]
                }
        try:  
            gm1 = None
            gm1 = GroundModel(data=d0bad)
            data1 = gm1.to_json()    
            # print (data1)
        except:
            print ("test_InitData: unable to initialise ground model")
        


         # create a JSON string 
        s1_bad = "{\"name\": \"Made Ground\", \"density\":20, \"phi_deg\":30, \"phi_deg\":32},{\"set_name\": \"_default\",  \"State\":\"undrained\", \"Name\":\"Alluvium\", \"level_top\":100, \"level_base\":98, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"cu_top\":40, \"cu_grad\":0, \"phi_deg\":20, \"cohesion\":0},"
        s1 = "{\"set_name\": \"_default\",  \"state\":\"drained\", \"description\":\"Made Ground\", \"level_top\":98, \"level_base\":94, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"phi_deg\":32},"
        s2 = "{\"set_name\": \"_default\",  \"state\":\"drained\", \"description\":\"River Terraced Deposists\", \"level_top\":98, \"level_base\":94, \"density_dry\":18, \"density_sat\":16, \"water_level\":101, \"ko\":0.5, \"poisson_ratio\":0.3, \"phi_deg\":32},"
        s3 = "{\"set_name\": \"_default\",  \"state\":\"undrained\", \"description\":\"London Clay\", \"level_top\":94, \"level_base\":74, \"density_dry\":20, \"density_sat\":20, \"water_level\":98, \"ko\":1.0, \"poisson_ratio\":0.3, \"cu_top\":70, \"cu_grad\":8, \"phi_deg\":25, \"cohesion\":2}"
        s0 = "{\"name\":\"Ground Model from json string\",\"strata\":[" + s1 + s2 + s3+"]}"
        s0_bad = "{\"name\":\"Ground Model from json string\",\"strata2\":[" + s1_bad + s2 + s3+"]}"
        try:
            gm2 = None
            gm2 = GroundModel(data=s0)
            data2 = gm2.to_json()    
            # print ("\n\r")
            # print (data2)
        except:
            print ("test_InitData: unable to initialise ground model") 


    def RunPileTests(self, gm:GroundModel, path:str):
        
        gm.collectStrataSet(['_default'])
        
        gm_pile = addStressesStrengthStiffness(gm, APP_LOGGER_PATH + "\ge_pile.log")
        gm_pile.GET_ATTR_NOT_FOUND_MSG_ON=False
        cp = CircularPile ( "CFA_450", dia=0.45,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
        pr = PileResistance ("450dia CFA pile with groundmodel sampled from +102m to +42m in -0.5m steps", cp, gm_pile, 102, 42, -0.5)
    
        factors = add_model_factor(r4_factors_cfa, False)

        cfa450_r4 = pr.getDrainedResistancesJSON (factors)
        json_to_file ( path + "/cfa450_r4_drained.json", cfa450_r4)

        header_resistance,rows_resistance = pr.getDrainedResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (path + '/cfa450_r4_drained.csv', rows_resistance)

        header_resistance,rows_resistance = pr.getUndrainedResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (path + '/cfa450_r4_undrained.csv', rows_resistance)
        
        header_resistance,rows_resistance = pr.getResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (path + '/cfa450_r4.csv', rows_resistance)


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
        json_to_file (path + '/res_stress.json', json_stress)    
    
        header_stress, rows_stress = gs.getStressesCSV(include_header_in_rows=True);
        csv_to_file (path + '/res_stress.csv', rows_stress)   

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
        json_to_file (path + "/ret_data.json",ret)


if __name__ == '__main__':
    main()
