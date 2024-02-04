import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class SHBG001(ags_query):
    def __init__(self):
        super().__init__(id='SHBG001', 
                         description="Is the SHBG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the SHBG group is present and that it contains data")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):
            self.check_row_count(SHBG,"SHBG","HEADING == 'DATA'",1,10000)
class SHBG002(ags_query):
    def __init__(self):
        super().__init__(id='SHBG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the SHBG group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the SHBG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        SHBG = self.get_group(tables, "SHBG", True)
        if (LOCA is not None and SHBG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(SHBG,"SHBG","SAMP_TOP",qry,0,FDEP)
                self.check_value(SHBG,"SHBG","SPEC_DPTH",qry,0,FDEP)
class SHBG003(ags_query):
    def __init__(self):
        super().__init__(id='SHBG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the SHBG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SAMP_REF","HEADING == 'DATA'",1,100)

class SHBG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='SHBGG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the SHBG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the SHBG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_allowed(SHBG,"SHBG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class SHBG005(ags_query):
    def __init__(self):
        super().__init__(id='SHBG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the SHBG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SAMP_ID","HEADING == 'DATA'",1,100)
class SHBG006(ags_query):
    def __init__(self):
        super().__init__(id='SHBG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the SHBG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SPEC_REF","HEADING == 'DATA'",1,100)
class SHBG007(ags_query):
    def __init__(self, SHBG_TYPE_ALLOWED):
        self.SHBG_TYPE_ALLOWED= SHBG_TYPE_ALLOWED
        super().__init__(id='SHBG007', 
                         description="Is the test type SHBG_TYPE recorded for all records in the SHBG group",
                         requirement = "key field",
                         action = "Check that the test type SHBG_TYPE is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_allowed(SHBG,"SHBG","SHBG_TYPE","HEADING == 'DATA'",self.SHBG_TYPE_ALLOWED)

class SHBG008(ags_query):
    def __init__(self):
        super().__init__(id='SHBG008', 
                         description="Have remarks SHBG_REM been recorded for all records in the SHBG group",
                         requirement = "check data",
                         action = "Check that remarks SHBG_REM are recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SHBG_REM","HEADING == 'DATA'",1,255)
class SHBG009(ags_query):
    def __init__(self, SHBG_METH_ALLOWED):
        self.SHBG_METH_ALLOWED=SHBG_METH_ALLOWED
        super().__init__(id='SHBG009', 
                         description="Is the test method SHBG_METH {0} recorded for all records in the SHBG group".format(self.SHBG_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type SHBG_METH {0} is recorded for all records in the SHBG group".format(self.SHBG_METH_ALLOWED))
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_allowed(SHBG,"SHBG","SHBG_METH","HEADING == 'DATA'",self.SHBG_METH_ALLOWED)   
class SHBG010(ags_query):
    def __init__(self):
        super().__init__(id='SHBG010', 
                         description="Is the sample condition SHBG_COND recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that the sample condition SHBG_COND is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SHBG_COND","HEADING == 'DATA'",1,100)   
class SHBG011(ags_query):
    def __init__(self):
        super().__init__(id='SHBG011', 
                         description="Are specific specimen condition statments SHBG_CONS recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that specific specimen conditions SHBG_CONS is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_string_length(SHBG,"SHBG","SHBG_CONS","HEADING == 'DATA'",1,255)   
class SHBG012(ags_query):
    def __init__(self):
        super().__init__(id='SHBG012', 
                         description="Is the peak cohesion intercept SHBG_PCOH recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that the peak cohesion intercept SHBG_PCOH is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_value(SHBG,"SHBG","SHBG_PCOH","HEADING == 'DATA'",0,25)   
class SHBG013(ags_query):
    def __init__(self):
        super().__init__(id='SHBG013', 
                         description="Is the peak friction angle SHBG_PHI recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that the peak friction angle SHBG_PHI is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_value(SHBG,"SHBG","SHBG_PHI","HEADING == 'DATA'",0,45)  
class SHBG014(ags_query):
    def __init__(self):
        super().__init__(id='SHBG014', 
                         description="Is the residual cohesion intercept SHBG_RCOH recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that the resicual cohesion intercept SHBG_RCOH is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_value(SHBG,"SHBG","SHBG_RCOH","HEADING == 'DATA'",0.5,2.5) 
class SHBG015(ags_query):
    def __init__(self):
        super().__init__(id='SHBG015', 
                         description="Is the residual friction angle SHBG_RPHI recorded for all records in the SHBG group",
                         requirement = "data required",
                         action = "Check that the residual friction anngle SHBG_RPHI is recorded for all records in the SHBG group")
    def run_query(self,  tables, headings):
        SHBG = self.get_group(tables, "SHBG", True)
        if (SHBG is not None):  
            self.check_value(SHBG,"SHBG","SHBG_RPHI","HEADING == 'DATA'",0.5,2.5)  