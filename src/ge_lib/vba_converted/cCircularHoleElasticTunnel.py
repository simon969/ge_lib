from dataclasses import dataclass
import math


@dataclass
class cCircularHoleElasticTunnel:
    mR: float = 0.0
    mK: float = 0.0
    mP: float = 0.0
    mTheta: float = 0.0
    mEs: float = 0.0
    mPS: float = 0.0
    mET: float = 0.0
    mPT: float = 0.0
    mA: float = 0.0
    mI: float = 0.0
    mSlipStatus: int = 0
    mUs: float = 0.0
    mVs: float = 0.0
    mT: float = 0.0
    mM: float = 0.0
    mSR: float = 0.0
    mST: float = 0.0
    intNoSlip: int = 0
    intFullSlip: int = 1

    def init(self, Radius: float, Ko: float, Pvert: float, theta_rad: float, E_soil: float, Poiss_soil: float, E_tun: float, Poiss_tun: float, A_tun: float, I_tun: float) -> None:
        self.mR, self.mK, self.mP, self.mTheta = Radius, Ko, Pvert, theta_rad
        self.mEs, self.mPS, self.mET, self.mPT = E_soil, Poiss_soil, E_tun, Poiss_tun
        self.mA, self.mI = A_tun, I_tun
        self.calc_NoSlip()

    def calc_NoSlip(self) -> None:
        c = self.mEs * self.mR * (1 - self.mPT ** 2) / (self.mET * self.mA * (1 - self.mPS ** 2))
        F = self.mEs * self.mR ** 3 * (1 - self.mPT ** 2) / (self.mET * self.mI * (1 - self.mPS ** 2))
        d1 = self.mP * self.mR * (1 + self.mPS) / self.mEs
        M1 = self.mP * self.mR ** 2 / 2
        f1 = self.mP * self.mR / 2
        beta = ((6 + F) * c * (1 - self.mPS) + 2 * F * self.mPS) / (3 * F + 3 * c + 2 * c * F * (1 - self.mPS))
        b2 = c * (1 - self.mPS) / (2 * (c * (1 - self.mPS) + 4 * self.mPS - 6 * beta - 3 * beta * c * (1 - self.mPS)))
        a2 = beta * b2
        a0 = c * F * (1 - self.mPS) / (c + F + c * F * (1 - self.mPS))
        angle = 2 * self.mTheta
        self.mUs = d1 * ((1 + self.mK) * a0 / 2 + (1 - self.mK) / 2 * (4 * (1 - self.mPS) * b2 - 2 * a2) * math.cos(angle))
        self.mVs = d1 * (-(1 - self.mK) * (a2 + (1 - 2 * self.mPS) * b2) * math.sin(angle))
        self.mSR = self.mP / 2 * ((1 + self.mK) * (1 - a0) - (1 - self.mK) * (1 - 6 * a2 + 4 * b2) * math.cos(angle))
        self.mST = self.mP / 2 * ((1 - self.mK) * (1 + 6 * a2 - 2 * b2) * math.sin(angle))
        self.mT = f1 * ((1 + self.mK) * (1 - a0) + (1 - self.mK) * (1 + 2 * a2) * math.cos(angle))
        self.mM = M1 * 0.5 * (1 - self.mK) * (1 - 2 * a2 + 2 * b2) * math.cos(angle)
        self.mSlipStatus = self.intNoSlip

    def calc_FullSlip(self) -> None:
        self.mSlipStatus = self.intFullSlip
        self.calc_NoSlip()

    def calc(self) -> None:
        if self.mSlipStatus == self.intFullSlip:
            self.calc_FullSlip()
        else:
            self.calc_NoSlip()
