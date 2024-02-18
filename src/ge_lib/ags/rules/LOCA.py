import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class LOCA001(ags_query):
    def __init__(self, LOCA_COUNT_MIN, LOCA_COUNT_MAX):
        self.LOCA_COUNT_MIN = LOCA_COUNT_MIN
        self.LOCA_COUNT_MAX = LOCA_COUNT_MAX 
        super().__init__(id='LOCA001', 
                         description="Is the LOCA group present and does it contain data",
                         requirement = "mandatory",
                         action = "Check that the LOCA group is present and that it contains data")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        if (LOCA is not None):
            self.check_row_count(LOCA,"LOCA", "HEADING == 'DATA'", self.LOCA_COUNT_MIN,self.LOCA_COUNT_MAX)
      
class LOCA002(ags_query):
    def __init__(self):
        super().__init__(id='LOCA002', 
                         description="Are all LOCA_IDs entered in LOCA group and unique",
                         requirement = "mandatory",
                         action = "Check that all the LOCA_ID's in the LOCA_ID field of the LOCA group are unique")
    def run_query(self,  tables, headings):
        # https://sparkbyexamples.com/pandas/pandas-get-list-of-all-duplicate-rows/#:~:text=Pandas%20DataFrame.,multiple%20columns%20or%20all%20columns.
        
        LOCA = self.get_group( tables, "LOCA", True)
       
        if (LOCA is not None): 
            self.check_unique(LOCA,"LOCA","HEADING == 'DATA'", "LOCA_ID")
            
class LOCA003(ags_query):
    def __init__(self):
        super().__init__(id='LOCA003', 
                         description="Is the LOCA_STAR datetime before the LOCA_ENDD field of the LOCA group",
                         requirement = "mandatory",
                         action = "Check that the LOCA_STAR and LOCA_END are completed and that the LOCA_STAR is earlier than the LOCA_ENDD")
    def run_query(self,  tables, headings):
        
        # https://stackoverflow.com/questions/71161553/how-to-compare-two-date-columns-in-a-dataframe-using-pandas
        
        LOCA = self.get_group(tables, "LOCA", True)


        if (LOCA is not None):

            IsLOCA_ENDD = self.is_present(LOCA, "LOCA", "LOCA_ENDD", True)
            IsLOCA_STAR = self.is_present(LOCA, "LOCA", "LOCA_STAR", True)

            if (IsLOCA_ENDD is not None and IsLOCA_STAR is not None):
                lLOCA = LOCA.query("HEADING == 'DATA'")
                for l_index, l_values in lLOCA.iterrows():
                    try:
                        diff = pd.to_datetime(l_values['LOCA_ENDD'], infer_datetime_format=True) - pd.to_datetime(l_values['LOCA_STAR'], infer_datetime_format=True)
                    except:
                        diff = timedelta(minutes=-1)
                    
                    if diff < timedelta(minutes=0):
                        line = l_values['line_number']
                        desc = 'The LOCA_STAR {0} is not before LOCA_ENDD {1}'.format(l_values['LOCA_STAR'], l_values['LOCA_ENDD'])
                        res =  {'line': line,'group':'LOCA','desc':desc}
                        self.results_fail.append (res)
                    else:
                        line = l_values['line_number']
                        desc = 'The LOCA_STAR {0} is not after LOCA_ENDD {1}'.format(l_values['LOCA_STAR'], l_values['LOCA_ENDD'])
                        res =  {'line': line,'group':'LOCA','desc':desc}
                        self.results_pass.append (res)

class LOCA004(ags_query):
    def __init__(self):
        super().__init__(id='LOCA004', 
                         description="Is the hole depth in the LOCA group equal to the sum of the thicknesses of the layers in the GEOL group",
                         requirement = "mandatory",
                         action = "Check that the LOCA_FDEP field in the LOCA table matches the sum of the thickness of records in the GEOL table")
    def run_query(self,  tables, headings):
        # https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values
        # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
       
       LOCA = self.get_group(tables, "LOCA", True)
       GEOL = self.get_group(tables, "GEOL", True)
       
       if (LOCA is not None and GEOL is not None):  
            lLOCA = LOCA.query("HEADING == 'DATA'")
            for l_index, l_values in lLOCA.iterrows():
                geol_sum = 0;
                qry = "LOCA_ID == '{0}'".format(l_values['LOCA_ID'])
                for g_index, g_values in GEOL.query(qry).iterrows():
                    geol_thk =  pd.to_numeric(g_values['GEOL_BASE']) - pd.to_numeric(g_values['GEOL_TOP']) 
                    geol_sum += geol_thk
                if (geol_sum != pd.to_numeric(l_values['LOCA_FDEP'])):
                    line = l_values['line_number']
                    desc = 'The value in LOCA_FDEP {0} does not equal to sum of the thicknesses of the records in GEOL table ({1})'.format(l_values['LOCA_FDEP'], geol_sum)
                    res = {'line':line, 'group':'LOCA', 'desc':desc}
                    self.results_fail.append (res)
                else:
                    line = l_values['line_number']
                    desc = 'The value in LOCA_HDEP {0} is equal the sum of the thicknesses of the records in GEOL table ({1})'.format(l_values['LOCA_FDEP'], geol_sum)
                    res = {'line':line, 'group':'LOCA', 'desc':desc}
                    self.results_pass.append (res)
