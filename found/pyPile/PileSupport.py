import inspect

class pile_calc:
    def __init__(self, id, description, reference, state, component, version):
        self.id = id
        self.state = state ## undrained/drained
        self.component = component ##shaft/base
        self.description = description
        self.reference = reference
        self.version =  version
    def calc(self, pile, gm, levels):
        pass

class pile_calc_collection:
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
    