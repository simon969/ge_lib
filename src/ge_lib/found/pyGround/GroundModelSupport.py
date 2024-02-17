import logging
import copy
from .GroundModel import GroundModel, StrataSet
from .Support import any_have_values, ValueLinear, get_value

DEFAULT_POISSON = 0.28
INCREMENT_DEFAULT = -0.5

def add_stresses_strength_stiffness(gm:GroundModel, log_file=None):
    """
    Takes a groundmodel (gm) and returns a copy with TotalStress, PWP, EffectiveStress and Cu profiles added to the gm.strata_set array

    Parameters
    ----------
    gm : Groundmodel
        Initialised ground model with stata_set populated, additional TotalStress, PWP, EffectiveStress and Cu profiles added
    log_file :  Logger file attached to the Groundmodel class to allow logging of errors and progress
    
    Returns 
    ----------
    GroundModel gm
        returns a deepcopy of the original GroundModel with the following added to the gm.strata_set array profiles
        stresses : TotalStress, PWP, EffectiveStress, 
        strengths : Cu 
        stiffnesses: UndrainedModulus, DrainedModulus
    """
    
    new_gm = copy.deepcopy(gm)
    add_total_stress(new_gm.strata_set, new_gm.surcharge)
    add_effective_stress(new_gm.strata_set)
    add_undrained_strength(new_gm.strata_set)
    add_emodulus(new_gm.strata_set)
    add_logger (new_gm, log_file)
    return new_gm

def get_value_grad (top, grad):
    if (top==None and grad==None):
        return None
    if (top==None and grad!=None):
        return ValueLinear(0,grad)
    if (top!=None and grad==None):
        return ValueLinear(top,0)
    if (top!=None and grad!=None):
        return ValueLinear(top, grad)

def add_undrained_strength (strataset:list):
    for s in strataset:
        if any_have_values(s, ["cu_top","cu_grad"]):
            s.Cu = get_value_grad(s.cu_top, s.cu_grad)
        
        if any_have_values(s,["ucs_top","usc_grad"]):
            s.UCS = get_value_grad(s.ucs_top, s.ucs_grad)
        
        if any_have_values (s,["su_top","su_grad"]):
            s.Su = get_value_grad(s.su_top, s.su_grad)

def add_total_stress (strataset:list, surcharge = 0.0):
    ts = surcharge  
    for s in strataset:
        ts = add_total_stress_grad(s,ts)     

def add_total_stress_grad(s:StrataSet, top_stress:float=0.0):
    
    s.TotalStress = ValueLinear(0,0) 
    s.PWP = ValueLinear(0,0)

    s.TotalStress.top = top_stress
    water_level = s.__dict__.get("water_level", s.level_base)

    if water_level >= s.level_top:
        s.TotalStress.base = s.TotalStress.top + s.thickness * s.density_sat
        s.TotalStress.gradient = s.density_sat
        s.PWP.top = (s.water_level - s.level_top) * s.water_density
        s.PWP.base = (s.water_level - s.level_base) * s.water_density
        s.PWP.average = s.water_density * (s.water_level - (s.level_top + s.level_base) / 2.0)
        s.PWP.gradient = s.water_density
    else:
        s.TotalStress.base = s.TotalStress.top + s.thickness * s.density_dry
        s.TotalStress.gradient = s.density_dry
        s.PWP.top = 0.0
        s.PWP.base = 0.0
        s.PWP.average = 0.0
        s.PWP.gradient = 0.0
    
    s.TotalStress.average = (s.TotalStress.top + s.TotalStress.base) / 2.0  

    return s.TotalStress.base

def add_effective_stress (strata:list):
        for s in strata:
            s.EffectiveStress = ValueLinear(0,0)
            # Calculate effective stress from TotalStress and PWP 
            s.EffectiveStress.top = s.TotalStress.top - s.PWP.top
            s.EffectiveStress.average = s.TotalStress.average - s.PWP.average
            s.EffectiveStress.gradient = s.TotalStress.gradient - s.PWP.gradient
            s.EffectiveStress.base = s.TotalStress.base - s.PWP.base

def add_emodulus(strata:list):
    for s in strata:
        
        # Undrained modulus
        eu_mod_top = get_value(s,"eu_mod_top",0)
        eu_mod_grad = get_value(s,"eu_mod_grad",0)

        if eu_mod_top != 0 or eu_mod_grad != 0:
            s.UndrainedEMod = ValueLinear(eu_mod_top,eu_mod_grad)

        if not hasattr(s,"UndrainedEMod"): 
            factor_eu_mod_cu = getattr(s, "factor_eu_mod_cu",0) 
            if factor_eu_mod_cu != 0 and hasattr(s, "Cu"):
                s.UndrainedEMod = s.Cu * factor_eu_mod_cu
        
        # Drained modulus
        ed_mod_top = get_value(s,"ed_mod_top",0)
        ed_mod_grad = get_value(s,"ed_mod_grad",0)

        if ed_mod_top != 0 or ed_mod_grad != 0:
            s.DrainedEMod = ValueLinear(ed_mod_top,ed_mod_grad)

        if not hasattr(s,"DrainedEMod"):
            factor_ed_mod_po = get_value(s, "factor_ed_mod_po",0)
            if factor_ed_mod_po != 0 and hasattr(s, "EffectiveStress"):
                s.DrainedEMod = s.EffectiveStress * factor_ed_mod_po
        
        if not hasattr(s,"DrainedEMod") and hasattr(s, "UndrainedEMod"):
            poisson = get_value(s,"poisson",DEFAULT_POISSON)
            EuEdRatio = (2.0*(1+poisson))/3.0
            s.DrainedEMod = s.UndrainedEMod * EuEdRatio
      
    

