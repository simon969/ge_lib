import math
from .Support import calc, calc_collection


class StandardCalcs(calc_collection):
     def __init__(self):
        super().__init__(id= '01', description='standard pile calc library',version='p01.1')
        self.append_calc(KsTandDeltaPo())
        self.append_calc(NqPo())
        self.append_calc(SPTFactor())
        self.append_calc(AlphaCu())
        self.append_calc(NcCu())
        self.append_calc(Nq_Reissner())
        # self.append_calc(Ng_Brinch_Hansen())
        # self.append_calc(Ng_Vesic())
        # self.append_calc(Ng_Meyerhof())
        # self.append_calc(Ng_Chen())
        # self.append_calc(Nc_Prandtl())

def min_width(pile):
        dia = pile.__dict__.get("diameter", None)
        breadth = pile.__dict__.get("breadth", None)
        if dia is not None:
             return dia
        if breadth is not None:
             return breadth

class SPTFactor (calc):
    def __init__(self):
        super().__init__(id='qb_spt', 
                         description='Calculation of end bearing using user provided spt factor and average SPT N value at toe level and at 2x min pile width below', 
                         reference = 'Standard UK effective stress calculation for end bearing derived from insitu spt n values', 
                         state = 'drained', 
                         component='base',
                         version = "p01.1")
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        spt_factor = pile.spt_factor
        dia =  min_width(pile)
        for x in range(levels.size):
            SPTtoe = gm.get_attr_value(levels[x], "SPT",0) 
            SPTbelow = gm.get_attr_value(levels[x]-2*dia, "SPT",0) 
            res[x] = (SPTtoe+SPTbelow) / 2 * spt_factor
        return res

class KsTandDeltaPo (calc):
    def __init__(self):
        super().__init__(id='qs_ks_tandelta_po', 
                         description='Calculation of shaft friction using lateral stress factor Ks, friction and factor TanDelta and vertical effective stress Po', 
                         reference = 'Standard UK effective stress calculation for shaft friction', 
                         state = 'drained', 
                         component='shaft',
                         version = 'p01.1')
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        ks = pile.ks
        tan_delta =pile.tan_delta
        for x in range(levels.size):
            res[x] = gm.get_attr_value(levels[x],"EffectiveStress",0)  * ks * tan_delta 
        return res
     
class NqPo (calc):
    def __init__(self):
        super().__init__(id='qb_nq_po', 
                         description='Calculation of end bearing using user provided Nq and vertical effective stress Po', 
                         reference = 'Standard UK effective stress calculation for end bearing', 
                         state = 'drained', 
                         component='base',
                         version = 'p01.1')
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        nq = pile.nq
        for x in range(levels.size):
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res 

class AlphaCu (calc):
    def __init__(self):
        super().__init__(id='qs_alpha_cu', 
                         description='Calculation of shaft friction using adhesion factor Alpha and undrained shear strength Cu', 
                         reference = 'Standard UK total stress calculation for shaft friction', 
                         state = 'undrained', 
                         component='shaft',
                         version='p01.1')
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        alpha = pile.alpha
        for x in range(levels.size):
            res[x] = gm.get_attr_value(levels[x],"Cu",0.0) * alpha 
        return res
class NcCu (calc):
    def __init__(self):
        super().__init__(id='qb_nc_cu', 
                         description='Calculation of end bearing using shape factor Nc and undrained shear strength Cu', 
                         reference = 'Standard UK total stress calculation for end bearing', 
                         state = 'undrained', 
                         component='base',
                         version='p01.1')
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        nc = pile.nc
        for x in range(levels.size):
            res[x] = gm.get_attr_value(levels[x],"Cu",0)  * nc
        return res 
    
def calc_Ng_Brinch_Hansen(nq, phi_rad):
        '''
        ==========================================================================================

       Calculation of Ng after Brinch-Hansen
        Brinch-Hasen, J. (1970) A revised and extended formula for bearing capacity,
        Danish Geotechnical Institute , Bulletin No 28, 6pp

        ==========================================================================================
        '''
        nq = 1.5 * (nq - 1) * math.tan(phi_rad)
        return nq 

class Ng_Brinch_Hansen (calc):
    def __init__(self):
        super().__init__(id='qb_brinch_hansen', 
                         description='Calculation of end bearing qb using Ng after Brinch-Hansen', 
                         reference = 'Calcualtion of Ng after Brinch-Hansen, Brinch-Hasen, J. (1970) A revised and extended formula for bearing capacity, Danish Geotechnical Institute , Bulletin No 28, 6pp', 
                         state = 'drained', 
                         component='base',
                         version='p01.1')
    
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)
            ng = calc_Ng_Brinch_Hansen(math.radians(phi_deg))
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res
def calc_Ng_Vesic (nq, phi_rad):
        '''
        ==========================================================================================
        
       Calculation of Ng after Vesic
        Vesic, A. S (19730 'Analysis of ultimate loads of shallow foundations'
        Journal of Soil Mechanics Foundation Division, American Society of Civil Engineers 99(1) pp 45-73

        ==========================================================================================
        '''
        ng = 2 * (nq + 1) * math.tan(phi_rad)
        return ng

