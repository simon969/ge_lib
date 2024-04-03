import json
import jsonschema

from .ground.GroundModel import ground_model_array
from .ground.GroundStresses import GroundStresses
from .ground.GroundStiffnesses import GroundStiffness
from .ground.GroundModelSupport import add_stresses_strength_stiffness
from .pile.PileResistances import PileResistance, PILE_RESISTANCE_INCREMENT_DEFAULT
from .pile.PileSettlement import PileSettlement, STANDARD_STEPS
from .pile.PileGeoms import CircularPile, pile_array, pileset_array
from .pile.EC7PartialFactors import get_ec7_pile_factors, unity_factors
from .schemas.Schemas import get_schema, registry

default_results = ['ground_stresses','pile_resistances','pile_settlements']

pile_schema = get_schema('piles_v4.json')

def process_request(data, format_return) :
    """
    arguments:
    ----------
        data: 
            json string or dictionary object containing ground model and pile array
        format_return: 
            "json", "dict"

    returns:
    --------
        returns json string or dictionary object with original data and additional results array
    """
    
    try:
        if isinstance(data, dict):
            dic = data
        else :
            dic = json.loads(data)
        
        validator = jsonschema.Draft7Validator(pile_schema, registry = registry)
        errors = validator.iter_errors(dic)  # get all validation errors
        error_msgs = []
        
        for error in errors:
            error_msgs.append(error.message)

        if len(error_msgs) > 0:
            raise ValueError (",".join(error_msgs)) 
        
        # ensure gm_data is an array with ids
        gm_data = []
        if 'ground_models' in dic.keys():
            gm_data = dic["ground_models"]
        if 'ground_model' in dic.keys():
            gm_data = [dic["ground_model"]]
        
        # ensure pile_data is an array with ids
        pile_data = []
        if 'pile_sets' in dic.keys():
            pile_data = dic["pile_sets"]
        if 'pile_set' in dic.keys():
            pile_data = [dic["pile_set"]]
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
    
    ground_models  = ground_model_array (gm_data, is_checked=False)
    
    pile_sets = pileset_array (pile_data, is_checked=False)

    ground_results = []
    ground_stress = []
    ground_stiffness = []
    pile_resist = []
    pile_settle = []

    for gm in ground_models:

        gm.collectStrataSet(['_default'])
        gm_pile = add_stresses_strength_stiffness(gm)
        min_level = gm_pile.minLevelBaseStrataSet()
        max_level = gm_pile.maxLevelTopStrataSet()
        gm_increment = gm_pile.__dict__.get("increment",PILE_RESISTANCE_INCREMENT_DEFAULT)
        description = "{0} groundmodel sampled from {1} to {2} in {3} steps".format(gm_pile.description, max_level, min_level, gm_increment)
        
        gstress = GroundStresses (description, gm_pile, max_level, min_level, gm_increment)
        gstress_res = gstress.getStressesJSON()
        # gstress_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gs_res)) 
        gstress_json = "{{\"ground_model\":\"{0}\",\"results\":[{1}]}}".format(gm.description + "("+ gm.id + ")", ",".join(gstress_res)) 
        ground_stress.append (gstress_json)
        
        gstiff = GroundStiffness (description, gm_pile, max_level, min_level, gm_increment)
        gstiff_res = gstiff.getStiffnessJSON()
        # gstiff_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gstiff_res))
        gstiff_json = "{{\"ground_model\":\"{0}\",\"results\":[{1}]}}".format(gm.description + "("+ gm.id + ")", ",".join(gstiff_res)) 
        ground_stiffness.append(gstiff_json)

        ground_json = "{{\"ground_model\":\"{0}\",\"ground_stiffness\":[{1}],\"ground_stiffness\":[{2}]}}".format(gm.description + "("+ gm.id + ")",",".join(gstress_res),",".join(gstiff_res))
        ground_results.append(ground_json)

        for pile_set in pile_sets:
           
            for pile in pile_set.piles: 
                cut_off_level = pile.__dict__.get("cut_off_level",max_level)
                increment = pile.__dict__.get("increment",gm_increment)
                description = "{0} pile with {1} groundmodel sampled from {2} to {3} in {4} steps".format(pile.description, gm_pile.description, cut_off_level, min_level, increment)
                
                pr = PileResistance (description, pile, gm_pile, cut_off_level, min_level, -0.5)
                pile_factors = get_ec7_pile_factors(pile)
                if pile_factors is None:
                    pile_factors = unity_factors
                res = pr.getResistancesJSON(pile_factors)
                # result = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(pile.description, ",".join(res))
                result = "{{\"ground_model\":\"{0}\",\"pile_set\":\"{1}\",\"pile\":\"{2}\",\"results\":[{3}]}}".format(gm.description + "(" + gm.id +")", pile_set.description + "(" + pile_set.id + ")", pile.description + "(" + pile.id + ")", ",".join(res))
                pile_resist.append (result)

                res_sls = pr.getResistances(unity_factors)

                ps = PileSettlement(description, pile, gm_pile, res_sls, steps=STANDARD_STEPS)
                set = ps.getSettlementProfilesJSON()
                # result = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(pile.description, ",".join(set))
                result = "{{\"ground_model\":\"{0}\",\"pile_set\":\"{1}\",\"pile\":\"{2}\",\"results\":[{3}]}}".format(gm.description + "(" + gm.id +")", pile_set.description + "(" + pile_set.id + ")", pile.description + "(" + pile.id + ")", ",".join(res))
                pile_settle.append(result)
                
                # pile_resist_json = "{{[{0}]}}".format(",".join(pile_resist))
                # pile_settle_json = "{{[{0}]}}".format(",".join(pile_settle))
                # data_ret = {
                #             "pile_resistance": pile_resist_json,
                #             "pile_settlements": pile_settle_json,
                #             }
        # if format_return == "json":
        #     data_json = json.dumps(data_ret)
        #     # all_json =  data_json[0:-1] + ",\"ground_stresses\":{0},\"ground_stiffness\":{1},\"pile_resistances\":{2},\"pile_settlements\":{3}}}".format(gs_json, gstiff_json, pile_resist_json, pile_settle_json)
        #     pile_results.append(data_json)
        # else: 
        #     data_ret["pile_resistances"] = json.loads(pile_resist_json)
        #     data_ret["pile_settlements"] = json.loads(pile_settle_json)
        #     pile_results.append(data_ret)
   
   
    results = { 
                "ground_stress": ground_stress,
                "ground_stiffness": ground_stiffness,                   
                "pile_settle": pile_settle,
                "pile_resist": pile_resist
            }

    return results

