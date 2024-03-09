# import cEC7_Bearing_Capacity from 'cEC7_Bearing_Capacity'; 
#//' ==========================================================================================
#//' Design bearing resistances calculated from EC-7 EN 1997-1:2004
#//'
#//' Equation D.3 Undrained conditions
#//' Equation D.4 Drained conditions
#//' ==========================================================================================
#//' Coded  | Simon Thomson
#//' ==========================================================================================
#//' Company | AECOM
#//' ==========================================================================================
#//' Date            |     Version   |         Description 
#//' ==========================================================================================
#//  Apr 2010        |    01.00.00   | Coded for Excel VBA addin             
#//  Dec 2021        |    02.00.00   | Coded for Excel JavaScript addin           
#//  Dec 2023        |    03.00.00   | Coded for Python
#//' ==========================================================================================


import math

from  .Support import calc
from  .FootingGeoms import Footing

def calc_nq_D4(data):
    data.nq = math.exp(math.pi * math.tan(data.phi_rad)) * math.pow(math.tan(math.pi / 4 + data.phi_rad / 2), 2)
    return data.nq

def calc_nc_D4(data):
    if (data.phi_rad == 0):
        data.nc = 0 
    else:
        data.nc = (data.nq - 1) / math.tan(data.phi_rad)
    return data.nc

def calc_ng_D4 (data):
    data.ng = 2 * (data.nq - 1) * math.tan(data.phi_rad);
    return data.ng

def calc_bq_D4(data):
    data.bq = math.pow((1 - data.alpha_rad * math.tan(data.phi_rad)), 2)
    return data.bq

def calc_bc_D4(data):
    if (data.phi_rad == 0 or data.nc==0):
        data.bc = 0 
    else:
        data.bc = data.bq - (1 - data.bq) / (data.nc * math.tan(data.phi_rad))
    return data.bc

def calc_bg_D4(data):
    data.bg = math.pow((1 - data.alpha_rad * math.tan(data.phi_rad)), 2)
    return data.bg

def calc_sq_D4(data):
    data.sq = 1 + (data.breadth/ data.length) * math.sin(data.phi_rad)
    return data.sq

def calc_sc_D4(data):
    data.sc = (data.sq * data.nq - 1) / (data.nq - 1)
    return data.sc

def calc_sg_D4(data):
    data.sg = 1 - 0.3 * (data.breadth/ data.length)
    return data.sg


# inclination factors

def calc_ic_D4(data):
    if (data.iq > 0 ):
        if (data.phi_rad == 0 or data.nc==0):
            data.ic = 0
        else:
            data.ic = data.iq - (1 - data.iq) / (data.nc * math.tan(data.phi_rad))
    else:
        data.ic = 1
    return data.ic

def calc_iq_D4(data):
    
    if (data.phi_rad==0):
        tan_phi = 1.0 
    else:
        tan_phi = math.tan(data.phi_rad)
    
    data.hmax = data.vload + data.length * data.breadth * data.cohesion / tan_phi
   
    if (data.hmax == 0):
        data.iq = 1
    else:
        test = 1 - data.hload / data.hmax 
        if (test > 0):
            data.iq = math.pow(test,data.m)
        else:
            data.iq = 0
    return data.iq

def calc_ig_D4(data):   
    if (data.phi_rad==0):
        tan_phi = 1.0 
    else:
        tan_phi = math.tan(data.phi_rad)

    data.hmax = data.vload + data.length * data.breadth * data.cohesion / tan_phi
    
    if (data.hmax == 0):
        data.ig = 1
    else:
        test = 1 - data.hload / data.hmax 
        if (test > 0):
            data.ig = math.pow(test, data.m + 1)
        else:
            data.ig = 0
    return data.ig
  
def calc_m_D4(data):
        data.mb = (2 + (data.breadth/ data.length)) / (1 + (data.breadth/ data.length))
        data.ml = (2 + (data.length / data.breadth)) / (1 + (data.length / data.breadth))
        data.m = data.ml * math.pow(math.cos(data.htheta_rad), 2) + data.mb * math.pow(math.sin(data.htheta_rad),2)
        return data.m

def calc_qnc_D4(obj, data):
    
    obj.calc_ng(data)
    
    obj.calc_nq(data)
    obj.calc_bq(data)
    obj.calc_sq(data)
    obj.calc_m(data)
    obj.calc_iq(data)
    
    obj.calc_nc(data)
    obj.calc_bc(data)
    obj.calc_sc(data)
    obj.calc_ic(data)

    data.q_nc = data.cohesion * data.nc * data.bc * data.sc * data.ic
    return data.q_nc

def calc_qnq_D4(obj, data):
    obj.calc_nq(data)
    obj.calc_bq(data)
    obj.calc_sq(data)
    obj.calc_m(data)
    obj.calc_iq(data)
    data.q_nq = data.surcharge * data.nq * data.bq * data.sq * data.iq
    return data.q_nq

def calc_qng_D4(obj, data):
    obj.calc_nq(data)
    obj.calc_ng(data)
    obj.calc_bg(data)
    obj.calc_sg(data)
    obj.calc_m(data)
    obj.calc_ig(data)
    data.q_ng = 0.5 * data.density * data.breadth* data.ng * data.bg * data.sg * data.ig
    return data.q_ng

