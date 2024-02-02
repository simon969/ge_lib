import math
import json
import copy

from .Support import ValueLinear,check_default_value,check_default_keys

default_material_factor_map = {
        'phi_deg':'phi',
        'cohesion':'cohesion',
        'cu_top':'undrained_shear',
        'cu_grad':'undrained_shear',
        'density_dry':'density',
        'density_sat':'density'
    }               

default_ground_model = {
    "surcharge": 0.0,
    "water_density":10.0,
    "increment":-0.5
}

default_strata = {


}


class GroundModel:
    def __init__(self, data = None, Description = "No Name Ground Model", is_checked=True):  
        self.description = Description
        self.strata = []
        self.set_names = ["_default"]
        self.strata_set = None
        self.water_density = 10.0
        self.surcharge = 0
      
        if (data is not None):
            if type(data) is dict:
                created = self.from_dict (data, is_checked)
            else:
                created = self.from_json (data, is_checked)
            if (created == False):
                raise ValueError("Unable to initialise GroundModel")
        
            
    def addStrata(self, data,check_data=False):

        if (data is not None):
            sets = data.get("sets",None)
            if (sets is None):
                # Check strata_set for water and level errors
                data2, errors = check_strata_set (data)
                if (data2 is None):
                    raise ValueError("Unable to addStrata from {0}".format(data))
                    _
                for d in data2: 
                    # Add properties from parent groundmodel if they are missing
                    d["water_density"] = d.get("water_density",self.water_density)
                    d["set_name"] = d.get("set_name", self.set_names[0])
                    s1 = Strata (data=d,
                                    check_data=False)
                    self.strata.append (s1)	
            else:
                s1 = Strata (data=data, 
                             check_data=check_data)
                self.strata.append (s1)	
    
    def addCohesiveStrata(self, description, level_top, level_base, density_dry, density_sat, water_level, cu_top, cu_grad):
        data = {"description": description,"set_name":self.set_names[0],"level_top":level_top,"level_base":level_base,"density_dry":density_dry, "density_sat":density_sat, "water_level":water_level, "cu_top":cu_top, "cu_grad":cu_grad}
        self.addStrata(data)
    def addGranularStrata(self, description, level_top, level_base, density_dry, density_sat, water_level,phi_deg, cohesion):
        data = {"description": description,"set_name":self.set_names[0],"level_top":level_top,"level_base":level_base,"density_dry":density_dry, "density_sat":density_sat, "water_level":water_level, "phi_deg":phi_deg, "cohesion":cohesion}
        self.addStrata(data)

    def getStrata(self, StrataName):
        for s in self.strata:
            if (s.Name == StrataName):
                return s
    def setStrataWaterLevel (self, description, water_level):
        for s in self.strata:
            if (s.description == description):
                s.water_level =  water_level
    
    def setStrataDrawdown(self, description, drawdown_level):
        for s in self.strata:
            if (s.description == description):
                s.water_level =  s.water_level - float(drawdown_level)
         #       print ("%s, %.2f, %.2f, %.2f" % (StrataName, s.WaterLevel, s.InitialWaterLevel, Drawdown))
    def minLevelBaseStrataSet(self):
        minLevel = 1000.0
        for s in self.strata_set:
            if minLevel > s.level_base:
                minLevel = s.level_base
        return minLevel
    def maxLevelTopStrataSet(self):
        maxLevel = -1000.0
        for s in self.strata_set:
            if maxLevel < s.level_top:
                maxLevel = s.level_top
        return maxLevel
    def collectStrataSet (self, set_names:list=['_default']):

        self.strata_set = []
           
        if (len(set_names)==1):
            for s in self.strata:
                st = s.getStrataSet(set_names[0])
                self.strata_set.append(st)
        else:
            for s, n in zip(self.strata, set_names):
                st = s.getStrataSet(n)
                self.strata_set.append(st)
         
    def getStrataSet(self, level:float):
        for s in self.strata_set:
            if level < s.level_top:
                if level >= s.level_base:
                    return s
        return None
    def copyStrataSet (self, existing_set_name, new_set_name, factors):
        if existing_set_name is None:
            existing_set_name = self.SetName
        for s in self.strata:
            s.copyStrataSet(existing_set_name, new_set_name, factors)

    def get_attr_str (self, level:float, attribute:str, not_found_str='None')->str:
        for s in self.strata_set:
            if level <= s.level_top:
                if level >= s.level_base:
                    return s.get_attr_str(level, attribute,not_found_str)
        return not_found_str

    def get_attr_value (self, level:float, attribute:str, not_found_value=0.0)->float:
        # try:
        for s in self.strata_set:
            if level <= s.level_top:
                if level >= s.level_base:
                    return s.get_attr_value(level, attribute, not_found_value)
        # if self.GET_ATTR_NOT_FOUND_MSG_ON:
        #     msg = "Not found value attribute {0} at level {1}".format(attribute,level)
        #     print (msg)
        #     self.logger.info(msg)
        return not_found_value           
    
    def to_json(self):
        ret = json.dumps(self, default=lambda o: o.__dict__, 
                        sort_keys=True, indent=None)
        return ret
    def to_dict(self):
        s = self.to_json()
        dict = json.loads(s)
        return dict
    def from_dict(self, data, is_checked):
        try:
            if (is_checked):
                checked_data = data
            else:
                checked_data = check_ground_model(data)
            
            temp = checked_data["strata"]
            self.__dict__.update(checked_data)
            self.strata = []
            for s in temp:
                self.addStrata(data=s)
            return True
        except Exception as e:
            print("Unable to read dict object! {0}".format(str(e)))
            return False

    def from_json(self, data, is_checked=True ):
        try :
            gm = json.loads(data)
            return self.from_dict (gm, is_checked)
        except Exception as e:
            print("Unable to read data as JSON string! {0}".format(str(e)))
            return False

