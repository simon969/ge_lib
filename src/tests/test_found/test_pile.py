import os
import json
import math
import unittest

from ge_lib.found.pyGround.GroundModel import GroundModel
from ge_lib.found.pyGround.GroundStresses import GroundStresses
from ge_lib.found.pyGround.GroundModelSupport import add_stresses_strength_stiffness
from ge_lib.found.pyPile.PileResistances import PileResistance, PILE_RESISTANCE_INCREMENT_DEFAULT
from ge_lib.found.pyPile.PileGeoms import CircularPile, pile_array
from ge_lib.found.pyPile.EC7PartialFactors import r4_factors_cfa, add_model_factor, get_factors
from ge_lib.found.PileProcess import process_request

from .test_ground import getGroundModel
from .test_support import json_to_file, csv_to_file


data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","pile")
    

def _model101():
    piles = []
    
    cp450 = CircularPile ( "CFA_450", dia=0.45,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
    piles.append(cp450)
    
    cp750 = CircularPile ( "CFA_750", dia=0.75,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
    piles.append(cp750)

    return piles

def _model102():
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

def _model103():
    piles = []

    return piles

def _model104():
    with open(os.path.join(data_folder,"pile_model104.json")) as my_file:
        s = my_file.read()
    return s

def _model105():
    with open(os.path.join(data_folder,"pile_model105.json")) as my_file:
        s = my_file.read()
    return s


_models_dict = {'101':_model101(),
                      '102':_model102(),
                      '103':_model103(),
                      '104': _model104(),
                      '105': _model105()
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
        
        gm_pile = add_stresses_strength_stiffness(gm)
        gm_pile.GET_ATTR_NOT_FOUND_MSG_ON=False
        cp = CircularPile ( "CFA_450", dia=0.45,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
        pr = PileResistance ("450dia CFA pile with groundmodel sampled from +102m to +42m in -0.5m steps", cp, gm_pile, 102, 42, -0.5)
    
        factors = add_model_factor(r4_factors_cfa, False)

        cfa450_r4 = pr.getDrainedResistancesJSON (factors)
        json_to_file (os.path.join(data_folder,'cfa450_r4_drained.json'), cfa450_r4)

        header_resistance,rows_resistance = pr.getDrainedResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (os.path.join(data_folder,'cfa450_r4_drained.csv'), rows_resistance)

        header_resistance,rows_resistance = pr.getUndrainedResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (os.path.join(data_folder,'cfa450_r4_undrained.csv'), rows_resistance)
        
        header_resistance,rows_resistance = pr.getResistancesCSV (factors,include_header_in_rows=True)
        csv_to_file (os.path.join(data_folder, 'cfa450_r4.csv'), rows_resistance)


    def test_RunExample101(self):
        
        gm = getGroundModel('103')
        
        json_to_file ( os.path.join(data_folder,"gm.json"), gm.to_json())

        f = open(os.path.join(data_folder, "gm.json"))
        data = json.load(f)
        f.close()
        
        gm_test = GroundModel(data=data)
        
        gm.collectStrataSet(['_default'])
        
        gm21 = add_stresses_strength_stiffness(gm)
        
        gs = GroundStresses ("Groundmodel sampled from +102m to +42m in -0.5m steps", gm21, 102, 80, -0.5)
        json_stress = gs.getStressesJSON ();
        json_to_file (os.path.join(data_folder,'res_stress.json'), json_stress)    
    
        header_stress, rows_stress = gs.getStressesCSV(include_header_in_rows=True);
        csv_to_file (os.path.join(data_folder, 'res_stress.csv'), rows_stress)   

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
        json_to_file (os.path.join(data_folder, "ret_data.json"),ret)

    def test_process_request104(self):
        request_dic = _models_dict["104"]
        json_str = json.dumps(request_dic)
        ret = process_request (json_str,"json")
        json_to_file (os.path.join(data_folder, "ret_data_104.json"),ret)
    
    def test_resistanceExample101(self):
        
        gm = getGroundModel ('101')
        gm.collectStrataSet (['_default'])
        gs = GroundStresses ("Groundmodel sampled from +102m to +42m in -0.5m steps", gm, 102, 42, -0.5)
        res_stress = gs.getStresses ();
        json_to_file (os.path.join(data_folder,'res_stress.csv'), res_stress)    
        
        cp = CircularPile ( "CFA_450", dia=0.45,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
        
        pr = PileResistance ("Groundmodel sampled from +102m to +42m in -0.5m steps", cp, gm, 102, 42, -0.5)
      
        res_sls = pr.getResistances (get_factors("unity_factors"))
        res_uls_c1 = pr.getResistances (get_factors("uls_c1_cfa_factors"))
        res_uls_c2 = pr.getResistances (get_factors("uls_c2_cfa_factors"))
        
        json_to_file ( os.path.join(data_folder,'res_sls.json'), res_sls)
        json_to_file ( os.path.join(data_folder,'res_uls_c1.json'), res_uls_c1)
        json_to_file ( os.path.join(data_folder,'res_uls_c2.json'), res_uls_c2)
    
    def test_process_request105(self):

        request_dic = _models_dict["105"]
        json_str = json.dumps(request_dic)
        ret = process_request (json_str,"json")
        json_to_file (os.path.join(data_folder, "ret_data_105.json"),ret)


if __name__ == '__main__':
    unittest.main()