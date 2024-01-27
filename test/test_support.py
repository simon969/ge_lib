import os
import json


def csv_to_file(fname, rows):
    with open (fname, 'w') as f:
        for row in rows:
            f.write(row + '\n')
    print('Output written to ' + fname)  

def json_to_file2(fname, data):
    
    if type(data) is list:
        json_string = json.dumps([ob.__dict__ for ob in data])
    else:
        json_string = json.dumps(data)
    
    with open(fname, 'w') as f:
       f.write (json_string)
    print('Output written to ' + fname)

def json_to_file(fname, data):
    with open(fname, 'w') as f:
        json.dump(data, f)
    print('Output written to ' + fname)

def str_to_file(fname, s):
    with open(fname, 'w') as f:
        f.write(s)
    print('Output written to ' + fname)

def max_property (footings:list, property):
    max_value = 0
    for f in footings:
        value = f.get(property,0)
        if max_value < value:
            max_value = value
        return max_value
    
def list_to_json(list):
    res = []
    
    for r in list:
        s1 = r.to_json()
        res.append("{" + s1 + "}")

    return "[" + ",".join(res) + "]" 