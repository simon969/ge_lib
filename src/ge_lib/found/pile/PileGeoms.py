import math

import json
from .PileCalcs import StandardCalcs

standard_calcs = StandardCalcs()

default_calc_methods = ['qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po']
allowed_calc_methods = standard_calcs.to_id_list()

default_options = {"conc_density":25.0
                  }

default_pile_properties = {
                            "description":"default pile",
                            "type":"bored",
                            "perimeter":0.0,
                            "base":0.0,
                            "calc_methods": default_calc_methods,
                            "nc":0.0,
                            "alpha": 0.0, 
                            "ks":0.0,
                            "tan_delta":0,
                            "nq":0,
                            "pile_test": True,
                            "sls_check": True,
                            "id":'001'
                            }

allowed_pile_types = ['bored','cfa','driven']
    
default_loadcase = {'fx':0.0,
                        'fy':0.0,
                        'fz':0.0,
                        'mx':0.0,
                        'my':0.0,
                        'mz':0.0,
                        'state':'',
                        'id':'001'
                        }

def check_default_keys(data:dict, default_dict):
    for key, value in default_dict.items():
        data[key] = data.get(key, value)
    return data

class PileSet:
    def __init__(self, data, is_checked=False):
        if type(data) is dict:
           self.from_dict(data, is_checked)
        else:
           self.from_json(data, is_checked)
    
    def from_dict(self, data, is_checked=False):
        if type(data) is dict:
            if is_checked:
                data_checked=data
            else:
                data_checked = check_pileset(data)
            self.__dict__= data_checked

    def from_json(self, data, is_checked=False):
        d = json.loads(data)
        self.from_dict(d, is_checked)

class Pile:

    def __init__(self, data, is_checked=False):
        if type(data) is dict:
           self.from_dict(data, is_checked)
        else:
           self.from_json(data, is_checked)
    
    def from_dict(self, data, is_checked=False):
        if type(data) is dict:
            if is_checked:
                data_checked=data
            else:
                data_checked = check_pile(data)
            self.__dict__= data_checked

    def from_json(self, data, is_checked=False):
        d = json.loads(data)
        self.from_dict(d, is_checked)

   

class CircularPile(Pile):
    def __init__(self, description, dia, alpha, ks, tan_delta, nq):
        self.shape = "circular"
        self.dia = float(dia)
        super().__init__(data = {"description":description, 
                                 "perimeter":dia*math.pi, 
                                 "base":math.pi*dia*dia/4,
                                 "nc":9.0,
                                 "alpha":alpha, 
                                 "ks":ks,
                                 "tan_delta":tan_delta,
                                 "nq":nq,
                                 "pile_type": "bored",
                                 "pile_test":True,
                                 "sls_check":True,
                                 "calc_methods": default_calc_methods
                                 },
                                 is_checked = True
                                )

class RectangularPile(Pile):
    def __init__(self, description, breadth, length, alpha, ks, tan_delta, nq):
        self.shape = "rectangular"
        self.breadth = float(breadth)
        self.length = float(length)
        super().__init__(data = {"description":description, 
                                 "perimeter": 2 * (breadth + length), 
                                 "base":breadth * length, 
                                 "nc":7.5,
                                 "alpha":alpha, 
                                 "ks":ks, 
                                 "tan_delta": tan_delta,
                                 "nq":nq,
                                 "pile_type": "bored",
                                 "pile_test":True,
                                 "sls_check":True,
                                 "calc_methods": default_calc_methods
                                 },
                                  is_checked = True
                                 )
class RectangularPilePS(Pile):
    def __init__(self, description, breadth, length, alpha, ks, tan_delta, nq):
        self.shape = "rectangular_ps"
        self.breadth = float(breadth)
        self.length = float(length)
        super().__init__(data = {"description":description, 
                                 "perimeter": 2 * length, 
                                 "base": breadth * length, 
                                 "nc":7.5,
                                 "alpha":alpha, 
                                 "ks":ks, 
                                 "tan_delta": tan_delta,
                                 "nq":nq,
                                 "pile_type": "bored",
                                 "pile_test":True,
                                 "sls_check":True,
                                 "calc_methods": default_calc_methods
                                 },
                                  is_checked = True
                                 )
