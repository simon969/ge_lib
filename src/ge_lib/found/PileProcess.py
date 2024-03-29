import json

from .pyGround.GroundModel import ground_model_array
from .pyGround.GroundStresses import GroundStresses
from .pyGround.GroundStiffnesses import GroundStiffness
from .pyGround.GroundModelSupport import add_stresses_strength_stiffness
from .pyPile.PileResistances import PileResistance, PILE_RESISTANCE_INCREMENT_DEFAULT
from .pyPile.PileSettlement import PileSettlement, STANDARD_STEPS
from .pyPile.PileGeoms import CircularPile, pile_array
from .pyPile.EC7PartialFactors import get_ec7_pile_factors, unity_factors



def process_request(data, format_return) :
    """
    arguments:
        data: 
            json string or dictionary object containing ground model and pile array
        format_return: 
            "json", "dict"
    return:
        returns json string or dictionary object with original data and additional results array
    """
    
    try:
        if isinstance(data, dict):
            dic = data
        else :
            dic = json.loads(data)
        
        if 'ground_models' in dic.keys():
            gm_data = dic["ground_models"]
        if 'ground_model' in dic.key():
            gm_data = [dic["ground_model"]]

        pile_data = dic["pile_set"]
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
    
    ground_models  = ground_model_array (gm_data, is_checked=False)
        
    piles = pile_array(data=pile_data["piles"], is_checked=False)
    
    results = []

    for gm in ground_models:
        pile_resist = []
        pile_settle = []

        if gm is not None:
            gm.collectStrataSet(['_default'])
            gm_pile = add_stresses_strength_stiffness(gm)
            min_level = gm_pile.minLevelBaseStrataSet()
            max_level = gm_pile.maxLevelTopStrataSet()
            gm_increment = gm_pile.__dict__.get("increment",PILE_RESISTANCE_INCREMENT_DEFAULT)
            description = "{0} groundmodel sampled from {1} to {2} in {3} steps".format(gm_pile.description, max_level, min_level, gm_increment)
            
            gs = GroundStresses (description, gm_pile, max_level, min_level, gm_increment)
            gs_res = gs.getStressesJSON()
            gs_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gs_res)) 
            
            gstiff = GroundStiffness (description, gm_pile, max_level, min_level, gm_increment)
            gstiff_res = gstiff.getStiffnessJSON()
            gstiff_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gstiff_res)) 
            
            if piles is not None:
                for pile in piles: 
                    cut_off_level = pile.__dict__.get("cut_off_level",max_level)
                    increment = pile.__dict__.get("increment",gm_increment)
                    description = "{0} pile with {1} groundmodel sampled from {2} to {3} in {4} steps".format(pile.description, gm_pile.description, cut_off_level, min_level, increment)
                    
                    pr = PileResistance (description, pile, gm_pile, cut_off_level, min_level, -0.5)
                    pile_factors = get_ec7_pile_factors(pile)
                    if pile_factors is None:
                        pile_factors = unity_factors
                    res = pr.getResistancesJSON(pile_factors)
                    result = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(pile.description, ",".join(res))
                    pile_resist.append (result)

                    res_sls = pr.getResistances(unity_factors)

                    ps = PileSettlement(description, pile, gm_pile, res_sls, steps=STANDARD_STEPS)
                    set = ps.getSettlementProfilesJSON()
                    result = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(pile.description, ",".join(set))
                    pile_settle.append(result)
                    
            pile_resist_json = "{{\"results\":[{0}]}}".format(",".join(pile_resist))
            pile_settle_json = "{{\"results\":[{0}]}}".format(",".join(pile_settle))
            data_ret = {
                        "ground_model":gm.to_dict(),
                        "pile_set":pile_data,
                        }

    if format_return == "json":
        data_json = json.dumps(data_ret)
        all_json =  data_json[0:-1] + ",\"ground_stresses\":{0},\"ground_stiffness\":{1},\"pile_resistances\":{2},\"pile_settlements\":{3}}}".format(gs_json, gstiff_json, pile_resist_json, pile_settle_json)
        results.append(all_json)
    else: 
        data_ret["pile_resistances"] = json.loads(pile_resist_json)
        data_ret["pile_settlements"] = json.loads(pile_settle_json)
        data_ret["ground_stresses"] = json.loads(gs_json)
        data_ret["ground_stiffness"] = json.loads(gstiff_json)
        results.append(data_ret)
    
    return results

