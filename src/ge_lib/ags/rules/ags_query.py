import pandas as pd
from datetime import datetime, timedelta

map_datetime = {"yyyy-mm-dd":"%Y-%m-%d",
                "yyyy-mm-ddThh:mm:ss":"%Y-%m-%dT%HH:%MM:%SS",
                "dd/mm/yyyy":"%d/%m/%Y"}

def is_datetime(var):

    if (isinstance(var, pd.DatetimeIndex) or isinstance(var, pd.Timestamp)):
        return True
    return False

class ags_query:
    def __init__(self, id, description, requirement, action):
        self.id = id
        self.description = description
        self.requirement = requirement
        self.action = action
        self.results_fail = []
        self.results_pass = []
    def run_query (self, tables, headings):
        pass
    
    def get_group(self, tables, table, add_result = True):
        try :

            grp = tables[table]
                      
            if (add_result):
                line = grp['line_number'][0]
                desc = 'The group {0} is present'.format(table)
                res = {'line':line, 'group':table, 'desc':desc}
                self.results_pass.append (res)
            
            return grp
        except:    
            if (add_result):
                line = 0
                desc = 'The group {0} is not present'.format(table)
                res = {'line':line, 'group':table, 'desc':desc}
                self.results_fail.append (res)
            return None
    def check_sum_thickness (self, table, table_name, where, heading_top, heading_base, LOCA_FDEP, line_number):
        
        if (where is not None):
            qry = table.query(where)
        else:
            qry = table.query("HEADING == 'DATA'")
        
        sum = 0

        for index, values in qry.iterrows():
                try:
                    thk =  pd.to_numeric(values[heading_base]) - pd.to_numeric(values[heading_top]) 
                    sum += thk
                    if (sum != LOCA_FDEP):
                        desc = 'The heading LOCA_FDEP value {0} in group LOCA does not equal to sum of the thicknesses of the records in {1} group sum({2}-{3}) {4}'.format(LOCA_FDEP,table_name,heading_base,heading_top, sum)
                        res = {'line':line_number, 'group':'LOCA', 'desc':desc}
                        self.results_fail.append (res)
                    else:
                        desc = 'The heading LOCA_FDEP value {0} in group LOCA does equals the sum of the thicknesses of the records in {1} group sum({2}-{3}) {4}'.format(LOCA_FDEP,table_name,heading_base,heading_top, sum)
                        res = {'line':line_number, 'group':'LOCA', 'desc':desc}
                        self.results_pass.append (res)
                except:
                    desc = 'The heading LOCA_FDEP value {0} in group LOCA does not equal to sum of the thicknesses of the records in {1} group sum({2}-{3}) {4}'.format(LOCA_FDEP,table_name,heading_base,heading_top, sum)
                    res = {'line':line_number, 'group':'LOCA', 'desc':desc}
                    self.results_fail.append (res)
   
    def is_present(self, table, table_name, field, add_result=True):
        try :
            t = table[field]
            if (add_result):
                line =  table['line_number'][0]
                line2 = table['line_number'].iloc[0]
                desc = 'The heading {0} present in group {1}'.format(field, table_name)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_pass.append (res)
            return True
        except:    
            if (add_result):
                line =  table['line_number'][0]
                desc = 'The heading {0} not present in group {1}'.format(field, table_name)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_fail.append (res)
            return False 
    def get_unit_pydatetime(self, table, table_name, field, add_result):
        unit = self.get_unit_string(table, table_name, field, add_result)
        pyunit = map_datetime.get(unit, None)
        return pyunit     
    def get_first_value (self, table, table_name, field, where, add_result):
        field_present =  self.is_present(table,table_name, field, add_result=add_result)
        if field_present:
            qry = table.query(where)
            if len(qry.index) > 0:
                value = pd.to_numeric(qry[field].iloc[0],errors='coerce')
                if (add_result):
                    if (value == 'Nan'):
                        line = qry['line_number'].iloc[0]
                        desc = 'The value {0} in heading {1} of group {2} is not numeric'.format(qry[field][0], field, table_name)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)
                        return value
                    else:
                        line = qry['line_number'].iloc[0]
                        desc = 'The value {0} in heading {1} of group {2} is numeric'.format(value,field, table_name)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                        return None
            else :
                if (add_result):  
                    line = table['line_number'][0]
                    desc = 'The query {0} returned no results from group {1}'.format(where, table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_fail.append (res)
                return None
    def get_unit_string(self, table, table_name, field, add_result):
        field_present =  self.is_present(table,table_name,field, add_result=add_result)
        unit = ''
        if field_present:
            qry = table.query("HEADING == 'UNIT'")
            unit = qry[field].iloc[0]
            if (add_result):
                if (unit == ""):
                    line = qry['line_number'].iloc[0]
                    desc = 'The heading {0} unit in group {1} is not provided'.format(field, table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_fail.append (res)
                else:
                    line = qry['line_number'].iloc[0]
                    desc = 'The heading {0} unit {1} in group {2} is provided'.format(field, unit, table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_pass.append (res)
        return unit

    def check_unit_string(self, table, table_name, field, unit_expected):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            qry = table.query("HEADING == 'UNIT'")
            unit = qry[field].iloc[0]
            if (unit == unit_expected):
                line = qry['line_number'].iloc[0]
                desc = 'The heading {0} unit {1} in group {2} is the expected unit {3}'.format(field, unit, table_name, unit_expected)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_pass.append (res)
            else:
                line =qry['line_number'].iloc[0]
                desc = 'The heading {0} unit {1} in group {2} is not the expected unit {3}'.format(field,unit,table_name, unit_expected)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_fail.append (res)
    def check_type_string(self, table, table_name, field, type_expected):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            qry = table.query("HEADING == 'TYPE'")
            type = qry[field].iloc[0]
            if (type == type_expected):
                line = qry['line_number'].iloc[0]
                desc = 'The heading {0} type {1} in the of group {2} is the expected type {3}'.format(field, type, table_name, type_expected)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_pass.append (res)
            else:
                line =qry['line_number'].iloc[0]
                desc = 'The heading {0} type {1} in the of group {2} is not the expected type {3}'.format(field,type,table_name, type_expected)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_fail.append (res)

    def check_datetime (self, table, table_name, field, where, min_dt, max_dt):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            UNIT = self.check_unit_string
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                try:
                    value = values[field]
                    dt = pd.to_datetime(values[field], infer_datetime_format=True)
                    if (dt> min_dt and dt < max_dt):
                        line = values['line_number']
                        desc = 'The heading {0} value in group {1} has a recognised date format {2} and is within the ranges {3} and {4}'.format(field, table_name, dt, min_dt, max_dt)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                except:
                    line = values['line_number']
                    if (len(value)==0):
                        desc = 'The heading {0} value in group {1} is blank'.format(field, table_name)
                    else:
                        desc = 'The heading {0} value ({1}) in group {2} is not in a recognised date format'.format(field, value, table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_pass.append (res)
    def check_string_contains(self, table, table_name, field, where, contains):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                value = values[field]
                if  contains in value:
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in group {2} contains {3}'.format( field, value, table_name, contains)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                else:
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in group {2} does not contain {3}'.format(field, value, table_name, contains)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)
    def check_value_or_string_allowed(self, table, table_name, field, where, min_val, max_val, str_allowed):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                str_val = values[field]
                if  str_val in str_allowed:
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in of group {2} is in the allowed list {3}'.format( field, str_val, table_name,','.join(str_allowed))
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                else:
                    try:
                        value = pd.to_numeric(values[field])
                        if (min_val <= value and value <= max_val):
                            line = values['line_number']
                            desc = 'The heading {0} value of {1} in group {2} is within the range of {3} and {4}'.format(field, value, table_name, min_val, max_val)
                            res = {'line':line, 'group':table_name, 'desc':desc}
                            self.results_pass.append (res)
                        else:
                            line = values['line_number']
                            desc = 'The heading {0} value ({1}) in group {2} is outside the range of {3} and {4}'.format(field, value, table_name, min_val, max_val)
                            res = {'line':line, 'group':table_name, 'desc':desc}
                            self.results_fail.append (res)
                    except:
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in group {2} is not a number and is not in allowed string list {3}'.format(field, str_val, table_name,','.join(str_allowed))
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)

    
    def check_string_allowed(self, table, table_name, field, where, allowed):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                value = values[field]
                if  value in allowed:
                        line = values['line_number']
                        desc = 'The heading {0} value {1} in group {2} is in the allowed list {3}'.format(field, value, table_name,','.join(allowed))
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                else:
                        line = values['line_number']
                        desc = 'The heading {0} value {1} in group {2} is not in the allowed list {3}'.format(field, value, table_name, ','.join(allowed))
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)
    def check_string_length(self, table, table_name, field, where, min_length, max_length):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                value = values[field]
                length = len(value)
                if  length >= min_length and length <= max_length:
                        line = values['line_number']
                        desc = 'The heading {0} string length ({1}) in group {2} is within the ranges {3} and {4}'.format(field, length, table_name, min_length, max_length)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                else:
                        line = values['line_number']
                        desc = 'The heading {0} strength length ({1}) in group {2} is outside the ranges {3} and {4}'.format(field, length, table_name, min_length, max_length)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)
    def check_unique(self,table,table_name, where, field):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            duplicates = qry.loc[qry[field].duplicated(keep='first')==True]
            if duplicates is None:
                line = table['line_number'][0]
                desc = 'The heading {0} values are not duplicated in {1} group'.format(field,table_name)
                res = {'line':line, 'group':table_name, 'desc':desc}
                self.results_pass.append (res)
            else:
                for index, values in duplicates.iterrows():
                    line = values['line_number']
                    desc = 'The heading {1} value {0} is duplicated in {2} group'.format(field, values[field], table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_fail.append (res)

    def check_value(self, table, table_name, field, where, min_value, max_value):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                qry = table.query(where)
            else:
                qry = table.query("HEADING == 'DATA'")
            for index, values in qry.iterrows():
                try:
                    value = pd.to_numeric(values[field])
                    if  value >= min_value and value <= max_value:
                        line = values['line_number']
                        desc = 'The heading {1} value ({0}) in group {2} is within the ranges {3} and {4}'.format(field,value,  table_name, min_value, max_value)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                    else:
                        line = values['line_number']
                        desc = 'The heading {1} value ({0}) in group {2} is outside the ranges {3} and {4}'.format(field,value,  table_name, min_value, max_value)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)    
                except:
                    line = values['line_number']
                    desc = 'The heading {1} value ({0}) in  in group {2} is not consided as a number'.format( field, values[field], table_name)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_fail.append (res)
        
    def check_duration(self, table, table_name, field, where, min_value, max_value):
        field_present =  self.is_present(table,table_name,field, add_result=True)
        if field_present:
            if (where is not None):
                data = table.query(where)
            else:
                data = table.query("HEADING == 'DATA'")
            units = table.query("HEADING == 'UNIT'")
            field_unit = units[field][0]
            for index, values in data.iterrows():
                value = self.to_timedelta(values[field], field_unit)
                if (value == 'naT'):
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in group {2} is not a timedelta'.format(field, values[field] , table_name) 
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)  
                else:                        
                    if (value >= min_value and value <= max_value):
                        line = values['line_number']
                        desc = 'The heading {0} value ({1}) in group {2} is within the ranges {3} and {4}'.format(field,value, table_name, min_value, max_value)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                    else:
                        line = values['line_number']
                        desc = 'The heading {0} value ({0}) in group {2} is outside the ranges {3} and {4}'.format(field, value, table_name, min_value, max_value)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)
            
    def to_timedelta(self, data, unit):
        try:
            if (unit == "hh:mm"):
                return pd.to_timedelta(data + ':00')
            else:
                return pd.to_timedelta(data)
        except:
            return 'naT'
    def check_row_count(self, table, table_name, where, min_value, max_value):
        
        if (where is not None):
            qry = table.query(where)
        else:
            qry = table.query("HEADING == 'DATA'")

        value  = len(qry.index)
        if value >= min_value and value <= max_value:
            line = table['line_number'][0]
            desc = 'The group {0} rowcount is {1} for query {2} is within the ranges {3} and {4}'.format(table_name, value, where, min_value, max_value)
            res = {'line':line, 'group':table_name, 'desc':desc}
            self.results_pass.append (res)
        else:
            line = table['line_number'][0]
            desc = 'The group {0} the rowcount is {1} for query {2} is outside the ranges {3} and {4}'.format(table_name, value, where, min_value, max_value)
            res = {'line':line, 'group':table_name, 'desc':desc}
            self.results_fail.append (res)    

