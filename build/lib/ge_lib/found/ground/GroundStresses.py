import numpy as np
from .GroundModel import GroundModel


class GroundStresses:
    def __init__(self, description, gm:GroundModel, level_top:float, level_base:float, increment: float):
        self.description = description
        self.levels = np.arange(level_top, level_base, increment)
        self.strata =  [None] * (self.levels.size)
        self.total_stress = [0.00] * self.levels.size
        self.effective_stress = [0.00] * self.levels.size
        self.pwp = [0.00] * self.levels.size
        for x in range(self.levels.size):
            s = gm.get_attr_str(self.levels[x],"description")
            if (s is not None):
                self.strata[x] = s
                self.total_stress[x] = gm.get_attr_value(self.levels[x],"TotalStress")
                self.effective_stress[x] = gm.get_attr_value(self.levels[x],"EffectiveStress")
                self.pwp[x] = gm.get_attr_value(self.levels[x],"PWP")
    def getStresses(self):
        res = []
        for x in range(self.levels.size):
            r = {"level":self.levels[x],
                 "effective":self.effective_stress[x],
                 "total": self.total_stress[x],
                 "strata": self.strata[x],
                 "pwp": self.pwp[x]}
            res.append(r)
        return res
    def getStressesJSON(self):
        ret = []
        res =  self.getStresses()
        for r in res:
            l = "{{\"level\":{0}, \"strata\":\"{1}\", \"total\":{2}, \"pwp\":{3}, \"effective\":{4}}}".format(r["level"],r["strata"],r["total"], r["pwp"],r["effective"])
            ret.append(l)
        return ret
    def getStressesCSV(self, select_columns = None, include_header_in_rows = False):
        rows = []
        res =  self.getStresses()

        if select_columns is None:
            header = ["level","strata","total","pwp","effective"]
        else:
            header = select_columns
        
        if (include_header_in_rows):
            rows.append (",".join(f"\"{w}\"" for w in header))
        
        for r in res:
            row = ""
            if select_columns is None:
                row = "{0},\"{1}\",{2},{3},{4}".format(r["level"],r["strata"],r["total"],r["pwp"],r["effective"])
            else:
                for column in select_columns:
                    if column=="level": row=+ str(r["level"]) + ","
                    if column=="strata": row=+ "\"" + r["strata"] + "\","
                    if column=="total": row=+ str(r["total"]) + ","
                    if column=="pwp": row=+ str(r["pwp"]) + ","
                    if column=="effective": row=+ str(r["effective"]) + ","
            rows.append(row)

        return ",".join(f"\"{w}\"" for w in header), rows
