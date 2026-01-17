import numpy as np
from .GroundModel import GroundModel
class GroundStiffness:
    def __init__(self, description, gm:GroundModel, level_top:float, level_base:float, increment: float):
        self.description = description
        self.levels = np.arange(level_top, level_base, increment)
        self.strata =  [None] * (self.levels.size)
        self.eu_modulus = [0.00] * self.levels.size
        self.ed_modulus = [0.00] * self.levels.size
        for x in range(self.levels.size):
            s = gm.get_attr_str(self.levels[x],"description")
            if (s is not None):
                self.strata[x] = s
                self.eu_modulus[x] = gm.get_attr_value(self.levels[x],"UndrainedEMod")
                self.ed_modulus[x] = gm.get_attr_value(self.levels[x],"DrainedEMod")
    def getStiffness(self):
        res = []
        for x in range(self.levels.size):
            r = {"level":self.levels[x],
                 "eu_modulus":self.eu_modulus[x],
                 "ed_modulus": self.ed_modulus[x],
                 "strata": self.strata[x]}
            res.append(r)
        return res
    def getStiffnessJSON(self):
        ret = []
        res =  self.getStiffness()
        for r in res:
            l = "{{\"level\":{0}, \"strata\":\"{1}\", \"eu_modulus\":{2}, \"ed_modulus\":{3}}}".format(r["level"],r["strata"],r["eu_modulus"], r["ed_modulus"])
            ret.append(l)
        return ret
    def getStiffnessCSV(self, select_columns = None, include_header_in_rows = False):
        rows = []
        res =  self.getStiffness()

        if select_columns is None:
            header = ["level","strata","eu_modulus","ed_modulus"]
        else:
            header = select_columns
        
        if (include_header_in_rows):
            rows.append (",".join(f"\"{w}\"" for w in header))
        
        for r in res:
            row = ""
            if select_columns is None:
                row = "{0},\"{1}\",{2},{3},{4}".format(r["level"],r["strata"],r["eu_modulus"],r["ed_modulus"])
            else:
                for column in select_columns:
                    if column=="level": row=+ str(r["level"]) + ","
                    if column=="strata": row=+ "\"" + r["strata"] + "\","
                    if column=="eu_modulus": row=+ str(r["eu_modulus"]) + ","
                    if column=="ed_modulus": row=+ str(r["ed_modulus"]) + ","
                rows.append(row)

        return ",".join(f"\"{w}\"" for w in header), rows
