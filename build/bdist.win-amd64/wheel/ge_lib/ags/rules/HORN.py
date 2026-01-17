import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class HORN001(ags_query):
    def __init__(self):
        super().__init__(id='HORN001', 
                         description="Is the HORN group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the HORN group is present and that it contains data")
    def run_query(self,  tables, headings):
        HORN = self.get_group(tables, "HORN", True)
        if (HORN is not None):
            self.check_row_count(HORN,"HORN","HEADING == 'DATA'",1,10000)
class HORN002(ags_query):
    def __init__(self):
        super().__init__(id='HORN002', 
                         description="Does each location in the LOCA table have a minimum of one record in the HORN table",
                         requirement = "mandatory",
                         action = "Check that the HORN table contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HORN = self.get_group(tables, "HORN", True)
        if (LOCA is not None and HORN is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(HORN,"HORN",qry, 1,10)
class HORN003(ags_query):
    def __init__(self):
        super().__init__(id='HORN003', 
                         description="Is the HORN_TOP and HORN_BASE heading completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the orientation has been recorded in the HORN_TOP and HORN_BASE heading for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HORN = self.get_group(tables, "HORN", True)
        if (LOCA is not None and HORN is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(HORN,"HORN","HORN_TOP",qry,0,FDEP)
                self.check_value(HORN,"HORN","HORN_BASE",qry,0,FDEP)
class HORN004(ags_query):
    def __init__(self):
        super().__init__(id='HORN004', 
                         description="Does the sum of the thicknesses (HORN_BASE-HORN_TOP) in the HORN group match the final depth (LOCA_FDEP) in the LOCA group",
                         requirement = "mandatory",
                         action = "Check that the HORN_BASE and HORN_TOP are completed for the full depth of the location and match the value in the LOCA_FDEP heading")
    def run_query(self,  tables, headings):
        # https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
        # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
       
       LOCA = self.get_group(tables, "LOCA", True)
       HORN = self.get_group(tables, "HORN", True)
       
       if (LOCA is not None and HORN is not None):  
            
            isLOCA_FDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isHORN_TOP = self.is_present(HORN,"HORN","HORN_TOP")
            isHORN_BASE = self.is_present(HORN,"HORN","HORN_BASE")

            if (isLOCA_FDEP and isHORN_TOP and isHORN_BASE): 

                lLOCA = LOCA.query("HEADING == 'DATA'")

                for l_index, l_values in lLOCA.iterrows():
                    horn_sum = 0;
                    qry = "LOCA_ID == '{0}'".format(l_values['LOCA_ID'])
                    for h_index, h_values in HORN.query(qry).iterrows():
                        horn_thk =  pd.to_numeric(h_values['HORN_BASE']) - pd.to_numeric(h_values['HORN_TOP']) 
                        horn_sum += horn_thk
                    if (horn_sum != pd.to_numeric(l_values['LOCA_FDEP'])):
                        line = l_values['line_number']
                        desc = 'The value in LOCA_FDEP {0} does not equal to sum of the thicknesses of the records in HORN group sum(HORN_BASE-HORN_TOP) {1}'.format(l_values['LOCA_FDEP'], horn_sum)
                        res = {'line':line, 'group':'LOCA', 'desc':desc}
                        self.results_fail.append (res)
                    else:
                        line = l_values['line_number']
                        desc = 'The value in LOCA_FDEP {0} does equals the sum of the thicknesses of the records in HORN group sum(HORN_BASE-HORN_TOP) {1}'.format(l_values['LOCA_FDEP'], horn_sum)
                        res = {'line':line, 'group':'LOCA', 'desc':desc}
                        self.results_pass.append (res)

class HORN005(ags_query):
    def __init__(self,HORN_ORNT_MIN,HORN_ORNT_MAX):
        self.HORN_ORNT_MIN=HORN_ORNT_MIN
        self.HORN_ORNT_MAX=HORN_ORNT_MAX
        super().__init__(id='HORN005', 
                         description="Is the HORN_ORNT field in the HORN table completed",
                         requirement = "mandatory",
                         action = "Check that the orientation (HORN_ORNT) of all records in the HORN table are completed")
    def run_query(self,  tables, headings):
        
        HORN = self.get_group(tables, "HORN", True)
        
        if (HORN is not None):
            self.check_value(HORN,"HORN","HORN_ORNT","HEADING == 'DATA'",self.HORN_ORNT_MIN,self.HORN_ORNT_MAX)

class HORN006(ags_query):
    def __init__(self, HORN_INCL_MIN, HORN_INCL_MAX):
        self.HORN_INCL_MIN=HORN_INCL_MIN
        self.HORN_INCL_MAX=HORN_INCL_MAX
        super().__init__(id='HORN006', 
                         description="Is the HORN_INCL field in the HORN table completed",
                         requirement = "mandatory",
                         action = "Check that the inclination (HORN_INCL) of all records in the HORN table are completed")
    def run_query(self,  tables, headings):
        
        HORN = self.get_group(tables, "HORN", True)
        
        if (HORN is not None):
            self.check_value(HORN,"HORN","HORN_INCL","HEADING == 'DATA'", self.HORN_INCL_MIN, self.HORN_INCL_MAX)     