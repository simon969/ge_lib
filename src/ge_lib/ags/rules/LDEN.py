import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class LDEN001(ags_query):
    def __init__(self):
        super().__init__(id='LDEN001', 
                         description="Is the LDEN group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the LDEN group is present and that it contains data")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):
            self.check_row_count(LDEN,"LDEN","HEADING == 'DATA'",1,10000)
class LDEN002(ags_query):
    def __init__(self):
        super().__init__(id='LDEN002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the LDEN group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        LDEN = self.get_group(tables, "LDEN", True)
        if (LOCA is not None and LDEN is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(LDEN,"LDEN","SAMP_TOP",qry,0,FDEP)
                self.check_value(LDEN,"LDEN","SPEC_DPTH",qry,0,FDEP)
class LDEN003(ags_query):
    def __init__(self):
        super().__init__(id='LDEN003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the LDEN group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_length(LDEN,"LDEN","SAMP_REF","HEADING == 'DATA'",1,100)

class LDEN004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='LDENG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the LDEN group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the LDEN group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_allowed(LDEN,"LDEN","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class LDEN005(ags_query):
    def __init__(self):
        super().__init__(id='LDEN005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the LDEN group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_length(LDEN,"LDEN","SAMP_ID","HEADING == 'DATA'",1,100)
class LDEN006(ags_query):
    def __init__(self):
        super().__init__(id='LDEN006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the LDEN group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_length(LDEN,"LDEN","SPEC_REF","HEADING == 'DATA'",1,100)
class LDEN007(ags_query):
    def __init__(self):
        super().__init__(id='LDEN007', 
                         description="Is the sample condition LDEN_COND recorded for all records in the LDEN group",
                         requirement = "key field",
                         action = "Check that the sample condition LDEN_COND is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_length(LDEN,"LDEN","LDEN_COND","HEADING == 'DATA'",1,255)

class LDEN008(ags_query):
    def __init__(self):
        super().__init__(id='LDEN008', 
                         description="Have remarks LDEN_REM been recorded for all records in the LDEN group",
                         requirement = "check data",
                         action = "Check that remarks LDEN_REM are recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_length(LDEN,"LDEN","LDEN_REM","HEADING == 'DATA'",1,255)
class LDEN009(ags_query):
    def __init__(self, LDEN_METH_ALLOWED):
        self.LDEN_METH_ALLOWED=LDEN_METH_ALLOWED
        super().__init__(id='LDEN009', 
                         description="Is the test method LDEN_METH {0} recorded for all records in the LDEN group".format(self.LDEN_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type LDEN_METH {0} is recorded for all records in the LDEN group".format(self.LDEN_METH_ALLOWED))
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_string_allowed(LDEN,"LDEN","LDEN_METH","HEADING == 'DATA'",self.LDEN_METH_ALLOWED)   
class LDEN010(ags_query):
    def __init__(self):
        super().__init__(id='LDEN010', 
                         description="Is the moisture content LDEN_MC recorded for all records in the LDEN group",
                         requirement = "data required",
                         action = "Check that the moisture content LDEN_MC is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_value(LDEN,"LDEN","LDEN_MC","HEADING == 'DATA'",0,100)   
class LDEN011(ags_query):
    def __init__(self):
        super().__init__(id='LDEN011', 
                         description="Is the bulk density LDEN_BDEN recorded for all records in the LDEN group",
                         requirement = "data required",
                         action = "Check that the bulk density LDEN_BDEN is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_value(LDEN,"LDEN","LDEN_BDEN","HEADING == 'DATA'",0.5,2.5)   
class LDEN012(ags_query):
    def __init__(self):
        super().__init__(id='LDEN012', 
                         description="Is the dry density LDEN_DDEN recorded for all records in the LDEN group",
                         requirement = "data required",
                         action = "Check that the dry density LDEN_DDEN is recorded for all records in the LDEN group")
    def run_query(self,  tables, headings):
        LDEN = self.get_group(tables, "LDEN", True)
        if (LDEN is not None):  
            self.check_value(LDEN,"LDEN","LDEN_DDEN","HEADING == 'DATA'",0.5,2.5)   

