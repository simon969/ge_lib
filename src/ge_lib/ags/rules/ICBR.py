import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class ICBR001(ags_query):
    def __init__(self):
        super().__init__(id='ICBR001', 
                         description="Is the ICBR group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the ICBR group is present and that it contains data")
    def run_query(self,  tables, headings):
        ICBR = self.get_group(tables, "ICBR", True)
        if (ICBR is not None):
            self.check_row_count(ICBR,"ICBR","HEADING == 'DATA'",1,10000)

class ICBR002(ags_query):
    def __init__(self):
        super().__init__(id='ICBR002', 
                         description="Is the insitu CBR test number ICBR_TESN recorded for all records in the ICBR group",
                         requirement = "mandatory",
                         action = "Check that the insitu CBR test number ICBR_TESN is recorded for all records in the ICBR group")
    def run_query(self,  tables, headings):
        ICBR = self.get_group(tables, "ICBR", True)
        
        if (ICBR is not None):  
            self.check_string_length(ICBR,"ICBR","ICBR_TESN","HEADING == 'DATA'",0,255)

class ICBR003(ags_query):
    def __init__(self):
        super().__init__(id='ICBR003', 
                         description="Is the depth to the top of the insitu CBR test ICBR_DPTH recorded for all records",
                         requirement = "mandatory",
                         action = "Check that the depth to the top of the insitu CBR test ICBR_DPTH is recorded for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        ICBR = self.get_group(tables, "ICBR", True)
        if (LOCA is not None and ICBR is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(ICBR,"ICBR","ICBR_DPTH",qry,0,FDEP)

class ICBR004(ags_query):
    def __init__(self):
        super().__init__(id='ICBR004', 
                         description="Is the insitu CBR test value ICBR_ICBR recorded for all records in the ICBR group",
                         requirement = "mandatory",
                         action = "Check that the insitu CBR test value ICBR_ICBR is recorded for all records in the ICBR group")
    def run_query(self,  tables, headings):
        ICBR = self.get_group(tables, "ICBR", True)
        
        if (ICBR is not None):  
            self.check_value(ICBR,"ICBR","ICBR_ICBR","HEADING == 'DATA'",0,100)
class ICBR005(ags_query):
    def __init__(self):
        super().__init__(id='ICBR005', 
                         description="Have remarks ICBR_REM been recorded for all records in the ICBR group",
                         requirement = "mandatory",
                         action = "Check that remarks ICBR_REM are recorded for all records in the ICBR group")
    def run_query(self,  tables, headings):
        ICBR = self.get_group(tables, "ICBR", True)
        
        if (ICBR is not None):  
            self.check_string_length(ICBR,"ICBR","ICBR_REM","HEADING == 'DATA'",1,255)
class ICBR006(ags_query):
    def __init__(self):
        super().__init__(id='ICBR006', 
                         description="Is the insitu CBR test method ICBR_METH recorded for all records in the ICBR group",
                         requirement = "mandatory",
                         action = "Check that the insitu CBR test method ICBR_METH is recorded for all records in the ICBR group")
    def run_query(self,  tables, headings):
        ICBR = self.get_group(tables, "ICBR", True)
        
        if (ICBR is not None):  
            self.check_string_length(ICBR,"ICBR","ICBR_METH","HEADING == 'DATA'",1,255)   
 