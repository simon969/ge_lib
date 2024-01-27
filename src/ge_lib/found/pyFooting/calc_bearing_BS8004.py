
import math

from ge_lib.found.pyGround.Support import calc
from ge_lib.found.pyGround.GroundModel import GroundModel
from ge_lib.found.pyFooting.FootingGeoms import Footing

def calc_nq_18(data):
    data.nq = math.exp(math.pi * math.tan(data.phi_rad)) * math.pow(math.tan(math.pi / 4 + data.phi_rad / 2), 2)
    return data.nq

def calc_nc_18(data):
    if data.phi_rad == 0:
        data.nc = 0
    else:
        data.nc = (data.nq-1) / math.tan(data.phi_rad)
    return data.nc

def calc_ng_18(data):
    if data.phi_rad == 0:
        data.ng = 0
    else:
        if data.smooth == True:
            data.ng_alpha = 0.0663
            data.ng_beta = 9.3
        else:
            data.ng_alpha = 0.1054
            data.ng_beta = 9.6
        
        data.ng = data.ng_alpha * math.exp(data.ng_alpha*data.phi_rad)
    return data.ng

def calc_sq_19(data):
    data.sq = 1 + (data.breadth/ data.length) * math.tan(data.phi_rad)
    return data.sq

def calc_sc_19(data):
    if (data.nc == 0):
        data.sc = 1.0
    else:
        data.sc = 1 + (data.breadth/data.length) * (data.ng / data.nc)
    return data.sc

def calc_sg_19(data):
    data.sg = 1 - 0.4 * (data.breadth/ data.length)
    return data.sg

def calc_ic_20(data):
    if (data.phi_rad == 0):
        if (data.cohesion * data.nc == 0):
            data.ic = 1
        else:
            data.ic = 1 - (data.m * data.hload / (data.cohesion * data.nc * data.length * data.breadth))
    else:
        data.ic = data.iq - (1 - data.iq) / (data.nc * math.tan(data.phi_rad))
    return data.ic

def calc_iq_20(data):
    
    if (data.phi_rad == 0):
        tan_phi = 1.0 
    else:
        tan_phi = math.tan(data.phi_rad)

    data.hmax = (data.vload + data.length * data.breadth * data.cohesion / tan_phi)
    
    if (data.hmax == 0):
        data.iq = 1
    else:
        test =  1 - (data.hload / (data.hmax))
        if (test > 0):
            data.iq = math.pow(test, data.m)
    
    return data.iq

def calc_ig_20(data): 
    
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

def calc_bq_21(data):
    data.bq = data.bg
    return data.bq

def calc_bc_21(data):
    if (data.phi_rad == 0):
        data.bc = 1.0 - 2 * data.alpha_rad / (math.pi + 2.0)
    else:
        data.bc = data.bq - (1.0 - data.bq) / (data.nc * math.tan(data.phi_rad))
    return data.bc

def calc_bg_21(data):
    data.bg = math.pow((1.0 - data.alpha_rad * math.tan(data.phi_rad)), 2.0)
    return data.bg

def calc_gq_22 (data):
    if (data.phi_rad == 0):
        data.gq= 1.0
    else:
        # omega_rad inclination of ground surface from horizontal in the direction away from the foundation
        if (data.omega_rad == 0):
            data.gq = 1.0
        else:
            data.gq =  math.pow (1.0 - math.tan(data.omega_rad), 2.0)
    return data.gq

def calc_gg_22(data):
    data.gg = data.gq
    return data.gg

def calc_gc_22 (data):
    if (data.phi_rad == 0):
        # omega_rad inclination of ground surface from horizontal in the direction away from the foundation
        data.gc = 1.0 -  (2.0 * data.omega_rad / (math.pi + 2.0))
    else:
        data.gc = data.gq - (1.0 - data.gq) / (data.nc * math.tan(data.phi_rad))
    return data.gc

def calc_dc_23 (data):
    if (data.phi_rad == 0):
        data.dc = 1.0 + 0.33 * math.atan(data.depth / data.breadth)
    else:
        data.dc = data.dq - (1.0 - data.dq) / (data.nc * math.tan(data.phi_rad))  
    return data.dc

def calc_dg_23(data):
    data.dg = 1.0
    return 

def calc_dq_23(data):
    data.dq = 1.0 +  2.0 * math.pow(math.tan(1.0 - math.sin(data.phi_rad)), 2.0) * math.atan (data.depth / data.breadth)
    return data.dq

