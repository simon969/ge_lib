import json

from found.pyGround.GroundModel import GroundModel
from found.pyGround.GroundStresses import GroundStresses
from found.pyGround.GroundStiffnesses import GroundStiffness
from found.pyGround.GroundModelSupport import addStressesStrengthStiffness
from found.pyFooting.FootingGeoms import footing_array, INCREMENT_DEFAULT, default_options
from found.pyFooting.EC7PartialFactors import m1_factors, m2_factors, states
from found.pyFooting.FootingCalcs import effective_footings, footing_resistance

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
        footing_data = dic["footings"]
    
    except Exception as e:
        msg  = {"error": str(e),
                "status" : 400}
        return msg
    
    
    gm = GroundModel (gm_data, is_checked=False)
    
    footings = footing_array (data=footing_data, is_checked=False)

    footings_resist = []
  
    if gm is not None:
        
        gm.copyStrataSet("_default","uls_c1", m1_factors)
        gm.copyStrataSet("_default","uls_c2", m2_factors)
        gm_dic = gm.to_dict()

        gm.collectStrataSet(['uls_c1']) 
        gm_m1 = addStressesStrengthStiffness(gm)
        res_uls_c1 = []
        res_sls = []

        gm.collectStrataSet(['uls_c2'])
       
        gm_m2 = addStressesStrengthStiffness(gm)
        res_uls_c2 = []
 
        if footings is not None:
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
                        res = footing_resistance (ef, gm_m1, methods)
                        res_uls_c1.append(res)
                    if (ef['state']  in states["set_c"]):
                        res = footing_resistance(ef, gm_m2, methods)
                        res_uls_c2.append(res)
                    if (ef['state']  in states["sls"]):
                        res = footing_resistance(ef, gm_m1, methods)
                        res_sls.append(res)
        
        data_ret = {
                        "ground_model": gm_dic,
                        "uls_c1": res_uls_c1,
                        "uls_c2": res_uls_c2,
                        "sls": res_sls
                        
                    }

    if format_return == "json":
        data_json = json.dumps(data_ret)
        return data_json
    else: 
        return data_ret
 
 
