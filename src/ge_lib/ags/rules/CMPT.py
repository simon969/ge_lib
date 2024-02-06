import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class CMPT001(ags_query):
    def __init__(self):
        super().__init__(id='CMPT001', 
                         description="Is the CMPT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CMPT group is present and that it contains data")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):
            self.check_row_count(CMPT,"CMPT","HEADING == 'DATA'",1,10000)
class CMPT002(ags_query):
    def __init__(self):
        super().__init__(id='CMPT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the CMPT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the CMPT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CMPT = self.get_group(tables, "CMPT", True)
        if (LOCA is not None and CMPT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CMPT,"CMPT","SAMP_TOP",qry,0,FDEP)
                self.check_value(CMPT,"CMPT","SPEC_DPTH",qry,0,FDEP)
class CMPT003(ags_query):
    def __init__(self):
        super().__init__(id='CMPT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the CMPT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","SAMP_REF","HEADING == 'DATA'",1,100)

class CMPT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='CMPTG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the CMPT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the CMPT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_allowed(CMPT,"CMPT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class CMPT005(ags_query):
    def __init__(self):
        super().__init__(id='CMPT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the CMPT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","SAMP_ID","HEADING == 'DATA'",1,100)
class CMPT006(ags_query):
    def __init__(self):
        super().__init__(id='CMPT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the CMPT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","SPEC_REF","HEADING == 'DATA'",1,100)
class CMPT007(ags_query):
    def __init__(self):
        super().__init__(id='CMPT007', 
                         description="Is the compaction point number CMPT_TESN recorded for all records in the CMPT group",
                         requirement = "key field",
                         action = "Check that the compaction point number CMPT_TESN is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","CMPT_TESN","HEADING == 'DATA'",0,100)

class CMPT008(ags_query):
    def __init__(self):
        super().__init__(id='CMPT008', 
                         description="Have remarks CMPT_REM been recorded for all records in the CMPT group",
                         requirement = "check data",
                         action = "Check that remarks CMPT_REM are recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","CMPT_REM","HEADING == 'DATA'",1,255)
class CMPT009(ags_query):
    def __init__(self):
        super().__init__(id='CMPT009', 
                         description="Is the compaction test no CMPG_TESN recorded for all records in the CMPT group",
                         requirement = "data required",
                         action = "Check that the compaction test no CMPG_TESN is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_string_length(CMPT,"CMPT","CMPG_TESN","HEADING == 'DATA'",1,100)   
class CMPT010(ags_query):
    def __init__(self):
        super().__init__(id='CMPT010', 
                         description="Is the moisture content CMPT_MC recorded for all records in the CMPT group",
                         requirement = "data required",
                         action = "Check that the moisture content CMPT_MC is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_value(CMPT,"CMPT","CMPT_MC","HEADING == 'DATA'",10,30)   
class CMPT011(ags_query):
    def __init__(self):
        super().__init__(id='CMPT011', 
                         description="Is the dry density CMPT_DDEN recorded for all records in the CMPT group",
                         requirement = "data required",
                         action = "Check that the dry density CMPT_DDEN is recorded for all records in the CMPT group")
    def run_query(self,  tables, headings):
        CMPT = self.get_group(tables, "CMPT", True)
        if (CMPT is not None):  
            self.check_value(CMPT,"CMPT","CMPT_DDEN","HEADING == 'DATA'",1000,2500)   
