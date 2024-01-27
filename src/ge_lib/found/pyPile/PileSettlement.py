import numpy as np
import math
import json

from ge_lib.found.pyGround.GroundModel import GroundModel
from ge_lib.found.pyGround.Support import has_values, as_float_list, list_has_not_none_attrib, as_one_list

from ge_lib.found.pyPile.PileGeoms import Pile
from ge_lib.found.pyPile.PileCalcs import StandardCalcs, min_width


standard_calc = StandardCalcs()

PILE_RESISTANCE_INCREMENT_DEFAULT = -0.5
STANDARD_STEPS = [0,0.0001,0.0002,0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.0015, 0.002, 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.10]


def get_resistances_at_level(level:float, levels:list, qs:list, qb:list):
  found = False
  for i in range(len(levels)):
    if levels[i] < level:
        found = True
        break
  if found==True:
    return levels[i-1], qs[i-1], qb[i-1]
  
def get_resistances_at_length(length:float, levels:list, qs:list, qb:list):
  level = levels[0] - length
  return get_resistances_at_level(level,levels,qs,qb)

def get_resistances_at_total_load(load:float, levels:list, qs:list, qb:list):
  found = False
  for i in range(len(levels)):
    if qs[i] + qb[i] > load:
        found = True
        break
  if found==True:
    return levels[i], qs[i], qb[i]
    
def get_CIRIA181Fleming1992 (dia:float, area:float,length:float, Epile:float, Ms:float, Ke:float, qub:float,qus:float, Em:float, disp):
    
    # https://www.pilegroups.com/single-post/fleming-s-method-for-pile-settlement-analysis-in-the-pilelat-program
    
    size = len(disp)
    res = []

    load_shaft_mob = [0.00] * size
    load_base_mob =  [0.00] * size
    load_total_mob =  [0.00] * size
    disp_elastic_no_slip =  [0.00] * size
    disp_elastic_full_slip =  [0.00] * size
    disp_elastic =  [0.00] * size
    disp_total =  [0.00] * size
    
    for i in range(size):
      load_shaft_mob[i] = disp[i] / (Ms * area + disp[i]) * qus
      load_base_mob[i] = qub * dia * Em * disp[i] / (0.6 * qub + dia * Em * disp[i])
      load_total_mob[i]= load_shaft_mob[i] + load_base_mob[i]
      disp_elastic_no_slip[i] =  Ke *(4.0*load_total_mob[i]*length)/(math.pi*math.pow(dia,2.0)*Epile)
      disp_elastic_full_slip[i] = 4.0*length*(load_total_mob[i]-qus*(1-Ke))/(math.pi*math.pow(dia,2.0)*Epile)
      if load_total_mob[i]> qus:
        disp_elastic[i] = disp_elastic_full_slip[i]
      else:
        disp_elastic[i] = disp_elastic_no_slip[i]
      disp_total[i] = disp[i] + disp_elastic[i]
      
      r = {"disp_geo": disp[i],
           "load_shaft_mob":load_shaft_mob[i],
           "load_base_mob":load_base_mob[i],
           "load_total_mob":load_total_mob[i],
           "disp_elastic_no_slip":disp_elastic_no_slip[i],
           "disp_elastic_full_slip":disp_elastic_full_slip[i],
           "disp_elastic":disp_elastic[i],
           "disp_total":disp_total[i],
           }
      res.append(r)

    data = {"qus":qus, 
              "Ms": Ms, 
              "area": area, 
              "Ke":Ke, 
              "Epile":Epile,
              "length":length,
              "qub":qub, 
              "Em":Em, 
              "dia":dia,
              "disp": disp}
    
    result = { "data":data,
               "results":res}
    
    return result 

def list_attrib(items:list, attrib):
  ret = []
  for i in range (len(items)):
    ret.append (items[i][attrib])
  return ret

