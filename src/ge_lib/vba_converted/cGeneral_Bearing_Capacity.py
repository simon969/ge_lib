from dataclasses import dataclass
import math


@dataclass
class cGeneral_Bearing_Capacity:
    c: float = 0.0
    G: float = 0.0
    phi_rad: float = 0.0
    L: float = 0.0
    B: float = 0.0
    a: float = 0.0
    H: float = 0.0
    Htheta_rad: float = math.pi / 2
    v: float = 0.0
    alpha: float = 0.0
    nc: float = 0.0
    Sc: float = 0.0
    Ic: float = 0.0
    bc: float = 0.0
    dc: float = 0.0
    gc: float = 0.0
    nq: float = 0.0
    sq: float = 0.0
    iq: float = 0.0
    bq: float = 0.0
    dq: float = 0.0
    gq: float = 0.0
    ng: float = 0.0
    sg: float = 0.0
    ig: float = 0.0
    bg: float = 0.0
    dg: float = 0.0
    gg: float = 0.0
    M: float = 0.0
    mb: float = 0.0
    ml: float = 0.0
    mtheta: float = 0.0
    q_nc: float = 0.0
    q_ng: float = 0.0
    q_nq: float = 0.0
    q: float = 0.0
    const_PI: float = 3.14159

    def calc_Nc_EC7(self) -> float:
        return self.calc_Nc_Prandtl()

    def calc_Ng_EC7(self) -> float:
        return self.calc_Ng_Chen()

    def calc_bq(self) -> float:
        self.bq = (1 - self.alpha * math.tan(self.phi_rad)) ** 2
        return self.bq

    def calc_bc0(self) -> float:
        self.bc = self.bq - (1 - self.bq) / (self.nc * math.tan(self.phi_rad))
        return self.bc

    def calc_bg(self) -> float:
        self.bg = (1 - self.alpha * math.tan(self.phi_rad)) ** 2
        return self.bg

    def calc_bc1(self) -> float:
        self.bc = 1 - 2 * self.alpha / (self.const_PI + 2)
        return self.bc

    def calc_sc0(self) -> float:
        self.Sc = 1 + 0.2 * (self.B / self.L)
        return self.Sc

    def calc_sq(self) -> float:
        self.sq = 1 + (self.B / self.L) * math.sin(self.phi_rad)
        return self.sq

    def calc_sg(self) -> float:
        self.sg = 1 + 0.2 * (self.B / self.L)
        return self.sg

    def calc_sc1(self) -> float:
        self.Sc = (self.sq * self.nq - 1) / (self.nq - 1)
        return self.Sc

    def calc_Ic(self) -> float:
        self.Ic = self.iq - (1 - self.iq) / (self.nc * math.tan(self.phi_rad))
        return self.Ic

    def calc_iq(self) -> float:
        self.iq = (1 - self.H / (self.v + self.a * self.c / math.tan(self.phi_rad))) ** self.M
        return self.iq

    def calc_ig(self) -> float:
        self.ig = (1 - self.H / (self.v + self.a * self.c / math.tan(self.phi_rad))) ** (self.M + 1)
        return self.ig

    def calc_q_nc(self) -> float:
        self.q_nc = self.c * self.nc * self.bc * self.Sc * self.Ic * self.dc * self.gc
        return self.q_nc

    def calc_q_nq(self) -> float:
        self.q_nq = self.q * self.nq * self.bq * self.sq * self.iq * self.dq * self.gq
        return self.q_nq

    def calc_q_ng(self) -> float:
        self.q_ng = 0.5 * self.G * self.ng * self.bg * self.sg * self.ig * self.dg * self.gg
        return self.q_ng

    def calc_M(self) -> float:
        self.mb = (2 + (self.B / self.L)) / (1 + (self.B / self.L))
        self.ml = (2 + (self.L / self.B)) / (1 + (self.L / self.B))
        self.M = self.ml * math.cos(self.Htheta_rad) ** 2 + self.mb * math.sin(self.Htheta_rad) ** 2
        return self.M

    def calc_Ng_Brinch_Hansen(self) -> float:
        self.ng = 1.5 * (self.nq - 1) * math.tan(self.phi_rad)
        return self.ng

    def calc_Ng_Vesic(self) -> float:
        self.ng = 2 * (self.nq + 1) * math.tan(self.phi_rad)
        return self.ng

    def calc_Ng_Meyerhof(self) -> float:
        self.ng = (self.nq - 1) * math.tan(self.phi_rad)
        return self.ng

    def calc_Ng_Chen(self) -> float:
        self.ng = 2 * (self.nq - 1) * math.tan(self.phi_rad)
        return self.ng

    def calc_Nq_Reissner(self) -> float:
        self.nq = math.exp(self.const_PI * math.tan(self.phi_rad)) * math.tan(self.const_PI / 4 + self.phi_rad / 2) ** 2
        return self.nq

    def calc_Nc_Prandtl(self) -> float:
        self.nc = (self.nq - 1) / math.tan(self.phi_rad)
        return self.nc

    @staticmethod
    def calc_radians(phi_deg: float) -> float:
        return phi_deg / 180.0 * math.pi

    def calc_Ng(self, phi_deg: float, method: str = "MEYERHOF") -> float:
        self.phi_rad = self.calc_radians(phi_deg)
        self.calc_Nq_Reissner()
        method = method.upper()
        if "MEYERHOF" in method:
            self.calc_Ng_Meyerhof()
        if "CHEN" in method:
            self.calc_Ng_Chen()
        if "VESIC" in method:
            self.calc_Ng_Vesic()
        if "BRINCH" in method or "HANSEN" in method:
            self.calc_Ng_Brinch_Hansen()
        return self.ng

    def calc_Nq(self, phi_deg: float, method: str = "REISSNER") -> float:
        self.phi_rad = self.calc_radians(phi_deg)
        method = method.upper()
        if "REISSNER" in method or "EC7" in method:
            self.calc_Nq_Reissner()
        return self.nq
