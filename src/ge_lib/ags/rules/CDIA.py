import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class CDIA001(ags_query):
    def __init__(self):
        super().__init__(id='CDIA001', 
                         description="Is the CDIA group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the CDIA group is present and that it contains data")
    def run_query(self,  tables, headings):
        CDIA = self.get_group(tables, "CDIA", True)
        if (CDIA is not None):
            self.check_row_count(CDIA,"CDIA","HEADING == 'DATA'",1,10000)
class CDIA002(ags_query):
    def __init__(self):
        super().__init__(id='CDIA002', 
                         description="Does each location in the LOCA table have a minimum of one record in the CDIA table",
                         requirement = "mandatory",
                         action = "Check that the CDIA table contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CDIA = self.get_group(tables, "CDIA", True)
        if (LOCA is not None and CDIA is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(CDIA,"CDIA",qry, 1,10)
class CDIA003(ags_query):
    def __init__(self):
        super().__init__(id='CDIA003', 
                         description="Is the CDIA_DPTH completed for all records and are the all less than the LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the casing diamter depth has been recorded in the CDIA_DPTH for all records and they are less than the LOCA_FDEP")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CDIA = self.get_group(tables, "CDIA", True)
        if (LOCA is not None and CDIA is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CDIA,"CDIA","CDIA_DPTH",qry,0,FDEP)
class CDIA004(ags_query):
    def __init__(self, CDIA_DIAM_MIN, CDIA_DIAM_MAX):
        self.CDIA_DIAM_MIN = CDIA_DIAM_MIN
        self.CDIA_DIAM_MAX = CDIA_DIAM_MAX
        super().__init__(id='CDIA004', 
                         description="Is the casing diameter CDIA_DIAM completed for all records",
                         requirement = "mandatory",
                         action = "Check that the casing diamter CDIA in the CDIA table is completed for all records")
    def run_query(self,  tables, headings):
        CDIA = self.get_group(tables, "CDIA", True)
        if (CDIA is not None):
            self.check_value(CDIA,"CDIA","CDIA_DIAM","HEADING == 'DATA'", self.CDIA_DIAM_MIN,self.CDIA_DIAM_MAX)