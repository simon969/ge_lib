import inspect

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

class calc:
    def __init__(self, id, description, reference, state, component, version):
        self.id = id
        self.state = state ## undrained/drained
        self.component = component ##shaft/base
        self.description = description
        self.reference = reference
        self.version =  version
    def calc(self, pile, gm, levels):
        pass
    def append(self, c):
        self.calcs.append(c)
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
    def to_id_list (self):
        res = []
        for calc in self.calcs:    
            res.append (calc.id)
        return res
    
    def to_json (self):
        to_return = {"id": self.id, "description": self.description}
        for calc in self.calcs:
            source = inspect.getsource(calc.calc)
            s =  "{{\"id\": \"{0}\", \"description\": \"{1}\",\"reference\":\"{2}\",\"component\":\"{3}\",\"stata\":\"{4}\",\"source\":\"{5}\"}}".format(calc.id, calc.description,calc.reference,calc.component,calc.state, source)        
            if len(res) > 0 : 
                res+= ","
            res += s
        return "[" + res + "]"
    