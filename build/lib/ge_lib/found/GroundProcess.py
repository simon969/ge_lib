import json
import jsonschema
from .ground.GroundModel import GroundModel
from .ground.GroundStresses import GroundStresses
from .ground.GroundStiffnesses import GroundStiffness
from .ground.GroundModelSupport import add_stresses_strength_stiffness, INCREMENT_DEFAULT
from .schemas.Schemas import get_schema, registry, get_schema_full

ground_model_schema = get_schema('ground_models_v4.json')

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
        
        validator = jsonschema.Draft7Validator(ground_model_schema, registry = registry)
        errors = validator.iter_errors(dic)  # get all validation errors
        
        for error in errors:
            print (error)
            print('------')
       
        # ensure gm_data is an array 
        gm_data = []
        if 'ground_models' in dic.keys():
            gm_data = dic["ground_models"]
        if 'ground_model' in dic.keys():
            gm_data = [dic["ground_model"]]
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
    
    results = []

    for gm_d in gm_data:

        gm = GroundModel (gm_d, is_checked=False)
            
        if gm is not None:
            gm.collectStrataSet(['_default'])
            gm_pile = add_stresses_strength_stiffness(gm)
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
            results.append(all_json)
        else: 
            data_ret["ground_stresses"] = json.loads(gs_json)
            data_ret["ground_stiffness"] = json.loads(gstiff_json)
            results.append(data_ret)
    
    return results