class PileSettlement:

  def __init__(self, description: str , pile:Pile, gm:GroundModel, pile_resistance:list, steps:[]=STANDARD_STEPS):
    self.description = description
    self.ground_model = gm
    self.pile = pile
    self.levels = list_attrib(pile_resistance,'level')
    self.qus = list_attrib(pile_resistance,'qus_comp')
    self.qub = list_attrib(pile_resistance,'qub')
    self.disp_geotech = min_width(pile) * np.array(steps)
  
  def getSettlementProfiles(self):
    
    set_profiles = []
  
    # Check that objects have required parameters for settlement calculations

    if not any(has_values(self.pile,['ke','ms','e_mod'],[0,0,0])):
      return set_profiles
    if not any(as_one_list(list_has_not_none_attrib(self.ground_model.strata_set,['UndrainedEMod', 'DrainedEMod']))):
      return set_profiles
    
    if hasattr(self.pile,"loads"):
      pile_loads = as_float_list(self.pile.loads)
      for i in range (len(pile_loads)):
        res = self.getSettlementProfile(load=pile_loads[i])
        set_profile = {"description":"Pile Load:" + str(pile_loads[i]),
                       "data":res["data"],
                       "results": res["results"]}
        set_profiles.append(set_profile)
        
    if hasattr(self.pile,"lengths"):
      pile_lengths = as_float_list(self.pile.lengths)
      for i in range (len(pile_lengths)):
        res = self.getSettlementProfile(length=pile_lengths[i])
        set_profile = {"description":"Pile Length:" + str(pile_lengths[i]),
                       "data": res["data"],
                       "results": res["results"]}
        set_profiles.append(set_profile)
    
    if hasattr(self.pile,"levels"):
      pile_levels = as_float_list(self.pile.levels)
      for i in range (len(pile_levels)):
        res = self.getSettlementProfile(level=pile_levels[i])
        set_profile = {"description":"Pile Level:" + str(pile_levels[i]),
                       "data": res["data"],
                       "results": res["results"]}
        set_profiles.append(set_profile)
      
    return set_profiles
  def getSettlementProfilesJSON (self):
    ret = []
    profiles = self.getSettlementProfiles()
    for p  in profiles:
      descr = p["description"]
      results = p["results"]
      data = p["data"]
      res = []
      for r in results:
        row = "{{\"disp_geo\":{0:.6f},\"load_shaft_mob\":{1:.3f},\"load_base_mob\":{2:.3f},\"load_total_mob\":{3:.3f},\"disp_elastic_no_slip\":{4:.6f},\"disp_elastic_full_slip\":{5:.6f},\"disp_elastic\":{6:.6f},\"disp_total\":{7:.6f}}}".format(r["disp_geo"],r["load_shaft_mob"],r["load_base_mob"],r["load_total_mob"],r["disp_elastic_no_slip"],r["disp_elastic_full_slip"],r["disp_elastic"],r["disp_total"])
        res.append (row)
      pres = "{{\"description\":\"{0}\",\"data\":\"{{1}}\",\"results\":[{2}]}}".format(descr, data, ",".join(res))
      ret.append(pres)
    return ret
  #"":disp_elastic_no_slip, 
  #            "disp_elastic_full_slip":disp_elastic_full_slip, 
  #            "disp_elastic":disp_elastic, 
  #            "disp_total":disp_total}
  #    
  def getSettlementProfile (self, level=None, load=None, length=None):
    
    if (load is not None):
      level, qus, qub = get_resistances_at_total_load(load, self.levels, self.qus, self.qub)
    
    if (level is not None):
       level, qus, qub = get_resistances_at_level(level, self.levels, self.qus, self.qub)
    
    if (length is not None):
       level, qus, qub = get_resistances_at_length(length, self.levels, self.qus, self.qub)

    if (level is not None and qus is not None and qub is not None):

      pile_length = self.levels[0] - level

      Eu = self.ground_model.get_attr_value (level, "UndrainedEMod")
      Ed = self.ground_model.get_attr_value (level, "DrainedEMod")
      
      if (Eu==0):
        Em = Ed
      else:
        if (Ed<Eu):
          Em = Ed
        else:
          Em = Eu
      
      equiv_dia = math.pow(self.pile.base*4/math.pi, 0.5)
      
      resp = get_CIRIA181Fleming1992 (dia = equiv_dia,
                                      area = pile_length * self.pile.perimeter,
                                      length = pile_length,
                                      Epile=self.pile.e_mod,
                                      Ms = self.pile.ms,
                                      Ke = self.pile.ke,
                                      qub = qub,
                                      qus = qus,
                                      Em = Em,
                                      disp=self.disp_geotech
                                      )

      return resp


    
  
     
