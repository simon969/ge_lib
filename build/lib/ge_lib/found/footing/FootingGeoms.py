import math
import json

INCREMENT_DEFAULT = 0.1

default_methods = ['DrainedBearing_BS8004','UndrainedBearing_BS8004','DrainedBearing_EC7','UndrainedBearing_EC7']

default_options = {"conc_density":25.0,
                  "methods": default_methods
                  }
default_geom = {'length':0.0,
                    'breadth':0.0,
                    'depth':0.0,
                    'id':''}
    
default_loadcase = {'fx':0.0,
                        'fy':0.0,
                        'fz':0.0,
                        'mx':0.0,
                        'my':0.0,
                        'mz':0.0,
                        'state':'',
                        'id':''
                        }
class Footing:

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
                data_checked = check_footing(data)
            self.__dict__= data_checked

    def from_json(self, data, is_checked=False):
        d = json.loads(data)
        self.from_dict(d, is_checked)

    def to_json(self):
        ret = json.dumps(self, default=lambda o: o.__dict__, 
                        sort_keys=True, indent=None)
        return ret
    
def footing_array (data:list, is_checked=False):
    """
    arguments:
        data: 
            list of footings as json strings 
    return:
        returns list of python Footing objects
    """
    footings = []
    for footing_data in data:
        footing = Footing (data=footing_data, is_checked=is_checked)
        if footing:
            footings.append(footing)
    
    return footings

def check_default_keys(data:dict, default_dict, id=""):
    for key, value in default_dict.items():
        if key == "id":
            data[key] = data.get(key, id)
        else:
            data[key] = data.get(key, value)
    return data

def check_footing(data:dict):
    
    try:   
        geoms = data.get("geoms",[])
        chk_geoms = []
        for idx, geom in enumerate(geoms):
            chk_geom = check_default_keys(geom,default_geom,"{:03d}".format(idx))
            chk_geoms.append(chk_geom)
        data['geoms'] = chk_geoms
    except Exception as e:
                message = {"error":e,
                        "status": 404}
                print ("unable to initialise footing geoms", message)    
    
        
    try:   
        loadings = data.get("loadings",[])
        chk_loadcases= []
         
        for idx, loadcase in enumerate(loadings):
            chk_loadcase = check_default_keys (loadcase,default_loadcase,"{:03d}".format(idx)) 
            chk_loadcases.append(chk_loadcase)
        data['loadings'] = chk_loadcases
    except Exception as e:
                message = {"error":e,
                        "status": 404}
                print ("unable to initialise footing loadings", message)    


    options =  data.get("options",default_options)
    chk_options = check_default_keys(options,default_options)
    data['options'] = chk_options
    return data


    