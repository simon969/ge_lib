import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class GRAG001(ags_query):
    def __init__(self):
        super().__init__(id='GRAG001', 
                         description="Is the GRAG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the GRAG group is present and that it contains data")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):
            self.check_row_count(GRAG,"GRAG","HEADING == 'DATA'",1,10000)
class GRAG002(ags_query):
    def __init__(self):
        super().__init__(id='GRAG002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the GRAG group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the GRAG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        GRAG = self.get_group(tables, "GRAG", True)
        if (LOCA is not None and GRAG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(GRAG,"GRAG","SAMP_TOP",qry,0,FDEP)
                self.check_value(GRAG,"GRAG","SPEC_DPTH",qry,0,FDEP)
class GRAG003(ags_query):
    def __init__(self):
        super().__init__(id='GRAG003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the GRAG group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_length(GRAG,"GRAG","SAMP_REF","HEADING == 'DATA'",1,100)

class GRAG004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='GRAGG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the GRAG group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the GRAG group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_allowed(GRAG,"GRAG","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class GRAG005(ags_query):
    def __init__(self):
        super().__init__(id='GRAG005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the GRAG group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_length(GRAG,"GRAG","SAMP_ID","HEADING == 'DATA'",1,100)
class GRAG006(ags_query):
    def __init__(self):
        super().__init__(id='GRAG006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the GRAG group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_length(GRAG,"GRAG","SPEC_REF","HEADING == 'DATA'",1,100)
class GRAG007(ags_query):
    def __init__(self):
        super().__init__(id='GRAG007', 
                         description="Is the uniformity coefficient D60/D10 GRAG_UC recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that the uniformity coefficient D60/D10 GRAG_UC is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_UC","HEADING == 'DATA'",0,1)

class GRAG008(ags_query):
    def __init__(self):
        super().__init__(id='GRAG008', 
                         description="Have remarks GRAG_REM been recorded for all records in the GRAG group",
                         requirement = "check data",
                         action = "Check that remarks GRAG_REM are recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_length(GRAG,"GRAG","GRAG_REM","HEADING == 'DATA'",1,255)
class GRAG009(ags_query):
    def __init__(self):
        super().__init__(id='GRAG009', 
                         description="Is the test method GRAG_METH recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that the test method GRAG_METH is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_string_length(GRAG,"GRAG","GRAG_METH","HEADING == 'DATA'",1,100)   
class GRAG010(ags_query):
    def __init__(self):
        super().__init__(id='GRAG010', 
                         description="Is the percentage of cobbles GRAG_VCRE recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that the percentage of cobbles GRAG_VCRE is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_VCRE","HEADING == 'DATA'",0,100)   
class GRAG011(ags_query):
    def __init__(self):
        super().__init__(id='GRAG011', 
                         description="Is the percentage of gravel GRAG_GRAV recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that the percentage of gravel GRAG_GRAV is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_GRAV","HEADING == 'DATA'",0,100)   
class GRAG012(ags_query):
    def __init__(self):
        super().__init__(id='GRAG012', 
                         description="Is the percentage of sand GRAG_SAND recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that the percentage of sand GRAG_SAND is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_SAND","HEADING == 'DATA'",0,100)  
class GRAG013(ags_query):
    def __init__(self):
        super().__init__(id='GRAG013', 
                         description="Is the percentage of silt GRAG_SILT recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that percentage of silt GRAG_SILT is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_SILT","HEADING == 'DATA'",0,100)  
class GRAG014(ags_query):
    def __init__(self):
        super().__init__(id='GRAG014', 
                         description="Is the percentage of clay GRAG_CLAY recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that percentage of clay GRAG_CLAY is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_CLAY","HEADING == 'DATA'",0,100)  
class GRAG015(ags_query):
    def __init__(self):
        super().__init__(id='GRAG015', 
                         description="Is the percentage of fines GRAG_FINE recorded for all records in the GRAG group",
                         requirement = "data required",
                         action = "Check that percentage of fines GRAG_FINE is recorded for all records in the GRAG group")
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        if (GRAG is not None):  
            self.check_value(GRAG,"GRAG","GRAG_FINE","HEADING == 'DATA'",0,100)  