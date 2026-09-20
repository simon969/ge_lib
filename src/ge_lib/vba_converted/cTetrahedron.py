from dataclasses import dataclass, field
import math


@dataclass
class cTetrahedron:
    p0: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    p1: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    P2: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    P3: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    vol: float = 0.0
    G: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    @staticmethod
    def _cross(v1: list[float], v2: list[float]) -> list[float]:
        return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]

    @staticmethod
    def _dot(v1: list[float], v2: list[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def set_P0(self, xval: float, yval: float, zval: float) -> None:
        self.p0 = [xval, yval, zval]

    def set_P1(self, xval: float, yval: float, zval: float) -> None:
        self.p1 = [xval, yval, zval]

    def set_P2(self, xval: float, yval: float, zval: float) -> None:
        self.P2 = [xval, yval, zval]

    def set_P3(self, xval: float, yval: float, zval: float) -> None:
        self.P3 = [xval, yval, zval]

    def calc(self) -> None:
        a = [x - y for x, y in zip(self.p1, self.p0)]
        b = [x - y for x, y in zip(self.P2, self.p0)]
        c = [x - y for x, y in zip(self.P3, self.p0)]
        self.vol = abs(self._dot(a, self._cross(b, c))) / 6
        self.G = [(a[i] + b[i] + c[i]) / 4 for i in range(3)]
