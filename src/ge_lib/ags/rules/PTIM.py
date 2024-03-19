import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class PTIM001(ags_query):
    def __init__(self):
        super().__init__(id='PTIM001', 
                         description="Is the PTIM group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the PTIM group is present and that it contains data")
    def run_query(self,  tables, headings):
        PTIM = self.get_group(tables, "PTIM", True)
        if (PTIM is not None):
            self.check_row_count(PTIM,"PTIM","HEADING == 'DATA'",1,10000)
class PTIM002(ags_query):
    def __init__(self):
        super().__init__(id='PTIM002', 
                         description="Does each location in the LOCA table have a minimum of one progress recod in the PTIM table",
                         requirement = "mandatory",
                         action = "Check that the PTIM table contains at least one record for every location in the LOCA table")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)
        if (LOCA is not None and PTIM is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_row_count(PTIM,"PTIM",qry, 1,100)
class PTIM003(ags_query):
    def __init__(self, PTIM_PTIM_MIN, PTIM_PTIM_MAX):
        self.PTIM_PTIM_MIN = PTIM_PTIM_MIN
        self.PTIM_PTIM_MAX = PTIM_PTIM_MAX
        super().__init__(id='PTIM003', 
                         description="Is the PTIM_PTIM completed for all records",
                         requirement = "mandatory",
                         action = "Check that the datetime field PTIM_PTIM has been recorded for all records")
    def run_query(self,  tables, headings):
        PTIM = self.get_group(tables, "PTIM", True)
        if (PTIM is not None):
            self.check_datetime(PTIM,"PTIM","PTIM_PTIM","HEADING=='DATA'",self.PTIM_PTIM_MIN, self.PTIM_PTIM_MAX)
class PTIM004(ags_query):
    def __init__(self):
        super().__init__(id='PTIM004', 
                         description="Are all the PTIM_PTIM recorded after the LOCA_STAR and before the LOCA_ENDD",
                         requirement = "mandatory",
                         action = "Check that the datetime field PTIM_PTIM is after the LOCA_STAR and before the LOCA_ENDD")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)

        if (LOCA is not None and PTIM is not None):  
            
            isLOCA_STAR = self.is_present(LOCA,"LOCA","LOCA_STAR")
            isLOCA_ENDD = self.is_present(LOCA,"LOCA","LOCA_ENDD")
            isPTIM_DTIM = self.is_present(LOCA,"PTIM","PTIM_DTIM")

            if (isLOCA_STAR and isLOCA_ENDD and isPTIM_DTIM):
                lLOCA =  LOCA.query("HEADING == 'DATA'")  
                for index, values in lLOCA.iterrows():
                    qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                    LOCA_STAR = pd.to_datetime(values['LOCA_STAR'])
                    LOCA_ENDD = pd.to_datetime(values['LOCA_ENDD'])
                    self.check_datetime(PTIM,"PTIM","PTIM_DTIM",qry,LOCA_STAR,LOCA_ENDD)
class PTIM005(ags_query):
    def __init__(self):
        super().__init__(id='PTIM005', 
                         description="Is the PTIM_DPTH completed for all records and is it always less than the LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the progress depth has been recorded in PTIM_DPTH for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)
       
        if (LOCA is not None and PTIM is not None):
            
            isLOCA_FDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isPTIM_DPTH = self.is_present(PTIM,"PTIM","PTIM_DPTH")

            if (isLOCA_FDEP and isPTIM_DPTH):
                lLOCA =  LOCA.query("HEADING == 'DATA'")  
                for index, values in lLOCA.iterrows():
                    qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                    LOCA_FDEP = pd.to_numeric(values['LOCA_FDEP'])
                    self.check_value (PTIM, "PTIM","PTIM_DPTH", qry, 0, LOCA_FDEP)
class PTIM006(ags_query):
    def __init__(self):
        super().__init__(id='PTIM006', 
                         description="Is the PTIM_CAS completed for all records and is it always less than the LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the progress casing depth has been recorded in PTIM_CAS for all records")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)

        if (LOCA is not None and PTIM is not None):
            isLOCA_FDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isPTIM_CAS = self.is_present(PTIM,"PTIM","PTIM_CAS")
            if (isLOCA_FDEP and isPTIM_CAS):
                lLOCA =  LOCA.query("HEADING == 'DATA'")  
                for index, values in lLOCA.iterrows():
                    qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                    LOCA_FDEP = pd.to_numeric(values['LOCA_FDEP'])
                    self.check_value (PTIM, "PTIM","PTIM_CAS", qry, 0, LOCA_FDEP)

class PTIM007(ags_query):
    def __init__(self, PTIM_WAT_TEXT_ALLOWED):
        self.PTIM_WAT_TEXT_ALLOWED=PTIM_WAT_TEXT_ALLOWED
        super().__init__(id='PTIM007', 
                         description="Is the PTIM_WAT completed for all records as 'Dry' or a value always less than the LOCA_FDEP",
                         requirement = "mandatory",
                         action = "Check that the progress water depth has been recorded in PTIM_WAT when water enounteerd and 'Dry' when not for all records")
    def run_query(self,  tables, headings):
        ptim_wat_text_allowed = ','.join(self.PTIM_WAT_TEXT_ALLOWED)
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)

        if (LOCA is not None and PTIM is not None):
            isLOCA_FDEP = self.is_present(LOCA,"LOCA","LOCA_FDEP")
            isPTIM_WAT = self.is_present(PTIM,"PTIM","PTIM_WAT")
            if (isLOCA_FDEP and isPTIM_WAT):
                lLOCA =  LOCA.query("HEADING == 'DATA'")  
                for index, values in lLOCA.iterrows():
                    qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                    LOCA_FDEP = pd.to_numeric(values['LOCA_FDEP'],errors='coerce')
                    for p_index, p_values in PTIM.query(qry).iterrows():
                        ptim_wat = p_values['PTIM_WAT']
                        ptim_wat_value = pd.to_numeric(p_values['PTIM_WAT'],errors='coerce')
                        if (ptim_wat_value == 'nan'):
                            if (ptim_wat in self.PTIM_WAT_TEXT_ALLOWED):
                                line = p_values['line_number']
                                desc = 'The text value in PTIM_WAT {0} is in the allowed text list {1}'.format(ptim_wat, ptim_wat_text_allowed)
                                res = {'line':line, 'group':'PTIM', 'desc':desc}
                                self.results_pass.append (res)
                            else:
                                line = p_values['line_number']
                                desc = 'The text value in PTIM_WAT {0} is not in the allowed text list {1}'.format(ptim_wat, ptim_wat_text_allowed)
                                res = {'line':line, 'group':'PTIM', 'desc':desc}
                                self.results_fail.append (res)
                        else:
                            if (ptim_wat_value <= LOCA_FDEP):
                                line = p_values['line_number']
                                desc = 'The value in PTIM_WAT {0} is less than or equal to the final hole depth in the LOCA table LOCA_FDEP {1}'.format(ptim_wat_value, LOCA_FDEP)
                                res = {'line':line, 'group':'PTIM', 'desc':desc}
                                self.results_pass.append (res)
                            else:
                                line = p_values['line_number']
                                desc = 'The value in LOCA_FDEP {0} is greater than the final hole depth in the LOCA table LOCA_FDEP {1}'.format(ptim_wat_value, LOCA_FDEP)
                                res = {'line':line, 'group':'PTIM', 'desc':desc}
                                self.results_fail.append (res)
            