from dataclasses import dataclass


@dataclass
class cSubgrade_TERZAGHI:
    Es: float = 0.0
    Poisson: float = 0.0
    B: float = 0.0
    Ip: float = 0.0
    ks: float = 0.0

    def calcKs(self) -> float:
        self.ks = self.Es / (self.Ip * (1 - self.Poisson ** 2) / self.B)
        return self.ks
