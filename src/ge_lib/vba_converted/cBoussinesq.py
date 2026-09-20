from dataclasses import dataclass
import math


@dataclass
class cBoussinesq:
    q: float = 0.0
    poisson: float = 0.0
    const_PI: float = 3.14159

    def line_sz(self, q: float, x: float, z: float) -> float:
        self.q = q
        p1 = (x ** 2 + z ** 2) ** 2
        return 2 * self.q / self.const_PI * p1 * z ** 3

    def line_sx(self, q: float, x: float, z: float) -> float:
        self.q = q
        p1 = (x ** 2 + z ** 2) ** 2
        return 2 * self.q / self.const_PI * p1 * x ** 2 * z

    def line_sxz(self, q: float, x: float, z: float) -> float:
        self.q = q
        p1 = (x ** 2 + z ** 2) ** 2
        return 2 * self.q / self.const_PI * p1 * x * z ** 2

    def point_sz(self, q: float, r: float, z: float) -> float:
        self.q = q
        p1 = (r / z) ** 2
        p2 = (1 / (1 + p1)) ** (5 / 2)
        return 3 * self.q / (2 * self.const_PI * z ** 2) * p2

    def point_sr(self, q: float, r: float, z: float, poisson: float) -> float:
        self.q = q
        self.poisson = poisson
        p1 = r ** 2 + z ** 2
        p2 = 3 * r ** 2 * z / (p1 ** (5 / 2))
        p3 = (1 - 2 * self.poisson) / (p1 + z * math.sqrt(p1))
        return self.q / (2 * self.const_PI) * (p2 - p3)

    def point_stheta(self, q: float, r: float, z: float, poisson: float) -> float:
        self.q = q
        self.poisson = poisson
        p1 = r ** 2 + z ** 2
        p2 = z / (p1 ** (3 / 2))
        p3 = 1 / (p1 + z * math.sqrt(p1))
        return self.q / (2 * self.const_PI) * (1 - 2 * self.poisson) * (p2 - p3)

    def point_srz(self, q: float, r: float, z: float) -> float:
        self.q = q
        p1 = r ** 2 + z ** 2
        p2 = (r * z ** 2) / (p1 ** (5 / 2))
        return 3 * self.q / (2 * self.const_PI) * p2

    def strip_sz(self, q: float, alpha_rad: float, beta_rad: float) -> float:
        self.q = q
        s1 = math.sin(beta_rad)
        c1 = math.cos(2 * alpha_rad + beta_rad)
        return self.q / self.const_PI * (beta_rad + s1 * c1)

    def strip_sx(self, q: float, alpha_rad: float, beta_rad: float) -> float:
        self.q = q
        s1 = math.sin(beta_rad)
        c1 = math.cos(2 * alpha_rad + beta_rad)
        return self.q / self.const_PI * (beta_rad - s1 * c1)

    def strip_sxz(self, q: float, alpha_rad: float, beta_rad: float) -> float:
        self.q = q
        s1 = math.sin(beta_rad)
        c1 = math.cos(beta_rad * (2 * alpha_rad + beta_rad))
        return self.q / self.const_PI * s1 * c1

    def linear_strip_sz(self, q: float, alpha_rad: float, beta_rad: float, x: float, c: float) -> float:
        self.q = q
        s1 = math.sin(2 * alpha_rad) / 2
        return self.q / self.const_PI * (x / c * beta_rad - s1)

    def linear_strip_sx(self, q: float, alpha_rad: float, beta_rad: float, x: float, z: float, c: float) -> float:
        self.q = q
        s1 = math.sin(2 * beta_rad) / 2
        p1 = (x ** 2 - z ** 2) / (x ** 2 - c ** 2 - z ** 2)
        p2 = z / c * math.log(p1)
        p3 = x / c * beta_rad
        return self.q / self.const_PI * (p3 + s1 - p2)

    def linear_strip_sxz(self, q: float, alpha_rad: float, beta_rad: float, z: float, c: float) -> float:
        self.q = q
        c1 = math.cos(2 * beta_rad)
        p1 = 2 * z / c * alpha_rad
        return self.q / self.const_PI * (1 + c1 - p1)

    def circle_sz(self, q: float, z: float, r: float) -> float:
        self.q = q
        p1 = 1 / (1 + (r / z) ** 2)
        return self.q * (1 - p1 ** (3 / 2))

    def circle_sr(self, q: float, z: float, r: float, poisson: float) -> float:
        self.q = q
        self.poisson = poisson
        p1 = 1 + (r / z) ** 2
        p2 = 2 * (1 + self.poisson) / math.sqrt(p1)
        p3 = 1 / (p1 ** (3 / 2))
        return self.q / 2 * ((1 + 2 * self.poisson) - p2 + p3)

    def circle_stheta(self, q: float, z: float, r: float, poisson: float) -> float:
        return self.circle_sr(q, z, r, poisson)

    def calc_Ir(self, M: float, N: float) -> float:
        M2 = M ** 2
        N2 = N ** 2
        mn2r = 2 * M * N * math.sqrt(M2 + N2 + 1)
        m2n2 = M2 + N2 + M2 * N2 + 1
        m2n21 = M2 + N2 - M2 * N2 + 1
        if abs(m2n21) < 1e-12:
            t1 = self.const_PI
        elif m2n21 < 0:
            t1 = math.atan(mn2r / m2n21) + self.const_PI
        else:
            t1 = math.atan(mn2r / m2n21)
        return 1 / (4 * self.const_PI) * ((mn2r / m2n2) * (M2 + N2 + 2) / (M2 + N2 + 1) + t1)

    def rectangle_sz(self, q: float, z: float, B: float, L: float) -> float:
        self.q = q
        if z == 0:
            Ir = 0.25
        else:
            M = B / z
            N = L / z
            Ir = self.calc_Ir(M, N)
        return q * Ir

    def calc_Ir3(self, M: float, N: float) -> float:
        v = M ** 2 + N ** 2 + 1
        v1 = (M * N) ** 2
        if abs(v1 - v) < 1e-12:
            t1 = self.const_PI
        elif v1 > v:
            t1 = math.atan((2 * M * N * math.sqrt(v)) / (v - v1)) + self.const_PI
        else:
            t1 = math.atan((2 * M * N * math.sqrt(v)) / (v - v1))
        return 1 / (4 * self.const_PI) * ((2 * M * N * math.sqrt(v)) / (v + v1) * (v + 1) / v + t1)

    def rectangle_sz3(self, q: float, z: float, B: float, L: float) -> float:
        self.q = q
        if z == 0:
            Ir = 0.25
        else:
            M = B / z
            N = L / z
            Ir = self.calc_Ir3(M, N)
        return q * Ir

    def calc_Ir2(self, z: float, a: float, B: float) -> float:
        r = math.sqrt(a ** 2 + B ** 2 + z ** 2)
        F = 2 * a * B * z * r / (z ** 2 * r ** 2 + a ** 2 * B ** 2)
        return 1 / (4 * self.const_PI) * (F * (1 + z ** 2 / r ** 2) + self.Asn(F))

    def rectangle_sz2(self, q: float, z: float, a: float, B: float) -> float:
        self.q = q
        if z == 0:
            Ir = 0.25
        else:
            Ir = self.calc_Ir2(z, a, B)
        return q * Ir

    def Asn(self, x: float) -> float:
        if abs(math.sqrt(1 - x * x)) <= 1e-12:
            return self.const_PI / 2
        return math.atan(x / math.sqrt(1 - x * x))
