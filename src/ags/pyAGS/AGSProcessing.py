import os

escapes = ''.join([chr(char) for char in range(1, 32)])

def _is_file_like(obj):
    """Check if object is file like

    Returns
    -------
    bool
        Return True if obj is file like, otherwise return False
    """

    if not (hasattr(obj, 'read') or hasattr(obj, 'write')):
        return False

    if not hasattr(obj, "__iter__"):
        return False

    return True



class ags_group:
    def __init__(self, group:str, line_start):
        # self.group = group.translate(None, escapes)
        self.group = group
        self.line_start = line_start
        self.headings = [] 
        self.units = []
        self.types = [] 
        self.data = []
    def line_end (self, line_end):
        self.line_end = line_end
    def split_headings(self):
        g = self.clean_split(self.group)
        self.name = g[1]
        self.headings = self.clean_split(self.heading)
        self.units = self.clean_split(self.unit)
        self.types = self.clean_split(self.type)

    def clean_split (self, s):
        s = s.replace("\"","") 
        s = s.replace("\n","")
        s = s.replace("\r","")
        return s.split(",")

class result:
    def __init__(self, file, group, line_start, line_end):
        self.file = file
        self.group = group
        self.line_start = line_start
        self.line_end = line_end
    def as_csv(self):
        return "\"{}\",\"{}\",{},{}".format(self.file, self.group, self.line_start, self.line_end) 
        # return "\"" + self.file + '\",\"' + self.group + '\",' + str(self.line_start) + ',' + str(self.line_end)
class result_bypoints:
    def __init__(self, file, group, point, count):
        self.file = file
        self.group = group
        self.point = point
        self.count = count
    def as_csv(self):
        return "\"{}\",\"{}\",\"{}\",{}".format(self.file, self.group, self.point, self.count)
        # return self.file + ',' + self.group + ',' + str(self.point) + ',' + str(self.count)
class group_summary:
    def __init__(self, ags_group):
        self.ags_group = ags_group
        self.points = {}
    def by_point(self):
        point_col = None
        for i, x in enumerate(self.ags_group.headings):
            if (x == "LOCA_ID"):
                point_col = i
        if point_col is not None:
            for s in self.ags_group.data:
                d = self.ags_group.clean_split(s)
                point = d[point_col]
                exist_count = self.points.get(point)
                if (exist_count is None):
                    self.points[point] = 1
                else:
                    update = {point: exist_count +1 } 
                    self.points.update (update)
        return self.points
    def by_result(self, filename):
            self.by_point()
            results = [] 
            for i, (point, count) in enumerate(self.points.items()):
                result = result_bypoints(filename, self.ags_group.name, point, count)
                results.append(result)
            return results





class processAGS:
    def __init__(self, files):
        self.files = files
        self.results =[]
        self.results_bypoints = []

    def process(self):
        for file in self.files:
            
            if _is_file_like(file):
                file_in = file
                close_file = False
            else:
                file_in =  open(file) 
                close_file = True

            print("Processing:" + file_in.name)
            
            lines = []
            ags_groups = []
            count = 0
            fname2 = os.path.basename(file_in.name)
            g = None
            
            for rawline in file_in:
                try:
                    line = rawline.decode()
                except:
                    line = rawline
                if "GROUP" in line[0:12]:
                    g =  ags_group (line, count)   
                if "UNIT" in line[0:12]:
                    g.unit = line
                if "HEADING" in line[0:12]:
                    g.heading = line
                if "TYPE" in line[0:12]:
                    g.type = line
                if "DATA" in line[0:12]:
                    g.data.append(line)    
                if '\n' in line[0:3] and g is not None:
                    g.line_end = count - 1    
                    ags_groups.append (g)
                    g = None
                lines.append(line)
                count = count + 1
            
            if ags_groups is not None:
                for g in ags_groups:
                    name = g.group.split(",")
                    r1 = result (fname2,name[1].strip(),g.line_start,g.line_end)
                    self.results.append (r1)
                    g.split_headings()
                    sg = group_summary(g)
                    rps = sg.by_result(fname2)
                    for rp in rps:
                        self.results_bypoints.append(rp)  
            
            if close_file:
                file_in.close()
          
    def report_lines(self, file=None):
            header = 'file_name,group_name,line_start,line_end\n'
            rows = ""
            
            if file is not None:
                if _is_file_like(file):
                    file_out = file
                    close_file = False
                else:
                    file_out =  open(file, "w")
                    close_file = True

                file_out.write(header) 
                for r in self.results:
                    file_out.write (r.as_csv() + '\n')
                
                if close_file:
                    file_out.close()
            
            for r in self.results:
                rows += r.as_csv() + '\n'
            return header+rows
            
            
            
            

    def report_summary(self, file=None):
            header = 'file_name,group_name,pointid,count\n'
            rows = ""
            
            if file is not None:
                if _is_file_like(file):
                    file_out = file
                    close_file = False
                else:
                    file_out =  open(file, "w")
                    close_file = True
                file_out.write(header) 
                for r in self.results_bypoints:
                    file_out.write (r.as_csv() + '\n')
                if close_file:
                    file_out.close()
                
            for r in self.results_bypoints:
                rows += r.as_csv() + '\n'
            return header+rows