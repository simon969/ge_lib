import pandas as pd
from datetime import timedelta
from .ags_query import ags_query


class TRIT001(ags_query):
    def __init__(self):
        super().__init__(id='TRIT001', 
                         description="Is the TRIT group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the TRIT group is present and that it contains data")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):
            self.check_row_count(TRIT,"TRIT","HEADING == 'DATA'",1,10000)
class TRIT002(ags_query):
    def __init__(self):
        super().__init__(id='TRIT002', 
                         description="Is the SAMP_TOP and SPEC_DPTH heading completed for all records in the TRIT group",
                         requirement = "key field",
                         action = "Check that the top of the samples and the specimen depth have been recorded in the SAMP_TOP and SPEC_DPTH headings for all records in the TRIT group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        TRIT = self.get_group(tables, "TRIT", True)
        if (LOCA is not None and TRIT is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(TRIT,"TRIT","SAMP_TOP",qry,0,FDEP)
                self.check_value(TRIT,"TRIT","SPEC_DPTH",qry,0,FDEP)
class TRIT003(ags_query):
    def __init__(self):
        super().__init__(id='TRIT003', 
                         description="Is the sample reference SAMP_REF recorded for all records in the TRIT group",
                         requirement = "key field",
                         action = "Check that the sample reference SAMP_REF is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","SAMP_REF","HEADING == 'DATA'",1,100)

class TRIT004(ags_query):
    def __init__(self, SAMP_TYPE_ALLOWED):
        self.SAMP_TYPE_ALLOWED= SAMP_TYPE_ALLOWED
        super().__init__(id='TRITG004', 
                         description="Is the allowed sample type SAMP_TYPE {0} recorded for all records in the TRIT group".format(self.SAMP_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct sample type SAMP_TYPE {0} is recorded for all records in the TRIT group".format(self.SAMP_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_allowed(TRIT,"TRIT","SAMP_TYPE","HEADING == 'DATA'",self.SAMP_TYPE_ALLOWED)

class TRIT005(ags_query):
    def __init__(self):
        super().__init__(id='TRIT005', 
                         description="Is the sample identification SAMP_ID recorded for all records in the TRIT group",
                         requirement = "key field",
                         action = "Check that the sample identification SAMP_ID is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","SAMP_ID","HEADING == 'DATA'",1,100)
class TRIT006(ags_query):
    def __init__(self):
        super().__init__(id='TRIT006', 
                         description="Is the specimen reference SPEC_REF recorded for all records in the TRIT group",
                         requirement = "key field",
                         action = "Check that the specimen reference SPEC_REF is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","SPEC_REF","HEADING == 'DATA'",1,100)
class TRIT007(ags_query):
    def __init__(self):
        super().__init__(id='TRIT007', 
                         description="Is the triaxial test/stage number TRIT_TESN recorded for all records in the TRIT group",
                         requirement = "key field",
                         action = "Check that the triaxial test/stage number TRIT_TESN is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","TRIT_TESN","HEADING == 'DATA'",1,100)

class TRIT008(ags_query):
    def __init__(self):
        super().__init__(id='TRIT008', 
                         description="Have remarks TRIT_REM been recorded for all records in the TRIT group",
                         requirement = "data required",
                         action = "Check that remarks TRIT_REM are recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","TRIT_REM","HEADING == 'DATA'",1,255)
class TRIT009(ags_query):
    def __init__(self):
        super().__init__(id='TRIT009', 
                         description="Is the inital bulk density TRIT_BDEN recorded for all records in the TRIT group",
                         requirement = "data required",
                         action = "Check that the initial bulk density TRIT_BDEN is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_BDEN","HEADING == 'DATA'",0.5, 2.5)   
class TRIT010(ags_query):
    def __init__(self):
        super().__init__(id='TRIT010', 
                         description="Is the inital dry density TRIT_DDEN recorded for all records in the TRIT group",
                         requirement = "data required",
                         action = "Check that the initial dry density TRIT_DDEN is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_DDEN","HEADING == 'DATA'",0.5,2.5)   
class TRIT011(ags_query):
    def __init__(self):
        super().__init__(id='TRIT011', 
                         description="Is the specimen diameter TRIT_SDIA recorded for all records in the TRIT group",
                         requirement = "data required",
                         action = "Check that the specimen diameter TRIT_SDIA is recorded for all records in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_SDIA","HEADING == 'DATA'",40,110)   
class TRIT012(ags_query):
    def __init__(self):
        super().__init__(id='TRIT012', 
                         description="Is the specimen length TRIT_LEN recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the specimen length TRIT_LEN is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_LEN","HEADING == 'DATA'",100,450)   
# class TRIT013(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT013', 
#                          description="Is the method of saturation TRIT_SAT recorded in the TRIT group",
#                          requirement = "check data",
#                          action = "Check that the method of saturation TRIT_SAT is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             self.check_string_length(TRIT,"TRIT","TRIT_SAT","HEADING == 'DATA'",1,255)  
# class TRIT014(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT014', 
#                          description="Are the details of the consolidation stage TRIT_CONS recorded in the TRIT group",
#                          requirement = "check data",
#                          action = "Check that the details of the consolidation stage TRIT_CONS is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             self.check_string_length(TRIT,"TRIT","TRIT_REVS","HEADING == 'DATA'",1,255) 
# class TRIT015(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT015', 
#                          description="Is the effective stress at the end of the consolidation stage TRIT_CONP recorded in the TRIT group",
#                          requirement = "data required",
#                          action = "Check that the effective stress at the end of the consolidation stage TRIT_CONP is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             self.check_value(TRIT,"TRIT","TRIT_CONP","HEADING == 'DATA'",10,600)  
class TRIT016(ags_query):
    def __init__(self):
        super().__init__(id='TRIT016', 
                         description="Is the total cell pressure during shearing stage TRIT_CELL recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the total cell pressure during shearing stage TRIT_CELL is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_CELL","HEADING == 'DATA'",10,600)  
# class TRIT017(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT017', 
#                          description="Is the porewater pressure at the start of the shearing stage TRIT_PWPI recorded in the TRIT group",
#                          requirement = "data required",
#                          action = "Check that the porewater pressure at the start of the shearing stage TRIT_PWPI is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             self.check_value(TRIT,"TRIT","TRIT_PWPI","HEADING == 'DATA'",1,30)  
# class TRIT018(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT018', 
#                          description="Is the rate of axial strain TRIT_STRR recorded in the TRIT group",
#                          requirement = "data required",
#                          action = "Check that therate of axial strain TRIT_STRR is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             # AGS4 v 4.1 Dec 2020 suggests 1.5% /hour  
#             self.check_value(TRIT,"TRIT","TRIT_STRR","HEADING == 'DATA'",0.5,3)  

class TRIT019(ags_query):
    def __init__(self):
        super().__init__(id='TRIT019', 
                         description="Is the axial strain at failure TRIT_STRN recorded in the TRIT group",
                         requirement = "check data",
                         action = "Check that the axial strain at failure TRIT_STRN is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
             # AGS4 v 4.1 Dec 2020 suggests 9% 
            self.check_value(TRIT,"TRIT","TRIT_STRN","HEADING == 'DATA'",1,20)

class TRIT020(ags_query):
    def __init__(self):
        super().__init__(id='TRIT020', 
                         description="Is the deviator stress at failure TRIT_DEVF recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the deviator stress at failure TRIT_DEVF is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_DEVF","HEADING == 'DATA'",100,600)
# class TRIT021(ags_query):
#     def __init__(self):
#         super().__init__(id='TRIT021', 
#                          description="Is the porewater pressure at failure TRIT_PWPF recorded in the TRIT group",
#                          requirement = "check data",
#                          action = "Check that the porewater pressure at failure TRIT_PWP is recorded in the TRIT group")
#     def run_query(self,  tables, headings):
#         TRIT = self.get_group(tables, "TRIT", True)
#         if (TRIT is not None):  
#             self.check_value(TRIT,"TRIT","TRIT_PWPF","HEADING == 'DATA'",40,200)
class TRIT022(ags_query):
    def __init__(self):
        super().__init__(id='TRIT022', 
                         description="Is the initial water/moisture content TRIT_IMC recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the initial water/moisture content TRIT_IMC is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_IMC","HEADING == 'DATA'",1,100)
class TRIT023(ags_query):
    def __init__(self):
        super().__init__(id='TRIT023', 
                         description="Is the final water/moisture content TRIT_FMC recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the final water/moisture content TRIT_FMC is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_value(TRIT,"TRIT","TRIT_FMC","HEADING == 'DATA'",1,100)
class TRIT024(ags_query):
    def __init__(self):
        super().__init__(id='TRIT024', 
                         description="Is the voumetric strain at failure TRIT_STV recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the volumetric strain at failure TRIT_STV is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            # AGS4 v 4.1 Dec 2020 suggests 2.56%
            self.check_value(TRIT,"TRIT","TRIT_STV","HEADING == 'DATA'",0.5,5)
class TRIT025(ags_query):
    def __init__(self):
        super().__init__(id='TRIT025', 
                         description="Is the mode of failure TRIT_MODE recorded in the TRIT group",
                         requirement = "data required",
                         action = "Check that the mode of failure TRIT_MODE is recorded in the TRIT group")
    def run_query(self,  tables, headings):
        TRIT = self.get_group(tables, "TRIT", True)
        if (TRIT is not None):  
            self.check_string_length(TRIT,"TRIT","TRIT_MODE","HEADING == 'DATA'",1,100)
