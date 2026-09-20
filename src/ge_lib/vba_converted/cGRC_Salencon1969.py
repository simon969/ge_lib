from dataclasses import dataclass, field
from .cCircularHoleMC_Salencon1969 import cCircularHoleMC_Salencon1969


@dataclass
class cGRC_Salencon1969:
    model: cCircularHoleMC_Salencon1969 = field(default_factory=cCircularHoleMC_Salencon1969)
    Pcr: float = 0.0
    Rp: float = 0.0
    Ure: float = 0.0
    Urp: float = 0.0
    Ur: float = 0.0

    def calc_Pcr(self) -> float:
        self.Pcr = (1 - __import__('math').sin(self.model.phi_rad)) * self.model.Po - self.model.c * __import__('math').cos(self.model.phi_rad)
        return self.Pcr

    def calc_Ure(self) -> float:
        self.Ure = 0.0
        return self.Ure

    def calc_Urp(self) -> float:
        self.Urp = 0.0
        return self.Urp

    def calc_Rp(self) -> float:
        self.model.calc_Ro()
        self.Rp = self.model.Ro
        return self.Rp

    def calc_Ur(self) -> float:
        self.calc_Pcr()
        self.calc_Ure()
        self.calc_Rp()
        self.calc_Urp()
        self.Ur = self.Ure if self.model.Pi > self.Pcr and self.Pcr > 0 else self.Urp + self.Ure
        return self.Ur
