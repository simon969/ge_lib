from dataclasses import dataclass, field
import math


@dataclass
class Strip:
    Ref: str = ""
    H: float = 0.0
    W: float = 0.0
    Td: float = 0.0
    L: float = 0.0
    Le: float = 0.0
    p: float = 0.0
    U: float = 0.0
    Ts: float = 0.0
    Tf: float = 0.0
    tP: float = 0.0
    Sv: float = 0.0


@dataclass
class cReinforcedWedge:
    H: float = 0.0
    Fl: float = 0.0
    Sl: float = 0.0
    gs: float = 0.0
    ws: float = 0.0
    fs: float = 0.0
    ff: float = 0.0
    fp: float = 0.0
    fn: float = 0.0
    ThetaRad: float = 0.0
    PhiRad: float = 0.0
    W: float = 0.0
    r: float = 0.0
    t: float = 0.0
    RT: float = 0.0
    _strips: list[Strip] = field(default_factory=list)
    const_PI: float = 3.14159

    @property
    def thetaRad(self) -> float:
        return self.ThetaRad

    @thetaRad.setter
    def thetaRad(self, value: float) -> None:
        self.ThetaRad = value

    @property
    def ThetaDeg(self) -> float:
        return self.ThetaRad * 180 / self.const_PI

    @ThetaDeg.setter
    def ThetaDeg(self, value: float) -> None:
        self.ThetaRad = value * self.const_PI / 180

    @property
    def PhiDeg(self) -> float:
        return self.PhiRad * 180 / self.const_PI

    @PhiDeg.setter
    def PhiDeg(self, value: float) -> None:
        self.PhiRad = value * self.const_PI / 180

    def count(self, value: int) -> None:
        self._strips = [Strip() for _ in range(value)]

    def Layer(self, Layerid: int, H: float, perimeter: float, Length: float, coefFriction: float, Td: float) -> None:
        while len(self._strips) < Layerid:
            self._strips.append(Strip())
        strip = self._strips[Layerid - 1]
        strip.H = H
        strip.p = perimeter
        strip.L = Length
        strip.U = coefFriction
        strip.Td = Td

    def _calc_tp(self, strip: Strip) -> Strip:
        strip.Le = strip.L - math.tan(self.const_PI / 2 - self.ThetaRad) * (self.H - strip.H)
        strip.tP = strip.p * strip.Le / (self.fp * self.fn) * (strip.U * self.fs * self.gs * strip.H + strip.U * self.ff * self.ws)
        return strip

    def CalcRT(self) -> float:
        self.W = self.H ** 2 * math.tan(self.const_PI / 2 - self.ThetaRad) * self.gs / 2 * self.fs + self.H * math.tan(self.const_PI / 2 - self.ThetaRad) * self.ws * self.ff
        psi = self.const_PI / 2 + self.PhiRad - self.ThetaRad
        self.r = (self.W + self.Sl) / math.sin(psi)
        self.t = self.r * math.cos(psi) + self.Fl
        self.RT = 0.0
        for strip in self._strips:
            if self.H > strip.H and strip.L > 0:
                self._calc_tp(strip)
                self.RT += min(strip.tP, strip.Td)
            else:
                strip.tP = 0.0
                strip.Le = 0.0
        return self.RT