def ground_model_array(data, is_checked=False):
    
    ground_models = []
    
    for idx, gm_data in enumerate(data):
        if is_checked:
            checked_data = gm_data
        else:
            checked_data = check_ground_model(gm_data,"{:03d}".format(idx))
        gm = GroundModel (data=checked_data, is_checked=True)
        if gm:
            ground_models.append(gm)
    
    return ground_models


def check_ground_model(data:dict, id = ""):

    checked = check_default_keys (data, default_ground_model)

    return checked
class Strata:
    def __init__(self, 
                 data, check_data=False
                ):
        self.sets = []
      
        if (data is not None):
            sets = data.get("sets",None)

            if (sets is None):
                ss = self.addStrataSet(data=data,
                                       check_data=check_data)
                if (ss == None):
                        raise ValueError("Unable to create strataset from {0}".format(data))
            else:
                for s in sets:
                    ss = self.addStrataSet(data=s,
                                           check_data=check_data)
                    if (ss == None):
                        raise ValueError("Unable to create strataset from {0}".format(s))   
                   
    def addStrataSet (self, data, check_data):
        try: 
            if (check_data) :
                data2, messages =  check_strata_set(data)
                if data2 == None:
                    return None
            else:
                data2 = [data]
            for d in data2: 
                s1 = StrataSet (d)
                self.sets.append(s1)
            return s1
        except:
            return None
    
    def getStrataSet(self, set_name):
         for s in self.sets:
             if (s.set_name == set_name):
                 return s

    def copyStrataSet(self, from_set_name, new_set_name, factors):
        
        new_strata_set = []

        for s in self.sets:
            if s.set_name == from_set_name:
                s1  = copy.deepcopy(s)
                s1.set_name = new_set_name
                if not factors is None:
                    s1.factor_properties(factors)
                new_strata_set.append (s1)
        
        if len(new_strata_set) > 0:
            self.sets.extend (new_strata_set)


    

