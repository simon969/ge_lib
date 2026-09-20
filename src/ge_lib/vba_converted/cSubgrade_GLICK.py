from dataclasses import dataclass
import math


@dataclass
class cSubgrade_GLICK:
    B: float = 0.0
    Es: float = 0.0
    Poisson: float = 0.0
    Lp: float = 0.0
    kh: float = 0.0

    def calc_kh(self) -> float:
        p1 = (1 + self.Poisson) * (3 - 4 * self.Poisson)
        p2 = 2 * math.log(2 * self.Lp / self.B) - 0.433
        self.kh = 22.4 * self.Es * (1 - self.Poisson) / (p1 * p2)
        return self.kh
