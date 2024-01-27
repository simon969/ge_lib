import math
from ge_lib.found.pyGround.GroundModel import GroundModel
import json

default_calc_methods = ['qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po']
allowed_pile_types = ['bored','cfa','driven']

default_pile_properties = {
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
                            "sls_check": True
                            }



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
    def __init__(self, name, dia, alpha, ks, tan_delta, nq):
        self.shape = "circular"
        self.dia = float(dia)
        super().__init__(data = {"name":name, 
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
    def __init__(self, name, breadth, length, alpha, ks, tan_delta, nq):
        self.shape = "rectangular"
        self.breadth = float(breadth)
        self.length = float(length)
        super().__init__(data = {"name":name, 
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
    def __init__(self, name, breadth, length, alpha, ks, tan_delta, nq):
        self.shape = "rectangular_ps"
        self.breadth = float(breadth)
        self.length = float(length)
        super().__init__(data = {"name":name, 
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
def GetPileArray (data:list):
    """
    arguments:
        data: 
            list of piles as json strings 
    return:
        returns list of python Pile objects
    """
    piles = []
    for p in data:
        checked_data = check_pile(p)
        pile = Pile (data=checked_data, is_checked=True)
        piles.append(pile)
    return piles

def check_pile(data:dict):
       
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

        for key, value in default_pile_properties.items:
            if not key in data:
                data[key] = value
        
        if not type(data["calc_methods"]) is list:
                arr = data["calc_methods"].split(",")
                data["calc_methods"] = inlist(arr,allowed_calc_methods)
        
        if not data["pile_type"] in allowed_pile_types:
           raise ValueError (f"pile type {0} not found in allowed pile types {1}".format(data["pile_type"], allowed_pile_types)) 
        
        return data

def inlist (arr:list, allowed:list):
    ret = []
    for a in arr:
        if a in allowed:
            ret.append(a)
    return ret
