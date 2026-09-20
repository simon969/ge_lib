from dataclasses import dataclass
import math


@dataclass
class cModifiedCamClay:
    Lambda: float = 0.0
    Kappa: float = 0.0
    poissonUR: float = 0.0
    KoNC: float = 0.0
    M: float = 0.0

    def calc_M(self) -> float:
        p1 = (1 - self.KoNC) ** 2
        p2 = (1 + 2 * self.KoNC) ** 2
        p3 = (1 - self.KoNC) * (1 - 2 * self.poissonUR) * (self.Lambda / self.Kappa - 1)
        p4 = (
            (1 + 2 * self.KoNC) * (1 - 2 * self.poissonUR) * self.Lambda / self.Kappa
            - (1 - self.KoNC) * (1 + self.poissonUR)
        )
        self.M = 3 * math.sqrt(p1 / p2 + p3 / p4)
        return self.M
