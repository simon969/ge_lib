from dataclasses import dataclass
import math


@dataclass
class cGRC_Eberhardt:
    R: float = 0.0
    phi_rad: float = 0.0
    c: float = 0.0
    ucs: float = 0.0
    poisson: float = 0.0
    e: float = 0.0
    Pi: float = 0.0
    Po: float = 0.0
    Rp: float = 0.0
    Pcr: float = 0.0
    K: float = 0.0
    Ure: float = 0.0
    Urp: float = 0.0
    Ur: float = 0.0
    const_PI: float = 3.14159

    def calc_ucs(self) -> float:
        self.ucs = 2 * self.c * math.cos(self.phi_rad) / (1 - math.sin(self.phi_rad))
        return self.ucs

    def calc_K(self) -> float:
        sine = math.sin(self.phi_rad)
        self.K = (1 + sine) / (1 - sine) if 1 - sine else 0.0
        return self.K

    def calc_Pcr(self) -> float:
        self.Pcr = (2 * self.Po - self.ucs) / (1 + self.K)
        return self.Pcr

    def calc_Ure(self) -> float:
        self.Ure = (1 + self.poisson) / self.e * self.R * (self.Po - self.Pi)
        return self.Ure

    def calc_Rp(self) -> float:
        p1 = 2 * (self.Po * (self.K - 1) + self.ucs)
        p2 = (1 + self.K) * ((self.K - 1) * self.Pi + self.ucs)
        self.Rp = self.R * (p1 / p2) ** (1 / (self.K - 1))
        return self.Rp

    def calc_Urp(self) -> float:
        p1 = 2 * (1 - self.poisson) * (self.Po - self.Pcr) * (self.Rp / self.R) ** 2
        p2 = (1 - 2 * self.poisson) * (self.Po - self.Pi)
        self.Urp = self.R * (1 + self.poisson) / self.e * (p1 - p2)
        return self.Urp

    def calc_Ur(self) -> float:
        self.calc_ucs()
        self.calc_K()
        self.calc_Pcr()
        self.calc_Ure()
        self.calc_Rp()
        self.calc_Urp()
        self.Ur = self.Ure if self.Pcr > 0 and self.Pi > self.Pcr else self.Urp + self.Ure
        return self.Ur
