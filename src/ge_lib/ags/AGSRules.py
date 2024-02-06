import json
from .AGSWorkingGroup import ags_to_dataframe
from .rules.RulesLTC import RulesLTC
from .rules.RulesNEOM import RulesNEOM 
from .rules.RulesGeneral import RulesGeneral 
from .rules.AGSQuery import ags_query_collection

title = "AECOM Ground Engineering"
header = "AGS Value Rules"

version = "Beta v0.0.1"
release_date = "2023-02-01"

rules_formats = ['csv', 'txt', 'json']

def rules_check (path, rules='default')->ags_query_collection:
    qr = None

    if (rules == 'NEOM'):
        qr = RulesNEOM()
    
    if (rules == 'LTC'):
        qr = RulesLTC()

    if (rules.lower() in ['general','default','_default']):
        qr = RulesGeneral()

    if qr is not None:
        tables, headings, line_numbers = ags_to_dataframe(path)
        qr.run_queries (tables, headings)
    
    return qr

def rules_file (qr:ags_query_collection, format = "txt")->str:
    
    def obj_dict(obj):
            return obj.__dict__
        
    if (format=="csv"):
        arr =  get_csv_array(qr)
        return array_to_string(arr)
    
    if (format=="txt"):
        arr = get_text_array(qr)
        return array_to_string(arr)
    
    if (format=="json"):
        s1 =  qr.to_json()
            # if json tab formating is required this can be done server side, 
            # but it takes time to parse the string and the file size is bigger
            # better to prettify the json string on the client side
            # data = json.loads(s1)
            # s2 = json.dumps(data, indent=4)
            # return s2
        return s1
    
def array_to_string(arr):
    return '\n'.join(arr)
 

def get_csv_summary_array(ags_rules):
    '''Print ags query pass fail report to array.'''
    arr =  []
    header = "rule,description,pass,fail"
    arr.append(header)
    for qry in ags_rules.queries:
        arr.append ("{0},'{1}',{2},{3}".format(qry.id, qry.description, len(qry.results_pass), len(qry.results_fail)))
    return arr;

def get_csv_array(ags_rules):
    '''Print ags query pass fail report to array.'''
    arr =  []
    header = "rule,description,requirement,result,line,group,message"
    arr.append(header)
    for qry in ags_rules.queries:
        for res in qry.results_fail:
            arr.append ("\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\"".format(qry.id, qry.description, qry.requirement, 'FAIL', res['line'], res['group'], res['desc']))       
        for res in qry.results_pass:
            arr.append ("\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\"".format(qry.id, qry.description, qry.requirement, 'PASS', res['line'], res['group'], res['desc']))
    return arr;

def get_text_array(ags_rules):

    '''Print ags query pass fail report to array.'''
    arr =  []
    
    arr.append (title)
    arr.append (header + ' ' + version + " (" + release_date + ")")
    arr.append ("Rules version: '" + ags_rules.version + "'")
    arr.append ('')

    fail_count = 0
    pass_count = 0

    for qry in ags_rules.queries:
        fail_count += len(qry.results_fail)
        pass_count += len(qry.results_pass)
    
    arr.append(f'FAIL results {fail_count}\n')
    arr.append(f'PASS results {pass_count}\n')

    for qry in ags_rules.queries:
        arr.append ('Rule: {0} Description: {1}'.format(qry.id, qry.description))
        arr.append ('FAIL results ({0})'.format(len(qry.results_fail)))
        for res in qry.results_fail:
            arr.append (' Line {0}: Group:{1} Description:{2}'.format (res['line'], res['group'], res['desc']))
        arr.append ('PASS results ({0})'.format(len(qry.results_pass)))
        for res in qry.results_pass:
            arr.append (' Line {0}: Group:{1} Description:{2}'.format (res['line'], res['group'], res['desc']))    
        arr.append('')
    return arr;
       