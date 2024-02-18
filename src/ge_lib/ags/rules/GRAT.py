import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class GRAT001(ags_query):
    def __init__(self):
        super().__init__(id='GRAT001', 
                         description="Is the GRAT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the GRAT group is present and that it contains data")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):
            self.check_row_count(GRAT,"GRAT","HEADING == 'DATA'",1,10000)
class GRAT002(ags_query):
    def __init__(self):
        super().__init__(id='GRAT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the GRAT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the GRAT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        GRAT = self.get_group(tables, "GRAT", True)
        if (LOCA is not None and GRAT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(GRAT,"GRAT","SAMP_TOP",qry,0,FDEP)
                self.check_value(GRAT,"GRAT","SPEC_DPTH",qry,0,FDEP)
class GRAT003(ags_query):
    def __init__(self):
        super().__init__(id='GRAT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the GRAT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_length(GRAT,"GRAT","SAMP_REF","HEADING == 'DATA'",1,100)

class GRAT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='GRATG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the GRAT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the GRAT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_allowed(GRAT,"GRAT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class GRAT005(ags_query):
    def __init__(self):
        super().__init__(id='GRAT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the GRAT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_length(GRAT,"GRAT","SAMP_ID","HEADING == 'DATA'",1,100)
class GRAT006(ags_query):
    def __init__(self):
        super().__init__(id='GRAT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the GRAT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_length(GRAT,"GRAT","SPEC_REF","HEADING == 'DATA'",1,100)
class GRAT007(ags_query):
    def __init__(self):
        super().__init__(id='GRAT007', 
                         description="Is the sieve or particle size GRAT_SIZE recorded for all records in the GRAT group",
                         requirement = "key field",
                         action = "Check that the sieve or particle size GRAT_SIZE is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_value(GRAT,"GRAT","GRAT_SIZE","HEADING == 'DATA'",0.00001,60)

class GRAT008(ags_query):
    def __init__(self):
        super().__init__(id='GRAT008', 
                         description="Have remarks GRAT_REM been recorded for all records in the GRAT group",
                         requirement = "check data",
                         action = "Check that remarks GRAT_REM are recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_length(GRAT,"GRAT","GRAT_REM","HEADING == 'DATA'",1,255)
class GRAT009(ags_query):
    def __init__(self):
        super().__init__(id='GRAT009', 
                         description="Is the test type GRAT_TYPE recorded for all records in the GRAT group",
                         requirement = "data required",
                         action = "Check that the test type GRAT_TYPE is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_string_length(GRAT,"GRAT","GRAT_TYPE","HEADING == 'DATA'",1,100)   
class GRAT010(ags_query):
    def __init__(self):
        super().__init__(id='GRAT010', 
                         description="Is the percentage passing GRAT_PERP finer than GRAT_SIZE is recorded for all records in the GRAT group",
                         requirement = "data required",
                         action = "Check that the percentage passing GRAT_PERP finer than GRAT_SIZE is recorded for all records in the GRAT group")
    def run_query(self,  tables, headings):
        GRAT = self.get_group(tables, "GRAT", True)
        if (GRAT is not None):  
            self.check_value(GRAT,"GRAT","GRAT_PERP","HEADING == 'DATA'",0,100)   
