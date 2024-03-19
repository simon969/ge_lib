import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class FRAC001(ags_query):
    def __init__(self):
        super().__init__(id='FRAC001', 
                         description="Is the FRAC group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the FRAC group is present and that it contains data")
    def run_query(self,  tables, headings):
        FRAC = self.get_group(tables, "FRAC", True)
        if (FRAC is not None):
            self.check_row_count(FRAC,"FRAC","HEADING == 'DATA'",1,10000)
class FRAC002(ags_query):
    def __init__(self):
        super().__init__(id='FRAC002', 
                         description="Is the FRAC_FROM and FRAC_TO headings completed for all records",
                         requirement = "mandatory",
                         action = "Check that the from and to of the fracture set have been recorded in the FRAC_FROM and FRAC_TO headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        FRAC = self.get_group(tables, "FRAC", True)
        if (LOCA is not None and FRAC is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(FRAC,"FRAC","FRAC_FROM",qry,0,FDEP)
                self.check_value(FRAC,"FRAC","FRAC_TO",qry,0,FDEP)
class FRAC003(ags_query):
    def __init__(self):
        super().__init__(id='FRAC003', 
                         description="Is the fracture set reference FRAC_SET recorded for all records in the FRAC group",
                         requirement = "mandatory",
                         action = "Check that the frcature set reference FRAC_SET been recorded for all records in the FRAC group")
    def run_query(self,  tables, headings):
        FRAC = self.get_group(tables, "FRAC", True)
        
        if (FRAC is not None):  
            self.check_string_length(FRAC,"FRAC","FRAC_SET","HEADING == 'DATA'",0,255)

class FRAC004(ags_query):
    def __init__(self, FRAC_FI_MIN, FRAC_FI_MAX):
        self.FRAC_FI_MIN = FRAC_FI_MIN
        self.FRAC_FI_MAX = FRAC_FI_MAX
        super().__init__(id='FRAC004', 
                         description="Is the fracture index FRAC_FI recorded for all records in the FRAC group",
                         requirement = "mandatory",
                         action = "Check that the fracture index FRAC_FI been recorded for all records in the FRAC group")
    def run_query(self,  tables, headings):
        FRAC = self.get_group(tables, "FRAC", True)
        
        if (FRAC is not None):  
            self.check_value(FRAC,"FRAC","FRAC_FI","HEADING == 'DATA'",self.FRAC_FI_MIN,self.FRAC_FI_MAX)
