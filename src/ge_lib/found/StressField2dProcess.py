import json
import os
import jsonschema
from .schemas.Schemas import get_schema, registry

stress_field_schema = get_schema ("stress_field2d_v1.json")

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
        
        validator = jsonschema.Draft7Validator(stress_field_schema, registry = registry)
        errors = validator.iter_errors(dic)  # get all validation errors
        if errors:
            for error in errors:
                print (error)
                print('------')
            raise Exception(errors)
        
    except Exception as e:
        msg  = {"data": data,
                "results":{},
                "errors": str(e),
                "status" : 400}
        return msg