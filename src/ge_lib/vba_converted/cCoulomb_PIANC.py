from dataclasses import dataclass
import math


@dataclass
class cCoulomb_PIANC:
    phi_rad: float = 0.0
    w1_rad: float = 0.0
    delta_rad: float = 0.0
    kae: float = 0.0
    Ka: float = 0.0
    kpe: float = 0.0
    Kp: float = 0.0

    def calc_kae(self) -> float:
        root = math.sqrt(math.sin(self.phi_rad + self.delta_rad) * math.sin(self.phi_rad - self.w1_rad) / math.cos(self.delta_rad + self.w1_rad))
        self.kae = math.cos(self.phi_rad - self.w1_rad) ** 2 / (math.cos(self.w1_rad) * math.cos(self.w1_rad + self.delta_rad) * (1 + root) ** 2)
        return self.kae

    def calc_Ka(self) -> float:
        root = math.sqrt(math.sin(self.phi_rad + self.delta_rad) * math.sin(self.phi_rad) / math.cos(self.delta_rad))
        self.Ka = math.cos(self.phi_rad) ** 2 / (math.cos(self.delta_rad) * (1 + root) ** 2)
        return self.Ka

    def calc_kpe(self) -> float:
        root = math.sqrt(math.sin(self.phi_rad + self.delta_rad) * math.sin(self.phi_rad - self.w1_rad) / math.cos(self.delta_rad + self.w1_rad))
        self.kpe = math.cos(self.phi_rad - self.w1_rad) ** 2 / (math.cos(self.w1_rad) * math.cos(self.w1_rad + self.delta_rad) * (1 - root) ** 2)
        return self.kpe

    def calc_Kp(self) -> float:
        root = math.sqrt(math.sin(self.phi_rad + self.delta_rad) * math.sin(self.phi_rad) / math.cos(self.delta_rad))
        self.Kp = math.cos(self.phi_rad) ** 2 / (math.cos(self.delta_rad) * (1 - root) ** 2)
        return self.Kp