class LOCA005(ags_query):
    def __init__(self):
        super().__init__(id='LOCA005', 
                         description="Is the LOCA_TYPE field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the location type (LOCA_TYPE) is recorded in the LOCA table")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_TYPE","HEADING == 'DATA'",1,255)  

class LOCA006(ags_query):
    def __init__(self):
        super().__init__(id='LOCA006', 
                         description="Is the LOCA_STAT field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the status of the location (LOCA_STAT) is recorded in the LOCA table")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_STAT","HEADING == 'DATA'",1,255)
  
class LOCA007(ags_query):
    def __init__(self, LOCA_NATE_MIN, LOCA_NATE_MAX):
        self.LOCA_NATE_MAX = LOCA_NATE_MAX
        self.LOCA_NATE_MIN = LOCA_NATE_MIN
        super().__init__(id='LOCA007', 
                         description="Is the LOCA_NATE field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the National Grid Easting coordinate (LOCA_NATE) is recorded in the LOCA table")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_NATE","HEADING == 'DATA'",self.LOCA_NATE_MIN,self.LOCA_NATE_MAX)  

class LOCA008(ags_query):
    def __init__(self, LOCA_NATN_MIN, LOCA_NATN_MAX):
        self.LOCA_NATN_MAX = LOCA_NATN_MAX
        self.LOCA_NATN_MIN = LOCA_NATN_MIN
        super().__init__(id='LOCA008', 
                         description="Is the LOCA_NATN field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the National Grid Northing coordinate (LOCA_NATN) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_NATN","HEADING == 'DATA'",self.LOCA_NATN_MIN,self.LOCA_NATN_MAX) 

class LOCA009(ags_query):
    def __init__(self):
        super().__init__(id='LOCA009', 
                         description="Is the LOCA_GREF field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the grid reference system (LOCA_GREF) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_GREF","HEADING == 'DATA'",1,64)  

class LOCA010(ags_query):
    def __init__(self, LOCA_GL_MIN, LOCA_GL_MAX):
        self.LOCA_GL_MIN = LOCA_GL_MIN
        self.LOCA_GL_MAX = LOCA_GL_MAX
        super().__init__(id='LOCA010', 
                         description="Is the LOCA_GL field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the ground level (LOCA_GL) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_GL","HEADING == 'DATA'", self.LOCA_GL_MIN,self.LOCA_GL_MAX) 

class LOCA011(ags_query):
    def __init__(self):
        super().__init__(id='LOCA011', 
                         description="Is the LOCA_FDEP field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the final depth (LOCA_FDEP) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_FDEP","HEADING == 'DATA'", 0,100) 
class LOCA012(ags_query):
    def __init__(self, LOCA_STAR_MIN, LOCA_STAR_MAX):
        self.LOCA_STAR_MIN=LOCA_STAR_MIN
        self.LOCA_STAR_MAX=LOCA_STAR_MAX
        super().__init__(id='LOCA012', 
                         description="Is the LOCA_STAR field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the start date (LOCA_STAR) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA",  True)
        
        if (LOCA is not None):
            self.check_datetime(LOCA,"LOCA","LOCA_STAR","HEADING == 'DATA'",self.LOCA_STAR_MIN, self.LOCA_STAR_MAX) 
