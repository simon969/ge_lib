from dataclasses import dataclass


@dataclass
class cShearWaveSmallStrainStiffness:
    Vs: float = 0.0
    Vp: float = 0.0
    Cs: float = 0.0
    Cp: float = 0.0
    SigmaA: float = 0.0
    SigmaB: float = 0.0
    SigmaC: float = 0.0
    na: float = 0.235
    nb: float = 0.235
    nc: float = 0.0
    e: float = 0.0

    def _factor(self) -> float:
        return 1 / (self.e ** 1.3) * self.SigmaA ** self.na * self.SigmaB ** self.nb * self.SigmaC ** self.nc

    def calc_Vs(self) -> float:
        self.Vs = self.Cs * self._factor() ** 0.5
        return self.Vs

    def calc_Cs(self) -> float:
        self.Cs = self.Vs / self._factor() ** 0.5
        return self.Cs

    def calc_Vp(self) -> float:
        self.Vp = self.Cp * self._factor() ** 0.5
        return self.Vp

    def calc_Cp(self) -> float:
        self.Cp = self.Vp / self._factor() ** 0.5
        return self.Cp
