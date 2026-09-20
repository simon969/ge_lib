from dataclasses import dataclass
import math


@dataclass
class cMohrsCircle:
    theta_rad: float = 0.0
    stressN: float = 0.0
    stressT: float = 0.0
    stressX: float = 0.0
    stressY: float = 0.0
    stressXY: float = 0.0

    def calc_stressN(self) -> float:
        self.stressN = (
            0.5 * (self.stressX + self.stressY)
            + 0.5 * (self.stressX - self.stressY) * math.cos(2 * self.theta_rad)
            + self.stressXY * math.sin(2 * self.theta_rad)
        )
        return self.stressN

    def calc_stressT(self) -> float:
        self.stressT = (
            -0.5 * (self.stressX - self.stressY) * math.sin(2 * self.theta_rad)
            + self.stressXY * math.cos(2 * self.theta_rad)
        )
        return self.stressT
