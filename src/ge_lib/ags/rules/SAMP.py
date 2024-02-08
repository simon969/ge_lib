import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query, is_datetime, map_datetime


class SAMP001(ags_query):
    def __init__(self):
        super().__init__(id='SAMP001', 
                         description="Is the SAMP group present and does is contain data",
                         requirement = "mandatory",
                         action = "Check that the SAMP group is present and that it contains data")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "GEOL", True)
        if (SAMP is not None):
            self.check_row_count(SAMP,"SAMP","HEADING == 'DATA'",1,10000)

class SAMP002(ags_query):
    def __init__(self):
        super().__init__(id='SAMP002', 
                         description="Is the SAMP_TOP and SAMP_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the samples have been recorded in the SAMP_TOP and SAMP_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        SAMP = self.get_group(tables, "SAMP", True)
        if (LOCA is not None and SAMP is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(SAMP,"SAMP","SAMP_TOP",qry,0,FDEP)
                self.check_value(SAMP,"SAMP","SAMP_BASE",qry,0,FDEP)

class SAMP003(ags_query):
    def __init__(self):
        super().__init__(id='SAMP003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the SAMP group",
                         requirement = "mandatory",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        
        if (SAMP is not None):  
            self.check_string_length(SAMP,"SAMP","SAMP_REF","HEADING == 'DATA'",1,100)

class SAMP004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='SAMP004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the SAMP group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "mandatory",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the SAMP group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):  
            self.check_string_allowed(SAMP,"SAMP","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class SAMP005(ags_query):
    def __init__(self):
        super().__init__(id='SAMP005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the SAMP group",
                         requirement = "mandatory",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        
        if (SAMP is not None):  
            self.check_string_length(SAMP,"SAMP","SAMP_ID","HEADING == 'DATA'",1,100)

class SAMP006(ags_query):
    def __init__(self, SAMP_DTIM_MIN, SAMP_DTIM_MAX):
        self.SAMP_DTIM_MIN = SAMP_DTIM_MIN
        self.SAMP_DTIM_MAX = SAMP_DTIM_MAX
        super().__init__(id='SAMP006', 
                         description="Is the date and time the sample was taken (SAMP_DTIM) recorded for all records in the SAMP group",
                         requirement = "mandatory",
                         action = "Check that the date and time the sample was taken (SAMP_DTIM) is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        SAMP = self.get_group(tables, "SAMP", True)

        if (LOCA is not None and SAMP is not None):
            unitEndDate = self.get_unit_pydatetime (LOCA,"LOCA","LOCA_ENDD",True)
            unitStartDate = self.get_unit_pydatetime (LOCA,"LOCA","LOCA_STAR",True)
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                locaEndDate = pd.to_datetime(values['LOCA_ENDD'],format=unitEndDate)
                locaStartDate = pd.to_datetime(values['LOCA_STAR'],format=unitStartDate)
                if is_datetime(locaStartDate) and is_datetime(locaEndDate):
                    self.check_datetime(SAMP,"SAMP","SAMP_DTIM",qry,locaStartDate, locaEndDate)
                else:
                    self.check_datetime(SAMP,"SAMP","SAMP_DTIM",qry,self.SAMP_DTIM_MIN, self.SAMP_DTIM_MAX)

class SAMP007(ags_query):
    def __init__(self,SAMP_UBLO_TYPES, SAMP_UBLO_MIN, SAMP_UBLO_MAX):
        self.SAMP_UBLO_TYPES=SAMP_UBLO_TYPES
        self.SAMP_UBLO_MIN=SAMP_UBLO_MIN
        self.SAMP_UBLO_MAX=SAMP_UBLO_MAX
        super().__init__(id='SAMP007', 
                         description="Is the sample blow count recorded for all undististurbed records ({0}) in the SAMP group".format(self.SAMP_UBLO_TYPES),
                         requirement = "mandatory",
                         action = "Check that the sample blow count SAMP_UBLO is recorded for all undisturbed records ({0}) in the SAMP group".format(self.SAMP_UBLO_TYPES))
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):
            qry = "SAMP_TYPE in ({0})".format(self.SAMP_UBLO_TYPES)  
            self.check_value(SAMP,"SAMP","SAMP_UBLO",qry,self.SAMP_UBLO_MIN, self.SAMP_UBLO_MAX) 

class SAMP008(ags_query):
    def __init__(self, SAMP_CONT_ALLOWED):
        self.SAMP_CONT_ALLOWED = SAMP_CONT_ALLOWED
        super().__init__(id='SAMP008', 
                         description="Is the sample container SAMP_CONT ({0})recorded for all records in the SAMP group".format(self.SAMP_CONT_ALLOWED),
                         requirement = "mandatory",
                         action = "Check that the sample container SAMP_CONT ({0}) is recorded for all records in the SAMP group".format(self.SAMP_CONT_ALLOWED))
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):  
            self.check_string_allowed(SAMP,"SAMP","SAMP_CONT","HEADING == 'DATA'",self.SAMP_CONT_ALLOWED)

class SAMP009(ags_query):
    def __init__(self, SAMP_SDIA_MIN, SAMP_SDIA_MAX):
        self.SAMP_SDIA_MIN = SAMP_SDIA_MIN
        self.SAMP_SDIA_MAX = SAMP_SDIA_MAX
        super().__init__(id='SAMP009', 
                         description="Is the sample diameter recorded in the range between {0} and {1} for all records in the SAMP group".format(self.SAMP_SDIA_MIN, self.SAMP_SDIA_MAX),
                         requirement = "mandatory",
                         action = "Check that the core diameter is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        
        if (SAMP is not None):  
            self.check_value(SAMP,"SAMP", "SAMP_SDIA", "HEADING == 'DATA'", self.SAMP_SDIA_MIN, self.SAMP_SDIA_MAX)

class SAMP010(ags_query):
    def __init__(self):
        super().__init__(id='SAMP010', 
                         description="Is the percentage of sample recovered SAMP_RECV recorded for all records in the SAMP group",
                         requirement = "mandatory",
                         action = "Check that the percentage of sample recovered SAMP_RECV is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):  
            self.check_value(SAMP,"SAMP","SAMP_RECV","HEADING == 'DATA'",1,100)

class SAMP011(ags_query):
    def __init__(self):
        super().__init__(id='SAMP011', 
                         description="Is the description of the sample SAMP_DESC recorded for all records in the SAMP group",
                         requirement = "mandatory",
                         action = "Check that the description of the sample SAMP_DESC is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):  
            self.check_string_length(SAMP,"SAMP","SAMP_DESC","HEADING == 'DATA'",1,255)
class SAMP012(ags_query):
    def __init__(self, SAMP_DESD_MIN, SAMP_DESD_MAX):
        self.SAMP_DESD_MIN = SAMP_DESD_MIN
        self.SAMP_DESD_MAX = SAMP_DESD_MAX
        super().__init__(id='SAMP012', 
                         description="Is the date the sample was described SAMP_DESD in the range {0} to {1} for all records in the SAMP group".format(self.SAMP_DESD_MIN, self.SAMP_DESD_MAX),
                         requirement = "mandatory",
                         action = "Check that the date the sample was described SAMP_DESD is recorded for all records in the SAMP group")
    def run_query(self,  tables, headings):
        SAMP = self.get_group(tables, "SAMP", True)
        if (SAMP is not None):  
            self.check_datetime(SAMP,"SAMP","SAMP_DESC","HEADING == 'DATA'", self.SAMP_DESD_MIN, self.SAMP_DESD_MAX)