class Ng_Vesic (calc):
    def __init__(self):
        super().__init__(id='qb_vesic', 
                         description='Calculation of end bearing qb using Ng after Vesic', 
                         reference = 'Calculation of Ng after Vesic, Vesic, A. S (1973) Analysis of ultimate loads of shallow foundations Journal of Soil Mechanics Foundation Division, American Society of Civil Engineers 99(1) pp 45-73', 
                         state = 'drained', 
                         component='base',
                         version='p01.1')
   
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)

            ng = calc_Ng_Vesic(math.radians(phi_deg))
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * ng
        return res

def calc_Ng_Meyerhof (nq, phi_rad):
        '''
        ==========================================================================================

        Calculation of Ng after Meyerhof
        Meyerhof, G. G 'Some recent research on the bearing capacity of foundations'
        Canadian Geotechnical Journal 1(1) pp 16-26

        ==========================================================================================
        '''
        ng = (nq - 1) * math.tan(phi_rad)
        return ng

class Ng_Meyerhof (calc):
    def __init__(self):
        super().__init__(id='qb_vesic', 
                         description='Calculation of end bearing qb using Ng after Vesic', 
                         reference = 'Calculation of Ng after Meyerhof Meyerhof, G. G Some recent research on the bearing capacity of foundations Canadian Geotechnical Journal 1(1) pp 16-26', 
                         state = 'drained', 
                         component='base',
                         version='p01.1')
   
    
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)
            nq = calc_Ng_Meyerhof(math.radians(phi_deg))
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res
def calc_Ng_Chen(nq, phi_rad):
        '''
        ==========================================================================================
        
        Calculation of Ng after Chen
        Chen W.F (1975) Limit analysis and soil plasticity, Elsevier
        
        ==========================================================================================
        '''
        
        ng = 2 * (nq - 1) * math.tan(phi_rad)
        return ng

class Ng_Chen (calc):
    def __init__(self):
        super().__init__(id='qb_chen', 
                         description='Calculation of end bearing qb using Ng after Chen', 
                         reference = 'Calculation of Ng after Vesic, Vesic, A. S (1973) Analysis of ultimate loads of shallow foundations Journal of Soil Mechanics Foundation Division, American Society of Civil Engineers 99(1) pp 45-73', 
                         state = 'drained', 
                         component='base',
                         version='p01.1')
    
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)
            nq = calc_Ng_Chen(math.radians(phi_deg))
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res

def calc_Nq_Reissner(phi_rad):
        '''
        ==========================================================================================

        Calculation of Nq after Reissner
        Reissner, H (1924) 'Zum Erddruckproblem'
        1st Inetrnational Conference on Applied Mechanics, Delft, pp.295-311

        ==========================================================================================
        '''
        nq = math.exp(math.pi * math.tan(phi_rad)) * math.tan(math.pi / 4 + phi_rad / 2) ^ 2
        return nq

class Nq_Reissner (calc):
    def __init__(self):
        super().__init__(id='qb_reissner', 
                         description='Calculation of end bearing qb using Nq after Reissner', 
                         reference = 'Calculation of Nq after Reissner Reissner, H (1924) Zum Erddruckproblem 1st Inetrnational Conference on Applied Mechanics, Delft, pp.295-311', 
                         state = 'drained', 
                         component='base',
                         version= 'p01.1')    

    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)
            nq = calc_Nq_Reissner(math.radians(phi_deg))
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res

def calc_Nc_Prandtl (nq, phi_rad):
        '''
        ==========================================================================================
        
        Calculation of Nc after Prandtl
        Prandtl L (1921) 'Uber die Eidringgungfestigkeit plastisher Baustoffe und die Festigkeit von Schneiden
        Zeitsch, Angew. Mathematik und Mechanik, 1,15-20
        
        ==========================================================================================
        '''
        nc = (nq - 1) / math.tan(phi_rad)
        return nc

class Nc_Prandtl(calc):
    def __init__(self):
        super().__init__(id='qb_prandtl', 
                         description='Calculation of end bearing qb using Nc after Prandtl', 
                         reference = 'Calculation of Nc after Prandtl Prandtl L (1921) Uber die Eidringgungfestigkeit plastisher Baustoffe und die Festigkeit von Schneiden Zeitsch, Angew. Mathematik und Mechanik, 1,15-20', 
                         state = 'undrained', 
                         component='base',
                         version = 'p01.1')
    
    def calc(self, pile, gm, levels):
        res = [0.00] * levels.size
        for x in range(levels.size):
            phi_deg = gm.get_attr_value(levels[x],"phi_deg",0)
            nq = calc_Nq_Reissner (phi_deg)
            nc = calc_Nc_Prandtl (nq, phi_deg)
            res[x] = gm.get_attr_value(levels[x],"Cu",0)  * nc
        return res 