import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class CHIS001(ags_query):
    def __init__(self):
        super().__init__(id='CHIS001', 
                         description="Is the CHIS group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the CHIS group is present and that it contains data")
    def run_query(self,  tables, headings):
        CHIS = self.get_group(tables, "CHIS", True)
        if (CHIS is not None):
            self.check_row_count(CHIS,"CHIS","HEADING == 'DATA'",1,10000)
class CHIS002(ags_query):
    def __init__(self):
        super().__init__(id='CHIS002', 
                         description="Is the CHIS_FROM and CHIS_TO heading completed for all records and within LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the chisling from and chisling to have been recorded in the CHIS_FROM and CHIS_TO headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        CHIS = self.get_group(tables, "CHIS", True)
        if (LOCA is not None and CHIS is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(CHIS,"CHIS","CHIS_FROM",qry,0,FDEP)
                self.check_value(CHIS,"CHIS","CHIS_TO",qry,0,FDEP)
class CHIS003(ags_query):
    def __init__(self, CHIS_TIME_MIN, CHIS_TIME_MAX):
        self.CHIS_TIME_MIN = CHIS_TIME_MIN
        self.CHIS_TIME_MAX = CHIS_TIME_MAX
        super().__init__(id='CHIS003', 
                         description="Is the chisling time CHIS_TIME recorded for all records in the CHIS group",
                         requirement = "mandatory",
                         action = "Check that chisling times have been recorded for all records in the CHIS group")
    def run_query(self,  tables, headings):
        CHIS= self.get_group(tables, "CHIS", True)
        
        if (CHIS is not None):  
            self.check_duration(CHIS,"CHIS","CHIS_TIME","HEADING == 'DATA'",self.CHIS_TIME_MIN, self.CHIS_TIME_MAX)

