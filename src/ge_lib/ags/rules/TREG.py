import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class TREG001(ags_query):
    def __init__(self):
        super().__init__(id='TREG001', 
                         description="Is the TREG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the TREG group is present and that it contains data")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):
            self.check_row_count(TREG,"TREG","HEADING == 'DATA'",1,10000)
class TREG002(ags_query):
    def __init__(self):
        super().__init__(id='TREG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the TREG group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the TREG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        TREG = self.get_group(tables, "TREG", True)
        if (LOCA is not None and TREG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(TREG,"TREG","SAMP_TOP",qry,0,FDEP)
                self.check_value(TREG,"TREG","SPEC_DPTH",qry,0,FDEP)
class TREG003(ags_query):
    def __init__(self):
        super().__init__(id='TREG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the TREG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","SAMP_REF","HEADING == 'DATA'",1,100)

class TREG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='TREGG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the TREG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the TREG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_allowed(TREG,"TREG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class TREG005(ags_query):
    def __init__(self):
        super().__init__(id='TREG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the TREG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","SAMP_ID","HEADING == 'DATA'",1,100)
class TREG006(ags_query):
    def __init__(self):
        super().__init__(id='TREG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the TREG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","SPEC_REF","HEADING == 'DATA'",1,100)
class TREG007(ags_query):
    def __init__(self, TREG_TYPE_ALLOWED):
        self.TREG_TYPE_ALLOWED= TREG_TYPE_ALLOWED
        super().__init__(id='TREG007', 
                         description="Is the test type TREG_TYPE recorded for all records in the TREG group",
                         requirement = "key field",
                         action = "Check that the test type TREG_TYPE is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_allowed(TREG,"TREG","TREG_TYPE","HEADING == 'DATA'",self.TREG_TYPE_ALLOWED)

class TREG008(ags_query):
    def __init__(self):
        super().__init__(id='TREG008', 
                         description="Have remarks TREG_REM been recorded for all records in the TREG group",
                         requirement = "check data",
                         action = "Check that remarks TREG_REM are recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","TREG_REM","HEADING == 'DATA'",1,255)
class TREG009(ags_query):
    def __init__(self, TREG_METH_ALLOWED):
        self.TREG_METH_ALLOWED=TREG_METH_ALLOWED
        super().__init__(id='TREG009', 
                         description="Is the test method TREG_METH {0} recorded for all records in the TREG group".format(self.TREG_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type TREG_METH {0} is recorded for all records in the TREG group".format(self.TREG_METH_ALLOWED))
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_allowed(TREG,"TREG","TREG_METH","HEADING == 'DATA'",self.TREG_METH_ALLOWED)   
class TREG010(ags_query):
    def __init__(self):
        super().__init__(id='TREG010', 
                         description="Is the sample condition TREG_COND recorded for all records in the TREG group",
                         requirement = "data required",
                         action = "Check that the sample condition TREG_COND is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","TREG_COND","HEADING == 'DATA'",1,100)   
class TREG011(ags_query):
    def __init__(self):
        super().__init__(id='TREG011', 
                         description="Is the failure criterin TREG_FCR recorded for all records in the TREG group",
                         requirement = "data required",
                         action = "Check that failure criterion TREG_FCR is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_string_length(TREG,"TREG","TREG_FCR","HEADING == 'DATA'",1,255)   
class TREG012(ags_query):
    def __init__(self):
        super().__init__(id='TREG012', 
                         description="Is the cohesion intercept TREG_COH recorded for all records in the TREG group",
                         requirement = "data required",
                         action = "Check that the cohesion intercept TREG_COH is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_value(TREG,"TREG","TREG_COH","HEADING == 'DATA'",0,25)   
class TREG013(ags_query):
    def __init__(self):
        super().__init__(id='TREG013', 
                         description="Is the friction angle TREG_PHI recorded for all records in the TREG group",
                         requirement = "data required",
                         action = "Check that the friction angle TREG_PHI is recorded for all records in the TREG group")
    def run_query(self,  tables, headings):
        TREG = self.get_group(tables, "TREG", True)
        if (TREG is not None):  
            self.check_value(TREG,"TREG","TREG_PHI","HEADING == 'DATA'",0,45)  
