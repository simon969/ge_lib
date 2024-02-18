import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class CBRT001(ags_query):
    def __init__(self):
        super().__init__(id='CBRT001', 
                         description="Is the CBRT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CBRT group is present and that it contains data")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):
            self.check_row_count(CBRT,"CBRT","HEADING == 'DATA'",1,10000)
class CBRT002(ags_query):
    def __init__(self):
        super().__init__(id='CBRT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the CBRT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the CBRT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CBRT = self.get_group(tables, "CBRT", True)
        if (LOCA is not None and CBRT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CBRT,"CBRT","SAMP_TOP",qry,0,FDEP)
                self.check_value(CBRT,"CBRT","SPEC_DPTH",qry,0,FDEP)
class CBRT003(ags_query):
    def __init__(self):
        super().__init__(id='CBRT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the CBRT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the CBRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_length(CBRT,"CBRT","SAMP_REF","HEADING == 'DATA'",1,100)

class CBRT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='CBRTG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the CBRT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the CBRT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_allowed(CBRT,"CBRT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class CBRT005(ags_query):
    def __init__(self):
        super().__init__(id='CBRT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the CBRT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the CBRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_length(CBRT,"CBRT","SAMP_ID","HEADING == 'DATA'",1,100)
class CBRT006(ags_query):
    def __init__(self):
        super().__init__(id='CBRT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the CBRT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the CBRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_length(CBRT,"CBRT","SPEC_REF","HEADING == 'DATA'",1,100)
class CBRT007(ags_query):
    def __init__(self):
        super().__init__(id='CBRT007', 
                         description="Is the CBR test reference CBRT_TESN recorded for all records in the CBRT group",
                         requirement = "key field",
                         action = "Check that the CBR test reference CBRT_TESN is recorded for all records in the CBRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_length(CBRT,"CBRT","CBRT_TESN","HEADING == 'DATA'",0,100)

class CBRT008(ags_query):
    def __init__(self):
        super().__init__(id='CBRT008', 
                         description="Have remarks CBRT_REM been recorded for all records in the CBRT group",
                         requirement = "check data",
                         action = "Check that remarks CBRT_REM are recorded for all records in the CBRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_string_length(CBRT,"CBRT","CBRT_REM","HEADING == 'DATA'",1,255)
class CBRT009(ags_query):
    def __init__(self):
        super().__init__(id='CBRT009', 
                         description="Is the CBR test result at the top CBRT_TOP recorded for all records in the CBRT group",
                         requirement = "data required",
                         action = "Check that the insitu CBR test results at the top CBRT_TOP is recorded for all records in the CPRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_value(CBRT,"CBRT","CBRT_TOP","HEADING == 'DATA'",1,100)   
class CBRT010(ags_query):
    def __init__(self):
        super().__init__(id='CBRT010', 
                         description="Is the moisture content at the top CBRT_MCT recorded for all records in the CBRT group",
                         requirement = "data required",
                         action = "Check that the moisture content at the top CBRT_MCT is recorded for all records in the CPRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_value(CBRT,"CBRT","CBRT_MCT","HEADING == 'DATA'",1,100)   
class CBRT011(ags_query):
    def __init__(self):
        super().__init__(id='CBRT011', 
                         description="Is the CBR test result at the base CBRT_BASE recorded for all records in the CBRT group",
                         requirement = "data required",
                         action = "Check that the insitu CBR test results at the base CBRT_BASE is recorded for all records in the CPRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_value(CBRT,"CBRT","CBRT_BASE","HEADING == 'DATA'",1,100)   
class CBRT012(ags_query):
    def __init__(self):
        super().__init__(id='CBRT012', 
                         description="Is the moisture content at the base CBRT_MCB recorded for all records in the CBRT group",
                         requirement = "data required",
                         action = "Check that the moisture content at the top CBRT_MCB is recorded for all records in the CPRT group")
    def run_query(self,  tables, headings):
        CBRT = self.get_group(tables, "CBRT", True)
        if (CBRT is not None):  
            self.check_value(CBRT,"CBRT","CBRT_MCB","HEADING == 'DATA'",1,100)   