from dataclasses import dataclass
import math


@dataclass
class cMeyerhof_Bearing_Capacity:
    c: float = 0.0
    G: float = 0.0
    phi_rad: float = 0.0
    L: float = 0.0
    B: float = 0.0
    d: float = 0.0
    beta_rad: float = 0.0
    nc: float = 0.0
    Sc: float = 0.0
    Ic: float = 0.0
    dc: float = 0.0
    nq: float = 0.0
    sq: float = 0.0
    iq: float = 0.0
    dq: float = 0.0
    ng: float = 0.0
    sg: float = 0.0
    ig: float = 0.0
    dg: float = 0.0
    kpr: float = 0.0
    q_nc: float = 0.0
    q_ng: float = 0.0
    q_nq: float = 0.0
    q: float = 0.0
    const_PI: float = 3.14159

    def calc_Nq(self) -> float:
        self.nq = math.exp(self.const_PI * math.tan(self.phi_rad)) * math.tan(self.const_PI / 4 + self.phi_rad / 2)
        return self.nq

    def calc_Nc(self) -> float:
        self.nc = (self.nq - 1) / math.tan(self.phi_rad)
        return self.nc

    def calc_Ng(self) -> float:
        self.ng = 2 * (self.nq - 1) * math.tan(self.phi_rad)
        return self.ng

    def calc_Kpr(self) -> float:
        self.kpr = math.tan(self.const_PI / 4 + self.phi_rad / 2) ** 2
        return self.kpr

    def calc_dq(self) -> float:
        self.dq = 1 + 2 * math.tan(self.phi_rad) * (1 - math.sin(self.phi_rad)) ** 2 * self.d / self.B
        return self.dq

    def calc_dg(self) -> float:
        self.dg = 1.0
        return self.dg

    def calc_dc(self) -> float:
        self.dc = 1 + 0.4 * self.d / self.B
        return self.dc

    def calc_sc(self) -> float:
        self.Sc = 1 + 0.2 * self.kpr * (self.B / self.L)
        return self.Sc

    def calc_sq(self) -> float:
        if self.phi_rad < 2 * self.const_PI / 360 * 10:
            self.sq = 1.0
        else:
            self.sq = 1 + 0.1 * self.kpr * (self.B / self.L)
        return self.sq

    def calc_sg(self) -> float:
        if self.phi_rad < 2 * self.const_PI / 360 * 10:
            self.sg = 1.0
        else:
            self.sg = 1 + 0.1 * self.kpr * (self.B / self.L)
        return self.sg

    def calc_Ic(self) -> float:
        self.Ic = (1 - self.beta_rad / (self.const_PI / 2)) ** 2
        return self.Ic

    def calc_iq(self) -> float:
        self.iq = (1 - self.beta_rad / (self.const_PI / 2)) ** 2
        return self.iq

    def calc_ig(self) -> float:
        if self.phi_rad < 2 * self.const_PI / 360 * 10:
            self.ig = 1.0
        else:
            self.ig = (1 - self.beta_rad / self.phi_rad) ** 2
        return self.ig

    def calc_q_nc(self) -> float:
        self.calc_Nc()
        self.calc_Ic()
        self.calc_dc()
        self.calc_Kpr()
        self.calc_sc()
        self.q_nc = self.c * self.nc * self.Sc * self.Ic * self.dc
        return self.q_nc

    def calc_q_nq(self) -> float:
        self.calc_Nq()
        self.calc_iq()
        self.calc_dq()
        self.calc_Kpr()
        self.calc_sq()
        self.q_nq = self.q * self.nq * self.dq * self.sq * self.iq
        return self.q_nq

    def calc_q_ng(self) -> float:
        self.calc_Ng()
        self.calc_ig()
        self.calc_dg()
        self.calc_sg()
        self.q_ng = 0.5 * self.G * self.ng * self.sg * self.ig * self.dg
        return self.q_ng

    def calc(self) -> float:
        self.calc_q_nc()
        self.calc_q_nq()
        self.calc_q_ng()
        self.q = self.q_nc + self.q_ng + self.q_nq
        return self.q
