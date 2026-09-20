from dataclasses import dataclass
import math


@dataclass
class cCircularHoleElastic:
    p1: float = 0.0
    P2: float = 0.0
    G: float = 0.0
    poisson: float = 0.0
    a: float = 0.0
    R: float = 0.0
    theta: float = 0.0
    a2r2: float = 0.0
    a4r4: float = 0.0
    a2r4g: float = 0.0
    SR: float = 0.0
    ST: float = 0.0
    SS: float = 0.0
    Ur: float = 0.0
    UT: float = 0.0

    def calc(self) -> None:
        self.a2r2 = self.a ** 2 / self.R ** 2
        self.a4r4 = self.a ** 4 / self.R ** 4
        self.SR = ((self.p1 + self.P2) / 2 * (1 - self.a2r2) + (self.p1 - self.P2) / 2 * (1 - 4 * self.a2r2 + 3 * self.a4r4) * math.cos(2 * self.theta))
        self.ST = ((self.p1 + self.P2) / 2 * (1 + self.a2r2) - (self.p1 - self.P2) / 2 * (1 + 3 * self.a4r4) * math.cos(2 * self.theta))
        self.SS = -(self.p1 - self.P2) / 2 * (1 + 2 * self.a2r2 - 3 * self.a4r4) * math.sin(2 * self.theta)
        if self.G > 0:
            self.a2r4g = self.a ** 2 / (4 * self.G * self.R)
            self.Ur = (self.p1 + self.P2) * self.a2r4g + (self.p1 - self.P2) * self.a2r4g * (4 * (1 - self.poisson) - self.a2r2) * math.cos(2 * self.theta)
            self.UT = -(self.p1 - self.P2) * self.a2r4g * (2 * (1 - 2 * self.poisson) + self.a2r2) * math.sin(2 * self.theta)
        else:
            self.Ur = 0.0
            self.UT = 0.0

    @property
    def theta_rad(self) -> float:
        return self.theta

    @theta_rad.setter
    def theta_rad(self, value: float) -> None:
        self.theta = value

    @property
    def Theta_Deg(self) -> float:
        return self.theta * 180 / 3.14159

    @Theta_Deg.setter
    def Theta_Deg(self, value: float) -> None:
        self.theta = value * 3.14159 / 180
