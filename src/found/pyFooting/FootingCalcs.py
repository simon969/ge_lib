import math
import json
from ..pyGround.Support import calc, calc_collection
from .calc_bearing_BS8004 import DrainedBearing_BS8004, UndrainedBearing_BS8004
from .calc_bearing_EC7 import DrainedBearing_EC7, UndrainedBearing_EC7



methods_dict = {
  'DrainedBearing_BS8004':DrainedBearing_BS8004(),
  'UndrainedBearing_BS8004':UndrainedBearing_BS8004(),
  'DrainedBearing_EC7':DrainedBearing_EC7(),
  'UndrainedBearing_EC7':UndrainedBearing_EC7()
   }
class StandardCalcs(calc_collection):
     def __init__(self):
        super().__init__(id= '01', description='standard bearing calc library',version='p01.1')
        self.append_calc(DrainedBearing_EC7())
        self.append_calc(DrainedBearing_BS8004())
        self.append_calc(UndrainedBearing_EC7())
        self.append_calc(UndrainedBearing_BS8004())     


def effective_footings (geoms:list, loadcases:list, conc_dens = 0.0) :
    
   # length = y
   # breadth = x
   
   results = []
   
   for geom in geoms:

      length = geom.get("length")
      breadth = geom.get("breadth")
      depth = geom.get("depth")

      for loadcase in loadcases:

         fx = loadcase.get("fx",0)
         fy = loadcase.get("fy",0)
         fz = loadcase.get("fz",0)
         mx = loadcase.get("mx",0)
         my = loadcase.get("my",0)
         mz = loadcase.get("mz",0)
         state = loadcase.get("state")
         
         self_weight = length * breadth * depth * conc_dens
         
         vload = fz + self_weight
         hload = math.pow(math.pow(fx, 2.0) + math.pow(fy, 2.0), 0.5)
         htheta_rad = 0.0
         
         if fy != 0:
            htheta_rad = math.atan(fx/fy)
         
         ex = my / vload
         ey = mx / vload

         eff_length =  length - 2 * ey
         eff_breadth = breadth - 2 * ex
         material_set = get_material_set(state)
         
         ef = {"geom":geom,
               "loadcase":loadcase,
               "length":eff_length, 
               "breadth":eff_breadth,
               "depth":depth,
               "vload":vload,
               "hload":hload,
               "htheta":htheta_rad,
               "state":state,
               "material_set":material_set
               }
         results.append(ef)
   
   return results

def get_material_set(state):

   if 'uls_c1' in state:
      return "m1" 
   if 'uls_c2' in state:
      return "m2" 
   if 'sls' in state:
      return "m1" 


def footing_resistance (footing, groundmodel, methods):
   
   results = []
   
   for method in methods:
       calc_class = methods_dict[method]
       if calc_class:
         calc_class.calc(gm=groundmodel, fg=footing)
         data = calc_class.data_to_dict()
         res = {"method":calc_class.method,
                "geom": footing["geom"],
                "loadcase": footing["loadcase"],
                "results": data}
         results.append(res)
   
   return results