def calc_qult_D4 (obj, data):
    obj.calc_qng(obj, data)
    obj.calc_qnq(obj, data)
    obj.calc_qnc(obj, data)
    data.q_ult = data.q_nc + data.q_nq + data.q_ng
    return data.q_ult

class DrainedBearing_EC7(calc):
    def __init__(self):
        super().__init__(id='EC7_D4', 
                         description = 'Calculation of drained bearing resistance based on formulaes in BS EN 1997 Annex D4', 
                         reference = 'BS EN 1993 Equation D4', 
                         state = 'drained', 
                         component = 'bearing',
                         version = "p01.1")
        
        self.calc_nc = calc_nc_D4
        self.calc_nq = calc_nq_D4
        self.calc_ng = calc_ng_D4
        
        self.calc_m = calc_m_D4

        self.calc_bc = calc_bc_D4
        self.calc_bq = calc_bq_D4
        self.calc_bg = calc_bg_D4
        
        self.calc_sc = calc_sc_D4
        self.calc_sq = calc_sq_D4
        self.calc_sg = calc_sg_D4
        
        self.calc_ic = calc_ic_D4
        self.calc_iq = calc_iq_D4
        self.calc_ig = calc_ig_D4
    
        self.calc_qnc = calc_qnc_D4
        self.calc_qnq = calc_qnq_D4
        self.calc_qng = calc_qng_D4

        self.calc_qult = calc_qult_D4
    
    def calc(self, gm, fg:Footing):
        
        if fg:
            self.data.geom = fg.get("geom",{})
            self.data.loadcase= fg.get("loadcase",{})
            self.data.length = fg.get("length",0)
            self.data.breadth = fg.get("breadth",0)
            self.data.depth = fg.get("depth",0)
            self.data.alpha_rad = fg.get("alpha_rad",0)
            self.data.state = fg.get("state","none")
            self.data.material_set = fg.get("material_set","none")
            self.data.vload = fg.get("vload",0)
            self.data.hload = fg.get("hload",0)
            self.data.htheta_rad = fg.get("htheta_rad",0)
        if gm:
            self.data.cohesion = gm.get_attr_value(self.data.depth, "cohesion")
            self.data.phi_rad = gm.get_attr_value(self.data.depth, "phi_rad") 
            self.data.density = gm.get_attr_value(self.data.depth, "density")
            self.data.surcharge = gm.get_attr_value(self.data.depth, "EffectiveStress")
        
        self.calc_qult(self, self.data)
        return self.data.q_ult

def calc_nc_D3(data):
    data.nc = math.pi + 2
    return data.nc

def calc_qult_D3(obj, data):
    obj.calc_qnc(obj, data)
    data.q_ult = data.q_nc + data.surcharge
    return data.q_ult
    
def calc_qnc_D3(obj, data):
    obj.calc_nc(data)
    obj.calc_bc(data)
    obj.calc_sc(data)
    obj.calc_ic(data)
    data.q_nc = (math.pi + 2) * data.cu * data.bc * data.sc * data.ic
    return data.q_nc
    
def calc_bc_D3(data):
    data.bc = 1 - 2 * data.alpha_rad / (math.pi + 2)
    return data.bc

def calc_sc_D3(data):
    data.sc = 1 + 0.2 * data.breadth/ data.length
    return data.sc

def calc_ic_D3(data):
    area = data.length * data.breadth
    if (data.hload < area * data.cu):
        data.ic = 0.5 * (1 + math.pow(1 - data.hload / (area * data.cu), 0.5))
    else:
        data.ic = 0.5
    return data.ic

class UndrainedBearing_EC7(calc):
    def __init__(self):
        super().__init__(id='EC7_D3', 
                         description='Calculation of undrained bearing resistance based on formulaes in BS EN 1997 Annex D3', 
                         reference = 'BS EN 1992 Annex D3', 
                         state = 'undrained', 
                         component='bearing',
                         version = "p01.1")
        
        self.calc_nc = calc_nc_D3
        self.calc_bc = calc_bc_D3
        self.calc_sc = calc_sc_D3
        self.calc_ic = calc_ic_D3
        self.calc_qnc = calc_qnc_D3
        self.calc_qult = calc_qult_D3

    def calc(self, gm, fg:Footing):
        
        if fg:
            self.data.geom = fg.get("geom",{})
            self.data.loadcase= fg.get("loadcase",{})
            self.data.length = fg.get("length",0)
            self.data.breadth = fg.get("breadth",0)
            self.data.depth = fg.get("depth",0)
            self.data.alpha_rad = fg.get("alpha_rad",0)
            self.data.state = fg.get("state","none")
            self.data.material_set = fg.get("material_set","none")
            self.data.vload = fg.get("vload",0)
            self.data.hload = fg.get("hload",0)
            self.data.htheta_rad = fg.get("htheta_rad",0)

        if gm:
            self.data.cu = gm.get_attr_value(self.data.depth, "cu")
            self.data.density = gm.get_attr_value(self.data.depth, "density")
            self.data.surcharge = gm.get_attr_value(self.data.depth, "EffectiveStress")
       
        self.calc_qult(self, self.data)
        return self.data.q_ult