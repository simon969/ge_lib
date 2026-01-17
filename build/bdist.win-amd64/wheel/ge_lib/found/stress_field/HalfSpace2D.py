
class Loadings2D:
    def __init__(self, data):
        self.id= '01'
        self.description ='new half space'
        self.lines = []
        self.strips = []
    def addLine(self, x_pos, z_pos, q):
        line = {"x":x_pos,
                "z":z_pos,
                "q":q}
        self.lines.append(line)
    def addStrip(self, x_pos, z_pos, width, q):
        strip = {"x":x_pos,
                 "z":z_pos,
                 "width": width,
                 "q":q
                }
        self.strips.append(strip)
    
def local_line (p, line):
    local = {"x":p["x"] - line["x"],
             "z":p["z"] - line["z"],
             "q":line["q"]
             }
    return local

def local_strip (p, strip):
    local = {"x":p["x"] - strip["x"],
             "z":p["z"] - strip["z"],
             "q":strip["q"],
             "width": strip["width"]
             }
    return local

def add_stress (p, load):
    p["sx"] += load["sx"]
    p["sz"] += load["sz"]
    p["sxz"] += load["sxz"]

class StressField2D:
    def __init__(self, 
                 data,
                 x_start,
                 x_stop,
                 x_step,
                 z_start,
                 z_stop,
                 z_step):
        self.id= '01'
        self.description ='new stress field'
        self.points = []
        self.__init_points ()
    
    def __init_points (self,
                       x_start,
                       x_stop,
                       x_step,
                       z_start,
                       z_stop,
                       z_step):
        for x in range(x_start, x_stop, x_step):
            for z in range (z_start, z_stop, z_step):
                point = {"x":x,
                         "z":z,
                         "sx":0,
                         "sz":0,
                         "sxz":0}
                self.points.append(point)
        
    def addLoading (self, loading:Loadings2D):

        for p in self.points:
            for line in loading.lines:
                lline = local_line (p,line)
                self.line_sz(lline)
                self.line_sx(lline)
                self.line_sxz(lline)
                add_stress(p, lline)
            for strip in loading.strips:
                lstrip = local_strip (p, strip)
                self.strip_sz(lstrip)
                self.strip_sx(lstrip)
                self.strip_sxz(lstrip)
                add_stress(p, lstrip)
            


                