def pileset_array (data:list, is_checked=False):
    """
    arguments:
        data: 
            list of pile_sets as json strings 
    return:
        returns list of python PileSet objects
    """
    pilesets = []
    for ps in data:
        if is_checked:
            checked_data = ps
        else:
            checked_data = check_pileset(ps)
        pileset = PileSet (data=checked_data, is_checked=True)
        pilesets.append(pileset)
    return pilesets
def pile_array (data:list, is_checked=False):
    """
    arguments:
        data: 
            list of piles as json strings 
    return:
        returns list of python Pile objects
    """
    piles = []
    for p in data:
        if is_checked:
            checked_data = p
        else:
            checked_data = check_pile(p, idx=None)
        pile = Pile (data=checked_data, is_checked=True)
        piles.append(pile)
    return piles

def check_pileset(data:dict):
    try:   
        piles = data.get("piles",[])
        chk_piles = []
        for idx, pile in enumerate(piles):
            chk_pile = check_pile(pile, idx)
            chk_piles.append(chk_pile)
        data['piles'] = chk_piles
    except Exception as e:
                message = {"error":e,
                        "status": 404}
                print ("unable to initialise pileset piles", message)    
        
    try:   
        loadings = data.get("loadings",[])
        chk_loadcases= []
         
        for idx, loadcase in enumerate(loadings):
            default_loadcase["id"] = "{:03d}".format(idx)
            chk_loadcase = check_default_keys (loadcase, default_loadcase) 
            chk_loadcases.append(chk_loadcase)
        data['loadings'] = chk_loadcases
    except Exception as e:
                message = {"error":e,
                        "status": 404}
                print ("unable to initialise pileset loadings", message)    

    options =  data.get("options",default_options)
    chk_options = check_default_keys(options,default_options)
    data['options'] = chk_options
    return data


def check_pile(data:dict, idx=None):
        
        if idx:
            default_pile_properties["id"] = "{:03d}".format(idx)
        
        check_default_keys(data, default_pile_properties)
        
        shape = data.get("shape",'none')

        if (shape == 'none'):
            if 'diameter' in data:
                data["shape"] = 'circular'
            if 'length' in data and 'breadth' in data:
                data["shape"] = 'rectangular'

        if (shape == "circular"):
            diameter = data.get("diameter",0.0)
            if diameter > 0:
                data["perimeter"] = math.pi * diameter
                data["base"] = math.pi * math.pow(diameter,2) / 4.0
    
        if (shape == "rectangular"):
            length = data.get("length",0.0)
            breadth = data.get("breadth",0.0)
            if (length > 0.0 and breadth > 0.0):
                data["perimeter"] = 2.0 * (length + breadth)
                data["base"] = length * breadth
        
        if (shape == "rectangular_ps"):
            length = data.get("length",0.0)
            breadth = data.get("breadth",0.0)
            if (length > 0.0 and breadth > 0.0):
                data["perimeter"] = 2.0 * (length + breadth)
                data["base"] = length * breadth
        
        if not type(data["calc_methods"]) is list:
                calc_methods = data["calc_methods"]
                if "','" in calc_methods:
                    calc_methods = calc_methods[1:-1]
                    delimeter = "','"
                else:
                    delimeter = ","
                arr = calc_methods.split(delimeter)
                data["calc_methods"] = inlist(arr,allowed_calc_methods)
        
        if not data["type"] in allowed_pile_types:
           raise ValueError (f"pile type {0} not found in allowed pile types {1}".format(data["pile_type"], allowed_pile_types)) 
        
        return data

def inlist (arr:list, allowed:list):
    ret = []
    for a in arr:
        if a in allowed:
            ret.append(a)
    return ret
