import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class DREM001(ags_query):
    def __init__(self):
        super().__init__(id='DREM001', 
                         description="Is the DREM group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the DREM group is present and that it contains data")
    def run_query(self,  tables, headings):
        DREM = self.get_group(tables, "DREM", True)
        if (DREM is not None):
            self.check_row_count(DREM,"DREM","HEADING == 'DATA'",1,10000)
class DREM002(ags_query):
    def __init__(self, LOCA_TYPE_MUST):
        self.LOCA_TYPE_MUST = LOCA_TYPE_MUST
        super().__init__(id='DREM002', 
                         description="Does each LOCA_TYPE {0} in the LOCA group have a minimum of one drilling remarks record in the DREM group".format(self.LOCA_TYPE_MUST),
                         requirement = "mandatory",
                         action = "Check that the DREM group contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        DREM = self.get_group(tables, "DREM", True)
        if (LOCA is not None and DREM is not None):  
            lLOCA =  LOCA.query("LOCA_TYPE in ({})".format(self.LOCA_TYPE_MUST))  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(DREM,"DREM",qry, 1,10)
class DREM003(ags_query):
    def __init__(self):
        super().__init__(id='DREM003', 
                         description="Is the DREM_TOP and DREM_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the drilling remarks run have been recorded in the DREM_TOP and DREM_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        DREM = self.get_group(tables, "DREM", True)
        if (LOCA is not None and DREM is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(DREM,"DREM","DREM_TOP",qry,0,FDEP)
                self.check_value(DREM,"DREM","DREM_BASE",qry,0,FDEP)
class DREM004(ags_query):
    def __init__(self):
        super().__init__(id='DREM004', 
                         description="Is the drilling remarks heading DREM_REM recorded for all records in the DREM group",
                         requirement = "mandatory",
                         action = "Check that drilling remarks DREM_REM have been recorded for all records in the DREM group")
    def run_query(self,  tables, headings):
        DREM = self.get_group(tables, "DREM", True)
        
        if (DREM is not None):  
            self.check_string_length(DREM,"DREM","DREM_REM","HEADING == 'DATA'",0,255)

