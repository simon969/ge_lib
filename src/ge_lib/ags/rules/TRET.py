import pandas as pd
from datetime import timedelta
from ..AGSQuery import ags_query


class TRET001(ags_query):
    def __init__(self):
        super().__init__(id='TRET001', 
                         description="Is the TRET group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the TRET group is present and that it contains data")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):
            self.check_row_count(TRET,"TRET","HEADING == 'DATA'",1,10000)
class TRET002(ags_query):
    def __init__(self):
        super().__init__(id='TRET002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the TRET group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the TRET group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        TRET = self.get_group(tables, "TRET", True)
        if (LOCA is not None and TRET is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(TRET,"TRET","SAMP_TOP",qry,0,FDEP)
                self.check_value(TRET,"TRET","SPEC_DPTH",qry,0,FDEP)
class TRET003(ags_query):
    def __init__(self):
        super().__init__(id='TRET003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the TRET group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","SAMP_REF","HEADING == 'DATA'",1,100)

class TRET004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='TRETG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the TRET group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the TRET group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_allowed(TRET,"TRET","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class TRET005(ags_query):
    def __init__(self):
        super().__init__(id='TRET005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the TRET group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","SAMP_ID","HEADING == 'DATA'",1,100)
class TRET006(ags_query):
    def __init__(self):
        super().__init__(id='TRET006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the TRET group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","SPEC_REF","HEADING == 'DATA'",1,100)
class TRET007(ags_query):
    def __init__(selfD):
        super().__init__(id='TRET007', 
                         description="Is the triaxial test/stage number TRET_TESN recorded for all records in the TRET group",
                         requirement = "key field",
                         action = "Check that the triaxial test/stage number TRET_TESN is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","TRET_TESN","HEADING == 'DATA'",1,100)

class TRET008(ags_query):
    def __init__(self):
        super().__init__(id='TRET008', 
                         description="Have remarks TRET_REM been recorded for all records in the TRET group",
                         requirement = "data required",
                         action = "Check that remarks TRET_REM are recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","TRET_REM","HEADING == 'DATA'",1,255)
class TRET009(ags_query):
    def __init__(self):
        super().__init__(id='TRET009', 
                         description="Is the inital bulk density TRET_BDEN recorded for all records in the TRET group",
                         requirement = "data required",
                         action = "Check that the initial bulk density TRET_BDEN is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_BDEN","HEADING == 'DATA'",0.5, 2.5)   
class TRET010(ags_query):
    def __init__(self):
        super().__init__(id='TRET010', 
                         description="Is the inital dry density TRET_DDEN recorded for all records in the TRET group",
                         requirement = "data required",
                         action = "Check that the initial dry density TRET_DDEN is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_DDEN","HEADING == 'DATA'",0.5,2.5)   
class TRET011(ags_query):
    def __init__(self):
        super().__init__(id='TRET011', 
                         description="Is the specimen diameter TRET_SDIA recorded for all records in the TRET group",
                         requirement = "data required",
                         action = "Check that the specimen diameter TRET_SDIA is recorded for all records in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_SDIA","HEADING == 'DATA'",40,110)   
class TRET012(ags_query):
    def __init__(self):
        super().__init__(id='TRET012', 
                         description="Is the specimen length TRET_LEN recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the specimen length TRET_LEN is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_LEN","HEADING == 'DATA'",100,450)   
class TRET013(ags_query):
    def __init__(self):
        super().__init__(id='TRET013', 
                         description="Is the method of saturation TRET_SAT recorded in the TRET group",
                         requirement = "check data",
                         action = "Check that the method of saturation TRET_SAT is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","TRET_SAT","HEADING == 'DATA'",1,255)  
class TRET014(ags_query):
    def __init__(self):
        super().__init__(id='TRET014', 
                         description="Are the details of the consolidation stage TRET_CONS recorded in the TRET group",
                         requirement = "check data",
                         action = "Check that the details of the consolidation stage TRET_CONS is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","TRET_REVS","HEADING == 'DATA'",1,255) 
class TRET015(ags_query):
    def __init__(self):
        super().__init__(id='TRET015', 
                         description="Is the effective stress at the end of the consolidation stage TRET_CONP recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the effective stress at the end of the consolidation stage TRET_CONP is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_CONP","HEADING == 'DATA'",10,600)  
class TRET016(ags_query):
    def __init__(self):
        super().__init__(id='TRET016', 
                         description="Is the total cell pressure during shearing stage TRET_CELL recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the total cell pressure during shearing stage TRET_CELL is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_CELL","HEADING == 'DATA'",10,600)  
class TRET017(ags_query):
    def __init__(self):
        super().__init__(id='TRET017', 
                         description="Is the porewater pressure at the start of the shearing stage TRET_PWPI recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the porewater pressure at the start of the shearing stage TRET_PWPI is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_PWPI","HEADING == 'DATA'",1,30)  
class TRET018(ags_query):
    def __init__(self):
        super().__init__(id='TRET018', 
                         description="Is the rate of axial strain TRET_STRR recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that therate of axial strain TRET_STRR is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            # AGS4 v 4.1 Dec 2020 suggests 1.5% /hour  
            self.check_value(TRET,"TRET","TRET_STRR","HEADING == 'DATA'",0.5,3)  

class TRET019(ags_query):
    def __init__(self):
        super().__init__(id='TRET019', 
                         description="Is the axial strain at failure TRET_STRN recorded in the TRET group",
                         requirement = "check data",
                         action = "Check that the axial strain at failure TRET_STRN is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
             # AGS4 v 4.1 Dec 2020 suggests 9% 
            self.check_value(TRET,"TRET","TRET_STRN","HEADING == 'DATA'",1,20)

class TRET020(ags_query):
    def __init__(self):
        super().__init__(id='TRET020', 
                         description="Is the deviator stress at failure TRET_DEVF recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the deviator stress at failure TRET_DEVF is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_DEVF","HEADING == 'DATA'",100,600)
class TRET021(ags_query):
    def __init__(self):
        super().__init__(id='TRET021', 
                         description="Is the porewater pressure at failure TRET_PWPF recorded in the TRET group",
                         requirement = "check data",
                         action = "Check that the porewater pressure at failure TRET_PWP is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_PWPF","HEADING == 'DATA'",40,200)
class TRET022(ags_query):
    def __init__(self):
        super().__init__(id='TRET022', 
                         description="Is the initial water/moisture content TRET_IMC recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the initial water/moisture content TRET_IMC is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_IMC","HEADING == 'DATA'",1,100)
class TRET023(ags_query):
    def __init__(self):
        super().__init__(id='TRET023', 
                         description="Is the final water/moisture content TRET_FMC recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the final water/moisture content TRET_FMC is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_value(TRET,"TRET","TRET_FMC","HEADING == 'DATA'",1,100)
class TRET024(ags_query):
    def __init__(self):
        super().__init__(id='TRET024', 
                         description="Is the voumetric strain at failure TRET_STV recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the volumetric strain at failure TRET_STV is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            # AGS4 v 4.1 Dec 2020 suggests 2.56%
            self.check_value(TRET,"TRET","TRET_STV","HEADING == 'DATA'",0.5,5)
class TRET025(ags_query):
    def __init__(self):
        super().__init__(id='TRET025', 
                         description="Is the mode of failure TRET_MODE recorded in the TRET group",
                         requirement = "data required",
                         action = "Check that the mode of failure TRET_MODE is recorded in the TRET group")
    def run_query(self,  tables, headings):
        TRET = self.get_group(tables, "TRET", True)
        if (TRET is not None):  
            self.check_string_length(TRET,"TRET","TRET_MODE","HEADING == 'DATA'",1,100)