def calc_rq_24(data):
    t = (-0.44 + 0.6 * data.breadth / data.length) * math.tan(data.phi_rad)
    if (data.lr == 0):
        s = 0
    else:
        s = 3.07 * math.sin(data.phi_rad) * math.log10(2 * data.lr) / (1 + math.sin(data.phi_rad))
    data.rq = math.exp(t + s)
    return data.rq

def calc_rg_24(data):
    data.rg = data.rq
    return data.rg

def calc_rc_24(data):
    if (data.phi_rad * data.nc == 0):
        if (data.lr == 0):
            data.rc = 0.32 + 0.12 * (data.breadth/data.length)
        else:
            data.rc = 0.32 + 0.12 * (data.breadth/data.length) + 0.6 * math.log10(data.lr)
    else:
        data.rc = data.rq - (1.0 - data.rq) / (data.nc * math.tan(data.phi_rad))
    return data.rc

def calc_lr (data):
    util = data.cohesion + data.surcharge * math.tan(data.phi_rad)
    if util == 0.0:
        data.lr = data.shear_mod
    else:
        data.lr = data.shear_mod / util
    return data.lr

def calc_m(data):
    data.mb = (2.0 + (data.breadth/ data.length)) / (1.0 + (data.breadth/ data.length))
    data.ml = (2.0 + (data.length / data.breadth)) / (1.0 + (data.length / data.breadth))
    data.m = data.ml * math.pow(math.cos(data.htheta_rad), 2.0) + data.mb * math.pow(math.sin(data.htheta_rad),2.0)
    return data.m

def calc_qnc_17(obj, data):
    
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
    obj.calc_dc(data)
    obj.calc_gc(data)
    obj.calc_rc(data)

    data.q_nc = data.cohesion * data.nc * data.bc * data.sc * data.ic * data.dc * data.gc * data.rc
    return data.q_nc

def calc_qnq_17(obj, data):
    obj.calc_nq(data)
    obj.calc_bq(data)
    obj.calc_sq(data)
    obj.calc_m(data)
    obj.calc_iq(data)
    obj.calc_dq(data)
    obj.calc_gq(data)
    obj.calc_lr(data) # required for calc_rq()
    obj.calc_rq(data)
    data.q_nq = data.surcharge * data.nq * data.bq * data.sq * data.iq * data.dq * data.gq * data.rq
    return data.q_nq

def calc_qng_17(obj, data):
    obj.calc_nq(data)
    obj.calc_ng(data)
    obj.calc_bg(data)
    obj.calc_sg(data)
    obj.calc_m(data)
    obj.calc_ig(data)
    obj.calc_dg(data)
    obj.calc_gq(data) # required for calc_gg()
    obj.calc_gg(data)
    obj.calc_lr(data) # required for calc_rq()
    obj.calc_rq(data) # required for calc_rg()
    obj.calc_rg(data)
    
    data.q_ng = 0.5 * data.density * data.breadth* data.ng * data.bg * data.sg * data.ig * data.dg * data.gg * data.rg
    return data.q_ng

def calc_qult_17 (obj, data):
    obj.calc_qng(obj, data) 
    obj.calc_qnq(obj, data)
    obj.calc_qnc(obj, data)
    data.q_ult = data.q_nc + data.q_nq + data.q_ng
    return data.q_ult

