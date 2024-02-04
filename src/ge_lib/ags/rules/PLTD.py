import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class PLTD001(ags_query):
    def __init__(self):
        super().__init__(id='PLTD001', 
                         description="Is the PLTD group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the PLTD group is present and that it contains data")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        if (PLTD is not None):
            self.check_row_count(PLTD,"PLTD","HEADING == 'DATA'",1,10000)

class PLTD002(ags_query):
    def __init__(self):
        super().__init__(id='PLTD002', 
                         description="Is the permeability test number PLTD_TESN recorded for all records in the PLTD group",
                         requirement = "mandatory",
                         action = "Check that the permeability test number PLTD_TESN is recorded for all records in the PLTD group")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        
        if (PLTD is not None):  
            self.check_string_length(PLTD,"PLTD","PLTD_TESN","HEADING == 'DATA'",0,255)

class PLTD003(ags_query):
    def __init__(self):
        super().__init__(id='PLTD003', 
                         description="Is the depth to the top of the test PLTD_DPTH heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top of the tests PLTD_DPTH heading has been completed for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PLTD = self.get_group(tables, "PLTD", True)
        if (LOCA is not None and PLTD is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(PLTD,"PLTD","PLTD_DPTH",qry,0,FDEP)

class PLTD004(ags_query):
    def __init__(self):
        super().__init__(id='PLTD004', 
                         description="Is the plate load cycle PLTD_CYC recorded for all records in the PLTD group",
                         requirement = "mandatory",
                         action = "Check that the plate load cycle PLTD_CYC is recorded for all records in the PLTD group")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        
        if (PLTD is not None):  
            self.check_value(PLTD,"PLTD","PLTD_CYC","HEADING == 'DATA'",0,10)

class PLTD005(ags_query):
    def __init__(self):
        super().__init__(id='PLTD005', 
                         description="Is the plate load stage PLTD_STG recorded for all records in the PLTD group",
                         requirement = "mandatory",
                         action = "Check that the plate load stage PLTD_STG is recorded for all records in the PLTD group")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        
        if (PLTD is not None):  
            self.check_value(PLTD,"PLTD","PLTD_STG","HEADING == 'DATA'",0,10)

class PLTD006(ags_query):
    def __init__(self, PLTD_TIME_MIN, PLTD_TIME_MAX):
        self.PLTD_TIME_MIN = PLTD_TIME_MIN
        self.PLTD_TIME_MAX = PLTD_TIME_MAX
        super().__init__(id='PLTD006', 
                         description="Is the elapsed time PLTD_TIME recorded for all records in the PLTD group",
                         requirement = "mandatory",
                         action = "Check that the elapsed time PLTD_TIME is recorded for all records in the PLTD group")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        
        if (PLTD is not None):  
            self.check_duration(PLTD,"PLTD","PLTD_TIME","HEADING == 'DATA'",self.PLTD_TIME_MIN, self.PLTD_TIME_MAX)

class PLTD007(ags_query):
    def __init__(self):
        super().__init__(id='ICBR007', 
                         description="Have remarks PLTD_REM been recorded for all records in the PLTD group",
                         requirement = "mandatory",
                         action = "Check that remarks PLTD_REM are recorded for all records in the PLTD group")
    def run_query(self,  tables, headings):
        PLTD = self.get_group(tables, "PLTD", True)
        
        if (PLTD is not None):  
            self.check_string_length(PLTD,"PLTD","PLTD_REM","HEADING == 'DATA'",1,255)
