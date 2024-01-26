import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class RUCS001(ags_query):
    def __init__(self):
        super().__init__(id='RUCS001', 
                         description="Is the RUCS group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the RUCS group is present and that it contains data")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):
            self.check_row_count(RUCS,"RUCS","HEADING == 'DATA'",1,10000)
class RUCS002(ags_query):
    def __init__(self):
        super().__init__(id='RUCS002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the RUCS group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the RUCS group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        RUCS = self.get_group(tables, "RUCS", True)
        if (LOCA is not None and RUCS is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(RUCS,"RUCS","SAMP_TOP",qry,0,FDEP)
                self.check_value(RUCS,"RUCS","SPEC_DPTH",qry,0,FDEP)
class RUCS003(ags_query):
    def __init__(self):
        super().__init__(id='RUCS003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the RUCS group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","SAMP_REF","HEADING == 'DATA'",1,100)

class RUCS004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='RUCSG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the RUCS group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the RUCS group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_allowed(RUCS,"RUCS","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class RUCS005(ags_query):
    def __init__(self):
        super().__init__(id='RUCS005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the RUCS group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","SAMP_ID","HEADING == 'DATA'",1,100)
class RUCS006(ags_query):
    def __init__(self):
        super().__init__(id='RUCS006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the RUCS group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","SPEC_REF","HEADING == 'DATA'",1,100)
class RUCS007(ags_query):
    def __init__(self):
        super().__init__(id='RUCS007', 
                         description="Is the water content of the specimen RUCS_MC recorded for all records in the RUCS group",
                         requirement = "key field",
                         action = "Check that the water content of the specimen RUCS_MC is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_MC","HEADING == 'DATA'",0,30)

class RUCS008(ags_query):
    def __init__(self):
        super().__init__(id='RUCS008', 
                         description="Have remarks RUCS_REM been recorded for all records in the RUCS group",
                         requirement = "check data",
                         action = "Check that remarks RUCS_REM are recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","RUCS_REM","HEADING == 'DATA'",1,255)
class RUCS009(ags_query):
    def __init__(self, RUCS_METH_ALLOWED):
        self.RUCS_METH_ALLOWED=RUCS_METH_ALLOWED
        super().__init__(id='RUCS009', 
                         description="Is the test method RUCS_METH {0} recorded for all records in the RUCS group".format(self.RUCS_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type RUCS_METH {0} is recorded for all records in the RUCS group".format(self.RUCS_METH_ALLOWED))
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_allowed(RUCS,"RUCS","RUCS_METH","HEADING == 'DATA'",self.RUCS_METH_ALLOWED)   
class RUCS010(ags_query):
    def __init__(self,RUCS_SDIA_MIN, RUCS_SDIA_MAX,):
        self.RUCS_SDIA_MIN = RUCS_SDIA_MIN
        self.RUCS_SDIA_MAX = RUCS_SDIA_MAX
        super().__init__(id='RUCS010', 
                         description="Is the specimen dimater RUCS_SDIA recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that specimen diamter RUCS_SDIA is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_SDIA","HEADING == 'DATA'",self.RUCS_SDIA_MIN, self.RUCS_SDIA_MAX)   
class RUCS011(ags_query):
    def __init__(self):
        super().__init__(id='RUCS011', 
                         description="Is the specimen length RUCS_LEN recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that the specimen length RUCS_LEN is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_LEN","HEADING == 'DATA'",100,450)   
class RUCS012(ags_query):
    def __init__(self):
        super().__init__(id='RUCS012', 
                         description="Is the condition of the specimen RUCS_COND recorded for all records in the RUCS group",
                         requirement = "check data",
                         action = "Check that the specimen condition RUCS_COND is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","RUCS_COND","HEADING == 'DATA'",1,100)   
class RUCS013(ags_query):
    def __init__(self, RUCS_DURN_MIN, RUCS_DURN_MAX):
        self.RUCS_DURN_MIN = RUCS_DURN_MIN
        self.RUCS_DURN_MAX = RUCS_DURN_MAX
        super().__init__(id='RUCS013', 
                         description="Is the duration of the test RUCS_DURN recorded for all records in the RUCS group",
                         requirement = "check data",
                         action = "Check that the duration of the test RUCS_DURN is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_duration(RUCS,"RUCS","RUCS_DURN","HEADING == 'DATA'",self.RUCS_DURN_MIN,self.RUCS_DURN_MAX)  
class RUCS014(ags_query):
    def __init__(self, RUCS_STRA_MIN, RUCS_STRA_MAX):
        self.RUCS_STRA_MIN = RUCS_STRA_MIN
        self.RUCS_STRA_MAX = RUCS_STRA_MAX
        super().__init__(id='RUCS014', 
                         description="Is the stress rate RUCS_STRA recorded for all records in the RUCS group",
                         requirement = "check data",
                         action = "Check that the stress rate RUCS_STRA is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_STRA","HEADING == 'DATA'", self.RUCS_STRA_MIN,  self.RUCS_STRA_MAX)  
class RUCS015(ags_query):
    def __init__(self):
        super().__init__(id='RUCS015', 
                         description="Is the uniaxial compressive strength RUCS_UCS recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that the unixial compressive strength RUCS_UCS is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_UCS","HEADING == 'DATA'",0.01,25)  
class RUCS016(ags_query):
    def __init__(self):
        super().__init__(id='RUCS016', 
                         description="Is the mode of failuer RUCS_MODE recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that the mode of failure RUCS_MODE is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_length(RUCS,"RUCS","RUCS_MODE","HEADING == 'DATA'",1,100)  
class RUCS017(ags_query):
    def __init__(self):
        super().__init__(id='RUCS017', 
                         description="Is the elastic modulus RUCS_E recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that the elastic modulus RUCS_E is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_E","HEADING == 'DATA'",1, 100)  
class RUCS017(ags_query):
    def __init__(self):
        super().__init__(id='RUCS017', 
                         description="Is the poisson's ratio RUCS_MU recorded for all records in the RUCS group",
                         requirement = "data required",
                         action = "Check that the poisson's ratio RUCS_MU is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_MU","HEADING == 'DATA'",1, 100)  
class RUCS018(ags_query):
    def __init__(self):
        super().__init__(id='RUCS018', 
                         description="Is the stress level at which the moduls measured RUCS_ESTR recorded for all records in the RUCS group",
                         requirement = "check data",
                         action = "Check that the stress level at which the moduls measured RUCS_ESTR is recorded for all records in the RUCS group")
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_value(RUCS,"RUCS","RUCS_ESTR","HEADING == 'DATA'",1, 100)  
class RUCS019(ags_query):
    def __init__(self, RUCS_ETYP_ALLOWED):
        self.RUCS_ETYP_ALLOWED=RUCS_ETYP_ALLOWED
        super().__init__(id='RUCS009', 
                         description="Is the method for determining the modulus RUCS_ETYP {0} recorded for all records in the RUCS group".format(self.RUCS_ETYP_ALLOWED),
                         requirement = "data required",
                         action = "Check that the method for determing the modulus RUCS_ETYP {0} is recorded for all records in the RUCS group".format(self.RUCS_ETYP_ALLOWED))
    def run_query(self,  tables, headings):
        RUCS = self.get_group(tables, "RUCS", True)
        if (RUCS is not None):  
            self.check_string_allowed(RUCS,"RUCS","RUCS_ETYP","HEADING == 'DATA'",self.RUCS_ETYP_ALLOWED)   