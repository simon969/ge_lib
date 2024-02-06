import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class SHBT001(ags_query):
    def __init__(self):
        super().__init__(id='SHBT001', 
                         description="Is the SHBT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the SHBT group is present and that it contains data")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):
            self.check_row_count(SHBT,"SHBT","HEADING == 'DATA'",1,10000)
class SHBT002(ags_query):
    def __init__(self):
        super().__init__(id='SHBT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the SHBT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the SHBT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        SHBT = self.get_group(tables, "SHBT", True)
        if (LOCA is not None and SHBT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(SHBT,"SHBT","SAMP_TOP",qry,0,FDEP)
                self.check_value(SHBT,"SHBT","SPEC_DPTH",qry,0,FDEP)
class SHBT003(ags_query):
    def __init__(self):
        super().__init__(id='SHBT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the SHBT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SAMP_REF","HEADING == 'DATA'",1,100)

class SHBT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='SHBTG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the SHBT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the SHBT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_allowed(SHBT,"SHBT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class SHBT005(ags_query):
    def __init__(self):
        super().__init__(id='SHBT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the SHBT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SAMP_ID","HEADING == 'DATA'",1,100)
class SHBT006(ags_query):
    def __init__(self):
        super().__init__(id='SHBT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the SHBT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SPEC_REF","HEADING == 'DATA'",1,100)
class SHBT007(ags_query):
    def __init__(self):
        super().__init__(id='SHBT007', 
                         description="Is the shear box stage/specimen reference SHBT_TESN recorded for all records in the SHBT group",
                         requirement = "key field",
                         action = "Check that the shear box stage/specimen reference SHBT_TESN is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SHBT_TESN","HEADING == 'DATA'",1,100)

class SHBT008(ags_query):
    def __init__(self):
        super().__init__(id='SHBT008', 
                         description="Have remarks SHBT_REM been recorded for all records in the SHBT group",
                         requirement = "data required",
                         action = "Check that remarks SHBT_REM are recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SHBT_REM","HEADING == 'DATA'",1,255)
class SHBT009(ags_query):
    def __init__(self):
        super().__init__(id='SHBT009', 
                         description="Is the inital bulk density SHBT_BDEN recorded for all records in the SHBT group",
                         requirement = "data required",
                         action = "Check that the initial bulk density SHBT_BDEN is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_BDEN","HEADING == 'DATA'",0.5, 2.5)   
class SHBT010(ags_query):
    def __init__(self):
        super().__init__(id='SHBT010', 
                         description="Is the inital dry density SHBT_DDEN recorded for all records in the SHBT group",
                         requirement = "data required",
                         action = "Check that the initial dry density SHBT_DDEN is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_DDEN","HEADING == 'DATA'",0.5,2.5)   
class SHBT011(ags_query):
    def __init__(self):
        super().__init__(id='SHBT011', 
                         description="Is the normal stress applied SHBT_NORM recorded for all records in the SHBT group",
                         requirement = "data required",
                         action = "Check that the normal stress applied SHBT_NORM is recorded for all records in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_NORM","HEADING == 'DATA'",10,900)   
class SHBT012(ags_query):
    def __init__(self):
        super().__init__(id='SHBT012', 
                         description="Is the displacement rate for peak stress stage SHBT_DISP recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the displacement rate for the peak stress stage SHBT_DISP is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_DISP","HEADING == 'DATA'",0,25)   
class SHBT013(ags_query):
    def __init__(self):
        super().__init__(id='SHBT013', 
                         description="Is the displacement rate of the residual stress stage SHBT_DISR recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the dispalcement rate of the residual stress SHBT_DISR is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_PHI","HEADING == 'DATA'",0,45)  
class SHBT014(ags_query):
    def __init__(self):
        super().__init__(id='SHBT014', 
                         description="Is the number of traverses SHBT_REVS recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the number of traverses SHBT_REVS is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_REVS","HEADING == 'DATA'",0,5) 
class SHBT015(ags_query):
    def __init__(self):
        super().__init__(id='SHBT015', 
                         description="Is the peak shear stress SHBT_PEAK recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the peak shear stress SHBT_PEAK is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_PEAK","HEADING == 'DATA'",10,600)  
class SHBT016(ags_query):
    def __init__(self):
        super().__init__(id='SHBT016', 
                         description="Is the residual shear stress SHBT_RES recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the peak shear stress SHBT_RES is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_RES","HEADING == 'DATA'",10,600)  
class SHBT017(ags_query):
    def __init__(self):
        super().__init__(id='SHBT017', 
                         description="Is the horizontal displacement at peak shear stress SHBT_PDIS recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the horizontal displacement at peak shear stress SHBT_PDIS is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_PDIS","HEADING == 'DATA'",1,30)  
class SHBT018(ags_query):
    def __init__(self):
        super().__init__(id='SHBT018', 
                         description="Is the horizontal displacement at residual shear stress SHBT_RDIS recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the horizontal displacement at residual shear stress SHBT_RDIS is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_RDIS","HEADING == 'DATA'",1,30)

class SHBT019(ags_query):
    def __init__(self):
        super().__init__(id='SHBT019', 
                         description="Is the vertical displacement at peak shear stress SHBT_PDIN recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the vertical displacement at peak shear stress SHBT_PDIN is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_PDIN","HEADING == 'DATA'",1,30)  

class SHBT020(ags_query):
    def __init__(self):
        super().__init__(id='SHBT020', 
                         description="Is the vertical displacement at residual shear stress SHBT_RDIN recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the vertical displacement at residual shear stress SHBT_RDIN is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_RDIN","HEADING == 'DATA'",1,30)

class SHBT021(ags_query):
    def __init__(self):
        super().__init__(id='SHBT021', 
                         description="Is the particle desnity SHBT_PDEN recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the particle density SHBT_PDEN is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_RDIN","HEADING == 'DATA'",0.5,2.6)
class SHBT022(ags_query):
    def __init__(self):
        super().__init__(id='SHBT022', 
                         description="Is the initial void ratio SHBT_IVR recorded in the SHBT group",
                         requirement = "check data",
                         action = "Check that the initial void ratio SHBT_IVR is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_IVR","HEADING == 'DATA'",0.1,0.3)
class SHBT023(ags_query):
    def __init__(self):
        super().__init__(id='SHBT023', 
                         description="Is the initial water/moisture content SHBT_MCI recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the initial water/moisture content SHBT_MCI is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_MCI","HEADING == 'DATA'",1,100)
class SHBT024(ags_query):
    def __init__(self):
        super().__init__(id='SHBT024', 
                         description="Is the final water/moisture content SHBT_MCF recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the final water/moisture content SHBT_MCF is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_MCF","HEADING == 'DATA'",1,100)
class SHBT025(ags_query):
    def __init__(self):
        super().__init__(id='SHBT025', 
                         description="Is the specimen diameter in the direction of shear SHBT_DIA1 recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the specimen diameter in the direction of shear SHBT_DIA1 is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_DIA1","HEADING == 'DATA'",50,100)
class SHBT026(ags_query):
    def __init__(self):
        super().__init__(id='SHBT026', 
                         description="Is the specimen diameter perpendicular to the direction of shear SHBT_DIA2 recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the specimen diameter perpendicular to the direction of shear SHBT_DIA2 is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_DIA2","HEADING == 'DATA'",50,100)
class SHBT027(ags_query):
    def __init__(self):
        super().__init__(id='SHBT027', 
                         description="Is the specimen height SHBT_HGT recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the specimen height SHBT_HGT is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_value(SHBT,"SHBT","SHBT_HGT","HEADING == 'DATA'",50,100)
class SHBT028(ags_query):
    def __init__(self):
        super().__init__(id='SHBT028', 
                         description="Is the failure/residual strength critera SHBT_CRIT recorded in the SHBT group",
                         requirement = "data required",
                         action = "Check that the failuer/residual strength criteria SHBT_CRIT is recorded in the SHBT group")
    def run_query(self,  tables, headings):
        SHBT = self.get_group(tables, "SHBT", True)
        if (SHBT is not None):  
            self.check_string_length(SHBT,"SHBT","SHBT_CRIT","HEADING == 'DATA'",1,100)                        