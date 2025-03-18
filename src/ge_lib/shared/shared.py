import json

class json_objs:
    def __init__(self, id, description, version, type):
        self.id = id
        self.description = description
        self.version = version
        self.type = type
        self.objs = {}
    def add (self,id,obj, description, version):
        data = {"obj":obj,
                "description":description,
                "version":version,
                "type":self.type}
        self.objs[id] = data
    
    def to_str(self, id):
        data = self.objs[id]
        if data is not None:
            s = json.dumps(data["obj"])
            return s