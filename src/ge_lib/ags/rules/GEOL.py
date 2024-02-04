import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class GEOL001(ags_query):
    def __init__(self):
        super().__init__(id='GEOL001', 
                         description="Is the GEOL group present and does is contain data",
                         requirement = "mandatory",
                         action = "Check that the GEOL group is present and that it contains data")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        if (GEOL is not None):
            self.check_row_count(GEOL,"GEOL","HEADING == 'DATA'",1,10000)
class GEOL002(ags_query):
    def __init__(self):
        super().__init__(id='GEOL002', 
                         description="Does each record in the LOCA group have a minimum of one record in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the GEOL group contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        GEOL = self.get_group(tables, "GEOL", True)
        if (LOCA is not None and GEOL is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(GEOL,"GEOL",qry, 1,10)
class GEOL003(ags_query):
    def __init__(self):
        super().__init__(id='GEOL003', 
                         description="Is the GEOL_TOP and GEOL_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the stratifications have been recorded in the GEOL_TOP and GEOL_BASE headings for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        GEOL = self.get_group(tables, "GEOL", True)
        if (LOCA is not None and GEOL is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(GEOL,"GEOL","GEOL_TOP",qry,0,FDEP)
                self.check_value(GEOL,"GEOL","GEOL_BASE",qry,0,FDEP)
class GEOL004(ags_query):
    def __init__(self):
        super().__init__(id='GEOL004', 
                         description="Does the sum of the thicknesses (GEOL_BASE-GEOL_TOP) in the GEOL group match the final depth (LOCA_FDEP) in the LOCA group",
                         requirement = "mandatory",
                         action = "Check that the sum of the thickness (GEOL_BASE-GEOL_TOP) match the value in the LOCA_FDEP heading of the LOCA group")
    def run_query(self,  tables, headings):
        # https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
        # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
       
        LOCA = self.get_group(tables, "LOCA", True)
        GEOL = self.get_group(tables, "GEOL", True)
       
        if (LOCA is not None and GEOL is not None):
            
            isFDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isTOP = self.is_present(GEOL,"GEOL","GEOL_TOP")
            isBASE = self.is_present(GEOL,"GEOL","GEOL_BASE")

            if (isFDEP and isTOP and isBASE):

                lLOCA = LOCA.query("HEADING == 'DATA'")

                for index, values in lLOCA.iterrows():
                    where = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                    LOCA_FDEP = pd.to_numeric(values['LOCA_FDEP'])
                    line_number = values['line_number']
                    self.check_sum_thickness (GEOL,"GEOL",where,"GEOL_TOP","GEOL_BASE",LOCA_FDEP,line_number)

class GEOL005(ags_query):
    def __init__(self):
        super().__init__(id='GEOL005', 
                         description="Is the geology description GEOL_DESC recorded for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the geology description GEOL_DESC is recorded for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_DESC","HEADING == 'DATA'",1,100)

class GEOL006(ags_query):
    def __init__(self):
        super().__init__(id='GEOL006', 
                         description="Is a legend code GEOL_LEG entered for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that legend code GEOL_LEG is entered for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_LEG","HEADING == 'DATA'",1,100)

class GEOL007(ags_query):
    def __init__(self):
        super().__init__(id='GEOL007', 
                         description="Is the geology code GEOL_GEOL entered for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the geology code GEOL_GEOL is entered for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_GEOL","HEADING == 'DATA'",1,100)

class GEOL008(ags_query):
    def __init__(self):
        super().__init__(id='GEOL008', 
                         description="Is the secondary geology code GEOL_GEO2 entered for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the secondary geology code GEOL_GEO2 is entered for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_GEO2","HEADING == 'DATA'",1,100)
class GEOL009(ags_query):
    def __init__(self):
        super().__init__(id='GEOL009', 
                         description="Is the BGS geology code GEOL_BGS entered for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the BGS geology code GEOL_BGS is entered for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_BGS","HEADING == 'DATA'",1,100)
class GEOL010(ags_query):
    def __init__(self):
        super().__init__(id='GEOL010', 
                         description="Is the formation geology code GEOL_FORM entered for all records in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the formation geology code GEOL_FORM is entered for all records in the GEOL group")
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_string_length(GEOL,"GEOL","GEOL_FORM","HEADING == 'DATA'",1,100)
class GEOL011(ags_query):
    def __init__(self, GEOL_LEG_MIN, GEOL_LEG_MAX):
        self.GEOL_LEG_MIN = GEOL_LEG_MIN
        self.GEOL_LEG_MAX = GEOL_LEG_MAX
        super().__init__(id='GEOL011', 
                         description="Is the geology legend code GEOL_LEG within the range of ({0}-{1}) for all records in the GEOL group".format(self.GEOL_LEG_MIN, self.GEOL_LEG_MAX),
                         requirement = "mandatory",
                         action = "Check that the geology legend code GEOL_LEG is within the range of ({0}-{1}) for all records in the GEOL group".format(self.GEOL_LEG_MIN, self.GEOL_LEG_MAX))
    def run_query(self,  tables, headings):
        GEOL = self.get_group(tables, "GEOL", True)
        
        if (GEOL is not None):  
            self.check_value(GEOL,"GEOL","GEOL_LEG","HEADING == 'DATA'",self.GEOL_LEG_MIN, self.GEOL_LEG_MAX)