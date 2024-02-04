import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class IPRG001(ags_query):
    def __init__(self):
        super().__init__(id='IPRG001', 
                         description="Is the IPRG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the IPRG group is present and that it contains data")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        if (IPRG is not None):
            self.check_row_count(IPRG,"IPRG","HEADING == 'DATA'",1,10000)

class IPRG002(ags_query):
    def __init__(self):
        super().__init__(id='IPRG002', 
                         description="Is the permeability test number IPRG_TESN recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the permeability test number IPRG_TESN is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_string_length(IPRG,"IPRG","IPRG_TESN","HEADING == 'DATA'",0,255)

class IPRG003(ags_query):
    def __init__(self):
        super().__init__(id='IPRG003', 
                         description="Is the depth to the top and base of the test zone IPRG_TOP and IPRG_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the IPRG run have been recorded in the IPRG_TOP and IPRG_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        IPRG = self.get_group(tables, "IPRG", True)
        if (LOCA is not None and IPRG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(IPRG,"IPRG","IPRG_TOP",qry,0,FDEP)
                self.check_value(IPRG,"IPRG","IPRG_BASE",qry,0,FDEP)

class IPRG004(ags_query):
    def __init__(self):
        super().__init__(id='IPRG004', 
                         description="Is the packer test stage IPRG_STG recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the packer test stage IPRG_STG is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_STG","HEADING == 'DATA'",0,10)

class IPRG005(ags_query):
    def __init__(self, IPRG_TYPE_ALLOWED):
        self.IPRG_TYPE_ALLOWED = IPRG_TYPE_ALLOWED
        super().__init__(id='IPRG005', 
                         description="Is the permeability test type IPRG_TYPE recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the permeability test type IPRG_TYPE is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_string_allowed(IPRG,"IPRG","IPRG_SREC","HEADING == 'DATA'",self.IPRG_TYPE_ALLOWED)

class IPRG006(ags_query):
    def __init__(self):
        super().__init__(id='IPRG006', 
                         description="Is water depth immediately before test IPRG_PRWL recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the water depth immediately before test IPRG_PRWL is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_PRWL","HEADING == 'DATA'",0,100)
class IPRG007(ags_query):
    def __init__(self):
        super().__init__(id='IPRG007', 
                         description="Is water depth at the start of the test IPRG_SWAL recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the water depth at the start of the test IPRG_SWAL is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_SWAL","HEADING == 'DATA'",0,100)

class IPRG008(ags_query):
    def __init__(self, IPRG_TDIA_MIN, IPRG_TDIA_MAX):
        self.IPRG_TDIA_MIN = IPRG_TDIA_MIN
        self.IPRG_TDIA_MAX = IPRG_TDIA_MAX
        super().__init__(id='IPRG008', 
                         description="Is the diameter of the test zone IPRG_TDIA recorded in the range between {0} and {1} for all records in the IPRG group".format(self.IPRG_TDIA_MIN, self.IPRG_TDIA_MAX),
                         requirement = "mandatory",
                         action = "Check that the diameter of the test zone IPRG_TDIA is recorded in the range between {0} and {1} for all records in the IPRG group".format(self.IPRG_TDIA_MIN, self.IPRG_TDIA_MAX))
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG", "IPRG_TDIA", "HEADING == 'DATA'", self.IPRG_TDIA_MIN, self.IPRG_TDIA_MAX)
class IPRG009(ags_query):
    def __init__(self, IPRG_SDIA_MIN, IPRG_SDIA_MAX):
        self.IPRG_SDIA_MIN = IPRG_SDIA_MIN
        self.IPRG_SDIA_MAX = IPRG_SDIA_MAX
        super().__init__(id='IPRG009', 
                         description="Is the diameter of the standpipe zone IPRG_SDIA recorded in the range between {0} and {1} for all records in the IPRG group".format(self.IPRG_SDIA_MIN, self.IPRG_SDIA_MAX),
                         requirement = "mandatory",
                         action = "Check that the diameter of the standpipe IPRG_SDIA is recorded in the range between {0} and {1}  for all records in the IPRG group".format(self.IPRG_SDIA_MIN, self.IPRG_SDIA_MAX))
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG", "IPRG_SDIA", "HEADING == 'DATA'", self.IPRG_SDIA_MIN, self.IPRG_SDIA_MAX)
class IPRG010(ags_query):
    def __init__(self):
        super().__init__(id='IPRG010', 
                         description="Is permeability test value IPRG_IPRM recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the permeability test value IPRG_IPRM recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_IPRM","HEADING == 'DATA'",0,100)
class IPRG011(ags_query):
    def __init__(self):
        super().__init__(id='IPRG011', 
                         description="Is the average flow during the packer IPRG_FLOW recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the average flow during the packer IPRG_FLOW recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_FLOW","HEADING == 'DATA'",0,100)
class IPRG012(ags_query):
    def __init__(self):
        super().__init__(id='IPRG012', 
                         description="Is the depth to the assumed standing water level IPRG_AWL recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the depth to the assumed standing water level IPRG_AWL recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_AWL","HEADING == 'DATA'",0,100)
class IPRG013(ags_query):
    def __init__(self):
        super().__init__(id='IPRG013', 
                         description="Is the applied total head at the packer test zone IPRG_HEAD recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the applied total head at the packer test zone IPRG_HEAD recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_value(IPRG,"IPRG","IPRG_HEAD","HEADING == 'DATA'",0,100)            
class IPRG014(ags_query):
    def __init__(self, IPRG_DATE_MIN, IPRG_DATE_MAX):
        self.IPRG_DATE_MIN = IPRG_DATE_MIN
        self.IPRG_DATE_MAX = IPRG_DATE_MAX
        super().__init__(id='IPRG014', 
                         description="Is the permability test date IPRG_DATE recorded in the range {0} and {1} for all records in the IPRG group".format(self.IPRG_DATE_MIN, self.IPRG_DATE_MAX),
                         requirement = "mandatory",
                         action = "Check that the permability test date IPRG_DATE recorded in the range {0} and {1} for all records in the IPRG group".format(self.IPRG_DATE_MIN, self.IPRG_DATE_MAX))
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_datetime(IPRG,"IPRG","IPRG_DATE","HEADING == 'DATA'", self.IPRG_DATE_MIN,self.IPRG_DATE_MAX)

class IPRG015(ags_query):
    def __init__(self):
        super().__init__(id='IPRG015', 
                         description="Have remarks IPRG_REM been recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that remarks IPRG_REM have been recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_string_length(IPRG,"IPRG","IPRG_REM","HEADING == 'DATA'",1,255)  

class IPRG016(ags_query):
    def __init__(self):
        super().__init__(id='IPRG016', 
                         description="Have the weather and environment IPRG_ENV been recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that remarks IPRG_REM have been recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_string_length(IPRG,"IPRG","IPRG_REM","HEADING == 'DATA'",1,255)  

class IPRG017(ags_query):
    def __init__(self, IPRG_METH_ALLOWED):
        self.IPRG_METH_ALLOWED = IPRG_METH_ALLOWED
        super().__init__(id='IPRG017', 
                         description="Is the permeability test method IPRG_METH recorded for all records in the IPRG group",
                         requirement = "mandatory",
                         action = "Check that the permeability test method IPRG_METH is recorded for all records in the IPRG group")
    def run_query(self,  tables, headings):
        IPRG = self.get_group(tables, "IPRG", True)
        
        if (IPRG is not None):  
            self.check_string_allowed(IPRG,"IPRG","IPRG_SREC","HEADING == 'DATA'",self.IPRG_METH_ALLOWED)
