import json

from found.pyGround.GroundModel import GroundModel
from found.pyGround.GroundStresses import GroundStresses
from found.pyGround.GroundStiffnesses import GroundStiffness
from found.pyGround.GroundModelSupport import addStressesStrengthStiffness
from found.pyPile.PileResistances import PileResistance, PILE_RESISTANCE_INCREMENT_DEFAULT
from found.pyPile.PileSettlement import PileSettlement, STANDARD_STEPS
from found.pyPile.PileGeoms import CircularPile, GetPileArray
from found.pyPile.EC7PartialFactors import get_ec7_pile_factors, unity_factors



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
        
        gm_data = dic["ground_model"]
        pile_data = dic["pile_set"]
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
    

    gm = GroundModel (gm_data, is_checked=False)
        
    piles = GetPileArray (data=pile_data["piles"])
    pile_resist = []
    pile_settle = []

    if gm is not None:
        gm.collectStrataSet(['_default'])
        gm_pile = addStressesStrengthStiffness(gm)
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
        return all_json
    else: 
        data_ret["pile_resistances"] = json.loads(pile_resist_json)
        data_ret["pile_settlements"] = json.loads(pile_settle_json)
        data_ret["ground_stresses"] = json.loads(gs_json)
        data_ret["ground_stiffness"] = json.loads(gstiff_json)
        return data_ret
