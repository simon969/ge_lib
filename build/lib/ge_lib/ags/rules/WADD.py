import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class WADD001(ags_query):
    def __init__(self):
        super().__init__(id='WADD001', 
                         description="Is the WADD group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the WADD group is present and that it contains data")
    def run_query(self,  tables, headings):
        WADD = self.get_group(tables, "WADD", True)
        if (WADD is not None):
            self.check_row_count(WADD,"WADD","HEADING == 'DATA'",1,10000)
class WADD002(ags_query):
    def __init__(self):
        super().__init__(id='WADD002', 
                         description="Is the WADD_TOP and WADD_BASE heading completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the water added top and base depths have been recorded in the WADD_TOP and WADD_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WADD = self.get_group(tables, "WADD", True)
        if (LOCA is not None and WADD is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WADD,"WADD","WADD_TOP",qry,0,FDEP)
                self.check_value(WADD,"WADD","WADD_BASE",qry,0,FDEP)
class WADD003(ags_query):
    def __init__(self, WADD_VOLM_MIN, WADD_VOLM_MAX):
        self.WADD_VOLM_MIN = WADD_VOLM_MIN
        self.WADD_VOLM_MAX = WADD_VOLM_MAX
        super().__init__(id='WADD003', 
                         description="Is the volume of water added WADD_VOLM recorded for all records in the WADD group",
                         requirement = "mandatory",
                         action = "Check that volume of water has been recorded in WADD_VOLM for all records in the WADD group")
    def run_query(self,  tables, headings):
        WADD= self.get_group(tables, "WADD", True)
        
        if (WADD is not None):  
            self.check_value(WADD,"WADD","WADD_VOLM","HEADING == 'DATA'",self.WADD_VOLM_MIN,self.WADD_VOLM_MAX)

