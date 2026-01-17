import math

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

def check_default_keys(data:dict, default_dict):
    for key, value in default_dict.items():
        data[key] = data.get(key, value)
    return data

def check_default_value(data:dict, prop_name:str, default_value:float):
    prop_value = data.get(prop_name,None)
    if prop_value is None:
        data[prop_name]=default_value

def all_have_values (s, props):
    for prop in props:
        if (s.__dict__.get(prop,None) == None):
            return False
    return True
def any_have_values (s, props):
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

