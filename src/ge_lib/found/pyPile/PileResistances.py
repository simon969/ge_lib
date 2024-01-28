import numpy as np
import math
from .PileGeoms import Pile
from .EC7PartialFactors import unity_factors,resistance_factors_array, add_model_factor, get_factors
from .PileCalcs import StandardCalcs
import sys

standard_calc = StandardCalcs()

PILE_RESISTANCE_INCREMENT_DEFAULT = -0.5

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1", "on")

class PileResistance:

    def __init__(self, description: str , pile:Pile, gm, level_top:float, level_base:float , increment:float):
        self.description = description
        self.ground_model = gm
        self.pile = pile
        self.levels = np.arange(level_top, level_base, increment)
        self.undrained_qb = []
        self.undrained_qs = []
        self.drained_qb = []
        self.drained_qs = []
        
        if type(pile.calc_methods) is list:
            self.calc_methods = pile.calc_methods
        else:
            self.calc_methods =  pile.calc_methods.replace("'","").split(",")

        for s in self.calc_methods:
            calc = standard_calc.get_calc(s)
            if calc is not None:
                res = {"method":s,
                      "results": calc.calc(pile, gm, self.levels)}
                if (calc.component == "shaft" and calc.state == "undrained"):
                    self.undrained_qs.append(res)
                if (calc.component == "base" and calc.state == "undrained"):
                    self.undrained_qb.append(res)
                if (calc.component == "shaft" and calc.state == "drained"):
                    self.drained_qs.append(res)
                if (calc.component == "base" and calc.state == "drained"):
                    self.drained_qb.append(res)
        
        self.qs = self.get_qs(self.levels, self.undrained_qs,self.drained_qs)
        self.qb = self.get_qb(self.levels, self.undrained_qb,self.drained_qb)
    

        # if 'qs_cu_alpha' in pile.calc_methods:
        #     res = {"method":'qs_cu_alpha',
        #            "results": self.get_undrained_qs_cu_alpha(pile, gm, self.levels)}
        #     self.undrained_qs.append(res)

        # if 'qb_cu_nc' in self.pile.calc_methods:
        #     res = {"method":'qb_cu_nc',
        #            "results":self.get_undrained_qb_cu_nc(pile, gm, self.levels)}
        #     self.undrained_qb.append(res)

        # if 'qs_ks_tandelta_po' in pile.calc_methods:
        #     res = {"method":'qs_ks_tandelta_po',
        #            "results": self.get_drained_qs_ks_tandelta_po(pile, gm, self.levels)}
        #     self.drained_qs.append (res) 
        
        # if 'qb_reissner_po' in pile.calc_methods:
        #     res = {"method":'qb_reissner_po',
        #            "results":self.get_drained_qb_reissner(pile, gm, self.levels)}
        #     self.drained_qb.append (res)
        
        # if 'qb_nq_po' in pile.calc_methods:
        #     res = {"method":'qb_nq_po',
        #            "results":self.get_drained_qb_nq(pile, gm, self.levels)}
        #     self.drained_qb.append (res) 
        
        # if 'qb_sptn' in pile.calc_methods:
        #     res = {"method":'qb_sptn',
        #            "results":self.get_drained_qb_sptn(pile, gm, self.levels)}
        #     self.drained_qb.append (res) 
                       
       
    # def get_undrained_qs_cu_alpha(self, pile:Pile, gm:GroundModel, levels:float):
    #     res = [0.00] * levels.size
    #     alpha = pile.alpha
    #     for x in range(levels.size):
    #         res[x] = gm.get_attr_value(levels[x],"Cu",0.0) * alpha 
    #     return res
    # def get_undrained_qb_cu_nc(self, pile:Pile, gm:GroundModel, levels:float):
    #     res = [0.00] * levels.size
    #     nc = pile.nc
    #     for x in range(levels.size):
    #         res[x] = gm.get_attr_value(levels[x],"Cu",0)  * nc
    #     return res    
    # def get_drained_qs_ks_tandelta_po(self, pile:Pile, gm:GroundModel, levels:float):
    #     res = [0.00] * levels.size
    #     ks = pile.ks
    #     tan_delta =pile.tan_delta
    #     for x in range(levels.size):
    #         res[x] = gm.get_attr_value(levels[x],"EffectiveStress",0)  * ks * tan_delta 
    #     return res    
    def get_drained_qb_sptn_factor(self, pile:Pile, gm, levels:float):
        res = [0.00] * levels.size
        spt_factor = pile.spt_factor
        for x in range(levels.size):
            res[x] =  gm.get_attr_value(levels[x],"SPT",0)  * spt_factor
        return res
    def get_drained_qb_nq(self, pile:Pile, gm, levels:float):
        res = [0.00] * levels.size
        nq = pile.nq
        for x in range(levels.size):
            res[x] =  gm.get_attr_value(levels[x],"EffectiveStress",0)  * nq
        return res 
    def get_min_results(self, levels:float, results:[]):
        try:
            res = [0.00] * levels.size
            if (len(results) > 0):
                for x in range(levels.size): 
                    res[x] = sys.float_info.max
                    for res2 in results:
                        if (res2["results"][x] < res[x]):
                            res[x] = res2["results"][x]
            return res
        except Exception as e:
            msg = "problem getting min results {0}".format(str(e))
            print (msg)
    def get_min_results_zero_neg(self, levels:float, results:[]):
        try:
            res = [0.00] * levels.size
            if (len(results) > 0):
                for x in range(levels.size): 
                    res[x] = sys.float_info.max
                    for res2 in results:
                        if res2["results"][x] < 0:
                            res[x] = 0
                        else: 
                            if (res2["results"][x] < res[x]):
                                res[x] = res2["results"][x]
            return res
        except Exception as e:
            msg = "problem getting min results {0}".format(str(e))
            print (msg)

    def get_qs(self, levels:float, undrained_qs:[], drained_qs:[]):
        min_undrained_qs = self.get_min_results(levels, undrained_qs)
        min_drained_qs = self.get_min_results(levels, drained_qs)
        res = [0.00] * levels.size
        for x in range(levels.size):
            if (min_undrained_qs[x] == 0 and min_drained_qs[x]>0):
                res[x] = min_drained_qs[x]
            else:
                res[x] = min_undrained_qs[x]
        return res    
    def get_qb (self, levels:float, undrained_qb:[], drained_qb:[]):
        min_undrained_qb = self.get_min_results(levels, undrained_qb)
        min_drained_qb = self.get_min_results(levels, drained_qb)
        res = [0.00] * levels.size
        for x in range(levels.size):
            if (min_undrained_qb[x] == 0 and min_drained_qb[x]>0):
                res[x] = min_drained_qb[x]
            else:
                res[x] = min_undrained_qb[x]
        return res 
    
    
    def getResistances(self, factors = unity_factors):
        res = []
        qs = 0
        qb = 0 
     
        for x in range(self.levels.size): 
            qs =+ self.qs[x] * self.pile.perimeter 
            qb = self.qb[x] * self.pile.base
           
            r = {"level": self.levels[x],
                 "qs":qs,
                 "qb":qb,
                 "qus_comp": qs / (factors['shaft_comp']*factors['model']),
                 "qus_tens": qs / (factors['shaft_tens']*factors['model']),
                 "qub":  qb / (factors['base']*factors['model']),
                 "qutot": (qs + qb) / (factors['total']*factors['model'])}
            res.append(r)
        return res 
    def getResistancesJSON (self, factors):
        ret = []
        res = self.getResistances(factors)
        for r in res:
            s = "{{\"level\":{0}, \"qs\":{1}, \"qb\":{2}, \"qus_comp\":{3}, \"qub\":{4}, \"qus_tens\":{5}, \"qutot\":{6}}}".format(r['level'],r['qs'],r['qb'],r['qus_comp'],r['qub'],r['qus_tens'],r['qutot'])
            ret.append(s)
        return ret
    def getResistancesCSV (self, factors = unity_factors, include_header_in_rows = False, include_factors_in_rows = False):
        ret= []
        res = self.getResistances(factors)
        header = ["level","qs","qb","qus_comp","qub","qus_tens","qutot"]
        
        if (include_factors_in_rows):
            head,values =  resistance_factors_array(factors)
            ret.append(",".join(head))
            ret.append(",".join(values))

        if (include_header_in_rows):
            ret.append(','.join(header))
       
        for r in res:
            s = f"{r['level']},{r['qs']},{r['qb']},{r['qus_comp']},{r['qub']},{r['qus_tens']},{r['qutot']}"
            ret.append(s)
        return ','.join(header), ret
            
    def getDrainedResistances(self, factors = unity_factors):
        res = []
        qs = 0
        qb = 0
        for x in range(self.levels.size): 
            qs =+ self.drained_qs[x] * self.pile.perimeter  
            qb = self.drained_qb[x] * self.pile.base
            r = {"level": self.levels[x],
                 "qs":qs,
                 "qb":qb,
                 "qus_comp": qs / (factors['shaft_comp']*factors['model']),
                 "qus_tens": qs / (factors['shaft_tens']*factors['model']),
                 "qub":qb / (factors['base']*factors['model']),
                 "qutot":(qs + qb) / (factors['total']*factors['model'])}
            res.append(r)
        return res  
    def getUndrainedResistances(self, factors = unity_factors):
        res = []
        qs = 0
        qb = 0
        for x in range(self.levels.size):
            qs =+ self.undrained_qs[x] * self.pile.perimeter 
            qb = self.undrained_qb[x] * self.pile.base
            r = {"level": self.levels[x],
                 "qs":qs,
                 "qb":qb,
                "qus_comp": qs / (factors['shaft_comp']*factors['model']),
                "qus_tens": qs / (factors['shaft_tens']*factors['model']),
                "qub": qb / (factors['base']*factors['model']),
                "qutot": (qs + qb) / (factors['total']*factors['model'])}
            res.append(r)
        return res         
    def getDrainedResistancesJSON (self, factors = unity_factors):
        ret = []
        res = self.getDrainedResistances(factors)
        for r in res:
            s = {'level':r['level'], 'qs':r['qs'], 'qb':r['qb'], 'qus_comp':r['qus_comp'], 'qub':r['qub'], 'qus_tens':r['qus_tens'], 'qutot':r['qutot']}
            ret.append(s)
        return ret
    def getUndrainedResistancesJSON (self, factors = unity_factors):
        ret = []
        res = self.getUndrainedResistances(factors)
        for r in res:
            s = {'level':r['level'], 'qs':r['qs'], 'qb':r['qb'], 'qus_comp':r['qus_comp'], 'qub':r['qub'], 'qus_tens':r['qus_tens'], 'qutot':r['qutot']}
            ret.append(s)
        return ret
    def getDrainedResistancesCSV (self, factors = unity_factors, include_header_in_rows = False):
        ret= []
        res = self.getDrainedResistances(factors)
        header = ["level","qs","qb","qus_comp","qub","qus_tens","qutot"]
        if (include_header_in_rows):
            ret.append(','.join(header))
        for r in res:
            s = f"{r['level']},{r['qs']},{r['qb']},{r['qus_comp']},{r['qub']},{r['qus_tens']},{r['qutot']}"
            ret.append(s)
        return ','.join(header), ret
    
    def getUndrainedResistancesCSV (self, factors = unity_factors, include_header_in_rows = False):
        ret= []
        res = self.getUndrainedResistances(factors)
        header = ["level","qs","qb","qus_comp","qub","qus_tens","qutot"]
        if (include_header_in_rows):
            ret.append(','.join(header))
        for r in res:
            s = f"{r['level']},{r['qs']},{r['qb']},{r['qus_comp']},{r['qub']},{r['qus_tens']},{r['qutot']}"
            ret.append(s)
        return ','.join(header), ret


