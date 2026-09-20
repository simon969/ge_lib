from dataclasses import dataclass
import math


@dataclass
class cOReillyNew:
    K: float = 0.0
    z0: float = 0.0
    i: float = 0.0
    y: float = 0.0
    Smax: float = 0.0
    Sv: float = 0.0
    Sh: float = 0.0
    Vloss: float = 0.0
    const_PI: float = 3.14159

    def calc_Sv(self) -> float:
        self.Sv = self.Smax * math.exp(-self.y ** 2 / (2 * self.i ** 2))
        return self.Sv

    def calc_Sh(self) -> float:
        self.Sh = self.y / self.z0 * self.Sv
        return self.Sh

    def calc_i(self) -> float:
        self.i = self.K * self.z0
        return self.i

    def calc_Smax(self) -> float:
        self.Smax = self.Vloss / (math.sqrt(2 * self.const_PI) * self.i)
        return self.Smax

    def calc(self) -> None:
        self.calc_i()
        if self.i > 0 and self.Vloss > 0:
            self.calc_Smax()
        else:
            self.Smax = 0.0
        self.calc_Sv()
        self.calc_Sh()
