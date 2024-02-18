import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class WETH001(ags_query):
    def __init__(self):
        super().__init__(id='WETH001', 
                         description="Is the WETH group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the WETH group is present and that it contains data")
    def run_query(self,  tables, headings):
        WETH = self.get_group(tables, "WETH", True)
        if (WETH is not None):
            self.check_row_count(WETH,"WETH","HEADING == 'DATA'",1,10000)
class WETH002(ags_query):
    def __init__(self):
        super().__init__(id='WETH002', 
                         description="Is the WETH_TOP and WETH_BASE headings completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and base of the weathering zones have been recorded in the WETH_TOP and WETH_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        WETH = self.get_group(tables, "WETH", True)
        if (LOCA is not None and WETH is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(WETH,"FRAC","WETH_TOP",qry,0,FDEP)
                self.check_value(WETH,"FRAC","WETH_BASE",qry,0,FDEP)
class WETH003(ags_query):
    def __init__(self, WETH_SCH_ALLOWED):
        self.WETH_SCH_ALLOWED =  WETH_SCH_ALLOWED
        super().__init__(id='WETH003', 
                         description="Is the correct weathering scheme WETH_SCH {0} recorded for all records in the WETH group".format(','.join(self.WETH_SCH_ALLOWED)),
                         requirement = "mandatory",
                         action = "Check that the correct weathering scheme WETH_SCH has been recorded for all records in the WETH group")
    def run_query(self,  tables, headings):
        WETH = self.get_group(tables, "WETH", True)
        
        if (WETH is not None):  
            self.check_string_allowed(WETH,"WETH","WETH_SCH","HEADING == 'DATA'",self.WETH_SCH_ALLOWED)
class WETH004(ags_query):
    def __init__(self, WETH_SYS_ALLOWED):
        self.WETH_SYS_ALLOWED = WETH_SYS_ALLOWED
        super().__init__(id='WETH004', 
                         description="Is the correct weathering system WETH_SYS {0} recorded for all records in the WETH group".format(','.join(self.WETH_SYS_ALLOWED)),
                         requirement = "mandatory",
                         action = "Check that the weathering scheme WETH_SYS has been recorded for all records in the WETH group")
    def run_query(self,  tables, headings):
        WETH = self.get_group(tables, "WETH", True)
        
        if (WETH is not None):  
            self.check_string_allowed(WETH,"WETH","WETH_SYS","HEADING == 'DATA'",self.WETH_SYS_ALLOWED)
class WETH005(ags_query):
    def __init__(self):
        super().__init__(id='WETH005', 
                         description="Is the weathering classifier WETH_WETH recorded for all records in the WETH group",
                         requirement = "mandatory",
                         action = "Check that the weathering classifier WETH_WETH has been recorded for all records in the WETH group")
    def run_query(self,  tables, headings):
        WETH = self.get_group(tables, "WETH", True)
        
        if (WETH is not None):  
            self.check_string_length(WETH,"WETH","WETH_WETH","HEADING == 'DATA'",0,255)

