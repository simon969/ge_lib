import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class TRIG001(ags_query):
    def __init__(self):
        super().__init__(id='TRIG001', 
                         description="Is the TRIG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the TRIG group is present and that it contains data")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):
            self.check_row_count(TRIG,"TRIG","HEADING == 'DATA'",1,10000)
class TRIG002(ags_query):
    def __init__(self):
        super().__init__(id='TRIG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the TRIG group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the TRIG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        TRIG = self.get_group(tables, "TRIG", True)
        if (LOCA is not None and TRIG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(TRIG,"TRIG","SAMP_TOP",qry,0,FDEP)
                self.check_value(TRIG,"TRIG","SPEC_DPTH",qry,0,FDEP)
class TRIG003(ags_query):
    def __init__(self):
        super().__init__(id='TRIG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the TRIG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_length(TRIG,"TRIG","SAMP_REF","HEADING == 'DATA'",1,100)

class TRIG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='TRIGG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the TRIG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the TRIG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_allowed(TRIG,"TRIG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class TRIG005(ags_query):
    def __init__(self):
        super().__init__(id='TRIG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the TRIG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_length(TRIG,"TRIG","SAMP_ID","HEADING == 'DATA'",1,100)
class TRIG006(ags_query):
    def __init__(self):
        super().__init__(id='TRIG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the TRIG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_length(TRIG,"TRIG","SPEC_REF","HEADING == 'DATA'",1,100)
class TRIG007(ags_query):
    def __init__(self, TRIG_TYPE_ALLOWED):
        self.TRIG_TYPE_ALLOWED= TRIG_TYPE_ALLOWED
        super().__init__(id='TRIG007', 
                         description="Is the test type TRIG_TYPE recorded for all records in the TRIG group",
                         requirement = "key field",
                         action = "Check that the test type TRIG_TYPE is recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_allowed(TRIG,"TRIG","TRIG_TYPE","HEADING == 'DATA'",self.TRIG_TYPE_ALLOWED)

class TRIG008(ags_query):
    def __init__(self):
        super().__init__(id='TRIG008', 
                         description="Have remarks TRIG_REM been recorded for all records in the TRIG group",
                         requirement = "check data",
                         action = "Check that remarks TRIG_REM are recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_length(TRIG,"TRIG","TRIG_REM","HEADING == 'DATA'",1,255)
class TRIG009(ags_query):
    def __init__(self, TRIG_METH_ALLOWED):
        self.TRIG_METH_ALLOWED=TRIG_METH_ALLOWED
        super().__init__(id='TRIG009', 
                         description="Is the test method TRIG_METH {0} recorded for all records in the TRIG group".format(self.TRIG_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type TRIG_METH {0} is recorded for all records in the TRIG group".format(self.TRIG_METH_ALLOWED))
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_allowed(TRIG,"TRIG","TRIG_METH","HEADING == 'DATA'",self.TRIG_METH_ALLOWED)   
class TRIG010(ags_query):
    def __init__(self):
        super().__init__(id='TRIG010', 
                         description="Is the sample condition TRIG_COND recorded for all records in the TRIG group",
                         requirement = "data required",
                         action = "Check that the sample condition TRIG_COND is recorded for all records in the TRIG group")
    def run_query(self,  tables, headings):
        TRIG = self.get_group(tables, "TRIG", True)
        if (TRIG is not None):  
            self.check_string_length(TRIG,"TRIG","TRIG_COND","HEADING == 'DATA'",1,100)   
