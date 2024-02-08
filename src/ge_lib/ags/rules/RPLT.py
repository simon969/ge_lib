import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class RPLT001(ags_query):
    def __init__(self):
        super().__init__(id='RPLT001', 
                         description="Is the RPLT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the RPLT group is present and that it contains data")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):
            self.check_row_count(RPLT,"RPLT","HEADING == 'DATA'",1,10000)
class RPLT002(ags_query):
    def __init__(self):
        super().__init__(id='RPLT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the RPLT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the RPLT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        RPLT = self.get_group(tables, "RPLT", True)
        if (LOCA is not None and RPLT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(RPLT,"RPLT","SAMP_TOP",qry,0,FDEP)
                self.check_value(RPLT,"RPLT","SPEC_DPTH",qry,0,FDEP)
class RPLT003(ags_query):
    def __init__(self):
        super().__init__(id='RPLT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the RPLT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_length(RPLT,"RPLT","SAMP_REF","HEADING == 'DATA'",1,100)

class RPLT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='RPLTG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the RPLT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the RPLT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_allowed(RPLT,"RPLT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class RPLT005(ags_query):
    def __init__(self):
        super().__init__(id='RPLT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the RPLT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_length(RPLT,"RPLT","SAMP_ID","HEADING == 'DATA'",1,100)
class RPLT006(ags_query):
    def __init__(self):
        super().__init__(id='RPLT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the RPLT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_length(RPLT,"RPLT","SPEC_REF","HEADING == 'DATA'",1,100)
class RPLT007(ags_query):
    def __init__(self):
        super().__init__(id='RPLT007', 
                         description="Is the water content of the specimen RPLT_MC recorded for all records in the RPLT group",
                         requirement = "check data",
                         action = "Check that the water content of the specimen RPLT_MC is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_value(RPLT,"RPLT","RPLT_MC","HEADING == 'DATA'",0,30)

class RPLT008(ags_query):
    def __init__(self):
        super().__init__(id='RPLT008', 
                         description="Have remarks RPLT_REM been recorded for all records in the RPLT group",
                         requirement = "check data",
                         action = "Check that remarks RPLT_REM are recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_length(RPLT,"RPLT","RPLT_REM","HEADING == 'DATA'",1,255)
class RPLT009(ags_query):
    def __init__(self, RPLT_METH_ALLOWED):
        self.RPLT_METH_ALLOWED=RPLT_METH_ALLOWED
        super().__init__(id='RPLT009', 
                         description="Is the test method RPLT_METH {0} recorded for all records in the RPLT group".format(self.RPLT_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type RPLT_METH {0} is recorded for all records in the RPLT group".format(self.RPLT_METH_ALLOWED))
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_allowed(RPLT,"RPLT","RPLT_METH","HEADING == 'DATA'",self.RPLT_METH_ALLOWED)   
class RPLT010(ags_query):
    def __init__(self):
        super().__init__(id='RPLT010', 
                         description="Is the uncorrected point load test RPLT_PLS recorded for all records in the RPLT group",
                         requirement = "data required",
                         action = "Check that the uncorrected point load test RPLT_PLS is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_value(RPLT,"RPLT","RPLT_PLS","HEADING == 'DATA'",0.1, 2.5)   
class RPLT011(ags_query):
    def __init__(self):
        super().__init__(id='RPLT011', 
                         description="Is the size corrected point load test RPLT_PLSI recorded for all records in the RPLT group",
                         requirement = "data required",
                         action = "Check that the size corrected point load test RPLT_PLSI is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_value(RPLT,"RPLT","RPLT_PLSI","HEADING == 'DATA'",0.1,2.5)   
class RPLT012(ags_query):
    def __init__(self,RPLT_PLTF_ALLOWED):
        self.RPLT_PLTF_ALLOWED= RPLT_PLTF_ALLOWED
        super().__init__(id='RPLT012', 
                         description="Is the point load test type RPLT_PLTF recorded for all records in the RPLT group",
                         requirement = "data required",
                         action = "Check that the point load test type RPLT_PLTF is recorded for all records in the RPLT group")
    def run_query(self,  tables, headings):
        RPLT = self.get_group(tables, "RPLT", True)
        if (RPLT is not None):  
            self.check_string_allowed(RPLT,"RPLT","RPLT_PLTF","HEADING == 'DATA'",self.RPLT_PLTF_ALLOWED)   
