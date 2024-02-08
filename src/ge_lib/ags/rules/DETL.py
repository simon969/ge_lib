import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class DETL001(ags_query):
    def __init__(self):
        super().__init__(id='DETL001', 
                         description="Is the DETL group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the DETL group is present and that it contains data")
    def run_query(self,  tables, headings):
        DETL = self.get_group(tables, "DETL", True)
        if (DETL is not None):
            self.check_row_count(DETL,"DETL","HEADING == 'DATA'",1,10000)
class DETL002(ags_query):
    def __init__(self):
        super().__init__(id='DETL002', 
                         description="Is the DETL_TOP and DETL_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the geology detail have been recorded in the DETL_TOP and DETL_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        DETL = self.get_group(tables, "DETL", True)
        if (LOCA is not None and DETL is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(DETL,"DETL","DETL_TOP",qry,0,FDEP)
                self.check_value(DETL,"DETL","DETL_BASE",qry,0,FDEP)
class DETL003(ags_query):
    def __init__(self):
        super().__init__(id='DETL003', 
                         description="Is the geology detail description DETL_DESC recorded for all records in the DETL group",
                         requirement = "mandatory",
                         action = "Check that the geology detail description DETL_DESC been recorded for all records in the DETL group")
    def run_query(self,  tables, headings):
        DETL = self.get_group(tables, "DETL", True)
        
        if (DETL is not None):  
            self.check_string_length(DETL,"DETL","DETL_DESC","HEADING == 'DATA'",0,255)

