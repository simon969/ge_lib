import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class WSTG001(ags_query):
    def __init__(self):
        super().__init__(id='WSTG001', 
                         description="Is the WSTG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the WSTG group is present and that it contains data")
    def run_query(self,  tables, headings):
        WSTG = self.get_group(tables, "WSTG", True)
        if (WSTG is not None):
            self.check_row_count(WSTG,"WSTG","HEADING == 'DATA'",1,10000)
class WSTG002(ags_query):
    def __init__(self):
        super().__init__(id='WSTG002', 
                         description="Is the WSTG_DPTH completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the water strike depth has been recorded in the WSTG_DPTH for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WSTG = self.get_group(tables, "WSTG", True)
        if (LOCA is not None and WSTG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WSTG,"WSTG","WSTG_DPTH",qry,0,FDEP)
class WSTG003(ags_query):
    def __init__(self, WSTG_DTIM_MIN, WSTG_DTIM_MAX):
        self.WSTG_DTIM_MIN = WSTG_DTIM_MIN
        self.WSTG_DTIM_MAX = WSTG_DTIM_MAX
        super().__init__(id='WSTG003', 
                         description="Is the date and time of the water strike recorded in the WSTG_DTIM heading with the of range {0} and {1} for all records in the WSTG group".format(self.WSTG_DTIM_MIN, self.WSTG_DTIM_MAX),
                         requirement = "mandatory",
                         action = "Check that date and time of the water strike has been recorded in WSTG_DTIM for all records in the WSTG group")
    def run_query(self,  tables, headings):
        WSTG = self.get_group(tables, "WSTG", True)
        
        if (WSTG is not None):  
            self.check_datetime(WSTG,"WSTG","WSTG_DTIM","HEADING == 'DATA'",self.WSTG_DTIM_MIN,self.WSTG_DTIM_MAX)

class WSTG004(ags_query):
    def __init__(self):
        super().__init__(id='WSTG004', 
                         description="Is the WSTG_SEAL completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the depth at which the water strike was sealed has been recorded in the WSTG_SEAL for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WSTG = self.get_group(tables, "WSTG", True)
        if (LOCA is not None and WSTG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WSTG,"WSTG","WSTG_SEAL",qry,0,FDEP)
class WSTG005(ags_query):
    def __init__(self):
        super().__init__(id='WSTG005', 
                         description="Is the WSTG_CAS completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the casing depth at the time of the water strike has been recorded in the WSTG_CAS for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WSTG = self.get_group(tables, "WSTG", True)
        if (LOCA is not None and WSTG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WSTG,"WSTG","WSTG_CAS",qry,0,FDEP)
class WSTG006(ags_query):
    def __init__(self):
        super().__init__(id='WSTG006', 
                         description="Is the WSTG_REM completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that remarks about the water strike have been recorded in the WSTG_REM for all records")
    def run_query(self,  tables, headings):
        WSTG = self.get_group(tables, "WSTG", True)
        
        if (WSTG is not None):
            self.check_string_length(WSTG,"WSTG","WSTG_REM","HEADING == 'DATA'", 0,255)