class DrainedBearing_BS8004(calc):
    def __init__(self):
        super().__init__(id='BS8004_Eq17', 
                         description='Calculation of drained bearing resistance based on formulaes in BS 8004', 
                         reference = 'BS 8004 Equation 17', 
                         state = 'drained', 
                         component='bearing',
                         version = "p01.1")
        
        self.calc_nc = calc_nc_18
        self.calc_nq = calc_nq_18
        self.calc_ng = calc_ng_18
        
        self.calc_bc = calc_bc_21
        self.calc_bq = calc_bq_21
        self.calc_bg = calc_bg_21
        
        self.calc_sc = calc_sc_19
        self.calc_sq = calc_sq_19
        self.calc_sg = calc_sg_19
        
        self.calc_m = calc_m
        self.calc_lr = calc_lr
        self.calc_ic = calc_ic_20
        self.calc_iq = calc_iq_20
        self.calc_ig = calc_ig_20
    
        self.calc_dc = calc_dc_23
        self.calc_dq = calc_dq_23
        self.calc_dg = calc_dg_23

        self.calc_gc = calc_gc_22
        self.calc_gq = calc_gq_22
        self.calc_gg = calc_gg_22
        
        self.calc_rc = calc_rc_24
        self.calc_rq = calc_rq_24
        self.calc_rg = calc_rg_24
        
        self.calc_qnc = calc_qnc_17
        self.calc_qnq = calc_qnq_17
        self.calc_qng = calc_qng_17

        self.calc_qult = calc_qult_17
    
    def calc(self, gm:GroundModel, fg:Footing):

        if fg:
            self.data.geom = fg.get("geom",{})
            self.data.loadcase= fg.get("loadcase",{})
            self.data.length = fg.get("length",0)
            self.data.breadth = fg.get("breadth",0)
            self.data.depth = fg.get("depth",0)
            self.data.alpha_rad = fg.get("alpha_rad",0)
            self.data.omega_rad = fg.get("omega_rad",0)
            self.data.vload = fg.get("vload",0)
            self.data.hload = fg.get("hload",0)
            self.data.htheta_rad = fg.get("htheta_rad",0)
            
        if gm:
            self.data.cohesion = gm.get_attr_value(self.data.depth, "cohesion")
            self.data.phi_rad = gm.get_attr_value(self.data.depth, "phi_rad")
            if self.data.phi_rad == 0.0:
                phi_deg = gm.get_attr_value(self.data.depth, "phi_deg")
                self.data.phi_rad = math.radians(phi_deg)

            self.data.density = gm.get_attr_value(self.data.depth, "density")
            if self.data.density == 0.0:
                density_sat = gm.get_attr_value(self.data.depth, "density_sat")
                self.data.density = density_sat - gm.water_density

            self.data.surcharge = gm.get_attr_value(self.data.depth, "EffectiveStress")
            
            self.data.shear_mod = gm.get_attr_value(self.data.depth, "shear_mod")
            if self.data.shear_mod == 0.0:
                drained_mod =  gm.get_attr_value(self.data.depth, "DrainedModulus")
                poisson_ratio =  gm.get_attr_value(self.data.depth, "poisson_ratio")
                self.data.shear_mod = drained_mod / (2 * (1 + poisson_ratio))

        self.calc_qult(self, self.data)
        return self.data.q_ult

def calc_nc_25(data):
    data.nc = math.pi + 2
    return data.nc

def calc_qult_25(obj, data):
    obj.calc_qnc(obj, data)
    data.q_ult = data.q_nc + data.surcharge
    return data.q_ult
    
def calc_qnc_25(obj, data):
    obj.calc_nc(data)
    obj.calc_sc(data)
    obj.calc_dc(data)
    data.q_nc = data.nc * data.cu * data.sc * data.dc
    return data.q_nc
    
def calc_dc_25(data):
    data.dc = 1 + 0.2 * data.breadth/ data.length
    return data.dc

def calc_sc_25(data):
    data.sc = 1.0 + 0.12 * data.breadth / data.length +  0.17 * math.pow(data.depth / data.breadth, 0.5)
    return data.sc

class UndrainedBearing_BS8004 (calc):
    def __init__(self):
        super().__init__(id='BS8004_Eq25', 
                         description='Calculation of undrained bearing resistance based on formulaes in BS 8004', 
                         reference = 'BS 8004 Equation 25', 
                         state = 'undrained', 
                         component='bearing',
                         version = "p01.1")
        
        self.calc_nc = calc_nc_25
        self.calc_sc = calc_sc_25
        self.calc_dc = calc_dc_25
        self.calc_qnc = calc_qnc_25
        self.calc_qult = calc_qult_25

    def calc(self, gm:GroundModel, fg:Footing):

        self.data.length = fg.get("length",0)
        self.data.breadth = fg.get("breadth",0)
        self.data.depth = fg.get("depth",0)
        self.data.alpha_rad = fg.get("alpha_rad",0)

        self.data.vload = fg.get("vload",0)
        self.data.hload = fg.get("hload",0)
        self.data.htheta_rad = fg.get("htheta_rad",0)

        self.data.cu = gm.get_attr_value(self.data.depth, "cu")
        self.data.density = gm.get_attr_value(self.data.depth, "density")
        self.data.surcharge = gm.get_attr_value(self.data.depth, "EffectiveStress")
       
        self.calc_qult(self, self.data)
        return self.data.q_ult