import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class PLTG001(ags_query):
    def __init__(self):
        super().__init__(id='PLTG001', 
                         description="Is the PLTG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the PLTG group is present and that it contains data")
    def run_query(self,  tables, headings):
        PLTG = self.get_group(tables, "PLTG", True)
        if (PLTG is not None):
            self.check_row_count(PLTG,"PLTG","HEADING == 'DATA'",1,10000)

class PLTG002(ags_query):
    def __init__(self):
        super().__init__(id='PLTG002', 
                         description="Is the plate load test number PLTG_TESN recorded for all records in the PLTG group",
                         requirement = "mandatory",
                         action = "Check that the plate load test number PLTG_TESN is recorded for all records in the PLTG group")
    def run_query(self,  tables, headings):
        PLTG = self.get_group(tables, "PLTG", True)
        
        if (PLTG is not None):  
            self.check_string_length(PLTG,"PLTG","PLTG_TESN","HEADING == 'DATA'",0,255)

class PLTG003(ags_query):
    def __init__(self):
        super().__init__(id='PLTG003', 
                         description="Is the depth to the top of the plate load test PLTG_DPTH recorded for all records",
                         requirement = "mandatory",
                         action = "Check that the depth to the top of the plate load test PLTG_DPTH is recorded for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PLTG = self.get_group(tables, "PLTG", True)
        if (LOCA is not None and PLTG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(PLTG,"PLTG","PLTG_DPTH",qry,0,FDEP)

class PLTG004(ags_query):
    def __init__(self):
        super().__init__(id='PLTG004', 
                         description="Is the insitu CBR test cycle PLTG_CYC recorded for all records in the PLTG group",
                         requirement = "mandatory",
                         action = "Check that the insitu CBR test cycle PLTG_CYC is recorded for all records in the PLTG group")
    def run_query(self,  tables, headings):
        PLTG = self.get_group(tables, "PLTG", True)
        
        if (PLTG is not None):  
            self.check_value(PLTG,"PLTG","PLTG_CYC","HEADING == 'DATA'",0,100)
class PLTG005(ags_query):
    def __init__(self):
        super().__init__(id='PLTG005', 
                         description="Have remarks PLTG_REM been recorded for all records in the PLTG group",
                         requirement = "mandatory",
                         action = "Check that remarks PLTG_REM are recorded for all records in the PLTG group")
    def run_query(self,  tables, headings):
        PLTG = self.get_group(tables, "PLTG", True)
        
        if (PLTG is not None):  
            self.check_string_length(PLTG,"PLTG","PLTG_REM","HEADING == 'DATA'",1,255)
class PLTG006(ags_query):
    def __init__(self, PLTG_METH_ALLOWED):
        self.PLTG_METH_ALLOWED = PLTG_METH_ALLOWED
        super().__init__(id='PLTG006', 
                         description="Is the insitu CBR test method PLTG_METH recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the insitu CBR test method PLTG_METH is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        PLTG = self.get_group(tables, "PLTG", True)
        
        if (PLTG is not None):  
            self.check_string_allowed(PLTG,"PLTG","PLTG_METH","HEADING == 'DATA'",self.PLTG_METH_ALLOWED)   
 