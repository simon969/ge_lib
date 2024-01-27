
from found.pyGround.Support import str2bool

unity_factors = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.0, "model":1.0}

# Tables A.NA.8 Partial resistance factors (gr) for continuous flight auger (cfa) piles for STR and GEO limit states
#cfa uls combination 1 and 2
r1_factors_cfa = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.0}
r2_factors_cfa = {"shaft_comp":1.1, "base":1.1, "total":1.1, "shaft_tens":1.15}
r3_factors_cfa = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.1}
r4_factors_cfa = {"shaft_comp":1.6, "base":2.0, "total":2.0, "shaft_tens":2.0}
r4_factors_cfa_withSLScheck = {"shaft_comp":1.4, "base":1.7, "total":1.7, "shaft_tens":1.7}

# Tables A.NA.6 Partial resistance factors (gr) for driven piles for STR and GEO limit states
#driven uls combination 1 and 2
r1_factors_driven = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.0}
r2_factors_driven = {"shaft_comp":1.1, "base":1.1, "total":1.1, "shaft_tens":1.15}
r3_factors_driven = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.1}
r4_factors_driven = {"shaft_comp":1.6, "base":2.0, "total":2.0, "shaft_tens":2.0}
r4_factors_driven_withSLScheck = {"shaft_comp":1.7,"base":1.7, "total":1.0, "shaft_tens":1.0}

# Tables A.NA.7 Partial resistance factors (gr) for bored piles for STR and GEO limit states
#bored uls combination 1 and 2
r1_factors_bored = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.0}
r2_factors_bored =  {"shaft_comp":1.1, "base":1.1, "total":1.1, "shaft_tens":1.15}
r3_factors_bored = {"shaft_comp":1.0, "base":1.0, "total":1.0, "shaft_tens":1.1}
r4_factors_bored = {"shaft_comp":1.6, "base":2.0, "total":2.0, "shaft_tens":2.0}
r4_factors_bored_withSLScheck = {"shaft_comp":1.4, "base":1.7, "total":1.7, "shaft_tens":1.7}

model_factor_unity = {"model":1.0}
model_factor_no_load_test = {"model":1.4}
model_factor_with_load_test =  {"model" :1.2}

EC7_PartialFactors = {
     
    "r1_factors_cfa":r1_factors_cfa,
    "r2_factors_cfa":r2_factors_cfa,
    "r3_factors_cfa":r3_factors_cfa,
    "r4_factors_cfa":r4_factors_cfa,
    "r4_factors_cfa_withSLScheck":r4_factors_cfa_withSLScheck,

    "r1_factors_driven":r1_factors_driven,
    "r2_factors_driven":r2_factors_driven,
    "r3_factors_driven":r3_factors_driven,
    "r4_factors_driven":r4_factors_driven,
    "r4_factors_driven_withSLScheck":r4_factors_driven_withSLScheck,

    "r1_factors_bored":r1_factors_bored,
    "r2_factors_bored":r2_factors_bored,
    "r3_factors_bored":r3_factors_bored,
    "r4_factors_bored":r4_factors_bored,
    "r4_factors_bored_withSLScheck":r4_factors_bored_withSLScheck,
    
    "unity_factors":unity_factors

    }
def get_factors (name:str):
    name = name.lower()
    return EC7_PartialFactors.get(name, unity_factors)

def add_model_factor(factor_set, piletest = False):
    factors = factor_set
    model_factor = model_factor_no_load_test
    if (piletest==True):
        model_factor = model_factor_with_load_test
    factors['model'] = model_factor['model']
    return factors
def resistance_factors_array(factors):
        header = ["resistance","shaft_comp","shaft_tens","base","total","model"]
        values = [factors['shaft_comp'],factors['shaft_tens'],factors['base'],factors['total'],factors['model']]
        return header, values
def get_ec7_pile_factors(pile):
       
        factors = None
        if (hasattr(pile,'factors')):
            factors = pile.factors 
        else:
            if (hasattr(pile,'code_factors')):
                factors = get_factors(pile.code_factors) 
            else: 
                if (hasattr(pile,'pile_type')):
                    s = "r4_factors_{0}".format(pile.pile_type)
                if (hasattr(pile,'sls_check')):
                    if (str2bool(pile.sls_check)):
                        s += "_withSLScheck" 
                factors = get_factors(s)
                if (hasattr(pile,"pile_test")):
                    factors = add_model_factor(factors,str2bool(pile.pile_test))
        return factors