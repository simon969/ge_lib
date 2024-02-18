import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class CORE001(ags_query):
    def __init__(self):
        super().__init__(id='CORE001', 
                         description="Is the CORE group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CORE group is present and that it contains data")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        if (CORE is not None):
            self.check_row_count(CORE,"CORE","HEADING == 'DATA'",1,10000)
class CORE002(ags_query):
    def __init__(self, LOCA_TYPE_MUST):
        self.LOCA_TYPE_MUST = LOCA_TYPE_MUST
        super().__init__(id='CORE002', 
                         description="Does each LOCA_TYPE {0} in the LOCA group have a minimum of one coring record in the CORE group".format(self.LOCA_TYPE_MUST),
                         requirement = "mandatory",
                         action = "Check that the CORE group contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CORE = self.get_group(tables, "CORE", True)
        if (LOCA is not None and CORE is not None):  
            lLOCA =  LOCA.query("LOCA_TYPE in ({})".format(self.LOCA_TYPE_MUST))  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(CORE,"CORE",qry, 1,10)
class CORE003(ags_query):
    def __init__(self):
        super().__init__(id='CORE003', 
                         description="Is the CORE_TOP and CORE_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the core run have been recorded in the CORE_TOP and CORE_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CORE = self.get_group(tables, "CORE", True)
        if (LOCA is not None and CORE is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CORE,"CORE","CORE_TOP",qry,0,FDEP)
                self.check_value(CORE,"CORE","CORE_BASE",qry,0,FDEP)
class CORE004(ags_query):
    def __init__(self):
        super().__init__(id='CORE004', 
                         description="Is the percentage core recovery CORE_PREC recorded for all records in the CORE group",
                         requirement = "mandatory",
                         action = "Check that the percentage core recovery CORE_PREC is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        
        if (CORE is not None):  
            self.check_value(CORE,"CORE","CORE_PREC","HEADING == 'DATA'",0,100)

class CORE005(ags_query):
    def __init__(self):
        super().__init__(id='CORE005', 
                         description="Is the solid core recovery CORE_SREC recorded for all records in the CORE group",
                         requirement = "mandatory",
                         action = "Check that the percentage solid core recovery CORE_SREC is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        
        if (CORE is not None):  
            self.check_value(CORE,"CORE","CORE_SREC","HEADING == 'DATA'",0,100)

class CORE006(ags_query):
    def __init__(self):
        super().__init__(id='CORE006', 
                         description="Is the rock qaulity designation CORE_RQD recorded for all records in the CORE group",
                         requirement = "mandatory",
                         action = "Check that the rock quality designation CORE_RQD is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        
        if (CORE is not None):  
            self.check_value(CORE,"CORE","CORE_RQD","HEADING == 'DATA'",0,100)

class CORE007(ags_query):
    def __init__(self, CORE_DIAM_MIN, CORE_DIAM_MAX):
        self.CORE_DIAM_MIN = CORE_DIAM_MIN
        self.CORE_DIAM_MAX = CORE_DIAM_MAX
        super().__init__(id='CORE007', 
                         description="Is the core diameter recorded in the range between {0} and {1} for all records in the CORE group".format(self.CORE_DIAM_MIN, self.CORE_DIAM_MAX),
                         requirement = "mandatory",
                         action = "Check that the core diameter is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        
        if (CORE is not None):  
            self.check_value(CORE,"CORE", "CORE_DIAM", "HEADING == 'DATA'", self.CORE_DIAM_MIN, self.CORE_DIAM_MAX)
class CORE008(ags_query):
    def __init__(self, CORE_DURN_MIN, CORE_DURN_MAX):
        self.CORE_DURN_MIN = CORE_DURN_MIN
        self.CORE_DURN_MAX = CORE_DURN_MAX
        super().__init__(id='CORE008', 
                         description="Is the core duration CORE_DURN recorded in the range {0} and {1} for all records in the CORE group".format(self.CORE_DURN_MIN, self.CORE_DURN_MAX),
                         requirement = "mandatory",
                         action = "Check that the coring duration CORE_DURN is recorded for all records in the CORE group")
    def run_query(self,  tables, headings):
        CORE = self.get_group(tables, "CORE", True)
        
        if (CORE is not None):  
            self.check_duration(CORE,"CORE","CORE_DURN","HEADING == 'DATA'", self.CORE_DURN_MIN,self.CORE_DURN_MAX)