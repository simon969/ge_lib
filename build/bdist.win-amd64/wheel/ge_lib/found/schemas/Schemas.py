import os
import json
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
from referencing.jsonschema import DRAFT202012
from ge_lib.shared.shared import json_objs

# SCHEMAS = Path("/tmp/yaml-schemas")

# def retrieve_yaml(uri: str):
#     if not uri.startswith("http://localhost/"):
#         raise NoSuchResource(ref=uri)
#     path = SCHEMAS / Path(uri.removeprefix("http://localhost/"))
#     contents = yaml.safe_load(path.read_text())
#     return Resource.from_contents(contents)

#     registry = Registry(retrieve=retrieve_yaml)


def get_schema (schema):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),schema)
    with open(schema_path) as schema_file:
        schema_json = json.load(schema_file)
    return schema_json

def get_registryDRAFT202012(schema_refs:dict):
    resources = []
    for schema, refs in schema_refs.items():
        sch = DRAFT202012.create_resource(get_schema(schema))
        for ref in refs:
            resources.append((ref, sch)) 
    return Registry().with_resources(resources)

registry = get_registryDRAFT202012( {"_loading_props.json":["urn:loading_props","local:loading_props"],
                                     "_pile_props.json":["urn:pile_props","local:pile_props"],
                                     "_geom_props.json":["urn:geom_props","local:geoms_props"],
                                     "_strata_props.json":["urn:strata_props","local:strata_props"]}
                                    )
replace_urn = [{"file_name":"_loading_props.json","urn":"urn:loading_props"},
             {"file_name":"_pile_props.json","urn":"urn:pile_props"},
             {"file_name":"_geom_props.json","urn":"urn:geom_props"},
             {"file_name":"_strata_props.json","urn":"urn:strata_props"},
            ]
def get_schema_expanded_str(schema):
   
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),schema)
    
    with open(schema_path) as schema_file:
        schema_str = schema_file.read()
        for item in replace_urn:
            schema_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),item["file_name"])
            with open(schema_path2) as schema_file2:
                urn_contents = schema_file2.read()
                search = "{\"$ref\":\"" + item["urn"] +"\"}"
                schema_str = schema_str.replace(search,urn_contents)
    
    return schema_str

# def get_schema_expanded_str(schema):
#     # https://stackoverflow.com/questions/47054088/fully-expanding-ref-references-in-a-json-schema-with-python
    
#     # https://github.com/purukaushik/ref-resolver/blob/master/ref_resolver/ref_resolver.py
#     # https://github.com/gazpachoking/jsonref
    
#     schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),schema)
    
#     with open(schema_path) as schema_file:
#         schema_str = schema_file.read()
#     for key, value in registry._resources:
#         search = "{\"$ref\":\"" + key +"\"}"
#         contents = value["contents"]
#         schema_str.replace(search,contents)
    
#     return schema_str

def get_schema_obj (schema):
    s = get_schema_expanded_str(schema)
    o = json.loads(s)
    return o
    
class FoundSchemas(json_objs):
    def __init__(self):
        super().__init__(id= '01', description='JSON schemas for foundations',version='p01.1',type='schema')
        self.add ('footings_v4.json', get_schema_obj('footings_v4.json'), 'schema for footings with ground models and loadings','P01.1')
        self.add ('piles_v4.json', get_schema_obj('piles_v4.json'), 'schema of ground model with pile set and loadings','P01.1')
        self.add ('ground_models_v4.json',get_schema_obj('ground_models_v4.json'), 'schema of ground models','P01.1')
        