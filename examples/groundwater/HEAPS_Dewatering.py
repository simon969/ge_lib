import GroundWaterModelling as gwm


def Main():
   
# run_HEAPS_20mGrid()
 run_HEAPS_ExistingRiverWall()
 
def run_HEAPS_TestShaftLocations():
    
    # HEAPS	Heathwall Pumping Station CSO shaft	529576.3369	177637.578	16	SH12X
    # HEAPS2 Heathwall Pumping Station InterceptionShaft	529523.663	177653.777	10	SH12A

    ds = get_HEAPS_DewateringSite()
    
    rp =  gwm.resultPoints("HEAPS Shafts")
    
    rp.addPoint (529576.3369, 177637.578)
    rp.addPoint (529523.663, 177653.777)
    rp.addPoint (526000, 181200)
    
    rp.setOutputDrawdownStrata("WCK")
    rp.readDewateringSite(ds)
    
    rp.Print()
    

    
def run_HEAPS_Line():
    
    # HEAPS	Heathwall Pumping Station CSO shaft	529576.3369	177637.578	16	SH12X
    # HEAPS2 Heathwall Pumping Station InterceptionShaft	529523.663	177653.777	10	SH12A

    ds = get_HEAPS_DewateringSite()
    
    rl =  gwm.resultLine("2m Line", 526000,181200,533100,174100,2)
    
    rl.setOutputDrawdownStrata ("WCK")
    
    rl.readDewateringSite(ds)
    
    rl.Print()
    
    folderOut = r'C:\Users\ThomsonSJ\Documents\2018\Tideway C410\HEAPS\Dewatering\\'
    
    rl.writeSettlement(folderOut + "HEAPS_Settlement_Line2m.csv")
    
    rl.writeDrawdown(folderOut + "HEAPS_Drawdown_Line2m.csv")

def run_HEAPS_ExistingRiverWall_LGF_WellsONLY():
    
    ds = get_HEAPS_LambethWells()
    
    rl =  gwm.resultLine("0.25m Line", 529469.5, 177588.4,529641.5, 177676.8, 0.25)
    
    rl.setOutputDrawdownStrata("LCF")
    
    rl.readDewateringSite(ds)
    
    rl.Print()
    
    folderOut = r'C:\Users\ThomsonSJ\Documents\2018\Tideway C410\HEAPS\Dewatering\\'
    
    rl.writeSettlement(folderOut + "HEAPS_Settlement_ExistingRiverWall_Line0.25m.csv")
    
    rl.writeDrawdown(folderOut + "HEAPS_WCK_Drawdown_ExistingRiverWall_Line0.25m.csv")



def run_HEAPS_ExistingRiverWall():
    
    ds = get_HEAPS_DewateringSite()
    
    rl =  gwm.resultLine("0.25m Line", 529469.5, 177588.4,529641.5, 177676.8, 0.25)
    
    rl.setOutputDrawdownStrata("WCK")
    
    rl.readDewateringSite(ds)
    
    rl.Print()
    
    folderOut = r'C:\Users\ThomsonSJ\Documents\2018\Tideway C410\HEAPS\Dewatering\\'
    
    rl.writeSettlement(folderOut + "HEAPS_Settlement_ExistingRiverWall_Line0.25m.csv")
    
    rl.writeDrawdown(folderOut + "HEAPS_WCK_Drawdown_ExistingRiverWall_Line0.25m.csv")
    
def run_HEAPS_2mGrid():
    ds = get_HEAPS_DewateringSite()
    
    rg = gwm.resultGrid("Grid2m", 526000,181200,533100,174100,2,-2)
    
    rg.setOutputDrawdownStrata("WCK")
    
    rg.readDewateringSite(ds)
    
    folderOut = r'C:\Users\ThomsonSJ\Documents\2018\Tideway C410\HEAPS\Dewatering\\'
    
    rg.writeSettlement(folderOut + "HEAPS_Settlement2mGrid.csv")
    
    rg.writeDrawdown(folderOut + "HEAPS_WCK_Drawdown2mGrid.csv")

