from dataclasses import dataclass


@dataclass
class cSubgrade_PHRI:
    Ah: float = 0.0
    alphak: float = 0.0
    beta: float = 0.0
    EI: float = 0.0
    Eo: float = 0.0
    E30: float = 0.0
    Ip: float = 0.0
    D: float = 0.0
    Poisson: float = 0.0
    Ef: float = 0.0
    kh: float = 0.0
    k30: float = 0.0

    def calc_kh(self) -> float:
        return self.kh

    def calc_kh30(self) -> float:
        self.kh = self.k30 / 30 * self.alphak * self.Eo
        return self.kh
