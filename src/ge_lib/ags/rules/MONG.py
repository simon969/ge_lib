import pandas as pd
from datetime import timedelta
from ags.pyAGS.AGSQuery import ags_query


class MONG001(ags_query):
    def __init__(self):
        super().__init__(id='MONG001', 
                         description="Is the MONG group present and does is contain data",
                         requirement = "optional",
                         action = "Check that the MONG group is present and that it contains data")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):
            self.check_row_count(MONG,"MONG","HEADING == 'DATA'",1,10000)
class MONG002(ags_query):
    def __init__(self):
        super().__init__(id='MONG002', 
                         description="Are the top and base of the reponse zone MONG_TRZ and MONG_BRZ headings completed for all records in the MONG group",
                         requirement = "key field",
                         action = "Check that the top and bottom of the response zone MONG_TRZ and MONG_BRZ have been completed for all records in the MONG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        MONG = self.get_group(tables, "MONG", True)
        if (LOCA is not None and MONG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(MONG,"MONG","MONG_TRZ",qry,0,FDEP)
                self.check_value(MONG,"MONG","MONG_BRZ",qry,0,FDEP)
class MONG003(ags_query):
    def __init__(self):
        super().__init__(id='MONG003', 
                         description="Is the pipe reference PIPE_REF recorded for all records in the MONG group",
                         requirement = "key field",
                         action = "Check that the pipe reference PIPE_REF is recorded for all records in the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","PIPE_REF","HEADING == 'DATA'",1,100)

class MONG004(ags_query):
    def __init__(self, MONG_TYPE_ALLOWED):
        self.MONG_TYPE_ALLOWED= MONG_TYPE_ALLOWED
        super().__init__(id='MONGG004', 
                         description="Is the allowed monitoring type MONG_TYPE {0} recorded for all records in the MONG group".format(self.MONG_TYPE_ALLOWED),
                         requirement = "key field",
                         action = "Check that the correct monitoing type MONG_TYPE {0} is recorded for all records in the MONG group".format(self.MONG_TYPE_ALLOWED))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_allowed(MONG,"MONG","MONG_TYPE","HEADING == 'DATA'",self.MONG_TYPE_ALLOWED)

class MONG005(ags_query):
    def __init__(self, MONG_DATE_MIN, MONG_DATE_MAX):
        self.MONG_DATE_MIN = MONG_DATE_MIN
        self.MONG_DATE_MAX = MONG_DATE_MAX
        super().__init__(id='MONG005', 
                         description="Is the monitoring instalation date MONG_DATE between {0} and {1} for all records in the MONG group".format(self.MONG_DATE_MIN,self.MONG_DATE_MAX),
                         requirement = "data required",
                         action = "Check that the monitoring date MONG_DATE is completed and in the range {0} and {1} for all records in the MONG group".format(self.MONG_DATE_MIN,self.MONG_DATE_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_datetime(MONG,"MONG","MONG_DATE","HEADING == 'DATA'",self.MONG_DATE_MIN,self.MONG_DATE_MAX)
class MONG006(ags_query):
    def __init__(self):
        super().__init__(id='MONG006', 
                         description="Are details of the instrument MONG_DETL recorded for all records in the MONG group",
                         requirement = "data required",
                         action = "Check that the details of the instrument MONG_DETL is recorded for all records in the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_DETL","HEADING == 'DATA'",1,255)
class MONG007(ags_query):
    def __init__(self, ):
        super().__init__(id='MONG007', 
                         description="Is the monitoring point reference MONG_ID unique and recorded for all records in the MONG group",
                         requirement = "key field",
                         action = "Check that the monitoring point reference MONG_ID is unique and recorded for all records in the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):
            dMONG= MONG.query("HEADING == 'DATA'")  
            for index, values in dMONG.iterrows():
                qry = "LOCA_ID == '{0}' and MONG_ID == '{1}'".format(values['LOCA_ID'],values['MONG_ID'])
                self.check_unique(MONG,"MOND", qry,"MONG_ID")
class MONG008(ags_query):
    def __init__(self):
        super().__init__(id='MONG008', 
                         description="Have remarks MONG_REM been recorded for all records in the MONG group",
                         requirement = "data required",
                         action = "Check that remarks MONG_REM are recorded for all records in the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_REM","HEADING == 'DATA'",1,255)
class MONG009(ags_query):
    def __init__(self):
        super().__init__(id='MONG009', 
                         description="Is the inital instalation depth of instrument MONG_DIS recorded for all records in the MONG group",
                         requirement = "data required",
                         action = "Check that the initial installation depth of the instrument MONG_DIS is recorded for all records in the MONG group")
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        MONG = self.get_group(tables, "MONG", True)
        if (LOCA is not None and MONG is not None):
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                FDEP = pd.to_numeric(values['LOCA_FDEP'])
                self.check_value(MONG,"MONG","MONG_DIS",qry,0,FDEP)
class MONG010(ags_query):
    def __init__(self, MONG_BRGA_MIN, MONG_BRGA_MAX):
        self.MONG_BRGA_MIN = MONG_BRGA_MIN
        self.MONG_BRGA_MAX = MONG_BRGA_MAX
        super().__init__(id='MONG010', 
                         description="Is the bearing of monitoring axis A MONG_BRGA recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGA_MIN, self.MONG_BRGA_MAX),
                         requirement = "check data",
                         action = "Check that the bearing of monitoring axis A MONG_BRGA is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGA_MIN, self.MONG_BRGA_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_BRGA","HEADING == 'DATA'",self.MONG_BRGA_MIN,self.MONG_BRGA_MAX)   


class MONG011(ags_query):
    def __init__(self, MONG_BRGB_MIN, MONG_BRGB_MAX):
        self.MONG_BRGB_MIN = MONG_BRGB_MIN
        self.MONG_BRGB_MAX = MONG_BRGB_MAX
        super().__init__(id='MONG011', 
                         description="Is the bearing of monitoring axis B MONG_BRGB recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGB_MIN, self.MONG_BRGB_MAX),
                         requirement = "check data",
                         action = "Check that the bearing of monitoring axis B MONG_BRGB is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGB_MIN, self.MONG_BRGB_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_BRGB","HEADING == 'DATA'",self.MONG_BRGB_MIN,self.MONG_BRGB_MAX)  

class MONG012(ags_query):
    def __init__(self, MONG_BRGC_MIN, MONG_BRGC_MAX):
        self.MONG_BRGC_MIN = MONG_BRGC_MIN
        self.MONG_BRGC_MAX = MONG_BRGC_MAX
        super().__init__(id='MONG012', 
                         description="Is the bearing of monitoring axis C MONG_BRGC recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGC_MIN, self.MONG_BRGC_MAX),
                         requirement = "check data",
                         action = "Check that the bearing of monitoring axis C MONG_BRGC is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_BRGC_MIN, self.MONG_BRGC_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_BRGC","HEADING == 'DATA'",self.MONG_BRGC_MIN,self.MONG_BRGC_MAX)  

class MONG013(ags_query):
    def __init__(self, MONG_INCA_MIN, MONG_INCA_MAX):
        self.MONG_INCA_MIN = MONG_INCA_MIN
        self.MONG_INCA_MAX = MONG_INCA_MAX
        super().__init__(id='MONG013', 
                         description="Is the inclination axis A of instrument MONG_INCA recorded in the range {0} to {1} for all records in the MONG group".format(self.MONG_INCA_MIN,self.MONG_INCA_MAX),
                         requirement = "check data",
                         action = "Check that the inclination axis A of instrument MONG_INCA is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_INCA_MIN,self.MONG_INCA_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_INCA","HEADING == 'DATA'", self.MONG_INCA_MIN, self.MONG_INCA_MAX)  
class MONG014(ags_query):
    def __init__(self, MONG_INCB_MIN, MONG_INCB_MAX):
        self.MONG_INCB_MIN = MONG_INCB_MIN
        self.MONG_INCB_MAX = MONG_INCB_MAX
        super().__init__(id='MONG014', 
                         description="Is the inclination axis B of instrument MONG_INCB recorded in the range {0} to {1} for all records in the MONG group".format(self.MONG_INCB_MIN,self.MONG_INCB_MAX),
                         requirement = "check data",
                         action = "Check that the inclination axis B of instrument MONG_INCB is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_INCB_MIN,self.MONG_INCB_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_INCB","HEADING == 'DATA'", self.MONG_INCB_MIN, self.MONG_INCB_MAX)  
class MONG015(ags_query):
    def __init__(self, MONG_INCC_MIN, MONG_INCC_MAX):
        self.MONG_INCC_MIN = MONG_INCC_MIN
        self.MONG_INCC_MAX = MONG_INCC_MAX
        super().__init__(id='MONG015', 
                         description="Is the inclination axis C of instrument MONG_INCC recorded in the range {0} to {1} for all records in the MONG group".format(self.MONG_INCC_MIN,self.MONG_INCC_MAX),
                         requirement = "check data",
                         action = "Check that the inclination axis C of instrument MONG_INCC is recorded in the range of {0} to {1} for all records in the MONG group".format(self.MONG_INCC_MIN,self.MONG_INCC_MAX))
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_value(MONG,"MONG","MONG_INCC","HEADING == 'DATA'", self.MONG_INCC_MIN, self.MONG_INCC_MAX)  
class MONG016(ags_query):
    def __init__(self):
        super().__init__(id='MONG016', 
                         description="Is the reading sign convention in direction A MONG_RSCA recorded for all records of the MONG group",
                         requirement = "check data",
                         action = "Check that the reading sign convention in direction A MONG_RSCA is recorded in all records of the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_RSCA","HEADING == 'DATA'",1,255)  
class MONG017(ags_query):
    def __init__(self):
        super().__init__(id='MONG017', 
                         description="Is the reading sign convention in direction B MONG_RSCB recorded for all records of the MONG group",
                         requirement = "check data",
                         action = "Check that the reading sign convention in direction B MONG_RSCB is recorded in all records of the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_RSCB","HEADING == 'DATA'",1,255)  
class MONG018(ags_query):
    def __init__(self):
        super().__init__(id='MONG018', 
                         description="Is the reading sign convention in direction C MONG_RSCC recorded for all records of the MONG group",
                         requirement = "check data",
                         action = "Check that the reading sign convention in direction C MONG_RSCC is recorded in all records of the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_RSCC","HEADING == 'DATA'",1,255)  
class MONG019(ags_query):
    def __init__(self):
        super().__init__(id='MONG019', 
                         description="Is the contractor who installed the instrument MONG_CONT recorded in all records of the MONG group",
                         requirement = "check data",
                         action = "Check that the contractor who installed the instrument MONG_CONT recorded in all records of the MONG group")
    def run_query(self,  tables, headings):
        MONG = self.get_group(tables, "MONG", True)
        if (MONG is not None):  
            self.check_string_length(MONG,"MONG","MONG_CONT","HEADING == 'DATA'",1,255)
