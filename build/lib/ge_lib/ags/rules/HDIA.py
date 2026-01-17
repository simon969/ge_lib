import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class HDIA001(ags_query):
    def __init__(self):
        super().__init__(id='HDIA001', 
                         description="Is the HDIA group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the HDIA group is present and that it contains data")
    def run_query(self,  tables, headings):
        HDIA = self.get_group(tables, "HDIA", True)
        if (HDIA is not None):
            self.check_row_count(HDIA,"HDIA","HEADING == 'DATA'",1,10000)
class HDIA002(ags_query):
    def __init__(self):
        super().__init__(id='HDIA002', 
                         description="Does each location in the LOCA table have a minimum of one record in the HDIA table",
                         requirement = "mandatory",
                         action = "Check that the HDIA table contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HDIA = self.get_group(tables, "HDIA", True)
        if (LOCA is not None and HDIA is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(HDIA,"HOIA",qry, 1,10)
class HDIA003(ags_query):
    def __init__(self):
        super().__init__(id='HDIA003', 
                         description="Is the HDIA_DPTH completed for all records and are the all less than the LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the hole diamter depth has been recorded in the HDIA_DPTH for all records and they are less than the LOCA_FDEP")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HDIA = self.get_group(tables, "HDIA", True)
        if (LOCA is not None and HDIA is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(HDIA,"HDIA","HDIA_DPTH",qry,0,FDEP)
class HDIA004(ags_query):
    def __init__(self, HDIA_DIAM_MIN, HDIA_DIAM_MAX):
        self.HDIA_DIAM_MIN = HDIA_DIAM_MIN
        self.HDIA_DIAM_MAX = HDIA_DIAM_MAX
        super().__init__(id='HDIA004', 
                         description="Is the hole diameter HDIA_DIAM completed for all records",
                         requirement = "mandatory",
                         action = "Check that the hole diamter HDIA in HDIA table is completed for all records")
    def run_query(self,  tables, headings):
        HDIA = self.get_group(tables, "HDIA", True)
        if (HDIA is not None):
            self.check_value(HDIA,"HDIA","HDIA_DIAM","HEADING == 'DATA'",self.HDIA_DIAM_MIN,self.HDIA_DIAM_MAX)