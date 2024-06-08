import json
import os
import jsonschema

from .ground.GroundModel import GroundModel, ground_model_array
from .ground.GroundStresses import GroundStresses
from .ground.GroundStiffnesses import GroundStiffness
from .ground.GroundModelSupport import add_stresses_strength_stiffness
from .footing.FootingGeoms import footing_array, INCREMENT_DEFAULT, default_options
from .footing.EC7PartialFactors import m1_factors, m2_factors, states
from .footing.FootingCalcs import effective_footings, footing_resistance
from .schemas.Schemas import get_schema, registry

footing_schema = get_schema('footings_v4.json')


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
         
        validator = jsonschema.Draft7Validator(footing_schema, registry = registry)
        errors = validator.iter_errors(dic)  # get all validation errors
        error_msgs = []
        
        for error in errors:
            error_msgs.append(error.message)

        if len(error_msgs) > 0:
            raise ValueError (",".join(error_msgs)) 
                
        # ensure gm_data is an array 
        gm_data = []
        if 'ground_models' in dic.keys():
            gm_data = dic["ground_models"]
        if 'ground_model' in dic.keys():
            gm_data = [dic["ground_model"]]
        
        # ensure footing_data is an array
        footing_data = []
        if 'footings' in dic.keys():    
            footing_data = dic["footings"]
        if 'footing' in dic.keys():
            footing_data = [dic["footing"]]
        
    except Exception as e:
        msg  = {"data": data,
                "results":{},
                "errors": str(e),
                "status" : 422}
        return msg
    
    
    ground_models  = ground_model_array (gm_data, is_checked=False)
     
    footings = footing_array (data=footing_data, is_checked=False)

    data_ret = []
  
    for gm in ground_models:
        
        gm.copyStrataSet("_default","uls_c1", m1_factors)
        gm.copyStrataSet("_default","uls_c2", m2_factors)
        gm_dic = gm.to_dict()

        gm.collectStrataSet(['uls_c1']) 
        gm_m1 = add_stresses_strength_stiffness(gm)

        gm.collectStrataSet(['uls_c2'])
        gm_m2 = add_stresses_strength_stiffness(gm)
 
        
        if footings is not None:
            
            footing_res = []

            for footing in footings: 
                geoms = footing.geoms
                loadcases = footing.loadings
                options = footing.options
                conc_density = options.get("conc_density", 0.0)
                eff_footings =  effective_footings(geoms = geoms, 
                                                  loadcases = loadcases, 
                                                  conc_dens= conc_density)
                methods = options.get("methods")
                
                for ef in eff_footings:
                    if (ef['state'] in states["set_b"]):
                        foot_res = footing_resistance (ef, gm_m1, methods)
                    if (ef['state']  in states["set_c"]):
                        res = footing_resistance(ef, gm_m2, methods)
                    if (ef['state']  in states["sls"]):
                        res = footing_resistance(ef, gm_m1, methods)
                    if not res is None:
                        res_obj = {"state":ef['state'],
                                   "results": res}
                        footing_res.append(res_obj)
            ground_res = {"ground_model": gm.description,
                          "results": footing_res}
        
        data_ret.append(ground_res)

    if format_return == "json":
        data_json = json.dumps(data_ret)
        return data_json
    else: 
        return data_ret
 
 