class ags_query_collection:

    def __init__(self, id, description, version):
        self.id = id
        self.description = description
        self.version = version
        self.queries = []
        self._init_queries()
    def _init_queries(self):
        pass
    
    def add_query(self, q):
        self.queries.append (q)
    
    def run_queries(self, tables, headings):
        start_time = datetime.now()
        print ("{0:%Y-%m-%d %H:%M:%S%z} started run_queries()".format(start_time))
        for q in self.queries:
            q.run_query (tables, headings)
            print("{0:%Y-%m-%d %H:%M:%S%z} rule {1} completed PASS({2}) FAIL({3})".format(datetime.now(), q.id,len(q.results_pass),len(q.results_fail)))
        end_time = datetime.now()
        print ("{0:%Y-%m-%d %H:%M:%S%z} ended run_queries() {1}".format(end_time, str(end_time-start_time)))
    
    def to_json(self):
        
        q_arr = []
        def results_to_str_array (list):
            r = []
            for e in list:
                s = f"{{\"line\":{e['line']}, \"group\":\"{e['group']}\", \"desc\":\"{e['desc']}\"}}"
                r.append(s)
            return r 
        for qry in self.queries:
            results_pass = ",".join(results_to_str_array(qry.results_pass))
            results_fail = ",".join(results_to_str_array(qry.results_fail))
            q1 = f"{{\"id\": \"{qry.id}\", \"description\": \"{self.description}\", \"pass_results\":[{results_pass}],\"fail_results\":[{results_fail}]}}"
            q_arr.append(q1)
        
        queries = ",".join(q_arr)

        s1 = f"{{\"id\": \"{self.id}\",  \"description\": \"{self.description}\",\"queries\": [{queries}]}}"

        return s1 
    
