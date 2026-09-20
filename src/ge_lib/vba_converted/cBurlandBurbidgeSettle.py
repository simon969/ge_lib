from dataclasses import dataclass
import math


@dataclass
class cBurlandBurbidgeSettle:
    fs: float = 0.0
    fl: float = 0.0
    ft: float = 0.0
    R3: float = 0.0
    Rt: float = 0.0
    t: float = 0.0
    Nvariation: int = -1
    ConsolState: int = -1
    LoadingType: int = -1
    Nave: float = 0.0
    B: float = 0.0
    L: float = 0.0
    Hs: float = 0.0
    Zi: float = 0.0
    Ic: float = 0.0
    q1: float = 0.0
    qv0: float = 0.0
    s0: float = 0.0
    ST: float = 0.0

    @staticmethod
    def _log10(x: float) -> float:
        return math.log10(x) if x > 0 else 0.0

    def calc_ft(self, t: float | None = None, LoadingType: int | None = None) -> float:
        if t is not None:
            self.t = t
        if LoadingType is not None:
            self.LoadingType = LoadingType

        if self.LoadingType == 1:
            self.R3 = 0.3
            self.Rt = 0.2
        elif self.LoadingType == 0:
            self.R3 = 0.7
            self.Rt = 0.8

        self.ft = 1 + self.R3 + self.Rt * self._log10(self.t / 3.0) if self.t > 0 else 0.0
        return self.ft

    def calc_Zi(self, B: float = 0.0, Nvariation: int | None = None) -> float:
        if B > 0:
            self.B = B
        if Nvariation is not None:
            self.Nvariation = Nvariation

        if self.Nvariation == 1:
            self.Zi = 10 ** (((math.exp(self.B)) / 1.34) / 2.3026)
        elif self.Nvariation == 0:
            self.Zi = 2 * self.B

        return self.Zi

    def calc_fs(self) -> float:
        self.fs = ((1.25 * self.L / self.B) / (self.L / self.B + 0.25)) ** 2
        return self.fs

    def calc_Ic(self, Nave: float | None = None) -> float:
        if Nave is not None:
            self.Nave = Nave
        self.Ic = 1.71 / (self.Nave ** 1.4) if self.Nave > 0 else 0.0
        return self.Ic

    def calc_fl(self, Hs: float | None = None, Zi: float | None = None) -> float:
        if Hs is not None:
            self.Hs = Hs
        if Zi is not None:
            self.Zi = Zi

        if self.Zi > 0:
            self.fl = self.Hs / self.Zi * (2 - self.Hs / self.Zi)
        else:
            self.fl = 0.0
        return self.fl

    def calc_s0(self, calc_derived: bool = False) -> float:
        if calc_derived:
            self.calc_Zi()
            self.calc_fs()
            self.calc_fl()
            self.calc_Ic()

        if self.ConsolState == 0:
            self.s0 = self.fs * self.fl * self.q1 * self.B ** 0.7 * self.Ic
        elif self.ConsolState == 1:
            if self.qv0 > self.q1:
                self.s0 = self.fs * self.fl * self.q1 * self.B ** 0.7 * self.Ic / 3.0
            else:
                self.s0 = self.fs * self.fl * ((self.q1 - 2.0 / 3.0 * self.qv0) * self.B ** 0.7 * self.Ic)
        else:
            self.s0 = 0.0

        return self.s0

    def calc_st(self, calc_derived: bool = False) -> float:
        if calc_derived:
            self.calc_s0(True)
            self.calc_ft(self.t, self.LoadingType)

        self.ST = self.s0 * self.ft
        return self.ST
