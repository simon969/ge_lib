import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class PIPE001(ags_query):
    def __init__(self):
        super().__init__(id='PIPE001', 
                         description="Is the PIPE group present and does it contain data",
                         requirement = "optional",
                         action = "Check that the PIPE group is present and that it contains data")
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):
            self.check_row_count(PIPE,"PIPE","HEADING == 'DATA'",1,10000)
class PIPE002(ags_query):
    def __init__(self):
        super().__init__(id='PIPE002', 
                         description="Is the pipe ref PIPE_REF completed for all records in the PIPE group",
                         requirement = "key field",
                         action = "Check that the pipe ref PIPE_REF has been completed for all records in the PIPE group")
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):  
            self.check_string_length(PIPE,"PIPE","PIPE_REF","HEADING == 'DATA'", 1, 50)
class PIPE003(ags_query):
    def __init__(self):
        super().__init__(id='PIPE003', 
                         description="Is the PIPE_TOP and PIPE_BASE completed for all records and are the all less than the LOCA_FDEP",
                         requirement = "key field",
                         action = "Check that the top and base of the pipe has been recorded in the PIPE_TOP and PIPE_BASE headers for all records and they are less than the LOCA_FDEP")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PIPE = self.get_group(tables, "PIPE", True)
        if (LOCA is not None and PIPE is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(PIPE,"PIPE","PIPE_TOP",qry,0,FDEP)
                self.check_value(PIPE,"PIPE","PIPE_BASE",qry,0,FDEP)
class PIPE004(ags_query):
    def __init__(self, PIPE_DIAM_MIN, PIPE_DIAM_MAX):
        self.PIPE_DIAM_MIN = PIPE_DIAM_MIN
        self.PIPE_DIAM_MAX = PIPE_DIAM_MAX
        super().__init__(id='PIPE004', 
                         description="Is the casing diameter PIPE_DIAM completed for all records",
                         requirement = "data required",
                         action = "Check that the casing diamter PIPE in the PIPE table is completed for all records")
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):
            self.check_value(PIPE,"PIPE","PIPE_DIAM","HEADING == 'DATA'", self.PIPE_DIAM_MIN,self.PIPE_DIAM_MAX)
class PIPE005(ags_query):
    def __init__(self, PIPE_TYPE_ALLOWED):
        self.PIPE_TYPE_ALLOWED = PIPE_TYPE_ALLOWED
        super().__init__(id='PIPE005', 
                         description="Is the type of pipe PIPE_TYPE {0} completed for all records in PIPE group".format(self.PIPE_TYPE_ALLOWED),
                         requirement = "data required",
                         action = "Check that the type of pipe PIPE_TYPE {0} is completed for all records".format(self.PIPE_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):
            self.check_string_allowed(PIPE,"PIPE","PIPE_TYPE","HEADING == 'DATA'", self.PIPE_TYPE_ALLOWED)
class PIPE006(ags_query):
    def __init__(self):
        super().__init__(id='PIPE006', 
                         description="Are the details of the pipe construction PIPE_CONS completed for all records in the PIPE group",
                         requirement = "data required",
                         action = "Check that the details of the pipe construction PIPE_CONS have been completed for all records in the PIPE group")
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):  
            self.check_string_length(PIPE,"PIPE", "PIPE_CONS","HEADING == 'DATA'", 1,255)
class PIPE007(ags_query):
    def __init__(self):
        super().__init__(id='PIPE007', 
                         description="Have remarks PIPE_REM been recorded for all records in the PIPE group",
                         requirement = "check data",
                         action = "Check that remarks PIPE_REM are recorded for all records in the PIPE group")
    def run_query(self,  tables, headings):
        PIPE = self.get_group(tables, "PIPE", True)
        if (PIPE is not None):  
            self.check_string_length(PIPE,"PIPE","PIPE_REM","HEADING == 'DATA'",1,255)