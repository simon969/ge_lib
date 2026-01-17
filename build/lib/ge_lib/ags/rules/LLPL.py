import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class LLPL001(ags_query):
    def __init__(self):
        super().__init__(id='LLPL001', 
                         description="Is the LLPL group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the LLPL group is present and that it contains data")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):
            self.check_row_count(LLPL,"LLPL","HEADING == 'DATA'",1,10000)
class LLPL002(ags_query):
    def __init__(self):
        super().__init__(id='LLPL002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the LLPL group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        LLPL = self.get_group(tables, "LLPL", True)
        if (LOCA is not None and LLPL is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(LLPL,"LLPL","SAMP_TOP",qry,0,FDEP)
                self.check_value(LLPL,"LLPL","SPEC_DPTH",qry,0,FDEP)
class LLPL003(ags_query):
    def __init__(self):
        super().__init__(id='LLPL003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the LLPL group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_length(LLPL,"LLPL","SAMP_REF","HEADING == 'DATA'",1,100)

class LLPL004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='LLPLG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the LLPL group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the LLPL group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_allowed(LLPL,"LLPL","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class LLPL005(ags_query):
    def __init__(self):
        super().__init__(id='LLPL005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the LLPL group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_length(LLPL,"LLPL","SAMP_ID","HEADING == 'DATA'",1,100)
class LLPL006(ags_query):
    def __init__(self):
        super().__init__(id='LLPL006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the LLPL group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_length(LLPL,"LLPL","SPEC_REF","HEADING == 'DATA'",1,100)
class LLPL007(ags_query):
    def __init__(self):
        super().__init__(id='LLPL007', 
                         description="Is the liquid limit LLPL_LL recorded for all records in the LLPL group",
                         requirement = "key field",
                         action = "Check that the liquid limit LLPL_LL is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_value(LLPL,"LLPL","LLPL_LL","HEADING == 'DATA'",1,100)

class LLPL008(ags_query):
    def __init__(self):
        super().__init__(id='LLPL008', 
                         description="Have remarks LLPL_REM been recorded for all records in the LLPL group",
                         requirement = "check data",
                         action = "Check that remarks LLPL_REM are recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_length(LLPL,"LLPL","LLPL_REM","HEADING == 'DATA'",1,255)
class LLPL009(ags_query):
    def __init__(self, LLPL_METH_ALLOWED):
        self.LLPL_METH_ALLOWED=LLPL_METH_ALLOWED
        super().__init__(id='LLPL009', 
                         description="Is the test method LLPL_METH {0} recorded for all records in the LLPL group".format(self.LLPL_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type LLPL_METH {0} is recorded for all records in the LLPL group".format(self.LLPL_METH_ALLOWED))
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_string_allowed(LLPL,"LLPL","LLPL_METH","HEADING == 'DATA'",self.LLPL_METH_ALLOWED)   
class LLPL010(ags_query):
    def __init__(self):
        super().__init__(id='LLPL010', 
                         description="Is the plastic limit LLPL_PL recorded for all records in the LLPL group",
                         requirement = "data required",
                         action = "Check that the plastic limit LLPL_PL is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_value(LLPL,"LLPL","LLPL_PL","HEADING == 'DATA'",1,100)   
class LLPL011(ags_query):
    def __init__(self):
        super().__init__(id='LLPL011', 
                         description="Is the plasticity index LLPL_PI recorded for all records in the LLPL group",
                         requirement = "data required",
                         action = "Check that the plasticity index LLPL_PI is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_value(LLPL,"LLPL","LLPL_PI","HEADING == 'DATA'",1,100)   
class LLPL010(ags_query):
    def __init__(self):
        super().__init__(id='LLPL010', 
                         description="Is the percentage passing 425um sieve size LLPL_425 recorded for all records in the LLPL group",
                         requirement = "data required",
                         action = "Check that the percentage passing 425um sieve size LLPL_425 is recorded for all records in the LLPL group")
    def run_query(self,  tables, headings):
        LLPL = self.get_group(tables, "LLPL", True)
        if (LLPL is not None):  
            self.check_value(LLPL,"LLPL","LLPL_425","HEADING == 'DATA'",0,100)   

