from dataclasses import dataclass


@dataclass
class cSkempton:
    d: float = 0.0
    B: float = 0.0
    DB: float = 0.0
    dc: float = 0.0

    def calc_DB(self) -> float:
        self.DB = self.d / self.B
        return self.DB

    def calc_dc(self) -> float:
        self.dc = 0.0053 * self.DB ** 3 - 0.0682 * self.DB ** 2 + 0.3003 * self.DB + 1.0085
        return self.dc
