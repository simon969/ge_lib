import math
import json

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1", "on")

def as_list(p):
  if hasattr(p, "__len__") and (not isinstance(p, str)):
    return p
  if ',' in p:
    return p.split(",")
  a = []
  a.append(p)
  return a

def as_float_list(p):
 return [float(v) for v in as_list(p)]

def get_value(obj, attrib:str, none_value:float):
    v = getattr(obj,  attrib, None)
    if v is None:
        return none_value
    return float(v)
def has_values(obj, attribs:str, min_values:float):
  
  res =  [False for i in range(len(attribs))]

  for i in range (len(attribs)):
    if hasattr(obj, attribs[i]):
      val = getattr(obj, attribs[i])
      if val is not None: 
         if (val > min_values[i]):
          res[i] = True
  
  return res

def as_one_list(obj:list[list]):
    ret = []
    for i in range (len(obj)):
        o = obj[i]
        for j in range (len(o)):
            ret.append(o[j])
    return ret

def list_has_not_none_attrib(obj:list, attribs:str):

    r =  [False for i in range(len(attribs))]
    res = [r for i in range(len(obj))]
  
    for j in range(len(obj)):
        o = obj[j]
        r = res[j]
        for i in range (len(attribs)):
            val = getattr(o, attribs[i],None)
            if val is not None:
                r[i] = True
    return res

def list_has_values(obj:list, attribs:str, min_values:float):
  
  r =  [False for i in range(len(attribs))]
  res = [r for i in range(len(obj))]
  
  for j in range(len(obj)):
    o = obj[j]
    r = res[j]
    for i in range (len(attribs)):
        if hasattr(o, attribs[i]):
            val = getattr(o, attribs[i])
            if val is not None: 
                if (val > min_values[i]):
                    r[i] = True
  
  return res
def check_default_value(data:dict, prop_name:str, default_value:float):
    prop_value = data.get(prop_name,None)
    if prop_value is None:
        data[prop_name]=default_value

def all_have_values (s, props:[]):
    for prop in props:
        if (s.__dict__.get(prop,None) == None):
            return False
    return True
def any_have_values (s, props:[]):
    for prop in props:
        if (s.__dict__.get(prop,None) != None):
            return True
    return False

class ValueLinear:
    def __init__(self, top:float, gradient:float):
        self.top = top
        self.gradient= gradient
        self.base = 0
        self.average = 0
    
    def __mul__(self, f:float):
        return ValueLinear(self.top*f, self.gradient*f)
    
    def get_value(self, depth_below_top=0.0)->float:
             if (self.gradient): 
                 return self.top + self.gradient * depth_below_top
             else:
                 return self.top
class ValueExponential:
    def __init__(self, top:float, gradient:float, power:float):  
        self.top = float(top)
        self.gradient = float(gradient)
        self.power = float(power)
    def get_value(self, depth_below_top=0.0)->float:
        if (self.gradient): 
                 return self.top + self.gradient * math.pow(depth_below_top, self.power)
        else:
            return self.top

import inspect
class calc_data: 
    def to_json(self):
        ret = json.dumps(self, default=lambda o: o.__dict__, 
                        sort_keys=True, indent=None)
        return ret
    def to_dict(self):
        s = self.to_json()
        dict = json.loads(s)
        return dict
class calc:
    def __init__(self, id, description, reference, state, component, version):
        method = {"id":id, 
                  "description":description, 
                  "reference": reference, 
                  "state": state,
                  "component":component,
                  "version":version}
        self.method = method
        self.data = calc_data()
    def load_footing(self, fg):
        if fg:
            self.data.geom = fg.get("geom",{})
            self.data.loadcase= fg.get("loadcase",{})
            self.data.length = fg.get("length",0)
            self.data.breadth = fg.get("breadth",0)
            self.data.depth = fg.get("depth",0)
            self.data.alpha_rad = fg.get("alpha_rad",0)
            self.data.state = fg.get("state","none")
            self.data.material_set = fg.get("material_set","none")
            self.data.vload = fg.get("vload",0)
            self.data.hload = fg.get("hload",0)
            self.data.htheta_rad = fg.get("htheta_rad",0)
    def load_ground_model(self, gm):
        if gm:
            if self.method["state"] == "undrained":
                self.data.cu = gm.get_attr_value(self.data.depth, "cu")
            
            if self.method["state"] == "drained":
                self.data.cohesion = gm.get_attr_value(self.data.depth, "cohesion")
                self.data.phi_rad = gm.get_attr_value(self.data.depth, "phi_rad")
                if self.data.phi_rad == 0.0:
                    phi_deg = gm.get_attr_value(self.data.depth, "phi_deg")
                    self.data.phi_rad = math.radians(phi_deg)

            self.data.density = gm.get_attr_value(self.data.depth, "density")
            if self.data.density == 0.0:
                density_sat = gm.get_attr_value(self.data.depth, "density_sat")
                self.data.density = density_sat - gm.water_density
            self.data.surcharge = gm.get_attr_value(self.data.depth, "EffectiveStress")
               
    def calc(self, pile, gm, levels):
        pass
    def data_to_dict(self):
        return self.data.to_dict()
    
class calc_collection:

    def __init__(self, id, description, version):
        self.id = id
        self.description=description
        self.version = version
        self.calcs = []
    def append_calc(self, c):
        self.calcs.append(c)
    def get_calc(self, id):
        for c in self.calcs:
            if (c.id==id):
                return c
        return None
    def to_dict (self):
        to_return = {"id": self.id, "description": self.description}
        calcs = {}
        for calc in self.calcs:
            source = inspect.getsource(calc.calc)
            calcs[calc.id] = {"description": calc.description,
                  "reference": calc.reference,
                  "component": calc.component,
                  "state": calc.state,
                  "source": source,
                  "version": calc.version}     
        to_return["calcs"] = calcs
        return to_return
        
    
    def to_json (self):
        to_return = {"id": self.id, "description": self.description}
        for calc in self.calcs:
            source = inspect.getsource(calc.calc)
            s =  "{{\"id\": \"{0}\", \"description\": \"{1}\",\"reference\":\"{2}\",\"component\":\"{3}\",\"stata\":\"{4}\",\"source\":\"{5}\"}}".format(calc.id, calc.description,calc.reference,calc.component,calc.state, source)        
            if len(res) > 0 : 
                res+= ","
            res += s
        return "[" + res + "]"
    