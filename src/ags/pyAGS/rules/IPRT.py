import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class IPRT001(ags_query):
    def __init__(self):
        super().__init__(id='IPRT001', 
                         description="Is the IPRT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the IPRT group is present and that it contains data")
    def run_query(self,  tables, headings):
        IPRT = self.get_group(tables, "IPRT", True)
        if (IPRT is not None):
            self.check_row_count(IPRT,"IPRT","HEADING == 'DATA'",1,10000)

class IPRT002(ags_query):
    def __init__(self):
        super().__init__(id='IPRT002', 
                         description="Is the permeability test number IPRT_TESN recorded for all records in the IPRT group",
                         requirement = "mandatory",
                         action = "Check that the permeability test number IPRT_TESN is recorded for all records in the IPRT group")
    def run_query(self,  tables, headings):
        IPRT = self.get_group(tables, "IPRT", True)
        
        if (IPRT is not None):  
            self.check_string_length(IPRT,"IPRT","IPRT_TESN","HEADING == 'DATA'",0,255)

class IPRT003(ags_query):
    def __init__(self):
        super().__init__(id='IPRT003', 
                         description="Is the depth to the top and base of the test zone IPRT_TOP and IPRT_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the IPRT run have been recorded in the IPRT_TOP and IPRT_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        IPRT = self.get_group(tables, "IPRT", True)
        if (LOCA is not None and IPRT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(IPRT,"IPRT","IPRT_TOP",qry,0,FDEP)
                self.check_value(IPRT,"IPRT","IPRT_BASE",qry,0,FDEP)

class IPRT004(ags_query):
    def __init__(self):
        super().__init__(id='IPRT004', 
                         description="Is the packer test stage IPRT_STG recorded for all records in the IPRT group",
                         requirement = "mandatory",
                         action = "Check that the packer test stage IPRT_STG is recorded for all records in the IPRT group")
    def run_query(self,  tables, headings):
        IPRT = self.get_group(tables, "IPRT", True)
        
        if (IPRT is not None):  
            self.check_value(IPRT,"IPRT","IPRT_STG","HEADING == 'DATA'",0,10)

class IPRT005(ags_query):
    def __init__(self, IPRT_TIME_MIN, IPRT_TIME_MAX):
        self.IPRT_TIME_MIN = IPRT_TIME_MIN
        self.IPRT_TIME_MAX = IPRT_TIME_MAX
        super().__init__(id='IPRT005', 
                         description="Is the elapsed time IPRT_TIME recorded for all records in the IPRT group",
                         requirement = "mandatory",
                         action = "Check that the elapsed time IPRT_TIME is recorded for all records in the IPRT group")
    def run_query(self,  tables, headings):
        IPRT = self.get_group(tables, "IPRT", True)
        
        if (IPRT is not None):  
            self.check_duration(IPRT,"IPRT","IPRT_TIME","HEADING == 'DATA'",self.IPRT_TIME_MIN, self.IPRT_TIME_MAX)

class IPRT006(ags_query):
    def __init__(self):
        super().__init__(id='IPRT006', 
                         description="Is water depth IPRT_DPTH at elapsed time IPRT_TIME recorded for all records in the IPRT group",
                         requirement = "mandatory",
                         action = "Check that the water depth IPRT_DPTH at elapsed time IPRT_TIME recorded for all records in the IPRT group")
    def run_query(self,  tables, headings):
        IPRT = self.get_group(tables, "IPRT", True)
        LOCA = self.get_group(tables, "LOCA", True)
        if (LOCA is not None and IPRT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
            self.check_value(IPRT,"IPRT","IPRT_DPTH","HEADING == 'DATA'",0,FDEP)
