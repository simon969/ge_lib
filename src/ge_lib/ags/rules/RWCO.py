import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class RWCO001(ags_query):
    def __init__(self):
        super().__init__(id='RWCO001', 
                         description="Is the RWCO group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the RWCO group is present and that it contains data")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):
            self.check_row_count(RWCO,"RWCO","HEADING == 'DATA'",1,10000)
class RWCO002(ags_query):
    def __init__(self):
        super().__init__(id='RWCO002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the RWCO group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the RWCO group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        RWCO = self.get_group(tables, "RWCO", True)
        if (LOCA is not None and RWCO is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(RWCO,"RWCO","SAMP_TOP",qry,0,FDEP)
                self.check_value(RWCO,"RWCO","SPEC_DPTH",qry,0,FDEP)
class RWCO003(ags_query):
    def __init__(self):
        super().__init__(id='RWCO003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the RWCO group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the RWCO group")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_length(RWCO,"RWCO","SAMP_REF","HEADING == 'DATA'",1,100)

class RWCO004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='RWCOG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the RWCO group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the RWCO group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_allowed(RWCO,"RWCO","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class RWCO005(ags_query):
    def __init__(self):
        super().__init__(id='RWCO005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the RWCO group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the RWCO group")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_length(RWCO,"RWCO","SAMP_ID","HEADING == 'DATA'",1,100)
class RWCO006(ags_query):
    def __init__(self):
        super().__init__(id='RWCO006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the RWCO group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the RWCO group")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_length(RWCO,"RWCO","SPEC_REF","HEADING == 'DATA'",1,100)

class RWCO007(ags_query):
    def __init__(self):
        super().__init__(id='RWCO007', 
                         description="Have remarks RWCO_REM been recorded for all records in the RWCO group",
                         requirement = "check data",
                         action = "Check that remarks RWCO_REM are recorded for all records in the RWCO group")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_length(RWCO,"RWCO","RWCO_REM","HEADING == 'DATA'",1,255)
class RWCO008(ags_query):
    def __init__(self, RWCO_METH_ALLOWED):
        self.RWCO_METH_ALLOWED=RWCO_METH_ALLOWED
        super().__init__(id='RWCO008', 
                         description="Is the test method RWCO_METH {0} recorded for all records in the RWCO group".format(self.RWCO_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type RWCO_METH {0} is recorded for all records in the RWCO group".format(self.RWCO_METH_ALLOWED))
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_string_allowed(RWCO,"RWCO","RWCO_METH","HEADING == 'DATA'",self.RWCO_METH_ALLOWED)   
class RWCO009(ags_query):
    def __init__(self):
        super().__init__(id='RWCO009', 
                         description="Is the moisture content RWCO_MC recorded for all records in the RWCO group",
                         requirement = "data required",
                         action = "Check that the moisture content RWCO_MC is recorded for all records in the RWCO group")
    def run_query(self,  tables, headings):
        RWCO = self.get_group(tables, "RWCO", True)
        if (RWCO is not None):  
            self.check_value(RWCO,"RWCO","RWCO_MC","HEADING == 'DATA'",0,100)   
