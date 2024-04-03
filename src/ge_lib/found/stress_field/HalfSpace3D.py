class Loadings3D:
    def __init__(self, data):
        self.id= '01'
        self.description ='new half space'
        self.rectangles = []
        self.circles = []
        self.points = []

def addRectangle(self, x_pos, y_pos, z_pos, x_width, y_width, q):
        rectangle = {"x":x_pos,
                     "y":y_pos,
                     "z":z_pos,
                     "x_width":x_width,
                     "y_width":y_width,
                     "q":q}
        self.rectangles.append(rectangle)
def addCircle(self, x_pos, y_pos, z_pos, radius, q):
        circle = {"x":x_pos,
                  "y":y_pos,
                  "z":z_pos,
                  "radius": radius,
                  "q":q
                }
        self.circles.append(circle)
def addPoint(self, x_pos, y_pos, z_pos, p):
        point = {"x":x_pos,
                 "y":y_pos,
                 "z":z_pos,
                 "p":p
                 }
        self.points.append(point)
def local_rect (p, rect):
    local = {"x":p["x"] - rect["x"],
             "y":p["y"] - rect["y"],
             "z":p["z"] - rect["z"],
             "x_width": rect["x_width"],
             "y_width": rect["y_width"],
             "q":rect["q"]
             }
    return local

def local_circle (p, circle):
    local = {"x":p["x"] - circle["x"],
             "y":p["y"] - circle["y"],
             "z":p["z"] - circle["z"],
             "q":circle["q"],
             "radius": circle["radius"]
             }
    return local

def local_point (p, point):
    local = {"x":p["x"] - point["x"],
             "y":p["y"] - point["y"],
             "z":p["z"] - point["z"],
             "p":point["p"],
            }
    return local

def add_stress (p, load):
    p["sx"] += load["sx"]
    p["sz"] += load["sz"]
    p["sxz"] += load["sxz"]
class StressField3D:
    def __init__(self, 
                 data,
                 x_start,
                 x_stop,
                 x_step,
                 y_start,
                 y_stop,
                 y_step,
                 z_start,
                 z_stop,
                 z_step):
        self.id= '01'
        self.description ='new stress field'
        self.points = []
        self.__init_points (x_start,
                            x_stop,
                            x_step,
                            y_start,
                            y_stop,
                            y_step,
                            z_start,
                            z_stop,
                            z_step)
    
    def __init_points (self,
                       x_start,
                       x_stop,
                       x_step,
                       y_start,
                       y_stop,
                       y_step,
                       z_start,
                       z_stop,
                       z_step):
        for x in range(x_start, x_stop, x_step):
            for y in range (y_start, y_stop, y_step):
                for z in range (z_start, z_stop, z_step):
                    point = {"x":x,
                             "y":y,
                             "z":z,
                             "sx":0,
                             "sy":0,
                             "sz":0,
                             "sxz":0,
                             "syz":0,
                             "sxy":0,}
                self.points.append(point)
        
    def addLoading (self, loading:Loadings3D):

        for p in self.points:
            for rect in loading.rectangles:
                lrect = local_rect (p,rect)
                self.rect_sz(lrect)
                self.rect_sy(lrect)
                self.rect_sx(lrect)
                self.rect_sxz(lrect)
                self.rect_syz(lrect)
                self.rect_sxy(lrect)
                add_stress(p, lrect)
            for circle in loading.circles:
                lcircle = local_circle (p, circle)
                self.circle_sz(lcircle)
                self.circle_sy(lcircle)
                self.circle_sx(lcircle)
                self.strip_sxz(lcircle)
                self.strip_syz(lcircle)
                self.strip_sxy(lcircle)
                add_stress(p, lcircle)
            for point in loading.points:
                lpoint = local_point (p, point)
                self.point_sz(lpoint)
                self.point_sy(lpoint)
                self.point_sx(lpoint)
                self.point_sxz(lpoint)
                self.point_syz(lpoint)
                self.point_sxy(lpoint)
                add_stress(p, lpoint)