def print_ground_model(gm:GroundModel):
        print("Ground Model Name         %s" % gm.Description)
        print ("Strata  Level Level  Thick Density Density FactorEmodPo Initial  Initial Inital Initial Initial                                     Change           Water")
        print ("Description   Top   Bottom       Dry     Sub                  Water    Top Sz  Int Sz Bot Sz  Avg Sz  Water Top Sz  Int Sz Bot Sz  Avg Sz Avg Sz Emodulus  State")
        for s in gm.strata:
           print ("%5s  %.2f  %.2f  %.2f %.2f  %.2f    %.1f         %.2f     %.2f    %.2f   %.2f    %.2f    %.2f    %.2f   %.2f    %.2f  %.2f    %.2f   %.2f    %.2f   %.1f      %s   "%(s.Name[0:5],s.LevelTop,s.LevelBot,s.Thickness,s.DensityDry,s.DensitySub,s.FactorEModPo,s.InitialWaterLevel, s.InitialTotalStressTop, s.InitialTotalStressInt,  s.InitialTotalStressBot, s.InitialTotalStressAvg, s.InitialPWPAvg,s.WaterLevel, s.TotalStress.Top, s.TotalStressInt,  s.TotalStress.Bottom, s.TotalStress.Average, s.PWPAvg,s.ChangeEffectiveStressAvg,s.EModulus, s.WaterState))
def print_stress(self, name, stress):
        print("%s Top %s" % name, stress.Top)
        print("%s Bottom %s" % name, stress.Bottom)
        print("%s Intermediate %s" % name, stress.Intermediate)
        print("%s Average %s" % name, stress.Average)

def add_logger(gm:GroundModel, log_file):
        if gm and log_file:
            hdlr = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            gm.logger = logging.getLogger('GroundModel')
            gm.logger.addHandler(hdlr)
            gm.logger.setLevel(logging.INFO)    



# def Print(s):
#     print("===================================================")
#     print("Strata Name              %s" % s.Name)
#     print("Level Top                %s" % s.LevelTop)
#     print("Level Bot                %s" % s.LevelBot)
#     print("Thickness                %s" % s.Thickness)
#     print("Density Dry              %s" % s.DensityDry)
#     print("Density Sub              %s" % s.DensitySub)
#     print("FactorEModPo             %s" % s.FactorEModPo)
#     print("Inital Water Level       %s" % s.WaterLevel)
#     self.PrintStress("Initial Total Stress", self.InitialTotalStress)
#     self.PrintStress("Initial PWP", self.InitialPWP)
#     print("----------------------------")
#     print("Water Level              %s" % self.WaterLevel)
#     self.PrintStress("Total Stress", self.TotalStress)
#     print("PWP Avg                  %s" % self.PWP.Average)
#     print("Change Effective         %s" % self.ChangeEffectiveStress.Average)
#     print("EModulus                 %s" % self.EModulus)
#     print("WaterState               %s" % self.WaterState)
#     print("===================================================")

# def Print2(self):
#     print("===================================================")
#     print("Strata Name              %s" % self.Name)
#     print("Level Top                %s" % self.LevelTop)
#     print("Level Bot                %s" % self.LevelBot)
#     print("Thickness                %s" % self.Thickness)
#     print("Density Dry              %s" % self.DensityDry)
#     print("Density Sub              %s" % self.DensitySub)
#     print("FactorEModPo             %s" % self.FactorEModPo)
#     print("Inital Water Level       %s" % self.InitialWaterLevel)
#     print("Initial Total Stress Top %s" % self.InitialTotalStressTop)
#     print("Initial Total Stress Bot %s" % self.InitialTotalStressBot)
#     print("Initial Total Stress Int %s" % self.InitialTotalStressInt)
#     print("Initial Total Stress Avg %s" % self.InitialTotalStressAvg)
#     print("Initial PWP Avg          %s" % self.InitialPWPAvg)
#     print("----------------------------")
#     print("Water Level              %s" % self.WaterLevel)
#     print("Total Stress Top         %s" % self.TotalStress.Top)
#     print("Total Stress Bot         %s" % self.TotalStress.Bottom)
#     print("Total Stress Int         %s" % self.TotalStressInt)
#     print("Total Stress Avg         %s" % self.TotalStress.Average)
#     print("PWP Avg                  %s" % self.PWPAvg)
#     print("Change Effective         %s" % self.ChangeEffectiveStressAvg)
#     print("EModulus                 %s" % self.EModulus)
#     print("WaterState               %s" % self.WaterState)
#     print("===================================================")




