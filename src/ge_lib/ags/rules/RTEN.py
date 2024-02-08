import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class RTEN001(ags_query):
    def __init__(self):
        super().__init__(id='RTEN001', 
                         description="Is the RTEN group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the RTEN group is present and that it contains data")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):
            self.check_row_count(RTEN,"RTEN","HEADING == 'DATA'",1,10000)
class RTEN002(ags_query):
    def __init__(self):
        super().__init__(id='RTEN002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the RTEN group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the RTEN group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        RTEN = self.get_group(tables, "RTEN", True)
        if (LOCA is not None and RTEN is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(RTEN,"RTEN","SAMP_TOP",qry,0,FDEP)
                self.check_value(RTEN,"RTEN","SPEC_DPTH",qry,0,FDEP)
class RTEN003(ags_query):
    def __init__(self):
        super().__init__(id='RTEN003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the RTEN group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","SAMP_REF","HEADING == 'DATA'",1,100)

class RTEN004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='RTENG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the RTEN group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the RTEN group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_allowed(RTEN,"RTEN","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class RTEN005(ags_query):
    def __init__(self):
        super().__init__(id='RTEN005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the RTEN group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","SAMP_ID","HEADING == 'DATA'",1,100)
class RTEN006(ags_query):
    def __init__(self):
        super().__init__(id='RTEN006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the RTEN group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","SPEC_REF","HEADING == 'DATA'",1,100)
class RTEN007(ags_query):
    def __init__(self):
        super().__init__(id='RTEN007', 
                         description="Is the water content of the specimen RTEN_MC recorded for all records in the RTEN group",
                         requirement = "key field",
                         action = "Check that the water content of the specimen RTEN_MC is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_value(RTEN,"RTEN","RTEN_MC","HEADING == 'DATA'",0,30)

class RTEN008(ags_query):
    def __init__(self):
        super().__init__(id='RTEN008', 
                         description="Have remarks RTEN_REM been recorded for all records in the RTEN group",
                         requirement = "check data",
                         action = "Check that remarks RTEN_REM are recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","RTEN_REM","HEADING == 'DATA'",1,255)
class RTEN009(ags_query):
    def __init__(self, RTEN_METH_ALLOWED):
        self.RTEN_METH_ALLOWED=RTEN_METH_ALLOWED
        super().__init__(id='RTEN009', 
                         description="Is the test method RTEN_METH {0} recorded for all records in the RTEN group".format(self.RTEN_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type RTEN_METH {0} is recorded for all records in the RTEN group".format(self.RTEN_METH_ALLOWED))
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_allowed(RTEN,"RTEN","RTEN_METH","HEADING == 'DATA'",self.RTEN_METH_ALLOWED)   
class RTEN010(ags_query):
    def __init__(self,RTEN_SDIA_MIN, RTEN_SDIA_MAX,):
        self.RTEN_SDIA_MIN = RTEN_SDIA_MIN
        self.RTEN_SDIA_MAX = RTEN_SDIA_MAX
        super().__init__(id='RTEN010', 
                         description="Is the specimen dimater RTEN_SDIA recorded for all records in the RTEN group",
                         requirement = "data required",
                         action = "Check that specimen diamter RTEN_SDIA is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_value(RTEN,"RTEN","RTEN_SDIA","HEADING == 'DATA'",self.RTEN_SDIA_MIN, self.RTEN_SDIA_MAX)   
class RTEN011(ags_query):
    def __init__(self):
        super().__init__(id='RTEN011', 
                         description="Is the specimen length RTEN_LEN recorded for all records in the RTEN group",
                         requirement = "data required",
                         action = "Check that the specimen length RTEN_LEN is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_value(RTEN,"RTEN","RTEN_LEN","HEADING == 'DATA'",100,450)   
class RTEN012(ags_query):
    def __init__(self):
        super().__init__(id='RTEN012', 
                         description="Is the condition of the specimen RTEN_COND recorded for all records in the RTEN group",
                         requirement = "data required",
                         action = "Check that the specimen condition RTEN_COND is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","RTEN_COND","HEADING == 'DATA'",1,100)   
class RTEN013(ags_query):
    def __init__(self, RTEN_DURN_MIN, RTEN_DURN_MAX):
        self.RTEN_DURN_MIN = RTEN_DURN_MIN
        self.RTEN_DURN_MAX = RTEN_DURN_MAX
        super().__init__(id='RTEN013', 
                         description="Is the duration of the test RTEN_DURN recorded for all records in the RTEN group",
                         requirement = "check data",
                         action = "Check that the duration of the test RTEN_DURN is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_duration(RTEN,"RTEN","RTEN_DURN","HEADING == 'DATA'",self.RTEN_DURN_MIN,self.RTEN_DURN_MAX)  
class RTEN014(ags_query):
    def __init__(self, RTEN_STRA_MIN, RTEN_STRA_MAX):
        self.RTEN_STRA_MIN = RTEN_STRA_MIN
        self.RTEN_STRA_MAX = RTEN_STRA_MAX
        super().__init__(id='RTEN014', 
                         description="Is the stress rate RTEN_STRA recorded for all records in the RTEN group",
                         requirement = "check data",
                         action = "Check that the stress rate RTEN_STRA is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_value(RTEN,"RTEN","RTEN_STRA","HEADING == 'DATA'", self.RTEN_STRA_MIN,  self.RTEN_STRA_MAX)  
class RTEN015(ags_query):
    def __init__(self):
        super().__init__(id='RTEN015', 
                         description="Is the tensile strength RTEN_TENS recorded for all records in the RTEN group",
                         requirement = "data required",
                         action = "Check that the tensile strength RTEN_TENS is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_value(RTEN,"RTEN","RTEN_TENS","HEADING == 'DATA'",0.01,2.5)  
class RTEN016(ags_query):
    def __init__(self):
        super().__init__(id='RTEN016', 
                         description="Is the mode of failuer RTEN_MODE recorded for all records in the RTEN group",
                         requirement = "data required",
                         action = "Check that the mode of failure RTEN_MODE is recorded for all records in the RTEN group")
    def run_query(self,  tables, headings):
        RTEN = self.get_group(tables, "RTEN", True)
        if (RTEN is not None):  
            self.check_string_length(RTEN,"RTEN","RTEN_MODE","HEADING == 'DATA'",1,100)   