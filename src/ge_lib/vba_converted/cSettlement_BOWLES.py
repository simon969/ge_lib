from dataclasses import dataclass
import math


@dataclass
class cInfluenceFactors:
    M: float = 0.0
    N: float = 0.0
    M2: float = 0.0
    N2: float = 0.0
    I1: float = 0.0
    I2: float = 0.0
    const_PI: float = 3.14159

    def set_values(self, M: float, N: float) -> None:
        self.M = M
        self.N = N
        self.M2 = self.M ** 2
        self.N2 = self.N ** 2

    def calc_I1(self) -> float:
        p1 = (1 + (self.M2 + 1) ** 0.5) * (self.M2 + self.N2) ** 0.5
        p2 = self.M * (1 + (self.M2 + self.N2 + 1) ** 0.5)
        p3 = (self.M + (self.M2 + 1) ** 0.5) * (1 + self.N2) ** 0.5
        p4 = self.M + (self.M2 + self.N2 + 1) ** 0.5
        self.I1 = 1 / self.const_PI * (self.M * math.log(p1 / p2) + math.log(p3 / p4))
        return self.I1

    def calc_I2(self) -> float:
        p1 = self.M / (self.N * (self.M2 + self.N2 + 1) ** 0.5)
        self.I2 = self.N / (2 * self.const_PI) * math.atan(p1)
        return self.I2


@dataclass
class cDepthFactor:
    values: list[list[float]] | None = None

    def __post_init__(self):
        if self.values is None:
            self.values = [
                [0.93, 0.91, 0.895, 0.875, 0.86, 0.85, 0.75, 0.69, 0.65, 0.625, 0.558],
                [0.87, 0.85, 0.83, 0.81, 0.795, 0.78, 0.675, 0.62, 0.585, 0.565, 0.51],
                [0.86, 0.822, 0.79, 0.765, 0.745, 0.725, 0.625, 0.59, 0.57, 0.555, 0.525],
                [0.775, 0.74, 0.715, 0.69, 0.67, 0.65, 0.565, 0.53, 0.515, 0.5, 0.5],
            ]

    def get_x(self, DoverB: float, offset: int) -> float:
        if offset < 1 or offset > 4:
            raise ValueError("offset out of range")
        x_index = min(max(int(DoverB), 1), 11) - 1
        return self.values[offset - 1][x_index]

    def get_DepthFactor(self, LoverB: float, Poisson: float, DoverB: float) -> float:
        if Poisson > 0.5:
            Poisson = 0.5
        if Poisson < 0.3:
            Poisson = 0.3
        if LoverB < 1:
            LoverB = 1
        if LoverB > 5:
            LoverB = 5

        offset = self.getXOffset(LoverB, Poisson)
        if offset == 0:
            valLB1P3 = self.get_x(DoverB, 4)
            valLB5P3 = self.get_x(DoverB, 2)
            valLB1P5 = self.get_x(DoverB, 3)
            valLB5P5 = self.get_x(DoverB, 1)

            LBFactor = (LoverB - 1) / (5 - 1)
            PoissonFactor = (Poisson - 0.3) / (0.5 - 0.3)

            valP3 = (valLB5P3 - valLB1P3) * LBFactor + valLB1P3
            valP5 = (valLB5P5 - valLB1P5) * LBFactor + valLB1P5
            return (valP5 - valP3) * PoissonFactor + valP3

        return self.get_x(DoverB, offset)

    @staticmethod
    def getXOffset(LoverB: float, Poisson: float) -> int:
        if LoverB == 5 and Poisson == 0.5:
            return 1
        if LoverB == 5 and Poisson == 0.3:
            return 2
        if LoverB == 1 and Poisson == 0.5:
            return 3
        if LoverB == 1 and Poisson == 0.3:
            return 4
        return 0


@dataclass
class cSettlement_BOWLES:
    mEs: float = 0.0
    mH: float = 0.0
    mdH: float = 0.0
    mqo: float = 0.0
    mPoisson: float = 0.0
    mM: float = 1.0
    mB: float = 0.0
    mL: float = 0.0
    mIs_B: float = 0.0
    mIs_L: float = 0.0
    mD: float = 0.0
    mIf: float = 0.0
    mIs: float = 0.0
    mI1: float = 0.0
    mI2: float = 0.0
    mks: float = 0.0

    def calcIs(self) -> float:
        ifactors = cInfluenceFactors()
        ifactors.set_values(self.mIs_L / self.mIs_B, self.mH / self.mB)
        self.mI1 = ifactors.calc_I1()
        self.mI2 = ifactors.calc_I2()
        self.mIs = self.mI1 + (1 - 2 * self.mPoisson) / (1 - self.mPoisson) * self.mI2
        return self.mIs

    def calcIf(self) -> float:
        df = cDepthFactor()
        self.mIf = df.get_DepthFactor(self.mL / self.mB, self.mPoisson, self.mD / self.mB)
        return self.mIf

    def calcKs(self) -> float:
        self.calcIs()
        self.calcIf()
        self.mks = self.mEs / (1 - self.mPoisson ** 2) / (self.mIs_B * self.mM * self.mIs * self.mIf)
        return self.mks

    def calcSettlement(self) -> float:
        self.calcIs()
        self.calcIf()
        self.mdH = self.mqo * self.mIs_B * (1 - self.mPoisson ** 2) / self.mEs * self.mM * self.mIs * self.mIf
        return self.mdH
