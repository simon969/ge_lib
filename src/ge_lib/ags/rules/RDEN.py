import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class RDEN001(ags_query):
    def __init__(self):
        super().__init__(id='RDEN001', 
                         description="Is the RDEN group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the RDEN group is present and that it contains data")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):
            self.check_row_count(RDEN,"RDEN","HEADING == 'DATA'",1,10000)
class RDEN002(ags_query):
    def __init__(self):
        super().__init__(id='RDEN002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the RDEN group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the RDEN group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        RDEN = self.get_group(tables, "RDEN", True)
        if (LOCA is not None and RDEN is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(RDEN,"RDEN","SAMP_TOP",qry,0,FDEP)
                self.check_value(RDEN,"RDEN","SPEC_DPTH",qry,0,FDEP)
class RDEN003(ags_query):
    def __init__(self):
        super().__init__(id='RDEN003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the RDEN group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_length(RDEN,"RDEN","SAMP_REF","HEADING == 'DATA'",1,100)

class RDEN004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='RDENG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the RDEN group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the RDEN group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_allowed(RDEN,"RDEN","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class RDEN005(ags_query):
    def __init__(self):
        super().__init__(id='RDEN005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the RDEN group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_length(RDEN,"RDEN","SAMP_ID","HEADING == 'DATA'",1,100)
class RDEN006(ags_query):
    def __init__(self):
        super().__init__(id='RDEN006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the RDEN group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_length(RDEN,"RDEN","SPEC_REF","HEADING == 'DATA'",1,100)
class RDEN007(ags_query):
    def __init__(self):
        super().__init__(id='RDEN007', 
                         description="Is the water content of the specimen RDEN_MC recorded for all records in the RDEN group",
                         requirement = "key field",
                         action = "Check that the water content of the specimen RDEN_MC is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_MC","HEADING == 'DATA'",0,30)

class RDEN008(ags_query):
    def __init__(self):
        super().__init__(id='RDEN008', 
                         description="Have remarks RDEN_REM been recorded for all records in the RDEN group",
                         requirement = "check data",
                         action = "Check that remarks RDEN_REM are recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_length(RDEN,"RDEN","RDEN_REM","HEADING == 'DATA'",1,255)
class RDEN009(ags_query):
    def __init__(self, RDEN_METH_ALLOWED):
        self.RDEN_METH_ALLOWED=RDEN_METH_ALLOWED
        super().__init__(id='RDEN009', 
                         description="Is the test method RDEN_METH {0} recorded for all records in the RDEN group".format(self.RDEN_METH_ALLOWED),
                         requirement = "data required",
                         action = "Check that the test type RDEN_METH {0} is recorded for all records in the RDEN group".format(self.RDEN_METH_ALLOWED))
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_string_allowed(RDEN,"RDEN","RDEN_METH","HEADING == 'DATA'",self.RDEN_METH_ALLOWED)   
class RDEN010(ags_query):
    def __init__(self):
        super().__init__(id='RDEN010', 
                         description="Is the saturated water content RDEN_SMC recorded for all records in the RDEN group",
                         requirement = "data required",
                         action = "Check that the saturated water content RDEN_SMC is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_SMC","HEADING == 'DATA'",0,100)   
class RDEN011(ags_query):
    def __init__(self):
        super().__init__(id='RDEN011', 
                         description="Is the bulk density RDEN_BDEN recorded for all records in the RDEN group",
                         requirement = "data required",
                         action = "Check that the bulk density RDEN_BDEN is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_BDEN","HEADING == 'DATA'",0.5,2.5)   
class RDEN012(ags_query):
    def __init__(self):
        super().__init__(id='RDEN012', 
                         description="Is the dry density RDEN_DDEN recorded for all records in the RDEN group",
                         requirement = "data required",
                         action = "Check that the dry density RDEN_DDEN is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_DDEN","HEADING == 'DATA'",0.5,2.5)   
class RDEN013(ags_query):
    def __init__(self):
        super().__init__(id='RDEN013', 
                         description="Is the porosityy RDEN_PORO recorded for all records in the RDEN group",
                         requirement = "data required",
                         action = "Check that the porosity RDEN_PORO is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_PORO","HEADING == 'DATA'",0.1,1)  
class RDEN014(ags_query):
    def __init__(self):
        super().__init__(id='RDEN014', 
                         description="Is the apparent particle density RDEN_PDEN recorded for all records in the RDEN group",
                         requirement = "data required",
                         action = "Check that the apparent particle density RDEN_PDEN is recorded for all records in the RDEN group")
    def run_query(self,  tables, headings):
        RDEN = self.get_group(tables, "RDEN", True)
        if (RDEN is not None):  
            self.check_value(RDEN,"RDEN","RDEN_PDEN","HEADING == 'DATA'",0.5,2.5)  