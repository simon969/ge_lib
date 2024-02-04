import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class CBRG001(ags_query):
    def __init__(self):
        super().__init__(id='CBRG001', 
                         description="Is the CBRG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CBRG group is present and that it contains data")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):
            self.check_row_count(CBRG,"CBRG","HEADING == 'DATA'",1,10000)
class CBRG002(ags_query):
    def __init__(self):
        super().__init__(id='CBRG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CBRG = self.get_group(tables, "CBRG", True)
        if (LOCA is not None and CBRG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CBRG,"CBRG","SAMP_TOP",qry,0,FDEP)
                self.check_value(CBRG,"CBRG","SPEC_DPTH",qry,0,FDEP)
class CBRG003(ags_query):
    def __init__(self):
        super().__init__(id='CBRG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the CBRG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the CBRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","SAMP_REF","HEADING == 'DATA'",1,100)

class CBRG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='CBRG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the CBRG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the CBRG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_allowed(CBRG,"CBRG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class CBRG005(ags_query):
    def __init__(self):
        super().__init__(id='CBRG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the CBRG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the CBRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","SAMP_ID","HEADING == 'DATA'",1,100)
class CBRG006(ags_query):
    def __init__(self):
        super().__init__(id='CBRG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the CBRG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the CBRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","SPEC_REF","HEADING == 'DATA'",1,100)
class CBRG007(ags_query):
    def __init__(self):
        super().__init__(id='CBRG007', 
                         description="Is the sample condition CBRG_COND recorded for all records in the CBRG group",
                         requirement = "check data",
                         action = "Check that the sample condition CBR_COND is recorded for all records in the CBRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","CBRG_COND","HEADING == 'DATA'",0,255)

class CBRG008(ags_query):
    def __init__(self):
        super().__init__(id='CBR008', 
                         description="Have remarks CBRG_REM been recorded for all records in the CBRG group",
                         requirement = "check data",
                         action = "Check that remarks CBRG_REM are recorded for all records in the CBRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","CBRG_REM","HEADING == 'DATA'",1,255)
class CBRG009(ags_query):
    def __init__(self):
        super().__init__(id='CBRG009', 
                         description="Is the laboratory CBR test method CBRG_METH recorded for all records in the CBRG group",
                         requirement = "data required",
                         action = "Check that the insitu CBR test method ICBR_METH is recorded for all records in the CPRG group")
    def run_query(self,  tables, headings):
        CBRG = self.get_group(tables, "CBRG", True)
        if (CBRG is not None):  
            self.check_string_length(CBRG,"CBRG","CBRG_METH","HEADING == 'DATA'",1,255)   
 