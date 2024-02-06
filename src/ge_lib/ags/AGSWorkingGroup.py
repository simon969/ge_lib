
import io
import pandas as pd
import math 
import json
from rich import print as rprint

from python_ags4.AGS4 import check_file, AGS4_to_dataframe
from AGS4_fs import AGS4_to_excel,get_dict_name
from pandas import ExcelWriter

ags_dics = {
    'AGS403': {'file': 'Standard_dictionary_v4_0_3.ags','version':'4.0.3'},
    'AGS404': {'file': 'Standard_dictionary_v4_0_4.ags','version':'4.0.4'},
    'AGS41' : {'file': 'Standard_dictionary_v4_1.ags','version':'4.1.0'},
    'AGS411' : {'file': 'Standard_dictionary_v4_1_1.ags','version':'4.1.1'}
}

title = 'AECOM Ground Engineering'
header = 'AGS File Checker'

version = 'Beta v0.0.2'
release_date = '2023-10-07'


    
def check_file (input_file, dict_file):
    # return print_to_string(AGS4.check_file(input_file, '{0}\\{1}'.format (dicts_path, dict_file)))
    return list_to_bytes(ags_errors_to_list(check_file(input_file, dict_file)))

def dict_file_name (input_file, version):
    
    if version in ags_dics:
        ags_dic = ags_dics[version]
        ags_version = ags_dic['version']
    else:
        ags_version='4.1.1'

    tables, headers = AGS4_to_dataframe (input_file,get_line_numbers=False)
    dict_file = get_dict_name(tables, ags_version)

    return dict_file

def export_xlsx(input_file):
    output = io.BytesIO()
    writer = ExcelWriter(output, engine='openpyxl')
    AGS4_to_excel(input_file, writer, encoding='utf-8')
    writer.close()
    return output.getvalue()
def ags_to_dataframe(input_file):

    return AGS4_to_dataframe(filepath_or_buffer=input_file,get_line_numbers=True, rename_duplicate_headers=True)

def list_to_bytes (arr:list):
    return bytes('\n'.join(arr), 'utf-8')

def list_to_string(arr:list):
    return '\n'.join(arr)

def ags_errors_to_list(ags_errors):

    '''Print error report to array.'''
    arr =  []
    
    arr.append (title)
    arr.append (header + ' ' + version + ' (' + release_date + ')')
    arr.append ('')

    error_count = 0
    for key, val in ags_errors.items():
        if 'Rule' in key:
            error_count += len(val)

    # Print  metadata
    if 'Metadata' in ags_errors.keys():
        for entry in ags_errors['Metadata']:
            arr.append(f'''{entry['line']}: \t {entry['desc']}''')
        arr.append('')

    # Summary of errors log
    if error_count == 0:
        arr.append('All checks passed.\n')
    else:
        arr.append(f'{error_count} error(s) found in file.\n')

    # Print 'General' error messages first if present
    if 'General' in ags_errors.keys():
        arr.append('General:')

        for entry in ags_errors['General']:
            arr.append(f'''  {entry['desc']}''')
        arr.append('')

    # Print other error messages
    for key in [x for x in ags_errors if 'Rule' in x]:
        arr.append('FAIL: 'f'''{key}:''')
        for entry in ags_errors[key]:
            arr.append(f'''  Line {entry['line']}\t {entry['group'].strip('"')}\t {entry['desc']}''')
        arr.append('')
    
    return arr



