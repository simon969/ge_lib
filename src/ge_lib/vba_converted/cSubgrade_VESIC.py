from dataclasses import dataclass


@dataclass
class cSubgrade_VESIC:
    Es: float = 0.0
    Poisson: float = 0.0
    B: float = 0.0
    Ef: float = 0.0
    If: float = 0.0
    ks: float = 0.0

    def calcKs(self) -> float:
        self.ks = 0.65 * ((self.Es * self.B ** 4) / (self.Ef * self.If)) ** (1 / 12) * self.Es / (1 - self.Poisson ** 2) / self.B
        return self.ks
