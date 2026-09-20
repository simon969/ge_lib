from dataclasses import dataclass


@dataclass
class cElastic_Constants:
    Lames: float = 0.0
    K: float = 0.0
    G: float = 0.0
    E: float = 0.0
    M: float = 0.0
    poisson: float = 0.0

    def get_value(self, var: str) -> float:
        key = var.upper()
        values = {
            "K": self.K,
            "E": self.E,
            "G": self.G,
            "LAMDA": self.Lames,
            "POISSON": self.poisson,
            "M": self.M,
        }
        return values.get(key, 0.0)

    def set_value(self, var: str, val: float) -> None:
        key = var.upper()
        if key == "K":
            self.K = val
        elif key == "E":
            self.E = val
        elif key == "G":
            self.G = val
        elif key == "LAMDA":
            self.Lames = val
        elif key == "POISSON":
            self.poisson = val
        elif key == "M":
            self.M = val

    def calc_LamesG(self, var: str | None = None) -> float:
        self.K = self.Lames + (2 * self.G / 3)
        self.E = self.G * (3 * self.Lames + 2 * self.G) / (self.Lames + self.G)
        self.poisson = self.Lames / (2 * (self.Lames + self.G))
        self.M = self.Lames + 2 * self.G
        if var and len(var) > 0:
            return self.get_value(var)
        return self.K

    def calc_EG(self, var: str | None = None) -> float:
        self.K = self.E * self.G / (3 * (3 * self.G - self.E))
        self.Lames = self.G * (self.E - 2 * self.G) / (3 * self.G - self.E)
        self.poisson = self.E / (2 * self.G) - 1
        self.M = self.G * (4 * self.G - self.E) / (3 * self.G - self.E)
        if var and len(var) > 0:
            return self.get_value(var)
        return self.K

    def calc_EPoisson(self, var: str | None = None) -> float:
        self.K = self.E / (3 * (1 - 2 * self.poisson))
        self.Lames = self.E * self.poisson / ((1 + self.poisson) * (1 - 2 * self.poisson))
        self.G = self.E / (2 * (1 + self.poisson))
        self.M = self.E * (1 - self.poisson) / ((1 + self.poisson) * (1 - 2 * self.poisson))
        if var and len(var) > 0:
            return self.get_value(var)
        return self.K

    def calc_KLames(self, var: str | None = None) -> float:
        if var and len(var) > 0:
            return self.get_value(var)
        return self.K

    def calc_KG(self, var: str | None = None) -> float:
        self.E = 9 * self.K * self.G / (3 * self.K + self.G)
        self.Lames = self.K - 2 * self.G / 3
        self.poisson = (3 * self.K - 2 * self.G) / (2 * (3 * self.K + self.G))
        self.M = self.K * 4 * self.G / 3
        if var and len(var) > 0:
            return self.get_value(var)
        return self.K
