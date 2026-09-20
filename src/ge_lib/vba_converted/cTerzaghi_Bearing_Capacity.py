from dataclasses import dataclass
import math


@dataclass
class cTerzaghi_Bearing_Capacity:
    c: float = 0.0
    q: float = 0.0
    G: float = 0.0
    phi_rad: float = 0.0
    B: float = 0.0
    nc: float = 0.0
    nq: float = 0.0
    ng: float = 0.0
    q_nc: float = 0.0
    q_ng: float = 0.0
    q_nq: float = 0.0
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

    def calc_q_nc(self) -> float:
        self.calc_Nq()
        self.calc_Nc()
        self.q_nc = self.nc * self.c
        return self.q_nc

    def calc_q_ng(self) -> float:
        self.calc_Nq()
        self.calc_Ng()
        self.q_ng = 0.5 * self.B * self.G * self.ng
        return self.q_ng

    def calc_q_nq(self) -> float:
        self.calc_Nq()
        self.q_nq = self.q * self.nq
        return self.q_nq

    def calc(self) -> float:
        self.calc_q_nc()
        self.calc_q_ng()
        self.calc_q_nq()
        self.q = self.q_nc + self.q_ng + self.q_nq
        return self.q
from dataclasses import dataclass
import math


@dataclass
class cTerzaghi_Bearing_Capacity:
    c: float = 0.0
    q: float = 0.0
    G: float = 0.0
    B: float = 0.0
    phi_rad: float = 0.0
    nc: float = 0.0
    nq: float = 0.0
    ng: float = 0.0
    q_nc: float = 0.0
    q_ng: float = 0.0
    q_nq: float = 0.0
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

    def calc_q_nc(self) -> float:
        self.calc_Nq()
        self.calc_Nc()
        self.q_nc = self.nc * self.c
        return self.q_nc

    def calc_q_ng(self) -> float:
        self.calc_Nq()
        self.calc_Ng()
        self.q_ng = 0.5 * self.B * self.G * self.ng
        return self.q_ng

    def calc_q_nq(self) -> float:
        self.calc_Nq()
        self.q_nq = self.q * self.nq
        return self.q_nq

    def calc(self) -> float:
        self.calc_q_nc()
        self.calc_q_ng()
        self.calc_q_nq()
        self.q = self.q_nc + self.q_ng + self.q_nq
        return self.q
