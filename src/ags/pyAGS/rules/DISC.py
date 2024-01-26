import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class DISC001(ags_query):
    def __init__(self):
        super().__init__(id='DISC001', 
                         description="Is the DISC group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the DISC group is present and that it contains data")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        if (DISC is not None):
            self.check_row_count(DISC,"DISC","HEADING == 'DATA'",1,10000)
class DISC002(ags_query):
    def __init__(self):
        super().__init__(id='DISC002', 
                         description="Are the DISC_TOP and DISC_BASE headings completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and base of the discontinuity set have been recorded in the DISC_TOP and DISC_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        DISC = self.get_group(tables, "DISC", True)
        if (LOCA is not None and DISC is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(DISC,"DISC","DISC_TOP",qry,0,FDEP)
                self.check_value(DISC,"DISC","DISC_BASE",qry,0,FDEP)
class DISC003(ags_query):
    def __init__(self):
        super().__init__(id='DISC003', 
                         description="Is the fracture set reference FRAC_SET recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the frcature set reference FRAC_SET been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_string_length(DISC,"DISC","FRAC_SET","HEADING == 'DATA'",0,255)
class DISC004(ags_query):
    def __init__(self):
        super().__init__(id='DISC004', 
                         description="Is the dicontinuity reference DISC_NUMB recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the discontinuity reference DISC_NUMB been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_string_length(DISC,"DISC","DISC_NUMB","HEADING == 'DATA'",0,255)
class DISC005(ags_query):
    def __init__(self):
        super().__init__(id='DISC005', 
                         description="Is the dicontinuity type DISC_TYPE recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the discontinuity reference DISC_TYPE been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_string_length(DISC,"DISC","DISC_TYPE","HEADING == 'DATA'",0,255)            
class DISC006(ags_query):
    def __init__(self, DISC_DIP_MIN, DISC_DIP_MAX):
        self.DISC_DIP_MIN = DISC_DIP_MIN
        self.DISC_DIP_MAX = DISC_DIP_MAX
        super().__init__(id='DISC006', 
                         description="Is the discontinuity dip DISC_DIP recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the discontinuity dip DISC_DIP has been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_value(DISC,"DISC","DISC_DIP","HEADING == 'DATA'",self.DISC_DIP_MIN,self.DISC_DIP_MAX)

class DISC007(ags_query):
    def __init__(self, DISC_DIR_MIN, DISC_DIR_MAX):
        self.DISC_DIR_MIN = DISC_DIR_MIN
        self.DISC_DIR_MAX = DISC_DIR_MAX
        super().__init__(id='DISC004', 
                         description="Is the discontinuity dip direction DISC_DIR recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the discontinuity dip direction DISC_DIR has been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_value(DISC,"DISC","DISC_DIR","HEADING == 'DATA'",self.DISC_DIR_MIN,self.DISC_DIR_MAX)
class DISC008(ags_query):
    def __init__(self):
        super().__init__(id='DISC008', 
                         description="Is the dicontinuity remarks DISC_REM recorded for all records in the DISC group",
                         requirement = "mandatory",
                         action = "Check that the discontinuity remarks DISC_REM been recorded for all records in the DISC group")
    def run_query(self,  tables, headings):
        DISC = self.get_group(tables, "DISC", True)
        
        if (DISC is not None):  
            self.check_string_length(DISC,"DISC","DISC_REM","HEADING == 'DATA'",0,255)   