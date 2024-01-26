import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class DOBS001(ags_query):
    def __init__(self):
        super().__init__(id='DOBS001', 
                         description="Is the DREM group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the DREM group is present and that it contains data")
    def run_query(self,  tables, headings):
        DREM = self.get_group(tables, "DREM", True)
        if (DREM is not None):
            self.check_row_count(DREM,"DREM","HEADING == 'DATA'",1,10000)
class DOBS002(ags_query):
    def __init__(self):
        super().__init__(id='DOBS002', 
                         description="Is the DOBS_TOP and DOBS_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the drilling advancment observations have been recorded in the DOBS_TOP and DOBS_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        DOBS = self.get_group(tables, "DOBS", True)
        if (LOCA is not None and DOBS is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(DOBS,"DOBS","DOBS_TOP",qry,0,FDEP)
                self.check_value(DOBS,"DOBS","DOBS_BASE",qry,0,FDEP)
class DOBS003(ags_query):
    def __init__(self):
        super().__init__(id='DOBS003', 
                         description="Is the drilling observation, parameter remarks heading DOBS_SET recorded for all records in the DOBS group",
                         requirement = "mandatory",
                         action = "Check that drilling observation, parameter remarks heading DOBS_SET have been recorded for all records in the DOBS group")
    def run_query(self,  tables, headings):
        DOBS= self.get_group(tables, "DOBS", True)
        
        if (DOBS is not None):  
            self.check_string_length(DOBS,"DOBS","DOBS_SET","HEADING == 'DATA'",0,255)

