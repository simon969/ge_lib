import json
import os
import jsonschema
from .schemas.Schemas import get_schema
from .section_props.SectionProperties import SectionProperties

schema = get_schema ("section_props_array_v1.json")

def process_request(data, format_return) :
    """
    arguments:
    ----------
        data: 
            dict object or json string containing array geometry name, coordinates and units
        format_return: 
            "json", "dict"

    returns:
    --------
        returns json string or dictionary object with original data and additional results array
    """
    
    try:
        if isinstance(data, dict):
            json_data = json.dumps([data])
        else:
            if  hasattr(data, "__len__") and not isinstance(data,str):
                json_data = json.dumps(data)
            else:
                json_data = data
        
        dic = json.loads(json_data)
        
        if hasattr(dic, "__len__"):
            dic_arr = dic
        else:
            dic_arr = [dic]
        
        validator = jsonschema.Draft7Validator(schema)
        errors = validator.iter_errors(dic)  # get all validation errors
        err_arr = []
        for error in sorted(errors, key=str):
                err = "{{\"message\":\"{0}\",\"path\":\"{1}\"}}".format(error.message,error.path)
                err_arr.append(err)
        if len(err_arr)>0:
            err_str = json.dumps(err_arr)
            raise Exception(err_str)
 
        sp =  SectionProperties()
        
        results = []

        for d in dic_arr:
            values, symbols, description, units = sp.calc_props(d)
            result = {"data":d,
                        "symbols":symbols,
                        "description":description,
                        "units": units,
                        "values":values}
            results.append(result)
        
        if format_return == "json":
            return json.dumps(results)
        else:
            return results
    
    except Exception as e:
        msg  = {"data": data,
                "results":{},
                "errors": str(e),
                "status" : 400}
        return msg