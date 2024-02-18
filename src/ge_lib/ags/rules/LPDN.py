import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class LPDN001(ags_query):
    def __init__(self):
        super().__init__(id='LPDN001', 
                         description="Is the LPDN group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the LPDN group is present and that it contains data")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):
            self.check_row_count(LPDN,"LPDN","HEADING == 'DATA'",1,10000)
class LPDN002(ags_query):
    def __init__(self):
        super().__init__(id='LPDN002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the LPDN group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        LPDN = self.get_group(tables, "LPDN", True)
        if (LOCA is not None and LPDN is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(LPDN,"LPDN","SAMP_TOP",qry,0,FDEP)
                self.check_value(LPDN,"LPDN","SPEC_DPTH",qry,0,FDEP)
class LPDN003(ags_query):
    def __init__(self):
        super().__init__(id='LPDN003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the LPDN group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_length(LPDN,"LPDN","SAMP_REF","HEADING == 'DATA'",1,100)

class LPDN004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='LPDNG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the LPDN group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the LPDN group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_allowed(LPDN,"LPDN","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class LPDN005(ags_query):
    def __init__(self):
        super().__init__(id='LPDN005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the LPDN group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_length(LPDN,"LPDN","SAMP_ID","HEADING == 'DATA'",1,100)
class LPDN006(ags_query):
    def __init__(self):
        super().__init__(id='LPDN006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the LPDN group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_length(LPDN,"LPDN","SPEC_REF","HEADING == 'DATA'",1,100)
class LPDN007(ags_query):
    def __init__(self):
        super().__init__(id='LPDN007', 
                         description="Is the particle density LPDN_PDEN recorded for all records in the LPDN group",
                         requirement = "data required",
                         action = "Check that the particle density LPDN_PDEN is recorded for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_value(LPDN,"LPDN","LPDN_PDEN","HEADING == 'DATA'",1,100)

class LPDN008(ags_query):
    def __init__(self):
        super().__init__(id='LPDN008', 
                         description="Have remarks LPDN_REM been recorded for all records in the LPDN group",
                         requirement = "check data",
                         action = "Check that remarks LPDN_REM are recorded for all records in the LPDN group")
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_length(LPDN,"LPDN","LPDN_REM","HEADING == 'DATA'",1,255)
class LPDN009(ags_query):
    def __init__(self, LPDN_METH_ALLOWED):
        self.LPDN_METH_ALLOWED=LPDN_METH_ALLOWED
        super().__init__(id='LPDN009', 
                         description="Is the test method LPDN_METH {0} recorded for all records in the LPDN group".format(self.LPDN_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type LPDN_METH {0} is recorded for all records in the LPDN group".format(self.LPDN_METH_ALLOWED))
    def run_query(self,  tables, headings):
        LPDN = self.get_group(tables, "LPDN", True)
        if (LPDN is not None):  
            self.check_string_allowed(LPDN,"LPDN","LPDN_METH","HEADING == 'DATA'",self.LPDN_METH_ALLOWED)   

