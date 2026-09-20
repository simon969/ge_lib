from dataclasses import dataclass
import math


@dataclass
class cCoulomb:
    phi_rad: float = 0.0
    beta_rad: float = 0.0
    alpha_rad: float = 0.0
    delta_rad: float = 0.0
    cw: float = 0.0
    c: float = 0.0
    G: float = 0.0
    ka: float = 0.0
    kac: float = 0.0
    kpc: float = 0.0
    Kp: float = 0.0
    z0: float = 0.0
    const_PI: float = 3.14159

    def calc_Kp(self) -> float:
        s1 = (math.sin(self.alpha_rad - self.phi_rad)) ** 2
        s2 = math.sin(self.alpha_rad) ** 2 * math.sin(self.alpha_rad + self.delta_rad)
        s3 = (
            math.sin(self.phi_rad + self.delta_rad)
            * math.sin(self.phi_rad + self.beta_rad)
            / (math.sin(self.alpha_rad + self.delta_rad) * math.sin(self.alpha_rad + self.beta_rad))
        )
        denom = s2 * (1 - math.sqrt(s3)) ** 2
        if abs(denom) < 1e-12:
            self.Kp = 0.0
        else:
            self.Kp = s1 / denom
        return self.Kp

    def calc_Ka(self) -> float:
        s1 = (math.sin(self.alpha_rad + self.phi_rad)) ** 2
        s2 = math.sin(self.alpha_rad) ** 2 * math.sin(self.alpha_rad - self.delta_rad)
        s3 = (
            math.sin(self.phi_rad + self.delta_rad)
            * math.sin(self.phi_rad - self.beta_rad)
            / (math.sin(self.alpha_rad - self.delta_rad) * math.sin(self.alpha_rad + self.beta_rad))
        )
        denom = s2 * (1 + math.sqrt(s3)) ** 2
        if abs(denom) < 1e-12:
            self.ka = 0.0
        else:
            self.ka = s1 / denom
        return self.ka

    def calc_Kac(self) -> float:
        if self.c > 0:
            self.kac = 2 * math.sqrt(self.ka * (1 + self.cw / self.c))
        else:
            self.kac = 2 * math.sqrt(self.kac)
        return self.kac

    def calc_Kpc(self) -> float:
        if self.c > 0:
            self.kpc = 2 * math.sqrt(self.Kp * (1 + self.cw / self.c))
        else:
            self.kpc = 2 * math.sqrt(self.Kp)
        return self.kpc

    def calc_z0(self) -> float:
        if self.c > 0 and self.G * self.ka > 0:
            self.z0 = 2 * self.c * math.sqrt(1 + self.cw / self.c) / (self.G * math.sqrt(self.ka))
        else:
            self.z0 = 0.0
        return self.z0

    def calc(self) -> None:
        self.calc_Ka()
        self.calc_Kac()
        self.calc_Kp()
        self.calc_Kpc()
        self.calc_z0()

    def calc_Active(self, v: float) -> float:
        return v * self.ka - self.kac * self.c

    def calc_Passive(self, v: float) -> float:
        return v * self.Kp + self.kpc * self.c

    def calc_zc(self, p: float) -> float:
        if self.G > 0:
            return math.sqrt(self.ka ** 2 / (1 - self.ka ** 2)) * math.sqrt(2 * p / (self.const_PI * self.G))
        return 0.0

    def calc_hc(self, p: float) -> float:
        if self.G > 0:
            return (1 / self.ka) * math.sqrt(2 * p / (self.const_PI * self.G))
        return 0.0
