import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class WSTD001(ags_query):
    def __init__(self):
        super().__init__(id='WSTD001', 
                         description="Is the WSTD group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the WSTD group is present and that it contains data")
    def run_query(self,  tables, headings):
        WSTD = self.get_group(tables, "WSTD", True)
        if (WSTD is not None):
            self.check_row_count(WSTD,"WSTD","HEADING == 'DATA'",1,10000)
class WSTD002(ags_query):
    def __init__(self):
        super().__init__(id='WSTD002', 
                         description="Is there at least one WSTD record for every WSTG record",
                         requirement = "optional",
                         action = "Check that the WSTD group contains at least one record for every WSTG record")
    def run_query(self,  tables, headings):
        WSTG = self.get_group (tables, "WSTG", True)
        WSTD = self.get_group(tables, "WSTD", True)

        if (WSTG is not None and WSTD is not None):
            wstg =  WSTG.query("HEADING == 'DATA'")  
            for index, values in wstg.iterrows():
                loca_id = values['LOCA_ID']
                wstg_dpth = values['WSTG_DPTH']
                qry = "LOCA_ID == '{0}' and WSTG_DPTH == {1}".format(loca_id, wstg_dpth)
                self.check_row_count(WSTD,"WSTD",qry,1,10000)
    
class WSTD003(ags_query):
    def __init__(self, WSTD_NMIN_MIN, WSTD_NMIN_MAX):
        self.WSTD_NMIN_MIN = WSTD_NMIN_MIN
        self.WSTD_NMIN_MAX = WSTD_NMIN_MAX  
        super().__init__(id='WSTD003', 
                         description="Is the WSTD_NMIN completed for all records in the WSTD group",
                         requirement = "mandatory",
                         action = "Check that the minutes after water strike have been recorded in the WSTD_NMIN for all records")
    def run_query(self,  tables, headings):
        WSTD = self.get_group(tables, "WSTD", True)
        
        if (WSTD is not None):
            self.check_duration(WSTD,"WSTD","WSTD_NMIN","HEADING == 'DATA'",self.WSTD_NMIN_MIN, self.WSTD_NMIN_MAX)

class WSTD004(ags_query):
    def __init__(self):
        super().__init__(id='WSTD004', 
                         description="Is the WSTD_POST completed for all records in the WSTD group and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the water depth after monitoring has been recorded in the WSTD_POST for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WSTD = self.get_group(tables, "WSTD", True)
        if (LOCA is not None and WSTD is not None):
            loca =  LOCA.query("HEADING == 'DATA'")  
            for index, values in loca.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WSTD,"WSTD","WSTD_POST",qry,0,FDEP)
class WSTD005(ags_query):
    def __init__(self):
        super().__init__(id='WSTD005', 
                         description="Is the WSTD_REM completed for all records in the WSTD group",
                         requirement = "mandatory",
                         action = "Check that remarks about the water strike have been recorded in the WSTD_REM for all records")
    def run_query(self,  tables, headings):
        WSTD = self.get_group(tables, "WSTD", True)

        if (WSTD is not None):
            self.check_string_length(WSTD,"WSTD","WSTD_REM","HEADING == 'DATA'", 0,255)