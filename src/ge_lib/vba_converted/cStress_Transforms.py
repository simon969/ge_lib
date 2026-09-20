from dataclasses import dataclass
import math


@dataclass
class cStress_Transforms:
    def calc_n(self, stress_x: float, stress_y: float, stress_xy: float, theta_rad: float) -> float:
        c = math.cos(theta_rad)
        s = math.sin(theta_rad)
        return 2 * c * stress_xy + stress_x * c ** 2 + stress_y * s ** 2

    def calc_s(self, stress_x: float, stress_y: float, stress_xy: float, theta_rad: float) -> float:
        c = math.cos(theta_rad)
        s = math.sin(theta_rad)
        return (1 - 2 * c) * stress_xy + stress_x * c * (1 / (c + s) - c) + stress_y * s * (1 / (c + s) - s)

    @staticmethod
    def calc_Ur(p1: float, p2: float, a: float, r: float, phi_rad: float, poiss: float, g: float) -> float:
        a2r = a ** 2 / r
        q1 = (p1 + p2) / (4 * g)
        q2 = (p1 - p2) / (4 * g)
        q3 = 4 * (1 - poiss) - a2r
        return q1 * a2r + q2 * a2r * q3 * math.cos(2 * phi_rad)

    @staticmethod
    def calc_pr(p1: float, p2: float, a: float, r: float, phi_rad: float) -> float:
        a2r2 = a ** 2 / r ** 2
        q1 = (p1 + p2) / 2
        q2 = (p1 - p2) / 2
        q3 = 1 - 4 * a2r2 + 3 * a2r2 ** 2
        return q1 * (1 - a2r2) + q2 * q3 * math.cos(2 * phi_rad)