class StrataSet:
    
    def __init__(self, data):
        self.__dict__ = data

    def factor_properties (self, factors, factor_map=default_material_factor_map):
        #  m2_factors  = {"phi":1.25,"cohesion":1.25, "undrained_shear":1.4, "unconfined_strength":1.4,"density":1.0}
        for key, value in factor_map.items():
            prop_val = self.__dict__.get(key,None)
            if prop_val is not None:
                new_prop_val = prop_val / factors[value]
                self.__setattr__(key, new_prop_val)
    
    def get_attr_value (self, level:float, attr:str, not_found_value:float):
        var =  self.__dict__.get(attr,None)
        if isinstance(var, ValueLinear):
            depth = self.level_top-level
            return var.get_value(depth)
        else:
            if (var is not None):
                return var
        return not_found_value
    
    def get_attr_str (self, level:float, attr:str, not_found_value:str):
        var =  self.__dict__.get(attr,None)
        if isinstance(var, ValueLinear):
            return not_found_value
        else:
            if (var is not None):
                return var
        return not_found_value
  


def check_strata_set(data):  
    
    messages = []

    try:
        
        level_top = data.get("level_top",None)
        level_base = data.get("level_base",None)
    
        if (level_top is None or level_base is None):
            msg = {'msg': 'level_top and/or level_base not provided for strataset',
                   'level':'fatal'}
            messages.append (msg)
            return None, messages
        
        data["thickness"] = level_top-level_base
        description = data.get("description","None")
        water_level = data.get("water_level", None)
        
        if (water_level is not None):
            
            if (water_level > level_top):
                data["water_state"] = "confined"
                msg = {'msg' : 'strata: {0} has a confined water_level ({1}'.format(description, water_level),
                       'level': 'info'}
                messages.append(msg)
                return [data], messages
            
            if (water_level == level_top):
                data["water_state"] = "unconfined"
                msg = {'msg' : 'strata: {0} has a unconfined water_level ({1}'.format(description, water_level),
                       'level': 'info'}
                messages.append(msg)
                return [data], messages
            
            if (water_level < level_top and water_level > level_base):
                msg = {'msg' : 'strata: {0} water_level ({1}) is between level_base ({2}) and level_top ({3}) strata_set will be split in two'.format(description, water_level, level_base, level_top),
                       'level': 'info'}
                messages.append (msg)
                data1 = copy.copy(data)  
                data2 = copy.copy(data)  
                
                data1["description"] = description + " (dry)" 
                data1["level_base"] = water_level
                data1["thickness"] = level_top-water_level
                data1["water_state"] = "dry"

                data2["description"] = description + " (sat)" 
                data2["level_top"] = water_level
                data2["thickness"] = water_level - level_base
                data2["water_state"] = "unconfined"
                cu_top = data1.get("cu_top",None)
                cu_grad = data1.get("cu_grad",None)
                if (cu_top is not None and cu_grad is not None):
                    data2["cu_top"] = cu_top + cu_grad * (level_top - water_level)
                    cu_top2 = data2["cu_top"]
                    msg = {'msg' : 'strata: {0} cu_top {1} and cu_grad {2} has also been split at cu_top{3}'.format(description, cu_top, cu_grad, cu_top2),
                           'level': 'info'}
                    messages.append (msg)
                return [data1,data2], messages
            
            if (water_level <= level_base):
                msg = {'msg' : 'strata: {0} water_level ({1}) is below level_base ({2}) and is therefore dry'.format(description, water_level, level_base, level_top),
                       'level': 'info'}
                messages.append (msg)
                data["water_state"] = "dry"
                return [data], messages
            
        else:
            return [data], messages 
        
    except Exception as e:
        msg = {'msg': 'unable to check strata_set {0} error msg: {1}'.format(description, str(e)),
               'level':'fatal'}
        msg.append("Unable to check strata_set {0}".format(str(e)))
        return None, messages
    