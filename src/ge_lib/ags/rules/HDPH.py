import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class HDPH001(ags_query):
    def __init__(self):
        super().__init__(id='HDPH001', 
                         description="Is the HDPH group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the HDPH group is present and that it contains data")
    def run_query(self,  tables, headings):
        HDPH = self.get_group(tables, "HDPH", True)
        if (HDPH is not None):
            self.check_row_count(HDPH,"HDPH","HEADING == 'DATA'",1,10000)
class HDPH002(ags_query):
    def __init__(self):
        super().__init__(id='HDPH002', 
                         description="Does each location in the LOCA table have a minimum of one record in the HDPH table",
                         requirement = "mandatory",
                         action = "Check that the HDPH table contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HDPH = self.get_group(tables, "HDPH", True)
        if (LOCA is not None and HDPH is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(HDPH,"HDPH",qry, 1,10)
class HDPH003(ags_query):
    def __init__(self):
        super().__init__(id='HDPH003', 
                         description="Is the HDPH_TOP and HDPH_BOT field completed for all records",
                         requirement = "mandatory",
                         action = "Check that the top and bottom of the depth information has been recorded in the HDPH_TOP and HDPH_BASE field for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        HDPH = self.get_group(tables, "HDPH", True)
        if (LOCA is not None and HDPH is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(HDPH,"HDPH","HDPH_TOP",qry,0,FDEP)
                self.check_value(HDPH,"HDPH","HDPH_BASE",qry,0,FDEP)
class HDPH004(ags_query):
    def __init__(self):
        super().__init__(id='HDPH004', 
                         description="Does the sum of the thicknesses (HDPH_BASE-HDPH_TOP) in the HDPH group match the final depth (LOCA_FDEP) in the LOCA group",
                         requirement = "mandatory",
                         action = "Check that the HDPH_BASE and HDPH_TOP are completed for the full depth of the location and match the value in the LOCA_FDEP heading")
    def run_query(self,  tables, headings):
        # https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
        # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
       
        LOCA = self.get_group(tables, "LOCA", True)
        HDPH = self.get_group(tables, "HDPH", True)
       
        if (LOCA is not None and HDPH is not None):
            
            isLOCA_FDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isHDPH_TOP = self.is_present(HDPH,"HDPH","HDPH_TOP")
            isHDPH_BASE = self.is_present(HDPH,"HDPH","HDPH_BASE")

            if (isLOCA_FDEP and isHDPH_TOP and isHDPH_BASE):

                lLOCA = LOCA.query("HEADING == 'DATA'")

                for l_index, l_values in lLOCA.iterrows():
                    hdph_sum = 0;
                    qry = "LOCA_ID == '{0}'".format(l_values['LOCA_ID'])
                    for h_index, h_values in HDPH.query(qry).iterrows():
                        hdph_thk =  pd.to_numeric(h_values['HDPH_BASE']) - pd.to_numeric(h_values['HDPH_TOP']) 
                        hdph_sum += hdph_thk
                    if (hdph_sum != pd.to_numeric(l_values['LOCA_FDEP'])):
                        line = l_values['line_number']
                        desc = 'The value in LOCA_FDEP {0} does not equal to sum of the thicknesses of the records in HDPH group sum(HDPH_TOP-HDPH_BASE) {1}'.format(l_values['LOCA_FDEP'], hdph_sum)
                        res = {'line':line, 'group':'LOCA', 'desc':desc}
                        self.results_fail.append (res)
                    else:
                        line = l_values['line_number']
                        desc = 'The value in LOCA_FDEP {0} does equals the sum of the thicknesses of the records in HDPH group sum(HDPH_TOP-HDPH_BASE) {1}'.format(l_values['LOCA_FDEP'], hdph_sum)
                        res = {'line':line, 'group':'LOCA', 'desc':desc}
                        self.results_pass.append (res)

class HDPH005(ags_query):
    def __init__(self):
        super().__init__(id='HDPH005', 
                         description="Is the HDPH_TYPE field in the HDPH table completed",
                         requirement = "check_data",
                         action = "Check that the type of depth information (HDPH_TYPE) is recorded in the HDPH table for all records")
    def run_query(self,  tables, headings):
        
        HDPH = self.get_group(tables, "HDPH", True)
        
        if (HDPH is not None):
            self.check_string_length(HDPH,"HDPH","HDPH_TYPE","HEADING == 'DATA'",1,64)  


class HDPH006(ags_query):
    def __init__(self, HDPH_STAR_MIN, HDPH_STAR_MAX):
        self.HDPH_STAR_MIN=HDPH_STAR_MIN
        self.HDPH_STAR_MAX=HDPH_STAR_MAX
        super().__init__(id='HDPH006', 
                         description="Is the HDPH_STAR field in the HDPH table completed and is it with correct ranges",
                         requirement = "mandatory",
                         action = "Check that the start date of the drilling info (HDPH_STAR) of all records in the HDPH table are completed")
    def run_query(self,  tables, headings):
        
        HDPH = self.get_group(tables, "HDPH", True)
        
        if (HDPH is not None):
            self.check_datetime(HDPH,"HDPH","HDPH_STAR","HEADING == 'DATA'", self.HDPH_STAR_MIN, self.HDPH_STAR_MAX)     

class HDPH007(ags_query):
    def __init__(self, HDPH_ENDD_MIN, HDPH_ENDD_MAX):
        self.HDPH_ENDD_MIN=HDPH_ENDD_MIN
        self.HDPH_ENDD_MAX=HDPH_ENDD_MAX
        super().__init__(id='HDPH007', 
                         description="Is the HDPH_ENDD field in the HDPH table completed and is it with correct ranges",
                         requirement = "mandatory",
                         action = "Check that the end date of the drilling info (HDPH_ENDD) of all records in the HDPH table are completed")
    def run_query(self,  tables, headings):
        
        HDPH = self.get_group(tables, "HDPH", True)
        
        if (HDPH is not None):
            self.check_datetime(HDPH,"HDPH","HDPH_ENDD","HEADING == 'DATA'", self.HDPH_ENDD_MIN, self.HDPH_ENDD_MAX)     