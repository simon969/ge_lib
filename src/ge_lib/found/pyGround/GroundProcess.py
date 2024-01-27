import json

from ge_lib.found.pyGround.GroundModel import GroundModel
from ge_lib.found.pyGround.GroundStresses import GroundStresses
from ge_lib.found.pyGround.GroundStiffnesses import GroundStiffness
from ge_lib.found.pyGround.GroundModelSupport import addStressesStrengthStiffness, INCREMENT_DEFAULT




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
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
   

    gm = GroundModel (gm_data, is_checked=False)
        
    if gm is not None:
        gm.collectStrataSet(['_default'])
        gm_pile = addStressesStrengthStiffness(gm)
        min_level = gm_pile.minLevelBaseStrataSet()
        max_level = gm_pile.maxLevelTopStrataSet()
        gm_increment = gm_pile.__dict__.get("increment",INCREMENT_DEFAULT)
        description = "{0} groundmodel sampled from {1} to {2} in {3} steps".format(gm_pile.description, max_level, min_level, gm_increment)
        
        gs = GroundStresses (description, gm_pile, max_level, min_level, gm_increment)
        gs_res = gs.getStressesJSON()
        gs_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gs_res)) 
        
        gstiff = GroundStiffness (description, gm_pile, max_level, min_level, gm_increment)
        gstiff_res = gstiff.getStiffnessJSON()
        gstiff_json = "{{\"description\":\"{0}\",\"results\":[{1}]}}".format(gm.description, ",".join(gstiff_res)) 
        
        data_ret = {
                    "ground_model":gm.to_dict()
                    }

    if format_return == "json":
        data_json = json.dumps(data_ret)
        all_json =  data_json[0:-1] + ",\"ground_stresses\":{0},\"ground_stiffness\":{1}}}".format(gs_json, gstiff_json)
        return all_json
    else: 
        data_ret["ground_stresses"] = json.loads(gs_json)
        data_ret["ground_stiffness"] = json.loads(gstiff_json)
        return data_ret
