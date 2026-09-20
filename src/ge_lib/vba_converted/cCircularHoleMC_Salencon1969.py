from dataclasses import dataclass
import math


@dataclass
class cCircularHoleMC_Salencon1969:
    a: float = 0.0
    R: float = 0.0
    Pi: float = 0.0
    Po: float = 0.0
    Pcr: float = 0.0
    phi_rad: float = 0.0
    dilation_rad: float = 0.0
    c: float = 0.0
    poisson: float = 0.0
    G: float = 0.0
    q: float = 0.0
    Kp: float = 0.0
    Kps: float = 0.0
    Si: float = 0.0
    Ro: float = 0.0
    State: int = 0
    stressR: float = 0.0
    stressT: float = 0.0
    dispR: float = 0.0

    def calc_Kp(self) -> float:
        sine = math.sin(self.phi_rad)
        self.Kp = (1 + sine) / (1 - sine) if 1 - sine else 0.0
        return self.Kp

    def calc_Kps(self) -> float:
        sine = math.sin(self.dilation_rad)
        self.Kps = (1 + sine) / (1 - sine) if 1 - sine else 0.0
        return self.Kps

    def calc_q(self) -> float:
        self.q = self.c * math.tan(3.14159 / 4 + self.phi_rad / 2)
        return self.q

    def calc_Ro(self) -> float:
        self.calc_q()
        self.calc_Kp()
        p1 = self.q / (self.Kp - 1)
        p2 = 0.0 if self.Kp == 1 else 1 / (self.Kp - 1)
        self.Ro = self.a * (2 / (self.Kp + 1) * (self.Po + p1) / (self.Pi + p1)) ** p2
        self.Pcr = (2 * self.Po - self.q) / (self.Kp + 1)
        return self.Ro

    def _elastic_region(self) -> None:
        self.stressR = -self.Po + (self.Po - self.Pcr) * (self.Ro / self.R) ** 2
        self.stressT = -self.Po - (self.Po - self.Pcr) * (self.Ro / self.R) ** 2
        self.dispR = -(self.Po - (2 * self.Po - self.q) / (self.Kp + 1)) * self.Ro / (2 * self.G) * self.Ro / self.R

    def _plastic_region(self) -> None:
        self.calc_Kps()
        p1 = self.q / (self.Kp - 1)
        p2 = 0.0 if self.Kp <= 1 else self.Kp - 1
        p3 = self.Kp + 1
        p4 = (1 - self.poisson) * self.Kp ** 2 - 1 / (self.Kp + self.Kps)
        p5 = (self.Pi + p1) * (self.Ro / self.a) ** p2 * (self.Ro / self.R) ** p3
        p6 = (2 - self.poisson) * (self.Po + p1)
        p7 = (1 - self.poisson) * (self.Kp * self.Kps + 1) / (self.Kp + self.Kps) + self.poisson
        p8 = (self.Pi + p1) * (self.R / self.a) ** p2
        self.Si = p6 + p4 * p5 + p7 * p8
        self.stressR = p1 - (self.Pi + p1) * (self.R / self.a) ** p2
        self.stressT = p1 - self.Kp * (self.Pi + p1) * (self.R / self.a) ** p2
        self.dispR = -self.R / (2 * self.G) * self.Si

    def calc(self) -> None:
        self.calc_Ro()
        if self.R == self.Ro:
            self.State = 0
            self.stressR = self.Pcr
            self.stressT = 0.0
            self.dispR = 0.0
        elif self.R < self.Ro:
            self.State = -1
            self._plastic_region()
        else:
            self.State = 1
            self._elastic_region()
