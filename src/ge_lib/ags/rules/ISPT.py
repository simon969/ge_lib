import pandas as pd
from datetime import timedelta
from .AGSQuery import ags_query


class ISPT001(ags_query):
    def __init__(self):
        super().__init__(id='ISPT001', 
                         description="Is the ISPT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the ISPT group is present and that it contains data")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_row_count(ISPT,"ISPT","HEADING == 'DATA'",1,10000)
class ISPT002(ags_query):
    def __init__(self, LOCA_TYPE_MUST):
        self.LOCA_TYPE_MUST = LOCA_TYPE_MUST
        super().__init__(id='ISPT002', 
                         description="Does each LOCA_TYPE {0} in the LOCA group have a minimum of one standard penetration test record in the ISPT group".format(self.LOCA_TYPE_MUST),
                         requirement = "mandatory",
                         action = "Check that the ISPT group contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        ISPT = self.get_group(tables, "ISPT", True)
        if (LOCA is not None and ISPT is not None):  
            lLOCA =  LOCA.query("LOCA_TYPE in ({})".format(self.LOCA_TYPE_MUST))  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(ISPT,"ISPT",qry, 1,10)
class ISPT003(ags_query):
    def __init__(self):
        super().__init__(id='ISPT003', 
                         description="Is the ISPT_TOP heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the depth to the top of the ISPT test has been recorded in the ISPT_TOP for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        ISPT = self.get_group(tables, "ISPT", True)
        if (LOCA is not None and ISPT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(ISPT,"ISPT","ISPT_TOP",qry,0,FDEP)

class ISPT004(ags_query):
    def __init__(self):
        super().__init__(id='ISPT004', 
                         description="Is the number of blows for the seating drive ISPT_SEAT recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the number of blows for the seating drive ISPT_SEAT is recorded for all records in the ISPT group")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        
        if (ISPT is not None):  
            self.check_value(ISPT,"ISPT","ISPT_SEAT","HEADING == 'DATA'",0,50)

class ISPT005(ags_query):
    def __init__(self):
        super().__init__(id='ISPT005', 
                         description="Is the number of blows for the main test drive ISPT_MAIN recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the number of blows for the main test drive ISPT_MAIN is recorded for all records in the ISPT group")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        
        if (ISPT is not None):  
            self.check_value(ISPT,"ISPT","ISPT_MAIN","HEADING == 'DATA'",0,50)

class ISPT006(ags_query):
    def __init__(self):
        super().__init__(id='ISPT006', 
                         description="Is the total penetration for the seating and test drive ISPT_NPEN recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the total penetration for the seating and test drive ISPT_NPEN is recorded for all records in the ISPT group")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        
        if (ISPT is not None):  
            self.check_value(ISPT,"ISPT","ISPT_NPEN","HEADING == 'DATA'",0,900)

class ISPT007(ags_query):
    def __init__(self, ISPT_NVAL_MIN, ISPT_NVAL_MAX):
        self.ISPT_NVAL_MIN = ISPT_NVAL_MIN
        self.ISPT_NVAL_MAX = ISPT_NVAL_MAX
        super().__init__(id='ISPT007', 
                         description="Is the SPT N value recorded in ISPT_NVAL in the range of {} and {} for all records in the ISPT group".format(self.ISPT_NVAL_MIN, self.ISPT_NVAL_MAX),
                         requirement = "mandatory",
                         action = "Check that the SPT N value is recorded for all records in the ISPT group")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        
        if (ISPT is not None):  
            self.check_value(ISPT,"ISPT", "ISPT_NVAL", "HEADING == 'DATA'", self.ISPT_NVAL_MIN, self.ISPT_NVAL_MAX)
class ISPT008(ags_query):
    def __init__(self):
        super().__init__(id='ISPT008', 
                         description="Is the SPT reported values ISPT_REP recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the reported SPT values ISPT_REP is recorded for all records in the ISPT group")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        
        if (ISPT is not None):  
            self.check_string_length(ISPT,"ISPT","ISPT_REP","HEADING == 'DATA'", 0, 255)

class ISPT009(ags_query):
    def __init__(self):
        super().__init__(id='ISPT009', 
                         description="Is the casing depth at the time of the SPT test completed for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the casing depth at the time of the SPT test SPT_CAS has been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        ISPT = self.get_group(tables, "ISPT", True)
        if (LOCA is not None and ISPT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(ISPT,"ISPT","ISPT_CAS",qry,0,FDEP)
class ISPT010(ags_query):
    def __init__(self, ISPT_WAT_TEXT_ALLOWED):
        self.ISPT_WAT_TEXT_ALLOWED =  ISPT_WAT_TEXT_ALLOWED
        super().__init__(id='ISPT010', 
                         description="Is the water depth ISPT_WAT at the time of the SPT test or allowed text {0} completed for all records in the ISPT group".format(self.ISPT_WAT_TEXT_ALLOWED),
                         requirement = "mandatory",
                         action = "Check that the water depth at the time of the SPT test SPT_WAT or {0} has been recorded in the ISPT group for all records".format(self.ISPT_WAT_TEXT_ALLOWED))
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        ISPT = self.get_group(tables, "ISPT", True)
        if (LOCA is not None and ISPT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value_or_string_allowed(ISPT,"ISPT","ISPT_CAS",qry,0,FDEP, self.ISPT_WAT_TEXT_ALLOWED)

class ISPT011(ags_query):
    def __init__(self, ISPT_TYPE_ALLOWED):
        self.ISPT_TYPE_ALLOWED =  ISPT_TYPE_ALLOWED
        super().__init__(id='ISPT011', 
                         description="Is the type of SPT test type ISPT_TYPE {0} completed for all records in the ISPT group".format(self.ISPT_TYPE_ALLOWED),
                         requirement = "mandatory",
                         action = "Check that the type of SPT test ISPT_TYPE {0} has been recorded in the ISPT group for all records".format(self.ISPT_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_allowed(ISPT,"ISPT","ISPT_TYPE","HEADING == 'DATA'",self.ISPT_TYPE_ALLOWED)

class ISPT012(ags_query):
    def __init__(self):
        super().__init__(id='ISPT012', 
                         description="Is the hammer manufacturers serial number ISPT_HAM completed for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the hammer manufacturers serial number ISPTN_HAM has been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_length(ISPT,"ISPT","ISPT_HAM","HEADING == 'DATA'",1,255)
class ISPT013(ags_query):
    def __init__(self):
        super().__init__(id='ISPT013', 
                         description="Is the energy ratio of the hammer ISPT_ERAT completed for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the energy ratio of the hammer ISPT_ERAT has been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_value(ISPT,"ISPT","ISPT_ERAT","HEADING == 'DATA'",0,100)   
class ISPT014(ags_query):
    def __init__(self):
        super().__init__(id='ISPT014', 
                         description="Is the self weight penetration of the hemmer ISPT_SWP completed for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the self weight penetration of the hammer ISPT_SWP has been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_value(ISPT,"ISPT","ISPT_SWP","HEADING == 'DATA'",0,150)
  
class ISPT015(ags_query):
    def __init__(self):
        super().__init__(id='ISPT015', 
                         description="Are the number of blows for each of the load increment ISPT_INC1...ISPT_INC6 been recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the number of blows for each of the load increment ISPT_INC1...ISPT_INC6 have been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_value(ISPT,"ISPT","ISPT_INC1","HEADING == 'DATA'", 0,50)     
            self.check_value(ISPT,"ISPT","ISPT_INC2","HEADING == 'DATA'", 0,50)  
            self.check_value(ISPT,"ISPT","ISPT_INC3","HEADING == 'DATA'", 0,50)  
            self.check_value(ISPT,"ISPT","ISPT_INC4","HEADING == 'DATA'", 0,50)  
            self.check_value(ISPT,"ISPT","ISPT_INC5","HEADING == 'DATA'", 0,50)  
            self.check_value(ISPT,"ISPT","ISPT_INC6","HEADING == 'DATA'", 0,50)

class ISPT016(ags_query):
    def __init__(self):
        super().__init__(id='ISPT016', 
                         description="Are the penetrations for each of the load increment ISPT_PEN1...ISPT_PEN6 been recorded for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that the penetrations for each load increment ISPT_PEN1...ISPT_PEN6 have been recorded in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_value(ISPT,"ISPT","ISPT_PEN1","HEADING == 'DATA'",0,75)     
            self.check_value(ISPT,"ISPT","ISPT_PEN2","HEADING == 'DATA'",0,75)  
            self.check_value(ISPT,"ISPT","ISPT_PEN3","HEADING == 'DATA'",0,75)  
            self.check_value(ISPT,"ISPT","ISPT_PEN4","HEADING == 'DATA'",0,75)  
            self.check_value(ISPT,"ISPT","ISPT_PEN5","HEADING == 'DATA'",0,75)  
            self.check_value(ISPT,"ISPT","ISPT_PEN6","HEADING == 'DATA'",0,75) 
class ISPT017(ags_query):
    def __init__(self, ISPT_ROCK_ALLOWED):
        self.ISPT_ROCK_ALLOWED = ISPT_ROCK_ALLOWED
        super().__init__(id='ISPT017', 
                         description="If the SPT test has been carried out in soft rock is this indicated in ISPT_ROCK heading for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check if the SPT test has been carried out in soft rock and that this has been recorded in ISPT_ROCK heading in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_allowed(ISPT,"ISPT","ISPT_ROCK","HEADING == 'DATA'",self.ISPT_ROCK_ALLOWED)

class ISPT018(ags_query):
    def __init__(self):
        super().__init__(id='ISPT018', 
                         description="Have test remarks ISPT_REM been included for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that test remarks ISPT_REM are included in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_length(ISPT,"ISPT","ISPT_REM","HEADING == 'DATA'",0,255)

class ISPT019(ags_query):
    def __init__(self):
        super().__init__(id='ISPT019', 
                         description="Have details of the weather and environment been included in ISPT_ENV for all records in the ISPT group",
                         requirement = "mandatory",
                         action = "Check that weather and environmental conditions have been included in ISPT_ENV heading in the ISPT group for all records")
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_length(ISPT,"ISPT","ISPT_ENV","HEADING == 'DATA'",0,255)
    
class ISPT020(ags_query):
    def __init__(self, ISPT_METH_ALLOWED):
        self.ISPT_METH_ALLOWED = ISPT_METH_ALLOWED
        super().__init__(id='ISPT020', 
                         description="Have details of the test method {0} been included in ISPT_METH for all records in the ISPT group".format(self.ISPT_METH_ALLOWED),
                         requirement = "mandatory",
                         action = "Check that the test method {0} have been included in ISPT_METH heading in the ISPT group for all records".format(self.ISPT_METH_ALLOWED))
    def run_query(self,  tables, headings):
        ISPT = self.get_group(tables, "ISPT", True)
        if (ISPT is not None):
            self.check_string_allowed(ISPT,"ISPT","ISPT_METH","HEADING == 'DATA'",self.ISPT_METH_ALLOWED)  