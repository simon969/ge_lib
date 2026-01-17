import os
import json


def get_schema (schema):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),schema)
    with open(schema_path) as schema_file:
        schema_json = json.load(schema_file)
    return schema_json


