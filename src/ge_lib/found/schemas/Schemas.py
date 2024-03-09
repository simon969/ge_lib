import os
import json
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
from referencing.jsonschema import DRAFT202012
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

def get_schema_full(schema):
    # https://stackoverflow.com/questions/47054088/fully-expanding-ref-references-in-a-json-schema-with-python
    
    # https://github.com/purukaushik/ref-resolver/blob/master/ref_resolver/ref_resolver.py
    # https://github.com/gazpachoking/jsonref
    
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),schema)
    
    with open(schema_path) as schema_file:
        schema_str = schema_file.read()
    for key, value in registry._resources:
        search = "{\"$ref\":\"" + key +"\"}"
        contents = value["contents"]
        schema_str.replace(search,contents)
    
    return schema_str