class LOCA013(ags_query):
    def __init__(self, LOCA_ENDD_MIN, LOCA_ENDD_MAX):
        self.LOCA_ENDD_MIN=LOCA_ENDD_MIN
        self.LOCA_ENDD_MAX=LOCA_ENDD_MAX
        super().__init__(id='LOCA013', 
                         description="Is the LOCA_ENDD field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the end date (LOCA_ENDD) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_datetime(LOCA,"LOCA","LOCA_ENDD","HEADING == 'DATA'",self.LOCA_ENDD_MIN, self.LOCA_ENDD_MAX) 

class LOCA014(ags_query):
    def __init__(self):
        super().__init__(id='LOCA014', 
                         description="Is the LOCA_PURP field in the LOCA table completed",
                         requirement = "optional",
                         action = "Check that the purpose of the location (LOCA_PURP) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_PURP","HEADING == 'DATA'",1,255)  

class LOCA015(ags_query):
    def __init__(self):
        super().__init__(id='LOCA015', 
                         description="Is the LOCA_PURP field in the LOCA table completed",
                         requirement = "mandatory",
                         action = "Check that the reason for terminating the location (LOCA_TERM) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_TERM","HEADING == 'DATA'",1,255)  
class LOCA016(ags_query):
    def __init__(self,LOCA_LOCX_MIN,LOCA_LOCX_MAX):
        self.LOCA_LOCX_MIN=LOCA_LOCX_MIN
        self.LOCA_LOCX_MAX=LOCA_LOCX_MAX
        super().__init__(id='LOCA016', 
                         description="Is the LOCA_LOCX field in the LOCA table completed",
                         requirement = "check data",
                         action = "Check that the local coordinate x (LOCA_LOCX) is recorded in the LOCA table")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_LOCX","HEADING == 'DATA'",self.LOCA_LOCX_MIN,self.LOCA_LOCX_MAX)  

class LOCA017(ags_query):
    def __init__(self,LOCA_LOCY_MIN,LOCA_LOCY_MAX):
        self.LOCA_LOCY_MIN=LOCA_LOCY_MIN
        self.LOCA_LOCY_MAX=LOCA_LOCY_MAX
        super().__init__(id='LOCA017', 
                         description="Is the LOCA_LOCY field in the LOCA table completed",
                         requirement = "check data",
                         action = "Check that the local coordinate y (LOCA_LOCY) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA",True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_LOCY","HEADING == 'DATA'",self.LOCA_LOCY_MIN,self.LOCA_LOCY_MAX) 

class LOCA018(ags_query):
    def __init__(self):
        super().__init__(id='LOCA018', 
                         description="Is the LOCA_LREF field in the LOCA table completed",
                         requirement = "check data",
                         action = "Check that the local grid reference system (LOCA_LREF) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_LREF","HEADING == 'DATA'",1,64)  

class LOCA019(ags_query):
    def __init__(self,LOCA_LOCZ_MIN,LOCA_LOCZ_MAX):
        self.LOCA_LOCZ_MIN = LOCA_LOCZ_MIN
        self.LOCA_LOCZ_MAX = LOCA_LOCZ_MAX
        super().__init__(id='LOCA019', 
                         description="Is the LOCA_LOCZ field in the LOCA table completed",
                         requirement = "check data",
                         action = "Check that the local ground level (LOCA_LOCZ) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_LOCZ","HEADING == 'DATA'",self.LOCA_LOCZ_MIN,self.LOCA_LOCZ_MAX) 

class LOCA020(ags_query):
    def __init__(self):
        super().__init__(id='LOCA020', 
                         description="Is the LOCA_DATM field in the LOCA table completed",
                         requirement = "check data",
                         action = "Check that the local datum referencing system (LOCA_DATM) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_string_length(LOCA,"LOCA","LOCA_DATM","HEADING == 'DATA'",1,64)  

class LOCA021(ags_query):
    def __init__(self,LOCA_LAT_MIN,LOCA_LAT_MAX):
        self.LOCA_LAT_MIN = LOCA_LAT_MIN
        self.LOCA_LAT_MAX = LOCA_LAT_MAX
        super().__init__(id='LOCA021', 
                         description="Is the LOCA_LAT field in the LOCA table completed",
                         requirement = "optional",
                         action = "Check that the latituded (LOCA_LAT) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_LAT","HEADING == 'DATA'",self.LOCA_LAT_MIN,self.LOCA_LAT_MAX)

class LOCA022(ags_query):
    def __init__(self,LOCA_LON_MIN, LOCA_LON_MAX):
        self.LOCA_LON_MIN = LOCA_LON_MIN
        self.LOCA_LON_MAX = LOCA_LON_MAX
        super().__init__(id='LOCA022', 
                         description="Is the LOCA_LON field in the LOCA table completed",
                         requirement = "optional",
                         action = "Check that the longitude (LOCA_LON) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):
            self.check_value(LOCA,"LOCA","LOCA_LON", "HEADING == 'DATA'", self.LOCA_LON_MIN, self.LOCA_LON_MAX)            

class LOCA023(ags_query):
    def __init__(self,LOCA_CKDT_MIN, LOCA_CKDT_MAX):
        self.LOCA_CKDT_MIN = LOCA_CKDT_MIN, 
        self.LOCA_CKDT_MAX = LOCA_CKDT_MAX
        super().__init__(id='LOCA023', 
                         description="Is the LOCA_CKDT field in the LOCA table completed",
                         requirement = "optional",
                         action = "Check that the checked date (LOCA_CKDT) is recorded in the LOCA table for all locations")
    def run_query(self,  tables, headings):
        
        LOCA = self.get_group(tables, "LOCA", True)
       
        if (LOCA is not None): 
            self.check_datetime(LOCA,"LOCA","LOCA_CKDT","HEADING == 'DATA'", self.LOCA_CKDT_MIN, self.LOCA_CKDT_MAX) 