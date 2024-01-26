import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class LNMC001(ags_query):
    def __init__(self):
        super().__init__(id='LNMC001', 
                         description="Is the LNMC group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the LNMC group is present and that it contains data")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):
            self.check_row_count(LNMC,"LNMC","HEADING == 'DATA'",1,10000)
class LNMC002(ags_query):
    def __init__(self):
        super().__init__(id='LNMC002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the LNMC group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        LNMC = self.get_group(tables, "LNMC", True)
        if (LOCA is not None and LNMC is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(LNMC,"LNMC","SAMP_TOP",qry,0,FDEP)
                self.check_value(LNMC,"LNMC","SPEC_DPTH",qry,0,FDEP)
class LNMC003(ags_query):
    def __init__(self):
        super().__init__(id='LNMC003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the LNMC group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_length(LNMC,"LNMC","SAMP_REF","HEADING == 'DATA'",1,100)

class LNMC004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='LNMCG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the LNMC group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the LNMC group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_allowed(LNMC,"LNMC","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class LNMC005(ags_query):
    def __init__(self):
        super().__init__(id='LNMC005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the LNMC group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_length(LNMC,"LNMC","SAMP_ID","HEADING == 'DATA'",1,100)
class LNMC006(ags_query):
    def __init__(self):
        super().__init__(id='LNMC006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the LNMC group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_length(LNMC,"LNMC","SPEC_REF","HEADING == 'DATA'",1,100)
class LNMC007(ags_query):
    def __init__(self):
        super().__init__(id='LNMC007', 
                         description="Is the liquid limit LNMC_LL recorded for all records in the LNMC group",
                         requirement = "data required",
                         action = "Check that the liquid limit LNMC_LL is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_value(LNMC,"LNMC","LNMC_LL","HEADING == 'DATA'",1,100)

class LNMC008(ags_query):
    def __init__(self):
        super().__init__(id='LNMC008', 
                         description="Have remarks LNMC_REM been recorded for all records in the LNMC group",
                         requirement = "check data",
                         action = "Check that remarks LNMC_REM are recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_length(LNMC,"LNMC","LNMC_REM","HEADING == 'DATA'",1,255)
class LNMC009(ags_query):
    def __init__(self, LNMC_METH_ALLOWED):
        self.LNMC_METH_ALLOWED=LNMC_METH_ALLOWED
        super().__init__(id='LNMC009', 
                         description="Is the test method LNMC_METH {0} recorded for all records in the LNMC group".format(self.LNMC_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type LNMC_METH {0} is recorded for all records in the LNMC group".format(self.LNMC_METH_ALLOWED))
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_string_allowed(LNMC,"LNMC","LNMC_METH","HEADING == 'DATA'",self.LNMC_METH_ALLOWED)   
class LNMC010(ags_query):
    def __init__(self):
        super().__init__(id='LNMC010', 
                         description="Is the plastic limit LNMC_PL recorded for all records in the LNMC group",
                         requirement = "data required",
                         action = "Check that the plastic limit LNMC_PL is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_value(LNMC,"LNMC","LNMC_PL","HEADING == 'DATA'",1,100)   
class LNMC011(ags_query):
    def __init__(self):
        super().__init__(id='LNMC011', 
                         description="Is the plasticity index LNMC_PI recorded for all records in the LNMC group",
                         requirement = "data required",
                         action = "Check that the plasticity index LNMC_PI is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_value(LNMC,"LNMC","LNMC_PI","HEADING == 'DATA'",1,100)   
class LNMC010(ags_query):
    def __init__(self):
        super().__init__(id='LNMC010', 
                         description="Is the percentage passing 425um sieve size LNMC_425 recorded for all records in the LNMC group",
                         requirement = "data required",
                         action = "Check that the percentage passing 425um sieve size LNMC_425 is recorded for all records in the LNMC group")
    def run_query(self,  tables, headings):
        LNMC = self.get_group(tables, "LNMC", True)
        if (LNMC is not None):  
            self.check_value(LNMC,"LNMC","LNMC_425","HEADING == 'DATA'",0,100)   

