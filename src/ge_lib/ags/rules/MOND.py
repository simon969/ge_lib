import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class MOND001(ags_query):
    def __init__(self):
        super().__init__(id='MOND001', 
                         description="Is the MOND group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the MOND group is present and that it contains data")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):
            self.check_row_count(MOND,"MOND","HEADING == 'DATA'",1,10000)
class MOND002(ags_query):
    def __init__(self):
        super().__init__(id='MOND002', 
                         description="Is the re-measured installation depth MONG_DIS headings completed for all records in the MOND group",
                         requirement = "key field",
                         action = "Check that the re-measured instalation depth MONG_DIS has been completed for all records in the MOND group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        MOND = self.get_group(tables, "MOND", True)
        if (LOCA is not None and MOND is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(MOND,"MOND","MONG_DIS",qry,0,FDEP)

class MOND003(ags_query):
    def __init__(self):
        super().__init__(id='MOND003', 
                         description="Is the monitoring reference MOND_REF recorded for all records in the MOND group",
                         requirement = "key field",
                         action = "Check that the monitoring reference MOND_REF is recorded for all records in the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_REF","HEADING == 'DATA'",1,100)

class MOND004(ags_query):
    def __init__(self, MOND_TYPE_ALLOWED):
        self.MOND_TYPE_ALLOWED= MOND_TYPE_ALLOWED
        super().__init__(id='MOND004', 
                         description="Is the correct monitoring type MOND_TYPE {0} recorded for all records in the MOND group".format(self.MOND_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct monitoing type MOND_TYPE {0} is recorded for all records in the MOND group".format(self.MOND_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_allowed(MOND,"MOND","MOND_TYPE","HEADING == 'DATA'",self.MOND_TYPE_ALLOWED)

class MOND005(ags_query):
    def __init__(self, MOND_DTIM_MIN, MOND_DTIM_MAX):
        self.MOND_DTIM_MIN = MOND_DTIM_MIN
        self.MOND_DTIM_MAX = MOND_DTIM_MAX
        super().__init__(id='MOND005', 
                         description="Is the monitoring date and time of reading MOND_DTIM between {0} and {1} for all records in the MOND group".format(self.MOND_DTIM_MIN,self.MOND_DTIM_MAX),
                         requirement = "data required",
                         action = "Check that the monitoring date and time of reading MOND_DTM is completed and in the range {0} and {1} for all records in the MOND group".format(self.MOND_DTIM_MIN,self.MOND_DTIM_MAX))
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_datetime(MOND,"MOND","MOND_DTIM","HEADING == 'DATA'",self.MOND_DTIM_MIN,self.MOND_DTIM_MAX)
class MOND006(ags_query):
    def __init__(self):
        super().__init__(id='MOND006', 
                         description="Is the instrument reference/serial number MOND_INST recorded for all records in the MOND group",
                         requirement = "data required",
                         action = "Check that the instrument reference/serial number MOND_INST is recorded for all records in the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_INST","HEADING == 'DATA'",1,255)
class MOND007(ags_query):
    def __init__(self, ):
        super().__init__(id='MOND007', 
                         description="Is the monitoring point reference MONG_ID recorded for all records in the MOND group",
                         requirement = "key field",
                         action = "Check that the monitoring point reference MONG_ID recorded for all records in the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MONG_ID","HEADING == 'DATA'",1,255)
class MOND008(ags_query):
    def __init__(self):
        super().__init__(id='MOND008', 
                         description="Have remarks MOND_REM been recorded for all records in the MOND group",
                         requirement = "check data",
                         action = "Check that remarks MOND_REM are recorded for all records in the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_REM","HEADING == 'DATA'",1,255)
class MOND009(ags_query):
    def __init__(self):
        super().__init__(id='MOND009', 
                         description="Is the instrument reading MOND_RDNG recorded for all records of the MOND group",
                         requirement = "data required",
                         action = "Check that the instrument reading MOND_RDNG is recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_RDNG","HEADING == 'DATA'",1,255)  
class MOND010(ags_query):
    def __init__(self):
        super().__init__(id='MOND010', 
                         description="Is the instrument reading units MOND_UNIT recorded for all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the instrument reading units MOND_UNIT is recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_UNIT","HEADING == 'DATA'",1,255)  
class MOND011(ags_query):
    def __init__(self):
        super().__init__(id='MOND011', 
                         description="Is the measurement method MOND_METH recorded for all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the measurement method MOND_METH is recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_METH","HEADING == 'DATA'",1,255)  
class MOND012(ags_query):
    def __init__(self):
        super().__init__(id='MOND012', 
                         description="Is the instrument/method reading/detection limit MOND_LIM recorded for all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the instrument/method reading/detection limit MOND_LIM is recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_LIM","HEADING == 'DATA'",1,255)  
class MOND013(ags_query):
    def __init__(self):
        super().__init__(id='MOND012', 
                         description="Is the instrument/method upper reading/detection limit MOND_ULIM recorded for all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the instrument/method upper reading/detection limit MOND_ULIM is recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_ULIM","HEADING == 'DATA'",1,255) 

class MOND014(ags_query):
    def __init__(self):
        super().__init__(id='MOND014', 
                         description="Is the client preferred name of measurement MOND_NAME recorded in all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the client preferred name of measurement MOND_NAME recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_NAME","HEADING == 'DATA'",1,255)
class MOND015(ags_query):
    def __init__(self):
        super().__init__(id='MOND015', 
                         description="Is the contractor who installed the instrument MOND_CONT recorded in all records of the MOND group",
                         requirement = "check data",
                         action = "Check that the contractor who installed the instrument MOND_CONT recorded in all records of the MOND group")
    def run_query(self,  tables, headings):
        MOND = self.get_group(tables, "MOND", True)
        if (MOND is not None):  
            self.check_string_length(MOND,"MOND","MOND_CONT","HEADING == 'DATA'",1,255)
