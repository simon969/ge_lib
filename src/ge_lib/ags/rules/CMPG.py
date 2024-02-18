import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class CMPG001(ags_query):
    def __init__(self):
        super().__init__(id='CMPG001', 
                         description="Is the CMPG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CMPG group is present and that it contains data")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):
            self.check_row_count(CMPG,"CMPG","HEADING == 'DATA'",1,10000)
class CMPG002(ags_query):
    def __init__(self):
        super().__init__(id='CMPG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CMPG = self.get_group(tables, "CMPG", True)
        if (LOCA is not None and CMPG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CMPG,"CMPG","SAMP_TOP",qry,0,FDEP)
                self.check_value(CMPG,"CMPG","SPEC_DPTH",qry,0,FDEP)
class CMPG003(ags_query):
    def __init__(self):
        super().__init__(id='CMPG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the CMPG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","SAMP_REF","HEADING == 'DATA'",1,100)

class CMPG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='CMPG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the CMPG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the CMPG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_allowed(CMPG,"CMPG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class CMPG005(ags_query):
    def __init__(self):
        super().__init__(id='CMPG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the CMPG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","SAMP_ID","HEADING == 'DATA'",1,100)
class CMPG006(ags_query):
    def __init__(self):
        super().__init__(id='CMPG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the CMPG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","SPEC_REF","HEADING == 'DATA'",1,100)
class CMPG007(ags_query):
    def __init__(self):
        super().__init__(id='CMPG007', 
                         description="Is the compaction test number CMPG_TESN recorded for all records in the CMPG group",
                         requirement = "key field",
                         action = "Check that the compaction test number CMPG_TESN is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","CMPG_TESN","HEADING == 'DATA'",1,255)

class CMPG008(ags_query):
    def __init__(self):
        super().__init__(id='CMPG008', 
                         description="Have remarks CMPG_REM been recorded for all records in the CMPG group",
                         requirement = "check data",
                         action = "Check that remarks CMPG_REM are recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","CMPG_REM","HEADING == 'DATA'",1,255)
class CMPG009(ags_query):
    def __init__(self):
        super().__init__(id='CMPG009', 
                         description="Is the compaction test method CMPG_METH recorded for all records in the CMPG group",
                         requirement = "data required",
                         action = "Check that the compaction test method CMPG_METH is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","CMPG_METH","HEADING == 'DATA'",1,255)   
class CMPG010(ags_query):
    def __init__(self, CMPG_TYPE_ALLOWED):
        self.CMPG_TYPE_ALLOWED = CMPG_TYPE_ALLOWED
        super().__init__(id='CMPG010', 
                         description="Is the compaction test type CMPG_TYPE {0} recorded for all records in the CMPG group".format(self.CMPG_TYPE_ALLOWED),
                         requirement = "data required",
                         action = "Check that the compaction test type CMPG_TYPE {0} is recorded for all records in the CMPG group".format(self.CMPG_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_allowed(CMPG,"CMPG","CMPG_TYPE","HEADING == 'DATA'",self.CMPG_TYPE_ALLOWED)   
class CMPG011(ags_query):
    def __init__(self, CMPG_MOLD_ALLOWED):
        self.CMPG_MOLD_ALLOWED= CMPG_MOLD_ALLOWED
        super().__init__(id='CMPG011', 
                         description="Is the compaction mould type CMPG_MOLD {0} recorded for all records in the CMPG group".format(self.CMPG_MOLD_ALLOWED),
                         requirement = "data required",
                         action = "Check that the compaction mould type CMPG_MOLD {0} is recorded for all records in the CMPG group".format(self.CMPG_MOLD_ALLOWED))
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_string_length(CMPG,"CMPG","CMPG_MOLD","HEADING == 'DATA'",1,255)   
class CMPG012(ags_query):
    def __init__(self):
        super().__init__(id='CMPG012', 
                         description="Is the maximum dry density CMPG_MAXD recorded for all records in the CMPG group",
                         requirement = "data required",
                         action = "Check that the maximum dry density CMPG_MAXD is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_value(CMPG,"CMPG","CMPG_MAXD","HEADING == 'DATA'",1000,2500)   
class CMPG013(ags_query):
    def __init__(self):
        super().__init__(id='CMPG013', 
                         description="Is the moisture content at maximum dry density CMPG_MCOP recorded for all records in the CMPG group",
                         requirement = "data required",
                         action = "Check that the moisture content at maximum dry density CMPG_MCOP is recorded for all records in the CMPG group")
    def run_query(self,  tables, headings):
        CMPG = self.get_group(tables, "CMPG", True)
        if (CMPG is not None):  
            self.check_value(CMPG,"CMPG","CMPG_MCOP","HEADING == 'DATA'",10,30)   
            