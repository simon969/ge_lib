from dataclasses import dataclass
import math


@dataclass
class cGRC_BrownBrayLadanyiHoek1983:
    R: float = 0.0
    phi_rad: float = 0.0
    dilation_rad: float = 0.0
    c: float = 0.0
    phi_res_rad: float = 0.0
    c_res: float = 0.0
    poisson: float = 0.0
    e: float = 0.0
    Pi: float = 0.0
    Po: float = 0.0
    Rp: float = 0.0
    Pcr: float = 0.0
    K: float = 0.0
    Nr: float = 0.0
    Ure: float = 0.0
    Urp: float = 0.0
    Ur: float = 0.0

    def calc_Pcr(self) -> float:
        self.Pcr = (1 - math.sin(self.phi_rad)) * self.Po - self.c * math.cos(self.phi_rad)
        return self.Pcr

    def calc_K(self) -> float:
        sine = math.sin(self.dilation_rad)
        self.K = (1 + sine) / (1 - sine) if 1 - sine else 0.0
        return self.K

    def calc_Nr(self) -> float:
        sine = math.sin(self.phi_rad)
        self.Nr = (1 + sine) / (1 - sine) if 1 - sine else 0.0
        return self.Nr

    def calc_Ure(self) -> float:
        self.Ure = (1 + self.poisson) / self.e * self.R * (self.Po - self.Pi)
        return self.Ure

    def calc_Rp(self) -> float:
        p1 = self.Po + self.c_res / math.tan(self.phi_res_rad)
        p2 = (self.Po + self.c / math.tan(self.phi_rad)) * math.cos(self.phi_rad)
        p3 = self.Pi + self.c_res / math.tan(self.phi_res_rad)
        p4 = (1 - math.sin(self.phi_res_rad)) / (2 * math.sin(self.phi_res_rad))
        self.Rp = self.R * ((p1 - p2) ** p4) / p3
        return self.Rp

    def calc_Urp(self) -> float:
        cot = self.c / math.tan(self.phi_rad)
        cot_res = self.c_res / math.tan(self.phi_res_rad)
        p1 = math.sin(self.phi_rad) * cot * self.Rp ** (self.K + 1) / self.R ** self.K
        p2 = (2 - 2 * self.poisson) * (self.Po + cot_res) / self.R ** self.K
        p3 = (1 + self.K * self.Nr - self.poisson * (self.K + 1) * (self.Nr + 1)) / ((self.Nr + self.K) * self.R ** (self.Nr - 1))
        p4 = (self.Pi + cot_res) * self.Rp ** (self.Nr + self.K) / self.R ** self.K * self.R ** self.Nr
        self.Urp = (1 + self.poisson) / self.e * (p1 + p2 - p3 * p4)
        return self.Urp

    def calc_Ur(self) -> float:
        self.calc_Pcr()
        self.calc_Ure()
        self.calc_K()
        self.calc_Nr()
        self.calc_Rp()
        self.calc_Urp()
        self.Ur = self.Ure if self.Pcr > 0 and self.Pi > self.Pcr else self.Urp + self.Ure
        return self.Ur
