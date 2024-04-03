
## A.3.2 Partial factors for soil parameters (gM)
## Table A.NA.4 - Partial factors for soil parameters (gM) for the STR and GEO limit states
m1_factors  = {"phi":1.0,"cohesion":1.0, "undrained_shear":1.0, "unconfined_strength":1.0,"density":1.0}
m2_factors  = {"phi":1.25,"cohesion":1.25, "undrained_shear":1.4, "unconfined_strength":1.4,"density":1.0}

states = {'set_b':['set_b','uls_c1'],
          'set_c':['set c','uls_c2'],
          'sls': ['sls']
          }

def material_factors_array (factors):
        header = ["phi","cohesion","undrained_shear","unconfined_strength","density"]
        values = [factors['phi'],factors['cohesion'],factors['undrained_shear'],factors['unconfined_strength'],factors['density']]
        return header, values   