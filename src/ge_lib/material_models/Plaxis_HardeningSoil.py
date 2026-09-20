from dataclasses import dataclass, field
import math


@dataclass
class PlaxisHS:
    Cc: float = 0.0
    Cs: float = 0.0
    pref: float = 0.0
    eint: float = 0.0
    Ko: float = 0.0
    poisson: float = 0.0
    E: float = 0.0
    E50: float = 0.0
    Eu: float = 0.0
    Rf: float = 0.9

    # internal / derived values
    poisson_u: float = 0.495
    G: float = 0.0
    Ku: float = 0.0
    Eoed: float = 0.0
    Eur: float = 0.0
    q: float = 0.0
    qf: float = 0.0
    qa: float = 0.0
    alpha: float = 0.0
    Ei: float = 0.0

    def calc_eoed(self) -> float:
        self.Eoed = 2.3 * (1 + self.eint) * self.pref / self.Cc
        return self.Eoed

    def calc_eur(self) -> float:
        self.Eur = (
            2.3
            * (1 + self.eint)
            * (1 + self.poisson)
            * (1 - 2 * self.poisson)
            * self.pref
            / ((1 - self.poisson) * self.Cs * self.Ko)
        )
        return self.Eur

    def calc_q(self, s1: float, s2: float, s3: float) -> float:
        self.q = s1 + (self.alpha - 1) * s2 - self.alpha * s3
        return self.q

    def calc_qf(self, c: float, phi_rad: float, s3: float) -> float:
        self.qf = (
            c / math.tan(phi_rad)
            - s3 * (2 * math.sin(phi_rad)) / (1 - math.sin(phi_rad))
        )
        self.qa = self.qf / self.Rf
        return self.qa

    def calc_eu(self) -> float:
        self.G = self.E / (2 * (1 + self.poisson))
        self.Ku = self.G * (1 + self.poisson_u) / (3 * (1 - 2 * self.poisson_u))
        self.Eu = 2 * self.G * (1 + self.poisson_u)
        return self.Eu

    def calc_alpha(self, phi_rad: float) -> float:
        self.alpha = (3 + math.sin(phi_rad)) / (3 - math.sin(phi_rad))
        return self.alpha

    def calc_e1(self, s1: float, s2: float, s3: float) -> float:
        self.calc_q(s1, s2, s3)
        self.Ei = 2 * self.E50 / (2 - self.Rf)
        return self.Ei