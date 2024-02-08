import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class GCHM001(ags_query):
    def __init__(self):
        super().__init__(id='GCHM001', 
                         description="Is the GCHM group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the GCHM group is present and that it contains data")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):
            self.check_row_count(GCHM,"GCHM","HEADING == 'DATA'",1,10000)
class GCHM002(ags_query):
    def __init__(self):
        super().__init__(id='GCHM002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the GCHM group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        GCHM = self.get_group(tables, "GCHM", True)
        if (LOCA is not None and GCHM is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(GCHM,"GCHM","SAMP_TOP",qry,0,FDEP)
                self.check_value(GCHM,"GCHM","SPEC_DPTH",qry,0,FDEP)
class GCHM003(ags_query):
    def __init__(self):
        super().__init__(id='GCHM003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","SAMP_REF","HEADING == 'DATA'",1,100)

class GCHM004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='GCHMG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the GCHM group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the GCHM group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_allowed(GCHM,"GCHM","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class GCHM005(ags_query):
    def __init__(self):
        super().__init__(id='GCHM005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","SAMP_ID","HEADING == 'DATA'",1,100)
class GCHM006(ags_query):
    def __init__(self):
        super().__init__(id='GCHM006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","SPEC_REF","HEADING == 'DATA'",1,100)
class GCHM007(ags_query):
    def __init__(self):
        super().__init__(id='GCHM007', 
                         description="Is the determinand GCHM_CODE recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the determinand GCHM_CODE is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_CODE","HEADING == 'DATA'",0,100)

class GCHM008(ags_query):
    def __init__(self):
        super().__init__(id='GCHM008', 
                         description="Have remarks GCHM_REM been recorded for all records in the GCHM group",
                         requirement = "check data",
                         action = "Check that remarks GCHM_REM are recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_REM","HEADING == 'DATA'",1,255)
class GCHM009(ags_query):
    def __init__(self):
        super().__init__(id='GCHM009', 
                         description="Is the test method GCHM_METH recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the test method GCHM_METH is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_METH","HEADING == 'DATA'",1,100)   
class GCHM010(ags_query):
    def __init__(self):
        super().__init__(id='GCHM010', 
                         description="Is the test type GCHM_TTYP recorded for all records in the GCHM group",
                         requirement = "key field",
                         action = "Check that the test type GCHM_TTYP is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_TTYP","HEADING == 'DATA'",1,100)   
class GCHM011(ags_query):
    def __init__(self):
        super().__init__(id='GCHM011', 
                         description="Is the test result GCHM_RESL recorded for all records in the GCHM group",
                         requirement = "data required",
                         action = "Check that the test result GCHM_RESL is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_value(GCHM,"GCHM","GCHM_RESL","HEADING == 'DATA'",0.001,2500)   
class GCHM012(ags_query):
    def __init__(self):
        super().__init__(id='GCHM012', 
                         description="Is the test unit GCHM_UNIT recorded for all records in the GCHM group",
                         requirement = "data required",
                         action = "Check that the test unit GCHM_UNIT is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_UNIT","HEADING == 'DATA'",1,100)  
class GCHM013(ags_query):
    def __init__(self):
        super().__init__(id='GCHM013', 
                         description="Is the preferred name of determiand GCHM_NAME recorded for all records in the GCHM group",
                         requirement = "data required",
                         action = "Check that the preferred name of the determinand GCHM_NAME is recorded for all records in the GCHM group")
    def run_query(self,  tables, headings):
        GCHM = self.get_group(tables, "GCHM", True)
        if (GCHM is not None):  
            self.check_string_length(GCHM,"GCHM","GCHM_NAME","HEADING == 'DATA'",1,100)  