def run_HEAPS_20mGrid():
    ds = get_HEAPS_DewateringSite()
    
    rg = gwm.resultGrid("Grid20m", 526000,181200,533100,174100,20,-20)
    
    rg.setOutputDrawdownStrata("WCK")
    
    rg.readDewateringSite(ds)
    
    folderOut = r'C:\Users\ThomsonSJ\Documents\2018\Tideway C410\HEAPS\Dewatering\\'
    
    rg.writeSettlement(folderOut + "HEAPS_Settlement20mGrid.csv")
    
    rg.writeDrawdown(folderOut + "HEAPS_WCK_Drawdown20mGrid.csv")

def run_Drawdown_Test101():
    
    heaps1 = gwm.DewateringSite('Heaps')
    heaps1.addStrata ('LCF',96.5,66.35,20,20,89.8,0.74*1000/0.7)
    heaps1.calcGroundModel()
    heaps1.GroundModel.Print()
    heaps1.GroundModel.setStrataDrawdown('LCF', 36.5)
    heaps1.GroundModel.calcStress()
    heaps1.GroundModel.Print()

def get_HEAPS_DewateringSite():
    
    heaps1 = gwm.DewateringSite('Heaps')
    
    heaps1.addStrata ('LCF',96.5,66.35,20,20,89.8,0.74*1000/0.7)
    heaps1.addStrata ('HF',66.35,66,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('USB,UMB',66,59.9,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LG-SU',59.9,59.1,20,20,89.7,1.71*1000/0.7)
    heaps1.addStrata ('LB-C',57.9,51.6,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LMB-C',51.6,49.95,14,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LMB-G,UF',49.95,48.6,20,20,89.7,1.71*1000/0.7)
    heaps1.addStrata ('TS',48.6,39.1,20,20,89.7,1*1000/0.7)
    heaps1.addStrata ('BB',39.1,38.9,20,20,89.7,1*1000/0.7)
    heaps1.addStrata ('WCK',38.9,8.9,20,20,89.7,1.74*1000/0.7)
    heaps1.calcGroundModel()
    
    heaps1.addWell("CH01",529587.4,177631.3,1728,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH01",1.0)
    heaps1.addWellStrata("TS","CH01",1.0)
    heaps1.addWellStrata("BB","CH01",1.0)
    heaps1.addWellStrata("WCK","CH01",1.0)
    
    heaps1.addWell("CH02",529559.1,177643.3,1728,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH02",1.0)
    heaps1.addWellStrata("TS","CH02",1.0)
    heaps1.addWellStrata("BB","CH02",1.0)
    heaps1.addWellStrata("WCK","CH02",1.0)
    
    heaps1.addWell("CH03",529515.8,177617.2,1728,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH03",1.0)
    heaps1.addWellStrata("TS","CH03",1.0)
    heaps1.addWellStrata("BB","CH03",1.0)
    heaps1.addWellStrata("WCK","CH03",1.0)
    
    heaps1.addWell("CW01",529235.77,177559.48,1361.790875,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CW01",1.0)
    heaps1.addWellStrata("TS","CW01",1.0)
    heaps1.addWellStrata("BB","CW01",1.0)
    heaps1.addWellStrata("WCK","CW01",1.0)

    heaps1.addWell("CW2",529282.38,177594.13,1361.790875,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CW2",1.0)
    heaps1.addWellStrata("TS","CW2",1.0)
    heaps1.addWellStrata("BB","CW2",1.0)
    heaps1.addWellStrata("WCK","CW2",1.0)
    
    heaps1.addWell("CW3",529214.28,177573.01,1361.790875,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CW3",1.0)
    heaps1.addWellStrata("TS","CW3",1.0)
    heaps1.addWellStrata("BB","CW3",1.0)
    heaps1.addWellStrata("WCK","CW3",1.0)
    
    heaps1.addWell("CW5",529193.76,177596.29,1361.790875,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CW5",1.0)
    heaps1.addWellStrata("TS","CW5",1.0)
    heaps1.addWellStrata("BB","CW5",1.0)
    heaps1.addWellStrata("WCK","CW5",1.0)
    
    heaps1.addWell("CH04",529526.3,177605.3,0,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH04",1.0)
    heaps1.addWellStrata("TS","CH04",1.0)
    heaps1.addWellStrata("BB","CH04",1.0)
    heaps1.addWellStrata("WCK","CH04",1.0)
    
    heaps1.addWell("CH05",529553.6,177612.5,0,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH05",1.0)
    heaps1.addWellStrata("TS","CH05",1.0)
    heaps1.addWellStrata("BB","CH05",1.0)
    heaps1.addWellStrata("WCK","CH05",1.0)
    
    heaps1.addWell("CH06",529567.9,177617.2,0,295,274,0.0001)
    heaps1.addWellStrata("LMB-G,UF","CH06",1.0)
    heaps1.addWellStrata("TS","CH06",1.0)
    heaps1.addWellStrata("BB","CH06",1.0)
    heaps1.addWellStrata("WCK","CH06",1.0)

    heaps1.addWell("PZ01",529573.5,177624.8,142.4346063,5,274,0.0003)
    heaps1.addWellStrata("LCF","PZ01",0.5)
    heaps1.addWellStrata("HF","PZ01",1.0)
    heaps1.addWellStrata("USB,UMB","PZ01",1.0)
    heaps1.addWellStrata("LG-SU","PZ01",1.0)
    heaps1.addWellStrata("LB-C","PZ01",1.0)
    heaps1.addWellStrata("LMB-C","PZ01",1.0)
    
    heaps1.addWell("SR7107",529569.9,177646,142.4346063,5,274,0.0003)
    heaps1.addWellStrata("LCF","SR7107",0.5)
    heaps1.addWellStrata("HF","SR7107",1.0)
    heaps1.addWellStrata("USB,UMB","SR7107",1.0)
    heaps1.addWellStrata("LG-SU","SR7107",1.0)
    heaps1.addWellStrata("LB-C","SR7107",1.0)
    heaps1.addWellStrata("LMB-C","SR7107",1.0)

    heaps1.calcWellProfiles(40)
    heaps1.GroundModel.Print()
    
    return heaps1

def get_HEAPS_LambethWells():
    LCFWaterLevel= 96.5 - 36.55/2
    heaps1 = gwm.DewateringSite('Heaps Lambeth Wells ONLY')
    heaps1.addStrata ('MG',105,101,20,20,105,0.74*1000/0.7)
    heaps1.addStrata ('ALV',101,96.5,20,20,101,0.74*1000/0.7)
    heaps1.addStrata ('LCF',96.5,66.35,20,20,LCFWaterLevel,0.74*1000/0.7)
    heaps1.addStrata ('HF',66.35,66,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('USB,UMB',66,59.9,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LG-SU',59.9,59.1,20,20,89.7,1.71*1000/0.7)
    heaps1.addStrata ('LB-C',57.9,51.6,20,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LMB-C',51.6,49.95,14,20,89.7,0.74*1000/0.7)
    heaps1.addStrata ('LMB-G,UF',49.95,48.6,20,20,89.7,1.71*1000/0.7)
    heaps1.addStrata ('TS',48.6,39.1,20,20,89.7,1*1000/0.7)
    heaps1.addStrata ('BB',39.1,38.9,20,20,89.7,1*1000/0.7)
    heaps1.addStrata ('WCK',38.9,8.9,20,20,89.7,1.74*1000/0.7)
    heaps1.calcGroundModel()
    
    heaps1.addWell("PZ01",529573.5,177624.8,142.4346063,5,274,0.0003)
    heaps1.addWellStrata("LCF","PZ01",0.5)
    heaps1.addWellStrata("HF","PZ01",1.0)
    heaps1.addWellStrata("USB,UMB","PZ01",1.0)
    heaps1.addWellStrata("LG-SU","PZ01",1.0)
    heaps1.addWellStrata("LB-C","PZ01",1.0)
    heaps1.addWellStrata("LMB-C","PZ01",1.0)
    
    heaps1.addWell("SR7107",529569.9,177646,142.4346063,5,274,0.0003)
    heaps1.addWellStrata("LCF","SR7107",0.5)
    heaps1.addWellStrata("HF","SR7107",1.0)
    heaps1.addWellStrata("USB,UMB","SR7107",1.0)
    heaps1.addWellStrata("LG-SU","SR7107",1.0)
    heaps1.addWellStrata("LB-C","SR7107",1.0)
    heaps1.addWellStrata("LMB-C","SR7107",1.0)

    heaps1.calcWellProfiles(40)
    heaps1.GroundModel.Print_tabular()
    
    return heaps1

Main()