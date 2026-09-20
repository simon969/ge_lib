from dataclasses import dataclass
import math


@dataclass
class cInfluenceFactors:
    M: float = 0.0
    N: float = 0.0
    N2: float = 0.0
    M2: float = 0.0
    I1: float = 0.0
    I2: float = 0.0
    const_PI: float = 3.14159

    @property
    def letM(self) -> float:
        return self.M

    @letM.setter
    def letM(self, value: float) -> None:
        self.M = value
        self.M2 = value ** 2

    @property
    def letN(self) -> float:
        return self.N

    @letN.setter
    def letN(self, value: float) -> None:
        self.N = value
        self.N2 = value ** 2

    def calc_I1(self) -> float:
        p1 = (1 + math.sqrt(self.M2 + 1)) * math.sqrt(self.M2 + self.N2)
        p2 = self.M * (1 + math.sqrt(self.M2 + self.N2 + 1))
        p3 = (self.M + math.sqrt(self.M2 + 1)) * math.sqrt(1 + self.N2)
        p4 = self.M + math.sqrt(self.M2 + self.N2 + 1)
        self.I1 = (self.M * math.log(p1 / p2) + math.log(p3 / p4)) / self.const_PI
        return self.I1

    def calc_I2(self) -> float:
        p1 = self.M / (self.N * math.sqrt(self.M2 + self.N2 + 1))
        self.I2 = self.N / (2 * self.const_PI) * math.atan(p1)
        return self.I2
