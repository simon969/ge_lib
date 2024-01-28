from ags.pyAGS.AGSQuery import ags_query

class PROJ001(ags_query):
    def __init__(self):
        super().__init__(id='PROJ001', 
                         description="Is PROJ table provided and does it contain a single row of data",
                         requirement = "mandatory",
                         action = "Check PROJ table is present and that it only contains a single row of data")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        if (PROJ is not None):
            self.check_row_count(PROJ,"PROJ","HEADING == 'DATA'",1,1)
        
class PROJ002(ags_query):
    def __init__(self):
        super().__init__(id='PROJ002', 
                         description="Is the PROJ_NAME field in the PROJ table completed",
                         requirement = "mandatory",
                         action = "Check that the name of the project (PROJ_NAME) is recorded in the PROJ table")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        
        if (PROJ is not None):
            self.check_string_length(PROJ,"PROJ","PROJ_NAME","HEADING == 'DATA'",1,255)

class PROJ003(ags_query):
    def __init__(self):
        super().__init__(id='PROJ003', 
                         description="Is the PROJ_LOC field in the PROJ table completed",
                         requirement = "mandatory",
                         action = "Check that the project location (PROJ_LOC) is recorded in the PROJ table")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        
        if (PROJ is not None):
            self.check_string_length(PROJ,"PROJ","PROJ_LOC","HEADING == 'DATA'",1,255)            

class PROJ004(ags_query):
    def __init__(self):
        super().__init__(id='PROJ004', 
                         description="Is the PROJ_CLNT field in the PROJ table completed",
                         requirement = "mandatory",
                         action = "Check that the project location (PROJ_CLNT is recorded in the PROJ table")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        
        if (PROJ is not None):
            self.check_string_length(PROJ,"PROJ","PROJ_CLNT","HEADING == 'DATA'",1,255)     

class PROJ005(ags_query):
    def __init__(self):
        super().__init__(id='PROJ005', 
                         description="Is the PROJ_CONT field in the PROJ table completed",
                         requirement = "mandatory",
                         action = "Check that the project contractor (PROJ_CONT) is recorded in the PROJ table")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        
        if (PROJ is not None):
            self.check_string_length(PROJ,"PROJ","PROJ_CONT","HEADING == 'DATA'",1,255)     

class PROJ006(ags_query):
    def __init__(self):
        super().__init__(id='PROJ006', 
                         description="Is the PROJ_ENG field in the PROJ table completed",
                         requirement = "mandatory",
                         action = "Check that the project engineer (PROJ_ENG) is recorded in the PROJ table")
    def run_query(self,  tables, headings):
        
        PROJ = self.get_group(tables, "PROJ", True)
        
        if (PROJ is not None):
            self.check_string_length(PROJ,"PROJ","PROJ_CONT","HEADING == 'DATA'",1,255)                      