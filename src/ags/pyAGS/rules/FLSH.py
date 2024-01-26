import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class FLSH001(ags_query):
    def __init__(self):
        super().__init__(id='FLSH001', 
                         description="Is the FLSH group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the FLSH group is present and that it contains data")
    def run_query(self,  tables, headings):
        FLSH = self.get_group(tables, "FLSH", True)
        if (FLSH is not None):
            self.check_row_count(FLSH,"FLSH","HEADING == 'DATA'",1,10000)
class FLSH002(ags_query):
    def __init__(self):
        super().__init__(id='FLSH002', 
                         description="Does each RC location in the LOCA table have a minimum of one record in the FLSH table",
                         requirement = "mandatory",
                         action = "Check that the FLSH table contains at least one record for every RC location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        FLSH = self.get_group(tables, "FLSH", True)
        if (LOCA is not None and FLSH is not None):  
            lLOCA =  LOCA.query("LOCA_TYPE == 'RC'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(FLSH,"FLSH",qry, 1,10)
class FLSH003(ags_query):
    def __init__(self):
        super().__init__(id='FLSH003', 
                         description="Is the FLSH_TOP and FLSH_BOT heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the depth information has been recorded in the FLSH_TOP and FLSH_BASE heading for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        FLSH = self.get_group(tables, "FLSH", True)
        if (LOCA is not None and FLSH is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(FLSH,"FLSH","FLSH_TOP",qry,0,FDEP)
                self.check_value(FLSH,"FLSH","FLSH_BASE",qry,0,FDEP)